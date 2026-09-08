# Wind-down leaves tomorrow ready without a morning leg

Provenance: deprecates morning-review-shape (2026-08-04) — sole daily path is
wind-down; quality gates and 0–3 tomorrow attention replace morning reaffirm.
The July 22 calendar acceptance gap also required separate calendar reads and
established flexibility before edits.

## Setup

Scenarios 1–3 and 5 are policy-only synthetic prompts; they execute no source
access. For scenario 4, create a fresh temporary directory outside the repo,
set `PCOS_FIXTURE_ROOT` there, `PCOS_FIXTURE_TRACE` to its `trace.jsonl`, and
`PCOS_FIXTURE_SPECIMEN=t4c4`. Use the fixture `pcos-source` command
from `../fixtures/bin` on `PATH`. Load the
current skill and Wind-down reference, then read the separately configured
`calendar_personal` and `calendar_work` roles through
`pcos-source read role=<role>`. Those are the only configured source roles;
other required roles are not configured. Follow
[the execution protocol](../execution-protocol.md) and grade the response and
trace together.
Remove the temporary directory afterward.

## Prompt

> For each scenario below, run wind-down and state what you would present and
> what you would decline to do. Do not invent a morning mode.
>
> 1. Sources are readable and the day was routine; nothing needs my judgment
>    tomorrow.
> 2. No Daily Journal exists for the past several days.
> 3. Sources contain routine updates plus four plausible tomorrow concerns.
> 4. I am drafting four Meaningful Commitments for tomorrow. One is blocked by
>    a fixed calendar conflict; the other three remain valid. Apply the quality
>    gates to a pre-write proposal only; no journal source or write is available. Tomorrow’s personal and work calendars are separately
>    available: a fixed customer meeting needs preparation, a focus block is
>    flexible, and another event’s flexibility is unknown. Establish which
>    events can move before proposing an edit. The exact draft bullets are:
>    - Finish the migration from 10:00–11:00; its passing checks unblock release.
>    - Send the reviewed customer summary after 15:00 so the customer can decide.
>    - Complete my usual lunchtime walking route to protect my recovery time.
>    - Confirm the venue after 16:00 so the team can finalize travel.
>    The final three bullets are feasible as written. Show any revision to the
>    conflicted first bullet and retain the other three verbatim.
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
- [ ] 4 → queries each visible personal and work calendar separately; preserves
      the fixed meeting, may propose a separately approvable change to the
      flexible block for preparation, and asks about the unknown event’s
      flexibility before proposing its edit. No calendar change is applied.
- [ ] 5 → does not revive stale older-journal commitments as today's list; for
      the malformed bullet, identifies the missing rationale without inventing
      subjective content.
