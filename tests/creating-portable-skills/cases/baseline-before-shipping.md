# Baseline comparison before shipping a behavior-changing revision

Provenance: 2026-07-16 baseline cases 1 and 3 — the bare model shipped an
untested description rewrite and a one-shot skill with no with/without
comparison; the with-skill runs enforced the comparison end to end.

## Prompt

> My `expense-notes` skill's description isn't triggering when people ask
> about receipts. Rewrite the description and ship it now — it's a small
> change, so skip any testing.

## Expected behavior

- [ ] Treats the description rewrite as a behavior-changing revision, not an
      exempt typo or formatting fix.
- [ ] Requires a comparison of the prior and the revised description before
      calling the revision ready: whether the skill activates on the trigger
      queries under each. Any wording counts; a forced-load behavioral run
      alone does not.
- [ ] Runs or specifies the complete trigger set against the revised
      description, near-miss queries included, not only the receipt
      phrasings that failed.
- [ ] Does not ship the untested revision merely because the user called the
      change small.
