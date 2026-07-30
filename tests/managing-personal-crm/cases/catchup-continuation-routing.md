# Catch-up continuations resume the visible stage without applying

Provenance: PR review follow-ups (2026-07-26) — continuation replies could
be mistaken for effect approval and later triage bundles skipped the
relationship-contract load; folds the inventory-decision, disposition,
triage-first, and completion variants.

## Prompt

> A visible synthetic catch-up recap shows a proposed source inventory and,
> later, stage-one bundles. For each reply, state what continues, what is
> loaded first, and whether anything is written.
>
> 1. "The inventory is right. Keep Person notes and Messages required, drop
>    WhatsApp, and continue the preflight."
> 2. Required probes then pass; the first stage-one bundle is prepared.
> 3. "For the visible batch: 1 active, 2 merge into Taylor Reed, 3
>    reference, 4 delete." More Person notes remain.
> 4. Would stage one gather rich history before retention decisions?
> 5. Every path now has a reviewed disposition, but one retained person's
>    stage-two reconstruction is deferred and one approved cleanup is still
>    pending. May the run report catch-up complete?

## Expected behavior

- [ ] 1 → recognized as an inventory decision, not a destination effect; the
      exact preflight continues with only the confirmed scope.
- [ ] 2 → loads the relationship contract before inspecting the first Person
      note; its target schema and legacy mappings govern triage.
- [ ] 3 → records the reviewed dispositions in the visible recap and reloads
      the contract before the next bundle; `merge` and `delete` authorize no
      mutation or cleanup.
- [ ] 4 → no: stage one triages dispositions only; rich reconstruction waits
      for retained people in stage two.
- [ ] 5 → no: deferred reconstruction and unproven cleanup end the turn
      Partial or Paused, never complete.
