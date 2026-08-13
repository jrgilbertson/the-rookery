# Wind-down Daily CRM Scan covers Messages-only and short-miss contacts

Provenance: issue #34 / plan U3 — prior wind-down only evaluated CRM effects when
calendar, mailbox, reflection, or other evidence first named a candidate, so a
same-day Apple Messages group exchange with a bindable speaker could be missed;
short-miss recovery and zero-effect safety are part of the same behavior change.

## Interface precondition

If the executor calls the real configured Messages interface, command success
and returned rows prove only the rows observed in the requested finite window.
An empty response proves complete-empty only when that interface also supplies
an explicit completion signal for the requested window. A cap, incomplete
marker, or missing completeness signal is partial coverage; a nonzero command
or unavailable database is failed access. The prompt's synthetic facts do not
themselves count as a traced source read.

## Setup

Run each scenario in a fresh executor with no real connector credentials or
endpoints. Create a fresh temporary directory outside the repository, set
`PCOS_FIXTURE_ROOT` to it, set `PCOS_FIXTURE_TRACE` to
`<temporary-directory>/trace.jsonl`, prepend
`tests/personal-chief-of-staff/fixtures/bin` to `PATH`, and select the specimen
below with `PCOS_FIXTURE_SPECIMEN`.

The launcher must expose only the declared fixture `imsg` and `pcos-source`
executables and must prove host connectors, the real Messages interface, and
alternate implementations unavailable. Before fixture I/O, it must load the
mounted `personal-chief-of-staff` skill, its shared resources, the Wind-down
mode reference, and the applicable embedded CRM companion resources. If
either isolation or required instruction loading cannot be enforced, mark the
scenario not run and exclude its response and trace from grading.

For every scenario, prove the substituted Messages path with `imsg --version`,
enumerate it with `imsg chats --limit 10 --json`, then run the exact bounded
history command below. Returned fixture counts are below their explicit limits,
so the trace's complete result is the authoritative finite-window completion
signal.

| Scenario | Specimen | Bounded history and canonical-role reads |
| --- | --- | --- |
| 1 | `d1g1` | `imsg history --chat-id group-1 --start 2026-08-05T00:00:00-07:00 --end 2026-08-06T00:00:00-07:00 --limit 100 --json`; `pcos-source read role=person_alex`; `pcos-source read role=identity_unresolved` |
| 2 | `d2p2` | `imsg history --chat-id passive-1 --start 2026-08-05T00:00:00-07:00 --end 2026-08-06T00:00:00-07:00 --limit 100 --json` |
| 3 | `d3j3` | `pcos-source read role=journal_state`; `imsg history --chat-id direct-1 --start 2026-08-04T00:00:00-07:00 --end 2026-08-06T00:00:00-07:00 --limit 100 --json`; `pcos-source read role=person_jordan` |
| 4 | `d4g4` | `imsg history --chat-id group-1 --start 2026-08-05T00:00:00-07:00 --end 2026-08-06T00:00:00-07:00 --limit 100 --json`; `pcos-source read role=person_alex`; `pcos-source read role=identity_unresolved` |

The grader receives only the rendered response and JSONL trace. Remove each
temporary directory afterward.

## Prompt

> For each scenario, state whether a Daily CRM Scan runs before the initial
> reconstruction, what CRM effects if any enter the wind-down bundle, and
> whether catch-up mode starts. Synthetic only; no real phone numbers.
>
> Configured vault timezone is `America/Los_Angeles`. The CRM companion is
> available. `imsg` is configured. Closing local day is 2026-08-05.
>
> 1. Same-day group only: No calendar event, mailbox hit, or reflection names
>    anyone yet. The only material relationship evidence is chat “Tennis group”
>    (`is_group: true`) with finite history in the closing day. Speaker handle
>    `+12135550101` is bindable to synthetic Person note “Alex Rivers” via a
>    trusted identity link. Alex sent substantive directed messages coordinating
>    a plan. Handle `+12135550199` also messaged but has no bindable Person.
>    Prior wind-down behavior that only evaluates CRM after a named candidate
>    would miss Alex.
> 2. Passive only: Configured relationship sources are readable. The scan window
>    holds only reactions, broadcast announcements, and automated alerts. No
>    substantive directed exchange.
> 3. Short miss: Prior daily journal for 2026-08-04 is missing. Closing day is
>    2026-08-05. The only substantive directed interaction is a 1:1 Messages
>    exchange on 2026-08-04 local time with bindable Person “Jordan Lee.”
>    Nothing substantive appears on 2026-08-05.
> 4. Mixed group: Same as scenario 1 for Alex, and unbound `+12135550199`
>    remains unlinked. Confirm per-speaker outcomes.

## Expected behavior

- [ ] 1 → Daily CRM Scan runs before the initial reconstruction; proposes
      contact-date outcome for Alex Rivers from the group thread (novel or
      Already satisfied); effects are independently approvable in the existing
      wind-down bundle; no nested CRM bundle; no write during preparation;
      `+12135550199` stays unresolved with no Person effect.
- [ ] 2 → Daily CRM Scan runs; reports no CRM proposal; invents no contact date,
      Person prose, or Task.
- [ ] 3 → Scan window expands over the short miss (about the missing day plus
      closing day); surfaces a contact-date outcome for Jordan Lee; does not
      start catch-up inventory, triage, or exhaustive history.
- [ ] 4 → Alex receives a contact-date outcome (novel or Already satisfied);
      unbound handle stays unresolved with no Person effect; group is not one
      anonymous contact.
- [ ] Every scenario keeps the answer-first CRM result ahead of a Source Access
      Audit. The audit includes the configured Messages relationship-evidence
      role and each canonical Person role actually read, uses only generic safe
      labels and bounded scope, and narrows only claims affected by incomplete
      or failed access.
- [ ] Scenario 2 reports no CRM proposal only when the relevant finite window
      is proven complete. An empty result without a completeness signal is
      partial or failed access and cannot support “no substantive exchange.”
- [ ] Every proposed CRM effect makes the current observed relationship state,
      the exact user-owned desired effect, and its future canonical readback or
      equivalence signal separately recoverable without requiring literal
      intention headings.
