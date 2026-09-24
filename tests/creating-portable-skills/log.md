# Run log: creating-portable-skills

Format: `date | git rev | check | result | note`

- 2026-09-24 | d8a87bb | archive pointer | recorded | Full earlier log at this revision preserves superseded runs, failures, grading disagreements and corrections, receipt failures/retry, per-run costs, and experiment accounting; no historical verdict is replaced by this condensation. Also preserved on PR #168: [part 1](https://github.com/jrgilbertson/the-rookery/pull/168#issuecomment-5817502125), [part 2](https://github.com/jrgilbertson/the-rookery/pull/168#issuecomment-5817504398).
- 2026-09-24 | 6113369 working tree | scanner pressure-boundary regression | fail → pass | Production fixtures: 40 passed/2 failed before correction; 42 passed/0 failed after. Attached markers and line counts corrected; textual boundary controls retained. No model or native activation rerun.
- 2026-09-24 | b46e4de working tree | scanner operational-error regression | fail → pass | Production fixtures: 33 passed/2 failed before correction; 35 passed/0 failed after. Real unreadable input exits 2 with empty stdout.
- 2026-09-24 | b46e4de working tree | scanner structural validation | pass | Cached official skills-ref; no native activation claim.
- 2026-09-24 | b46e4de working tree | independent scanner source/package review | pass | Separate subagent reviewers; source reviewer reran 35 assertions, shell syntax and dash no-match control; package qualification and three simplification reviews found no changes needed.
- 2026-09-24 | b46e4de working tree | repository pre-push gates | pass | Catalog, integrity, secrets and fixtures; 292 s. Local check costs and other durations not recorded.
- 2026-09-24 | c6b6051 working tree | selected source scope | recorded | Initial adoptions add focused validation, evaluation containment and outcome-based conventions. Cwd guard adds pre-dispatch working-directory/resolved-write-path verification. Vendor scope adds only the checklist clause requiring model/harness scope in vendor recommendations. Labels below name these successive frozen packages; they are not committed revisions or final-head executions.
- 2026-09-24 | c6b6051 working tree | independent matched grading | recorded | Fresh CLI executor contexts: Codex CLI 0.156.1/Sol high and Grok CLI 1.0.41/Grok high. Separate blinded CLI grading: Claude Code 2.1.281/Opus 5.5 medium for all Sol packets; Sol high for all Grok packets, including containment repeats. Neutral full packets include observed artifacts/public tool records; Grok exports show invocations, not command success.
- 2026-09-24 | c6b6051 working tree | selected comparison | pass | First two runs across six cases: Sol prior 5/12 → revised 12/12; Grok prior 7/12 → revised 12/12. Grok containment including r3/r4: prior 2/4 → revised 4/4. All 52 selected results follow, with scoped reuse of initial-adoptions and cwd-guard outputs; only four revised vendor-scope executions are new.
- 2026-09-24 | c6b6051 working tree: vendor scope | revised Sol vendor r1 source admission | receipt failed; execution admitted | Wrapper exit 1 retained: quotation was not an exact entrypoint quote. Independent reviewer accepted completed native reads matching frozen SKILL.md/checklist bytes plus digest output. Opus graded the unchanged full packet; no retry or receipt-pass claim.
- 2026-09-24 | c6b6051 working tree | selected evidence limitations | recorded | Clarified control prompts reran both variants with unchanged checklists. Corrected snapshot labels and absolute-path anonymization prompted whole-packet regrades, not executor reruns. Identical existing comparison definitions accompanied both latest vendor packets. Earlier judgments/failures remain in the archive; no per-answer favorable grade selection.
- 2026-09-24 | c6b6051 working tree | experiment accounting | recorded | 83 distinct executor calls, including one earlier install receipt retry; 14 baseline copies deduplicated. Reported historical spend $7.45868012 includes executions and grading, with $0.26515784 for the latest four executions/two graders; Codex dollars unavailable, so these are not total billing. Per-run rows report execution cost only; Sol tokens include cached input. Dates are UTC.
- 2026-09-24 | c6b6051 working tree: vendor scope | independent final checklist/ship-rule review | pass | Separate subagent, neither author nor grader, inspected source, artifacts, selected grades, provenance and costs; scoped gains judged worth measured cost. Sol tokens +43.5% and Grok execution dollars +7.7% do not establish savings. Earlier source scopes remain binding.
- 2026-09-24 | c6b6051 working tree: vendor scope | structural/repository validation | pass | Official cached skills-ref 0.1.1, four pre-push gates, post-log/learning lint, diff/privacy checks; description and install layout unchanged.
- 2026-09-24 | c6b6051 working tree | native smoke applicability | not run | Explicit package loading in matched runs does not establish discovery/activation. No new trigger or install smoke result; accepted Claude omission below remains applicable.
- 2026-09-23 | b3917a2 | smoke: Codex CLI 0.155.1, Sol high | pass | Local-source copy install via skills CLI 1.7.0 into disposable project matched every file and executable bit; native trace read the installed .agents skill entrypoint on the trigger query. Cost not available; tokens/duration not recorded here. Historical source only.
- 2026-09-23 | b3917a2 | smoke: Claude Code, Opus 5.5 | not run — usage limit; owner accepted | Copy identity/executable bit verified, activation usage-limited. Owner: “Yes, accept the missing current Claude smoke check”. Earlier activation is historical; installation identity is not activation.

