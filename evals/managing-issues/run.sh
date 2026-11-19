#!/usr/bin/env bash
set -euo pipefail

work=$(cd -- "${1:?Pass the directory printed by prepare.sh}" && pwd)
case "${2:-all}" in
  all) arms='.' ;;
  claude-skill) arms='^Claude with skill$' ;;
  claude-baseline) arms='^Claude baseline$' ;;
  codex-skill) arms='^Codex with skill$' ;;
  *)
    echo 'Choose all, claude-skill, claude-baseline, or codex-skill.' >&2
    exit 2
    ;;
esac

node_dir=$(dirname -- "$(command -v node)")
cd "$work"
env -i PATH="$node_dir:/usr/bin:/bin" HOME="$work/home" \
  CLAUDE_CONFIG_DIR="$work/claude-home" PROMPTFOO_DISABLE_TELEMETRY=1 \
  CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 DISABLE_PROMPT_CACHING=1 \
  timeout 300 ./node_modules/.bin/promptfoo eval -c promptfooconfig.cjs \
  --no-cache --no-share --max-concurrency 1 --no-table --filter-providers "$arms" \
  --output "$work/results-${2:-all}.json"
