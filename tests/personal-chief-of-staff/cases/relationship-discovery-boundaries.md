# Relationship discovery stays bounded inside the review

Provenance: CRM soft-companion integration and the quarterly boundary
correction (2026-07-24) — cadence-threshold outreach, nested CRM bundles,
and invented relationship data were the observed risks; folds the morning,
wind-down, weekly, and quarterly variants.

## Prompt

> For each scenario, state what relationship item, if any, enters the
> review and where it lives. Rowan is a synthetic contact.
>
> 1. Morning: one close relationship is past its cadence threshold, and
>    current project evidence gives a concrete reason to reconnect.
> 2. Morning and quarterly: people are past cadence thresholds, but the
>    evidence gives no useful reason or plausible action today.
> 3. Wind-down: today's reflection mentions a direct conversation with
>    Rowan that revealed a durable career change worth remembering.
> 4. Weekly: current work makes one person a strong potential adviser.
> 5. Weekly: the optional relationship companion is unavailable.

## Expected behavior

- [ ] 1 → one relationship item counted within the zero-to-three foreground
      limit and numbered in the existing bundle; every effect independently
      approvable; no write during preparation.
- [ ] 2 → cadence alone creates no outreach suggestion, action, or
      classification; the review simply continues.
- [ ] 3 → proposes the contact date and the narrow durable prose as separate
      actions in the existing wind-down bundle, and reports the contact
      date already satisfied when the canonical date is equal or newer.
- [ ] 4 → explains why the person matters now and names one plausible action
      inside the existing weekly bundle; no catch-up, hidden progress
      state, or automatic Task, draft, or Person-note update.
- [ ] 5 → completes the review from the remaining evidence, names reduced
      relationship coverage only if it limits a material conclusion, and
      invents no contact date, tier, status, or Person-note effect.
