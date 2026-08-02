# Cadence scan derives thresholds and never rewrites newer notes

Provenance: U5 package review (2026-07-24). The pre-review package could
rewrite a Person note whose canonical contact date was already newer, and it
used provider-specific task routing. Folds the weak-tie and excluded-status
variants.

## Prompt

> Run a deliberate relationship-cadence scan over four synthetic Person
> notes and state each outcome. Today is 2026-07-24 local.
>
> 1. `status: active`, `tier: 15-close`, last contacted 31 local days ago,
>    with a note naming an open thread we said we would pick up this month.
>    If I pick next Tuesday for outreach, where does that date live?
> 2. `status: active`, `tier: 500-weak-tie`, last contacted 200 days ago.
> 3. `status: dormant`, `status: reference`, and `status: ended` notes far
>    past any rhythm.
> 4. An observed interaction dated `2026-07-20`, but the note's canonical
>    `date_last_contacted` is already `2026-07-22`.

## Expected behavior

- [ ] 1 → any outreach proposal is justified by the named open thread, not
      overdue-ness alone; the chosen date routes only to the canonical task
      system, never `next_touch` or Person prose.
- [ ] 2 → derives no fixed maximum-silence threshold for the weak tie.
- [ ] 3 → excludes dormant, reference, and ended people from ordinary
      overdue exceptions.
- [ ] 4 → reports the contact-date effect as already satisfied and does not
      rewrite the note; `date_last_contacted` advances only monotonically.