- 2026-09-24 | c6b6051 | gpt-6-sol high, authoring-conventions, prior, r1 | fail (items 1, 2, 5) | cost not available; 77217 tokens; 89 s
- 2026-09-24 | c6b6051 | gpt-6-sol high, authoring-conventions, prior, r2 | fail (items 1, 2) | cost not available; 70530 tokens; 64 s
- 2026-09-24 | c6b6051 working tree: initial adoptions | gpt-6-sol high, authoring-conventions, revised, r1 | pass | cost not available; 92229 tokens; 45 s
- 2026-09-24 | c6b6051 working tree: initial adoptions | gpt-6-sol high, authoring-conventions, revised, r2 | pass | cost not available; 70805 tokens; 35 s
- 2026-09-24 | c6b6051 | gpt-6-sol high, evaluation-containment, prior, r1 | fail (items 5) | cost not available; 162674 tokens; 103 s
- 2026-09-24 | c6b6051 | gpt-6-sol high, evaluation-containment, prior, r2 | fail (items 5) | cost not available; 110885 tokens; 57 s
- 2026-09-24 | c6b6051 working tree: cwd guard | gpt-6-sol high, evaluation-containment, revised, r1 | pass | cost not available; 297473 tokens; 159 s
- 2026-09-24 | c6b6051 working tree: cwd guard | gpt-6-sol high, evaluation-containment, revised, r2 | pass | cost not available; 231604 tokens; 145 s
- 2026-09-24 | c6b6051 | gpt-6-sol high, independent-fresh-context-review, prior, r1 | pass | cost not available; 70965 tokens; 55 s
- 2026-09-24 | c6b6051 | gpt-6-sol high, independent-fresh-context-review, prior, r2 | pass | cost not available; 70157 tokens; 35 s
- 2026-09-24 | c6b6051 working tree: initial adoptions | gpt-6-sol high, independent-fresh-context-review, revised, r1 | pass | cost not available; 71161 tokens; 32 s
- 2026-09-24 | c6b6051 working tree: initial adoptions | gpt-6-sol high, independent-fresh-context-review, revised, r2 | pass | cost not available; 93845 tokens; 56 s
- 2026-09-24 | c6b6051 | gpt-6-sol high, install-and-grading-gates, prior, r1 (clarified prompt) | pass | cost not available; 90929 tokens; 49 s
- 2026-09-24 | c6b6051 | gpt-6-sol high, install-and-grading-gates, prior, r2 (clarified prompt) | pass | cost not available; 71692 tokens; 46 s
- 2026-09-24 | c6b6051 working tree: cwd guard | gpt-6-sol high, install-and-grading-gates, revised, r1 (clarified prompt) | pass | cost not available; 121571 tokens; 62 s
- 2026-09-24 | c6b6051 working tree: cwd guard | gpt-6-sol high, install-and-grading-gates, revised, r2-receipt-retry (clarified prompt) | pass | cost not available; 72699 tokens; 50 s
- 2026-09-24 | c6b6051 | gpt-6-sol high, proportionate-validation, prior, r1 | fail (items 1, 2, 3, 4) | cost not available; 291911 tokens; 214 s
- 2026-09-24 | c6b6051 | gpt-6-sol high, proportionate-validation, prior, r2 | fail (items 1, 2, 3) | cost not available; 417911 tokens; 198 s
- 2026-09-24 | c6b6051 working tree: cwd guard | gpt-6-sol high, proportionate-validation, revised, r1 | pass | cost not available; 557320 tokens; 188 s
- 2026-09-24 | c6b6051 working tree: cwd guard | gpt-6-sol high, proportionate-validation, revised, r2 | pass | cost not available; 469036 tokens; 164 s
- 2026-09-24 | c6b6051 | gpt-6-sol high, vendor-specific-advice-stays-out, prior, r1 (clarified prompt) | pass | cost not available; 91133 tokens; 54 s
- 2026-09-24 | c6b6051 | gpt-6-sol high, vendor-specific-advice-stays-out, prior, r2 (clarified prompt) | fail (items 1) | cost not available; 109371 tokens; 84 s
- 2026-09-24 | c6b6051 working tree: vendor scope | gpt-6-sol high, vendor-specific-advice-stays-out, revised, r1 (clarified prompt) | pass | cost not available; 135341 tokens; 80 s
- 2026-09-24 | c6b6051 working tree: vendor scope | gpt-6-sol high, vendor-specific-advice-stays-out, revised, r2 (clarified prompt) | pass | cost not available; 133545 tokens; 64 s
- 2026-09-24 | c6b6051 | grok-4.7 high, authoring-conventions, prior, r1 | fail (items 1, 2) | $0.06853584; 103326 tokens; 256 s
- 2026-09-24 | c6b6051 | grok-4.7 high, authoring-conventions, prior, r2 | fail (items 1, 2) | $0.1182112; 135036 tokens; 344 s
- 2026-09-24 | c6b6051 working tree: initial adoptions | grok-4.7 high, authoring-conventions, revised, r1 | pass | $0.088672; 112392 tokens; 288 s
- 2026-09-24 | c6b6051 working tree: initial adoptions | grok-4.7 high, authoring-conventions, revised, r2 | pass | $0.06499916; 92459 tokens; 164 s
- 2026-09-24 | c6b6051 | grok-4.7 high, evaluation-containment, prior, r1 | fail (items 2, 4) | $0.1887918; 460295 tokens; 311 s
- 2026-09-24 | c6b6051 | grok-4.7 high, evaluation-containment, prior, r2 | pass | $0.21351592; 433522 tokens; 392 s
- 2026-09-24 | c6b6051 | grok-4.7 high, evaluation-containment, prior, r3 | pass | $0.18410524; 335097 tokens; 385 s
- 2026-09-24 | c6b6051 | grok-4.7 high, evaluation-containment, prior, r4 | fail (items 2) | $0.19240804; 338571 tokens; 341 s
- 2026-09-24 | c6b6051 working tree: cwd guard | grok-4.7 high, evaluation-containment, revised, r1 | pass | $0.16763768; 335546 tokens; 336 s
- 2026-09-24 | c6b6051 working tree: cwd guard | grok-4.7 high, evaluation-containment, revised, r2 | pass | $0.22878804; 393777 tokens; 265 s
- 2026-09-24 | c6b6051 working tree: cwd guard | grok-4.7 high, evaluation-containment, revised, r3 | pass | $0.1946466; 370237 tokens; 415 s
- 2026-09-24 | c6b6051 working tree: cwd guard | grok-4.7 high, evaluation-containment, revised, r4 | pass | $0.22471008; 440656 tokens; 404 s
- 2026-09-24 | c6b6051 | grok-4.7 high, independent-fresh-context-review, prior, r1 | pass | $0.05329704; 85562 tokens; 157 s
- 2026-09-24 | c6b6051 | grok-4.7 high, independent-fresh-context-review, prior, r2 | pass | $0.09191152; 136516 tokens; 172 s
- 2026-09-24 | c6b6051 working tree: initial adoptions | grok-4.7 high, independent-fresh-context-review, revised, r1 | pass | $0.07475036; 110901 tokens; 153 s
- 2026-09-24 | c6b6051 working tree: initial adoptions | grok-4.7 high, independent-fresh-context-review, revised, r2 | pass | $0.04796584; 89892 tokens; 145 s
- 2026-09-24 | c6b6051 | grok-4.7 high, install-and-grading-gates, prior, r1 (clarified prompt) | pass | $0.04095708; 77757 tokens; 114 s
- 2026-09-24 | c6b6051 | grok-4.7 high, install-and-grading-gates, prior, r2 (clarified prompt) | pass | $0.07409756; 120379 tokens; 181 s
- 2026-09-24 | c6b6051 working tree: cwd guard | grok-4.7 high, install-and-grading-gates, revised, r1 (clarified prompt) | pass | $0.04874376; 64818 tokens; 133 s
- 2026-09-24 | c6b6051 working tree: cwd guard | grok-4.7 high, install-and-grading-gates, revised, r2 (clarified prompt) | pass | $0.05299648; 82478 tokens; 166 s
- 2026-09-24 | c6b6051 | grok-4.7 high, proportionate-validation, prior, r1 | fail (items 1, 3) | $0.115583; 210743 tokens; 451 s
- 2026-09-24 | c6b6051 | grok-4.7 high, proportionate-validation, prior, r2 | fail (items 1, 3) | $0.21667044; 365133 tokens; 599 s
- 2026-09-24 | c6b6051 working tree: cwd guard | grok-4.7 high, proportionate-validation, revised, r1 | pass | $0.27688444; 551433 tokens; 471 s
- 2026-09-24 | c6b6051 working tree: cwd guard | grok-4.7 high, proportionate-validation, revised, r2 | pass | $0.22057432; 326848 tokens; 475 s
- 2026-09-24 | c6b6051 | grok-4.7 high, vendor-specific-advice-stays-out, prior, r1 (clarified prompt) | pass | $0.06524532; 97315 tokens; 187 s
- 2026-09-24 | c6b6051 | grok-4.7 high, vendor-specific-advice-stays-out, prior, r2 (clarified prompt) | pass | $0.07193856; 116132 tokens; 217 s
- 2026-09-24 | c6b6051 working tree: vendor scope | grok-4.7 high, vendor-specific-advice-stays-out, revised, r1 (clarified prompt) | pass | $0.05814068; 93071 tokens; 164 s
- 2026-09-24 | c6b6051 working tree: vendor scope | grok-4.7 high, vendor-specific-advice-stays-out, revised, r2 (clarified prompt) | pass | $0.09046516; 128737 tokens; 215 s

