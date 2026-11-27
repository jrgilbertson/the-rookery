#!/usr/bin/env bash
# Run one Eval Case on one arm with the existing Claude Code subscription login.
# This calls a paid model: get the skill owner's approval first.
set -euo pipefail
umask 077

work=$(cd -- "${1:?Pass the directory printed by prepare.sh}" && pwd)
case "${2:?Pass an arm}" in
  claude-skill) arms='^Claude with skill$' ;;
  claude-baseline) arms='^Claude baseline$' ;;
  *) echo 'Choose claude-skill or claude-baseline.' >&2; exit 2 ;;
esac
case_id=${3:?Pass an Eval Case ID}
if [[ "$case_id" == */* || "$case_id" == '.' || "$case_id" == '..' || ! -f "$work/cases/$case_id/prompt.md" ]]; then
  echo "Unknown Eval Case: $case_id" >&2
  exit 2
fi

run_home="$work/home"
claude_home="$work/claude-home"
mkdir -p "$run_home" "$claude_home"

# Keep Promptfoo and Claude Code state out of the operator's real home while
# preserving signed-in Claude Code subscription auth on macOS and Linux:
# - File-backed credentials (Linux or custom CLAUDE_CONFIG_DIR): link only
#   .credentials.json into the temporary CLAUDE_CONFIG_DIR.
# - macOS Keychain: pin CLAUDE_SECURESTORAGE_CONFIG_DIR to the operator's
#   original CLAUDE_CONFIG_DIR (empty string when unset) so the Keychain
#   service lookup matches the signed-in account.
real_claude_dir="${CLAUDE_CONFIG_DIR:-${HOME:+$HOME/.claude}}"
if [[ -n "$real_claude_dir" && "$real_claude_dir" != "$claude_home" && -r "$real_claude_dir/.credentials.json" ]]; then
  ln -sf "$real_claude_dir/.credentials.json" "$claude_home/.credentials.json"
fi
secure_storage_dir="${CLAUDE_SECURESTORAGE_CONFIG_DIR-${CLAUDE_CONFIG_DIR:-}}"

node_dir=$(dirname -- "$(command -v node)")
cmd=(./node_modules/.bin/promptfoo eval -c promptfooconfig.cjs
  --no-cache --no-share --max-concurrency 1 --no-table
  --filter-providers "$arms"
  --output "$work/results-$case_id-$2.json")
timeout_bin=$(command -v timeout || command -v gtimeout || true)
if [[ -n "$timeout_bin" ]]; then
  cmd=("$timeout_bin" 360 "${cmd[@]}")
fi

cd "$work"
env -i PATH="$node_dir:/usr/bin:/bin" HOME="$run_home" USER="${USER:-}" \
  TMPDIR="${TMPDIR:-/tmp}" \
  CLAUDE_CONFIG_DIR="$claude_home" \
  CLAUDE_SECURESTORAGE_CONFIG_DIR="$secure_storage_dir" \
  ROOKERY_EVAL_CASE="$case_id" \
  PROMPTFOO_DISABLE_TELEMETRY=1 \
  PROMPTFOO_EVAL_TIMEOUT_MS=300000 \
  CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 \
  CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 \
  "${cmd[@]}"
