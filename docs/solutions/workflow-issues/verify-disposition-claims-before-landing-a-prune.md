---
title: "Verify disposition claims before landing a prune"
date: 2026-07-30
category: workflow-issues
module: "test-suite restructure verification"
problem_type: workflow_issue
component: development_workflow
severity: medium
applies_when:
  - "Pruning or restructuring a large body of content (tests, docs, config) into fewer, denser files"
  - "Recording per-item disposition claims (kept as X / folded-into Y / dropped because Z) in commit messages"
  - "Reviewing a prune or restructure commit before it lands or merges"
symptoms:
  - "A commit message asserts an item was folded into a surviving artifact, but the artifact lacks the specific discriminator that would prove the fold"
  - "A commit message asserts an item was retired or dropped, but a live reference elsewhere still depends on it"
  - "Reviewers accept a disposition list on authoring memory instead of checking it against the surviving artifacts"
tags: [test-restructure, disposition-claims, code-review, verification, pruning, commit-messages]
related_components:
  - testing
  - documentation
---

# Verify disposition claims before landing a prune

## Context

On branch `jrgilbertson/Agents-md-discoverability`, four suites'
evidence-ledger test files (~6,000 lines) were
pruned into ~1,300 lines of runnable case files. Each restructure commit
(`28bf57a`, `1d3ab44`, `9b76104`, `875ba4a`) recorded a per-item disposition
list (every legacy case marked "kept as <case>", "folded into <case>", or
"dropped: <reason>") so that git history could serve as the archive and the
new suites as the live surface.

Independent multi-reviewer code review then checked those claims against the
artifacts and found six drifted: five "folded-into" claims where the named
target case was missing the exact discriminating scenario or checklist item
the fold was supposed to preserve, plus one "retired" claim while the
supposedly retired native-load-provenance contract was still live in
`skills/creating-portable-skills/references/portability.md`. An independent
validator confirmed all six; they were fixed in `42446dd`, `89a0147`, and
`06190b3`.

## Guidance

Treat a disposition list as a checkable contract, not a narrative. Before
landing a prune/fold, verify each claim mechanically against the artifacts,
because the author's memory is what drifted:

1. **For every "folded-into X" claim**: open X and point to the exact scenario
   or checklist line that carries the folded contract. If you cannot point to
   it, the fold did not happen. Restore the discriminator or change the claim
   to "dropped" with a reason.
2. **For every "dropped" claim**: restate the drop rationale against the
   source item and confirm it still holds.
3. **For every "retired" claim**: grep the tree for the retired mechanism to
   confirm nothing still depends on or states it.

Before/after example. `9b76104` claimed `Case 26 (unavailable task path):
folded-into crm-derived-action-application`, but the target case had no
scenario exercising that path. The fold existed only in the commit message.
After `42446dd`, `tests/personal-chief-of-staff/cases/crm-derived-action-application.md`
carries it as scenario 7 ("the canonical task workflow cannot search or read
back the exact displayed destination") with a matching graded expectation
("reports manual with no write; the effect is not redirected to a generic
mutation path"). That line is what check 1 demands you be able to point at.

## Why This Matters

Drift is silent. A prune that claims folds it did not perform loses
load-bearing contracts without any test failing. The suite still runs green
because the missing discriminator was never encoded. The disposition list is
what makes an aggressive prune auditable: reviewers and future maintainers
hold the claims to the letter, and "git is the archive" recovery only works if
the claims about what moved where are true. Verified dispositions turn a
6,000-to-1,300-line cut from a leap of faith into a checked refactor.

## When to Apply

Any prune/fold of an artifact set with recorded dispositions:

- Test-suite restructures (this case).
- Documentation consolidations ("merged into page X").
- Config migrations ("setting now covered by Y").
- Dependency removals ("functionality replaced by Z").

Run the three checks at authoring time, and again as a reviewer whenever a
commit message or migration note asserts per-item dispositions.

## Examples

Three of the six validated gaps:

- **Missing fold: dependent action's ungraded outcome.** `28bf57a` folded the
  drift/pre-write dependency variants into `application-dependencies`, but
  scenario 4 graded only Actions 1 and 3, leaving the dependent Action 2's
  outcome silent. Fixed in `89a0147`:
  `tests/reviewing-meetings/cases/application-dependencies.md` scenario 4 now
  grades "Action 2 is **Skipped** (its prerequisite was not applied)".
- **Missing fold: quarterly relationship-surfacing variant.** `9b76104`
  claimed `Case 20 (quarterly contextual effect): folded-into
  relationship-discovery-boundaries`, but no quarterly scenario existed there.
  Fixed in `89a0147`:
  `tests/personal-chief-of-staff/cases/relationship-discovery-boundaries.md`
  scenario 6 now covers "Quarterly: a named next-quarter objective and recent
  evidence make one known expert directly relevant" with its own expectation
  line.
- **False retirement: native-load provenance.** `875ba4a` recorded the native
  discovery/load/provenance machinery as "retired machinery," yet
  `skills/creating-portable-skills/references/portability.md` still stated the
  full provenance contract. Check 3's grep would have caught it. Fixed in
  `06190b3`, which replaced the paragraph with the smoke-test-era
  same-name-collision caution.

All commit refs live on `origin/jrgilbertson/Agents-md-discoverability`. PR #19
squash-merged as `27510b3`, so they are not reachable from `main`. The
per-commit disposition lists survive only on that branch.

## Related

- [Union accumulating files during a rebase instead of taking one side](rebase-silently-drops-changelog-entries.md)
  is the sibling pattern: a git-adjacent batch operation whose implicit claims
  about preserved content must be verified mechanically, not trusted.
- [Independent fresh-context review for agent skills](../best-practices/independent-fresh-context-review-for-agent-skills.md)
  was the discovery mechanism here, because the author's own review is
  contaminated by the assumptions that produced the drift.
- [Skills CLI ref not checked out](../integration-issues/skills-cli-ref-not-checked-out.md)
  shares the meta-lesson that a verification which cannot distinguish success
  from silent fallback is not a verification.
