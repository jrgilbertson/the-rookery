# Run log: creating-portable-skills

Format: `date | git rev | check | result | note`

Method for the 2026-09-19 lines: forced-load runs in disposable projects, one per variant, with the skill read from an explicit path and harness skill discovery disabled, so no same-name user-level copy could load. Claude Code 2.1.278 ran Opus 5 and Fable 5.1 at medium effort; Codex CLI 0.154.0 ran Sol at medium effort. Blind Opus subagent grader against the case checklists at c951057, variant and run folder hidden. Codex reports no duration, so its notes carry wall-clock seconds and input/cached/output tokens.

- 2026-09-19 | c2b4c81 | structural validation | pass | `agentskills validate` from the official `skills-ref` package through uvx: valid skill, scripts directory included
- 2026-09-19 | c2b4c81 | fixture runner: signal scan | pass (37/37) | deterministic runner in the pre-push roster; includes the assertion that the scan writes no file
- 2026-09-19 | c2b4c81 | signal scan over skills/ | recorded | zero hits for pressure language, thinking scaffolds, format and narration suppressors, and every other vendor signal; 10 migration-relative hits are ordinary domain prose, 3 history identifiers are issue references and a review date, 7 pinned model names are the dated routing table
- 2026-09-19 | 15abed3 (prior) | matched comparison: planted-rot-review, Claude Code Opus 5 | fail (3/6) | 65k tokens, 86 s; no signal counts, listed the ordinary-prose sentence as a defect
- 2026-09-19 | c2b4c81 | matched comparison: planted-rot-review, Claude Code Opus 5 | pass (6/6) | 81k tokens, 76 s
- 2026-09-19 | 15abed3 (prior) | matched comparison: planted-rot-review, Claude Code Fable 5.1 | fail (4/6) | 89k tokens, 110 s
- 2026-09-19 | c2b4c81 | matched comparison: planted-rot-review, Claude Code Fable 5.1 | pass (6/6) | 56k tokens, 47 s
- 2026-09-19 | 15abed3 (prior) | matched comparison: planted-rot-review, Codex Sol | fail (3/6) | 202 s; 255k/221k/3.7k tokens
- 2026-09-19 | c2b4c81 | matched comparison: planted-rot-review, Codex Sol | fail (5/6) | 195 s; 330k/298k/5.7k tokens; reported counts, history, the named-model workaround, and the unverified version, but faulted the row-count completion check, so the case shows no pass on this target
- 2026-09-19 | 15abed3 (prior) | matched comparison: cost-and-check-pruning, Claude Code Opus 5 | pass (6/6) | 110k tokens, 63 s; same as revised, so this target does not discriminate
- 2026-09-19 | c2b4c81 | matched comparison: cost-and-check-pruning, Claude Code Opus 5 | pass (6/6) | 51k tokens, 52 s
- 2026-09-19 | 15abed3 (prior) | matched comparison: cost-and-check-pruning, Claude Code Fable 5.1 | fail (5/6) | 47k tokens, 35 s; routed the taste comment to a new checklist item
- 2026-09-19 | c2b4c81 | matched comparison: cost-and-check-pruning, Claude Code Fable 5.1 | pass (6/6) | 118k tokens, 53 s
- 2026-09-19 | 15abed3 (prior) | matched comparison: cost-and-check-pruning, Codex Sol | fail (4/6) | 69 s; 105k/75k/2.1k tokens
- 2026-09-19 | c2b4c81 | matched comparison: cost-and-check-pruning, Codex Sol | pass (6/6) | 136 s; 128k/99k/3.1k tokens
- 2026-09-19 | c2b4c81 | control: vendor-specific-advice-stays-out | pass (5/5) on Opus 5 and Sol | prior package also passes 5/5 on both, so the case is a labeled control; Opus 5 60k to 84k tokens, Sol 108 to 110 s
- 2026-09-19 | c2b4c81 | control: fixture-review-prioritized-findings | pass (5/5) on Opus 5, pass (5/5) twice on Sol | prior package passes 5/5 twice on Sol; Opus 5 82k tokens, 70 s
- 2026-09-19 | c2b4c81 | control: lightweight-artifacts-and-no-ceremony | pass (4/4) twice on Opus 5, pass (4/4) on Sol | prior package passes on both; Opus 5 57k to 61k tokens
- 2026-09-19 | c2b4c81 | control: independent-fresh-context-review | pass (3/3) on Opus 5 and Sol | Opus 5 60k tokens, 47 s; Sol 38 s
- 2026-09-19 | c2b4c81 | control: passing-baseline-regression-control, Claude Code Opus 5 | pass (5/5) | 51k tokens, 47 s
- 2026-09-19 | c2b4c81 | control: passing-baseline-regression-control, Codex Sol | fail (3/5) | 27 s; one run; the prior package passed once (5/5) and failed once (4/5) on the same target, so a regression is not established; variance reruns not run, Codex usage limit
- 2026-09-19 | c2b4c81 | control: baseline-before-shipping, Claude Code Opus 5 | fail (4/5), pass (5/5), fail (4/5) | three runs; the prior package failed both of its runs (4/5) on the same item, a prior-versus-revised activation comparison for a description-only change, so the weakness predates this revision
- 2026-09-19 | c2b4c81 | control: baseline-before-shipping, Codex Sol | fail (2/5) | 203 s; the prior package also fails 2/5
- 2026-09-19 | c2b4c81 | variance reruns on Codex Sol | not run — harness usage limit | six runs never started or were cut off; none is counted
- 2026-09-19 | c2b4c81 | smoke: Claude Code, Codex CLI | not run | no packaging probe yet for the new scripts directory
- 2026-09-19 | c2b4c81 | final checklist review | not run | pending the remaining Codex runs
- 2026-09-19 | 31790a6 | case correction: planted-rot fixture | recorded | the fixture skipped deleted-customer rows and also required the full row count; three of four first-round runs reported that real contradiction and two items failed them for it; fixture fixed, checklist untouched, first-round planted-rot runs discarded
- 2026-09-19 | c951057 | case correction: seven checklists | recorded | a reviewer who saw no outputs or grades rewrote items that graded phrasing, a fixed output order, or the skill's vocabulary, merged duplicates, and removed items any agent passes; all earlier grades against the old items are superseded by the lines above
- 2026-09-19 | c2b4c81 | grading correction: blinding | recorded | first-round packets leaked the variant through run-folder names quoted in outputs; planted-rot was regraded from scrubbed packets and those grades are the ones logged

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
