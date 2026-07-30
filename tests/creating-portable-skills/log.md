# Run log: creating-portable-skills

Format: `date | git rev | check | result | note`

- 2026-07-30 | 9b76104 | case: fixture-review-prioritized-findings | pass (5/5) | Fresh-context run against the retuned repo package (U5); read SKILL.md + review-checklist.md.
- 2026-07-30 | 9b76104 | case: independent-fresh-context-review | pass (4/4) | Fresh-context run against the retuned repo package (U5).
- 2026-07-30 | f2fe80d | case: baseline-before-shipping | pass (5/5) | Fresh-context rerun against the final checked-in case text (post-clarification) and the retuned repo package; graded including the unforced-activation carve-out item. Supersedes the pre-clarification run at 9b76104.
- 2026-07-30 | 93f0a43 | smoke: Claude Code | pass | Rerun with provenance: installed from source into a disposable project (project settings only); the transcript shows the Skill tool activating creating-portable-skills on a should-trigger query and reading the installed copy's own base directory (`.claude/skills/creating-portable-skills` under the disposable project). Supersedes the activation-only run at 9b76104.
- 2026-07-30 | 9b76104 | smoke: Codex CLI 0.145.0 | pass | Installed from source into a disposable project; trace read the exact installed .agents path and activated on a should-trigger query.
- 2026-07-30 | cc66ee8 | archive pointer | — | Full prior evidence (listing
  runs, matched comparisons, native checks, package hashes) is in git
  history at this commit, before the restructure removed trigger-queries.md,
  baseline-cases.md, and results.md.
