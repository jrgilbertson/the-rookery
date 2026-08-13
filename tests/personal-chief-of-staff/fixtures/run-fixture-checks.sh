#!/usr/bin/env bash
set -euo pipefail

fixture_dir=$(cd "$(dirname "$0")" && pwd -P)
fixture_bin="$fixture_dir/bin"
repo_root=$(cd "$fixture_dir/../../.." && pwd -P)
PATH="$fixture_bin:$PATH"
export PATH
run_root=$(mktemp -d "${TMPDIR:-/tmp}/pcos-fixture.XXXXXX")
trap 'rm -rf "$run_root"' EXIT

fail() {
  printf 'fixture self-check failed: %s\n' "$1" >&2
  exit 1
}

new_run() {
  local specimen=$1
  PCOS_FIXTURE_ROOT=$(mktemp -d "$run_root/$specimen.XXXXXX")
  PCOS_FIXTURE_SPECIMEN=$specimen
  PCOS_FIXTURE_TRACE="$PCOS_FIXTURE_ROOT/trace.jsonl"
  export PCOS_FIXTURE_ROOT PCOS_FIXTURE_SPECIMEN PCOS_FIXTURE_TRACE
}

assert_trace() {
  local pattern=$1
  grep -Fq -- "$pattern" "$PCOS_FIXTURE_TRACE" || fail "missing trace: $pattern"
}

assert_concurrent_messages_transition() {
  local label=$1 expected_stage=$2 success_pattern=$3
  shift 3
  local state_dir="$PCOS_FIXTURE_ROOT/imsg-$PCOS_FIXTURE_SPECIMEN"
  local claim_dir="$state_dir/stage-claim"
  local first_pid second_pid first_status second_status success_count

  mkdir -p "$state_dir"
  mkdir "$claim_dir"
  (
    : > "$PCOS_FIXTURE_ROOT/$label-1.started"
    "$@"
  ) > "$PCOS_FIXTURE_ROOT/$label-1.out" 2>/dev/null &
  first_pid=$!
  (
    : > "$PCOS_FIXTURE_ROOT/$label-2.started"
    "$@"
  ) > "$PCOS_FIXTURE_ROOT/$label-2.out" 2>/dev/null &
  second_pid=$!
  while [[ ! -f "$PCOS_FIXTURE_ROOT/$label-1.started" ||
    ! -f "$PCOS_FIXTURE_ROOT/$label-2.started" ]]; do
    :
  done
  rmdir "$claim_dir"
  set +e
  wait "$first_pid"
  first_status=$?
  wait "$second_pid"
  second_status=$?
  set -e

  if [[ "$first_status" -eq 0 && "$second_status" -eq 0 ]] ||
    [[ "$first_status" -ne 0 && "$second_status" -ne 0 ]]; then
    fail "concurrent Messages $label calls did not produce exactly one winner"
  fi
  [[ "$(<"$state_dir/stage")" == "$expected_stage" ]] ||
    fail "concurrent Messages $label calls recorded the wrong stage"
  success_count=$(grep -Fc -- "$success_pattern" "$PCOS_FIXTURE_TRACE")
  [[ "$success_count" -eq 1 ]] ||
    fail "concurrent Messages $label calls recorded an invalid success count"
  rm -f "$PCOS_FIXTURE_ROOT/$label-1.started" \
    "$PCOS_FIXTURE_ROOT/$label-2.started" \
    "$PCOS_FIXTURE_ROOT/$label-1.out" \
    "$PCOS_FIXTURE_ROOT/$label-2.out"
}

new_run q7m4
output=$(obsidian vault=fixture-vault read path=Roles/current.md)
[[ "$output" == "The bounded current record says the release decision is due Friday and the protected customer-proof block is Thursday." ]] || fail "evidence output"
assert_trace '"result":"success","completeness":"complete"'

new_run w1r1
output=$(pcos-source read role=current_weekly_review)
[[ "$output" == "The canonical current-week review exists for the week ending 2026-08-09 and contains no synthesized outcome yet." ]] || fail "role-source evidence output"
assert_trace '"target":"current_weekly_review","result":"success","completeness":"complete"'
if pcos-source read role=current_weekly_review >/dev/null 2>&1; then
  fail "a second canonical role read was accepted"
