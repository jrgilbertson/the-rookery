# Weekly and quarterly reviews resume without backfill

Provenance: quarterly acceptance scan (2026-07-22) found per-calendar querying
and question-bound health analysis ambiguous; a 2026-07-31 baseline comparison
also found no explicit rationale-based, non-scoring commitment coaching. Folds
the weekly, quarterly, and repeated-commitment-pattern variants.

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
