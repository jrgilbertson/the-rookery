# One reviewable deliverable stays one analyzed leaf

Provenance: the bare-model baseline omitted the required issue shape and
invented constraints.

## Prompt

> Draft an issue for `example/project`: the settings form accepts an invalid
> timezone and then fails on save. The fix is one reviewable pull request. It
> should reject unsupported timezone values and preserve valid selections.
> Available provider choices are priorities `high` and `normal`, labels `bug`
> and `settings`, estimates `small` and `medium`, and readiness labels for all
> three portable readiness postures. Give me the issue draft, explain the
> metadata choice, and name any issue relationships you would create. Do not
> implement the fix or open a pull request.

## Expected behavior

- [ ] The body contains `Problem`, `Scope`, and observable `Verification`
      criteria in the product team's language.
- [ ] Context or constraints are omitted unless they add material information.
- [ ] The issue remains one implementation leaf with no artificial parent or
      sibling, and receives an analyzed leaf estimate rather than a default.
- [ ] It analyzes priority, relevant labels, and one portable readiness posture
      from the supplied facts and available provider choices. If two choices are
      indistinguishable, it asks rather than guesses.
- [ ] Readiness describes the issue information, not a literal skill, agent, or
      workflow recommendation.
- [ ] The response creates no project, execution plan, worktree, worker
      assignment, or separate leaf per hypothetical implementation step.
- [ ] The response stops at issue facts; it does not implement code or execute a
      pull-request workflow.
