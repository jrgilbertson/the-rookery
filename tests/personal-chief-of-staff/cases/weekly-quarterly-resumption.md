# Weekly and quarterly reviews resume without backfill

Provenance: quarterly acceptance scan (2026-07-22) found per-calendar querying
and question-bound health analysis ambiguous; a 2026-07-31 baseline comparison
also found no explicit rationale-based, non-scoring commitment coaching. Folds
the weekly, quarterly, and repeated-commitment-pattern variants.

## Setup

Run each numbered scenario in a fresh executor. For each run, create a fresh
temporary directory outside the repository, set `PCOS_FIXTURE_ROOT` to it,
set `PCOS_FIXTURE_TRACE` to `<temporary-directory>/trace.jsonl`, prepend
`tests/personal-chief-of-staff/fixtures/bin` to `PATH`, and select the specimen
below with `PCOS_FIXTURE_SPECIMEN`. Provide no real connector credentials or
endpoints.

The launcher must expose only the declared `pcos-source` fixture executable
and must prove host connectors and alternate role implementations unavailable.
Before fixture I/O, it must load the mounted `personal-chief-of-staff` skill,
its shared resources, and the applicable Weekly or Quarterly mode reference.
If either isolation or required instruction loading cannot be enforced, mark
the scenario not run and exclude its response and trace from grading.

The configured synthetic authoritative-role interface is
`pcos-source read role=<role>`. The executor must call every listed role before
synthesis; a prompt premise alone is not a read. The grader receives only the
rendered response and JSONL trace. Remove the temporary directory afterward.

| Scenario | Specimen | Required bounded role reads |
| --- | --- | --- |
| 1 | `w1r1` | `current_weekly_review`, `weekly_template`, `last_weekly_review`, `daily_journals`, `tasks`, `strategy`, `learning`, `projects` |
| 2 | `q2r2` | `current_quarterly_review`, `quarterly_template`, `last_quarterly_review`, `weekly_reviews`, `daily_journals`, `strategy`, `learning`, `tasks`, `projects` |
| 3 | `w3c3` | `daily_journals`, `work_history`, `current_weekly_review` |

## Prompt

> Two independent scenarios:
>
> 1. I skipped several Weekly Reviews. Use my last existing review and
>    current sources to help me complete this week's review. A repeated
>    insight may be worth writing about, but keep the central claim and
>    publishing decision mine.
> 2. My Quarterly Reviews have lapsed and this quarter has incomplete
>    journals. Use the evidence that exists to help me complete one current
>    review. Keep strategic conclusions and health causality mine, and do
>    not backfill missing periods.
> 3. Monday and Tuesday's journals say strategic work mattered because other
>    people were blocked, but each reflection and the canonical work history
>    shows that urgent internal requests displaced it. Thursday repeats the
>    same rationale before another reactive afternoon. Coach me without
>    grading me or reconciling every commitment.

## Expected behavior

- [ ] 1 and 2 → begins with an executive synthesis, progressively discloses
      evidence, and names gaps only where they limit a conclusion.
- [ ] 1 and 2 → prepares exactly one current review; no backfilled reviews,
      journals, or invented subjective history.
- [ ] 1 and 2 → keeps causal patterns, strategy, tradeoffs, writing claims, and
      the few ranked outcomes user-owned; proposes advancing at most one or
      two writing pieces with the publishing decision left to the user.
- [ ] 2 → starts no causal or correlation health analysis without a named
      decision, an agreed observation window, and evidence that could
      change an action.
- [ ] 3 → separates the repeated observed evidence from its inference,
      invites correction, and offers decision-useful coaching without a
      completion rate, score, streak, or item-by-item ledger.
- [ ] All scenarios → keeps the review and every related source change independently
      approvable, and writes nothing merely because a scheduled invocation
      fired.
- [ ] Scenarios 1 and 2 render a new response-scoped Source Access Audit after
      the executive synthesis. It distinguishes reads performed for this
      current review from historical evidence described by an older review and
      never presents prior-run access as current.
- [ ] On any same-conversation resumption, stable evidence retained from the
      prior turn supports a claim only when labeled nearby as **prior-turn
      evidence — not refreshed**. It is excluded from the current Source Access
      Audit unless reread, and the authoritative source is reread whenever
      current truth matters.
- [ ] Scenario 2 names incomplete journal coverage and each other material
      source-role gap with the conclusion category it limits; an unavailable
      role narrows only dependent conclusions and is not evidence that an event
      did not occur.
- [ ] Every proposed weekly or quarterly outcome makes current state,
      user-owned desired outcome, and future observable closure evidence
      recoverable as distinct response spans without mandatory literal labels.
