# Weekly codebase design

Survey the codebase for modules worth deepening.

- **Cadence:** Saturday at 04:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** Matt Pocock's [`improve-codebase-architecture` skill](https://github.com/mattpocock/skills/tree/main/skills/engineering/improve-codebase-architecture), its `codebase-design` vocabulary dependency, and access to the target repository. Each run also needs a clone of your private automation-state repository; see [Shared run state](README.md#shared-run-state).

## Prompt

```text
Before assessing, confirm `improve-codebase-architecture` and its `codebase-design` vocabulary dependency are available to the selected agent. If either skill is missing or cannot load, report it and stop. Do not install or update skills or plugins.

History: clone or update <your private automation-state repository> at `~/.local/state/automation-runs`. Read `weekly-codebase-design-<repository name>` runs and owner decisions before assessing. Follow that history repository's README for storage instructions, using its helper when available or its documented Git steps otherwise. Revisit declined findings only with new evidence.

Use `improve-codebase-architecture` to survey this repository for modules worth deepening. Start with areas that change frequently. Present candidates in the final Markdown report using the approval rules below. End the scheduled run after saving the report and leave interactive design and grilling for a follow-up with the owner.

Assessment only: issue creation, implementation, and PR publication require separate approval.

Judge each draft recommendation as its own decision against current evidence, including recommendations to leave a confirmed finding unchanged and how the recommendations interact. The approval list holds only the recommendations you support, in leverage order, highest first, each with its evidence, tradeoffs, and uncertainty. List each recommendation you reject in one line with its reason, outside the approval list.

Save the final report afterward.
```
