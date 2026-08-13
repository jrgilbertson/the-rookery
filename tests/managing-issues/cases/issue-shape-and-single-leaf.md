# One reviewable deliverable stays one leaf

Provenance: the bare baseline omitted the required `Problem` and positive
`Scope` structure and invented constraints; accepted contract R1 and AE1 keeps
a simple one-PR task as one concise leaf.

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
