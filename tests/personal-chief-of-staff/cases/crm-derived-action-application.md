# CRM-derived actions keep the chief-of-staff contract

Provenance: PR-review follow-ups (2026-07-26) — approved CRM-derived effects
risked generic-fallback application, duplicate creation, and nested CRM
bundles; folds the applied, unavailable, equivalent, novel, ambiguous, and
communication-text variants. Companion-internal application mechanics are
owned by the managing-personal-crm suite.

## Prompt

> Each scenario approves exactly one displayed action from a visible
> chief-of-staff bundle, derived from the relationship context of Rowan, a
> synthetic contact. State each action's result and who reports it.
>
> 1. Add displayed durable context to Rowan's Person note; the relationship
>    companion is available.
> 2. Create the displayed dated relationship Task; companion unavailable.
> 3. Create the displayed repository issue; an equivalent issue with a
>    different title appeared after the bundle was reviewed.
> 4. Create the displayed repository issue; the equivalence search finds no
>    equivalent.
> 5. Add the displayed writing idea to the exact backlog shown; similar
>    ideas exist but equivalence stays ambiguous.
> 6. The action is displayed communication text, either approved unchanged
>    or edited before approval.

## Expected behavior

- [ ] All → the action number, result, and completion state stay with the
      chief-of-staff bundle; no nested CRM bundle, renumbering, generic
      fallback path, redirected destination, or new review discovery.
- [ ] 1 → applies through the embedded companion with a pre-write re-read of
      the exact Person note and post-write readback.
- [ ] 2 → reports manual and leaves the Task unapplied.
- [ ] 3 → reports already satisfied and performs no write.
- [ ] 4 → applies exactly once, reads back the exact target, and does not
      retry an indeterminate result.
- [ ] 5 → reports manual rather than treating a title difference as novelty.
- [ ] 6 → keeps the text conversational: unchanged approval is already
      satisfied, an edit needs new exact approval, and nothing is sent or
      saved as a draft or artifact.
