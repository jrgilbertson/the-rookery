---
title: Share query-scoped inventories with truthful coverage
date: 2026-08-24
last_updated: 2026-09-07
category: workflow-issues
module: "skills/repo-gardener"
problem_type: workflow_issue
component: development_workflow
severity: high
applies_when:
  - "Several maintenance areas need overlapping provider results"
  - "A filtered or paginated read may be mistaken for backlog exhaustion"
tags:
  - census
  - repo-gardener
  - filtered-discovery
  - identifier-listing
---

# Share query-scoped inventories with truthful coverage

## Historical context

A Corvly dogfood run stopped its open-issue census at four pages of 100 with
446 open issues still knowable. Floor 2 treated that named page bound as
honesty. Both issue lanes reported partial. The report was true. The last
cheap page never ran.

A first repair tried a size cap: list-style censuses of at most 1,000 items
must finish. The field failure was not the number. It was stopping while
another page or a provider total still made the remainder knowable. The same
sentence still allowed an unknown-size stop when only `hasNextPage` was
known. Raising the cap without owning the list once would also let three
issue-facing lanes each page Linear or GitHub to completion.

That repair required whole-population completion and fixed body-read floors.
The current workflow replaces those obligations with bounded, filtered
discovery. The reusable lesson is to share source reads and describe their
coverage accurately, not to enumerate every backlog before useful work.

## Reusable guidance

Repo Gardener no longer runs censuses or Gardening Tracker record reads;
its Sense section reads each source with what the host can reach and
names gaps.
The lesson below applies to any skill that shares paginated provider
reads.
A Census describes one stated query and window. Record its filters, returned
counts, pagination or search limits, and inspected coverage. Reuse results
and body reads across areas when queries overlap.

Start implementation discovery with supported open/ready filters and a
preference for mapped estimates 1–2. Narrow metadata locally when the native
interface lacks an estimate filter; if estimates are absent from metadata,
inspect the supported-filter shortlist. Missing estimates or readiness mappings
remain eligible for selective broadening. Triage uses its own relevant query.

Complete the quick available-input pass across all five areas before dispatch,
then deepen where another read could change an assignment or recommendation.
Fetch further pages when they serve that decision, and state any remaining
coverage limit. A completed filtered query proves only its own population and
window. An empty result does not establish that the repository has no work.
Source unavailability limits dependent coverage while independent work proceeds.

Keep returned records, inspected bodies, qualified candidates, and authored
work distinct. There is no fixed body-read count or full-backlog prerequisite.

## Example

A provider reports 446 open issues. An open/ready query returns 12 records,
of which six have mapped estimates 1–2. Inspect that shortlist first. A separate
triage query may reveal older feedback; reuse any overlapping records. Broaden
when an unestimated request or another page could change the recommendation.
Report the actual filters and reads, leaving the rest unassessed.

When a query is complete at 12/12, a known total is no reason to fetch again.
When another page exists but remains unread, report that limit rather than
claiming query completion or backlog exhaustion.

## Related

- Historical motivation: pull request 69 on `jrgilbertson/the-rookery`
- [Repo Gardener](../../../skills/repo-gardener/SKILL.md)
- [Make skill safe stops local and observable](make-skill-safe-stops-local-and-observable.md)
- [Cross-harness dogfood testing](../best-practices/cross-harness-dogfood-testing.md)
