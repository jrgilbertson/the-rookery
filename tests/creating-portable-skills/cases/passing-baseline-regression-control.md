# A passing baseline can protect a load-bearing contract

Provenance: an independent 2026-08-26 package review removed a load-bearing
owner-decision case solely because the bare baseline passed; the owner rejected
waiting for that behavior to fail before protecting it.

## Prompt

> Apply this package's written baseline-comparison protocol exactly; do not add
> an unwritten exception from general testing practice. I already have a
> separate failing-baseline case that proves the new skill's intended
> improvement. A second case passes both bare and skilled today, so it cannot
> demonstrate improvement, but it protects a load-bearing contract: a product
> decision must remain orthogonal to a binary simplicity verdict. May I keep
> the second case, what may I claim from it, and what happens if that control
> later fails?

## Expected behavior

- [ ] Allows the case to remain as an explicitly labeled regression control.
- [ ] Does not count the control as evidence that the new skill improves on the
      baseline.
- [ ] Says any claim of improvement must rest on a discriminating case, such
      as the separate failing-baseline case, not on the control.
- [ ] Treats a failure of the control in any run with the change as a
      regression: fix the instruction or the item and rerun, rather than
      averaging it against passing runs, and never waive it because the
      control proves no improvement.
