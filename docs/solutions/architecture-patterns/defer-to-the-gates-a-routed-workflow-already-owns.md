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
`grill-with-docs`, `managing-issues`, or `impeccable`. The contract lives in root `ROUTING.md`,
and `skills/route-work/references/routing.md` is its byte-identical copy.

Over time the contract picked up rules that restated what those workflows
already decide: how many workers to start and how, a concurrency cap and queue,
when to add a reviewer, which grants to spell out, where workers run, and why a
grant was safe to omit. On 2026-09-23, on the unmerged branch
`jrgilbertson/New-models` (no PR opened yet), each of these restated rules
either conflicted with the workflow it sat in front of or leaked into the cards
runners produced. The 2026-09-23 entries in `tests/route-work/log.md` record the
evals behind each change.

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

The workflow gates that the route-work contract had restated, with their
defining lines. These paths are inside the installed Compound Engineering
plugin's `skills/` directory (version 3.28.1), not this repository, so line
numbers drift with plugin releases:

- **`ce-plan` never implements.** "Research, decide, and write the plan —
  never implement. Do not write production code, run tests..."
  (`ce-plan/SKILL.md:15`). Implementation starts only through its handoff to
  `ce-work` (`ce-plan/SKILL.md:31`, `:60`).
- **`ce-work` derives and schedules units.** Parallel dispatch of independent
  dependency layers is its default, driven by the plan's `Dependencies` and
  `Files` (`ce-work/references/execution-strategy.md:5`), gated by its
  Parallel Safety Check (`:13-22`), which also caps concurrency at a bounded batch (`:20`).
- **`ce-work` picks isolation.** "Isolation for native workers is the
  harness's job" (`execution-strategy.md:24-27`), with a shared-workspace
  wave contract for the fallback (`:49-55`).
- **`ce-work` owns canonical commits.** Shared-workspace workers never
  commit, and worktree-isolated workers commit only on their own branch,
  which the orchestrator merges; "the orchestrator owns staging, committing,
  and the authoritative test runs" (`execution-strategy.md:43`, `:46`, `:53`,
  `:65`; `ce-work/SKILL.md:14`).
- **`ce-work` runs its own review.** It reviews the diff with
  `ce-code-review` as the single path and cannot finish shipping without a
  completed review receipt or an explicit skip phrase
  (`ce-work/references/shipping-workflow.md:29-31`), then applies justified
  fixes itself (`:39`).
- **`ce-work` opens the PR.** The shipping phase loads `ce-commit-push-pr` to
  commit, push, and open the PR without asking (`shipping-workflow.md:85`),
  unless the project names its own shipping process (`:83`). The one
  exception is a branch carrying unpublished commits no open PR covers,
  where it only commits locally (`:81`).

What stays in the contract is what no workflow supplies: which model and
effort each seat runs on, the subscription-billing constraint, the operator's
stated limits (including a condition or scope attached to a grant), and the
closing "Don't merge without human approval." line for any run that may reach
implementation, since the shipping workflow ends at an open PR and merge is
the step the operator holds for a human.

## Why This Matters

A restated gate is a second source of truth, and it disagrees with the first
as soon as either changes. It also fails in two concrete ways here.

**It conflicts with the workflow it wraps.** A kickoff that says "start three
Executors" is an instruction to the session running the starting workflow. On
a `ce-plan` start, that session is told to dispatch implementers inside a
workflow that forbids implementation. On a `ce-work` start, it overrides the
unit derivation, Parallel Safety Check, isolation choice, and commit ownership
that `ce-work` already performs.

**It leaks into cards.** Runners copy what the contract says. In one
eval run logged on 2026-09-23, runners copied Setup's Executor count,
the concurrency cap, or a write scope into three of the kickoffs even after the
contract stopped asking for them. Only pinning the sentence to fixed template
wording stopped the leak: the revised candidate matched all five Coordinator +
Executors kickoffs word for word.

**A false rationale hides a real decision.** A draft of the authority rule
justified dropping grants with "the workflows ask before each step." A
fresh-context falsification pass showed that `ce-work`'s shipping phase
commits, pushes, and opens the PR through `ce-commit-push-pr` without asking.
The clause would have let an operator believe a PR required a second
approval. Removing it put the real behavior in front of the operator, who
accepted `ce-work` opening PRs. The no-merge line stays because it is the only
stop the operator actually gets.

The deferral also made the contract shorter. The five-worker budget and
queue, the subagent-or-session instruction, the worktree placement, the grant
sentences, and the acceptance-criteria Reviewer all came out on the branch.
The eval checklists moved with them: the `roster-route` checklist line for
prompt item 3 now expects one Executor per named module with no cap, and the
line for prompt item 2 expects no Reviewer from acceptance criteria alone.

