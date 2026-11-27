# Improve audit

Survey the whole codebase with shadcn's `improve` skill and recommend improvements for approval.

- **Cadence:** Tuesday at 04:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** shadcn's [`improve` skill](https://github.com/shadcn/improve), [`managing-issues`](../skills/managing-issues/SKILL.md), and access to the target repository and its issue tracker. Each run also needs a clone of your private automation-state repository; see [Shared run state](README.md#shared-run-state).

## Setup

Use a repository-specific slug in the prompt (`improve-audit-<repository name>`) and replace each `<placeholder>`. Keep the automation paused while validating its first manual run.

The skill covers correctness, security, performance, tests, tech debt,
dependencies, developer experience, docs, and direction, and it returns many
more findings than the other reviews. The scheduled run therefore returns
every finding in leverage order, names any open issue that already covers it,
and stops. Judgment runs only on the findings you pick when you reply in that
chat.

## Prompt

```text
Before assessing, confirm `improve` and `managing-issues` are available to the selected agent. If either skill is missing or cannot load, report it and stop. Do not install or update skills or plugins.

History: clone or update <your private automation-state repository> at `~/.local/state/automation-runs`. Read `improve-audit-<repository name>` runs and owner decisions before assessing. Follow that history repository's README for storage instructions, using its helper when available or its documented Git steps otherwise. Revisit declined findings only with new evidence.

Use `improve` to audit this repository and recommend improvements. Run the skill as written, at its default effort and across all of its categories; other tools and automations covering an area do not narrow its scope.

Assessment only: stop after the vetted, prioritized findings and direction options. Plan files, `execute`, `--issues`, issue creation, implementation, and PR publication require separate approval. Approved plans go in the repository's ignored working path for plans.

Before saving the report, use `managing-issues` read-only to check the repository's tracker for open issues that already cover any vetted finding, and name each covering open issue beside its finding. If the tracker is unreachable or open-issue results are truncated, report that coverage gap instead of treating unchecked findings as untracked.

List every vetted finding in leverage order, highest first. Score each with the four leverage factors, not with `improve`'s own Effort and Risk columns, and keep each finding's title stable between runs. Mark every finding `not reviewed`, save the report, and stop. The owner picks which findings to review; do not pick for them.

When the owner replies with the findings they picked, judge each picked recommendation on its own against current evidence. Apply the same bar to recommendations to leave a confirmed finding unchanged, and check how recommendations interact. Put only the recommendations you support in the approval list, in leverage order, highest first, with each one's evidence, tradeoffs, and uncertainty. List each rejected recommendation in one line with its reason, outside the approval list.

Save the judgment as a new timestamped follow-up report under `runs/` that references the initial scan report (never overwrite any saved file under `runs/`), and append the owner's answers to `decisions.md` through the history repository's storage procedure.
```
