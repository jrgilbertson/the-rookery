---
title: Integrate research depth without exposing workflow telemetry
date: 2026-08-03
category: design-patterns
module: skills
problem_type: design_pattern
component: assistant
severity: medium
applies_when:
  - A research skill uses internal analytical checks and execution records
tags: [skills, research, output-design, systems-thinking, first-principles]
---

# Integrate research depth without exposing workflow telemetry

## Context

A research workflow required separate first-principles and systems-thinking
sections plus an execution manifest in every full briefing. The checks improved
rigor, but their fixed placement produced mechanical prose and made a human
reader consume internal workflow state.

## Guidance

Treat analytical methods as research-quality checks, not report headings.
Apply them while choosing questions, evaluating sources, mapping contradictions,
and synthesizing findings. Keep facts, assumptions, mechanisms, system
relationships, and downstream effects traceable, but render them only where they
help the reader.

Keep the execution record internal for isolation, degradation, and fidelity
review. Normal output should disclose only limitations that affect how the
reader interprets the answer. Expose the complete record when the user requests
an audit or trace.

The Storm Research contract implements this split in
`skills/storm-research/SKILL.md`, with detailed conditional checks in
`skills/storm-research/references/analysis-methods.md` and the human output shape
in `skills/storm-research/references/briefing-template.md`.

## Why This Matters

Requiring a heading proves only that a section exists. Moving the checks into
question selection changes what gets researched, while separating internal
telemetry from public output keeps the final artifact useful without weakening
verification.

## When to Apply

- A workflow has useful internal checks that have become mandatory prose.
- A reader-facing deliverable includes executor, queue, or reviewer telemetry.
- A method should affect evidence collection earlier than final synthesis.

## Examples

Before: research first, then append mandatory analytical sections and a full
execution manifest.

After: use foundational and systems-oriented questions throughout research,
integrate material findings into natural sections, and retain the run record
only for internal fidelity review or an explicitly requested audit.

## Related

- `docs/solutions/design-patterns/allow-honest-nulls-in-mandatory-novelty-fields.md`
- `docs/solutions/design-patterns/isolate-adversarial-mutations-in-runtime-evaluators.md`
