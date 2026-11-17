# Improve audit

Survey the whole codebase with shadcn's `improve` skill and recommend improvements for approval.

- **Cadence:** Tuesday at 04:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** shadcn's [`improve` skill](https://github.com/shadcn/improve), this repository's [`checking-simplicity`](../skills/checking-simplicity/SKILL.md) skill, `ce-pov`, and access to the target repository. Each run also needs a clone of your private automation-state repository; see [Shared run state](README.md#shared-run-state).

## Setup

Use a repository-specific slug in the prompt, and keep the automation paused
while validating its first manual run.

The skill covers correctness, security, performance, tests, tech debt,
dependencies, developer experience, docs, and direction, and it returns many
more findings than the other reviews. The scheduled run therefore returns
every finding in leverage order and stops. Independent review runs only on the
findings you pick when you reply in that chat.

## Prompt

```text
Before assessing, confirm the required skills are available to the selected agent. If a required skill is missing or cannot load, report it and stop. Do not install or update skills or plugins.

History: clone or update <your private automation-state repository> at `~/.local/state/automation-runs`. Read `improve-audit-<repository name>` runs and owner decisions before assessing. Follow that history repository's README for storage instructions, using its helper when available or its documented Git steps otherwise. Revisit declined findings only with new evidence.

Use `improve` to audit this repository and recommend improvements. Run the skill as written, at its default effort and across all of its categories; other tools and automations covering an area do not narrow its scope.

Assessment only: stop after the vetted, prioritized findings and direction options. Plan files, `execute`, `--issues`, issue creation, implementation, and PR publication require separate approval. Approved plans go in the repository's ignored working path for plans.

List every vetted finding in leverage order, highest first. Score each with the four leverage factors, not with `improve`'s own Effort and Risk columns, and keep each finding's title stable between runs. Mark every finding `not reviewed`, save the report, and stop. The owner picks which findings to review; do not pick for them.

When the owner replies with the findings they picked, group those into coherent sets; split those needing materially different context. Include recommendations to leave a confirmed finding unchanged. Invoke `checking-simplicity` afresh on each set, covering every recommendation and their interactions. Skip it for an empty set; incomplete assessment remains a coverage gap. If independent review cannot finish, retain the assessment and label affected recommendations `review pending`; do not substitute self-review.

Then run `ce-pov` once on the revised picked recommendations as a whole, including review-pending items and interactions across sets. Have it judge each recommendation as its own decision against current evidence. The approval list holds only the recommendations it supports, in leverage order, highest first, each with its evidence, tradeoffs, uncertainty, and any pending-review label. List each recommendation it rejects in one line with its reason, outside the approval list. If either review cannot finish, save useful assessment work and name the missing review; without a completed `ce-pov`, keep the list provisional.

Save the updated report afterward.
```
