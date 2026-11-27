# State-machine correctness audit

Assess whether application lifecycles follow their intended rules, including under retries and concurrency, and recommend fixes for approval.

- **Cadence:** Sunday at 04:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** Access to the target repository and its tests. Complex or concurrent areas also require TLA+ and the TLC model checker. Each run also needs a clone of your private automation-state repository; see [Shared run state](README.md#shared-run-state).

## Setup

Use a repository-specific slug in the prompt (`state-machine-audit-<repository name>`) and replace each `<placeholder>`. Keep the automation paused while validating its first manual run. The assessment reads the application and its tests; its report, models, and debugging evidence live in the private audit history. Issue creation and implementation follow separate owner approval.

## Prompt

```text
History: clone or update <your private automation-state repository> at `~/.local/state/automation-runs`. Read `state-machine-audit-<repository name>` runs and owner decisions before assessing. Follow that history repository's README for storage instructions, using its helper when available or its documented Git steps otherwise. Revisit declined findings only with new evidence.

Assess whether the application's behavior matches its intended rules over time.

Find explicit and implicit state machines and document their states, invariants, and transition tables in one report. Identify invalid states or transitions the code can actually reach, with evidence, including through retries and concurrency. Separate confirmed bugs from hypotheses, group related findings, and recommend fixes and regression tests by leverage. State what remains unassessed.

For complex or concurrent areas, use TLA+ and TLC to check the relevant lifecycle and interactions, including retries and failures. Check safety and liveness, stating assumptions, scope, and checking bounds. Connect model counterexamples to implementation evidence before calling them code bugs. Reuse and update prior assessment models.

Recommend the simplest complete fix for the underlying cause, judging the resulting lifecycle and its maintenance rather than the size of the patch. Understanding an implicit state machine does not require replacing it; recommend a replacement when evidence shows a meaningful improvement within the current goal.

Assessment only: run existing tests and isolated scratch reproductions. Keep reports, models, and debugging artifacts outside the application checkout. Do not modify application files, create or update issues, or publish PRs; implementation and issue creation require separate approval.

Judge each draft recommendation on its own against current evidence. Apply the same bar to recommendations to leave a confirmed finding unchanged, and check how recommendations interact. Put only the recommendations you support in the approval list, in leverage order, highest first, with each one's evidence, tradeoffs, and uncertainty. List each rejected recommendation in one line with its reason, outside the approval list.

Save the final report afterward.
```
