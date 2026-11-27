#!/usr/bin/env bash
# Build one run directory for the managing-issues Skill Eval: a plain workspace
# per case and arm with synthetic tracker config, the skill staged into each
# with-skill workspace at a Git revision (default HEAD), and Promptfoo
# installed from package-lock.json via npm ci. Prints the directory.
set -euo pipefail
umask 077

here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
repo=$(git -C "$here" rev-parse --show-toplevel)
revision=$(git -C "$repo" rev-parse --verify "${1:-HEAD}^{commit}")

work=$(mktemp -d "${TMPDIR:-/tmp}/rookery-managing-issues.XXXXXXXX")
mkdir -p "$work/skills" "$work/home" "$work/claude-home"
git -C "$repo" archive "$revision" skills/managing-issues |
  tar -x --strip-components=1 -C "$work/skills"
for case_path in "$here"/cases/*/; do
  case_id=$(basename -- "$case_path")
  case "$case_id" in
    password-reset-plus) provider=github ;;
    follow-up-later|mention-link) provider=linear ;;
    *) echo "No provider fixture for $case_id" >&2; exit 2 ;;
  esac
  workspace="$work/workspaces/$case_id"
  for arm in claude-skill claude-baseline; do
    mkdir -p "$workspace/$arm/.agents"
    cp "$here/fixtures/$provider.json" "$workspace/$arm/.agents/managing-issues.json"
  done
  python3 -I "$work/skills/managing-issues/scripts/config_check.py" \
    --repo-root "$workspace/claude-baseline" --config .agents/managing-issues.json > /dev/null
  mkdir -p "$workspace/claude-skill/.claude/skills"
  cp -R "$work/skills/managing-issues" "$workspace/claude-skill/.claude/skills/"
done
cp -R "$here/cases" "$here/package.json" "$here/package-lock.json" \
  "$here/promptfooconfig.cjs" "$here/checks.mjs" "$work/"
printf '%s\n' "$revision" > "$work/skill-revision.txt"
PROMPTFOO_DISABLE_TELEMETRY=1 npm --prefix "$work" ci --no-audit --no-fund >&2
printf '%s\n' "$work"
