---
module: skill evaluation
date: 2026-07-27
last_updated: 2026-10-03
problem_type: best_practice
component: testing_framework
severity: high
applies_when:
  - "Grading matched prior and revised skill outputs"
  - "Performing a final package review after creating or revising a skill"
  - "Deciding whether a behavioral artifact crossed every workflow boundary named by its pass claim"
  - "Recording a result when an independent review context is unavailable"
  - "Recording fresh-context judgments without archiving full transcripts"
tags:
  - skills
  - independent-review
  - fresh-context
  - artifact-inspection
  - execution-traces
  - evidence-integrity
  - claim-ceiling
  - skill-evaluation
---

# Use independent contexts for skill grading and review

> The repository-specific eval formats, run protocol, and benchmark rules
> described here were retired on 2026-10-03. The evidence and independent-review
> principles remain useful; follow [SKILLS.md](../../../SKILLS.md#evaluation-workflow)
> for the current workflow. Case paths below refer to files in Git history.

## Context

Agent-authored skill changes need two kinds of verification. Deterministic
tools can check structural facts such as frontmatter, file identity, line
counts, and links. The former repository protocol ran affected evals once per
declared Executor target with a blind different-model grader and one independent
review of the package and evidence. Author inspection supplies no independent
evidence.

The distinction matters because a plausible executor summary can hide an
incomplete artifact. A filename or heading can satisfy a weak check while the
actual output misses the required outcome. The former protocol gave judgment work to independent agent contexts and left
mechanical checks to scripts. The current workflow is in
[SKILLS.md](../../../SKILLS.md#evaluation-workflow).

## Guidance

Keep three evidence layers separate:

| Layer | What it establishes | Suitable mechanism |
| --- | --- | --- |
| Provenance | Which package, model, harness, and configuration ran | Hashes, runtime metadata, load traces, and deterministic comparisons |
| Outcome evidence | Whether the output met the required outcome and hard constraints | Inspection of actual artifacts and relevant traces; blind different-model grading of the changed skill |
| Coverage | Which changed behaviors were tested and how far the conclusion reaches | Declared cases and limitations; one independent review of the package and evidence |

The retired protocol kept eval definitions in `evals/evals.json`, raw runs in
a machine-local archive, and one committed benchmark per graded round. Its
regression and attribution rules are historical, not current repository
requirements. The following practices describe that protocol; adapt them to
the selected evaluation workflow rather than restoring its formats or gates.

1. Run affected cases once per declared target in fresh contexts and confirm
   that the intended version loaded.
2. Give the independent different-model grader the final answer, all tool names
   and inputs, relevant artifacts and observations, and available child
   readouts. Remove variant labels, private reasoning, and author conclusions.
3. Inspect every failed grade against the original transcript. Distinguish a
   behavior failure, grader/assertion error, and capture gap. Keep original
   grades and explain corrections in notes.
4. Compare or rerun the prior skill only on failures to attribute changed text.
   Unresolved attribution stays unverified. Never compute an aggregate delta
   between unmatched cohorts or claim improvement from a baseline subset.
5. Give one independent reviewer the package and evidence. Use scripts for
   mechanical facts. The operator owns further iteration and stopping within
   the authorized budget.
6. If required independent judgment is unavailable, prepare a self-contained
   handoff and keep it unverified. Author self-review does not replace it.
7. Record only what the retained artifacts establish.

Treat a source edit as an evidence boundary. Preserve earlier artifacts with
their original revision labels, then identify which checks crossed the changed
instruction, case, or resource. Reinstall the new package before rerunning
affected behavior, and give each new behavioral artifact to an independent
grader. Do not rename or summarize an older output as though the new bytes produced it.

Package identity has two independent links:

1. Compare canonical source with the disposable installed package.
2. Prove from the runtime trace that the harness loaded that exact installed
   path or base directory.

Neither link substitutes for the other. An install comparison cannot rule out
a same-named runtime collision, and a loaded path does not prove its contents
match the intended source. If either link is missing, the run is inconclusive.

Make every claimed workflow transition observable in the case. “No write
before approval” and “safe write after approval” are separate behaviors: a
prompt that authorizes nothing can prove the first, but it cannot prove the
second. To claim the approved path, use a safe synthetic follow-up or disposable
fixture that causes the agent to re-read the authoritative target, revalidate
the exact approval, write once, and read the result back. Grade those operations
from the resulting artifact or trace, not from policy narration. Keep fixture
facts neutral and keep expected conclusions in the checklist or grader rather
than leaking them into the executor prompt.

Apply the same boundary to provider adapters. A deterministic seam can prove
which command ran, what disposable provider state changed, and whether exact
readback succeeded. It cannot prove that an agent chose to stop a later
approved effect when the harness never presented that effect to an agent or
batch executor. Put the later effect in a behavior case, make its disposition
observable, and grade the agent's decision in a fresh context. Absence from a
provider log is evidence only for operations that the scenario could actually
have emitted.

Keep routine verification proportionate. One graded execution supports only
that case, in that context, at that revision. A matched comparison can show
intended improvement across its declared discriminating cases and absence of
regression across the cases actually run. It does not by itself establish
general reliability, broad non-regression, or causal improvement.

## Why This Matters

An author carries assumptions from the conversation that produced the
artifact. Those assumptions make it easier to accept the intended result
instead of the observable one. A fresh grader reduces that contamination, and
an independent review checks whether the evidence covers
the complete package rather than only the cases already graded.

Identity evidence does not prove quality, and a correct score on one case does
not prove general reliability. The evidence record must say which layer passed
and stop its claims there.

An unexercised transition creates the same claim inflation inside one evidence
layer. A correct refusal before approval is not evidence that the agent handles
approval-time drift, duplicate writes, wrong targets, or failed readback. The
run log must name only the states and transitions the retained artifacts
actually demonstrate.

Keeping each rule in one authoritative record prevents the workflow, checklist,
and cases from diverging. The case and its graded artifact carry the evidence;
a context identifier can establish independence, but it cannot prove what the
run contained.

## When to Apply

Use [`SKILLS.md`](../../../SKILLS.md#evaluation-workflow) to select this
repository's current evaluation workflow.
A check establishes only its exercised behavior and does not establish
comparative improvement. Independent review is especially useful when success
depends on qualitative completeness, evidence use, authority boundaries, or
execution trace interpretation.

It also applies when pass/fail, waiver, scoring, or claim-limit rules appear in
more than one file, or when a trigger table contains bare judgments without
run-specific provenance.

Use deterministic validation alone for mechanical questions. Typo,
formatting, and link-only edits do not need a behavioral comparison. Broader
cross-model sweeps are separate work.

## Example

During `managing-issues` qualification, a final review found that the GitHub
command reference still allowed a relationship flag during issue creation,
even though the graph contract required authoritative node identity and
readback before any dependent edge. Correcting the package made the earlier
exact-install candidate runs and native activation smokes evidence for the old
bytes, not the correction. The correction required preserving those artifacts,
adding a deterministic check that rejects create-with-edge before state
changes, rerunning the affected behavior from a new exact install, regrading it
independently, and repeating native activation probes.
The source edit did not make the earlier work useless; it narrowed what that
work could still prove. The append-only record preserves both the failed review
and the corrected qualification (`tests/managing-issues/log.md`).

The same qualification exposed a narrower stopped-batch evidence error. A
provider fixture invoked one indeterminate create and then asserted that no
later edit appeared in its command log
(`tests/managing-issues/fixtures/run-provider-checks.py:214`). That can detect an
unexpected command from the fixture interaction, but it cannot prove an agent
declined a separately approved later effect because the harness never offered
one. In this branch, the corrected evidence keeps provider facts in the
deterministic runner, uses a small transition model that actually iterates
across later effects
(`tests/managing-issues/fixtures/run-graph-checks.py:198`), and grades the real
agent decision with a fresh-context case that supplies three ordered effects
and requires the third to remain `unapplied`
(`tests/managing-issues/cases/partial-mutation-and-global-stop.md:8`). The
retained run record limits its claim to that focused case
(`tests/managing-issues/log.md:111`).

A personal-chief-of-staff case exposed a vacuous pass at an action boundary.
Its first prompt correctly authorized no journal write, but the test and log
also claimed approval, write, and readback safety. No approved action existed,
so the post-approval path could not occur.

The original repair added a synthetic follow-up with exact approval and asked
for the authoritative re-read, revalidation, one-write, and CLI-readback
sequence. That was a bounded narration check, not executable acceptance
evidence. The current suite checks approval-time drift, exact-match decisions,
preservation proposals, and unclear readback in `tests/personal-chief-of-staff/cases/obsidian-canonical-access.md`.
Those checks supply source outcomes and grade the agent's decisions; they make
no CLI calls and claim no executed writes. Command syntax and Obsidian behavior
belong to the CLI owner's tests. No isolated launcher or test vault is needed
for these decision checks. A pass requires a fresh executor and independent
grading of its actual response. The
production order remains in "Revalidate, apply, and read back" in
`skills/personal-chief-of-staff/references/action-application.md`. A separate
pressure case asks the agent to keep a one-day failure labeled as isolated even
when the user explicitly requests durable capture, making the recurrence and
approval boundaries observable
(`tests/personal-chief-of-staff/cases/wind-down-coaching-and-durable-signal.md:24`).

## Related

- `docs/solutions/best-practices/cross-harness-dogfood-testing.md` explains why
  fresh context and loaded-package identity are separate requirements.
- `docs/solutions/best-practices/operationalize-abstract-qualifiers-in-instruction-review.md`
  shows why the quality of a check needs its own review pass.
- `docs/solutions/workflow-issues/falsifiability-contracts-need-executable-tests.md`
  explains why every documented state needs an executable failing specimen.
- `docs/solutions/conventions/keep-the-test-seam-out-of-the-shipped-skill.md`
  keeps rubric answers and harness accommodations out of the production skill.
- `docs/solutions/integration-issues/skills-cli-ref-not-checked-out.md` gives a
  concrete example of a green check that could not distinguish success from a
  silent fallback.
