# Test audit

Review the repository's tests, find gaps in what they protect, and recommend improvements.

- **Cadence:** Thursday at 21:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** The Compound Engineering `ce-simplify-code` skill and access to the target repository. Each run also needs a clone of your private automation-state repository; see [Shared run state](README.md#shared-run-state).

## Prompt

```text
Before assessing, confirm the required skills are available to the selected agent. If a required skill is missing or cannot load, report it and stop. Do not install or update skills or plugins.

History: clone or update <your private automation-state repository> at `~/.local/state/automation-runs`. Read `test-audit-<repository name>` runs and owner decisions before assessing. Follow that history repository's README for storage instructions, using its helper when available or its documented Git steps otherwise. Revisit declined findings only with new evidence.

Use `compound-engineering:ce-simplify-code` to audit this repo's tests and recommend improvements without applying them.

Then map material high-risk behaviors and invariants to the tests protecting them. Label the strongest evidence:

- declared: claimed by a name or document; test unread.
- inspected: assertions read and confirmed to exercise the real boundary.
- executed: test run and result observed.
- falsified: a safe, reverted break made the test fail.

Treat risks without inspected evidence as gaps or unknowns. Coverage, test count, and pass rate are diagnostic signals, not proof of protection. Recommend the cheapest test layer that exercises the real boundary.

Combine both passes, group findings by cause, include every material recommendation, and state what remains unassessed. Repository edits are limited to temporary, reverted test falsification. Issue creation, implementation, and PR publication require separate approval.

Judge each draft recommendation as its own decision against current evidence, including recommendations to leave a confirmed finding unchanged and how the recommendations interact. The approval list holds only the recommendations you support, in leverage order, highest first, each with its evidence, tradeoffs, and uncertainty. List each recommendation you reject in one line with its reason, outside the approval list.

Save the final report afterward.
```
