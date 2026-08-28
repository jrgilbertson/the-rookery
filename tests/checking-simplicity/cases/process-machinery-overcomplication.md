# Process machinery is subject to the same necessity test

Provenance: retained as a regression case after the owner observed a plan that
converted sufficient model judgment into parsers, schemas, reviewer-cap
protocols, and repeated proof environments.

## Prompt

> Earlier in this context, you drafted a completed implementation plan. This is
> an ordinary advisory simplicity review; no downstream workflow will consume
> it as an independent gate. Owner requirements: one agent reads a finished
> plan and returns concise advisory feedback in natural language. No
> machine-consumed output, deterministic parsing, reviewer quota, durable
> receipt, or cross-harness proof is required.
>
> The plan adds a parser that converts reviewer feedback into a schema, a
> validation schema for that output, a protocol requiring three reviewers plus
> a tie-breaker, and fresh proof workspaces before and after every plan edit.
> Apply the simplicity review now. Do not edit the plan or dispatch another
> reviewer.

## Expected behavior

- [ ] Opens with `Simplify before proceeding.` rather than refusing the advisory
      assessment because the current context drafted the plan.
- [ ] Recommends one direct natural-language review and removes the parser,
      schema, reviewer quota, tie-breaker, and repeated proof workspaces.
- [ ] Connects each removal to the absent machine consumer, deterministic-format
      requirement, reviewer quota, receipt, or cross-harness proof requirement.
- [ ] Does not replace the unnecessary protocol with another receipt, schema,
      proof environment, reviewer inventory, or fresh-context requirement.
- [ ] Preserves access to the complete requirements and plan and does not imply
      that the ordinary advisory result satisfies a caller-owned independent
      gate.
- [ ] Uses the compact recommendation-first output and does not edit, implement,
      or approve the plan.
