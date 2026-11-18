# Coding standards audit

Review coding standards against repository evidence and current primary sources.

- **Cadence:** Saturday at 07:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** `ce-pov`, access to the target repository, its PR and review history, and current primary sources. Each run also needs a clone of your private automation-state repository; see [Shared run state](README.md#shared-run-state).

If `CODING_STANDARDS.md` is missing, the prompt asks the agent to propose a first edition.

## Prompt

```text
Before assessing, confirm the required skills are available to the selected agent. If a required skill is missing or cannot load, report it and stop. Do not install or update skills or plugins.

History: clone or update <your private automation-state repository> at `~/.local/state/automation-runs`. Read `coding-standards-audit-<repository name>` runs and owner decisions before assessing. Follow that history repository's README for storage instructions, using its helper when available or its documented Git steps otherwise. Revisit declined findings only with new evidence.

Review root CODING_STANDARDS.md and recommend additions, revisions, consolidation, or removal. If missing, propose a repository-specific first edition.

Ground recommendations in the architecture, installed versions, tooling, accepted decisions, recent PRs and reviews, and current primary sources for the technologies actually used. Existing code informs the review without limiting better approaches; resolve conflicting guidance for this repository.

Prioritize correctness, security, maintainability, and behavior over style. Preserve implementation freedom. Distinguish mandatory rules from defaults and exceptions. Prefer enforcement through existing types, schemas, tests, or tooling; distinguish actual checks from human review. Scope broader migrations separately. Apply new standards to new and materially changed code by default.

For each recommendation, give the exact edit, evidence and benefit, dated source links, tradeoffs and exceptions, and current or proposed enforcement. Keep adopted coding guidance separate from research procedures and unadopted proposals.

Assessment only: do not modify repository files, install tools, change configuration, create or update issues, or publish PRs without separate approval.

Run `ce-pov` once on the draft recommendations as a whole, including recommendations to leave a confirmed finding unchanged and how the recommendations interact. Have it judge each recommendation as its own decision against current evidence. The approval list holds only the recommendations it supports, in leverage order, highest first, each with its evidence, tradeoffs, and uncertainty. List each recommendation it rejects in one line with its reason, outside the approval list. If `ce-pov` cannot finish, save useful assessment work, name the missing review, and keep the list provisional.

Save the final report afterward.
```
