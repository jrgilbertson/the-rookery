# Action replies route to the visible bundle, not rediscovery

Provenance: proactive review (2026-07-26) — deferred embedded actions
originally risked re-discovery and renumbering on revisit.

## Prompt

> A visible meeting bundle holds numbered actions; some are decided, action 3
> is deferred, action 4 was skipped as a terminal decision. For each later
> user message, state what the workflow does and does not do.
>
> 1. `Approve action 2.`
> 2. `Resume the deferred action 3.` (an overlapping scheduled run fired in
>    between)
> 3. Every action in the bundle is now applied, already satisfied, or
>    terminally skipped; a later overlapping run processes the same window.
> 4. The user skipped action 4 earlier; other actions are still pending. What
>    is the meeting's disposition?
> 5. `Approve action 2, and also check for new meetings.`

## Expected behavior

- [ ] 1 → applies against the exact visible bundle; no meeting rediscovery,
      broad source query, or unrelated proposal.
- [ ] 2 → returns the existing action 3 to review with its original numbering;
      the scheduled run may have reminded but never regenerated, renumbered,
      or recomputed it.
- [ ] 3 → the meeting is **Reviewed in this conversation**; the bundle is not
      regenerated, and no durable marker is invented to record this.
- [ ] 4 → **Already pending**; a skipped action is not a whole-meeting
      dismissal and does not hide the remaining actions.
- [ ] 5 → application finishes first; discovery follows as a separate
      read-only phase.
