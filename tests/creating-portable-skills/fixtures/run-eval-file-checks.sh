#!/usr/bin/env bash
#
# run-eval-file-checks.sh — exercises the creating-portable-skills eval file
# validator against valid and invalid fixture skills. It tests the script. It
# does not validate skills/.
#
# Usage: bash tests/creating-portable-skills/fixtures/run-eval-file-checks.sh
# Exits 0 when every assertion passes, 1 otherwise.

set -uo pipefail

here=$(cd "$(dirname "$0")" && pwd)
check="$here/../../../skills/creating-portable-skills/scripts/check-evals.py"
fixtures="$here/eval-files"

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

has() { printf '%s\n' "$1" | grep -qF -- "$2"; }

# run <skill-directory...> sets out and code from one validator run.
run() {
	out=$(python3 "$check" "$@" 2>&1)
	code=$?
}

expect_code() { # expect_code <label> <want>
	if [ "$code" -eq "$2" ]; then ok; else bad "$1: want exit $2 got $code: $out"; fi
}

expect_violation() { # expect_violation <label> <text>
	holds "$1 not reported: $2" has "$out" "$2"
}

# Valid files, including a single-configuration focused benchmark, pass.
run "$fixtures/valid-skill"
expect_code "valid skill" 0
holds "valid skill printed output: $out" [ -z "$out" ]

# A trailing slash names the same directory.
run "$fixtures/valid-skill/"
expect_code "valid skill with trailing slash" 0

# A skill without evals passes.
run "$fixtures/no-evals"
expect_code "skill without evals" 0

run "$fixtures/bad-evals"
expect_code "invalid evals.json" 1
expect_violation evals "skill_name 'another-skill' does not match directory 'bad-evals'"
expect_violation evals "evals[0].prompt: must be a non-empty string"
expect_violation evals "evals[0].files[0]: 'evals/files/missing.csv' does not exist"
expect_violation evals "evals[0].files[1]: '../valid-skill/SKILL.md' leaves the skill directory"
expect_violation evals "evals[0].files[2]: 'evals' is not a file"
expect_violation evals "evals[0].assertions[1]: must be a non-empty string"
expect_violation evals "evals[0].provenance: must be a string"
expect_violation evals "evals[0].regression_control: must be a boolean"
expect_violation evals "evals[1].id: duplicate id 1"
expect_violation evals "evals[1].assertions: must be an array of strings"
expect_violation evals "evals[2].assertions: a regression control needs at least one assertion"
holds "violations are prefixed with the file path" has "$out" "bad-evals/evals/evals.json: "

run "$fixtures/bad-queries"
expect_code "invalid eval_queries.json" 1
expect_violation queries "[0].query: must be a non-empty string"
expect_violation queries "[1].should_trigger: must be a boolean"
expect_violation queries "[1].owner: must be a non-empty string"

run "$fixtures/bad-benchmark"
expect_code "invalid benchmark" 1
expect_violation benchmark "metadata.harness: must be a non-empty string"
expect_violation benchmark "metadata.executor_model: must be a non-empty string"
expect_violation benchmark "metadata.archive_ref: must be a non-empty string"
expect_violation benchmark "run_summary.with_skill.pass_rate.stddev: must be a number"
expect_violation benchmark "run_summary.delta.pass_rate: must be a number"
expect_violation benchmark "latest.json: file name must be <YYYY-MM-DD>-<short-rev>[-<target>].json"

# Several directories are checked in one run; any violation fails it.
run "$fixtures/valid-skill" "$fixtures/bad-queries"
expect_code "valid plus invalid skill" 1
fails "valid skill reported beside an invalid one" has "$out" "valid-skill/"

# Bad invocations and unreadable input exit 2.
run
expect_code "no arguments" 2
run "$fixtures"
expect_code "directory without SKILL.md" 2
expect_violation "missing SKILL.md" "not a skill directory"

scratch=$(mktemp -d)
trap 'rm -rf "$scratch"' EXIT
mkdir -p "$scratch/broken-json/evals"
cp "$fixtures/no-evals/SKILL.md" "$scratch/broken-json/SKILL.md"
printf '{"skill_name": }\n' >"$scratch/broken-json/evals/evals.json"
run "$scratch/broken-json"
expect_code "malformed evals.json" 2
expect_violation "malformed JSON" "cannot read JSON"

mkdir -p "$scratch/nan-json/evals/benchmarks"
cp "$fixtures/no-evals/SKILL.md" "$scratch/nan-json/SKILL.md"
printf '{"metadata": {}, "run_summary": {"delta": {"pass_rate": NaN}}}\n' \
	>"$scratch/nan-json/evals/benchmarks/2026-09-24-abc1234.json"
run "$scratch/nan-json"
expect_code "non-standard JSON constant" 2

