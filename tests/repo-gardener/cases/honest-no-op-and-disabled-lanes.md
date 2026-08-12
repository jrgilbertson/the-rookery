# Honest no-op and disabled lanes

Provenance: Observed failure where no selected work was called a successful no-op despite missing scout evidence and disabled lanes were omitted.

## Prompt

> Run a synthetic reconcile with all lane mutations false, no gate-passing
> candidate, two retained rows, seven report slots, and one missing expected
> Scout Receipt. Then rerun with terminal coverage for every expected scout.
> Separately classify the fixture's ordinary code-health observation and
> confirmed applicable critical security exposure, both from disabled lanes.
> Render a separate, fully numbered seven-slot projection and completion fields
> for each run. For the complete run, use the fixture's
> `reconciliation_complete: true` fact. Keep the two separate disabled-lane
> observations outside both run completions; they do not change either run's
> attention state or next action.

## Expected behavior

- [ ] The missing-receipt run is `Action required`, not a Routine no-op.
- [ ] The complete run may be Routine only after row/intent reconciliation and terminal coverage for every scout.
- [ ] Ordinary disabled-lane findings render `Routine (disabled lane)` and confirmed critical exposure renders `Action required (lane disabled)`.
- [ ] Both runs render exactly seven retained-or-`available` slots.
- [ ] Complete no-op returns `next_owner_action: none`; neither run mutates source work.
