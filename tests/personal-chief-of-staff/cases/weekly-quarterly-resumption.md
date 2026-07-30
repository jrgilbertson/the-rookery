# Weekly and quarterly reviews resume without backfill

Provenance: quarterly acceptance scan (2026-07-22) — per-calendar querying
and question-bound health analysis were ambiguous until corrected; folds the
weekly and quarterly resumption variants.

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

## Expected behavior

- [ ] Both → begins with an executive synthesis, progressively discloses
      evidence, and names gaps only where they limit a conclusion.
- [ ] Both → prepares exactly one current review; no backfilled reviews,
      journals, or invented subjective history.
- [ ] Both → keeps causal patterns, strategy, tradeoffs, writing claims, and
      the few ranked outcomes user-owned; proposes advancing at most one or
      two writing pieces with the publishing decision left to the user.
- [ ] 2 → starts no causal or correlation health analysis without a named
      decision, an agreed observation window, and evidence that could
      change an action.
- [ ] Both → keeps the review and every related source change independently
      approvable, and writes nothing merely because a scheduled invocation
      fired.
