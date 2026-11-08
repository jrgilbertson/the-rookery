# Coding standards audit

Review coding standards against repository evidence and current primary sources.

- **Cadence:** Saturday at 07:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** This repository's [`checking-simplicity`](../skills/checking-simplicity/SKILL.md) skill, access to the target repository, its PR and review history, and current primary sources. Each run also needs a clone of your private automation-state repository; see [Shared run state](README.md#shared-run-state).

If `CODING_STANDARDS.md` is missing, the prompt asks the agent to propose a first edition.

## Prompt

```text
Review root CODING_STANDARDS.md and recommend additions, revisions, consolidation, or removal. If missing, propose a repository-specific first edition.

Ground recommendations in the architecture, installed versions, tooling, accepted decisions, recent PRs and reviews, and current primary sources for the technologies actually used. Existing code informs the review without limiting better approaches; resolve conflicting guidance for this repository.

Prioritize correctness, security, maintainability, and behavior over style. Preserve implementation freedom. Distinguish mandatory rules from defaults and exceptions. Prefer enforcement through existing types, schemas, tests, or tooling; distinguish actual checks from human review. Scope broader migrations separately. Apply new standards to new and materially changed code by default.

For each recommendation, give the exact edit, evidence and benefit, dated source links, tradeoffs and exceptions, and current or proposed enforcement. Keep adopted coding guidance separate from research procedures and unadopted proposals.

Assessment only: do not modify repository files, install tools, change configuration, create or update issues, or publish PRs without separate approval.

Run `checking-simplicity` on each draft recommendation, then run `ce-pov` on the revised recommendations and incorporate its judgment into the final prioritized recommendations for approval. Preserve evidence, tradeoffs, and uncertainty. Report blocked reviews and cases where no change is justified.

History: clone or update <your private automation-state repository> at `~/.local/state/automation-runs`. Read `coding-standards-audit` runs and owner decisions before assessing, and save the final report afterward. Follow the README's storage instructions, using its helper when available or its documented Git steps otherwise. Revisit declined findings only with new evidence.
```