- 2026-09-23 | b83df51, 9d39948, b3917a2 | refresh selected comparison: Opus 5.5 medium | pass | Prior 7/12 → revised 12/12 across six retained cases; every revised control passes. Rows retain scoped reused source revisions; no whole-suite final-head execution claim.
- 2026-09-23 | 15abed3, b3917a2 | refresh selected comparison: Sol high | pass | Prior 6/12 → revised 12/12 across six retained cases; every revised control passes. Revised source unchanged since b3917a2; historical refresh evidence precedes later adoptions.
- 2026-09-23 | b3917a2 | refresh independent grading/review | pass | Fresh CLI executions: Claude Code 2.1.281/Opus medium and Codex CLI 0.155.1/Sol high; separate blinded Sol graders for Opus, Grok CLI 1.0.41/Grok high for Sol. Complete control adjudication and vendor checklist correction preserved in archive; separate final-review subagent inspected all twelve packets and 48 measured rows. Opus tokens include cache creation/read; Sol input includes cache. Reported costs are not subscription billing.

- 2026-09-23 | 15abed3 | Opus 5.5: cost-and-check-pruning, prior r1 | fail (4/6); items 3, 5 | $0.1330 reported cost; 44,453 total tokens, 34 s
- 2026-09-23 | b3917a2 | Opus 5.5: cost-and-check-pruning, revised r2 | pass (6/6) | $0.1317 reported cost; 42,856 total tokens, 47 s
- 2026-09-23 | b3917a2 | Opus 5.5: cost-and-check-pruning, revised r1 | pass (6/6) | $0.1280 reported cost; 30,708 total tokens, 38 s
- 2026-09-23 | 15abed3 | Opus 5.5: cost-and-check-pruning, prior r2 | pass (6/6) | $0.1753 reported cost; 61,649 total tokens, 44 s
- 2026-09-23 | 15abed3 | Opus 5.5: independent-fresh-context-review, prior r1 | pass (3/3) | $0.1011 reported cost; 30,382 total tokens, 18 s
- 2026-09-23 | 9d39948 | Opus 5.5: independent-fresh-context-review, revised r1 | pass (3/3) | $0.0888 reported cost; 28,942 total tokens, 23 s
- 2026-09-23 | 15abed3 | Opus 5.5: independent-fresh-context-review, prior r2 | pass (3/3) | $0.0864 reported cost; 29,503 total tokens, 18 s
- 2026-09-23 | 9d39948 | Opus 5.5: independent-fresh-context-review, revised r2 | pass (3/3) | $0.1170 reported cost; 32,258 total tokens, 20 s
- 2026-09-23 | b83df51 | Opus 5.5: install-and-grading-gates, revised r1 | pass (4/4) | $0.0920 reported cost; 29,439 total tokens, 32 s
- 2026-09-23 | b83df51 | Opus 5.5: install-and-grading-gates, revised r2 | pass (4/4) | $0.0947 reported cost; 29,961 total tokens, 23 s
- 2026-09-23 | 15abed3 | Opus 5.5: install-and-grading-gates, prior r2 | fail (0/4); items 1, 2, 3, 4 | $0.1173 reported cost; 45,510 total tokens, 36 s
- 2026-09-23 | 15abed3 | Opus 5.5: install-and-grading-gates, prior r1 | fail (0/4); items 1, 2, 3, 4 | $0.1246 reported cost; 58,523 total tokens, 41 s
- 2026-09-23 | 15abed3 | Opus 5.5: passing-baseline-regression-control, prior r1 | pass (4/4) | $0.0924 reported cost; 29,807 total tokens, 21 s
- 2026-09-23 | 9d39948 | Opus 5.5: passing-baseline-regression-control, revised r2 | pass (4/4) | $0.0889 reported cost; 28,620 total tokens, 21 s
- 2026-09-23 | 15abed3 | Opus 5.5: passing-baseline-regression-control, prior r2 | pass (4/4) | $0.0881 reported cost; 41,153 total tokens, 18 s
- 2026-09-23 | 9d39948 | Opus 5.5: passing-baseline-regression-control, revised r1 | pass (4/4) | $0.0870 reported cost; 28,526 total tokens, 21 s
- 2026-09-23 | 15abed3 | Opus 5.5: planted-rot-review, prior r2 | fail (3/5); items 3, 4 | $0.1540 reported cost; 35,013 total tokens, 39 s
- 2026-09-23 | b83df51 | Opus 5.5: planted-rot-review, revised r1 | pass (5/5) | $0.2370 reported cost; 96,663 total tokens, 50 s
- 2026-09-23 | b83df51 | Opus 5.5: planted-rot-review, revised r2 | pass (5/5) | $0.1908 reported cost; 53,795 total tokens, 49 s
- 2026-09-23 | 15abed3 | Opus 5.5: planted-rot-review, prior r1 | fail (4/5); items 3 | $0.2009 reported cost; 52,257 total tokens, 50 s
- 2026-09-23 | 15abed3 | Opus 5.5: vendor-specific-advice-stays-out, prior r2 | pass (6/6) | $0.1572 reported cost; 51,751 total tokens, 33 s
- 2026-09-23 | 9d39948 | Opus 5.5: vendor-specific-advice-stays-out, revised r1 | pass (6/6) | $0.1569 reported cost; 49,087 total tokens, 42 s
- 2026-09-23 | 9d39948 | Opus 5.5: vendor-specific-advice-stays-out, revised r2 | pass (6/6) | $0.1516 reported cost; 48,019 total tokens, 46 s
- 2026-09-23 | 15abed3 | Opus 5.5: vendor-specific-advice-stays-out, prior r1 | pass (6/6) | $0.1460 reported cost; 51,101 total tokens, 29 s
- 2026-09-23 | 15abed3 | Sol high: cost-and-check-pruning, prior r2 | pass (6/6) | cost not available; 113,054 total tokens, 97 s
- 2026-09-23 | b3917a2 | Sol high: cost-and-check-pruning, revised r1 | pass (6/6) | cost not available; 84,126 total tokens, 65 s
- 2026-09-23 | b3917a2 | Sol high: cost-and-check-pruning, revised r2 | pass (6/6) | cost not available; 126,626 total tokens, 77 s
- 2026-09-23 | 15abed3 | Sol high: cost-and-check-pruning, prior r1 | fail (5/6); items 3 | cost not available; 123,316 total tokens, 96 s
- 2026-09-23 | 15abed3 | Sol high: independent-fresh-context-review, prior r1 | pass (3/3) | cost not available; 68,779 total tokens, 37 s
- 2026-09-23 | b3917a2 | Sol high: independent-fresh-context-review, revised r2 | pass (3/3) | cost not available; 102,023 total tokens, 38 s
- 2026-09-23 | 15abed3 | Sol high: independent-fresh-context-review, prior r2 | pass (3/3) | cost not available; 88,477 total tokens, 42 s
- 2026-09-23 | b3917a2 | Sol high: independent-fresh-context-review, revised r1 | pass (3/3) | cost not available; 68,514 total tokens, 42 s
- 2026-09-23 | 15abed3 | Sol high: install-and-grading-gates, prior r2 | fail (1/4); items 1, 3, 4 | cost not available; 52,658 total tokens, 26 s
- 2026-09-23 | b3917a2 | Sol high: install-and-grading-gates, revised r1 | pass (4/4) | cost not available; 47,963 total tokens, 29 s
- 2026-09-23 | b3917a2 | Sol high: install-and-grading-gates, revised r2 | pass (4/4) | cost not available; 67,450 total tokens, 34 s
- 2026-09-23 | 15abed3 | Sol high: install-and-grading-gates, prior r1 | fail (1/4); items 1, 3, 4 | cost not available; 82,108 total tokens, 28 s
- 2026-09-23 | 15abed3 | Sol high: passing-baseline-regression-control, prior r2 | pass (4/4) | cost not available; 73,209 total tokens, 37 s
- 2026-09-23 | 15abed3 | Sol high: passing-baseline-regression-control, prior r1 | pass (4/4) | cost not available; 73,004 total tokens, 29 s
- 2026-09-23 | b3917a2 | Sol high: passing-baseline-regression-control, revised r1 | pass (4/4) | cost not available; 45,857 total tokens, 19 s
- 2026-09-23 | b3917a2 | Sol high: passing-baseline-regression-control, revised r2 | pass (4/4) | cost not available; 64,522 total tokens, 32 s
- 2026-09-23 | 15abed3 | Sol high: planted-rot-review, prior r1 | fail (3/5); items 1, 4 | cost not available; 126,556 total tokens, 103 s
- 2026-09-23 | 15abed3 | Sol high: planted-rot-review, prior r2 | fail (1/5); items 1, 2, 4, 5 | cost not available; 146,306 total tokens, 101 s
- 2026-09-23 | b3917a2 | Sol high: planted-rot-review, revised r1 | pass (5/5) | cost not available; 91,092 total tokens, 56 s
- 2026-09-23 | b3917a2 | Sol high: planted-rot-review, revised r2 | pass (5/5) | cost not available; 92,387 total tokens, 74 s
- 2026-09-23 | b3917a2 | Sol high: vendor-specific-advice-stays-out, revised r2 | pass (6/6) | cost not available; 192,363 total tokens, 63 s
- 2026-09-23 | 15abed3 | Sol high: vendor-specific-advice-stays-out, prior r2 | fail (5/6); items 3 | cost not available; 194,710 total tokens, 82 s
- 2026-09-23 | b3917a2 | Sol high: vendor-specific-advice-stays-out, revised r1 | pass (6/6) | cost not available; 103,879 total tokens, 77 s
- 2026-09-23 | 15abed3 | Sol high: vendor-specific-advice-stays-out, prior r1 | pass (6/6) | cost not available; 156,797 total tokens, 118 s

