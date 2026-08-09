---
module: agent-skill evaluation
date: 2026-07-27
last_updated: 2026-08-09
problem_type: best_practice
component: testing_framework
severity: high
applies_when:
  - "Grading matched prior and revised agent-skill outputs"
  - "Performing a final package review after creating or revising an agent skill"
  - "Deciding whether a behavioral artifact crossed every workflow boundary named by its pass claim"
  - "Recording a result when an independent review context is unavailable"
  - "Recording fresh-context judgments without archiving full transcripts"
tags:
  - agent-skills
  - independent-review
  - fresh-context
  - artifact-inspection
  - execution-traces
  - evidence-integrity
  - claim-ceiling
  - skill-evaluation
---

# Use independent contexts for skill grading and review

## Context

Agent-authored skill changes need two kinds of verification. Deterministic
tools can check structural facts such as frontmatter, file identity, line
counts, and links. Behavioral grading and final package review require
judgment, so the author or artifact producer should not perform them.

The distinction matters because a plausible executor summary can hide an
incomplete artifact. A filename or heading can satisfy a weak check while the
actual output misses the required outcome. The workflow in
`skills/creating-portable-skills/SKILL.md` therefore gives judgment work to
fresh agent contexts and leaves mechanical checks to scripts.

## Guidance

Keep three evidence layers separate:

| Layer | What it establishes | Suitable mechanism |
| --- | --- | --- |
| Provenance | Which package, model, harness, and configuration ran | Hashes, runtime metadata, load traces, and deterministic comparisons |
| Outcome evidence | Whether the output met the required outcome and hard constraints | Independent inspection of actual artifacts and relevant traces |
| Coverage | Which changed behaviors were tested and how far the conclusion reaches | Declared cases, limitations, and an independent final review |

Keep the durable record small: self-contained case files contain the prompt and
binary checklist, while the log keeps one bounded line per run or check
(`tests/README.md:10`). Behavioral revisions use matched prior/candidate runs in
fresh contexts and ship only when discriminating cases improve without
regression (`tests/README.md:64`).

For a substantive skill change:

1. Run matched variants in fresh contexts and confirm the intended version was
   loaded.
2. Give the outputs and relevant traces to a separate fresh-context grader who
   did not author the change or produce either artifact.
3. Require concrete evidence for every pass. The grader should challenge any
   check that is trivial, cannot be verified from the supplied evidence, or
   omits part of the required outcome.
4. Give the complete package and evidence record to another fresh-context
   agent for the final checklist and holistic review.
5. Use deterministic scripts for mechanical facts. They do not need an agent
   reviewer.
6. If an independent context is unavailable, prepare a self-contained handoff
   and keep the affected result unverified. Author self-review does not replace
   the missing context.
7. Record the result at the narrowest level the artifact supports. A log line
   states only what its run actually checked (`tests/README.md:82`).

Make every claimed workflow transition observable in the case. “No write
before approval” and “safe write after approval” are separate behaviors: a
prompt that authorizes nothing can prove the first, but it cannot prove the
second. To claim the approved path, use a safe synthetic follow-up or disposable
fixture that causes the agent to re-read the authoritative target, revalidate
the exact approval, write once, and read the result back. Grade those operations
from the resulting artifact or trace, not from policy narration. Keep fixture
facts neutral and keep expected conclusions in the checklist or grader rather
than leaking them into the executor prompt.

Keep routine verification proportionate. One graded execution supports only
that case, in that context, at that revision. A matched comparison can show
intended improvement across its declared discriminating cases and absence of
regression across the cases actually run. It does not by itself establish
general reliability, broad non-regression, or causal improvement.

## Why This Matters

An author carries assumptions from the conversation that produced the
artifact. Those assumptions make it easier to accept the intended result
instead of the observable one. A fresh grader reduces that contamination, and
a different fresh context for final review checks whether the evidence covers
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

Apply this pattern when instruction semantics, trigger descriptions, or
bundled resources change. It is especially useful when success depends on
qualitative completeness, evidence use, authority boundaries, or execution
trace interpretation.

It also applies when pass/fail, waiver, scoring, or claim-limit rules appear in
more than one file, or when a trigger table contains bare judgments without
run-specific provenance.

Use deterministic validation alone for mechanical questions. Typo,
formatting, and link-only edits do not need a behavioral comparison. Expand
beyond a small matched comparison only when the requested claim requires it.

## Example

A personal-chief-of-staff case exposed a vacuous pass at an action boundary.
Its first prompt correctly authorized no journal write, but the test and log
also claimed approval, write, and readback safety. No approved action existed,
so the post-approval path could not occur.

The repaired case keeps that no-approval turn, then adds a separate synthetic
follow-up with exact approval and observable authoritative re-read,
revalidation, one supported write, and CLI readback
(`tests/personal-chief-of-staff/cases/wind-down-journal-ownership.md:11`). The
production contract requires that same order
(`skills/personal-chief-of-staff/references/source-behavior.md:278`), and the
result log records the bounded matched-run outcomes
(`tests/personal-chief-of-staff/log.md:43`). A separate pressure case asks the
agent to promote a one-day failure into durable learning, making the refusal
behavior observable instead of merely describing it
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
