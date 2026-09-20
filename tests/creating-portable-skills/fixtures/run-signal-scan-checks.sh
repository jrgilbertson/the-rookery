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
	"prohibition run"
	"numbered workflow heading"
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
expect_count planted "$planted" "prohibition run" 1
expect_count planted "$planted" "numbered workflow heading" 2

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

# The scan writes nothing, so it runs in a read-only sandbox.
code=$(grep -v '^[[:space:]]*#' "$scan")
fails "scan writes a file" has "$code" 'mktemp\|>>\|> *"\|> *[$/a-z]'

# Two consecutive prohibitions are not a run.
two=$(sh "$scan" "$fixtures/two-prohibitions")
expect_count two-prohibitions "$two" "prohibition run" 0

# A directory with no SKILL.md is the only error exit.
fails "missing SKILL.md should exit non-zero" quiet sh "$scan" "$fixtures"
fails "no arguments should exit non-zero" quiet sh "$scan"

printf 'signal-scan: %s passed, %s failed\n' "$passed" "$failed"
[ "$failed" -eq 0 ]
