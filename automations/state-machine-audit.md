# State-machine correctness audit

Assess whether application lifecycles follow their intended rules, including under retries and concurrency, and recommend fixes for approval.

- **Cadence:** Sunday at 04:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** Access to the target repository and its tests, TLA+ and the TLC model checker for complex or concurrent areas, and this repository's [`checking-simplicity`](../skills/checking-simplicity/SKILL.md) skill. Each run also needs a clone of your private automation-state repository and `ce-pov` for the final recommendation review; see [Shared run state](README.md#shared-run-state).

Use a repository-specific slug in the prompt. Keep the automation paused while validating its first manual run. The assessment reads the application and issue trackers; its report, models, and debugging evidence live in the private audit history. Issue creation and implementation follow separate owner approval.

## Prompt

```text
Assess whether the application's behavior matches its intended rules over time.

Find explicit and implicit state machines and document their states, invariants, and transition tables in one report. Identify invalid states or transitions the code can actually reach, with evidence, including through retries and concurrency. Separate confirmed bugs from hypotheses, group related findings, and recommend fixes and regression tests by impact. State what remains unassessed.

For complex or concurrent areas, use TLA+ and TLC to check the relevant lifecycle and interactions, including retries and failures. Check safety and liveness, stating assumptions, scope, and checking bounds. Connect model counterexamples to implementation evidence before calling them code bugs. Reuse and update prior assessment models.

Prefer the simplest fix. Understanding an implicit state machine does not require replacing it.

Assessment only: run existing tests and isolated scratch reproductions. Keep reports, models, and debugging artifacts outside the application checkout. Do not modify application files, create or update issues, or publish PRs; implementation and issue creation require separate approval.

Run `checking-simplicity` on each draft recommendation, then run `ce-pov` on the revised recommendations and incorporate its judgment into the final prioritized recommendations for approval. Preserve evidence, tradeoffs, and uncertainty. Report blocked reviews and cases where no change is justified.

History: clone or update <your private automation-state repository> at `~/.local/state/automation-runs`. Read `state-machine-audit-<repository name>` runs and owner decisions before assessing, and save the final report afterward. Follow the README's storage instructions, using its helper when available or its documented Git steps otherwise. Revisit declined findings only with new evidence.
```
