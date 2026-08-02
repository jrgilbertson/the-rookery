---
title: "Loosening a test checklist during grading removes the check"
date: 2026-08-01
category: workflow-issues
module: "checking-merge-readiness behavioral battery"
problem_type: workflow_issue
component: testing_framework
severity: high
applies_when:
  - "Grading a hand-run behavioral battery whose checklists are prose, not code"
  - "A checklist item fails and the observed run's answer looks defensible"
  - "One wording change is applied to several scenarios at once"
  - "The same person authored the checklist and is now grading runs against it"
symptoms:
  - "A checklist item is edited mid-grading and the run that prompted the edit then passes"
  - "An item's new wording accepts a range of outcomes where the source criterion named one"
  - "A justification quoted from one acceptance example is applied to scenarios that example does not cover"
  - "A scenario passes both the skilled and the bare run and no longer separates them"
tags: [test-checklists, grading, falsifiability, acceptance-criteria, agent-skills, behavioral-testing, run-logs]
related_components:
  - testing
  - development_workflow
---

# Loosening a test checklist during grading removes the check

## Context

The `checking-merge-readiness` battery
(`tests/checking-merge-readiness/cases/merge-digest-battery.md`) was authored as
nine scenarios, each with a four-item binary checklist a blind grader marks pass
or fail. As first committed, the scenario 2 (defensive accretion), scenario 5
(unresolved thread), and scenario 7 (evidence pack conflict) checklists each
carried a recommendation item reading "The recommendation is pause, not merge."

Partway through grading, runs on those specimens returned do not merge instead.
That is not a wrong answer. The skill's grade-to-recommendation mapping is fixed
(`skills/checking-merge-readiness/SKILL.md:197-200`): every driver low gives
merge, any driver medium and none high gives pause, any driver high gives do not
merge. A specimen that grades high produces do not merge by construction, so a
literal "pause" item fails a correct run.

The three items were rewritten to "at most pause (pause or do not merge,
following the fixed grade-to-light mapping from the grades actually given),
never merge", and grading continued. The edit was recorded in the run log as its
own line, justified "per AE7's wording and R10's fixed mapping (a high-graded
driver maps to do not merge, and the literal 'pause' would have failed a
defensible stronger block)". That line was later dropped from
`tests/checking-merge-readiness/log.md` when the harness was rebuilt around the
`gh` stub; it survives in the file's history.

The justification holds for exactly one of the three scenarios it was applied
to. AE7, which scenario 5 encodes, says "the recommendation is at most pause"
(`docs/plans/2026-08-01-001-feat-checking-merge-readiness-plan.md:105`). AE2,
which scenario 2 encodes, says "the recommendation is pause with that concern
stated" with no hedge (same file, line 100). AE9, which scenario 7 encodes,
states no recommendation at all (line 108). One acceptance example's wording was
carried across two scenarios it does not govern.

The consequence is recorded as a known limitation in the current log
(`tests/checking-merge-readiness/log.md:46`). The defensive-accretion specimen
grades high, so scenario 2 exercises the do-not-merge branch and AE2's literal
pause branch goes unexercised.

Closing it took a new specimen, and the closing was harder than expected in a
way worth recording. Scenario 2b (`specimen-h`) had to be built to grade medium
on complexity accretion, and the first two attempts graded low instead. Both
times the skill gave the same reason: the accretion was self-explaining, with
inline comments naming each ordering constraint and a test pinning the
combination, so a reader did not need the review history to understand the
sequence. That is the low anchor, correctly applied. The specimen only reached
medium once the explanatory comments and the combination test were removed, so
the ordering constraints lived only in the closed review threads.

The lesson inside the lesson: for complexity accretion, the low-to-medium
boundary turns on whether the accumulated shape documents itself, not on how
much accumulated. That is not obvious from the anchor text, and it is the kind
of thing only a specimen that refuses to grade where you expected will teach
you. It also sets a standing temptation. Three attempts at a specimen is the
point where widening the checklist item starts to look reasonable, and widening
it would have been the same mistake this document is about.

A second edit that same day ran the other way. Scenario 5's driver item
originally accepted "graded at least medium" on a specimen the rubric's high
anchor covers exactly, so a run that under-graded the reproduced race would
still pass. Tightening it to require high and do not merge is what made the
scenario discriminate. The current run log line for the bare variant records
that it "reached the same do-not-merge conclusion with sound reasoning but
assigned no grade; under the earlier 'at least medium' wording this scenario did
not discriminate, and the tightened item is what separates them"
(`log.md:32`).

## Guidance

An item edited during grading, after seeing what a run produced, is the one edit
in a test suite that can silently delete a check. Handle it as its own decision:

1. **Name the direction before making the edit.** Loosening widens the set of
   outputs an item accepts. Tightening narrows it. State which one you are doing
   in the same sentence as the justification, so the log line carries the fact a
   reviewer needs.
2. **Send any loosening back to the source criterion, quoted.** Open the
   acceptance example, requirement, or rubric line the item encodes and paste
   its exact words next to the proposed wording. If the source hedges, the item
   may hedge. If it names one outcome, the item names one outcome and the run
   that produced something else is the thing to explain.
3. **Never apply one criterion's wording to another criterion's scenario.**
   Scenarios 2, 5, and 7 encode AE2, AE7, and AE9. A justification that quotes
   AE7 licenses a change to scenario 5 alone. Batch edits across scenarios need
   one justification per scenario, each against its own source.
