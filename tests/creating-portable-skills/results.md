# Acceptance evidence: creating-portable-skills

Recorded runs for the plan's Verification Contract (`docs/plans/2026-07-16-001-feat-creating-skills-plan.md` (the plan keeps its pre-rename filename as a point-in-time record)). Date: 2026-07-16. Tool versions this run: `skills-ref` 0.1.5, `skills` CLI 1.5.19, Codex CLI 0.144.4, Grok CLI 0.2.101, Claude Code (Fable 5 session; judge runs also on Haiku 4.5 and Sonnet).

## Gate results

| Gate | Result | Evidence |
| --- | --- | --- |
| Static validation | Pass | `npx skills-ref validate skills/creating-portable-skills` → "Valid skill", clean after every edit round |
| Line budget | Pass | `SKILL.md` at 107 lines (ceiling 500, target ~200) |
| Same-door sweep | Pass | Zero hits for home-directory paths and owner-environment identifiers across `skills/creating-portable-skills/` and `tests/creating-portable-skills/` |
| Install probe | Partial pass: local-source probe passed; remote probe (from jrgilbertson/the-rookery) pending post-merge (see caveat) | `npx skills add . --skill creating-portable-skills --agent claude-code --agent codex -g -y --copy` installed to both `~/.claude/skills/` and `~/.agents/skills/`; skill registered live in the running harness. See the branch-ref caveat below |
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
- **writing-great-skills review pass** — the owner-invoked review found two description findings (a workflow-summary sentence the skill's own gotcha warns against; a duplicated migrate/port branch) and one negation-phrasing bullet in step 3. All three were fixed; the description change was ruled substantive under the skill's own rule, and the trigger set re-ran with three fresh judges across three model families: identical pass (rate 1.0 on all should-triggers, zero near-miss activations). The step 3 rewording preserves instruction semantics (positive phrasing of the same constraints), so it fell under the trivial-edit exemption.
- **Skill-engineering adoption pass** — two additions sourced from Paul Bakaus's "Dark Arts of Skill Engineering" (via the Latent Space write-up): a steering-points interview bullet (which decisions stay with the user) and an operationalized-qualifiers review-checklist item. Ruled substantive (instruction semantics + bundled resource); the prior-vs-revised gate probe confirmed both deltas — the prior interview yields a fully-automatic skill for a taste-heavy job while the revised one forces named steering points, and the qualifiers item flags undefined adjectives ("punchier", "thorough", "clean") that the delete test demonstrably keeps but never defines. Description unchanged, so the trigger set was unaffected.
- **Owner review pass (style + protocol)** — owner-directed revisions: intro rewritten to drop the models-already-know-the-format assumption (it conflicted with the skill's own weaker-models gotcha), an em-dash and unnecessary-colon sweep across all six files, and step 8's trigger test reduced from a 48-60-call protocol to a 10-call default (5+5 queries judged once, all-pass rule) with a full-rigor tier (8-10 queries, 3 runs) reserved for public-collection shipping. Gate probe confirmed the reduction preserves test integrity at roughly one-sixth the cost and the escalation fork is live, and adversarially caught that "borderline" was an undefined qualifier (the exact failure class of the new checklist item); fixed by requiring plain yes/no/unsure judgments with unsure-or-hedged defined as borderline. Description changed only in punctuation, which is formatting-exempt from the trigger gate. This skill's own fixture stays on the full-rigor tier since it ships to a public collection.
- **Rename** — `creating-skills` became `creating-portable-skills` by owner decision, putting the cross-harness stance in the name so catalog browsers see it before investing (and Claude-Code-only expectations are corrected up front). Earlier run-log entries reference the new name retroactively; the runs themselves predate the rename. The listing changed, so the trigger set re-ran at the full-rigor tier under the new name: three fresh judges across three model families (Haiku 4.5, Sonnet, Fable 5), identical pass, every should-trigger at rate 1.0, zero near-miss activations. Installed copies on the maintainer machine were refreshed under the new name and the old-name copies removed.
- **AE4** — near-miss queries ("design evals for my dataset" and nine others) produced zero activations in every judge run.

## Caveats and deferred confirmations

- **Remote install probe runs post-merge.** `npx skills add jrgilbertson/the-rookery` scans the default branch; skills CLI 1.5.19's `@ref` targeting clones but does not check out the requested ref (verified against both a branch name and a commit SHA), so the branch-ref workaround does not work. The plain remote probe re-runs against `main` after merge.
- Baseline case 2 (full review/migrate flow on a real skill) is scheduled with the post-merge dogfood: the `design-evals` migration review is the acceptance run per the plan's KTD10. Cases 1 and 3 ran pre-merge.
- Trigger judgments are listing-level (name + description shown to a fresh judge), the standard approximation for description routing; harness-native discovery was additionally confirmed live in Claude Code, Codex, and Grok.

## 2026-07-27 frontier retune

Plan: `docs/plans/2026-07-27-001-refactor-creating-portable-skills-frontier-retune-plan.md`.
Frozen prior: `af5e4f686528961b7dd401fa7b780f485ca774fd`.
Final behavioral candidate for this phase: `c1ec71a`.

Tool and target metadata:

- Agent Skills validator 0.1.5.
- Codex CLI 0.145.0 with exact model `gpt-5.6-sol`, high reasoning,
  ephemeral read-only runs, and user config ignored.
- Claude Code 2.1.220 with exact model `claude-opus-5`, high effort, project
  settings, and no session persistence for matched cells.

### U3 gate states

| Gate | State | Evidence and limitation |
| --- | --- | --- |
| Structural validation | passed | `npx skills-ref validate skills/creating-portable-skills` → `Valid skill`; final body 95 lines |
| FR-D1 create comparison | passed within Claim Ceiling | Both target cells used the complete contract without questions and preserved every named item; the result was `same`, so the final candidate retained focused one-question-at-a-time clarification for material gaps |
| FR-C1 authority control | passed within Claim Ceiling | Both target cells stopped before drafting and kept auto-close authority user-owned; final Opus led with that boundary, final Sol asked the same single focused boundary question as prior |
| FR-P1 same-decision probe | passed | Both priors chose subtraction; both finals retained the instruction and treated missing affected evidence as unverified |
| FR-P2 waiver probe | passed | Both finals kept the unavailable cell unverified and did not raise the label or authorize removal |
| FR-P3 divergence probe | passed | Both finals preserved pass, loss, and unavailable states and required revision/rerun, then retention or target narrowing |
| Strong-claim probe | passed | Both finals refused causal and non-regression labels for a small matched comparison and named the missing rigor without requiring another skill |
| Opus full fixture flow | retained | Audit, pre-edit approval boundary, scoped disposable revision, validation, and matched application comparison ran; application result was `same`, so the candidate removals remained unsupported and the safe-publication sequence remained intact |
| Sol focused fixture audit | passed as focused coverage | Prior and final both stopped for approval and preserved the fragile sequence; the final used explicit System-Owned Invariant classification, but prose-level differences alone were not treated as improvement evidence |
| Listing proxy | passed in both target cells | Full tables in `trigger-queries.md`; 10/10 should-trigger at 3/3 `yes` in each target and zero near-miss `yes`; Opus recorded two `unsure` judgments on one near-miss |

### Raw-enough decision excerpts

- Prior Sol FR-P1: `"decision": "subtract"`, because the observation did
  not discriminate prior from revised.
- Prior Opus FR-P1: `Do not ship as-is. Subtract` because `same everywhere`
  did not let the instruction earn its tokens.
- Final Sol FR-P1: `retain_current_instruction`; the discriminating case
  showed no intended delta and the missing control stayed unverified.
- Final Opus FR-P1: `Retain the candidate instruction as-is; do not remove or
  relax it.`
- Final Sol FR-C1: `What exact ticket classes, if any, may the skill close
  without per-ticket user approval?`
- Final Opus FR-C1 led with `Auto-close authority` and explicitly labeled it
  the one question asked now; later material gaps were queued rather than used
  to widen auto-close authority.
- Opus fixture audit returned `edited_files: []` and
  `next_action: await_fix_scope_approval`; a repository diff confirmed the
  disposable target was unchanged until approval.

### Claim Ceiling after U3

The retune is a **DirectionalCandidate**. The predeclared create and policy
cases show no observed invariant loss, and the unsafe `same` → delete shortcut
changed in the intended direction on both current targets. These runs do not
prove causal improvement, non-regression, equivalent behavior across targets,
or behavior outside the named cases. Listing results remain proxy evidence.
Local-source installation, installed-content identity, native discovery,
native load, and native trigger are still unverified until U4 records them.
