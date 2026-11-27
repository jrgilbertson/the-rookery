# Reviewing PRs Skill Eval

Four synthetic Eval Cases, each run once with the `reviewing-prs` skill and
once with a no-skill Baseline, on Claude through Promptfoo
(`anthropic:claude-agent-sdk` with `apiKeyRequired: false`). Every case uses
plain synthetic snapshot files for invented repositories (`acme/ledger-app`,
`acme/cli-kit`, `acme/handbook`, `acme/payroll-internal`), an invented operator
(`dana-acme`), and invented pull requests, diffs, comments, and review threads.
[`fixture.py`](fixture.py) builds each case's workspace with no Git repository,
no `Bash` tool, and no real GitHub credentials or access.

## Cases

The set is four cases, kept small on purpose. Add a case when a failure returns
after its fix, as [SKILLS.md](../../SKILLS.md#improving-from-real-use)
describes.

| Case | What it checks |
| --- | --- |
| [owner-routing-and-scrubbing](cases/owner-routing-and-scrubbing/README.md) | Classifies an external fork with a copied `Owner:` line as untrusted, echoes verdicts before confirmation, posts three-line top-level verdict comments, scrubs a local path and private repo name from a public comment, merges nothing and changes no label, and routes next actions by valid vs conflicting vs missing ownership |
| [conflicts-impact-digest-html](cases/conflicts-impact-digest-html/README.md) | Groups overlapping PRs (`#426` and `#427` on `app/routes.ts`) with a merge order, classifies merged-window PRs since November 13 into `changedAfter`, `autoMerged`, and `without` while dropping decoys, treats hostile script/steering text in `#139` as untrusted data/finding, and specifies hardened private page rendering |
| [risk-overview-and-situations](cases/risk-overview-and-situations/README.md) | Splits open PRs at the hold line from raw diffs (`#440` with hidden `currency_exponent` column and `#441` with undescribed `Math.floor`/`Math.ceil` rounding over the hold line; `#442` footer typo under), shows the undescribed rounding situation with its code excerpt and declined bot thread, and states value sources without running PR code |
| [verdict-at-reviewed-head](cases/verdict-at-reviewed-head/README.md) | Posts `#470`'s merge verdict with `Head:` pinned to the reviewed head even after `#470` moved before confirmation, tells the operator the head moved and that `repo-captain` judges the delta, posts `#471`'s request-changes verdict at its unchanged head, and merges nothing |

Three earlier cases were removed on 2026-11-24: a mislabeled new view, hidden
stored names, and a description claiming work the diff lacked. A no-skill agent
caught each of them, so they measured the model more than the skill. Git
history keeps them. `design-system-departures` was removed the same day because
both arms passed every check.

Each case folder holds the single-turn request in `prompt.md` and human-read
judgment statements in `README.md`. Cases that span multiple operator turns
(`owner-routing-and-scrubbing` and `verdict-at-reviewed-head`) carry prior
turns directly in `prompt.md`, with pre-write reread snapshots under
`github/reread-at-confirmation/` where applicable. Fixture dates are fixed
around 2026-11-20, and the digest case's prompt names the merged window's
start, so no case depends on today's date.

The four-case set SHA-256 is
`48460e0f5fb3710917f7b4b0fc89e3a539c3d3a30d2b940b9d449dbb30079127`. From this
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
work=$(bash evals/reviewing-prs/prepare.sh)
bash evals/reviewing-prs/run.sh "$work" claude-skill owner-routing-and-scrubbing
bash evals/reviewing-prs/run.sh "$work" claude-baseline owner-routing-and-scrubbing
```

[`prepare.sh`](prepare.sh) builds a plain workspace per case and arm in a new
temporary directory, stages `skills/reviewing-prs` at the given Git revision
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
- **Loaded the skill:** the agent called `reviewing-prs`, checked by
  Promptfoo's built-in `skill-used` assertion. It fails on every no-skill
  baseline run, as it should.

Run `node evals/reviewing-prs/check-fixtures.mjs` (or
`lefthook run pre-push --force`) to exercise write-tool denial, fixture
building, and `promptfooconfig.cjs`, lockfile, and launcher invariants offline
with zero model calls; the built-in skill check is not exercised offline. The
HTML review page template itself is tested deterministically by
[`tests/reviewing-prs/fixtures/run-template-checks.py`](../../tests/reviewing-prs/fixtures/run-template-checks.py).
Judge reasoning, ownership routing, scrubbing, risk scoring, and merged-window
classification by reading the response and transcript against each case's
`README.md`. Keep raw results and session logs outside the repository.

## Eval Records

The records below are historical runs from the previous multi-turn harness
before this suite moved to the canonical Claude-only Promptfoo template. Fresh
Promptfoo Eval Records will be added once paid live runs are approved.

- [Review page, 2026-11-24 (historical)](records/2026-11-24-review-page/README.md):
  each case once with the skill and once without, in Claude.
- [Simplify pass, 2026-11-25 (historical)](records/2026-11-25-simplify-pass/README.md):
  each case once with the skill at `dc81d24e`, in Claude, against the
  previous record's skill arms.
- [Post only, 2026-11-25 (historical)](records/2026-11-25-post-only/README.md):
  each case once with the skill at `4f0a8a92`, after it stopped merging, in
  Claude.
- [Shared contract, 2026-11-25 (historical)](records/2026-11-25-shared-contract/README.md):
  each case once with the skill at `b6d3f62f`, after it moved its shared
  rules into the review contract, in Claude.

Commit each new record under `records/<date>-<slug>/` with the fields
[SKILLS.md](../../SKILLS.md#eval-records) lists, and keep raw runner output,
credentials, and staged run directories outside the repository.
