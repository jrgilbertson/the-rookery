# An independent gate needs one reviewer, not reviewer churn

Provenance: applying the skill to its own process found that excluding anyone
who reviewed an earlier draft forced a new reviewer and proof handoff after
every revision without improving the simplicity decision.

## Prompt

> A caller explicitly requires an independent simplicity result before
> implementation. One reviewer who did not author or implement the plan returns
> `Simplify before proceeding.` The author applies only that reviewer's proposed
> reductions. May the same reviewer assess the revised plan, and what evidence
> does this skill itself require? Return the answer only.

## Expected behavior

- [ ] Allows the same independent reviewer to assess the revision because
      reviewing an earlier draft is not authorship or implementation.
- [ ] Requires the current owner-authoritative requirements and complete revised
      plan, and no broader evidence by default.
- [ ] Does not require another reviewer, a reviewer quota, a receipt, a Git
      identity inventory, an uninterrupted handoff, or a proof workspace.
- [ ] Leaves any stronger continuity or evidence contract to the caller that
      explicitly requires it.
- [ ] Does not install a lifecycle or Git hook.
