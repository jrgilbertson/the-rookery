# Optimize CI

Review continuous integration and recommend improvements.

- **Cadence:** Saturday at 09:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** The Compound Engineering `ce-optimize` skill and access to the target repository's CI configuration.

The job is read-only. The installed `ce-optimize` workflow builds measurement
scaffolding before its experiment approval gate, so the prompt keeps that work
outside the repository and forbids changes to it.

## Prompt

```text
ce-optimize look at the CI and provide recommendations for improvement.

Recommendations only. Do not edit tracked files or create branches, commits,
pushes, pull requests, or issues. Measure from read-only sources such as
workflow files and `gh run` data, and keep any scratch scripts or data in a
temporary directory outside the repository. Return a short prioritized list;
give each item its measured evidence, expected saving, and risk.
```
