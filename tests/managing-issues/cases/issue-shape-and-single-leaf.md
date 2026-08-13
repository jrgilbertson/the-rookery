# One reviewable deliverable stays one leaf

Provenance: accepted managing-issues contract R1 and AE1 — a simple one-PR task
must not acquire artificial hierarchy or workflow ceremony. Behavioral grade
not yet run.

## Prompt

> Draft an issue for `example/project`: the settings form accepts an invalid
> timezone and then fails on save. The fix is one reviewable pull request. It
> should reject unsupported timezone values and preserve valid selections.
> Give me the issue draft and the issue relationships you would create. Do not
> implement the fix or open a pull request.

## Expected behavior

- [ ] The body contains `Problem`, `Scope`, and observable `Verification`
      criteria.
- [ ] Context or constraints are omitted unless they add material information.
- [ ] The issue remains one leaf with no artificial parent or sibling.
- [ ] The response creates no project, execution plan, worker assignment, or
      separate leaf per hypothetical implementation step.
- [ ] The response does not implement code or execute a pull-request workflow.
