---
title: Finish a knowable list census once per population
date: 2026-08-24
category: workflow-issues
module: "skills/repo-gardener"
problem_type: workflow_issue
component: development_workflow
severity: high
applies_when:
  - "An agent skill lists issues, pull requests, or alerts and may stop at a page bound"
  - "Several lanes would otherwise page the same provider list"
  - "A size threshold is being written as a stand-in for finishing cheap listing"
tags:
  - census
  - repo-gardener
  - sensing-floors
  - continue-until
  - identifier-listing
---

# Finish a knowable list census once per population

## Context

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

## Guidance

Keep listing a list-style population of issues, pull requests, or alerts
while the count is under the named backstop and either another page exists
or the listed count is below a provider-reported total. Stopping then is an
omission, not a stated bound. A named bound is allowed only at the backstop
with remainder, or when the provider cannot continue. Incomplete list-style
censuses keep the affected lanes partial and do not by themselves change
`run_outcome`.

Produce one identifier census per those populations per run. The parent
lists after `run-opened`. Lanes consume that list and do not re-page it. A
missing census is a sequencing gap, not a license to list.
Source-unavailable and empty-complete are census results. An empty-complete
census establishes absence for a zero-candidate verdict; the five-body
sample is complete at zero.

Do not treat a size threshold as the meaning of the rule. The backstop is
only a stop when remainder remains. The continue-until loop must require a
reason to fetch another page (another page exists, or listed count is below
the provider total). A loop that continues merely because a total is known
never exits after a finished 446-item census.

Body reads stay a separate floor. Cheap listing is identities plus cheap
list fields the endpoint already returns.

## Why This Matters

An honest partial on a knowable cheap list looks like integrity and still
leaves the owner without the census. A size cap papers over the same stop.
Per-lane listing multiplies provider cost without giving each lane a
verdict. A continue-until sentence that keys only on "total is known" hangs
after completion.

## When to Apply

- Rewriting sensing floors or other list-style census rules in an agent skill
- Seeing a run stop one page short of a provider total or `hasNextPage`
- Adding a numeric cap to force "small" lists to finish
- Splitting one provider population across parallel scouts

## Examples

Before: "first page of >=100; total unknown" counted as a stated bound, so
446 open issues stopped at 400 and both issue lanes reported partial.

After: keep listing while another page exists or listed count is below the
provider total, under the backstop; issue, health, and triage consume that
identifier list and read five bodies; an omission keeps those lanes partial
without failing the run.

A loop written as "keep listing while a total is known and count < 10,000"
does not stop at 446/446. Require another page or listed count below the
provider total.

## Related

- Pull request 69 on `jrgilbertson/the-rookery` (unmerged at time of writing)
- `skills/repo-gardener/references/lane-contracts.md` sensing floors
- `docs/solutions/workflow-issues/make-agent-skill-safe-stops-local-and-observable.md`
- `docs/solutions/best-practices/cross-harness-dogfood-testing.md`
