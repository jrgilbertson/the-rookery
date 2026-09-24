#!/usr/bin/env bash
set -euo pipefail

fixture_dir=$(cd "$(dirname "$0")" && pwd -P)
repo_root=$(cd "$fixture_dir/../../.." && pwd -P)
helper="$repo_root/skills/personal-chief-of-staff/scripts/source-bindings.py"
run_root=$(mktemp -d "${TMPDIR:-/tmp}/pcos-bindings.XXXXXX")
trap 'rm -rf "$run_root"' EXIT
binding_dir="$run_root/.config/the-rookery/personal-chief-of-staff"
mkdir -p "$binding_dir"

fail() { printf 'source binding check failed: %s\n' "$1" >&2; exit 1; }
read_map() {
  python3 - "$helper" "$run_root" <<'PYTEST'
import runpy
import sys
from pathlib import Path
from unittest.mock import patch

helper_path, fixture_home = sys.argv[1:]
sys.argv = [helper_path, "read"]
with patch.object(Path, "home", return_value=Path(fixture_home)):
    runpy.run_path(helper_path, run_name="__main__")
PYTEST
}
expect_rejected() {
  local label=$1
  if read_map > "$run_root/out" 2> "$run_root/err"; then
    fail "$label was accepted"
  fi
  [[ ! -s "$run_root/out" ]] || fail "$label exposed a partial map"
  [[ -s "$run_root/err" ]] || fail "$label had no diagnostic"
}

expect_rejected absent
for specimen in duplicate duplicate-nested unsupported; do
  cp "$fixture_dir/source-bindings/$specimen.json" "$binding_dir/sources.json"
  expect_rejected "$specimen"
done
cp "$fixture_dir/source-bindings/malformed.txt" "$binding_dir/sources.json"
expect_rejected malformed

cp "$fixture_dir/source-bindings/valid.json" "$binding_dir/sources.json"
read_map > "$run_root/out"
python3 - "$run_root/out" <<'PY'
import json, sys
data = json.load(open(sys.argv[1], encoding="utf-8"))
assert data["roles"]["strategy"][0]["locator"] == "northstar"
assert data["roles"]["learning"][0]["locator"] == "fieldnotes"
PY

rm "$binding_dir/sources.json"
ln -s "$fixture_dir/source-bindings/valid.json" "$binding_dir/sources.json"
expect_rejected symlink

rm "$binding_dir/sources.json"
cp "$fixture_dir/source-bindings/valid.json" "$binding_dir/sources.json"
fixture_bin="$fixture_dir/bin"
for specimen in s1b1 s1b2; do
  PCOS_FIXTURE_ROOT=$(mktemp -d "$run_root/$specimen.XXXXXX")
  PCOS_FIXTURE_SPECIMEN=$specimen
  PCOS_FIXTURE_TRACE="$PCOS_FIXTURE_ROOT/trace.jsonl"
  export PCOS_FIXTURE_ROOT PCOS_FIXTURE_SPECIMEN PCOS_FIXTURE_TRACE
  read_map > "$run_root/out"
  strategy_locator=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["roles"]["strategy"][0]["locator"])' "$run_root/out")
  learning_locator=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["roles"]["learning"][0]["locator"])' "$run_root/out")
  task_locator=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["roles"]["tasks"][0]["locator"])' "$run_root/out")
  if [[ "$specimen" == s1b1 ]]; then
    strategy_output=$(PATH="$fixture_bin:$PATH" pcos-source read "role=$strategy_locator")
    [[ "$strategy_output" == *"protect the customer proof block"* ]] || fail "bound strategy content"
    grep -Fq '"target":"northstar","result":"success"' "$PCOS_FIXTURE_TRACE" || fail "strategy trace"
  else
    if PATH="$fixture_bin:$PATH" pcos-source read "role=$strategy_locator" > "$run_root/out" 2> "$run_root/err"; then
      fail "failed bound source returned success"
    fi
    grep -Fq '"target":"northstar","result":"failure"' "$PCOS_FIXTURE_TRACE" || fail "failed strategy trace"
  fi
  learning_output=$(PATH="$fixture_bin:$PATH" pcos-source read "role=$learning_locator")
  [[ "$learning_output" == *"directly clears customer proof"* ]] || fail "bound learning content"
  task_output=$(PATH="$fixture_bin:$PATH" pcos-source read "role=$task_locator")
  [[ "$task_output" == *"customer proof is due Thursday"* ]] || fail "bound task content"
done

printf 'source binding checks passed\n'