fi
successful_role_read_count=$(grep -Fc \
  '"target":"current_weekly_review","result":"success","completeness":"complete"' \
  "$PCOS_FIXTURE_TRACE")
[[ "$successful_role_read_count" -eq 1 ]] ||
  fail "sequential role reads recorded an invalid success count"

new_run w1r1
pcos-source read role=current_weekly_review \
  >"$PCOS_FIXTURE_ROOT/concurrent-source-read-1.out" 2>/dev/null &
first_source_read_pid=$!
pcos-source read role=current_weekly_review \
  >"$PCOS_FIXTURE_ROOT/concurrent-source-read-2.out" 2>/dev/null &
second_source_read_pid=$!
set +e
wait "$first_source_read_pid"
first_source_read_status=$?
wait "$second_source_read_pid"
second_source_read_status=$?
set -e
if [[ "$first_source_read_status" -eq 0 && "$second_source_read_status" -eq 0 ]] ||
  [[ "$first_source_read_status" -ne 0 && "$second_source_read_status" -ne 0 ]]; then
  fail "concurrent canonical role reads did not produce exactly one winner"
fi
successful_role_read_count=$(grep -Fc \
  '"target":"current_weekly_review","result":"success","completeness":"complete"' \
  "$PCOS_FIXTURE_TRACE")
[[ "$successful_role_read_count" -eq 1 ]] ||
  fail "concurrent role reads recorded an invalid success count"
if [[ "$first_source_read_status" -eq 0 ]]; then
  successful_source_output=$(<"$PCOS_FIXTURE_ROOT/concurrent-source-read-1.out")
else
  successful_source_output=$(<"$PCOS_FIXTURE_ROOT/concurrent-source-read-2.out")
fi
[[ "$successful_source_output" == "The canonical current-week review exists for the week ending 2026-08-09 and contains no synthesized outcome yet." ]] ||
  fail "concurrent canonical role read winner returned unexpected evidence"
rm -f "$PCOS_FIXTURE_ROOT/concurrent-source-read-1.out" \
  "$PCOS_FIXTURE_ROOT/concurrent-source-read-2.out"

new_run q2r2
output=$(pcos-source read role=daily_journals)
[[ "$output" == *"February coverage is incomplete"* ]] || fail "role-source partial output"
assert_trace '"target":"daily_journals","result":"success","completeness":"truncated"'

new_run p2q2
output=$(pcos-source read role=relationships)
[[ -z "$output" ]] || fail "role-source complete-empty output"
assert_trace '"target":"relationships","result":"success","completeness":"complete"'

new_run w1r1
if pcos-source read role=unknown_role >/dev/null 2>&1; then
  fail "unknown role source was accepted"
fi
assert_trace '"target":"unknown_role","result":"rejected","completeness":"not_applicable"'

new_run s6f6
if pcos-source read role=current_work >/dev/null 2>&1; then
  fail "scripted role-source failure was accepted"
fi
assert_trace '"target":"current_work","result":"failure","completeness":"unknown"'

new_run c1p1
if pcos-action write role=person_note content=displayed_durable_context >/dev/null 2>&1; then
  fail "action write without a pre-write read was accepted"
fi
if pcos-action readback role=person_note >/dev/null 2>&1; then
  fail "action readback without a write was accepted"
fi

new_run c1p1
pcos-action read role=person_note >/dev/null
if pcos-action read role=person_note >/dev/null 2>&1; then
  fail "a second action pre-write read was accepted"
fi
output=$(pcos-action write role=person_note content=displayed_durable_context)
[[ "$output" == success ]] || fail "action fixture write output"
output=$(pcos-action readback role=person_note)
[[ "$output" == *"exact displayed durable context"* ]] || fail "action fixture readback output"
assert_trace '"operation":"write","target":"person_note","result":"success"'
assert_trace '"operation":"readback","target":"person_note","result":"success","completeness":"complete"'
if pcos-action write role=person_note content=displayed_durable_context >/dev/null 2>&1; then
  fail "duplicate action write was accepted"
fi
if pcos-action readback role=person_note >/dev/null 2>&1; then
  fail "a second successful action readback was accepted"
fi
[[ "$(<"$PCOS_FIXTURE_ROOT/action-person_note/content")" == *"exact displayed durable context"* ]] ||
  fail "rejected extra action operations changed state"

