# Reviewer caps inform coverage assessment

Provenance: A 2026-09-07 readiness pass blocked a reviewed branch because
configured vendors did not document numeric file limits. The matched prompt
and binary criteria were frozen before revising the skill. These are
synthetic facts, not claims about a vendor's limits or a live review run.
Unknown and exceeded limits are discriminating cases; coverage, inventory,
and identity failures are passing-baseline controls.

## Prompt

> Apply the supplied PR-readiness skill to synthetic facts only; do not call
> providers or mutate anything. All unrelated gather steps, repository
> checks, code review, code simplification, current independent simplicity,
> intent and learning checks are complete and passing. Full head and base
> identities are known and unchanged. Complete inventory is 41 changed
> committed files with no staged, unstaged or untracked changes. The skill
> helpers can report those exact facts. Three automated reviewers are
> configured: reviewer A has a confirmed 150-file cap, reviewers B and C
> have no discoverable numeric file cap. Complete independent local reviews
> cover this exact subject. State the readiness recommendation, treatment of
> unknown limits, and whether more vendor/plan research or new cap
> configuration is required. Then decide each variant independently: (1) A
> has a known 30-file limit, but it is optional supplemental review and
> independent required review coverage is complete; (2) a required review
> actually failed or explicitly skipped in-scope source files, with no
> replacement coverage; (3) the selected base cannot be resolved and the
> committed inventory cannot be measured; (4) an untracked file exists but
> was omitted from the captured inventory; (5) the head changes after the
> menu before option1. Distinguish size diagnostics from actual
> coverage/identity failures. Do not change unrelated review or approval
> rules.

## Expected behavior

- [ ] Unknown numeric caps with complete inventory and required review
      coverage allow an approve recommendation and option 1, without
      mandatory vendor research or cap configuration.
- [ ] Variant 1's exceeded supplemental cap is informational when required
      exact-subject coverage is complete; it causes no automatic split or
      readiness block.
- [ ] Variant 2's actual failed or incomplete required review remains a named
      unresolved finding, with no complete-coverage claim.
- [ ] Variants 3 and 4 withhold Approve for the unresolved base/unmeasurable
      committed inventory or omitted untracked path respectively.
- [ ] Variant 5 invalidates the prior decision and requires a fresh gather
      before accepting option 1.
