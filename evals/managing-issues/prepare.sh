#!/usr/bin/env bash
set -euo pipefail
umask 077

case_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
repo=$(git -C "$case_dir" rev-parse --show-toplevel)
revision=$(git -C "$repo" rev-parse --verify "${1:-HEAD}^{commit}")
claude_auth="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/.credentials.json"
codex_auth="${CODEX_HOME:-$HOME/.codex}/auth.json"

if [[ ! -r "$claude_auth" || ! -r "$codex_auth" ]]; then
  echo 'Sign in to Claude Code and Codex with file-backed credentials first.' >&2
  exit 1
fi

work=$(mktemp -d /tmp/rookery-managing-issues.XXXXXXXX)
mkdir -p "$work/home" "$work/claude-home" "$work/codex-home" \
  "$work/claude-skill/.claude/skills" "$work/claude-baseline" "$work/codex-skill/.agents/skills"
ln -s "$claude_auth" "$work/claude-home/.credentials.json"
ln -s "$codex_auth" "$work/codex-home/auth.json"
git -C "$repo" archive "$revision" skills/managing-issues |
  tar -x --strip-components=1 -C "$work/claude-skill/.claude/skills"
cp -R "$work/claude-skill/.claude/skills/managing-issues" "$work/codex-skill/.agents/skills/"
cp -R "$case_dir/cases" "$case_dir/package.json" "$case_dir/promptfooconfig.cjs" "$work/"
printf '%s\n' "$revision" > "$work/skill-revision.txt"
PROMPTFOO_DISABLE_TELEMETRY=1 npm --prefix "$work" install --no-audit --no-fund >&2
printf '%s\n' "$work"
