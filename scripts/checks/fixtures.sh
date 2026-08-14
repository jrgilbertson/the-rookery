#!/usr/bin/env bash
set -euo pipefail

repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root"
export PYTHONDONTWRITEBYTECODE=1

runners=(
  tests/checking-merge-readiness/fixtures/run-fetch-checks.sh
  tests/checking-merge-readiness/fixtures/run-stub-checks.sh
  tests/checking-pr-readiness/fixtures/run-assessment-checks.py
  tests/checking-pr-readiness/fixtures/run-helper-checks.sh
  tests/managing-issues/fixtures/run-graph-checks.py
  tests/managing-issues/fixtures/run-policy-checks.py
  tests/managing-issues/fixtures/run-provider-checks.py
  tests/personal-chief-of-staff/fixtures/run-fixture-checks.sh
  tests/repository-integrity/check_catalog.py
  tests/repository-integrity/check_repository.py
  tests/repo-gardener/fixtures/effects/check_effects.py
  tests/repo-gardener/fixtures/github-register/check_snapshots.py
  tests/repo-gardener/fixtures/reconciliation/check_decisions.py
  tests/repo-gardener/fixtures/run-records/check_run_records.py
)

discovered=()
while IFS= read -r -d '' task_runner; do
  discovered+=("$task_runner")
done < <(git ls-files --cached --others --exclude-standard -z -- \
  'tests/**/run-*.sh' 'tests/**/run-*.py' 'tests/**/check_*.py')

if ! diff -u \
  <(printf '%s\n' "${runners[@]}" | LC_ALL=C sort) \
  <(printf '%s\n' "${discovered[@]}" | LC_ALL=C sort); then
  echo "fixtures: explicit roster does not match discovered runners" >&2
  exit 1
fi

for runner in "${runners[@]}"; do
  if [[ ! -f "$runner" ]]; then
    echo "fixtures: missing runner $runner" >&2
    exit 1
  fi
  echo "fixtures: $runner"
  case "$runner" in
    *.sh) bash "$runner" ;;
    *.py) python3 "$runner" ;;
    *) echo "fixtures: unsupported runner $runner" >&2; exit 1 ;;
  esac
done
