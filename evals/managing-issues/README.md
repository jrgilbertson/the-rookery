# Managing Issues Skill Eval

Three synthetic Eval Cases, each run once with the `managing-issues` skill and
once without it, through Promptfoo on macOS or Linux. The arms for a case get
the same synthetic tracker configuration (`.agents/managing-issues.json`) in
separate plain workspaces with no Git repository, no `Bash` tool, no tracker
credentials, and no connected tracker tools. The model is offered `Write` and
`Edit` but allowed only `Read`, `Glob`, `Grep`, and `Skill` in `dontAsk` mode,
so every write attempt is denied before touching disk and fails the case. The
fixtures support draft and preview checks; live matchback and applying a batch
are outside the run.

- [Password reset with a plus sign](cases/password-reset-plus/README.md)
- [A follow-up for a backup failure](cases/follow-up-later/README.md)
- [A Linear issue mention](cases/mention-link/README.md)

The current three-case set SHA-256 is
`1314e69b636612997d13f4ab29b5abd7839b85bcbd31fa2bd39768f50d33f35f`. From this
directory, reproduce it with
`{ find cases fixtures -type f -print0; printf '%s\0' promptfooconfig.cjs checks.mjs; } | LC_ALL=C sort -z | xargs -0 shasum -a 256 | shasum -a 256`.

## Run

Each run calls a paid model, so get the skill owner's approval first. With
Node.js 22.22 or later, npm, Git, Python 3, and Claude Code signed in, run from
the repository root:

```sh
work=$(bash evals/managing-issues/prepare.sh)
bash evals/managing-issues/run.sh "$work" claude-skill password-reset-plus
bash evals/managing-issues/run.sh "$work" claude-baseline password-reset-plus
```

Pass a Git revision to [`prepare.sh`](prepare.sh) to rerun a specific version
of the skill (default `HEAD`). [`prepare.sh`](prepare.sh) builds plain
workspaces per case and arm in a new temporary directory, validates the staged
tracker fixtures with `config_check.py`, stages `skills/managing-issues` into
each with-skill workspace, copies [`package-lock.json`](package-lock.json), and
installs the pinned Promptfoo and Claude Agent SDK with `npm ci`.
[`run.sh`](run.sh) runs one case on one arm (`claude-skill` or
`claude-baseline`) inside an isolated temporary `HOME` and `CLAUDE_CONFIG_DIR`
(preserving signed-in Claude Code subscription auth on macOS and Linux) with
Claude Opus 5.5 at high effort, project settings only, no MCP servers,
auto-memory turned off in [`promptfooconfig.cjs`](promptfooconfig.cjs), a
five-minute per-run timeout, a $0.95 per-run budget cap, and reads limited to
the workspace. It writes `results-<case>-<arm>.json` in the run directory.
Promptfoo exits 100 when a check fails even though the run finished.

## Read the results

Four code checks run on every result, plus a fifth on `mention-link`:

- **Changes nothing:** the agent called only the allowed read-only tools,
  checked by [`checks.mjs`](checks.mjs).
- **Loaded the skill:** the agent called `managing-issues`, checked by
  Promptfoo's built-in `skill-used` assertion. It fails on every no-skill
  baseline run, as it should.
- **Draft sections:** the response includes `Problem`, `Scope`, and
  `Verification` headings (Markdown or inline bold), checked by
  [`checks.mjs`](checks.mjs).
- **Leverage scores:** the response includes all four numeric leverage scores
  (`Impact`, `Confidence`, `Verification effort`, and `Undo cost`), checked by
  [`checks.mjs`](checks.mjs).
- **STORE-412 present** (`mention-link` only): the response mentions
  `STORE-412`, checked by [`checks.mjs`](checks.mjs).

Run `node evals/managing-issues/check-fixtures.mjs` (or
`lefthook run pre-push --force`) to exercise `checks.mjs`, historical Claude
transcript replays, and the `promptfooconfig.cjs`, lockfile, and launcher
invariants offline; the built-in `skill-used` check is not exercised offline.

Judge everything else by reading the response and transcript against each
case's `README.md`. For an Eval Record, match the result's session ID to the
transcript under `claude-home/projects/` in the temporary run directory, review
all turns, tool calls, and results, and save a reviewed transcript with the
record. Keep raw results, session logs, and credentials outside the repository.

## Historical Eval Records

The 2026-11-19 Eval Records below were captured under the previous Linux-only
Bubblewrap/Codex runner and are historical until a fresh paid macOS run is
approved:

- [Five-case Eval Record](records/2026-11-19-five-cases/README.md)
- [Runner bake-off record](records/2026-11-19-runner-bakeoff/README.md)
