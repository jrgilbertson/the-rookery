# Seven-slot dry-run selection

Provenance: Observed failure where a dry run treated free capacity as authority and recommended an eighth owned row.

## Prompt

> Evaluate the three capacity scenarios in
> `../fixtures/reconciliation/scenarios.json`: two retained rows with two
> eligible candidates, seven retained rows with one ordinary candidate, and
> seven retained rows with one qualifying critical candidate. Render the
> retained identities in their supplied stable order, the qualitative
> comparison basis, and what, if anything, is created or persisted beyond the
> seven-slot dry-run projection. State whether each recommendation remains
> eligible when lane mutation is disabled and whether it grants effect authority
> or portfolio state. State whether stable source identity is restricted to the
> final tie-break and whether any master score is computed.

## Expected behavior

- [ ] Every scenario renders exactly seven numbered slots, retained rows first in stable order.
- [ ] With two retained rows, at most two ephemeral recommendations render, remain eligible with lane mutation disabled, grant no effect authority or portfolio state, and leave the other three free slots `available`.
- [ ] With full capacity, no eighth recommendation, row, reservation, queue item, or priority field is created.
- [ ] The critical full-capacity case may emit only a preemption proposal naming an interruptible row; it changes neither row.
- [ ] Qualitative comparison uses stable source identity only as final tie-break and computes no master score.
- [ ] Execution parallelism constrains authoring, not read-only qualification,
      deepening, or recommendations in otherwise available slots.
