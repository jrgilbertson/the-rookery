# Reviewing PRs Eval Record · 2026-11-25, simplify pass

Each of the three Eval Cases, once with `reviewing-prs`, in Claude, after the
sensitive-kind hold, the per-owner merged window, the merge-queue query with
GraphQL variables, and a simplify pass on the page template and the `gh`
stand-in. The Baseline is the previous version of the skill.

- **Host and date** macOS (arm64), 2026-11-25 PST. Claude Code subscription
  sign-in.
- **Skill revision** `skills/reviewing-prs` at commit `dc81d24e`, staged as a
  copy in each run directory.
- **Cases** all three in [the case set](../../README.md#cases). The case-set
  SHA-256 was
  `0fd98be95996a55202734d2fe900d476a608787d8fedb4affd207b6165634ce9`. It
  differs from the previous record's only because the stand-in was
  refactored. Over a fixed battery of 1,074 calls across the three fixtures,
  the refactored stand-in gave the same output, exit code, trace, and final
  state as before.
- **Baseline** the skill arms of the
  [2026-11-24 record](../2026-11-24-review-page/README.md), which ran the
  same cases against `reviewing-prs` at `1de3e14c`. That record's no-skill
  arms are the last no-skill Baseline.
- **Model and effort** `claude-opus-5-5` at high effort, as recorded in every
  assistant message of the transcripts, the same as the Baseline.
- **Runner** Anthropic's `skill-creator` loop inside one Claude Code 2.1.331
  session: each run was a subagent started with the Agent tool, as in the
  Baseline.
- **Repeats and completion** one run per case. All three finished. The
  `owner-routing-and-scrubbing` run received turns 2 and 3 of its
  `turns.json`.

## Results

Checks are the statements in each case's `graders/`. Each transcript file's
`labels` holds every label with its reason, and `unmeasured` holds the checks
a run could not exercise.

| Case | Transcript | Checks passed | Baseline (`1de3e14c`) | GitHub writes | Output tokens | Seconds |
| --- | --- | --- | --- | ---: | ---: | ---: |
| [owner-routing-and-scrubbing](../../cases/owner-routing-and-scrubbing/README.md) | [Claude with skill](owner-routing-and-scrubbing-claude-skill.json) | 4/4, 5 unmeasured | 4/4, 5 unmeasured | 0 | 29,472 | 288 |
| [conflicts-impact-digest-html](../../cases/conflicts-impact-digest-html/README.md) | [Claude with skill](conflicts-impact-digest-html-claude-skill.json) | 8/8 | 8/8 | 0 | 23,286 | 223 |
| [risk-overview-and-situations](../../cases/risk-overview-and-situations/README.md) | [Claude with skill](risk-overview-and-situations-claude-skill.json) | 4/4 | 4/4 | 0 | 15,350 | 145 |

The three runs used 330,288 cache-write tokens, 7,029,370 cache-read tokens,
and 68,108 output tokens over 656 seconds. Cost is unknown: the runs used a
subscription sign-in and the runner reported no price.

Seconds and the reported totals come from the runner's completion notices,
which are cumulative across a run's turns, so a multi-turn run's figures are
its last turn's. The previous record summed them; its two
`owner-routing-and-scrubbing` durations are corrected in this change.

## What the run shows

- **Nothing regressed.** Every check that passed at `1de3e14c` passed again,
  and the same five stayed unmeasured.
- **The sensitive-kind hold reaches the page.** Each run named sensitive
  kinds in its data: money on `acme/ledger-app#421` and #441, stored data and
  money on #440, and access and authorization on #426. The page put each one
  over the hold line and said why.
- **The merged window is stated per owner.** The digest run started acme's
  window 24 hours before the newest Verdict, at 2026-11-18 10:00 PST, and
  used the 72-hour default for dana-acme, which has no Verdict. It listed the
  same merges as the Baseline and kept out #411, #416, and #390.
- **The write path is prepared but still not exercised.** In
  `owner-routing-and-scrubbing`, the skill wrote four Verdict comments to its
  private round directory. Each was exactly three lines with the reviewed
  40-character head, and the #136 note left out the local path and
  `acme/payroll-internal`. It posted none of them, for the reason below.

## Limits of this run

- **Five checks are unmeasured in `owner-routing-and-scrubbing`.** The runner
  delivers turns 2 and 3 as messages from the coordinating session. The skill
  counts a Verdict and a confirmation only when the operator gives them
  directly, so the agent stopped at the echo both times. Posting, pinned
  merging, and the label swap were not exercised.
- **The runs could tell the setup was an evaluation.** The stand-in's refusal
  messages and the environment variable names name the stand-in, and the
  session's agent list, which each run saw once, named the other runs
  `eval-r1` and `eval-r2`.
- **One run per case, and no new no-skill arm.** There is no variance
  figure.
- **Isolation was by convention.** Each run reached the stand-in by sourcing
  an environment file before every shell command, with no GitHub token in
  that environment, and was told not to read outside its run folder.
- **The request carried the Baseline's launcher text** after the case's
  prompt: where the environment file was, to work only through `gh`, not to
  start subagents, to read the staged skill, and where to save the reply.
- **The page opener was a logging stub**, so no run opened a browser.

The transcripts keep user and assistant messages, tool calls, and tool
results, with long results cut and marked. Run directories, host paths, and
the invented home-directory path from turn 2 are replaced with placeholders.
Internal reasoning and session context stayed in the private run directory.
