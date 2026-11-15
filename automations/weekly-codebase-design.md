# Weekly codebase design

Review the codebase design and recommend improvements.

- **Cadence:** Saturday at 04:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** Matt Pocock's [`codebase-design` skill](https://github.com/mattpocock/skills/tree/main/skills/engineering/codebase-design), this repository's [`checking-simplicity`](../skills/checking-simplicity/SKILL.md) skill, `ce-pov`, and access to the target repository. Each run also needs a clone of your private automation-state repository; see [Shared run state](README.md#shared-run-state).

## Prompt

```text
Before assessing, confirm the required skills are available to the selected agent. If a required skill is missing or cannot load, report it and stop. Do not install or update skills or plugins.

History: clone or update <your private automation-state repository> at `~/.local/state/automation-runs`. Read `weekly-codebase-design` runs and owner decisions before assessing. Follow that history repository's README for storage instructions, using its helper when available or its documented Git steps otherwise. Revisit declined findings only with new evidence.

Use `codebase-design` to review this repository and recommend improvements grounded in its current design and needs.

Assessment only: issue creation, implementation, and PR publication require separate approval.

Group related draft recommendations into coherent sets; split those needing materially different context. Include recommendations to leave a confirmed finding unchanged. Each run, invoke `checking-simplicity` afresh on each set, covering every recommendation and their interactions. Skip it for an empty set; incomplete assessment remains a coverage gap. If independent review cannot finish, retain the assessment and label affected recommendations `review pending`; do not substitute self-review.

Run `ce-pov` once on the revised recommendations as a whole, including review-pending items and interactions across sets. Incorporate its judgment into the final prioritized recommendations for approval, preserving evidence, tradeoffs, uncertainty, and any pending-review labels. If either review cannot finish, save useful assessment work and name the missing review; without a completed `ce-pov`, keep the list provisional.

Save the final report afterward.
```
