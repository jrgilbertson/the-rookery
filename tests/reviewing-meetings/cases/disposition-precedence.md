# Disposition precedence across durable and conversational state

Provenance: U1 regression contract — folds the exact-duplicate, collision,
conversation-suppression, precedence, and cross-provider-ID variants; the
bare model had no disposition vocabulary or precedence order.

## Prompt

> For each scenario below, state the disposition for the meeting (or, for
> scenario 6, the suppression consequence) and whether any durable check
> still runs. Every meeting is completed with sufficient generated notes
> unless stated otherwise.
>
> 1. One approved note contains the exact source-and-ID pair
>    (`synthetic`/`meeting-d1`); the live template read is unavailable.
> 2. Two approved notes each contain the exact pair (`synthetic`/`meeting-d2`).
> 3. The latest visible instruction in this conversation exactly dismissed the
>    whole meeting (`synthetic`/`meeting-d3`); the filename convention is
>    unavailable.
> 4. An exact pending proposal for (`synthetic`/`meeting-d4`) is visible with
>    no later whole-meeting dismissal.
> 5. One exact approved note and an older pending proposal are both visible
>    for (`synthetic`/`meeting-d5`).
> 6. Two configured providers both return native ID `meeting-d6`; a pending
>    proposal exists for provider `alpha` only. What does that mean for
>    provider `beta`'s meeting?
> 7. Two approved notes contain the exact pair (`synthetic`/`meeting-d7`),
>    and an exact pending proposal for the same pair is also visible.
> 8. Required source access for (`synthetic`/`meeting-d8`) cannot establish
>    the meeting's identity, while an exact pending proposal is visible.

## Expected behavior

- [ ] 1 → **Already approved**; the exact approved note suppresses creation
      even with the template unavailable.
- [ ] 2 → **Collision stop**.
- [ ] 3 → **Dismissed in this conversation**; no filename is derived.
- [ ] 4 → **Already pending**; no template or filename work.
- [ ] 5 → **Already approved** (approved outranks pending).
- [ ] 6 → provider `beta` is not suppressed; every comparison uses the exact
      source-and-ID pair, and a title, ID-only, or substring match never
      suppresses a meeting.
- [ ] 7 → **Collision stop**; a collision outranks any conversational state.
- [ ] 8 → **Unable to prepare**; unestablishable required identity outranks
      every lower disposition, including the pending proposal.
