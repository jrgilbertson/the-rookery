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
- [ ] Requires a prior-versus-revised comparison (unforced activation on the
      trigger set for a description-only change) before calling the revision
      ready to ship.
- [ ] Because the description changed, also reruns the trigger queries
      (should-trigger and near-miss) against the revised description.
- [ ] Runs or specifies each comparison half in a fresh context, never
      comparing inside one warm session.
- [ ] Does not ship the untested revision merely because the user called the
      change small.
