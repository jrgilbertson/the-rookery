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

- [ ] Reports a count for every mechanical signal before the judgment
      findings, including the signals with no hits.
- [ ] Fails the history item for the line that says the exporter "now works
      differently since the March incident" and cites PR 212, and proposes
      stating the current column order alone.
- [ ] Flags the repeated header instruction as a workaround for a named
      model and proposes removing it or re-testing it, not keeping it as is.
- [ ] Flags the `csvtool 1.0.7` and `--no-inference` claim as a hardcoded
      fact with no source of truth or verification.
- [ ] Lets the "customer no longer exists" sentence stand, with a stated
      reason, instead of listing it as a defect.
- [ ] Leaves the row-count, decimal, and handoff-note completion criteria in
      place as observable checks.
- [ ] Edits nothing.
