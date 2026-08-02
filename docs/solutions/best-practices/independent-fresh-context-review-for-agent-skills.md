---
title: "Independent fresh-context review for agent skills"
date: 2026-07-16
last_updated: 2026-08-01
category: best-practices
module: "creating-portable-skills skill verification"
problem_type: best_practice
component: testing_framework
severity: high
applies_when:
  - "Grading a matched comparison between a frozen prior skill version and a revision"
  - "Performing the final package review after creating or revising an agent skill"
  - "Running a smoke test for a skill on a roster harness"
  - "A project skill shares its name with a user-level, shared, or system-provided skill"
  - "A blind review cannot be started in the current environment"
symptoms:
  - "The context that authored a revision also grades it, and every case passes"
  - "A pass rests on the executor's summary or a filename rather than the artifact"
  - "A model quotes an instruction absent from the package under test"
  - "A smoke test records activation without naming which installed copy activated"
root_cause: missing_validation
resolution_type: workflow_improvement
related_components:
  - development_workflow
  - testing
  - documentation
tags:
  - agent-skills
  - independent-review
  - fresh-context
  - load-identity
  - skill-name-collision
  - smoke-test
  - false-positive
  - artifact-inspection
---

# Independent fresh-context review for agent skills

## Context

An agent-produced result is not evidence until someone else can check it. Two
different things go wrong, and they fail independently.

The first is **who judged it**. An author carries the assumptions of the
conversation that produced the artifact, which makes it easy to accept the
intended result instead of the observable one. A plausible executor summary
hides an incomplete artifact, and a filename or heading satisfies a weak check
while the output misses the required outcome.

The second is **which copy ran**. A fresh conversation and a clean repository
do not prove which same-named skill the harness loaded. During the
frontier-model retune (issue jrgilbertson/the-rookery#13), two policy probes
quoted rules absent from the project files and were discarded rather than
averaged into a result. Polished output from the wrong copy is still
contaminated.

`skills/creating-portable-skills/SKILL.md` gives judgment work to fresh agent
contexts and mechanical facts to the validator, and `tests/README.md` owns the
protocol both halves run under.

## Guidance

1. **Give judgment to a context that did not produce the work.** A Blind
   Review (see `CONCEPTS.md`) comes from an agent that neither saw the
   authoring discussion nor produced the artifact. One independent context
   grades the matched cases; a different one runs
   `skills/creating-portable-skills/references/review-checklist.md` top to
   bottom for the final package review.
2. **Do not let a user waiver stand in for the missing context.** The
   checklist's Evidence integrity section states that grader and final
   reviewer availability and independence cannot receive an exception. If no
   independent context can be started, prepare a self-contained handoff and
   leave the affected result unverified until a separate session completes it.
3. **Require concrete evidence for every pass.** The reviewer opens the
   artifacts and traces instead of trusting a summary, and challenges any
   check that is trivial, unverifiable from the supplied evidence, or silent
   on part of the required outcome.
4. **Use deterministic checks for mechanical facts.** `npx skills-ref
   validate` and equivalent scripts need no agent reviewer. Reserve fresh
   contexts for judgment.
5. **Prove which copy ran, from the run's own trace.** The smoke test
   installs the skill from current source into a disposable project on each
   roster harness, asks one trigger query, and confirms from the trace that
   the copy which activated is the just-installed one, by its path or base
   directory. Distinctive expected output may corroborate that; it cannot
   establish it on its own.
6. **Log `inconclusive`, not `pass`, when provenance is unconfirmed.** When a
   same-name copy exists in a user or system location and the activated copy
   cannot be identified, the result is inconclusive
   (`tests/README.md`, Running). Before rerunning, inventory project, user,
   shared-collection, and system locations for the name and move or disable
   the non-authoritative copies. Never delete a user's installation to
   simplify a test.
7. **Discard, do not average, a contaminated run.** If the output quotes a
   clause absent from the authoritative package, the run proves nothing about
   that package. Isolate the collision and rerun.
8. **Keep the claim inside what the run checked.** A trigger-suite pass is a
   proxy measure; only a smoke test shows native triggering. A smoke test
   shows installability and activation for one harness, not behavior. Log
   lines say what the run actually checked and stop there.

Record runs as one line per run in `tests/<skill-name>/log.md`:
`date | git rev | check | result | note`. Git is the archive, with no
hand-recorded hashes, session IDs, evidence labels, or run ledgers in test
artifacts.

## Why This Matters

The two failures produce the same outcome: a green result that could not have
gone red. A self-graded revision passes because the grader shares the author's
assumptions. A smoke test that records activation without provenance passes
whether or not the intended copy ran. A verification that cannot distinguish
success from a silent fallback is a false-positive generator, and the honest
response to an unresolvable one is `inconclusive` rather than a pass.

Independence and identity do not cover for each other. A fresh grader looking
at output from a stale same-name copy grades the wrong artifact. An
airtight identity trace judged by the author still inherits the author's
blind spots.

## When to Apply

- Instruction semantics, a trigger description, or a bundled resource changed
  and the change needs a matched comparison.
- A skill is being installed or evaluated on more than one roster harness, or
  its packaging or install path changed.
- A project skill shares its name with a user-level, shared, or
  system-provided skill.
- A model response mentions an instruction, section, or clause absent from the
  package under test.

Deterministic validation alone is enough for mechanical questions. Typo,
formatting, and link-only edits need no behavioral comparison.

## Examples

**Independence.** `tests/creating-portable-skills/cases/independent-fresh-context-review.md`
encodes the failure directly: the prompt asks the authoring context to grade
its own revision and nudges it to self-review and mark the step done. The
graded checklist requires it to decline, to name the fresh context as the only
acceptable grader, and to leave the review incomplete. Its provenance line
records both observed failures from the 2026-07-27/28 matched comparisons:
the authoring context grading itself, and a user exception replacing the
independent reviewer.

**Identity.** The 2026-07-30 Claude Code smoke line in
`tests/creating-portable-skills/log.md` passes on provenance, not on
activation alone: it installed from source into a disposable project and the
transcript shows the Skill tool reading the installed copy's own base
directory (`.claude/skills/creating-portable-skills` under that disposable
project). It explicitly supersedes an earlier activation-only run at
`9b76104`, which could not say which copy answered.

Earlier per-run numbers from the retired evidence-ledger artifacts live in git
history at commit `cc66ee8`, named by the run log's archive-pointer line.

## Related

- [Verify disposition claims before landing a prune](../workflow-issues/verify-disposition-claims-before-landing-a-prune.md)
  Independent review is the mechanism that caught the drift there, because
  the author's own review carried the assumptions that produced it.
- [Ship bundled skill helpers with an executable fail-closed contract](../workflow-issues/falsifiability-contracts-need-executable-tests.md)
  applies the same lesson to helper scripts: a contract that has never been
  executed cannot fail.
- [skills CLI ref targeting](../integration-issues/skills-cli-ref-not-checked-out.md)
  owns the remote-install mechanism detail and its false-positive install
  check; the shared principle is that a check unable to distinguish success
  from a silent fallback is not a check.
- Issue jrgilbertson/the-rookery#13 is the frontier-model retune that produced
  this guidance.
