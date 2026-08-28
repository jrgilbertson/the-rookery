# One lifecycle contract governs every caller

Provenance: the activation reference duplicated the core skill's clean-exit,
staleness, and recheck semantics. This regression control protects those
outcomes after the reference was reduced to caller mechanics.

## Prompt

> Apply the configured simplicity checkpoint to three caller states.
> 1. The unchanged current plan already has a clean independent result that
>    begins `Proceed with the current approach.` and no owner question.
> 2. After that result, required behavior changes materially.
> 3. Only a copy edit changes the plan, but the earlier result is being consumed
>    as a gate.
> For each state, say whether the caller continues or starts another checkpoint.

## Expected behavior

- [ ] State 1 continues to the next planner or executor without another
      simplicity review.
- [ ] State 2 treats the result as stale and obtains a new independent review
      of the changed subject before crossing the boundary.
- [ ] State 3 recognizes that a copy edit does not inherently need a new
      simplicity assessment, but invalidates the earlier result when it is
      consumed as a gate, so the current subject needs a new independent review.
- [ ] Applies the core skill's validity, staleness, and completion contract
      rather than inventing a second activation-specific threshold.
- [ ] Does not install or rely on a lifecycle or Git hook.
