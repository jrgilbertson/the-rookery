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
mkdir -p "$work/home" "$work/claude-home" "$work/codex-home" "$work/skills"
ln -s "$claude_auth" "$work/claude-home/.credentials.json"
ln -s "$codex_auth" "$work/codex-home/auth.json"
git -C "$repo" archive "$revision" skills/managing-issues |
  tar -x --strip-components=1 -C "$work/skills"
for case_path in "$case_dir"/cases/*/; do
  case_id=$(basename -- "$case_path")
  case "$case_id" in
    password-reset-plus) provider=github ;;
    follow-up-later|mention-link) provider=linear ;;
    *) echo "No provider fixture for $case_id" >&2; exit 2 ;;
  esac
  workspace="$work/workspaces/$case_id"
  for arm in claude-skill claude-baseline codex-skill; do
    mkdir -p "$workspace/$arm/.agents"
    cp "$case_dir/fixtures/$provider.json" "$workspace/$arm/.agents/managing-issues.json"
  done
  python3 -I "$work/skills/managing-issues/scripts/config_check.py" \
    --repo-root "$workspace/claude-baseline" --config .agents/managing-issues.json > /dev/null
  mkdir -p "$workspace/claude-skill/.claude/skills" "$workspace/codex-skill/.agents/skills"
  cp -R "$work/skills/managing-issues" "$workspace/claude-skill/.claude/skills/"
  cp -R "$work/skills/managing-issues" "$workspace/codex-skill/.agents/skills/"
done
cp -R "$case_dir/cases" "$case_dir/package.json" "$case_dir/promptfooconfig.cjs" "$work/"
printf '%s\n' "$revision" > "$work/skill-revision.txt"
PROMPTFOO_DISABLE_TELEMETRY=1 npm --prefix "$work" install --no-audit --no-fund >&2

codex_binaries=("$work"/node_modules/@openai/codex-linux-*/vendor/*/bin/codex)
if [[ ${#codex_binaries[@]} -ne 1 || ! -x "${codex_binaries[0]}" ]]; then
  echo 'Expected one native Codex CLI from the pinned SDK.' >&2
  exit 1
fi
# Let the sandbox re-exec its helper binary without mounting the rest of the run.
{
  printf '%s\n' 'default_permissions = "rookery_eval"' '[permissions.rookery_eval.filesystem]' \
    '":minimal" = "read"' '":workspace_roots" = "read"'
  printf '"%s" = "read"\n' "${codex_binaries[0]}"
  if [[ -f /usr/bin/gh && ! -L /usr/bin/gh ]]; then
    printf '%s\n' '"/usr/bin/gh" = "deny"'
  fi
  printf '%s\n' '[permissions.rookery_eval.network]' 'enabled = false'
} > "$work/codex-home/config.toml"

env -i PATH=/usr/bin:/bin HOME="$work/home" CODEX_HOME="$work/codex-home" \
  "${codex_binaries[0]}" sandbox --permission-profile rookery_eval \
  --cd "$work/workspaces/password-reset-plus/codex-skill" -- \
  /bin/bash -e -s -- "$work/codex-home/auth.json" >&2 <<'SANDBOX'
test -r .agents/skills/managing-issues/SKILL.md
test -r .agents/managing-issues.json
test ! -r "$1"
test ! -r ../claude-skill/.agents/managing-issues.json
if touch .sandbox-write-probe 2>/dev/null; then exit 1; fi
python3 -I - <<'PY'
import socket
try:
    socket.socket()
except PermissionError:
    pass
else:
    raise SystemExit(1)
PY
SANDBOX
printf '%s\n' "$work"
