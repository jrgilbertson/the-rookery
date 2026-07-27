---
# Delete every "#" comment line when instantiating this template.
name: skill-name-here
# name: lowercase kebab-case, at most 64 characters, matching the directory.
description: Use when [triggering conditions and user phrasings, including a non-obvious one]. [What it does, in one clause.] Do not use for [the closest near-miss and its destination].
# description: at most 1024 characters. Put trigger language first. Describe
# when to use the skill, not a summary of the workflow.
license: "[choose a license, or delete this field if the host collection declares one]"
# license: optional. Choose it deliberately; never carry over a template default.
# compatibility: optional. Declare only real command, network, credential, or
# environment requirements. Delete it when there are none.
---

# Skill Title

<!-- Delete this comment. State the skill's one job and observable outcome.
Include only intent an agent cannot safely infer from the task context. -->

## When to use

<!-- Delete this comment. State the trigger boundary and route near-misses.
Keep it consistent with the frontmatter description. -->

## Contract

<!-- Delete this comment. Name the output contract and success criteria, then
the hard constraints and decisions that remain with the user. Omit this section
if those facts are already clear elsewhere without duplication. -->

## Workflow

<!-- Delete this comment. Use the least-prescriptive instructions that protect
the contract. Give the agent freedom over reasoning and implementation. Keep
exact formats, deterministic checks, user authority boundaries, reusable
resource contracts, and genuinely fragile ordering explicit because those are
System-Owned Invariants. Use a numbered sequence only when order matters; for
open-ended work, organize around outcomes and completion criteria. Put
branch-specific detail one level deep behind an explicit read-trigger. -->

[Minimum instructions needed to satisfy the contract.]

## Gotchas

<!-- Delete this comment. Include only observed failure modes and their
correction. Delete this section when there are none. -->

## Verification

<!-- Delete this comment. Name the artifact or observable state that proves the
job is done. Prefer a deterministic check when one exists. -->
