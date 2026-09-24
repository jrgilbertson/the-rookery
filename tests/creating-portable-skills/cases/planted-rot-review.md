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

- [ ] Flags the "now works differently since the March incident … PR 212"
      line as history or migration-relative phrasing (Sediment, by any name),
      and its fix drops the incident and the PR reference. Restating the
      column order as a plain present-tense fact and cutting the sentence
      outright both pass; keeping the incident framing or the PR reference,
      or only adding a caveat around it, fails.
- [ ] Flags the repeated header instruction as a workaround for a named
      model and proposes removing it or re-testing it, not keeping it as is.
- [ ] Flags the `csvtool 1.0.7` and `--no-inference` claim as a hardcoded
      fact with no source of truth or verification.
- [ ] Does not list the "customer no longer exists" sentence as a defect; if
      it mentions the sentence, it treats it as ordinary domain prose that
      stands.
- [ ] Does not call the row-count, decimal, or handoff-note completion
      criterion wrong, inadequate, or in need of replacement. Proposing an
      added check or a specification the fixture lacks passes.
