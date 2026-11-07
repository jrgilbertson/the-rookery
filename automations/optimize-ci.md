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
Use `ce-optimize` to assess CI and recommend improvements. Keep experiments within its approval requirements; recommendations do not authorize issue creation, implementation, or PR publication.

Reuse the measurement harness and experiment history at $HOME/.local/state/ci-optimize/<repository name>/. Keep new measurements dated and compare them with earlier runs.

Run `ce-pov` on the draft recommendations, then incorporate its judgment into the final prioritized recommendations for approval. Preserve evidence, tradeoffs, and uncertainty. Report blocked reviews and cases where no change is justified.

History: clone or update <your private automation-state repository> at `~/.local/state/automation-runs`. Use its helper to read `optimize-ci` runs and owner decisions before assessing, and save the final report afterward. Revisit declined findings only with new evidence. README documents storage and helper usage.
```
