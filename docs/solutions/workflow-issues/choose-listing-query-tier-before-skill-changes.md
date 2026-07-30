---
title: Let users choose the listing-query tier before changing a skill
date: 2026-07-28
category: workflow-issues
module: creating-portable-skills verification
problem_type: workflow_issue
component: development_workflow
severity: medium
applies_when:
  - "Creating a new Agent Skill"
  - "Continuing an approved skill revision or migration"
  - "Choosing a listing-query tier for an ordinary personal skill or a public or unusually load-bearing skill"
tags:
  - agent-skills
  - verification-mode
  - listing-queries
  - trigger-contract
  - user-authority
superseded: 2026-07-30
---

> **Superseded (2026-07-30).** The verification-tier doctrine this learning
> describes was retired with the lightweight testing convention in
> `tests/README.md`, and the trigger/results records it cites were replaced
> by per-suite `triggers.md` and `log.md`. Kept as history; do not apply its
> tier-selection instruction. A `ce-compound-refresh` pass owns full
> reconciliation.

# Let users choose the listing-query tier before changing a skill

## Context

Skill verification has two useful listing-query tiers. An ordinary personal
skill can use a small routine set. A public or unusually load-bearing skill
needs broader, repeated judgments. When this distinction appeared only in the
evidence template, an agent could proceed without asking which tier the user
wanted.

This choice controls only listing-proxy evaluation. The selected tier sets the
query count, repetition, and tier-specific judgment rules used to check whether
a skill is selected for realistic requests and rejected for near misses.

## Guidance

Ask the user to choose between the ordinary personal and public or unusually
load-bearing listing-query tiers before change-producing work. Ask before
drafting a new skill. For a revision or migration, first complete the read-only
audit and obtain scope approval, then ask before editing. Do not ask during a
read-only audit, and do not ask again when the user has already chosen in the
current request (`skills/creating-portable-skills/SKILL.md:18`).

Briefly recommend the tier that fits the skill, but leave the decision with the
user. Record the choice in the trigger evidence and map it to the listing-query
tier defined by the authoritative trigger template
(`skills/creating-portable-skills/assets/trigger-queries-template.md:15`).

Keep the choice narrow. It must not change the matched behavioral comparison,
structural validation, native or installation checks, or declared model-harness
targets (`skills/creating-portable-skills/assets/trigger-queries-template.md:38`).

## Why This Matters

An early choice prevents people from forgetting the broader checks when a skill
will be public or unusually consequential. It also keeps routine personal skill
work proportionate. Limiting the choice to listing-proxy evaluation avoids
implying that one level has a different quality standard or a separate target
matrix.

A larger query set supports a broader activation check for the declared queries
and targets. It does not by itself establish behavioral reliability,
non-regression, or portability across other models and harnesses.

## When to Apply

Use this choice whenever creating a new skill or starting an approved change to
an existing skill. Recommend ordinary personal verification when the skill is
mainly for its owner and a listing mistake has limited consequences. Recommend
public or unusually load-bearing verification when the skill will be
distributed, governs consequential work, or shapes other skills.

Do not introduce the choice during a read-only audit because no verification
run has been authorized.

## Example

The `creating-portable-skills` skill is unusually load-bearing because it shapes
future skills. A matched comparison showed the revised workflow asking for the
choice in new-skill and approved-revision cases while leaving a read-only audit
control materially stable. The canonical summary is retained in
`tests/creating-portable-skills/results.md`. That is directional evidence for
the recorded cases, not a general reliability claim.

## Related

- [Use independent contexts for skill grading and review](../best-practices/independent-fresh-context-review-for-agent-skills.md)
- [Dogfood Agent Skills through their real harness paths](../best-practices/cross-harness-dogfood-testing.md)
- [Issue 13: Update creating-portable-skills for Claude Opus 5 and GPT-5.6 Sol](https://github.com/jrgilbertson/the-rookery/issues/13)
