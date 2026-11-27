#!/usr/bin/env bash
# Build one run directory for the repo-captain Skill Eval: a plain workspace per
# case and arm (no Git repo, no executable shims), the skill staged into the
# with-skill workspaces at a Git revision (default HEAD), a no-skill baseline,
# and Promptfoo installed from package-lock.json via npm ci. Prints the directory.
set -euo pipefail
umask 077

here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
repo=$(git -C "$here" rev-parse --show-toplevel)
revision=$(git -C "$repo" rev-parse --verify "${1:-HEAD}^{commit}")

work=$(mktemp -d "${TMPDIR:-/tmp}/rookery-repo-captain.XXXXXXXX")
mkdir -p "$work/skills" "$work/home" "$work/claude-home"
git -C "$repo" archive "$revision" skills/repo-captain |
  tar -x --strip-components=1 -C "$work/skills"
for case_path in "$here"/cases/*/; do
  case_id=$(basename -- "$case_path")
  for arm in claude-skill claude-baseline; do
    python3 -I "$here/fixture.py" "$work/workspaces/$case_id/$arm" "$case_id"
  done
  mkdir -p "$work/workspaces/$case_id/claude-skill/.claude/skills"
  cp -R "$work/skills/repo-captain" "$work/workspaces/$case_id/claude-skill/.claude/skills/"
done
cp -R "$here/cases" "$here/package.json" "$here/package-lock.json" \
  "$here/promptfooconfig.cjs" "$here/checks.mjs" "$work/"
printf '%s\n' "$revision" > "$work/skill-revision.txt"
PROMPTFOO_DISABLE_TELEMETRY=1 npm --prefix "$work" ci --no-audit --no-fund >&2
printf '%s\n' "$work"
