---
title: Defer to the gates a routed workflow already owns
date: 2026-09-23
category: architecture-patterns
module: skills/route-work
problem_type: architecture_pattern
component: development_workflow
severity: high
applies_when:
  - "A router, kickoff card, or wrapper skill hands work to ce-plan, ce-work, or impeccable"
  - "A contract rule describes worker counts, concurrency, review, commits, PRs, isolation, or authority"
  - "A contract sentence explains what a downstream workflow does"
tags:
  - route-work
  - routing-contract
  - compound-engineering
  - ce-work
  - authority
  - simplicity
---

# Defer to the gates a routed workflow already owns

## Context

`route-work` renders one card that starts work in a development framework:
Compound Engineering's `ce-brainstorm`, `ce-plan`, `ce-work`, or `ce-debug`,
`grill-with-docs`, `managing-issues`, or `impeccable`. The contract lives in
root `ROUTING.md`. It had picked up rules that restated what those workflows
already decide: how many workers to start and how, a concurrency cap, when to
add a reviewer, which grants to spell out, where workers run, and why a grant
was safe to omit. Each one either conflicted with the workflow it sat in front
of or leaked into the cards runners produced.

## Guidance

A router or kickoff contract that sits in front of a workflow should name only
what the workflow cannot know: the starting owner, the profile (model and
effort) for each seat, and the limits the operator stated. For everything the
workflow already gates, the contract defers. It does not restate the gate,
summarize it, or justify itself by describing it.

Before writing a rule that says how a downstream workflow behaves, read the
lines that define that behavior. Then pick one of three outcomes:

1. **The workflow owns it.** Delete the rule, or reduce it to one pinned
   sentence that hands the decision to the workflow.
2. **The workflow does not own it, and the operator supplied it.** Keep it,
   stated once, as the operator's own limit.
3. **The rule's rationale is a claim about the workflow.** Verify the claim
   against source. If it is false, remove the clause and put the real
   behavior in front of the operator for a decision.

The workflow gates that the route-work contract had restated, with the
Compound Engineering skill file that defines each:

- **`ce-plan` never implements.** "Research, decide, and write the plan —
  never implement. Do not write production code, run tests..."
  (`ce-plan/SKILL.md`). Implementation starts only through its handoff to
  `ce-work` (`ce-plan/SKILL.md`).
- **`ce-work` derives and schedules units.** Parallel dispatch of independent
  dependency layers is its default, driven by the plan's `Dependencies` and
  `Files` (`ce-work/references/execution-strategy.md`), gated by its Parallel
  Safety Check, which also caps concurrency at a bounded batch.
- **`ce-work` picks isolation.** "Isolation for native workers is the
  harness's job" (`execution-strategy.md`), with a shared-workspace wave
  contract for the fallback.
- **`ce-work` owns canonical commits.** Shared-workspace workers never commit,
  and worktree-isolated workers commit only on their own branch, which the
  orchestrator merges; "the orchestrator owns staging, committing, and the
  authoritative test runs" (`execution-strategy.md`; `ce-work/SKILL.md`).
- **`ce-work` runs its own review.** It reviews the diff with `ce-code-review`
  as the single path and cannot finish shipping without a completed review
  receipt or an explicit skip phrase
  (`ce-work/references/shipping-workflow.md`), then applies justified fixes
  itself.
- **`ce-work` opens the PR.** The shipping phase loads `ce-commit-push-pr` to
  commit, push, and open the PR without asking (`shipping-workflow.md`),
  unless the project names its own shipping process. The one exception is a
  branch carrying unpublished commits no open PR covers, where it only commits
  locally.

What stays in the contract is what no workflow supplies: which model and
effort each seat runs on, the subscription-billing constraint, the operator's
stated limits (including a condition or scope attached to a grant), and the
closing "Don't merge without human approval." line for any run that may reach
implementation, since the shipping workflow ends at an open PR and merge is
the step the operator holds for a human.

## Why This Matters

A restated gate is a second source of truth, and it disagrees with the first
as soon as either changes. It fails in three concrete ways:

- **It conflicts with the workflow it wraps.** "Start three Executors" on a
  `ce-plan` start tells the session to dispatch implementers inside a workflow
  that forbids implementation. On a `ce-work` start it overrides the unit
  derivation, safety check, isolation choice, and commit ownership `ce-work`
  already performs.
- **It leaks into cards.** Runners copy what the contract says, including
  Setup values such as an Executor count, into the part of the card the
  receiving session executes. A sentence that must reach the card exactly has
  to be pinned in the template, with the values that belong elsewhere named.
- **A false rationale hides a real decision.** A draft rule justified dropping
  grants with "the workflows ask before each step," but `ce-work` opens the PR
  without asking. Checking the claim against source put that behavior in front
  of the operator for a decision.

## When to Apply

- Writing or reviewing a router, kickoff template, wrapper skill, or
  orchestrator prompt that hands work to another workflow.
- A contract line mentions worker counts, concurrency, scheduling, isolation,
  worktrees, commits, review, PRs, or authority, and the receiving workflow
  has its own rule for that topic.
- A contract sentence explains why a rule is safe by describing another
  workflow.

It does not apply when the receiving workflow has no gate for the topic. For
example, route-work still adds a Reviewer to a run that does not implement
through `ce-work`, because nothing else reviews a plan or grill output against
the operator's criteria.

## Examples

A Coordinator + Executors kickoff once told the coordinator to start a fixed
number of Executors, give each a write path, and start them as subagents or
separate sessions. It now carries one pinned sentence and leaves the rest to
the workflow:

> When the work reaches implementation, run implementation workers on
> [Executor model] at [effort]; [the implementing workflow] decides how many
> and how to schedule them.

Two checks catch a restated gate before it ships:

1. **Fresh falsification pass.** Give a fresh-context agent the contract and
   the workflow sources and ask it to break one invariant with a concrete
   sequence.
2. **Probe prompt through a fresh runner.** Write a prompt that hits exactly
   the rule's edge, run it through a fresh subagent that loads only the
   package, and have a separate grader read the card against a prediction
   written in advance. The route-work eval log records these runs.

## Related

- [Reuse the shipping pipeline instead of a managed-run protocol](reuse-the-shipping-pipeline-instead-of-a-managed-run-protocol.md):
  the same principle for Repo Gardener, whose Executor contract restated
  publication gates the installed skills already own.
- [Gate on host-readable facts, not config grants](../design-patterns/gate-on-host-readable-facts-not-config-grants.md):
  a restated fact becomes a second authority that can only be wrong; keep only
  what the owner cannot know.
