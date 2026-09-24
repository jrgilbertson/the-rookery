---
title: Key contract exceptions on facts the model already decided
date: 2026-09-23
category: best-practices
module: skills/route-work
problem_type: best_practice
component: development_workflow
severity: medium
applies_when:
  - "An instruction contract followed by a model carves an exception out of a default"
  - "The exception depends on what the request needs, where the work goes next, or another judgment the model makes fresh each run"
  - "Behavioral runs of the same prompt disagree on whether the exception applies"
tags: [route-work, routing-contract, instruction-prose, exceptions, behavioral-evals]
---

# Key contract exceptions on facts the model already decided

## Context

Issue #162 changed `route-work` so that a route that says nothing about
implementation predicts implementation and sizes the roster for it. Some runs
had to keep their own end, so the first exception in `ROUTING.md` read:

> unless supplied evidence ends the run earlier: ... or the request only needs
> issue-tracker changes through `managing-issues` or a pressure test of a
> supplied document through `grill-with-docs`.

Fresh runners read the same case two ways. In one run, a `managing-issues`
route for incomplete descendant coverage (`issue-family-existing-owner` item
1) carried no prediction. In a later run, the runner reasoned that
implementation would follow the tracker work, so the request needed more than
tracker changes. It predicted implementation and added "Don't merge without
human approval." to a tracker-only card. Nothing in the contract had changed
for that item between the two runs (`tests/route-work/log.md`, 2026-09-23
entries).

## Guidance

When an exception can be keyed either on a judgment about the request or on a
fact the model has already fixed, key it on the fact. Here the starting owner
had already been chosen from the owner table before the roster rule ran, so
the exception now reads (`ROUTING.md`, "Estimate the pattern and roster"):

> Skip the prediction when the operator limits the run to planning or
> withholds implementation, or when the run starts with `managing-issues` or
> `grill-with-docs`.

Keep the keyed rule free of claims about where those runs end. A first
version added "which end at the tracker or the document", and a review showed
a runner could read that clause as overriding an operator who said "grill the
doc, then implement". The prediction only applies when nothing is said, so a
stated follow-on still sizes for implementation without the clause.

In the rerun, every `managing-issues` and grill route carried no prediction
and no merge line, and every route that said nothing about implementation
still predicted it.

## Why This Matters

A judgment such as "only needs", "is mainly", or "will likely lead to" is
evaluated anew on every run, and a model reasoning one step further ("the
tracker work will lead to building") reaches the opposite branch. A fact the
model already committed to, such as a table lookup or the starting workflow,
does not move between runs, so the exception fires the same way each time.
The wider scope is usually cheap: here, work that does follow the tracker gets
its own route once the tracker is settled.

## When to Apply

- Before adding an "unless the request ..." clause, look for an earlier
  decision in the same contract that already separates the cases.
- When a behavioral case flips between runs on an exception, check whether
  the exception reads a judgment instead of a decided fact.

## Examples

A related failure from the same branch: in the "Preserve authority"
paragraph, "When the operator withheld merge, that line is the limit's one
sentence. Otherwise say nothing about authority." let "Otherwise" attach to
the nearest condition, which could cancel the limit and no-merge rules before
it. The fix, "Add nothing else about authority.", names what is excluded
instead of branching on the last condition.

## Related

- [Defer to the gates a routed workflow already owns](../architecture-patterns/defer-to-the-gates-a-routed-workflow-already-owns.md)
- [Operationalize abstract qualifiers in instruction review](operationalize-abstract-qualifiers-in-instruction-review.md)
- Issue #162
