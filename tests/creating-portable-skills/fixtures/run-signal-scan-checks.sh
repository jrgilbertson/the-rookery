#!/usr/bin/env bash
#
# run-signal-scan-checks.sh — exercises the creating-portable-skills signal
# scan against planted fixtures. It tests the script. It does not scan skills/.
#
# Usage: bash tests/creating-portable-skills/fixtures/run-signal-scan-checks.sh
# Exits 0 when every assertion passes, 1 otherwise.

set -uo pipefail

here=$(cd "$(dirname "$0")" && pwd)
scan="$here/../../../skills/creating-portable-skills/scripts/signal-scan.sh"
fixtures="$here/signal-scan"

passed=0
failed=0

ok() { passed=$((passed + 1)); }
bad() { failed=$((failed + 1)); printf 'FAIL: %s\n' "$1"; }

# holds <label> <command...> passes when the command succeeds.
holds() {
	label="$1"
	shift
	if "$@"; then ok; else bad "$label"; fi
}

# fails <label> <command...> passes when the command does not succeed.
fails() {
	label="$1"
	shift
	if "$@"; then bad "$label"; else ok; fi
}

has() { printf '%s\n' "$1" | grep -q "$2"; }
quiet() { "$@" >/dev/null 2>&1; }

# count <output> <signal> prints the number in that signal's header line.
count() {
	printf '%s\n' "$1" | sed -n "s/^## $2 (\([0-9][0-9]*\)).*/\1/p"
}

expect_count() { # expect_count <label> <output> <signal> <want>
	got=$(count "$2" "$3")
	if [ "$got" = "$4" ]; then ok; else bad "$1: $3 want $4 got '${got}'"; fi
}

signals=(
	"pressure language"
	"hedged requirement"
	"model trait claim"
	"thinking scaffold"
	"output clamp or cadence"
	"format or narration suppressor"
	"reinforcement padding"
	"grader vocabulary"
	"migration-relative phrasing"
	"history identifier"
	"pinned model name"
)

planted=$(sh "$scan" "$fixtures/planted")
planted_code=$?
clean=$(sh "$scan" "$fixtures/clean")
clean_code=$?

holds "a completed scan with hits exits 0, got $planted_code" [ "$planted_code" -eq 0 ]
holds "a clean scan exits 0, got $clean_code" [ "$clean_code" -eq 0 ]

for signal in "${signals[@]}"; do
	expect_count clean "$clean" "$signal" 0
done

expect_count planted "$planted" "pressure language" 1
expect_count planted "$planted" "hedged requirement" 2
expect_count planted "$planted" "model trait claim" 1
expect_count planted "$planted" "thinking scaffold" 1
expect_count planted "$planted" "output clamp or cadence" 1
expect_count planted "$planted" "format or narration suppressor" 1
expect_count planted "$planted" "reinforcement padding" 1
expect_count planted "$planted" "grader vocabulary" 1
expect_count planted "$planted" "migration-relative phrasing" 1
expect_count planted "$planted" "history identifier" 1
expect_count planted "$planted" "pinned model name" 1

# Every header names the checklist item that judges the signal.
headers=$(printf '%s\n' "$planted" | grep -c '^## .* -> .')
holds "every header names a checklist item: want ${#signals[@]} got $headers" [ "$headers" -eq "${#signals[@]}" ]

# "retry to" is not a hedged requirement.
fails "retry to reported as a hedge" has "$planted" 'Restrict the retry'

# The references hit is reported; the assets pattern is not.
holds "references file not scanned" has "$planted" 'references/notes.md'
fails "assets file scanned" has "$planted" 'assets/template.md'

# A trailing slash on the package path gives the same output.
slashed=$(sh "$scan" "$fixtures/planted/")
holds "trailing slash changes the counts" [ "$(printf '%s\n' "$slashed" | grep '^## ')" = "$(printf '%s\n' "$planted" | grep '^## ')" ]

# Invalid inputs must fail.
fails "missing SKILL.md should exit non-zero" quiet sh "$scan" "$fixtures"
fails "no arguments should exit non-zero" quiet sh "$scan"

# Inject dependency failures so error handling is tested even as root, where
# chmod 000 cannot reliably make a file unreadable. The production scan runs.
scratch=$(mktemp -d)
trap 'rm -rf "$scratch"' EXIT
real_grep=$(command -v grep)
real_find=$(command -v find)
mkdir "$scratch/grep-bin" "$scratch/find-bin"
cat >"$scratch/grep-bin/grep" <<'SH'
#!/bin/sh
for file do :; done
if [ "$file" = "$SCAN_TEST_BAD_FILE" ]; then
	printf 'injected read failure: %s\n' "$file" >&2
	exit 2
fi
exec "$SCAN_TEST_REAL_GREP" "$@"
SH
cat >"$scratch/find-bin/find" <<'SH'
#!/bin/sh
"$SCAN_TEST_REAL_FIND" "$@" || exit
echo 'injected traversal failure after partial results' >&2
exit 1
SH
chmod +x "$scratch/grep-bin/grep" "$scratch/find-bin/find"

# A later readable reference must not hide an earlier file's read error.
PATH="$scratch/grep-bin:$PATH" SCAN_TEST_REAL_GREP="$real_grep" \
	SCAN_TEST_BAD_FILE="$fixtures/planted/SKILL.md" \
	sh "$scan" "$fixtures/planted" >"$scratch/read.out" 2>"$scratch/read.err"
read_code=$?
holds "read failure must exit non-zero, got $read_code" [ "$read_code" -ne 0 ]
holds "read failure diagnostic is preserved" has "$(cat "$scratch/read.err")" 'injected read failure'

# Sorting a partial file list must not hide find's failure.
PATH="$scratch/find-bin:$PATH" SCAN_TEST_REAL_FIND="$real_find" \
	sh "$scan" "$fixtures/planted" >"$scratch/find.out" 2>"$scratch/find.err"
find_code=$?
holds "traversal failure must exit non-zero, got $find_code" [ "$find_code" -ne 0 ]
holds "traversal failure diagnostic is preserved" has "$(cat "$scratch/find.err")" 'injected traversal failure'

printf 'signal-scan: %s passed, %s failed\n' "$passed" "$failed"
[ "$failed" -eq 0 ]