- 2026-09-08 | b075928 (working tree) | structural validation | pass | official `skills-ref` was unavailable; manual Agent Skills field, length, name, and package checks passed with the repository validator, catalog, and relative-link checks
- 2026-09-08 | b075928 (working tree) | trigger sample after SKILL.md/eval routing | pass (3/3) | three isolated fresh-context judges saw only the name, candidate description, and one query; eval update and SKILL.md/grader edit activated; standalone grader/rubric near miss stayed inactive. Complete trigger suite not rerun in this session.

- 2026-08-26 | db15238 | matched comparison: passing-baseline-regression-control (prior) | fail (2/5) | isolated runner allowed the control and limited its claim, but omitted the separate-discrimination requirement, matched-control regression blocking, and bounded-use guidance; separate blind grader
- 2026-08-26 | db15238 (working tree) | matched comparison: passing-baseline-regression-control (candidate) | pass (5/5) | fresh runner applied the candidate protocol; a separate blind grader confirmed explicit control labeling, separate discrimination, matched regression blocking, bounded use, and honest claims
- 2026-08-26 | db15238 (working tree) | structural validation | pass | official `skills-ref` was unavailable; manual Agent Skills field, length, name, and package checks passed with the repository validator, catalog, and relative-link checks

- 2026-08-17 | b8fbafb + terminology diff | trigger suite: generic skill terminology | pass (10/10 should-trigger; 11/11 near misses) | Twenty-one isolated ephemeral Codex CLI 0.147.0 contexts each saw only the current name, description, and one query; every first judgment was categorical, including `no` for the added role-playing-game near miss.

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
