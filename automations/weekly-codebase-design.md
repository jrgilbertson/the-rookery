# Weekly codebase design

Review the codebase design and recommend improvements.

- **Cadence:** Saturday at 04:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** Matt Pocock's [`codebase-design` skill](https://github.com/mattpocock/skills/tree/main/skills/engineering/codebase-design), this repository's [`checking-simplicity`](../skills/checking-simplicity/SKILL.md) skill, and access to the target repository. Each run also needs a clone of your private automation-state repository; see [Shared run state](README.md#shared-run-state).

Before scheduling, install the skill for the agent selected in Orca. Follow the
[upstream installation instructions](https://github.com/mattpocock/skills#installation-30-second-setup)
for that agent, or run `npx skills@latest add mattpocock/skills` and select
`codebase-design`.

## Prompt

```text
Use `codebase-design` to review this repository and recommend improvements grounded in its current design and needs.

Assessment only: issue creation, implementation, and PR publication require separate approval.

Run `checking-simplicity` on each draft recommendation, then run `ce-pov` on the revised recommendations and incorporate its judgment into the final prioritized recommendations for approval. Preserve evidence, tradeoffs, and uncertainty. Report blocked reviews and cases where no change is justified.

History: clone or update <your private automation-state repository> at `~/.local/state/automation-runs`. Read `weekly-codebase-design` runs and owner decisions before assessing, and save the final report afterward. Follow the README's storage instructions, using its helper when available or its documented Git steps otherwise. Revisit declined findings only with new evidence.
```
