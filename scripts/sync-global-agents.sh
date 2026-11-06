#!/usr/bin/env bash
# Copy the maintainer's global agent guidance into the published GLOBAL-AGENTS.md.
# The local file is the source of truth; the repository holds a one-way copy.
# The maintainer opts in once per clone:
#   git config rookery.globalAgentsSource ~/.codex/AGENTS.md
#   scripts/sync-global-agents.sh          copy the local file into the repository
#   scripts/sync-global-agents.sh --check  fail when the copy on main, or on a
#                                          branch that edits it, is stale
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
    # A branch that edits the copy is judged by what its push sends. Any other
    # branch is judged by the default branch, so an old branch does not fail
    # because main refreshed the copy after it forked.
    published=HEAD
    if git rev-parse --verify --quiet origin/main >/dev/null &&
      git diff --quiet origin/main...HEAD -- GLOBAL-AGENTS.md 2>/dev/null; then
      published=origin/main
    fi
    if ! git show "$published:GLOBAL-AGENTS.md" 2>/dev/null |
      diff -u --label "$published:GLOBAL-AGENTS.md" --label "$source_file" - "$source_file"; then
      echo "global-agents: $published:GLOBAL-AGENTS.md is stale; run scripts/sync-global-agents.sh and commit" >&2
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
    python3 -I - "$source_file" <<'PYTHON'
import os
import shutil
import stat
import sys
import tempfile

try:
    if stat.S_ISDIR(os.lstat("GLOBAL-AGENTS.md").st_mode):
        raise IsADirectoryError("GLOBAL-AGENTS.md is a directory")
except FileNotFoundError:
    pass

descriptor, temporary = tempfile.mkstemp(prefix=".GLOBAL-AGENTS.", dir=".")
try:
    with os.fdopen(descriptor, "wb") as destination, open(sys.argv[1], "rb") as source:
        shutil.copyfileobj(source, destination)
        os.fchmod(destination.fileno(), 0o644)
    os.replace(temporary, "GLOBAL-AGENTS.md")
finally:
    if os.path.exists(temporary):
        os.unlink(temporary)
PYTHON
    echo "global-agents: copied $source_file to GLOBAL-AGENTS.md"
    ;;
  *)
    echo "usage: scripts/sync-global-agents.sh [--check]" >&2
    exit 2
    ;;
esac
