#!/usr/bin/env bash
set -euo pipefail

repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root"

catalog_dirs=$(find skills -mindepth 1 -maxdepth 1 -type d -exec test -f '{}/SKILL.md' ';' -print | LC_ALL=C sort)
readme_links=$(sed -n 's|^- \[.*\](\(skills/[^/]*/SKILL\.md\)).*$|\1|p' README.md | sed 's|/SKILL\.md$||' | LC_ALL=C sort)

if [[ -z "$catalog_dirs" ]]; then
  echo "catalog: no skill packages found" >&2
  exit 1
fi

if ! command -v ruby >/dev/null 2>&1; then
  echo "catalog: required tool 'ruby' is not installed" >&2
  exit 1
fi

if ! diff -u <(printf '%s\n' "$catalog_dirs") <(printf '%s\n' "$readme_links"); then
  echo "catalog: README skill list does not match skills/" >&2
  exit 1
fi

while IFS= read -r skill_dir; do
  skill_path="$skill_dir/SKILL.md"
  if [[ -L "$skill_path" ]]; then
    echo "$skill_path: must not be a symlink" >&2
    exit 1
  fi

  ruby scripts/checks/skill_packages.rb "$skill_dir"
done <<< "$catalog_dirs"

echo "catalog: ${catalog_dirs//$'\n'/, }"
