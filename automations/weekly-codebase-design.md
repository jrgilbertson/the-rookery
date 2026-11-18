# Weekly codebase design

Review the codebase design and recommend improvements.

- **Cadence:** Saturday at 04:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** Matt Pocock's [`codebase-design` skill](https://github.com/mattpocock/skills/tree/main/skills/engineering/codebase-design) and access to the target repository. Each run also needs a clone of your private automation-state repository; see [Shared run state](README.md#shared-run-state).

## Prompt

```text
Before assessing, confirm the required skills are available to the selected agent. If a required skill is missing or cannot load, report it and stop. Do not install or update skills or plugins.

History: clone or update <your private automation-state repository> at `~/.local/state/automation-runs`. Read `weekly-codebase-design-<repository name>` runs and owner decisions before assessing. Follow that history repository's README for storage instructions, using its helper when available or its documented Git steps otherwise. Revisit declined findings only with new evidence.

Use `codebase-design` to review this repository and recommend improvements grounded in its current design and needs.

Assessment only: issue creation, implementation, and PR publication require separate approval.

Judge each draft recommendation as its own decision against current evidence, including recommendations to leave a confirmed finding unchanged and how the recommendations interact. The approval list holds only the recommendations you support, in leverage order, highest first, each with its evidence, tradeoffs, and uncertainty. List each recommendation you reject in one line with its reason, outside the approval list.

Save the final report afterward.
```
