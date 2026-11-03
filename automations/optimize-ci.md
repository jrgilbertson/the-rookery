# Optimize CI

Review continuous integration and recommend improvements.

- **Cadence:** Saturday at 09:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** The Compound Engineering `ce-optimize` skill and access to the target repository's CI configuration. Each run also needs a clone of your private automation-state repository; see [Shared run state](README.md#shared-run-state).

The installed `ce-optimize` workflow builds measurement scaffolding before its
experiment approval gate. This prompt asks for recommendations and leaves that
setup work to the skill.

Orca starts each run in a new worktree, and `ce-optimize` keeps its state in
the checkout unless a durable state root is named. The prompt names one outside
the repository, so each run reuses the harness and compares against earlier
runs.

## Prompt

```text
ce-optimize look at the CI and provide recommendations for improvement.

Use $HOME/.local/state/ci-optimize/<repository name>/ as the durable state root, so
the measurement harness and experiment logs outlive this run's worktree. Reuse
the harness already there, start a new dated experiment for this run, and
compare its results with earlier runs.

Shared state: follow the run contract in ~/.local/state/automation-runs/README.md for the `optimize-ci` folder; clone <your private automation-state repository> there first if it is missing. Before you start, read that folder's decisions.md and its three newest runs from any host. When you finish, write this run's file there and push it. When the owner answers your findings, record the answers in decisions.md and push before acting on them.
```
