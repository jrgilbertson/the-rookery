#!/usr/bin/env bash
# Loaded after bootstrap by the synthetic Obsidian executable.
# These globals are set by fixture_bootstrap in the caller.
# shellcheck disable=SC2154
journal_specimen="$fixture_dir/specimens/$PCOS_FIXTURE_SPECIMEN"
state_dir="$fixture_root/state-$PCOS_FIXTURE_SPECIMEN"
fixture_prepare_state_dir "$state_dir" "$state_dir/read-index" \
  "$state_dir/read" "$state_dir/written" "$state_dir/content" "$state_dir/stage"

journal_trace() {
  printf '{"operation":"%s","target":"%s","result":"%s","completeness":"%s"}\n' \
    "$1" "$2" "$3" "$4" >> "$trace_path"
}
journal_reject() {
  journal_trace "${operation:-rejected}" "${target_token:-unrecognized}" rejected not_applicable
  die "$1"
}
[[ $# -ge 3 && $1 == vault=fixture-vault ]] || journal_reject "explicit fixture vault required"
operation=$2
shift 2
path=""
content="__unset__"
silent=0
for arg in "$@"; do
  case "$arg" in
    path=*) [[ -z "$path" ]] || journal_reject "duplicate path"; path=${arg#path=} ;;
    content=*) [[ "$content" == __unset__ ]] || journal_reject "duplicate content"; content=${arg#content=} ;;
    silent) [[ $silent == 0 ]] || journal_reject "duplicate silent"; silent=1 ;;
    *) journal_reject "unsupported parameter" ;;
  esac
done
case "$path" in
  Templates/daily.md) target_token=journal_template ;;
  Journals/tuesday.md) target_token=daily_journal ;;
  *) journal_reject "unapproved journal target" ;;
esac
case "$operation" in read|append|write) ;; *) journal_reject "unsupported operation" ;; esac
claim="$state_dir/sequence-claim"
[[ ! -L "$claim" ]] || journal_reject "symlinked sequence claim"
mkdir "$claim" 2>/dev/null || journal_reject "concurrent journal operation"
trap 'rmdir "$claim" 2>/dev/null || true' EXIT
[[ -f "$state_dir/read-index" ]] || printf '0\n' > "$state_dir/read-index"
[[ -f "$state_dir/read" ]] || printf '%s\n' -1 > "$state_dir/read"
[[ -f "$state_dir/written" ]] || printf '0\n' > "$state_dir/written"
[[ -f "$state_dir/stage" ]] || printf 'waiting\n' > "$state_dir/stage"
[[ -f "$state_dir/content" ]] || cp "$journal_specimen/before.md" "$state_dir/content"
if [[ "$operation" == read ]]; then
  [[ "$content" == __unset__ && $silent == 0 ]] || journal_reject "read takes only path"
  if [[ "$target_token" == journal_template ]]; then
    cat "$journal_specimen/template.md"
    cat "$state_dir/read-index" > "$state_dir/read"
  else
    count=$(<"$state_dir/read-index")
    [[ "$count" =~ ^[0-9]+$ ]] || journal_reject "invalid read state"
    if [[ "$PCOS_FIXTURE_SPECIMEN" == j1d1 && $(<"$state_dir/stage") == pending ]]; then
      printf 'Manual note added after approval.\n' >> "$state_dir/content"
      printf 'injected:%s\n' "$((count + 1))" > "$state_dir/stage"
    fi
    printf '%s\n' "$((count + 1))" > "$state_dir/read-index"
    cat "$state_dir/content"
    [[ $(<"$state_dir/written") == 0 ]] || operation=readback
  fi
  journal_trace "$operation" "$target_token" success complete
else
  [[ "$target_token" == daily_journal && "$content" != __unset__ && $silent == 1 ]] ||
    journal_reject "exact silent journal write required"
  [[ $(<"$state_dir/written") == 0 && "$PCOS_FIXTURE_SPECIMEN" != j2e2 ]] ||
    journal_reject "extra or already-satisfied write"
  count=$(<"$state_dir/read-index")
  [[ "$count" =~ ^[0-9]+$ && "$count" -ge 2 ]] || journal_reject "journal reread required"
  [[ $(<"$state_dir/read") == "$((count - 1))" || $(<"$state_dir/read") == "$count" ]] ||
    journal_reject "template refresh must accompany the final journal reread"
  if [[ "$PCOS_FIXTURE_SPECIMEN" == j1d1 ]]; then
    stage=$(<"$state_dir/stage")
    [[ "$stage" =~ ^injected:([0-9]+)$ && "$count" -gt "${BASH_REMATCH[1]}" ]] ||
      journal_reject "post-drift journal reread required"
  fi
  proposed=$content
  if [[ "$operation" == append ]]; then
    # Preserve the final newline when reading the existing journal.
    current=$(cat "$state_dir/content"; printf '.')
    proposed=${current%.}$content
  fi
  expected=$(cat "$journal_specimen/after.md")
  [[ "${proposed%$'\n'}" == "$expected" ]] || journal_reject "write does not preserve the exact approved journal"
  cp "$journal_specimen/after.md" "$state_dir/content"
  printf '1\n' > "$state_dir/written"
  journal_trace "$operation" "$target_token" success not_applicable
fi
rmdir "$claim"
trap - EXIT
