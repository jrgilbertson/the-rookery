# Test audit

Review the repository's tests, find gaps in what they protect, and recommend improvements.

- **Cadence:** Thursday at 21:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** The Compound Engineering `ce-simplify-code` skill, this repository's [`checking-simplicity`](../skills/checking-simplicity/SKILL.md) skill, `ce-pov`, and access to the target repository. Each run also needs a clone of your private automation-state repository; see [Shared run state](README.md#shared-run-state).

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

Group related draft recommendations into coherent sets; split those needing materially different context. Include recommendations to leave a confirmed finding unchanged. Each run, invoke `checking-simplicity` afresh on each set, covering every recommendation and their interactions. Skip it for an empty set; incomplete assessment remains a coverage gap. If independent review cannot finish, retain the assessment and label affected recommendations `review pending`; do not substitute self-review.

Run `ce-pov` once on the revised recommendations as a whole, including review-pending items and interactions across sets. Have it judge each recommendation as its own decision against current evidence. The approval list holds only the recommendations it supports, in leverage order, highest first, each with its evidence, tradeoffs, uncertainty, and any pending-review label. List each recommendation it rejects in one line with its reason, outside the approval list. If either review cannot finish, save useful assessment work and name the missing review; without a completed `ce-pov`, keep the list provisional.

Save the final report afterward.
```
