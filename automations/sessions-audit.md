# Sessions audit

Review recent AI sessions for changes that could improve development effectiveness.

- **Cadence:** Daily at 03:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** Access to the AI session histories being reviewed and the repository's current guidance.

## Prompt

```text
Review my AI sessions from the last 24 hours across Claude, Codex, Grok, and other accessible sources, together with The Rookery repository's skills, workflows, guidance, and related configuration.

Identify the changes most likely to improve development effectiveness, reduce recurring friction, and help the code and workflow improve over time. Prioritize impact over ease of implementation.

Investigate whatever the evidence warrants. Relevant patterns include repeated corrections, excessive coordination, missing domain knowledge, and guidance that conflicts, duplicates other mechanisms, or constrains capable models unnecessarily. Consult earlier sessions when useful.

Recommend concrete changes to create, update, delete, or consolidate repo content and mechanisms. Consider code, tests, tooling, and controls alongside skills and instructions.

Present prioritized recommendations backed by session IDs, short quotes or sequences, and relevant repo paths. Explain the proposed change, expected benefit, material tradeoffs, and uncertainty. Include draft wording where it helps us decide. Note gaps in the sources available to you, and identify the single highest-impact recommendation.

Return recommendations for approval. Do not modify skills, files, or configuration until I approve specific changes.
```
