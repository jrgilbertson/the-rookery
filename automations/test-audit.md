# Test audit

Review the repository's tests, find gaps in what they protect, and recommend improvements.

- **Cadence:** Thursday at 21:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** The Compound Engineering `ce-simplify-code` skill and access to the target repository. Each run also needs a clone of your private automation-state repository; see [Shared run state](README.md#shared-run-state).

## Setup

Use a repository-specific slug in the prompt (`test-audit-<repository name>`) and replace each `<placeholder>`. Keep the automation paused while validating its first manual run. Repository edits during a run are limited to temporary, reverted test falsification; issue creation, implementation, and PR publication follow separate owner approval.

## Prompt

```text
Before assessing, confirm the `ce-simplify-code` skill is available to the selected agent. If it is missing or cannot load, report it and stop. Do not install or update skills or plugins.

History: clone or update <your private automation-state repository> at `~/.local/state/automation-runs`. Read `test-audit-<repository name>` runs and owner decisions before assessing. Follow that history repository's README for storage instructions, using its helper when available or its documented Git steps otherwise. Revisit declined findings only with new evidence.

Use `ce-simplify-code` to audit this repo's tests and recommend improvements without applying them.

Then map material high-risk behaviors and invariants to the tests protecting them. Label the strongest evidence:

- declared: claimed by a name or document; test unread.
- inspected: assertions read and confirmed to exercise the real boundary.
- executed: test run and result observed.
- falsified: a safe, reverted break made the test fail.

Treat risks without inspected evidence as gaps or unknowns. Coverage, test count, and pass rate are diagnostic signals, not proof of protection. Recommend the cheapest test layer that exercises the real boundary.

Combine both passes, group findings by cause, include every material recommendation, and state what remains unassessed. Repository edits are limited to temporary, reverted test falsification. Issue creation, implementation, and PR publication require separate approval.

Judge each draft recommendation on its own against current evidence. Apply the same bar to recommendations to leave a confirmed finding unchanged, and check how recommendations interact. Put only the recommendations you support in the approval list, in leverage order, highest first, with each one's evidence, tradeoffs, and uncertainty. List each rejected recommendation in one line with its reason, outside the approval list.

Save the final report afterward.
```
