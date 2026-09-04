# An independent gate needs one reviewer, not reviewer churn

Provenance: applying the skill to its own process found that excluding anyone
who reviewed an earlier draft forced a new reviewer and proof handoff after
every revision without improving the simplicity decision.

## Prompt

> A caller explicitly requires an independent simplicity result before
> implementation. One reviewer who did not author or implement the plan returns
> a recommendation to simplify first. The author applies only that reviewer's proposed
> reductions. May the same reviewer assess the revised plan, and what evidence
> does this skill itself require? Return the answer only.

## Expected behavior

- [ ] Allows the same reviewer to assess the revision because it did not
      author or implement the revision.
- [ ] Requires the revised plan in full and the available decision frame, and
      no broader evidence by default.
- [ ] Does not require another reviewer, extra reviewers, a tracking file, a
      Git identity inventory, an uninterrupted handoff, or a separate
      workspace used only to prove the review.
- [ ] Leaves any stronger evidence trail or repeated-review rule to the caller
      that explicitly requires it.
- [ ] Does not install a lifecycle or Git hook.
