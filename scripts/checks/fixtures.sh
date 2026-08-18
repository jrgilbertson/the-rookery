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

if ! python3 - "$repo_root" "${runners[@]}" <<'PY'
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve(strict=True)
for raw_path in sys.argv[2:]:
    relative = Path(raw_path)
    candidate = root / relative
    if candidate.is_symlink():
        print(f"fixtures: symbolic-link runner is not allowed: {raw_path}", file=sys.stderr)
        raise SystemExit(1)
    if not candidate.exists():
        print(f"fixtures: missing runner {raw_path}", file=sys.stderr)
        raise SystemExit(1)
    try:
        candidate.relative_to(root)
    except ValueError:
        print(f"fixtures: runner path escapes the repository: {raw_path!r}", file=sys.stderr)
        raise SystemExit(1)
    current = root
    for component in relative.parts:
        current /= component
        if current.is_symlink():
            print(f"fixtures: symbolic-link runner is not allowed: {raw_path!r}", file=sys.stderr)
            raise SystemExit(1)
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root)
    except (FileNotFoundError, OSError, ValueError):
        print(f"fixtures: runner resolves outside the repository or cannot be verified: {raw_path!r}", file=sys.stderr)
        raise SystemExit(1)
    if not resolved.is_file():
        print(f"fixtures: runner is not a regular file: {raw_path!r}", file=sys.stderr)
        raise SystemExit(1)
PY
then
  exit 1
fi

for runner in "${runners[@]}"; do
  echo "fixtures: $runner"
  case "$runner" in
    *.sh) bash "$runner" ;;
    *.py) python3 "$runner" ;;
    *) echo "fixtures: unsupported runner $runner" >&2; exit 1 ;;
  esac
done
