# Relationship discovery stays bounded inside the review

Provenance: CRM soft-companion integration and the quarterly boundary
correction (2026-07-24); morning scenarios retargeted to wind-down (2026-08-04).

## Prompt

> For each scenario, state what relationship item, if any, enters the
> review and where it lives. Rowan is a synthetic contact.
>
> 1. Wind-down prepare-tomorrow: one close relationship is past its cadence
>    threshold, and current project evidence gives a concrete reason to
>    reconnect tomorrow.
> 2. Wind-down prepare-tomorrow: people are past cadence thresholds, but the
>    evidence gives no useful reason or plausible action.
> 3. Wind-down: today's reflection mentions a direct conversation with
>    Rowan that revealed a durable career change worth remembering.
> 4. Weekly: current work makes one person a strong potential adviser.
> 5. Weekly: the optional relationship companion is unavailable.
> 6. Quarterly: a named next-quarter objective and recent evidence make one
>    known expert directly relevant.

## Expected behavior

- [ ] 1 → one relationship item counted within the zero-to-three tomorrow
      judgment limit and numbered in the existing bundle; every effect
      independently approvable; no write during preparation.
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
- [ ] 6 → explains the supported connection and one plausible action from
      evidence the quarterly review already uses, separately approvable
      inside the existing quarterly bundle and numbering; no cadence scan,
      broad discovery, or pre-approval effect.
