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

new_run q7m4
output=$(obsidian vault=fixture-vault read path=Roles/current.md)
[[ "$output" == "The bounded current record says the release decision is due Friday and the protected customer-proof block is Thursday." ]] || fail "evidence output"
assert_trace '"result":"success","completeness":"complete"'

new_run w1r1
output=$(pcos-source read role=current_weekly_review)
[[ "$output" == "The canonical current-week review exists for the week ending 2026-08-09 and contains no synthesized outcome yet." ]] || fail "role-source evidence output"
assert_trace '"target":"current_weekly_review","result":"success","completeness":"complete"'

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
output=$(pcos-action write role=person_note content=displayed_durable_context)
[[ "$output" == success ]] || fail "action fixture write output"
output=$(pcos-action readback role=person_note)
[[ "$output" == *"exact displayed durable context"* ]] || fail "action fixture readback output"
assert_trace '"operation":"write","target":"person_note","result":"success"'
assert_trace '"operation":"readback","target":"person_note","result":"success","completeness":"complete"'
if pcos-action write role=person_note content=displayed_durable_context >/dev/null 2>&1; then
  fail "duplicate action write was accepted"
fi
output=$(pcos-action readback role=person_note)
[[ "$output" == *"exact displayed durable context"* ]] ||
  fail "duplicate action write changed state"

new_run a2m2
pcos-action read role=mailbox_draft >/dev/null
output=$(pcos-action write role=mailbox_draft content=approved_draft)
[[ "$output" == ambiguous ]] || fail "ambiguous action fixture write output"
if pcos-action readback role=mailbox_draft >/dev/null 2>&1; then
  fail "scripted action readback failure was accepted"
fi
assert_trace '"operation":"write","target":"mailbox_draft","result":"ambiguous"'
assert_trace '"operation":"readback","target":"mailbox_draft","result":"failure","completeness":"unknown"'

new_run b5r5
pcos-action read role=task_note >/dev/null
pcos-action write role=task_note content=phase_separated_effect >/dev/null
pcos-action readback role=task_note >/dev/null
pcos-source read role=current_weekly_review >/dev/null
pcos-source read role=tasks >/dev/null
pcos-source read role=calendar >/dev/null
assert_trace '"operation":"readback","target":"task_note","result":"success","completeness":"complete"'
assert_trace '"operation":"read","target":"current_weekly_review","result":"success","completeness":"complete"'

new_run n1m1
pcos-source read role=current_work >/dev/null
pcos-source read role=calendar >/dev/null
assert_trace '"operation":"read","target":"current_work","result":"success","completeness":"complete"'
assert_trace '"operation":"read","target":"calendar","result":"success","completeness":"complete"'

new_run d1g1
output=$(imsg --version)
[[ "$output" == 'imsg fixture 1.0' ]] || fail "Messages preflight output"
assert_trace '"operation":"preflight","target":"messages_interface","result":"success"'
output=$(imsg chats --limit 10 --json)
[[ "$output" == *'"id":"group-1"'* ]] || fail "Messages chat output"
output=$(imsg history --chat-id group-1 \
  --start 2026-08-05T00:00:00-07:00 \
  --end 2026-08-06T00:00:00-07:00 --limit 100 --json)
[[ "$output" == *'"sender":"+12135550101"'* ]] || fail "Messages history output"
assert_trace '"operation":"chats","target":"messages_chats","result":"success","completeness":"complete"'
assert_trace '"operation":"history","target":"messages_history","result":"success","completeness":"complete"'
if imsg chats --limit 11 --json >/dev/null 2>&1; then
  fail "non-prescribed Messages chat limit was accepted"
fi
if imsg history --chat-id group-1 \
  --start 2026-08-05T00:00:00-07:00 \
  --end 2026-08-06T00:00:00-07:00 --limit 101 --json >/dev/null 2>&1; then
  fail "non-prescribed Messages history limit was accepted"
fi
if imsg send --chat-id group-1 --text unexpected >/dev/null 2>&1; then
  fail "Messages write operation was accepted"
fi
assert_trace '"operation":"rejected","target":"unrecognized","result":"rejected"'

new_run o1t1
obsidian vault=fixture-vault read path=Actions/task.md >/dev/null
obsidian vault=fixture-vault append path=Actions/task.md content='approved next step' silent
output=$(obsidian vault=fixture-vault read path=Actions/task.md)
[[ "$output" == 'manual context with [[existing wiki link]];approved next step' ]] ||
  fail "Obsidian preservation fixture readback"

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

new_run w1r1
outside_trace="$run_root/outside-trace.jsonl"
ln -s "$outside_trace" "$PCOS_FIXTURE_TRACE"
if pcos-source read role=current_weekly_review >/dev/null 2>&1; then
  fail "symlinked fixture trace was accepted"
fi
[[ ! -e "$outside_trace" ]] || fail "symlinked trace escaped the fixture root"

new_run c1p1
outside_action_state="$run_root/outside-action-state"
mkdir -p "$outside_action_state"
ln -s "$outside_action_state" "$PCOS_FIXTURE_ROOT/action-person_note"
if pcos-action read role=person_note >/dev/null 2>&1; then
  fail "symlinked action state directory was accepted"
fi
[[ -z "$(find "$outside_action_state" -mindepth 1 -print -quit)" ]] ||
  fail "action state symlink escaped the fixture root"

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
  ! \( -name trace.jsonl -o -name read-index -o -name read -o -name written -o -name content \) \
  -print -quit)
[[ -z "$unexpected_file" ]] || fail "unexpected fixture state file"

printf 'fixture self-check passed\n'
