# Coding standards audit

Review coding standards against repository evidence and current primary sources.

- **Cadence:** Saturday at 07:00.
- **Timezone:** America/Los_Angeles.
- **Requires:** Access to the target repository, its PR and review history, and current primary sources.

If `CODING_STANDARDS.md` is missing, the prompt asks the agent to propose a first edition.

## Prompt

```text
Review this repository’s root CODING_STANDARDS.md and recommend improvements that keep it current, curated, and useful for humans and AI coding agents.

Ground the review in the repository’s architecture, installed versions, tooling, accepted decisions, and recent PRs and code review feedback. Existing code is evidence, not the ceiling for good practice. Check previous audit results when available and avoid repeating recommendations already addressed.

Research current primary sources for the languages, frameworks, infrastructure, and ML/AI systems actually used here. Consult relevant practitioners without treating any author as authoritative for every decision. Highlight conflicting guidance and explain which approach fits this repository and why.

Recommend additions, revisions, consolidation, or removal. Prioritize correctness, security, maintainability, and useful guardrails over stylistic preferences. Favor rules that protect observable behavior, interface contracts, and task intent while leaving agents freedom over implementation. Distinguish mandatory requirements from defaults with justified exceptions.

For each worthwhile recommendation, provide:

1. The exact proposed wording or edit.
2. The problem or source-backed benefit, with repository evidence where relevant.
3. Primary-source links and the date checked.
4. Material tradeoffs, conflicting guidance, and exceptions.
5. How compliance is enforced today, and any tooling or migration work needed.

Prefer structural prevention through existing types, schemas, tests, or tooling when appropriate. Do not imply that a check exists when compliance currently depends on review. Keep broader migrations separately scoped. New standards should normally apply to new and materially changed code, including substantive refactors.

Keep the standards focused on adopted coding guidance. Research procedures, audit instructions, and unadopted candidates belong outside it.
Return a small, prioritized set of recommendations for approval. If the file is missing, propose a repository-specific first edition. If no changes are justified, say so.

Do not modify repository files, install tools, change configuration, or publish issues or PRs without approval.
```
