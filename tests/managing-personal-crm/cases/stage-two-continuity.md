# Stage-two replies continue the current person without restart

Provenance: PR review follow-ups (2026-07-26) — stage-two continuations
could restart discovery or skip the relationship-contract load; folds the
interpretation-correction, focused-answer, and deferred-resume variants.

## Prompt

> A visible synthetic catch-up recap marks Morgan as the current stage-two
> person and Priya's reconstruction as deferred. For each reply, state what
> continues, what loads first, and whether anything is written.
>
> 1. "Your interpretation for Morgan is right, except the shared project
>    ended in May rather than June. Continue with Morgan."
> 2. Answering the focused question: "We met through the Atlas project, and
>    I expect to stay in touch."
> 3. "Resume the deferred stage-two reconstruction for Priya."

## Expected behavior

- [ ] 1 → continues Morgan's exact reconstruction, loading the relationship
      contract before inspecting the note; the correction is judgment, not
      effect approval, and nothing is written.
- [ ] 2 → stays evidence for the current person; no new inventory or triage
      bundle starts, and any resulting effect remains a separately numbered
      proposal.
- [ ] 3 → restores Priya in place from the visible recap; resume is not
      approval and triggers no recheck or write.
- [ ] Across all three, reconstructed prose carries only
      relationship-load-bearing meaning and a populated legacy `next_touch`
      stays visible until its canonical task equivalent is resolved.
