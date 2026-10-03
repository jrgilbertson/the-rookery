#!/usr/bin/env bash
set -euo pipefail

fixture_dir=$(cd "$(dirname "$0")" && pwd -P)
bash "$fixture_dir/binding-checks.sh"
python3 "$fixture_dir/setup-checks.py"
