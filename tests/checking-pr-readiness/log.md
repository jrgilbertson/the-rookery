# Run log: checking-pr-readiness

Format: `date | git rev | check | result | note`

- 2026-07-31 | 87efcac (working tree) | trigger suite | fail (16/20) | fresh-context subagent judges, one context per direction with per-query independence; three should-triggers weak (ready-for-CI, final-approval, gate phrasings), one near-miss fired (open a PR)
- 2026-07-31 | 87efcac (working tree) | trigger suite (re-judge after description revision) | pass (6/6) | fresh-context subagent, blind to expected direction; revised description names the weak phrasings and excludes PR-opening; merge and PR-description controls held
- 2026-07-31 | 87efcac (working tree) | matched comparison: readiness-honesty-battery | pass — bare fail (1/4) prior vs skilled pass (4/4) | fresh-context subagents per side against constructed fixture state; blind independent grader; scenarios 1-3 discriminate, scenario 4 is a control passing both sides
- 2026-07-31 | 87efcac (working tree) | smoke: install probe (pre-merge, local source) | pass | skills CLI 1.5.21, disposable project, --copy; all six files arrived, scripts kept executable bits; activation coverage via trigger suite, per-harness in-session smoke deferred to post-merge
