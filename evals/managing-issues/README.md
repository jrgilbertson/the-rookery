# Managing Issues Skill Eval

[Password reset with a plus sign](cases/password-reset-plus/prompt.md) is a
synthetic draft-only case. It runs against a fresh Claude Baseline and against
the same revision of `managing-issues` in Claude and Codex. Claude can read
files and invoke a skill. Codex uses a read-only workspace without network
access for agent commands. The workspaces have no tracker configuration.

## Run on Linux

Use Node.js 22.22 or later, npm, Git, Bash, Python 3 and GNU `timeout`. The
launcher uses existing Claude Code and Codex logins with file-backed
credentials. It stages only the skill under test and points the SDKs at those
credentials from separate, private temporary homes.

With approval for model usage, run from the repository root:

```sh
work=$(bash evals/managing-issues/prepare.sh)
bash evals/managing-issues/run.sh "$work" claude-skill
bash evals/managing-issues/run.sh "$work" claude-baseline
bash evals/managing-issues/run.sh "$work" codex-skill
```

Pass a Git revision to `prepare.sh` to rerun a specific version of the skill.
Each invocation uses a fresh agent turn. The launcher disables Promptfoo caching,
sharing and telemetry. Claude's per-run ceiling is $0.95. The Codex SDK reports
usage but exposes no dollar ceiling. Check usage between arms against your budget.

## Read the results

Promptfoo writes a local `results-<arm>.json`. Its assertions check the three
issue sections, four numeric leverage scores, and the recorded tool calls.
The command audit recognizes a limited set of read-only commands. Inspect an
unrecognized call before concluding what happened. A failed assertion can make
Promptfoo exit 100 even when the agent finished and the output was written.
To exercise the checks offline, run
`node evals/managing-issues/cases/password-reset-plus/check-fixtures.mjs`.

For an Eval Record, match the results' session IDs to the transcripts under
`claude-home/projects/` and `codex-home/sessions/` in the temporary run directory.
Read all turns, session context, calls and results, then save a reviewed transcript
with the record. The operator supplies the final Eval Labels and reasons. Keep
the raw results, session logs and credentials outside the repository. See the
[runner bake-off record](records/2026-11-19-runner-bakeoff/README.md).
