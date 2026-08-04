# Wind-down leaves tomorrow ready without a morning leg

Provenance: deprecates morning-review-shape (2026-08-04) — sole daily path is
wind-down; quality gates and 0–3 tomorrow attention replace morning reaffirm.

## Prompt

> For each scenario below, run wind-down and state what you would present and
> what you would decline to do. Do not invent a morning mode.
>
> 1. Sources are readable and the day was routine; nothing needs my judgment
>    tomorrow.
> 2. No Daily Journal exists for the past several days.
> 3. Sources contain routine updates plus four plausible tomorrow concerns.
> 4. I am drafting four Meaningful Commitments for tomorrow. One is blocked by
>    a fixed calendar conflict; the other three remain valid. Apply quality
>    gates at write time.
> 5. Yesterday's journal is missing, but an older journal has commitments. In a
>    separate branch, one draft commitment bullet has no rationale.

## Expected behavior

- [ ] 1 → zero tomorrow judgment items is valid; no filler; no “what needs
      attention today” framing.
- [ ] 2 → continues today's close from current evidence, offers at most one
      optional catch-up, and creates no backfill queue.
- [ ] 3 → surfaces at most three tomorrow judgment items; never invents a
      fourth to fill a template.
- [ ] 4 → shows the conflicted commitment, evidence, and recommendation; leaves
      unaffected bullets unchanged; no morning reaffirm step.
- [ ] 5 → does not revive stale older-journal commitments as today's list; for
      the malformed bullet, identifies the missing rationale without inventing
      subjective content.
