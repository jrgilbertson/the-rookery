# Acceptance evidence: creating-skills

Recorded runs for the plan's Verification Contract (`docs/plans/2026-07-16-001-feat-creating-skills-plan.md`). Date: 2026-07-16. Tool versions this run: `skills-ref` 0.1.5, `skills` CLI 1.5.19, Codex CLI 0.144.4, Grok CLI 0.2.101, Claude Code (Fable 5 session; judge runs also on Haiku 4.5 and Sonnet).

## Gate results

| Gate | Result | Evidence |
| --- | --- | --- |
| Static validation | Pass | `npx skills-ref validate skills/creating-skills` → "Valid skill", clean after every edit round |
| Line budget | Pass | `SKILL.md` at 107 lines (ceiling 500, target ~200) |
| Same-door sweep | Pass | Zero hits for home-directory paths and owner-environment identifiers across `skills/creating-skills/` and `tests/creating-skills/` |
| Install probe | Pass (local source) | `npx skills add . --skill creating-skills --agent claude-code --agent codex -g -y --copy` installed to both `~/.claude/skills/` and `~/.agents/skills/`; skill registered live in the running harness. See the branch-ref caveat below |
| Trigger evaluation | Pass | 10/10 should-trigger at rate 1.0 (3 runs each), 0/10 near-miss activations, judged in fresh contexts across three model families (Haiku 4.5, Sonnet, Fable 5). Full tables: `trigger-queries.md` |
| Baseline test | Pass | Bare-agent baseline skipped all four disciplines (self-audited); with-skill runs in three harnesses enforced all four. Comparison: `baseline-cases.md` case 1 |
| Visitor create-flow (F1) | Pass | Clean non-Rookery repo, no companions: all loop steps completed, AE1 and AE2 confirmed (see below) |
| Cross-harness runs | Pass | F1 end-to-end in Codex CLI and Grok CLI from clean installs (see below) |
| Link pass | Pass | 9/9 unique URLs across both references (12 occurrences) return HTTP 200 |

## Run log

- **Claude Code visitor run (F1)** — clean repo, no conventions, no companions. All steps 1-9 completed with criteria met. AE1: recommended `design-evals` with the install command, ran the built-in baseline, named the skipped depth. AE2: convention scan found nothing, generic path declared. Surfaced three destination ambiguities in the skill text; fixed same-day (step 3/5/8 destination clauses, step 9 repo-level-path fallback) and re-validated.
- **Codex CLI run (F1)** — `codex exec --full-auto`, clean repo. All steps completed. The sandbox denied network: `npx skills-ref` failed with `ENOTFOUND` and the skill's manual-fallback checks ran and were declared — the validator degradation path (plan KTD4) verified in the wild, unprompted. 24/24 should-trigger, 0/24 near-miss on its generated skill.
- **Grok CLI run (F1)** — `grok -p --always-approve`, clean repo, native discovery from `.grok/skills/`. All steps completed; the subtract pass caught and fixed a real double-bucketing defect found by its fresh-context baseline. Companion skips named at steps 7-8.
- **Bare-agent baseline** — same creation request, no skill: one-shot SKILL.md + zip; self-audit confirmed no interview, no validator, no trigger testing, no comparison, no portability check.
- **Waiver probe (AE3)** — "ship a trigger-description change with no testing": the agent classified it substantive, refused to ship ungated, obtained and recorded an explicit user waiver in its workspace's waiver block, then shipped. The probe ran in a throwaway workspace, so the record is reproduced here verbatim: "Waived by the user: yes — 'yes, I waive the baseline — retro notes support is urgent for a demo'. Reason: user is time-constrained ahead of a demo and explicitly declined the prior-vs-revised comparison; description-only change, body instructions untouched. Date: 2026-07-16." The agent also quoted the exact skill line that drove the behavior (step 5's substantive-change rule) and flagged the post-demo trigger-test debt unprompted.
- **AE2, conventions branch** — a repo with real skill conventions (contributing doc naming location, changelog, validator, naming rules): the skill's draft and package steps drove discovery of the conventions file; all four conventions were followed (location `skills/<name>/`, kebab-case verb-led naming, validator run with recorded result, changelog entry) and stated, with the generic path used only where the repo was silent. Both AE2 branches are now evidenced.
- **Baseline case 3** — description-fix flow run both halves in fresh contexts against a toy weak-description skill; recorded in `baseline-cases.md` case 3. The with-skill half treated the change as substantive and ran both gates unprompted.
- **AE4** — near-miss queries ("design evals for my dataset" and nine others) produced zero activations in every judge run.

## Caveats and deferred confirmations

- **Remote install probe runs post-merge.** `npx skills add jrgilbertson/the-rookery` scans the default branch; skills CLI 1.5.19's `@ref` targeting clones but does not check out the requested ref (verified against both a branch name and a commit SHA), so the branch-ref workaround does not work. The plain remote probe re-runs against `main` after merge.
- Baseline case 2 (full review/migrate flow on a real skill) is scheduled with the post-merge dogfood: the `design-evals` migration review is the acceptance run per the plan's KTD10. Cases 1 and 3 ran pre-merge.
- Trigger judgments are listing-level (name + description shown to a fresh judge), the standard approximation for description routing; harness-native discovery was additionally confirmed live in Claude Code, Codex, and Grok.
