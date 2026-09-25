---
# Delete every "#" comment line and every HTML comment when instantiating this
# template. Field limits and description rules: the "Package format" and
# "Descriptions and triggering" sections of creating-portable-skills'
# references/skills.md.
name: skill-name-here
description: "Use when [owned capability and triggering conditions, including non-obvious user phrasings]."
license: "[choose a license, or delete this field if the host collection declares one]"
# compatibility: optional. Declare only real command, network, credential, or
# environment requirements. Delete it when there are none.
---

# Skill Title

<!-- State the skill's one job and observable outcome.
Include only intent an agent cannot safely infer from the task context. -->

## Outcome and constraints

<!-- State the intended outcome,
including any required artifact or handoff. Name only hard constraints: facts
whose omission could change acceptability, safety, user authority, exact format,
or completion. Leave the reasoning and method open. Omit this section when
these facts are already clear elsewhere. -->

## Workflow

<!-- Provide only the instructions needed to reach the
outcome within its hard constraints, applying the checklist sections that
step 3 of creating-portable-skills names. Use a numbered sequence only when
order matters; for open-ended work, organize around outcomes and completion
criteria. When the skill does destructive or batch work, have it confirm the
exact targets and planned action against the system that owns those targets
before executing. -->

<!-- When invocation leads to distinct runtime branches,
route among them beside the corresponding branch instructions instead of
repeating the frontmatter description. -->

[Minimum instructions needed to reach the outcome within its constraints.]

<!-- Add one concise Example section only when it resolves
a real ambiguity or demonstrates an exact format. -->

## Gotchas

<!-- Include only failure modes observed in real work,
execution traces, or user corrections. State the correction. Delete this
section when there are none. -->

## Verification

<!-- Name the artifact or observable state that proves the
job is done. Prefer a deterministic check when one exists. -->
