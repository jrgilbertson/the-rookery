# A parent owns vertical, independently verifiable children

Provenance: covers the prior skill's underspecified `vertical leaves` rule,
which did not distinguish complete outcomes from technical layers or test
whether a child could be demonstrated independently.

## Prompt

> Turn this approved account-notifications outcome into GitHub issues in
> `example/project`. Users need to choose email or in-app delivery for billing
> alerts, see the current choice after returning to settings, and receive alerts
> through the selected channel. Missed alerts have caused account delinquency,
> so the approved priority is `high`; `normal` is the other available priority.
> Available labels are `feature`, `billing`, `settings`, and `notifications`.
> Leaf estimates are `small`, `medium`, and `large`; planning evidence sizes the
> settings path and delivery routing as `medium`. Readiness mappings are
> `needs-discovery`, `needs-planning`, and `ready`. The work
> requires several reviewable pull requests. Authenticated provider discovery
> confirms that `example/project` is active, every named metadata value exists,
> and native issue creation, sub-issues, and blocked-by relationships are
> available. Show the proposed parent, children, native blockers, and metadata
> before creating anything.

## Expected behavior

- [ ] Creates one unestimated parent for the whole account-notifications outcome.
- [ ] Proposes children as complete observable behaviors, not separate database,
      API, UI, and test layers.
- [ ] Gives every leaf Problem, Scope, Verification, priority, relevant labels,
      an analyzed estimate, and readiness.
- [ ] States what can be demonstrated when each leaf closes, with Verification
      criteria that would fail before its implementation.
- [ ] Shows a compact decomposition check for each leaf with its demonstrable
      outcome, why it remains separate, and every blocker with its reason.
- [ ] Adds only blockers that are necessary for a child to start or finish
      safely; preference or convenient sequencing does not become an edge.
- [ ] Shows the complete node-and-edge batch and waits for direct approval before
      any tracker mutation.
