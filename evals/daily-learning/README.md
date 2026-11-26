# Daily Learning Skill Eval

Four synthetic Eval Cases, each run once with the `daily-learning` skill and
once without it. Every case comes from a failure seen when Claude Opus 5.5 ran
the same request with no skill. The cases share one invented vault, three
session logs, and an Anki export, built by [`fixture.py`](fixture.py).

- [daily-pass](daily-pass/case.yaml): a daily review over a vault with a wrong
  note, a note an AI session disagrees with, new concepts, unprocessed
  highlights, a leech card, and a web clip carrying a planted instruction.
- [digest-reply](digest-reply/case.yaml): the user picks two items from
  yesterday's digest.
- [failing-card](failing-card/case.yaml): a leech card that teaches the
  version of CAP its own note rejects.
- [quiet-day](quiet-day/case.yaml): nothing changed in the vault and the only
  session is a dependency bump.

Each case folder uses the skill-creator layout: `prompt.md`, `case.yaml`,
one statement per file in `graders/`, and `place-files.sh`, which builds the
case's workspace in the current directory.

The case-set SHA-256 is
`646316a7c9090ef8dd472918832474955b25573bf2ab2c5b919fb78ba9bf7077`. From this
directory, reproduce it with
`{ find daily-pass digest-reply failing-card quiet-day -type f -print0; printf '%s\0' fixture.py run.sh safe-git.sh; } | LC_ALL=C sort -z | xargs -0 shasum -a 256 | shasum -a 256`.

## Run

Each run calls a paid model, so get the skill owner's approval first. The
model runs as you and reads a web clip with a planted instruction. `run.sh`
routes Git through [`safe-git.sh`](safe-git.sh), which always uses the
vault's repository and blocks options that write files or run commands. It
also limits edits to the workspace and makes the vault's `.git` folder
read-only.
The Read and WebFetch tools can still reach local files and the network, so
use a disposable VM or container for full isolation. With
Claude Code, Git, and Python 3, run from this directory:

```sh
./run.sh daily-pass with_skill <out-dir> [git-revision]
./run.sh daily-pass without_skill <out-dir>
```

[`run.sh`](run.sh) builds a fresh workspace, runs Claude Opus 5.5 at high effort
with no user settings, installed skills, plugins, MCP servers, or global
instructions, and adds only `skills/daily-learning` at the given revision for
the `with_skill` arm. It writes the event stream, a list of changed files, the
final response, and a JSON transcript of every turn, with local paths and the
user name replaced.

## Read the results

Check `file_changes.txt` first: every no-skill run so far edited the vault,
and no run with the skill has. Then read `response.md` and `transcript.json`
against the case's graders. Judge by reading; none of the graders is a text
match.

- [Eval Record, 2026-11-25](records/2026-11-25-opus-5-5/README.md)
