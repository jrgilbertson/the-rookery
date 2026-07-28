---
# Delete every "#" comment line when instantiating this template.
name: skill-name-here
# name: lowercase kebab-case, at most 64 characters, matching the directory.
description: Use when [owned triggering conditions and user phrasings, including a non-obvious one]. [What it does, in one clause.]
# description: at most 1024 characters. Put trigger language first. Describe
# when to use the skill, not a summary of the workflow. Keep adjacent jobs in
# near-miss tests unless a positive destination resolves harmful ambiguity.
license: "[choose a license, or delete this field if the host collection declares one]"
# license: optional. Choose it deliberately; never carry over a template default.
# compatibility: optional. Declare only real command, network, credential, or
# environment requirements. Delete it when there are none.
---

# Skill Title

<!-- Delete this comment. State the skill's one job and observable outcome.
Include only intent an agent cannot safely infer from the task context. -->

## Outcome and constraints

<!-- Delete this comment. State the intended outcome and observable done state,
including any required artifact or handoff. Name only hard constraints: facts
whose omission could change acceptability, safety, user authority, exact format,
or completion. Leave the reasoning and method open. Omit this section when
these facts are already clear elsewhere. -->

## Workflow

<!-- Delete this comment. Provide only the instructions needed to reach the
outcome within its hard constraints. Keep exact formats, deterministic checks,
user authority boundaries, reusable resource requirements, and genuinely
fragile ordering explicit because those are System-Owned Invariants. Leave
reasoning and implementation choices to the agent. Use a numbered sequence only
when order matters; for open-ended work, organize around outcomes and
completion criteria. When naming several tools or approaches, give a default or
selection rule. For destructive or batch work, confirm the exact targets and
planned action against the system that owns those targets before execution. Put
branch-specific detail one level deep behind an explicit read-trigger. -->

<!-- Delete this comment. When invocation leads to distinct runtime branches,
route among them beside the corresponding branch instructions instead of
repeating the frontmatter description. -->

[Minimum instructions needed to reach the outcome within its constraints.]

<!-- Delete this comment. Add one concise Example section only when it resolves
a real ambiguity or demonstrates an exact format. -->

## Gotchas

<!-- Delete this comment. Include only failure modes observed in real work,
execution traces, or user corrections. State the correction. Delete this
section when there are none. -->

## Verification

<!-- Delete this comment. Name the artifact or observable state that proves the
job is done. Prefer a deterministic check when one exists. -->
