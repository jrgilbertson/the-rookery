#!/usr/bin/env bash
# Copy the maintainer's global agent guidance into the published GLOBAL-AGENTS.md.
# The local file is the source of truth; the repository holds a one-way copy.
# The maintainer opts in once per clone:
#   git config rookery.globalAgentsSource ~/.codex/AGENTS.md
#   scripts/sync-global-agents.sh          copy the local file into the repository
#   scripts/sync-global-agents.sh --check  fail when the committed copy is stale
set -euo pipefail

repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root"
source_file=$(git config --path --get rookery.globalAgentsSource || true)

case "${1:-}" in
  --check)
    # Contributors and CI have not opted in, so there is nothing to compare.
    if [[ -z "$source_file" ]]; then
      exit 0
    fi
    if [[ ! -f "$source_file" ]]; then
      echo "global-agents: configured source not found: $source_file" >&2
      exit 1
    fi
    # Compare the committed copy, which is what a push sends.
    if ! git show HEAD:GLOBAL-AGENTS.md 2>/dev/null |
      diff -u --label "HEAD:GLOBAL-AGENTS.md" --label "$source_file" - "$source_file"; then
      echo "global-agents: committed GLOBAL-AGENTS.md is stale; run scripts/sync-global-agents.sh and commit" >&2
      exit 1
    fi
    ;;
  '')
    if [[ -z "$source_file" ]]; then
      echo "global-agents: set the source first: git config rookery.globalAgentsSource ~/.codex/AGENTS.md" >&2
      exit 1
    fi
    if [[ ! -f "$source_file" ]]; then
      echo "global-agents: source not found: $source_file" >&2
      exit 1
    fi
    cp "$source_file" GLOBAL-AGENTS.md
    echo "global-agents: copied $source_file to GLOBAL-AGENTS.md"
    ;;
  *)
    echo "usage: scripts/sync-global-agents.sh [--check]" >&2
    exit 2
    ;;
esac
