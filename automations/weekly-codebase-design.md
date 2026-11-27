# Weekly codebase design

Survey the codebase for modules worth deepening.

- **Cadence:** Saturday at 04:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** Matt Pocock's [`improve-codebase-architecture` skill](https://github.com/mattpocock/skills/tree/main/skills/engineering/improve-codebase-architecture), its `codebase-design` vocabulary dependency, and access to the target repository. Each run also needs a clone of your private automation-state repository; see [Shared run state](README.md#shared-run-state).

## Setup

Use a repository-specific slug in the prompt (`weekly-codebase-design-<repository name>`) and replace each `<placeholder>`. Keep the automation paused while validating its first manual run. The scheduled run stops after saving the report; interactive design discussion happens in a follow-up with the owner, and issue creation, implementation, and PR publication follow separate approval.

## Prompt

```text
Before assessing, confirm `improve-codebase-architecture` and its `codebase-design` vocabulary dependency are available to the selected agent. If either skill is missing or cannot load, report it and stop. Do not install or update skills or plugins.

History: clone or update <your private automation-state repository> at `~/.local/state/automation-runs`. Read `weekly-codebase-design-<repository name>` runs and owner decisions before assessing. Follow that history repository's README for storage instructions, using its helper when available or its documented Git steps otherwise. Revisit declined findings only with new evidence.

Use `improve-codebase-architecture` to survey this repository for modules worth deepening. Start with areas that change frequently. Also inspect older, infrequently changed modules for design debt that still makes changes or testing harder. Present candidates in the final Markdown report using the approval rules below. End the scheduled run after saving the report and leave interactive design discussion and follow-up questioning for a session with the owner.

Assessment only: issue creation, implementation, and PR publication require separate approval.

Judge each draft recommendation on its own against current evidence. Apply the same bar to recommendations to leave a confirmed finding unchanged, and check how recommendations interact. Put only the recommendations you support in the approval list, in leverage order, highest first, with each one's evidence, tradeoffs, and uncertainty. List each rejected recommendation in one line with its reason, outside the approval list.

Save the final report afterward.
```
