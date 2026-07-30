# Run log: creating-portable-skills

Format: `date | git rev | check | result | note`

Branch-time `git rev` values below are preserved by PR #19 even if the
branch is squash-merged; the archive pointer's mainline commit stays
directly reachable.

- 2026-07-30 | 176b818 (prior) | matched comparison: baseline-before-shipping | pass (5/5) | Prior-side run against the frozen pre-retune package for the U5 revision's matched pair. Control held — the substantive-change discipline exists in both variants; the prior-specific tier question, monolithic record artifacts, and waiver machinery surfaced as the process delta the retune removes.
- 2026-07-30 | 176b818 (prior) | matched comparison: independent-fresh-context-review | pass (4/4) | Prior-side control held; independence outcome identical across variants.
- 2026-07-30 | 176b818 (prior) | matched comparison: fixture-review-prioritized-findings | pass (5/5) | Prior-side control held; read-only audit shape identical. With the three revised-side runs above, the matched comparison shows no regression and locates the intended delta in the retired ceremony and emitted artifact shape.

- 2026-07-30 | 9b76104 | case: fixture-review-prioritized-findings | pass (5/5) | Fresh-context run against the retuned repo package (U5); read SKILL.md + review-checklist.md.
- 2026-07-30 | 9b76104 | case: independent-fresh-context-review | pass (4/4) | Fresh-context run against the retuned repo package (U5).
- 2026-07-30 | f2fe80d | case: baseline-before-shipping | pass (5/5) | Fresh-context rerun against the final checked-in case text (post-clarification) and the retuned repo package; graded including the unforced-activation carve-out item. Supersedes the pre-clarification run at 9b76104.
- 2026-07-30 | aa6f7e4 | case: lightweight-artifacts-and-no-ceremony (revised) | pass (3/3) | Fresh-context run against the retuned repo package; no tier question, thin artifacts only, not-run handling without waivers.
- 2026-07-30 | 176b818 (prior) | matched comparison: lightweight-artifacts-and-no-ceremony | fail (0/3) | Prior-side half against the frozen pre-retune package: it asked the tier question, kept two monolithic evidence records, and routed the unrunnable check through waiver/Claim Ceiling machinery — the discriminating delta the U5 revision intends. With the three controls above, the matched comparison shows the intended improvement with no regression.
- 2026-07-30 | aa6f7e4 | structural validation (skills-ref) | pass | Tier-1 check on the retuned package including all PR-review corrections; rerun on the final package state before merge.
- 2026-07-30 | 93f0a43 | smoke: Claude Code | pass | Rerun with provenance: installed from source into a disposable project (project settings only); the transcript shows the Skill tool activating creating-portable-skills on a should-trigger query and reading the installed copy's own base directory (`.claude/skills/creating-portable-skills` under the disposable project). Supersedes the activation-only run at 9b76104.
- 2026-07-30 | 9b76104 | smoke: Codex CLI 0.145.0 | pass | Installed from source into a disposable project; trace read the exact installed .agents path and activated on a should-trigger query.
- 2026-07-30 | cc66ee8 | archive pointer | — | Full prior evidence (listing
  runs, matched comparisons, native checks, package hashes) is in git
  history at this commit, before the restructure removed trigger-queries.md,
  baseline-cases.md, and results.md.
