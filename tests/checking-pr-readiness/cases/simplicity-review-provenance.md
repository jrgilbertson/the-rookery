# PR readiness treats simplicity as an early check with a late backstop

Provenance: repeated sessions required fresh reviewers; the 2026-08-26 bare
baseline verified self-review and omitted approach-level simplicity.

## Prompt

> At interactive PR-readiness step 3, the subject is repository
> `example/importer`, branch `feature/dry-run`, full `HEAD`
> `1111111111111111111111111111111111111111`, with committed paths
> `src/import.ts` and `tests/import.test.ts`; all other surface categories are
> empty. Linked issue `example/importer#42` requires one `--dry-run` flag to use
> the existing synchronous path without writes, preserve authorization and
> validation, and pass focused flag and no-write tests. Valid receipts cover
> code review, cleanup, tests, and learnings; no path touches a user interface.
> The implementation added a strategy registry, environment selection, and a
> JSON state store with no second caller or current variation. Its implementer
> self-reviewed the approach. Inventory the upstream steps and statuses, give
> the next action, why its timing is a backstop, and the exact fresh-review
> dispatch, acceptance, and continuity requirements. Then explain how the gate
> handles a matching `unverified` result, an independent `PASS` with an open
> owner decision, an independent `CHANGES_NEEDED` result, and a later read-only
> independent clean `PASS` when no requirement or file changed. Do not run a
> companion check.

## Expected behavior

- [ ] Inventories code review, code simplification, solution simplicity,
      browser testing, design critique or audit, and learnings capture.
- [ ] Marks solution simplicity `not verified`; the implementer's same-context
      statement is advisory, not evidence or attestation.
- [ ] Offers a fresh `checking-simplicity` run as the late backstop and says the
      intended checkpoint was before the machinery landed.
- [ ] Supplies and requires the result to repeat issue `example/importer#42`,
      its objective, behavior, constraints, verification, repository, branch,
      full `HEAD`, and all four surface categories.
- [ ] Requires exactly `Review context: independent` from a reviewer with no
      prior review or findings that shaped the surface; `unverified` stays not
      verified.
- [ ] Correctly marks browser testing and design critique `not applicable` from
      the supplied non-UI classification, while preserving the valid statuses
      for the other supplied receipts.
- [ ] Does not verify a `PASS` while its owner decision remains open; resolution
      and a new check are required.
- [ ] Keeps an independent `CHANGES_NEEDED` result failed until the approach is
      revised and the resulting subject receives a new independent `PASS` with
      no owner decision.
- [ ] Refreshes step 3 from the later read-only result after confirming the
      complete requirements and full working-surface content are unchanged in
      an uninterrupted handoff, rather than checking path names or requiring a
      changed path.
