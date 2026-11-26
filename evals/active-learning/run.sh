#!/usr/bin/env bash
# Run one Eval Case on one arm with the existing Claude Code login. This calls
# a paid model: get the skill owner's approval first.
set -euo pipefail

work=$(cd -- "${1:?Pass the directory printed by prepare.sh}" && pwd)
case "${2:?Pass an arm}" in
  claude-skill) arms='^Claude with skill$' ;;
  claude-baseline) arms='^Claude baseline$' ;;
  *) echo 'Choose claude-skill or claude-baseline.' >&2; exit 2 ;;
esac
case_id=${3:?Pass an Eval Case ID}
if [[ "$case_id" == */* || ! -f "$work/cases/$case_id/prompt.md" ]]; then
  echo "Unknown Eval Case: $case_id" >&2
  exit 2
fi

node_dir=$(dirname -- "$(command -v node)")
cd "$work"
env -i PATH="$node_dir:/usr/bin:/bin" HOME="$HOME" USER="${USER:-}" TMPDIR="${TMPDIR:-/tmp}" \
  ${CLAUDE_CONFIG_DIR:+CLAUDE_CONFIG_DIR="$CLAUDE_CONFIG_DIR"} \
  ROOKERY_EVAL_CASE="$case_id" PROMPTFOO_DISABLE_TELEMETRY=1 \
  CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 \
  ./node_modules/.bin/promptfoo eval -c promptfooconfig.cjs \
  --no-cache --no-share --max-concurrency 1 --no-table --filter-providers "$arms" \
  --output "$work/results-$case_id-$2.json"
