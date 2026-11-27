# Repo Captain Skill Eval

Eight synthetic Eval Cases, each run once with the `repo-captain` skill and
once with a no-skill Baseline, on Claude through Promptfoo
(`anthropic:claude-agent-sdk` with `apiKeyRequired: false`). Every case uses
plain synthetic snapshot files for one invented repository (`acme/ledger-app`),
an invented operator (`dana-acme`), and invented issues, pull requests, diffs,
and Orca worker states. [`fixture.py`](fixture.py) builds each case's workspace
with no Git repository, no `Bash` tool, and no real GitHub or Orca access.

## Cases

One case covers each behavior group the skill must show. Add a case when a
failure returns after its fix, as
[SKILLS.md](../../SKILLS.md#improving-from-real-use) describes.

| Case | What it checks |
| --- | --- |
| [coupled-plan-versus-uniform-backlog](cases/coupled-plan-versus-uniform-backlog/README.md) | Scouts `main` first (skips `#512` already fixed by `#498`), plans coupled export issues together into an ephemeral plan before dispatching, and sends independent leaves to `lfg` |
| [overlap-and-one-migration](cases/overlap-and-one-migration/README.md) | Serializes leaves overlapping active workers or external PRs, enqueues at most one database migration at a time, and swaps labels only after `MERGED` |
| [direction-change-restarts-executor](cases/direction-change-restarts-executor/README.md) | Stops an active Executor building a dropped direction with `worker-stop`, restarts on a complete brief, leaves unrelated workers alone, and records the change in state |
| [hold-gate-raises-scores](cases/hold-gate-raises-scores/README.md) | Merges routine PRs pinned to head, holds schema/UI/CI-workflow PRs with receipts, raises stored issue scores upward with audit trail, and never lowers scores |
| [rebase-revert-and-merge-queue](cases/rebase-revert-and-merge-queue/README.md) | Compares reviewed vs current heads after a rebase, enqueues a clean rebase pinned to current head, sends a quiet revert back with a new hold receipt, re-enqueues on ejection, and swaps labels only after `MERGED` |
| [domain-lead-custody-and-self-merge](cases/domain-lead-custody-and-self-merge/README.md) | Merges a Domain Lead's routine PR itself, holds Captain-authored PRs, retires only finished Leads with `worker-release`, and defers overlapping new leaves |
| [held-pr-keeps-wake-and-calm-alert](cases/held-pr-keeps-wake-and-calm-alert/README.md) | Stays quiet on no-op wakes, stops merging and opens a held revert PR with one calm alert after red default-branch CI, never repeats open alerts, and keeps the wake timer armed for held PRs |
| [restart-split-brain-and-boundaries](cases/restart-split-brain-and-boundaries/README.md) | Stands down while an earlier Captain is live, reconciles exited vs unverifiable workers on takeover, ignores forged verdicts, reports untrusted fork prompt-injection as a finding, and keeps human-only actions with the operator |

Each case folder holds the single-turn request in `prompt.md` and human-read
judgment statements in `README.md`. Cases that span multiple wakes or operator
turns carry prior context in `prompt.md` and sequential state snapshots under
`wakes/` or `github/`. Fixture dates are fixed around 2026-11-20.

The eight-case set SHA-256 is
`9bb5f58fb043a315b72a3a32f63e030e5424cbbd049ee7b7c9638adf632366c5`. From this
directory, reproduce it with:

```sh
{ find cases -type f -print0; printf '%s\0' fixture.py promptfooconfig.cjs checks.mjs; } | LC_ALL=C sort -z | xargs -0 shasum -a 256 | shasum -a 256
```

[`trigger-queries.json`](trigger-queries.json) holds requests that should load
the skill and near misses that belong to another workflow, for tuning the
description. It is outside the case set and its hash.

## Run

Each live run calls a paid model, so get the skill owner's approval first. With
Node.js 22.22 or later, npm, Git, Python 3, and Claude Code signed in on macOS
or Linux, run from the repository root:

```sh
work=$(bash evals/repo-captain/prepare.sh)
bash evals/repo-captain/run.sh "$work" claude-skill coupled-plan-versus-uniform-backlog
bash evals/repo-captain/run.sh "$work" claude-baseline coupled-plan-versus-uniform-backlog
```

[`prepare.sh`](prepare.sh) builds a plain workspace per case and arm in a new
temporary directory, stages `skills/repo-captain` at the given Git revision
(default `HEAD`) into each `claude-skill` workspace (leaving `claude-baseline`
with no skill), copies [`package-lock.json`](package-lock.json), and installs
the pinned Promptfoo dependencies with `npm ci`. [`run.sh`](run.sh) runs one
case on one arm inside an isolated temporary `HOME` and `CLAUDE_CONFIG_DIR`
(preserving signed-in Claude Code subscription auth on macOS and Linux) with
Claude Opus 5.5 at high effort, project settings only, no MCP servers,
auto-memory turned off in [`promptfooconfig.cjs`](promptfooconfig.cjs), a
five-minute per-run timeout, and reads limited to the workspace. It writes
`results-<case>-<arm>.json` in the run directory. Promptfoo exits 100 when a
check fails even though the run finished.

The model is offered `Write` and `Edit` in `tools` but allowed only `Read`,
`Glob`, `Grep`, and `Skill` under `permission_mode: 'dontAsk'`, so nothing is
ever written and any write attempt is recorded and fails the case.

## Read the results

Two code checks run on every result:

- **Changes nothing:** the agent called only the allowed read-only tools,
  checked by [`checks.mjs`](checks.mjs).
- **Loaded the skill:** the agent called `repo-captain`, checked by Promptfoo's
  built-in `skill-used` assertion. It fails on every no-skill baseline run, as
  it should.

Run `node evals/repo-captain/check-fixtures.mjs` (or
`lefthook run pre-push --force`) to exercise write-tool denial, fixture
building, and `promptfooconfig.cjs`, lockfile, and launcher invariants offline
with zero model calls; the built-in skill check is not exercised offline. Judge
reasoning, custody, receipts, and merge decisions by reading the response and
transcript against each case's `README.md`. Keep raw results and session logs
outside the repository.

## Eval Records

The records below are historical runs from the previous multi-turn harness
before this suite moved to the canonical Claude-only Promptfoo template with a
no-skill Baseline. Fresh Promptfoo Eval Records will be added once paid live
runs are approved.

- [2026-11-25, first round (historical)](records/2026-11-25-first-round/README.md)
- [2026-11-25, second round (historical)](records/2026-11-25-second-round/README.md)

Commit each new record under `records/<date>-<slug>/` with the fields
[SKILLS.md](../../SKILLS.md#eval-records) lists, and keep raw runner output,
credentials, and staged run directories outside the repository.
