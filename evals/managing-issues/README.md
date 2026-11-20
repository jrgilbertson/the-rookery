# Managing Issues Skill Eval

Each synthetic Eval Case runs against a fresh Claude Baseline and against the
same revision of `managing-issues` in Claude and Codex. The arms for a case get
the same synthetic tracker configuration in separate workspaces. Claude can
read files and invoke a skill. Codex uses a read-only workspace without network
access for agent commands. The agents have no tracker credentials or connected
tracker tools. The fixtures support draft and preview checks. Live matchback
and applying a batch are outside the run.

- [Password reset with a plus sign](cases/password-reset-plus/README.md)
- [Two export defects in a single issue](cases/file-both-single/README.md)
- [A follow-up for a backup failure](cases/follow-up-later/README.md)
- [A recurring release checklist gap](cases/recurring-gap/README.md)
- [A Linear issue mention](cases/mention-link/README.md)

## Run on Linux

Use Node.js 22.22 or later, npm, Git, Bash, Python 3, Bubblewrap, and GNU
`timeout`. The launcher uses existing Claude Code and Codex logins with
file-backed credentials. It stages only the skill under test and points the
SDKs at those logins from separate, private temporary homes. The Codex shell
profile allows reads in the active case workspace and the minimal system paths
it needs. It keeps the model login, other workspaces, and host runtime sockets
outside the shell and disables command networking.

With approval for model usage, run from the repository root:

```sh
work=$(bash evals/managing-issues/prepare.sh origin/main)
bash evals/managing-issues/run.sh "$work" claude-skill file-both-single
```

Pass a Git revision to `prepare.sh` to rerun a specific version of the skill.
Run each case once with each arm (`claude-skill`, `claude-baseline`, and
`codex-skill`). Start the next invocation after the last finishes and you've
checked the usage against your remaining budget. The launcher disables
Promptfoo caching, sharing and telemetry. Claude's per-run ceiling is $0.95.
The Codex SDK reports usage and the launcher applies a five-minute timeout.

## Read the results

Promptfoo writes a local `results-<case>-<arm>.json`. Its assertions check the
three issue sections, four numeric leverage scores, and the recorded tool calls.
The export case also counts `Problem` sections. The Linear mention case checks
for the incident identifier in the response. Each case's README lists what the
operator should judge by reading the response and transcript.
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
