# Improve audit

Survey the whole codebase with shadcn's `improve` skill and recommend improvements for approval.

- **Cadence:** Tuesday at 04:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** shadcn's [`improve` skill](https://github.com/shadcn/improve), this repository's [`checking-simplicity`](../skills/checking-simplicity/SKILL.md) skill, `ce-pov`, and access to the target repository. Each run also needs a clone of your private automation-state repository; see [Shared run state](README.md#shared-run-state).

Before scheduling, install the skill for the agent selected in Orca with
`npx skills add shadcn/improve`. Use a repository-specific slug in the prompt,
and keep the automation paused while validating its first manual run.

The skill covers correctness, security, performance, tests, tech debt,
dependencies, developer experience, docs, and direction, and it returns many
more findings than the other reviews. The recommendation review therefore
covers the larger recommendations and the highest-leverage findings, not every
one.

## Prompt

```text
History: clone or update <your private automation-state repository> at `~/.local/state/automation-runs`. Read `improve-audit-<repository name>` runs and owner decisions before assessing. Follow that history repository's README for storage instructions, using its helper when available or its documented Git steps otherwise. Revisit declined findings only with new evidence.

Use `improve` to audit this repository and recommend improvements. Run the skill as written, at its default effort and across all of its categories; other tools and automations covering an area do not narrow its scope.

Assessment only: stop after the vetted, prioritized findings and direction options. Plan files, `execute`, `--issues`, issue creation, implementation, and PR publication require separate approval. Approved plans go in the repository's ignored working path for plans, not a tracked `plans/` folder.

Select recommendations of medium or large effort and the ten highest-leverage findings for review. List the remaining findings without that review. Report a finding that returns after its fix as a repeat.

Group the selected recommendations into coherent sets; split those needing materially different context. Within that selection, include recommendations to leave a confirmed finding unchanged. Each run, invoke `checking-simplicity` afresh on each set, covering every recommendation and their interactions. Skip it for an empty set; incomplete assessment remains a coverage gap. If independent review cannot finish, retain the assessment and label affected recommendations `review pending`; do not substitute self-review.

Run `ce-pov` once on the revised selected recommendations as a whole, including review-pending items and interactions across sets. Incorporate its judgment into the final prioritized recommendations for approval, preserving evidence, tradeoffs, uncertainty, and any pending-review labels. If either review cannot finish, save useful assessment work and name the missing review; without a completed `ce-pov`, keep the list provisional.

Save the final report afterward.
```