# Arms use the names the convention defines: with_skill against one baseline.
arm_case() { # arm_case <name> <run_summary JSON> [runs_per_configuration]
	mkdir -p "$scratch/$1/evals/benchmarks"
	cp "$fixtures/no-evals/SKILL.md" "$scratch/$1/SKILL.md"
	printf '{"metadata": {"skill_name": "%s", "executor_model": "m", "timestamp": "t", "runs_per_configuration": %s, "harness": "h", "grader": "g", "archive_ref": "a", "cost_available": false}, "run_summary": %s}\n' \
		"$1" "${3:-3}" "$2" >"$scratch/$1/evals/benchmarks/2026-09-24-abc1234.json"
	run "$scratch/$1"
}
arm='{"pass_rate": {"mean": 1, "stddev": 0}, "time_seconds": {"mean": 1, "stddev": 0}, "tokens": {"mean": 1, "stddev": 0}}'
delta='{"pass_rate": 0, "time_seconds": 0, "tokens": 0}'
arm_case unknown-arm "{\"with_skill\": $arm, \"baseline\": $arm, \"delta\": $delta}"
expect_code "unknown arm name" 1
expect_violation "unknown arm" "run_summary.baseline: unknown arm; use with_skill, old_skill, or without_skill"
arm_case no-changed-arm "{\"old_skill\": $arm}"
expect_code "missing with_skill" 1
expect_violation "missing with_skill" "run_summary: must include with_skill"
arm_case two-baselines "{\"with_skill\": $arm, \"old_skill\": $arm, \"without_skill\": $arm, \"delta\": $delta}"
expect_code "two baselines" 1
expect_violation "two baselines" "run_summary: compare with_skill against one baseline, not both old_skill and without_skill"

# A comparison runs each arm 3 times; a focused check runs once.
arm_case comparison-one-run "{\"with_skill\": $arm, \"old_skill\": $arm, \"delta\": $delta}" 1
expect_code "comparison with one run" 1
expect_violation "comparison runs" "metadata.runs_per_configuration: a comparison runs each arm 3 times"
arm_case focused-three-runs "{\"with_skill\": $arm}" 3
expect_code "focused check with three runs" 1
expect_violation "focused runs" "metadata.runs_per_configuration: a focused check runs once"

# Every field the benchmark format names has its type; cost is recorded or
# declared unavailable.
bench_case() { # bench_case <name> <extra metadata fields> <extra top-level fields>
	mkdir -p "$scratch/$1/evals/benchmarks"
	cp "$fixtures/no-evals/SKILL.md" "$scratch/$1/SKILL.md"
	printf '{"metadata": {"skill_name": "%s", "executor_model": "m", "timestamp": "t", "runs_per_configuration": 1, "harness": "h", "grader": "g", "archive_ref": "a"%s}, "run_summary": {"with_skill": %s}%s}\n' \
		"$1" "$2" "$arm" "$3" >"$scratch/$1/evals/benchmarks/2026-09-24-abc1234.json"
	run "$scratch/$1"
}
bench_case cost-usd-recorded ', "cost_usd": 0.42' ', "runs": [{"eval_id": 1}], "notes": ["a note"]'
expect_code "cost_usd with runs and notes" 0
bench_case no-cost-record '' ''
expect_code "no cost record" 1
expect_violation "no cost record" "metadata: record cost_usd, or set cost_available to false"
bench_case cost-available-true ', "cost_available": true' ''
expect_violation "cost available without cost_usd" "metadata: record cost_usd, or set cost_available to false"
bench_case cost-available-text ', "cost_available": "no"' ''
expect_violation "cost_available type" "metadata.cost_available: must be a boolean"
bench_case cost-usd-text ', "cost_usd": "0.42"' ''
expect_violation "cost_usd type" "metadata.cost_usd: must be a number"
bench_case empty-final-reviewer ', "cost_available": false, "final_reviewer": ""' ''
expect_violation "final_reviewer type" "metadata.final_reviewer: must be a non-empty string"
bench_case bad-notes ', "cost_available": false' ', "notes": [7]'
expect_violation "notes entries" "notes[0]: must be a non-empty string"
bench_case bad-runs ', "cost_available": false' ', "runs": ["run-1"]'
expect_violation "runs entries" "runs[0]: must be an object"

# The validator writes nothing to disk.
before=$(find "$fixtures" "$scratch" | LC_ALL=C sort)
run "$fixtures/valid-skill" "$fixtures/bad-evals" "$fixtures/bad-benchmark"
after=$(find "$fixtures" "$scratch" | LC_ALL=C sort)
holds "validator wrote files" [ "$before" = "$after" ]

printf 'eval-file-checks: %s passed, %s failed\n' "$passed" "$failed"
[ "$failed" -eq 0 ]
