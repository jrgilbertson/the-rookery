---
module: creating-portable-skills skill evaluation
date: 2026-07-27
last_updated: 2026-07-28
problem_type: best_practice
component: testing_framework
severity: high
applies_when:
  - "Grading matched prior and revised agent-skill outputs"
  - "Performing a final package review after creating or revising an agent skill"
  - "Deciding whether artifact and execution-trace evidence supports a pass"
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
| Coverage | Which changed behaviors were tested and how far the conclusion reaches | Predeclared cases, controls, limitations, and an independent final review |

Record routine matched-comparison case construction, candidate decisions,
evidence labels, matched-comparison waivers, and Claim Ceiling results in the
baseline template
(`skills/creating-portable-skills/assets/baseline-test-template.md:7`). Record
listing-query construction, scoring, evidence states, and native checks in the
trigger template
(`skills/creating-portable-skills/assets/trigger-queries-template.md:8`).
Workflow and review files should link to these records instead of repeating
their thresholds or decision rules.

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
7. For listing judgments, record the result and a context or transcript
   reference in every run cell. A session ID can identify a distinct fresh run
   without preserving a transcript archive. If a decision depends on output
   details, also keep a concise supporting excerpt or durable transcript
   reference (`skills/creating-portable-skills/assets/trigger-queries-template.md:43`).

Keep routine verification proportionate. One observed execution is a smoke
probe and earns no baseline label. A small matched comparison with a
discriminating case and a stable control can support a directional
observation. Reliability, non-regression, or causal-improvement claims require
deeper evaluation that accounts for normal run variation.

## Why This Matters

An author carries assumptions from the conversation that produced the
artifact. Those assumptions make it easier to accept the intended result
instead of the observable one. A fresh grader reduces that contamination, and
a different fresh context for final review checks whether the evidence covers
the complete package rather than only the cases already graded.

Identity evidence does not prove quality, and a correct score on one case does
not prove a better grading policy. The evidence record must say which layer
passed and stop its claims there.

Keeping each rule in one authoritative record prevents the workflow, checklist,
and templates from diverging. Per-run context references make aggregate tables
auditable without turning routine skill work into transcript retention. A
context ID identifies which fresh run produced a judgment; it does not prove
what the run contained.

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

A report was required to identify three evidence-backed operational risks and
ask for approval before any changes. The probe paired a PASS summary with
checks that required only the filename `report.md` and a `Recommendations`
heading. Direct inspection showed one unsupported sentence and no approval
request. The trace also showed that the source data was never opened.

Both the prior and revised graders rejected the pass after inspecting the
artifact and trace. That result established correct behavior for one probe,
but it did not show that the revised policy was generally more reliable. The
separate policy comparison supported only the recorded procedural changes:
use an independent grader, inspect artifacts and traces directly, cite
concrete evidence and challenge weak checks, route subjective quality to human
or blind review, and preserve an unverified handoff when an independent
context is unavailable. The canonical result and its Claim Ceiling are retained
in `tests/creating-portable-skills/results.md`.

The later trigger review caught a different gap. The final tables recorded
bare `yes` and `no` judgments, so they did not support the claim that every
judgment came from a fresh process. The suite was rerun as 20 queries, three
times in each of two target cells. Each of the 120 cells now carries a unique
session ID. Sol recorded 30 expected should-trigger decisions and 30 expected
near-miss decisions. Opus recorded 29 of 30 expected should-trigger decisions,
with the remaining query passing two of three, and all 30 expected near-miss
decisions (`tests/creating-portable-skills/trigger-queries.md:201`). This
supports the recorded listing-proxy result for those queries and targets only.
It is not a reliability or non-regression claim.

## Related

- `docs/solutions/best-practices/cross-harness-dogfood-testing.md` explains why
  fresh context and loaded-package identity are separate requirements.
- `docs/solutions/best-practices/operationalize-abstract-qualifiers-in-instruction-review.md`
  shows why the quality of a check needs its own review pass.
- `docs/solutions/integration-issues/skills-cli-ref-not-checked-out.md` gives a
  concrete example of a green check that could not distinguish success from a
  silent fallback.
- `tests/creating-portable-skills/results.md` retains the canonical bounded
  verification summaries.
- Issue jrgilbertson/the-rookery#13 is the frontier-model retune that produced
  this guidance.