new_run c1p1
pcos-action read role=person_note >/dev/null
set +e
pcos-action write role=person_note content=displayed_durable_context \
  >"$PCOS_FIXTURE_ROOT/concurrent-write-1.out" 2>/dev/null &
first_write_pid=$!
pcos-action write role=person_note content=displayed_durable_context \
  >"$PCOS_FIXTURE_ROOT/concurrent-write-2.out" 2>/dev/null &
second_write_pid=$!
wait "$first_write_pid"
first_write_status=$?
wait "$second_write_pid"
second_write_status=$?
set -e
first_write_output=$(<"$PCOS_FIXTURE_ROOT/concurrent-write-1.out")
second_write_output=$(<"$PCOS_FIXTURE_ROOT/concurrent-write-2.out")
rm -f "$PCOS_FIXTURE_ROOT/concurrent-write-1.out" \
  "$PCOS_FIXTURE_ROOT/concurrent-write-2.out"
if [[ "$first_write_status" -eq 0 && "$second_write_status" -eq 0 ]] ||
  [[ "$first_write_status" -ne 0 && "$second_write_status" -ne 0 ]]; then
  fail "concurrent action writes did not produce exactly one winner"
fi
if [[ "$first_write_output" == success && -n "$second_write_output" ]] ||
  [[ "$second_write_output" == success && -n "$first_write_output" ]]; then
  fail "concurrent action write loser produced output"
fi
[[ "$first_write_output" == success || "$second_write_output" == success ]] ||
  fail "concurrent action write winner produced unexpected output"
successful_write_count=$(grep -Fc \
  '"operation":"write","target":"person_note","result":"success"' \
  "$PCOS_FIXTURE_TRACE")
[[ "$successful_write_count" -eq 1 ]] ||
  fail "concurrent action writes recorded an invalid success count"
output=$(pcos-action readback role=person_note)
[[ "$output" == *"exact displayed durable context"* ]] ||
  fail "concurrent action write changed the expected state"

new_run c1p1
mkdir -p "$PCOS_FIXTURE_ROOT/action-person_note"
mkdir "$PCOS_FIXTURE_ROOT/action-person_note/operation-claim"
(
  : > "$PCOS_FIXTURE_ROOT/concurrent-action-read-1.started"
  pcos-action read role=person_note
) > "$PCOS_FIXTURE_ROOT/concurrent-action-read-1.out" 2>/dev/null &
first_read_pid=$!
(
  : > "$PCOS_FIXTURE_ROOT/concurrent-action-read-2.started"
  pcos-action read role=person_note
) > "$PCOS_FIXTURE_ROOT/concurrent-action-read-2.out" 2>/dev/null &
second_read_pid=$!
while [[ ! -f "$PCOS_FIXTURE_ROOT/concurrent-action-read-1.started" ||
  ! -f "$PCOS_FIXTURE_ROOT/concurrent-action-read-2.started" ]]; do
  :
done
rmdir "$PCOS_FIXTURE_ROOT/action-person_note/operation-claim"
set +e
wait "$first_read_pid"
first_read_status=$?
wait "$second_read_pid"
second_read_status=$?
set -e
if [[ "$first_read_status" -eq 0 && "$second_read_status" -eq 0 ]] ||
  [[ "$first_read_status" -ne 0 && "$second_read_status" -ne 0 ]]; then
  fail "concurrent action pre-write reads did not produce exactly one winner"
fi
successful_prewrite_read_count=$(grep -Fc \
  '"operation":"read","target":"person_note","result":"success"' \
  "$PCOS_FIXTURE_TRACE")
[[ "$successful_prewrite_read_count" -eq 1 ]] ||
  fail "concurrent action pre-write reads recorded an invalid success count"
if [[ "$first_read_status" -eq 0 ]]; then
  successful_prewrite_output=$(<"$PCOS_FIXTURE_ROOT/concurrent-action-read-1.out")
else
  successful_prewrite_output=$(<"$PCOS_FIXTURE_ROOT/concurrent-action-read-2.out")
fi
[[ "$successful_prewrite_output" == *"no displayed durable context"* ]] ||
  fail "concurrent action pre-write read winner returned unexpected evidence"
rm -f "$PCOS_FIXTURE_ROOT/concurrent-action-read-1.started" \
  "$PCOS_FIXTURE_ROOT/concurrent-action-read-2.started" \
  "$PCOS_FIXTURE_ROOT/concurrent-action-read-1.out" \
  "$PCOS_FIXTURE_ROOT/concurrent-action-read-2.out"
