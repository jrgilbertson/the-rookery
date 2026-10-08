#!/usr/bin/env bash
# Copy the maintainer's global agent guidance into the published GLOBAL-AGENTS.md.
# The local file is the source of truth; the repository holds a one-way copy.
#   scripts/sync-global-agents.sh          copy the local file into the repository
#   scripts/sync-global-agents.sh --check  fail when the repository copy is stale
set -euo pipefail

repo_root=$(git rev-parse --show-toplevel)
source_file="${GLOBAL_AGENTS_SOURCE:-$HOME/.codex/AGENTS.md}"
published_file="$repo_root/GLOBAL-AGENTS.md"

case "${1:-}" in
  --check)
    # Contributors and CI have no local source, so there is nothing to compare.
    if [[ ! -f "$source_file" ]]; then
      exit 0
    fi
    if ! diff -u --label GLOBAL-AGENTS.md --label "$source_file" \
      "$published_file" "$source_file"; then
      echo "global-agents: GLOBAL-AGENTS.md is stale; run scripts/sync-global-agents.sh" >&2
      exit 1
    fi
    ;;
  '')
    if [[ ! -f "$source_file" ]]; then
      echo "global-agents: source not found: $source_file" >&2
      exit 1
    fi
    cp "$source_file" "$published_file"
    echo "global-agents: copied $source_file to GLOBAL-AGENTS.md"
    ;;
  *)
    echo "usage: scripts/sync-global-agents.sh [--check]" >&2
    exit 2
    ;;
esac
