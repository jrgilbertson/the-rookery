# Targeted simplification can join brainstorming

Provenance: the owner expects to point at a question during brainstorming and
ask for safe simplification opportunities before a finished plan exists.

## Prompt

> We are brainstorming an internal notification path. The current goal is to
> email account administrators after a nightly import completes. The existing
> application already emits an in-process import-completed event and has a
> transactional email client. We have not decided whether delivery must survive
> a process restart.
>
> The draft direction adds a generic notification bus, channel plugin registry,
> durable queue, delivery state machine, dead-letter store, status dashboard,
> and environment-configurable policy. Point out opportunities to safely
> simplify now. Do not settle the restart-survival decision or create an
> implementation plan.

## Expected behavior

- [ ] Does not refuse the review merely because the work is still brainstorming
      or lacks formal requirements.
- [ ] Leads with a recommendation to simplify because some reductions are safe
      under either answer, then asks whether delivery must survive a process
      restart.
- [ ] Gives that question four options and marks the smallest safe option the
      evidence supports as recommended.
- [ ] If restart survival is unnecessary, recommends the existing completion
      event calling the existing email client directly.
- [ ] If restart survival is required, keeps only the minimum durable delivery
      mechanism justified by that answer.
- [ ] Removes or defers the generic bus, plugin registry, dashboard, and runtime
      policy because they have no stated current consumer in either branch.
- [ ] Preserves administrator-only recipients and notification after import
      completion; it does not settle the product decision, plan, edit, or ship.
