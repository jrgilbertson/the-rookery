# Fixture review produces prioritized, file-specific findings

Provenance: 2026-07-27/28 disposable-fixture review runs — the discriminator
was separating removable ceremony from the load-bearing safe-publication
sequence and stopping for scope approval; a bare run edits ad hoc from
generic advice without a prioritized audit.

## Prompt

> Review the skill at `../fixtures/review-target/SKILL.md` (resolve the path
> relative to this case file) and tell me what to fix. Do not edit anything
> yet.

## Expected behavior

- [ ] Reads the actual fixture file rather than answering from the request
      alone.
- [ ] Findings are specific to this file, naming at least the
      workflow-summarizing description and the rote one-question-at-a-time
      interview that re-asks already-answered questions.
- [ ] Flags the think-carefully opener, double reread, delegated polish
      check, or self-declared completion as removable ceremony.
- [ ] Identifies the ordered temporary-sibling publication sequence in step 5
      as behavior to preserve, not ceremony.
- [ ] Presents the findings as a prioritized list and stops for fix-scope
      approval without editing the fixture.