## When to Apply

- Writing or reviewing any router, kickoff template, wrapper skill, or
  orchestrator prompt that hands work to another workflow.
- A contract line mentions worker counts, concurrency, scheduling, isolation,
  worktrees, commits, review, PRs, or authority, and the receiving workflow
  has its own rule for that topic.
- A contract sentence explains *why* a rule is safe by describing another
  workflow ("the workflow asks first", "the workers do not commit").
- An eval shows runners copying a Setup value (a count, a cap, a scope) into
  the part of the card the receiving session executes.

It does not apply when the receiving workflow has no gate for the topic. The
route-work Reviewer rule still adds a Reviewer for a run that does not
implement through `ce-work`, because nothing else reviews a plan or grill
output against the operator's criteria.

## Examples

### Kickoff implementation sentence

Before, a Coordinator + Executors kickoff told the coordinator how to staff
and run the units. This is condensed from a probe card and the contract text
behind it:

> Start three Executors … give each its module as a separate write path …
> start each Executor as a subagent or a separate session.

The contract behind it budgeted "five concurrent workers total, including the
coordinator and Reviewer", queued units that did not fit, and told the
coordinator to start differing-effort workers "as a subagent or a separate
session."

After, the kickoff carries one pinned sentence, and the count stays in Setup
(`ROUTING.md:230`, `:235-236`):

> When the work reaches implementation, run implementation workers on
> [Executor model] at [effort]; [the implementing workflow] decides how many
> and how to schedule them.

The pattern row's guardrail now reads "The kickoff names the Executors' model
and effort; the workflow decides how many run and when" (`ROUTING.md:136`).
The five-worker cap and queue were deleted, because `ce-work` decides
concurrency. Isolated-worktree placement was deleted, because `ce-work` and
the harness choose isolation.

### Reviewer rule

Before, acceptance criteria alone added a Reviewer, even on a `ce-work` run:

| Pattern | Use when |
|---|---|
| Executor + Reviewer | Explicit acceptance criteria exist or the operator asks for review |

After (`ROUTING.md:135`):

| Pattern | Use when |
|---|---|
| Executor + Reviewer | The operator asks for a separate Reviewer, or explicit acceptance criteria exist for a run that does not implement through `ce-work`, which runs its own review |

Probes on the new rule: a `ce-work` fix with criteria only added no Reviewer;
"have GPT-6 Sol review Opus's work" added a Sol high Reviewer with the
one-round stop; a planning-only run with listed criteria added a Sol high
Reviewer on the plan and no no-merge line.

### Grants and limits

Before, cards carried grant sentences such as "Implementation is authorized"
or "Implementation through an open pull request is authorized." After, cards
leave supplied grants off, keep every operator-stated limit in one sentence
(a condition or scope attached to a grant counts as a limit), and end any
kickoff whose run may reach implementation with "Don't merge without human
approval." unless merge was granted (`ROUTING.md:58-65`).

### Testing a restated rule

Two checks catch a restated gate before it ships:

1. **Fresh falsification pass.** Give a fresh-context agent the contract and
   the workflow sources and ask it to break one invariant with a concrete
   sequence. This is how the "workflows ask before each step" rationale was
   shown false: the pass traced `ce-work`'s shipping phase straight into
   `ce-commit-push-pr`. Self-review had not caught it.
2. **Probe prompt through a fresh runner.** Write a prompt that hits exactly
   the rule's edge, such as criteria on a `ce-work` fix, a conditional grant,
   or "plan the refactor of modules A, B and C… implementation follows". Run
   it through a fresh subagent that loads only the candidate package, and
   have a separate grader read the card against a prediction written in
   advance. A probe that misses its prediction is a finding either way. In
   one logged run, the "implementation follows" probe routed three
   Executors on a conditional grant, which surfaced an operator-wording
   decision rather than a contract bug.

Log each run in `tests/route-work/log.md` as one execution, not a
reliability estimate.

## Related

- [Reuse the shipping pipeline instead of a managed-run protocol](reuse-the-shipping-pipeline-instead-of-a-managed-run-protocol.md):
  the same principle for Repo Gardener, whose Executor contract restated
  publication gates the installed skills already own.
- [Gate on host-readable facts, not config grants](../design-patterns/gate-on-host-readable-facts-not-config-grants.md):
  a restated fact becomes a second authority that can only be wrong; keep only
  what the owner cannot know.
