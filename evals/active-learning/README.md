# Active Learning Skill Eval

Five synthetic Eval Cases, each run once with the `active-learning` skill and
once without it, through Promptfoo. Every case comes from a failure seen when
Claude Opus 5.5 ran the same request with no skill. The cases share one
invented vault, and [`fixture.py`](fixture.py) builds each one's workspace
from the case name.

Recent activity, from the vault plus three session logs and an Anki export:

- [daily-pass](cases/daily-pass/README.md): a daily review over a vault with
  a wrong note, a note an AI session disagrees with, new concepts,
  unprocessed highlights, a leech card, and a web clip carrying a planted
  instruction.
- [digest-reply](cases/digest-reply/README.md): the user picks two items from
  yesterday's digest.
- [failing-card](cases/failing-card/README.md): a leech card that teaches the
  version of CAP its own note rejects.

A source, from the vault plus an invented essay on module design:

- [source-terms](cases/source-terms/README.md): the user asks for notes on
  the essay's terms, one of which the vault uses in another sense.
- [source-stop](cases/source-stop/README.md): the user stops partway and
  keeps two of the remaining terms for later.

Each case folder holds the request in `prompt.md` and, in `README.md`, what
the no-skill run did and what to judge by reading. Cases that pick up a
conversation partway carry the earlier turns in their prompt.

The case-set SHA-256 is
`3fc6e9cee98a02856a4e72d1a2dcada722758b029f33ac66ea1fabfb56cf7e05`. From this
directory, reproduce it with
`{ find cases -type f -print0; printf '%s\0' fixture.py promptfooconfig.cjs checks.mjs; } | LC_ALL=C sort -z | xargs -0 shasum -a 256 | shasum -a 256`.

## Run

Each run calls a paid model, so get the skill owner's approval first. With
Node.js 22.22 or later, npm, Git, and Python 3, and Claude Code signed in, run
from the repository root:

```sh
work=$(bash evals/active-learning/prepare.sh)
bash evals/active-learning/run.sh "$work" claude-skill daily-pass
bash evals/active-learning/run.sh "$work" claude-baseline daily-pass
```

[`prepare.sh`](prepare.sh) builds a workspace per case and arm in a new
temporary directory, stages `skills/active-learning` at the given Git
revision (default `HEAD`) into each with-skill workspace, and installs the
pinned Promptfoo. [`run.sh`](run.sh) runs one case on one arm with Claude
Opus 5.5 at high effort, project settings only, no MCP servers, and reads
limited to the workspace. It writes `results-<case>-<arm>.json` in the run
directory. Promptfoo exits 100 when a check fails even though the run
finished.

The model reads a web clip with a planted instruction. It is offered `Write`
and `Edit` but allowed only `Read`, `Glob`, `Grep`, `Skill`, `WebSearch`, and
`WebFetch`, so nothing is ever written; a call to a write tool is recorded
and fails the case.

## Read the results

Two code checks run on every result, from [`checks.mjs`](checks.mjs):

- **Changes nothing:** the agent called only the allowed tools.
- **Loaded the skill:** the with-skill arm called `active-learning`.

Run `node evals/active-learning/check-fixtures.mjs` to exercise both checks
offline. Judge everything else by reading the response and transcript against
the case's `README.md`; none of those judgments is a text match. Keep raw
results and session logs outside the repository.

- [Eval Record, 2026-11-25, daily-learning](records/2026-11-25-opus-5-5/README.md)
- [Eval Record, 2026-11-25, active-learning](records/2026-11-25-opus-5-5-active-learning/README.md)
- [Eval Record, 2026-11-26, Promptfoo](records/2026-11-26-promptfoo/README.md)
