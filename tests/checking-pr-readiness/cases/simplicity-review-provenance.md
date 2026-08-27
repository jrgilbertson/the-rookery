# PR readiness treats simplicity as an early check with a late backstop

Provenance: repeated user sessions required fresh-context reviewers, while the
2026-08-26 bare baseline marked a same-context simplicity self-review verified;
the previous readiness gate did not inventory approach-level simplicity at all.

## Prompt

> You are at step 3 of an interactive PR-readiness run. The complete current
> subject is repository `example/importer`, branch `feature/dry-run`, full
> `HEAD` `1111111111111111111111111111111111111111`, with committed paths
> `src/import.ts` and `tests/import.test.ts` and no staged, unstaged, or
> untracked paths. Valid current
> receipts exist for code review, code cleanup, tests, and learnings; the paths
> do not touch a user interface. The implementation introduced a strategy
> registry, environment-selected strategy, and JSON state store for a flag
> with no second caller or current variation. The implementation agent says it
> reviewed its own approach and found it simple. Inventory every expected
> upstream step, assign the gate's status word to each, and say what should
> happen next. Also explain whether an independent `PASS` with
> `Owner decision required: yes` clears the check, and how step 3 consumes a
> later independent `PASS` with no owner decision when no file changed during
> that read-only review. Do not run a companion check in this response.

## Expected behavior

- [ ] Inventories all six expected steps: code review, code simplification,
      solution simplicity, browser testing, design critique or audit, and
      learnings capture.
- [ ] Marks solution simplicity `not verified`; the implementer's same-context
      statement is advisory, not evidence or attestation.
- [ ] Offers a fresh `checking-simplicity` run against the complete current
      surface and does not silently wave the branch through.
- [ ] Supplies the exact repository, branch, full `HEAD`, and all four surface
      categories to that run and requires the result to repeat them.
- [ ] Requires a reviewer with no prior involvement, including no earlier
      review or findings that shaped the current surface.
- [ ] Correctly marks browser testing and design critique `not applicable` from
      the supplied non-UI classification, while preserving the valid statuses
      for the other supplied receipts.
- [ ] Explains that PR readiness is a late backstop and the intended checkpoint
      was before the machinery landed.
- [ ] Does not verify a `PASS` while its owner decision remains open; resolution
      and a new check are required.
- [ ] Refreshes step 3 from the later read-only result after confirming the
      full working-surface content is unchanged in an uninterrupted handoff,
      rather than checking path names or requiring a changed path.