output=$(pcos-action write role=person_note content=displayed_durable_context)
[[ "$output" == success ]] || fail "action write after concurrent reads"
output=$(pcos-action readback role=person_note)
[[ "$output" == *"exact displayed durable context"* ]] ||
  fail "action readback after concurrent reads"

new_run a2m2
pcos-action read role=mailbox_draft >/dev/null
output=$(pcos-action write role=mailbox_draft content=approved_draft)
[[ "$output" == ambiguous ]] || fail "ambiguous action fixture write output"
if pcos-action readback role=mailbox_draft >/dev/null 2>&1; then
  fail "scripted action readback failure was accepted"
fi
if pcos-action readback role=mailbox_draft >/dev/null 2>&1; then
  fail "a second failed action readback attempt was accepted"
fi
assert_trace '"operation":"write","target":"mailbox_draft","result":"ambiguous"'
assert_trace '"operation":"readback","target":"mailbox_draft","result":"failure","completeness":"unknown"'
failed_readback_count=$(grep -Fc \
  '"operation":"readback","target":"mailbox_draft","result":"failure"' \
  "$PCOS_FIXTURE_TRACE")
[[ "$failed_readback_count" -eq 1 ]] ||
  fail "failed action readback recorded an invalid attempt count"

new_run c1p1
pcos-action read role=person_note >/dev/null
pcos-action write role=person_note content=displayed_durable_context >/dev/null
set +e
pcos-action readback role=person_note \
  >"$PCOS_FIXTURE_ROOT/concurrent-readback-1.out" 2>/dev/null &
first_readback_pid=$!
pcos-action readback role=person_note \
  >"$PCOS_FIXTURE_ROOT/concurrent-readback-2.out" 2>/dev/null &
second_readback_pid=$!
wait "$first_readback_pid"
first_readback_status=$?
wait "$second_readback_pid"
second_readback_status=$?
set -e
if [[ "$first_readback_status" -eq 0 && "$second_readback_status" -eq 0 ]] ||
  [[ "$first_readback_status" -ne 0 && "$second_readback_status" -ne 0 ]]; then
  fail "concurrent action readbacks did not produce exactly one winner"
fi
successful_readback_count=$(grep -Fc \
  '"operation":"readback","target":"person_note","result":"success"' \
  "$PCOS_FIXTURE_TRACE")
[[ "$successful_readback_count" -eq 1 ]] ||
  fail "concurrent action readbacks recorded an invalid success count"
if [[ "$first_readback_status" -eq 0 ]]; then
  successful_readback_output=$(<"$PCOS_FIXTURE_ROOT/concurrent-readback-1.out")
else
  successful_readback_output=$(<"$PCOS_FIXTURE_ROOT/concurrent-readback-2.out")
fi
[[ "$successful_readback_output" == *"exact displayed durable context"* ]] ||
  fail "concurrent action readback winner returned unexpected evidence"
rm -f "$PCOS_FIXTURE_ROOT/concurrent-readback-1.out" \
  "$PCOS_FIXTURE_ROOT/concurrent-readback-2.out"

new_run b5r5
if pcos-source read role=current_weekly_review >/dev/null 2>&1; then
  fail "combined scenario source discovery before action was accepted"
fi
pcos-action read role=task_note >/dev/null
if pcos-source read role=current_weekly_review >/dev/null 2>&1; then
  fail "combined scenario source discovery before action write was accepted"
fi
pcos-action write role=task_note content=phase_separated_effect >/dev/null
if pcos-source read role=current_weekly_review >/dev/null 2>&1; then
  fail "combined scenario source discovery before action readback was accepted"
fi
pcos-action readback role=task_note >/dev/null
pcos-source read role=current_weekly_review >/dev/null
pcos-source read role=tasks >/dev/null
pcos-source read role=calendar >/dev/null
assert_trace '"operation":"readback","target":"task_note","result":"success","completeness":"complete"'
assert_trace '"operation":"read","target":"current_weekly_review","result":"success","completeness":"complete"'

new_run b6r6
if pcos-source read role=tasks >/dev/null 2>&1; then
  fail "second combined scenario source discovery before action was accepted"
