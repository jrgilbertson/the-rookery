---
title: Separate scout measurement stages from authoring capacity
date: 2026-08-12
last_updated: 2026-09-10
category: architecture-patterns
module: skills/repo-gardener/reconciliation
problem_type: architecture_pattern
component: development_workflow
severity: high
applies_when:
  - "An autonomous workflow scouts many source records before qualifying recommendations"
  - "Deterministic evaluators are being asked to certify qualitative model decisions"
  - "Read-only analysis and authored work have different capacity limits"
  - "Repository policy may change while an autonomous run is active"
  - "A durable run history is useful but per-step receipts add ceremony without assurance"
related_components:
  - assistant
  - testing_framework
tags:
  - autonomous-agents
  - repository-gardening
  - model-judgment
  - structural-verification
  - two-record-closure
  - live-policy
  - data-trust
  - execution-parallelism
---

# Separate scout measurement stages from authoring capacity

This learning documented Repo Gardener's two-record tracker protocol,
structural checkers, and capacity accounting. That machinery was removed
on 2026-09-10 because it turned every uncertainty into a no-op run.
Ceremony around opened and closed records, revision check points, and
per-area mutation grants did not make the morning report more true.

The surviving lesson is that qualitative judgment stays with the model:
which work is small, testable, and worth shipping, and when a source gap
is a finding rather than a stop. Deterministic checks should only prove
mechanically falsifiable facts. They must not certify that a candidate
matters or that a plan is good.

The current skill is one short unattended pass. It reads
`.agents/repo-gardener.yaml`, runs approved scans, senses five areas,
dispatches Executors that each ship one reviewable pull request, and
posts one plain morning report. See
[Repo Gardener](../../../skills/repo-gardener/SKILL.md).
