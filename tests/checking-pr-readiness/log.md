# Run log: checking-pr-readiness

Format: `date | git rev | check | result | note`

- 2026-07-31 | 87efcac (working tree) | trigger suite | fail (16/20) | fresh-context subagent judges, one context per direction with per-query independence; three should-triggers weak (ready-for-CI, final-approval, gate phrasings), one near-miss fired (open a PR)
- 2026-07-31 | 87efcac (working tree) | trigger suite (re-judge after description revision) | pass (6/6) | fresh-context subagent, blind to expected direction; revised description names the weak phrasings and excludes PR-opening; merge and PR-description controls held
- 2026-07-31 | 87efcac (working tree) | matched comparison: readiness-honesty-battery | pass — bare fail (1/4) prior vs skilled pass (4/4) | fresh-context subagents per side against constructed fixture state; blind independent grader; scenarios 1-3 discriminate, scenario 4 is a control passing both sides. Competing installed copies of the predecessor skill were not moved out of discovery scope; the bare side was instructed skill-blind and its transcript shows no gate-skill influence (it failed the discriminating scenarios), so contamination would have biased against, not toward, this result
- 2026-07-31 | 87efcac (working tree) | install probe (pre-merge, local source) | pass | skills CLI 1.5.21, disposable project, --copy; all six files arrived, scripts kept executable bits. File mechanics only — this line claims nothing about activation
- 2026-07-31 | — | smoke: Claude Code | not run — deferred to post-merge | per-harness in-session activation with identity proof still owed; a trigger-suite pass is a listing proxy, not activation proof
- 2026-07-31 | — | smoke: Codex CLI | not run — harness not exercised pre-merge | same identity-proof requirement applies
- 2026-07-31 | 0be78bc | helper fixture runs | pass (34/34) | committed runner fixtures/run-helper-checks.sh asserts every documented verdict line and exit code across all three helpers; first green run after the review fixes closed the silent-pass holes
- 2026-08-01 | e8f1108 (working tree) | helper fixture runs + verdict drift guard | pass (50/50) | runner now also asserts every verdict the scripts can emit appears in references/sweep-classes.md, so the reference cannot silently drift from the helpers
- 2026-08-01 | dc6b5ee (working tree) | helper fixture runs (post PR-review fix) | pass (52/52) | changelog-union.sh and evidence-freshness.sh now fail closed on failed git reads (read_or_fail, exit 4), closing the silent-pass paths PR review found; corrupted-index fixtures added for both