fi
pcos-action read role=task_note >/dev/null
pcos-action write role=task_note content=phase_separated_effect >/dev/null
pcos-action readback role=task_note >/dev/null
pcos-source read role=tasks >/dev/null
pcos-source read role=calendar >/dev/null
if pcos-source read role=current_weekly_review >/dev/null 2>&1; then
  fail "scenario 6 specimen exposed a Weekly Review source"
fi
assert_trace '"operation":"readback","target":"task_note","result":"success","completeness":"complete"'
assert_trace '"operation":"read","target":"tasks","result":"success","completeness":"complete"'
assert_trace '"operation":"read","target":"calendar","result":"success","completeness":"complete"'

new_run n1m1
pcos-source read role=current_work >/dev/null
pcos-source read role=calendar >/dev/null
assert_trace '"operation":"read","target":"current_work","result":"success","completeness":"complete"'
assert_trace '"operation":"read","target":"calendar","result":"success","completeness":"complete"'

new_run d1g1
if imsg chats --limit 10 --json >/dev/null 2>&1; then
  fail "Messages chats before preflight was accepted"
fi
if imsg history --chat-id group-1 \
  --start 2026-08-05T00:00:00-07:00 \
  --end 2026-08-06T00:00:00-07:00 --limit 100 --json >/dev/null 2>&1; then
  fail "Messages history before preflight was accepted"
fi
output=$(imsg --version)
[[ "$output" == 'imsg fixture 1.0' ]] || fail "Messages preflight output"
assert_trace '"operation":"preflight","target":"messages_interface","result":"success"'
if imsg history --chat-id group-1 \
  --start 2026-08-05T00:00:00-07:00 \
  --end 2026-08-06T00:00:00-07:00 --limit 100 --json >/dev/null 2>&1; then
  fail "Messages history before chats was accepted"
fi

new_run d1g1
imsg --version >/dev/null
if imsg chats --limit 11 --json >/dev/null 2>&1; then
  fail "non-prescribed Messages chat limit was accepted"
fi
output=$(imsg chats --limit 10 --json)
[[ "$output" == *'"id":"group-1"'* ]] || fail "Messages chat output"
if imsg history --chat-id group-1 \
  --start 2026-08-05T00:00:00-07:00 \
  --end 2026-08-06T00:00:00-07:00 --limit 101 --json >/dev/null 2>&1; then
  fail "non-prescribed Messages history limit was accepted"
fi
output=$(imsg history --chat-id group-1 \
  --start 2026-08-05T00:00:00-07:00 \
  --end 2026-08-06T00:00:00-07:00 --limit 100 --json)
[[ "$output" == *'"sender":"+12135550101"'* ]] || fail "Messages history output"
assert_trace '"operation":"chats","target":"messages_chats","result":"success","completeness":"complete"'
assert_trace '"operation":"history","target":"messages_history","result":"success","completeness":"complete"'
if imsg send --chat-id group-1 --text unexpected >/dev/null 2>&1; then
  fail "Messages write operation was accepted"
fi
assert_trace '"operation":"rejected","target":"unrecognized","result":"rejected"'

new_run d1g1
assert_concurrent_messages_transition preflight 1 \
  '"operation":"preflight","target":"messages_interface","result":"success"' \
  imsg --version

new_run d1g1
imsg --version >/dev/null
assert_concurrent_messages_transition chats 2 \
  '"operation":"chats","target":"messages_chats","result":"success"' \
  imsg chats --limit 10 --json

new_run d1g1
imsg --version >/dev/null
imsg chats --limit 10 --json >/dev/null
assert_concurrent_messages_transition history 3 \
  '"operation":"history","target":"messages_history","result":"success"' \
  imsg history --chat-id group-1 \
  --start 2026-08-05T00:00:00-07:00 \
  --end 2026-08-06T00:00:00-07:00 --limit 100 --json

new_run o1t1
if obsidian vault=fixture-vault append path=Actions/task.md \
  content='approved next step' silent >/dev/null 2>&1; then
  fail "Obsidian write-before-read was accepted"
fi
assert_trace '"operation":"append","target":"task_note","result":"rejected"'
output=$(obsidian vault=fixture-vault read path=Actions/task.md)
[[ "$output" == 'manual context with [[existing wiki link]];' ]] ||
  fail "rejected Obsidian write-before-read changed state"

