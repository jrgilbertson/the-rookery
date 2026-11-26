# Active Learning Skill Eval

Eleven synthetic Eval Cases, each run once with the `active-learning` skill
and once without it. Every case comes from a failure seen when Claude Opus 5.5
ran the same request with no skill. The cases share one invented vault, and
[`fixture.py`](fixture.py) builds each one's workspace from the case name.

Recent activity, from the vault plus three session logs and an Anki export:

- [daily-pass](daily-pass/case.yaml): a daily review over a vault with a wrong
  note, a note an AI session disagrees with, new concepts, unprocessed
  highlights, a leech card, and a web clip carrying a planted instruction.
- [digest-reply](digest-reply/case.yaml): the user picks two items from
  yesterday's digest.
- [failing-card](failing-card/case.yaml): a leech card that teaches the
  version of CAP its own note rejects.
- [quiet-day](quiet-day/case.yaml): nothing changed in the vault and the only
  session is a dependency bump.

A source, from the vault plus an invented essay on module design:

- [source-terms](source-terms/case.yaml): the user asks for notes on the
  essay's terms, one of which the vault uses in another sense.
- [source-stop](source-stop/case.yaml): the user stops partway and keeps two
  of the remaining terms for later.
- [source-unreadable](source-unreadable/case.yaml): the essay is cut off by a
  paywall.

A topic or a single concept, from the vault alone:

- [topic-frontier](topic-frontier/case.yaml): what the user doesn't know
  about distributed systems.
- [frontier-pick](frontier-pick/case.yaml): the user picks one frontier item
  to learn.
- [free-time](free-time/case.yaml): the user has half an hour free.
- [single-note](single-note/case.yaml): a note for one named concept, with no
  source.

The cases that pick up a conversation partway carry the earlier turns in
their prompt.

Each case folder uses the skill-creator layout: `prompt.md`, `case.yaml`,
one statement per file in `graders/`, and `place-files.sh`, which builds the
case's workspace in the current directory.

The case-set SHA-256 is
`4132d955592c137571d55c6d4daf38caae4529f064b8fd5a26d5a36f31b55bdc`. From this
directory, reproduce it with
`{ find daily-pass digest-reply failing-card free-time frontier-pick quiet-day single-note source-stop source-terms source-unreadable topic-frontier -type f -print0; printf '%s\0' fixture.py run.sh safe-git.sh; } | LC_ALL=C sort -z | xargs -0 shasum -a 256 | shasum -a 256`.

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
instructions, and adds only `skills/active-learning` at the given revision for
the `with_skill` arm. Pass a clone of the repository that holds
`atomic-note` as a fifth argument to stage it too, for the cases that hand a
note to it. It writes the event stream, a list of changed files, the final
response, and a JSON transcript of every turn, with local paths and the
user name replaced.

## Read the results

Check `file_changes.txt` first: no case asks for a change the user has not
approved, so a run with the skill should change no file. Then read `response.md` and `transcript.json`
against the case's graders. Judge by reading; none of the graders is a text
match.

- [Eval Record, 2026-11-25, daily-learning](records/2026-11-25-opus-5-5/README.md)
- [Eval Record, 2026-11-25, active-learning](records/2026-11-25-opus-5-5-active-learning/README.md)
