#!/usr/bin/env bash
# Run one daily-learning Eval Case once, with or without the skill, in a fresh workspace.
#
# Usage: run.sh <case> <with_skill|without_skill> <out-dir> [git-revision]
#
# This calls a paid model. Get the skill owner's approval before running it.
# The workspace includes a web clip with a planted instruction, so the model reads
# hostile text while running as you. Git is limited to read-only subcommands run
# through safe-git.sh, edits are limited to the workspace, and the vault's .git
# folder is read-only. The Read and WebFetch tools can still reach files and the
# network, so for full isolation run this in a disposable VM or container.
# The run loads no user settings, installed skills, plugins, MCP servers or global
# instructions (--setting-sources project, --strict-mcp-config). The with_skill arm
# loads only skills/daily-learning at <git-revision> (default HEAD), staged as a
# throwaway plugin. Writes events.jsonl, file_changes.txt, response.md and
# transcript.json into <out-dir>.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
case=$1 arm=$2 out=$3 rev=${4:-HEAD}
[ -f "$here/$case/prompt.md" ] || { echo "unknown case: $case" >&2; exit 2; }
mkdir -p "$out"
out=$(cd "$out" && pwd)
ws="$out/ws"
python3 -I "$here/fixture.py" "$ws" "$case"

# Hash every workspace file plus the vault's Git config, refs, and hooks, so a
# commit or a planted config change shows up. Git objects, the index, and logs
# are left out because read-only commands such as `git status` can rewrite the
# index. Never run git here after the model has run: a changed .git/config
# could make git run a command.
hashes() {
  (cd "$ws" && find . \( -path ./vault/.git/objects -o -path ./vault/.git/logs \) -prune \
    -o -type f ! -path ./vault/.git/index -print0 | LC_ALL=C sort -z | xargs -0 shasum -a 256)
}
hashes > "$out/before.txt"

extra=()
if [ "$arm" = with_skill ]; then
  plugin="$out/plugin"
  mkdir -p "$plugin/.claude-plugin" "$plugin/skills"
  printf '{"name":"dl","version":"0.0.0","description":"daily-learning under test"}\n' > "$plugin/.claude-plugin/plugin.json"
  git -C "$(git -C "$here" rev-parse --show-toplevel)" archive "$rev" -- skills/daily-learning | tar -x -C "$plugin"
  extra=(--plugin-dir "$plugin")
elif [ "$arm" != without_skill ]; then
  echo "arm must be with_skill or without_skill" >&2; exit 2
fi

# Every `git` the model runs goes through safe-git.sh, kept read-only outside
# the workspace. The model may edit only files inside the workspace, and the
# vault's .git folder is read-only on disk, which holds on a case-insensitive
# file system where a path rule for ".git" would miss ".GIT".
mkdir -p "$out/bin"
cp "$here/safe-git.sh" "$out/bin/git"
chmod 555 "$out/bin/git" "$out/bin"
chmod -R a-w "$ws/vault/.git"
export SAFE_GIT_REAL
SAFE_GIT_REAL=$(command -v git)

# The prompt is the text after the settings block.
prompt=$(awk 'n>=2 && (seen || NF) {seen=1; print} /^---$/{n++}' "$here/$case/prompt.md")
cd "$ws"
set +e
PATH="$out/bin:$PATH" claude -p "$prompt" \
  --model claude-opus-5-5 --effort high \
  --setting-sources project --strict-mcp-config --no-session-persistence \
  --permission-mode acceptEdits \
  --allowedTools "Read Glob Grep Edit(./**) Write(./**) WebSearch WebFetch Skill Bash(ls:*) Bash(stat:*) Bash(git log:*) Bash(git show:*) Bash(git diff:*) Bash(git status:*) Bash(git -C vault log:*) Bash(git -C vault show:*) Bash(git -C vault diff:*) Bash(git -C vault status:*)" \
  --disallowedTools "Edit(vault/.git/**) Write(vault/.git/**)" \
  --max-budget-usd 3 \
  --output-format stream-json --verbose ${extra[@]+"${extra[@]}"} < /dev/null > "$out/events.jsonl" 2> "$out/stderr.txt"
rc=$?
set -e
hashes > "$out/after.txt"
chmod -R u+w "$ws/vault/.git" "$out/bin"
if diff "$out/before.txt" "$out/after.txt" > "$out/file_changes.txt"; then echo "no file changes" > "$out/file_changes.txt"; fi
python3 -I "$here/render.py" "$out" "$ws" "$case" "$arm"
exit $rc
