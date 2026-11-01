# Optimize CI

Review continuous integration and recommend improvements.

- **Cadence:** Saturday at 09:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** The Compound Engineering `ce-optimize` skill and access to the target repository's CI configuration.

The installed `ce-optimize` workflow builds measurement scaffolding before its
experiment approval gate. This prompt requests recommendations but does not
explicitly restrict that setup work. For a read-only audit, state that limit
when adapting the prompt.

## Prompt

```text
ce-optimize look at the CI and provide recommendations for improvement.
```