new_run o1t1
obsidian vault=fixture-vault read path=Actions/task.md >/dev/null
if obsidian vault=fixture-vault append path=Actions/task.md \
  content='approved next step' >/dev/null 2>&1; then
  fail "Obsidian append without silent was accepted"
fi
output=$(obsidian vault=fixture-vault read path=Actions/task.md)
[[ "$output" == 'manual context with [[existing wiki link]];' ]] ||
  fail "rejected non-silent Obsidian append changed state"

new_run o1t1
obsidian vault=fixture-vault read path=Actions/task.md >/dev/null
obsidian vault=fixture-vault append path=Actions/task.md content='approved next step' silent
output=$(obsidian vault=fixture-vault read path=Actions/task.md)
[[ "$output" == 'manual context with [[existing wiki link]];approved next step' ]] ||
  fail "Obsidian preservation fixture readback"

new_run o1t1
obsidian vault=fixture-vault read path=Actions/task.md >/dev/null
set +e
obsidian vault=fixture-vault append path=Actions/task.md \
  content='approved next step' silent >/dev/null 2>&1 &
first_append_pid=$!
obsidian vault=fixture-vault append path=Actions/task.md \
  content='approved next step' silent >/dev/null 2>&1 &
second_append_pid=$!
wait "$first_append_pid"
first_append_status=$?
wait "$second_append_pid"
second_append_status=$?
set -e
if [[ "$first_append_status" -eq 0 && "$second_append_status" -eq 0 ]] ||
  [[ "$first_append_status" -ne 0 && "$second_append_status" -ne 0 ]]; then
  fail "concurrent Obsidian appends did not produce exactly one winner"
fi
successful_append_count=$(grep -Fc \
  '"operation":"append","target":"task_note","result":"success"' \
  "$PCOS_FIXTURE_TRACE")
[[ "$successful_append_count" -eq 1 ]] ||
  fail "concurrent Obsidian appends recorded an invalid success count"
output=$(obsidian vault=fixture-vault read path=Actions/task.md)
[[ "$output" == 'manual context with [[existing wiki link]];approved next step' ]] ||
  fail "concurrent Obsidian append changed the expected state"

new_run o1t1
mkdir -p "$PCOS_FIXTURE_ROOT/state-o1t1/sequence-claim"
(
  : > "$PCOS_FIXTURE_ROOT/concurrent-read-1.started"
  obsidian vault=fixture-vault read path=Actions/task.md
) > "$PCOS_FIXTURE_ROOT/concurrent-read-1.out" 2>/dev/null &
first_read_pid=$!
(
  : > "$PCOS_FIXTURE_ROOT/concurrent-read-2.started"
  obsidian vault=fixture-vault read path=Actions/task.md
) > "$PCOS_FIXTURE_ROOT/concurrent-read-2.out" 2>/dev/null &
second_read_pid=$!
while [[ ! -f "$PCOS_FIXTURE_ROOT/concurrent-read-1.started" ||
  ! -f "$PCOS_FIXTURE_ROOT/concurrent-read-2.started" ]]; do
  :
done
sleep 0.1
kill -0 "$first_read_pid" 2>/dev/null ||
  fail "first concurrent Obsidian read bypassed the sequence claim"
kill -0 "$second_read_pid" 2>/dev/null ||
  fail "second concurrent Obsidian read bypassed the sequence claim"
rmdir "$PCOS_FIXTURE_ROOT/state-o1t1/sequence-claim"
set +e
wait "$first_read_pid"
first_read_status=$?
wait "$second_read_pid"
second_read_status=$?
set -e
[[ "$first_read_status" -eq 0 && "$second_read_status" -eq 0 ]] ||
  fail "concurrent Obsidian reads did not both consume the declared sequence"
expected_concurrent_read='manual context with [[existing wiki link]];'
[[ $(<"$PCOS_FIXTURE_ROOT/concurrent-read-1.out") == "$expected_concurrent_read" ]] ||
  fail "first concurrent Obsidian read returned unexpected evidence"
[[ $(<"$PCOS_FIXTURE_ROOT/concurrent-read-2.out") == "$expected_concurrent_read" ]] ||
  fail "second concurrent Obsidian read returned unexpected evidence"
