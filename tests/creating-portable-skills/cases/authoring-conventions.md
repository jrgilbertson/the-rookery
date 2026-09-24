# Judge authoring conventions by their effect

Provenance: the checklist required a literal description opening, one-level
reference depth, and fixed navigation/context thresholds regardless of outcome.

## Prompt

> Judge only the stated properties of these synthetic skill designs. All
> unmentioned format fields and resources are valid. For each, name any
> correction that is actually required and explain why. Do not rewrite files.
>
> 1. A description reads: "Create and edit CSV exports when a user needs
>    stable column ordering and an explicit missing-value representation."
>    Near-miss queries belong to charting, and its trigger checks pass.
> 2. A format-specific branch links to a reference that links to a maintained
>    schema. Both links name when the next file is needed. The schema is a
>    320-line alphabetically sorted field reference with searchable headings
>    and no table of contents. All resources ship inside the package.
> 3. A description says only "Helps with data." A required schema exists in
>    the bundle but no instruction points to it.
> 4. A skill exceeds a declared host context limit and omits the exact output
>    schema the caller requires.
> 5. Another skill exceeds the approximate 5,000-token authoring estimate.
>    Each instruction protects a distinct demonstrated requirement; no host
>    limit is exceeded and its body is below 500 lines.

## Expected behavior

- [ ] Accepts design 1 without requiring a literal "Use when" opening.
- [ ] Accepts design 2 without requiring flattened references or a table of
      contents solely because of its nesting or line count.
- [ ] Requires a discriminating description and a discoverable schema for
      design 3, explaining their effect on activation and execution.
- [ ] Requires design 4 to satisfy the real host limit and exact output contract.
- [ ] Treats design 5's token estimate as guidance and accepts the justified
      exception without discarding required behavior.
