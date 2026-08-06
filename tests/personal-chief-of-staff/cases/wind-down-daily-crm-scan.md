# Wind-down Daily CRM Scan covers Messages-only and short-miss contacts

Provenance: issue #34 / plan U3 — prior wind-down only evaluated CRM effects when
calendar, mailbox, reflection, or other evidence first named a candidate, so a
same-day Apple Messages group exchange with a bindable speaker could be missed;
short-miss recovery and zero-effect safety are part of the same behavior change.

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
