# Reviewing PRs Eval Record · 2026-11-25, shared contract

Each of the four Eval Cases, once with `reviewing-prs` in Claude, after the
skill moved its formats and hold tests into the review contract it shares
with `repo-captain`. The skill now posts a Verdict even when the pull
request's head moved after review, naming the reviewed commit, and holds an
edit to the design system itself. The new verdict-at-reviewed-head case also
ran with the previous revision as its Baseline.

- **Host and date** macOS (arm64), 2026-11-25 PST. Claude Code subscription
  sign-in.
- **Skill revision** `skills/reviewing-prs` at commit `b6d3f62f`, staged as a
  copy in each run directory.
- **Cases** all four in [the case set](../../README.md#cases). The case-set
  SHA-256 was
  `3957773a8f8444049bf11652cc1df779bdf06f21bf40e08d356276203e5bb5b1`.
- **Baseline** for the three earlier cases, the
  [2026-11-25 post-only record](../2026-11-25-post-only/README.md), which ran
  `reviewing-prs` at `4f0a8a92`. For verdict-at-reviewed-head, a new run of
  `reviewing-prs` as it stood at `abd0e525`, before this change.
- **Model and effort** `claude-opus-5-5` at high effort.
- **Runner** one `claude -p --safe-mode` process per turn, later turns by
  `--resume` as real user turns, with only the `gh` stand-in on `PATH` and
  empty GitHub token variables. Safe mode loads no installed skill, so no
  installed copy could shadow the staged one.
- **Repeats and completion** one run per case and arm. All five finished,
  and every multi-turn case received all of its turns.
- **Labels** a `claude-sonnet-5-5` grader subagent labeled each check from
  the run's tool calls, replies, and the stand-in trace.

## Results

| Case | Checks passed | Baseline | Output tokens | Seconds |
| --- | --- | --- | ---: | ---: |
| [conflicts-impact-digest-html](../../cases/conflicts-impact-digest-html/README.md) | 5/8, 3 unmeasured | post-only: 8/8 | 15,272 | 182 |
| [owner-routing-and-scrubbing](../../cases/owner-routing-and-scrubbing/README.md) | 8/9 | post-only: 6/6, 3 unmeasured | 18,092 | 215 |
| [risk-overview-and-situations](../../cases/risk-overview-and-situations/README.md) | 2/4, 2 unmeasured | post-only: 4/4 | 12,810 | 146 |
| [verdict-at-reviewed-head](../../cases/verdict-at-reviewed-head/README.md) | 4/4 | `abd0e525`: 2/4 | 12,276 / 11,945 | 148 / 149 |

The five runs used 70,395 output tokens, 2,929,159 cache-read tokens, and
183,688 cache-write tokens over 840 seconds. Cost is unknown: the runs used a
subscription sign-in and the runner reported no price.

## What the run shows

- **The moved-head change works and is needed.** With the revised skill, the
  operator's merge Verdict on #470 posted at the reviewed head after the head
  moved, with a note that it moved. The previous revision posted nothing for
  #470 and never said who judges the change since review.
- **Owner routing now posts Verdicts.** This runner delivers the later turns
  as the operator's own, so the three checks the post-only record left
  unmeasured were measured, and they passed.
- **One new failure.** In owner-routing-and-scrubbing, the fork from an
  outside contributor (#134) was described as waiting on its author, without
  telling the operator to merge it or hand it on. Step 5 already says a pull
  request with an external author waits for the operator, so this is the
  first time this failure appears, and it is kept here as an observation.
- **Page checks were unmeasured, not failed.** The grader saw the run's
  replies and trace, not the page it built, so the CSP, escaping, file mode,
  and per-value source checks could not be decided.

## Limits of this run

- **The page is not in the evidence.** Five checks across two cases need the
  built page.
- **One run per case.** There is no variance figure.
- **The runs could tell the setup was an evaluation.** The stand-in's refusal
  messages name it.

The transcripts keep user and assistant messages, tool calls, and tool
results, with long results cut and marked. Run directories, home and
temporary paths, and the account name are replaced with placeholders.
