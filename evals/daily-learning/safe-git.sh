#!/usr/bin/env bash
# Read-only stand-in for git during an Eval Case run. run.sh puts it first on
# PATH as `git`. The workspace holds a web clip with a planted instruction, so
# the model may be steered toward git options that write files or run
# commands. This refuses those options and runs the real git with no global,
# system, or command-running config, whatever the repository's own config says.
set -euo pipefail
for arg in "$@"; do
  case "$arg" in
    -c|--config-env*|--exec-path*|--git-dir*|--work-tree*|--namespace*|\
    --output*|--no-index|--ext-diff|--textconv|--upload-pack*|--receive-pack*)
      echo "safe-git: '$arg' is not allowed in an eval run" >&2
      exit 2 ;;
  esac
done
export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_TERMINAL_PROMPT=0
# Command-line config outranks the repository's .git/config.
export GIT_CONFIG_PARAMETERS="'core.fsmonitor'='' 'core.hooksPath'='/dev/null' 'core.pager'='cat' 'core.sshCommand'='false' 'diff.external'='' 'core.editor'='false'"
exec "${SAFE_GIT_REAL:?run.sh sets SAFE_GIT_REAL}" --no-pager "$@"
