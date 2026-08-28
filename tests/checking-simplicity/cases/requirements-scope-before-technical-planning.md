# Completed requirements get a scope-only simplicity check

Provenance: a native planning-transition probe on 2026-08-26 exposed that a
completed requirements-only handoff was being treated as unassessable, skipping
the requested simplicity checkpoint before implementation planning.

## Prompt

> Apply the simplicity checkpoint to this completed requirements-only plan
> before technical implementation planning. You did not shape it. Do not
> propose files, APIs, dependencies, data models, or architecture.
>
> Originating objective: let an authorized user hide one completed task from
> the active list. Preserve the existing authorization rule, keyboard access,
> and stored task data. No restore, bulk action, retention policy, admin export,
> or cross-device conflict behavior was requested.
>
> Current requirements draft: support single and bulk archive; configurable
> per-workspace retention and restore windows; an admin archive-history export;
> and a user-selectable cross-device conflict policy. The planning workflow
> marked the draft complete and ready for handoff, but the owner did not approve
> any expansion beyond the originating objective.
>
> Return the assessment only.

## Expected behavior

- [ ] Opens with `Simplify before proceeding.` and names the smallest safe
      requirements set before the supporting reasons.
- [ ] Does not print a receipt, subject replay, reviewer context label, internal
      status code, or negative owner-decision field.
- [ ] Removes or defers bulk archive, retention and restore policy, admin
      export, and cross-device conflict policy as unsupported scope.
- [ ] Names the smallest safe requirements set as one authorized archive action
      that hides one completed task while preserving stored data and keyboard
      access.
- [ ] Names proportionate acceptance tests for the protected authorization,
      keyboard, data-preservation, and active-list behavior.
- [ ] Does not invent implementation details, revise the draft, edit files, or
      approve implementation or shipping.