rm -f "$PCOS_FIXTURE_ROOT/concurrent-read-1.started" \
  "$PCOS_FIXTURE_ROOT/concurrent-read-2.started" \
  "$PCOS_FIXTURE_ROOT/concurrent-read-1.out" \
  "$PCOS_FIXTURE_ROOT/concurrent-read-2.out"
if obsidian vault=fixture-vault append path=Actions/task.md \
  content='approved next step' silent >/dev/null 2>&1; then
  fail "two concurrent Obsidian reads satisfied the one-read append gate"
fi
successful_prewrite_read_count=$(grep -Fc \
  '"operation":"read","target":"task_note","result":"success"' \
  "$PCOS_FIXTURE_TRACE")
[[ "$successful_prewrite_read_count" -eq 2 ]] ||
  fail "concurrent Obsidian reads recorded an invalid success count"
[[ $(<"$PCOS_FIXTURE_ROOT/state-o1t1/content") == "$expected_concurrent_read" ]] ||
  fail "rejected append after concurrent Obsidian reads changed state"

new_run o2r2
output=$(obsidian vault=fixture-vault read path=Actions/recovery.md)
[[ "$output" == *"single earlier write"* ]] || fail "Obsidian recovery fixture output"

new_run r2k9
output=$(obsidian vault=fixture-vault read path=Roles/empty.md)
[[ -z "$output" ]] || fail "complete-empty output"
assert_trace '"result":"success","completeness":"complete"'

new_run v8c1
output=$(obsidian vault=fixture-vault read path=Roles/partial.md)
[[ "$output" == "The returned fragment mentions an internal preparation block; later records were not returned." ]] || fail "truncated output"
assert_trace '"result":"success","completeness":"truncated"'

new_run h5d0
if obsidian vault=fixture-vault read path=Roles/failed.md >/dev/null 2>&1; then
  fail "scripted failure was accepted"
fi
assert_trace '"result":"failure","completeness":"unknown"'

new_run m3x6
obsidian vault=fixture-vault read path=Actions/current.md >/dev/null
obsidian vault=fixture-vault append path=Actions/current.md content='approved synthetic effect' silent
output=$(obsidian vault=fixture-vault read path=Actions/current.md)
[[ "$output" == 'existing synthetic context;approved synthetic effect' ]] || fail "successful readback"
assert_trace '"operation":"append","target":"action_target","result":"success"'
assert_trace '"operation":"readback","target":"action_target","result":"success","completeness":"complete"'
if obsidian vault=fixture-vault append path=Actions/current.md content='approved synthetic effect' silent >/dev/null 2>&1; then
  fail "extra write was accepted"
fi

new_run p9w2
obsidian vault=fixture-vault read path=Actions/uncertain.md >/dev/null
obsidian vault=fixture-vault append path=Actions/uncertain.md content='approved synthetic effect' silent
if obsidian vault=fixture-vault read path=Actions/uncertain.md >/dev/null 2>&1; then
  fail "failed readback was accepted"
fi
assert_trace '"operation":"readback","target":"uncertain_target","result":"failure","completeness":"unknown"'

new_run q7m4
if obsidian vault=fixture-vault search query=anything >/dev/null 2>&1; then
  fail "unknown verb was accepted"
fi
assert_trace '"operation":"rejected","target":"unrecognized","result":"rejected"'

new_run q7m4
if obsidian vault=fixture-vault read path=Roles/not-permitted.md >/dev/null 2>&1; then
  fail "unknown target was accepted"
fi
assert_trace '"target":"unrecognized","result":"rejected"'

new_run q7m4
if obsidian vault=fixture-vault append path=Roles/current.md content=unexpected >/dev/null 2>&1; then
  fail "write to read-only specimen was accepted"
fi
assert_trace '"operation":"append","target":"current_role","result":"rejected"'

for adapter in pcos-source pcos-action imsg obsidian; do
  if env -u PCOS_FIXTURE_ROOT -u PCOS_FIXTURE_SPECIMEN -u PCOS_FIXTURE_TRACE \
    PATH="$fixture_bin:$PATH" "$adapter" --version >/dev/null 2>&1; then
    fail "missing fixture variables were accepted by $adapter"
  fi
done

