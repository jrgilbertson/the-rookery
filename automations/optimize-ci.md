# Optimize CI

Review continuous integration and recommend improvements.

- **Cadence:** Saturday at 09:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** The Compound Engineering `ce-optimize` skill and access to the target repository's CI configuration.

The installed `ce-optimize` workflow builds measurement scaffolding before its
experiment approval gate. This prompt requests recommendations but does not
explicitly restrict that setup work. For a read-only audit, state that limit
when adapting the prompt.

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
```
