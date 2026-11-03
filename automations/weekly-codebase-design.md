# Weekly codebase design

Review the codebase design and recommend improvements.

- **Cadence:** Saturday at 04:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** Matt Pocock's [`codebase-design` skill](https://github.com/mattpocock/skills/tree/main/skills/engineering/codebase-design) and access to the target repository. Each run also needs a clone of your private automation-state repository; see [Shared run state](README.md#shared-run-state).

Before scheduling, install the skill for the agent selected in Orca. Follow the
[upstream installation instructions](https://github.com/mattpocock/skills#installation-30-second-setup)
for that agent, or run `npx skills@latest add mattpocock/skills` and select
`codebase-design`.

## Prompt

```text
codebase-design review the repo and provide recommendations for improvement.

Shared state: follow the run contract in ~/.local/state/automation-runs/README.md for the `weekly-codebase-design` folder; clone <your private automation-state repository> there first if it is missing. Before you start, read that folder's decisions.md and its three newest runs from any host. When you finish, write this run's file there and push it. When the owner answers your findings, record the answers in decisions.md and push before acting on them.
```