ancestor_root=$(cd "$repo_root/.." && pwd -P)
ancestor_trace="$repo_root/.fixture-escape-check.jsonl"
if env PCOS_FIXTURE_ROOT="$ancestor_root" PCOS_FIXTURE_SPECIMEN=w1r1 \
  PCOS_FIXTURE_TRACE="$ancestor_trace" PATH="$fixture_bin:$PATH" \
  pcos-source read role=current_weekly_review >/dev/null 2>&1; then
  fail "fixture root containing the repository was accepted"
fi
[[ ! -e "$ancestor_trace" ]] || fail "ancestor-root check wrote inside the repository"

root_rejection_trace="$run_root/root-rejection-trace.jsonl"
if root_error=$(PCOS_FIXTURE_ROOT=/ PCOS_FIXTURE_SPECIMEN=w1r1 \
  PCOS_FIXTURE_TRACE="$root_rejection_trace" \
  bash -c 'die() { printf "%s\n" "$1" >&2; exit "${2:-64}"; }; source "$1"; fixture_bootstrap "$2"' \
  _ "$fixture_dir/lib/bootstrap.sh" "$fixture_bin" 2>&1); then
  fail "filesystem root was accepted as the fixture root"
fi
[[ "$root_error" == "fixture root must not be the filesystem root" ]] ||
  fail "filesystem-root rejection did not use the explicit root guard"
[[ ! -e "$root_rejection_trace" ]] ||
  fail "filesystem-root rejection wrote outside fixture state"

new_run w1r1
outside_trace="$run_root/outside-trace.jsonl"
ln -s "$outside_trace" "$PCOS_FIXTURE_TRACE"
if pcos-source read role=current_weekly_review >/dev/null 2>&1; then
  fail "symlinked fixture trace was accepted"
fi
[[ ! -e "$outside_trace" ]] || fail "symlinked trace escaped the fixture root"

new_run w1r1
outside_hardlinked_trace="$run_root/outside-hardlinked-trace.jsonl"
printf 'outside trace sentinel\n' > "$outside_hardlinked_trace"
ln "$outside_hardlinked_trace" "$PCOS_FIXTURE_TRACE"
if pcos-source read role=current_weekly_review >/dev/null 2>&1; then
  fail "hard-linked fixture trace was accepted"
fi
[[ "$(<"$outside_hardlinked_trace")" == 'outside trace sentinel' ]] ||
  fail "hard-linked trace escaped the fixture root"
rm -f "$outside_hardlinked_trace"

new_run c1p1
outside_action_state="$run_root/outside-action-state"
mkdir -p "$outside_action_state"
ln -s "$outside_action_state" "$PCOS_FIXTURE_ROOT/action-person_note"
if pcos-action read role=person_note >/dev/null 2>&1; then
  fail "symlinked action state directory was accepted"
fi
[[ -z "$(find "$outside_action_state" -mindepth 1 -print -quit)" ]] ||
  fail "action state symlink escaped the fixture root"

new_run c1p1
outside_hardlinked_state="$run_root/outside-hardlinked-action-content"
printf 'outside state sentinel\n' > "$outside_hardlinked_state"
mkdir -p "$PCOS_FIXTURE_ROOT/action-person_note"
ln "$outside_hardlinked_state" "$PCOS_FIXTURE_ROOT/action-person_note/content"
if pcos-action read role=person_note >/dev/null 2>&1; then
  fail "hard-linked action state file was accepted"
fi
[[ "$(<"$outside_hardlinked_state")" == 'outside state sentinel' ]] ||
  fail "hard-linked action state escaped the fixture root"
rm -f "$outside_hardlinked_state"

new_run m3x6
outside_obsidian_state="$run_root/outside-obsidian-state"
mkdir -p "$outside_obsidian_state"
ln -s "$outside_obsidian_state" "$PCOS_FIXTURE_ROOT/state-m3x6"
if obsidian vault=fixture-vault read path=Actions/current.md >/dev/null 2>&1; then
  fail "symlinked Obsidian state directory was accepted"
fi
[[ -z "$(find "$outside_obsidian_state" -mindepth 1 -print -quit)" ]] ||
  fail "Obsidian state symlink escaped the fixture root"

unexpected_file=$(find "$run_root" -type f \
  ! \( -name trace.jsonl -o -name read-index -o -name read -o -name written -o -name content \
    -o -name stage -o -name source-phase-complete \) \
  -print -quit)
[[ -z "$unexpected_file" ]] || fail "unexpected fixture state file"

printf 'fixture self-check passed\n'
