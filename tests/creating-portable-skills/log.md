# Run log: creating-portable-skills

Format: `date | git rev | check | result | note`

- 2026-07-30 | 9b76104 | case: fixture-review-prioritized-findings | pass (5/5) | Fresh-context run against the retuned repo package (U5); read SKILL.md + review-checklist.md.
- 2026-07-30 | 9b76104 | case: independent-fresh-context-review | pass (4/4) | Fresh-context run against the retuned repo package (U5).
- 2026-07-30 | 9b76104 | case: baseline-before-shipping | pass (5/5) | Fresh-context run against the retuned repo package (U5); the comparison item was clarified after the run, but the graded answer had already taken the description-only carve-out the clarified item names, so the result stands for the checked-in text.
- 2026-07-30 | 9b76104 | smoke: Claude Code | pass | Installed from source into a disposable project (project settings only); transcript shows the Skill tool loading creating-portable-skills on a should-trigger query.
- 2026-07-30 | 9b76104 | smoke: Codex CLI 0.145.0 | pass | Installed from source into a disposable project; trace read the exact installed .agents path and activated on a should-trigger query.
- 2026-07-30 | 176b818 | archive pointer | — | Full prior evidence (listing
  runs, matched comparisons, native checks, package hashes) is in git
  history at this commit, before the restructure removed trigger-queries.md,
  baseline-cases.md, and results.md.
