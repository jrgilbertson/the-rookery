# Review finds planted rot and leaves ordinary prose alone

Provenance: 2026-09-19 scan of the catalog — the checklist's one-line
Sediment item gave a reviewer nothing to run, and the scan's only
"no longer" hits were ordinary domain prose that a blunt rule would
have flagged.

## Prompt

> Audit the skill at `../fixtures/rot-review-target/SKILL.md` (resolve the
> path relative to this case file) against your review checklist and tell me
> what to fix. Do not edit anything.

## Expected behavior

- [ ] Reports a count for each mechanical pre-check signal, zero-hit
      signals included, rather than listing only the hits.
- [ ] Flags the "now works differently since the March incident … PR 212"
      line as history or migration-relative phrasing (Sediment, by any
      name), and the fix keeps the current column order while dropping
      the incident and PR reference.
- [ ] Flags the repeated header instruction as a workaround for a named
      model and proposes removing it or re-testing it, not keeping it as is.
- [ ] Flags the `csvtool 1.0.7` and `--no-inference` claim as a hardcoded
      fact with no source of truth or verification.
- [ ] Lets the "customer no longer exists" sentence stand, with a stated
      reason, instead of listing it as a defect.
- [ ] Does not list the row-count, decimal, or handoff-note completion
      criteria as defects.
