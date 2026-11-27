#!/usr/bin/env bash
# Build one run directory for a Skill Eval: a workspace per case and arm, the
# skill staged into each with-skill workspace at a Git revision (default HEAD),
# and Promptfoo installed from package-lock.json via npm ci. Prints the directory.
set -euo pipefail
umask 077

# Replace with the skill directory name under skills/ when copying this template.
skill_name='<skill-name>'
if [[ "$skill_name" == '<skill-name>' ]]; then
  echo 'Set skill_name in prepare.sh to a skill under skills/ before running.' >&2
  exit 2
fi

here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
repo=$(git -C "$here" rev-parse --show-toplevel)
revision=$(git -C "$repo" rev-parse --verify "${1:-HEAD}^{commit}")

work=$(mktemp -d "${TMPDIR:-/tmp}/rookery-${skill_name}.XXXXXXXX")
mkdir -p "$work/skills" "$work/home" "$work/claude-home"
git -C "$repo" archive "$revision" "skills/$skill_name" |
  tar -x --strip-components=1 -C "$work/skills"
for case_path in "$here"/cases/*/; do
  case_id=$(basename -- "$case_path")
  for arm in claude-skill claude-baseline; do
    mkdir -p "$work/workspaces/$case_id/$arm"
    # Populate each workspace with plain synthetic fixture files (no Git repo
    # and no Bash stand-ins). Replace this block with a generator if cases share
    # computed files.
    if [[ -d "$case_path/workspace" ]]; then
      cp -R "$case_path/workspace/." "$work/workspaces/$case_id/$arm/"
    fi
  done
  mkdir -p "$work/workspaces/$case_id/claude-skill/.claude/skills"
  cp -R "$work/skills/$skill_name" "$work/workspaces/$case_id/claude-skill/.claude/skills/"
done
cp -R "$here/cases" "$here/package.json" "$here/package-lock.json" \
  "$here/promptfooconfig.cjs" "$here/checks.mjs" "$work/"
printf '%s\n' "$revision" > "$work/skill-revision.txt"
PROMPTFOO_DISABLE_TELEMETRY=1 npm --prefix "$work" ci --no-audit --no-fund >&2
printf '%s\n' "$work"