4. **When a correct run fails an item, prefer a new specimen to a wider item.**
   A specimen that grades high cannot exercise a pause branch no matter how the
   item is worded. Widening the item hides that; adding a medium-capped specimen
   fixes it. Scenario 2b is the shape of the second option.
5. **Record the gap the moment you accept a loosening you cannot fully
   justify.** The `log.md:46` limitation line is what kept AE2's uncovered pause
   branch findable after grading moved on.
6. **Re-check what a loosened item still separates.** After widening, ask which
   wrong output the item would now fail. If the answer is none, or if both the
   skilled and bare run now pass a scenario built to discriminate, the item is
   decorative and the scenario is a regression guard at best.
7. **Log the edit in the run log rather than only in the diff.** A checklist
   diff shows the words changing; the log line shows when, against what run, and
   on whose reasoning, which is what a later reviewer reads.

## Why This Matters

A checklist item is the only thing standing between a behavioral suite and its
author's expectations. Loosen one so the run in front of you passes, and the
item stops being able to fail. Nothing goes red, the suite still reports a
scenario count, and the branch it was supposed to hold no longer has any test
pointed at it.

The failure is hard to catch because each edit is defensible in isolation. The
AE7 half of this recalibration was correct, the mapping argument behind it was
correct, and the same sentence carried an unjustified change to two other
scenarios along with it. A reviewer skimming the diff sees one reasonable-looking
wording change repeated three times.

What made it catchable was that the recalibration was written into the run log
as a line of its own, with its justification attached. That let a later reader
open AE2, compare its words to the new item, and find that half the edit had no
support. An unlogged recalibration leaves nothing to compare, and the suite
carries the hole with no record that a decision was ever made.

The tightening case shows the value on the other side. Scenario 5 had passed
under "at least medium" without separating the skilled run from the bare one.
Requiring the grade its rubric anchor actually calls for made the scenario fail
the bare run for the first time, which is the whole point of a discriminating
scenario.

## When to Apply

Apply this whenever checklists are graded by hand against runs, which covers
skill behavioral batteries, prompt evaluations, and matched-pair comparisons
where the criteria live in prose rather than in an assertion. It applies most
strongly when the author of the checklist is also the grader, since the
loosening is generated by the same expectations that will accept it.

It applies with less force before any run exists. Rewriting a draft checklist
against its source criteria is ordinary authoring; the risk starts once an
observed output is what motivates the wording.

It does not apply to fixing an item that tests the harness rather than the
skill. Scenario 1 item 4 was rescoped to evidence packs alone after failing a
run for honestly reporting it could not see CI status the stub never served
(`log.md:24`). That is a defect in the item's scope, and the rescope narrowed
what the item covers rather than widening what it accepts.

## Examples

**The loosening.** Scenario 2's recommendation item, as first committed, read:

```text
- [ ] The recommendation is pause, not merge.
```

It now reads:

```text
- [ ] The recommendation is at most pause (pause or do not merge,
      following the fixed grade-to-light mapping from the grades
      actually given), never merge.
```

AE2's text, which the item encodes, is "a defensive-complexity driver is graded
and named with the specific accretion, and the recommendation is pause with that
concern stated". The rewrite accepts do not merge, which AE2 does not name, so
the item stopped testing AE2's mapping branch. Scenario 7 took the same rewrite
on AE9's authority, and AE9 names no recommendation at all.

**The gap it left, and the specimen that closes it.** The current log records it
as a known limitation, not a fix (`log.md:46`). Scenario 2b answers it with a
specimen whose accretion genuinely caps at medium, and its first item refuses
both neighbors:

```text
- [ ] The recommendation is pause. Neither merge nor do not merge is
      correct here: no driver reaches high, and at least one reaches
      medium.
```

**The tightening.** Scenario 5's driver item, as first committed, read "The open
thread is a named unresolved-items driver graded at least medium." It now reads:

```text
- [ ] The open thread is a named unresolved-items driver graded high. The
      rubric's high anchor covers this specimen exactly (a reproduced
      misbehavior the record never rebuts), so a medium grade is a fail,
      not a defensible reading.
```

Same kind of edit, opposite direction, and the run log line for the superseded
battery states why it was needed: the item "accepted 'at least medium' on a
specimen the rubric's high anchor covers exactly, so an under-grade could pass;
tightened to require high and do not merge" (`log.md:62`).

## Related

- [Verify disposition claims before landing a prune](../workflow-issues/verify-disposition-claims-before-landing-a-prune.md)
  is the same failure family in prose form. There a fold claim passed because
  nothing forced it to be checked against the surviving artifact; here a
  checklist item passes because nothing forces its wording to be checked against
  the criterion it encodes.
- [Ship bundled skill helpers with an executable fail-closed contract](../workflow-issues/falsifiability-contracts-need-executable-tests.md)
  states the general rule this case instantiates. A check that cannot fail is
  not a check, whether the hole came from a self-matching grep or from an item
  widened to fit the run in front of you.
- [Independent fresh-context review for agent skills](../best-practices/independent-fresh-context-review-for-agent-skills.md)
  covers why the loosening survives. The context that authored the checklist is
  the context deciding whether a failing item was wrong, and it will reach for
  the reading that keeps grading moving.
