#!/usr/bin/env bash
set -euo pipefail

fixture_dir=$(cd "$(dirname "$0")" && pwd -P)
validator="$fixture_dir/source-map-schema.py"
run_root=$(mktemp -d "${TMPDIR:-/tmp}/pcos-bindings.XXXXXX")
trap 'rm -rf "$run_root"' EXIT
binding_dir="$run_root/.config/the-rookery/personal-chief-of-staff"
mkdir -p "$binding_dir"

fail() { printf 'source binding check failed: %s\n' "$1" >&2; exit 1; }
read_map() {
  python3 "$validator" "$binding_dir/sources.json"
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


printf 'source binding checks passed\n'
