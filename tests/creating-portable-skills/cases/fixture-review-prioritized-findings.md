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

- [ ] Findings are specific to this file, naming at least the
      workflow-summarizing description and the rote one-question-at-a-time
      interview that re-asks already-answered questions.
- [ ] Flags as removable at least one of: the think-carefully opener
      (step 1), the double reread or delegated polish check (step 4), the
      self-declared completion (step 6). One suffices.
- [ ] Identifies the ordered temporary-sibling publication sequence in step 5
      as behavior to preserve, not ceremony.
- [ ] Presents the findings in a stated priority order (ranked, tiered, or
      severity-labeled), not as an unordered list of observations.
- [ ] Ends at the findings and leaves the choice of fixes to the user. It
      neither edits the fixture nor presents a rewritten SKILL.md as the
      applied result.
