# Weekly codebase design

Review the codebase design and recommend improvements.

- **Cadence:** Saturday at 04:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** Matt Pocock's [`codebase-design` skill](https://github.com/mattpocock/skills/tree/main/skills/engineering/codebase-design), `ce-pov`, and access to the target repository. Each run also needs a clone of your private automation-state repository; see [Shared run state](README.md#shared-run-state).

## Prompt

```text
Before assessing, confirm the required skills are available to the selected agent. If a required skill is missing or cannot load, report it and stop. Do not install or update skills or plugins.

History: clone or update <your private automation-state repository> at `~/.local/state/automation-runs`. Read `weekly-codebase-design-<repository name>` runs and owner decisions before assessing. Follow that history repository's README for storage instructions, using its helper when available or its documented Git steps otherwise. Revisit declined findings only with new evidence.

Use `codebase-design` to review this repository and recommend improvements grounded in its current design and needs.

Assessment only: issue creation, implementation, and PR publication require separate approval.

Run `ce-pov` once on the draft recommendations as a whole, including recommendations to leave a confirmed finding unchanged and how the recommendations interact. Have it judge each recommendation as its own decision against current evidence. The approval list holds only the recommendations it supports, in leverage order, highest first, each with its evidence, tradeoffs, and uncertainty. List each recommendation it rejects in one line with its reason, outside the approval list. If `ce-pov` cannot finish, save useful assessment work, name the missing review, and keep the list provisional.

Save the final report afterward.
```
