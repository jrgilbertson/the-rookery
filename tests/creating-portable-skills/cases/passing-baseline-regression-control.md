# A passing baseline can protect a load-bearing contract

Provenance: regression control for retaining load-bearing passing-baseline
cases without claiming improvement from them, and correcting a failed control
before shipping. An independent 2026-08-26 package review removed an
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

- [ ] Keeps the named regression control without claiming it establishes
      improvement over the baseline.
- [ ] Inspects any failed grade against the original transcript, distinguishes
      behavior failure, grader/assertion error, or capture gap, and diagnoses
      changed-text attribution with the prior skill on the failing case;
      preserves original grades and leaves unresolved attribution unverified.
