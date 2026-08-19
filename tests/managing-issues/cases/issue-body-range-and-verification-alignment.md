# Issue bodies scale without hiding requirements in Verification

Provenance: the prior template treated every issue as broken or missing,
overlapped Scope with Verification, and did not guard against acceptance checks
that test behavior the issue never promised.

## Prompt

> Using Managing Issues, draft issue bodies only for these four synthetic tasks.
> Do not contact a provider or invent tracker metadata.
>
> 1. Replace one stale support URL in the README and confirm the new link works.
> 2. Decide whether to adopt a compiler optimization. The outcome is unresolved;
>    compare compatibility and measured performance, then record adopt or defer
>    with its rationale and reconsideration trigger.
> 3. Fix an intermittent Safari settings failure that occurs only after changing
>    locale, navigating away, returning, and saving. Chrome is unaffected. Safari
>    should save successfully. The browser version and exact sequence matter.
> 4. Make every project-search entry point honor the Include archived toggle. A
>    teammate suggested verifying only that the global palette's result count
>    increases and that its query uses a CTE, but neither requirement is part of
>    the requested product behavior.

## Expected behavior

- [ ] Every draft uses Problem, Scope, and Verification with distinct roles:
      current gap or uncertainty, one owned outcome and boundary, then proof.
- [ ] The README task stays terse and gains no optional section without a
      material need.
- [ ] The decision task describes unresolved evidence rather than pretending a
      defect exists, and Verification requires a durable evidence-backed result.
- [ ] The Safari task gives the multi-step, environment-specific reproduction a
      separate optional section while keeping expected and actual behavior clear.
- [ ] Search Verification proves the behavior promised across every entry point;
      it does not accept result-count change or a CTE as sufficient or required
      proof of unstated behavior or implementation.
