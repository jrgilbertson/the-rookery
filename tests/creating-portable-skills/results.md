# Acceptance evidence: creating-portable-skills

Recorded runs for the plan's Verification Contract (`docs/plans/2026-07-16-001-feat-creating-skills-plan.md` (the plan keeps its pre-rename filename as a point-in-time record)). Date: 2026-07-16. Tool versions this run: `skills-ref` 0.1.5, `skills` CLI 1.5.19, Codex CLI 0.144.4, Grok CLI 0.2.101, Claude Code (Fable 5 session; judge runs also on Haiku 4.5 and Sonnet).

## Gate results

| Gate | Result | Evidence |
| --- | --- | --- |
| Static validation | Pass | `npx skills-ref validate skills/creating-portable-skills` → "Valid skill", clean after every edit round |
| Line budget | Pass | `SKILL.md` at 107 lines (ceiling 500, target ~200) |
| Same-door sweep | Pass | No owner-specific home paths or owner-environment identifiers across `skills/creating-portable-skills/` and `tests/creating-portable-skills/`; generic documented discovery locations and normalized disposable placeholders are acceptable |
| Historical 2026-07-16 install probe | Pass: local-source installation passed on 2026-07-16; the remote default-branch listing passed after merge on 2026-07-27 | The local install copied the skill to both agent locations and registered it in the running harness. Skills CLI 1.5.20 later found `creating-portable-skills` in `jrgilbertson/the-rookery` through the plain remote listing command. The follow-up is non-gating for the 2026-07-27 final-source U4 result |
| Trigger evaluation | Pass | 10/10 should-trigger at rate 1.0 (3 runs each), 0/10 near-miss activations, judged in fresh contexts across three model families (Haiku 4.5, Sonnet, Fable 5). Full tables: `trigger-queries.md` |
| Baseline test | Pass | Bare-agent baseline skipped all four disciplines (self-audited); with-skill runs in three harnesses enforced all four. Comparison: `baseline-cases.md` case 1 |
| Visitor create-flow (F1) | Pass | Clean non-Rookery repo, no companions: all loop steps completed, AE1 and AE2 confirmed (see below) |
| Cross-harness runs | Pass | F1 end-to-end in Codex CLI and Grok CLI from clean installs (see below) |
| Link pass | Pass | 9/9 unique URLs across both references (12 occurrences) return HTTP 200 |

## Run log

- **Claude Code visitor run (F1).** The clean repository had no conventions or
  companions. All steps 1-9 met their criteria. For AE1, the run recommended
  `design-evals`, included the install command, ran the built-in baseline, and
  named the skipped depth. For AE2, the convention scan found nothing and used
  the generic path. The run exposed destination ambiguities in steps 3, 5, and
  8, plus a missing repository-level path fallback in step 9. Each became a
  small skill-text fix and passed revalidation the same day.
- **Codex CLI run (F1).** `codex exec --full-auto` completed every step in a
  clean repository. The sandbox denied network access, so `npx skills-ref`
  failed with `ENOTFOUND`. The skill used its manual fallback checks and stated
  that the validator was skipped, which exercised the KTD4 degradation path
  without a scripted failure. The generated skill passed 24/24 should-trigger
  queries with zero activations across 24 near-misses.
- **Grok CLI run (F1).** `grok -p --always-approve` loaded the project skill
  from `.grok/skills/` and completed every step. The fresh-context baseline
  found a real double-bucketing defect, and the subtract pass fixed it. The run
  also named the companion checks skipped at steps 7-8.
- **Bare-agent baseline.** The same creation request without the skill produced
  one `SKILL.md` file and a zip. Its self-audit confirmed that it skipped the
  interview, validator, trigger tests, behavior comparison, and portability
  check.
- **Waiver probe (AE3).** The request was "ship a trigger-description change
  with no testing." The agent treated the change as substantive, refused to
  ship without a gate, recorded an explicit user waiver, and then shipped. The
  throwaway workspace recorded this text verbatim: "Waived by the user: yes —
  'yes, I waive the baseline — retro notes support is urgent for a demo'.
  Reason: user is time-constrained ahead of a demo and explicitly declined the
  prior-vs-revised comparison; description-only change, body instructions
  untouched. Date: 2026-07-16." The agent also quoted the skill rule that drove
  the decision, identified it as step 5's substantive-change rule, and flagged
  the post-demo trigger-test debt.
- **AE2 conventions branch.** The test repository defined a skill location,
  naming rule, validator, and changelog policy. The workflow found and followed
  all four: `skills/<name>/`, a kebab-case verb-led name, a recorded validator
  run, and a changelog entry. It used the generic path only where the repository
  was silent. Both AE2 branches now have evidence.
- **Baseline case 3.** Both halves of the description-fix flow ran in fresh
  contexts against a toy skill with a weak description. The with-skill run
  treated the edit as substantive and ran both required gates. Full results are
  in `baseline-cases.md`.
- **`writing-great-skills` review pass.** The review found a workflow summary in
  the description, duplicate migrate and port triggers, and one negative step 3
  instruction. All three were fixed. The description change was substantive,
  so three fresh judges from three model families reran the trigger set. Every
  should-trigger passed at 1.0 and no near-miss activated. The step 3 edit kept
  the same meaning and qualified for the trivial-edit exemption.
- **Skill-engineering adoption pass.** Two additions came from Paul Bakaus's
  "Dark Arts of Skill Engineering" through the Latent Space write-up: a list of
  decisions that remain with the user and a checklist item for undefined
  qualifiers. The prior-versus-revised probe confirmed both changes. The prior
  interview made every decision for a taste-heavy task. The revision stopped at
  the named user decisions. The new checklist item flagged "punchier,"
  "thorough," and "clean," which the delete test kept without defining. The
  description did not change, so the trigger set was unaffected.
- **Owner review pass for style and protocol.** The intro stopped assuming that
  models already knew the format because that conflicted with its own
  weaker-model guidance. All six files received an em-dash and colon cleanup,
  and the trigger test dropped from 48-60 calls to a 10-call default. The gate
  probe showed that the smaller test kept its integrity at roughly one-sixth the
  cost. Public collections still use 8-10 queries per side with three runs each.
  The same probe found "borderline" undefined, so the protocol now requires
  plain `yes`, `no`, or `unsure` judgments and treats unsure or hedged answers as
  borderline. The description changed only in punctuation, so the trigger gate
  did not rerun. This public skill keeps the larger query tier.
- **Rename.** The owner renamed `creating-skills` to
  `creating-portable-skills` so catalog readers see its cross-harness scope
  before opening it and do not assume it is Claude Code-only. Earlier run-log
  entries use the new name, although those runs predate the rename. Three fresh
  judges from Haiku 4.5, Sonnet, and Fable 5 reran the full trigger tier. Every
  should-trigger passed at 1.0, no near-miss activated, and installed copies
  moved to the new name.
- **AE4.** The near-miss query "design evals for my dataset" and nine other
  queries produced zero activations in every judge run.

## Caveats and deferred confirmations

- **Historical 2026-07-16 remote publication follow-up (non-gating for the 2026-07-27 final-source U4 result).** Skills CLI 1.5.19's `@ref` targeting cloned the repository but did not check out the requested ref, verified against both a branch name and a commit SHA. After PR #4 merged, `npx skills@1.5.20 add jrgilbertson/the-rookery --list` reported four skills from the default branch and included `creating-portable-skills`. This completed the deferred publication check on 2026-07-27 without changing the historical `@ref` finding.
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

### U3 checkpoint gate states

This table preserves the U3 checkpoint before the later review-fix follow-up.
Pending or unverified states here are superseded by the current sections below.

| Gate | State | Evidence and limitation |
| --- | --- | --- |
| Structural validation | passed | `npx skills-ref validate skills/creating-portable-skills` → `Valid skill`; final body 95 lines |
| FR-D1 create comparison | retained within Claim Ceiling | Both target cells used the complete contract without questions and preserved every named item; the discriminating result was `same`, so it earns no behavioral-improvement claim for the step-1 group |
| FR-C1 authority control | passed as a stable control | Both target cells stopped before drafting and kept auto-close authority user-owned; final Opus led with that boundary, but question-order movement in a predeclared control is not improvement evidence |
| FR-P1 same-decision probe | passed | Both priors chose subtraction; both finals retained the instruction and treated missing affected evidence as unverified |
| FR-P2 waiver probe | passed | Both finals kept the unavailable cell unverified and did not raise the label or authorize removal |
| FR-P3 divergence probe | passed | Both finals preserved pass, loss, and unavailable states and required revision/rerun, then retention or target narrowing |
| FR-P4 new-skill unavailable-target probe | pending at U3 checkpoint; superseded below | Predeclared in `baseline-cases.md`; the later review-fix follow-up passed in both target cells |
| Strong-claim probe | passed | Both finals refused causal and non-regression labels for a small matched comparison and named the missing rigor without requiring another skill |
| Opus full fixture flow | completed; candidate retained | Audit, pre-edit approval boundary, scoped disposable revision, validation, matched application comparison, affected listing-proxy checks, and local-source packaging ran; application result was `same`, so the candidate removals remained unsupported and the safe-publication sequence remained intact |
| Sol focused fixture audit | passed as focused coverage | Prior and final both stopped for approval and preserved the fragile sequence; the final used explicit System-Owned Invariant classification, but prose-level differences alone were not treated as improvement evidence |
| Listing proxy | Sol passed; Opus failed under the current public-tier rule | Full historical tables in `trigger-queries.md`; 10/10 should-trigger passed in each target, but the Opus `unsure` / `unsure` / `no` near-miss result had only one categorical `no`. The later 2026-07-28 full rerun separately supports the final description-bound pass |

### Decision excerpts

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

### Opus fixture trigger and package completion

Because the disposable fixture description changed, a routine listing-proxy
check ran five should-trigger and five near-miss queries on Opus 5. Each ran in
a fresh tool-less process that saw only the fixture name and description. All
five should-trigger judgments were `yes`, all five near-miss judgments were
`no`, and no result was borderline.

The revised fixture then installed from its local source through skills CLI
1.5.20 into a disposable Claude Code project. `diff -qr` found no difference
between source and installed content. Both source and installed `SKILL.md`
files had SHA-256
`94877b118a7c4e7b1b1351db8d4c6d6ba601831199a8b648c12ecbebc714b238`.

### Claim Ceiling at the U3 checkpoint

The unsafe `same` → delete shortcut changed in the intended direction on both
current targets, supporting a **DirectionalCandidate** for the
candidate-decision policy only. The step-1 candidate is **Retained**: FR-D1 was
`same` in both targets, and FR-C1's stable-control question-order movement does
not earn a behavioral-improvement claim. These runs do not prove causal
improvement, non-regression, equivalent behavior across targets, or behavior
outside the named cases. Listing results remain proxy evidence. At this U3
checkpoint, local-source installation, installed-content identity, native
discovery, native load, and native trigger were unverified; the later U4
sections supersede this interim state.

### U4 local-source and native checks

The final package source was revision
`61bd49283426c4c7f149b8f245b8408bcff7cbba`; its `SKILL.md` SHA-256 was
`092a0846f2d0b1faf77f3bed646f547374dc0622268c9368ae9848642c872c57`.
The skills CLI was version 1.5.20.

From a fresh disposable Git repository, this command ran against the local
working tree rather than a remote default branch:

```bash
npx skills add <local-repository-path> \
  --skill creating-portable-skills --agent codex --agent claude-code --copy -y
```

The installer reported one selected skill and copied it to both
`.agents/skills/creating-portable-skills` and
`.claude/skills/creating-portable-skills`. `diff -qr` returned no differences
between either installed directory and the canonical source. All six installed
file hashes matched across the two destinations; the `SKILL.md` hash above
also matched the source.

| Check | Codex package/model cell | Claude Code package/model cell |
| --- | --- | --- |
| Local-source install | passed | passed |
| Installed-content identity | passed | passed |
| Native discovery | passed; implicit query selected the project skill after the colliding user-level path was disabled | passed; Claude initialization listed `creating-portable-skills` in both `skills` and `slash_commands` |
| Native load | passed; tool trace read `<disposable-project>/.agents/skills/creating-portable-skills/SKILL.md` | passed; native `Skill` tool returned `Launching skill: creating-portable-skills` and a base directory under the disposable project's `.claude/skills` |
| Native trigger | passed on “turn this repeated Agent Skill review prompt into a reusable skill” | passed on the same representative implicit query |

Both native runs also returned the exact first body sentence as corroboration:
`Create or revise a skill from its intent, hard constraints, authority
boundaries, success criteria, and output contract.` Codex ran as
`gpt-5.6-sol` at high reasoning in read-only mode. Claude Code ran as
`claude-opus-5` at high effort with only the native `Skill` capability enabled;
its stream showed the direct tool invocation and project-local base directory.

These U4 checks apply to source revision `61bd492`. Review fixes later changed
bundled package files at `feb9a0e`, so the install, identity, and native checks
must rerun against the final source before they can support the final status.

### Review-fix follow-up at `feb9a0ee9246b8c079bea7c049efe9f5a67c657c`

#### FR-P4 new-skill unavailable-target policy

The Sol exact-file run returned `NewSkillCandidate`, kept the Sol target
unverified, set shipment to `UnverifiedCandidate`, and assigned no
`DirectionalCandidate` or cross-target upgrade. It labeled the already observed
Opus-only cell `smoke-tested` without treating that observation as Sol or
cross-target evidence.

Two initial Opus attempts quoted rules absent from the exact project files,
consistent with contamination from an older same-name user skill. Both were
discarded and are not evidence. A fresh Opus 5 safe-mode, tool-less run with the
exact authoritative policy embedded returned `NewSkillCandidate`, kept Sol
unverified, set shipment to `UnverifiedCandidate`, assigned no
`DirectionalCandidate` or cross-target upgrade, and left the earned label
unchanged.

FR-P4 passed in both target cells within its policy-probe scope.

#### Full Sol fixture flow

The final `creating-portable-skills` package at revision `feb9a0e` installed
into the disposable Codex project and exactly matched the source. Its
`SKILL.md` SHA-256 was
`092a0846f2d0b1faf77f3bed646f547374dc0622268c9368ae9848642c872c57`.

The audit loaded that installed project skill, made no edits, identified the
fixture's description and workflow ceremony, preserved the temporary-sibling →
formatter and validator → replace only after both pass → leave the live file
untouched and report the temporary path on failure sequence, returned an
approval boundary, and waited. After scripted scoped approval, Sol revised only
the disposable fixture and validated it with `skills-ref` 0.1.5. The prior
fixture SHA-256 was
`b9236148a6cad1f1365e68fd775ea3183031d0eef60d4baf1676ef7457e6760e`; the
revised SHA-256 was
`bb12c084300e23b7e9aae8406ab7a50c75da281ce4e7aea73348cb61522b4105`.

Fresh matched results:

- **Drafting discriminator:** the prior stopped on a redundant audience
  question despite the supplied audience. The revision was ready with no
  questions, grounded every factual claim, included the breaking-change action,
  and preserved review-only/no-overwrite authority. The intended delta was
  observed on Sol.
- **Formatter-failure control:** both variants left `RELEASE_NOTES.md`
  untouched after formatter failure and reported `RELEASE_NOTES.md.tmp`; the
  fragile invariant was preserved.

The revised fixture's routine Sol listing proxy ran five should-trigger and
five near-miss queries in fresh tool-less contexts. All five should-trigger
judgments were `yes`, all five near-misses were `no`, and no result was
borderline. Local-source Codex packaging through skills CLI 1.5.20 passed; the
installed fixture hash matched
`bb12c084300e23b7e9aae8406ab7a50c75da281ce4e7aea73348cb61522b4105`, and
`diff -qr` was clean.

The Sol discriminator improved while the Opus fixture result was `same`.
Accordingly, the cross-target fixture candidate remains **Retained**. The cells
are not averaged, and this record supports no general improvement claim.

### Final-source U4 rerun at `feb9a0ee9246b8c079bea7c049efe9f5a67c657c`

The current local source installed into both project paths under disposable
workspace `<final-source-disposable-workspace>`:

- `.agents/skills/creating-portable-skills`
- `.claude/skills/creating-portable-skills`

All six installed files exactly matched the current source:

| Package file | SHA-256 |
| --- | --- |
| `SKILL.md` | `092a0846f2d0b1faf77f3bed646f547374dc0622268c9368ae9848642c872c57` |
| `assets/baseline-test-template.md` | `2bd6e275e0c89efddddec86730fd0bfd6d9acc2391b2a8e53bdd15b32bfce60a` |
| `assets/skill-template.md` | `275694e017dcb91a4299a021ba9dacbf02a9873d006d7499e04d8d4db042e1aa` |
| `assets/trigger-queries-template.md` | `eb521fbc1a40dd1fb499e27a9c3cf14d079a8f6766ae32ca5474286352d935cb` |
| `references/portability.md` | `7b349942cee171f2bc25a1e3084db2695ee689e8b54b8c09cb12f15620ed9d31` |
| `references/review-checklist.md` | `901fcb57dac272d1b6f443b7e183feae7d150c010a50e9d94f2ee4f17e0ecedd` |

| Check | Codex / `gpt-5.6-sol` high | Claude Code / `claude-opus-5` high |
| --- | --- | --- |
| Local-source install | passed at the final source revision | passed at the final source revision |
| Installed-content identity | passed; all six files matched | passed; all six files matched |
| Native discovery | passed; the query triggered `creating-portable-skills` | passed; initialization listed the skill and slash command |
| Native load | passed; the tool trace read the exact installed `.agents` `SKILL.md` | passed; direct `Skill` call reported `Launching skill: creating-portable-skills` from the exact installed `.claude` base directory |
| Native trigger | passed; the implicit query selected the native skill | passed; the implicit query invoked the native `Skill` tool |

As separate behavioral corroboration, both finals included this exact sentence:
`Create or revise a skill from its intent, hard constraints, authority
boundaries, success criteria, and output contract.`

### U2 template-instantiation verification

At disposable root `<template-instantiation-disposable-root>`, the current
`assets/skill-template.md` was instantiated as skill
`template-instantiation-smoke`. Authoring comments were stripped, a concrete
description was supplied, the optional license was deliberately omitted, and
the workflow was filled. The current baseline and trigger templates were also
instantiated by filling every bracketed record placeholder. A placeholder sweep
found zero remaining bracketed placeholders.

The first validator run failed only because the generated directory was named
`skill` while frontmatter named the skill `template-instantiation-smoke`.
Renaming the directory to match frontmatter satisfied the documented package
invariant. The corrected run:

```text
npx skills-ref validate <template-instantiation-disposable-root>/template-instantiation-smoke
Valid skill
```

Generated artifact hashes:

| Artifact | SHA-256 |
| --- | --- |
| `template-instantiation-smoke/SKILL.md` | `fe0d2dfe7e8cbd8709270db46b78fca3d9d8a0008835b2551fd90e0c8df951d3` |
| Instantiated baseline record | `7b0ffd1e8ecc108a0bc8b4b3a7fc2439ededabc42107f87b075fe5d491220600` |
| Instantiated trigger record | `27e98a3159ef225c5c94dffddf447638e0706ab3f94d2404237daf0b353fa4a0` |

The instantiated baseline exposed mode, candidate group, named invariant,
output contract, target set, target conclusions, earned label, and limitation.
The instantiated trigger record exposed target metadata, listing-proxy rows,
package-harness and native rows, earned label, and limitation. This is
structural template evidence only; it does not upgrade any behavioral claim.

### Historical final retune state at `feb9a0e`

| Evidence layer | State |
| --- | --- |
| Structural validation | passed |
| U2 template instantiation | passed; generated skill validated and both evidence records exposed every required field, structural evidence only |
| Step-1 behavioral candidate | Retained; FR-D1 was `same`, while FR-C1 remained a stable control |
| Directional behavioral comparison | passed for the unsafe `same` → delete policy transition only |
| FR-P4 new-skill state policy | passed in both target cells within the predeclared policy-probe scope |
| Full fixture flow | completed in both target cells; cross-target candidate Retained because Opus was `same` while Sol showed the intended delta |
| Listing proxy | passed in both target cells on the later 2026-07-28 full rerun; every near-miss received three categorical `no` judgments |
| Prior-source U4 install, identity, and native checks | passed at source revision `61bd492`; superseded for final-package verification |
| Final-source U4 install, identity, and native checks | passed at `feb9a0e` in both recorded target harnesses; all six installed files matched the source |

Final workflow state: **VerifiedRetune**, scoped strictly to the recorded
`gpt-5.6-sol`/Codex and `claude-opus-5`/Claude Code target cells and the checks
above under the Claim Ceiling. This does not establish causal improvement,
non-regression, equivalent behavior across targets, universal behavior, or
behavior outside the recorded cases. The remote default-branch listing passed
after merge and remains separate from the pre-merge behavioral evidence.

### Outcome-and-constraints follow-up

The optional template section is now `Outcome and constraints`. A focused
prior-versus-revised comparison ran one discriminating incident-note case and
one simple sorting control on Claude Code 2.1.220 with `claude-opus-5` at high
effort and Codex CLI 0.145.0 with `gpt-5.6-sol` at high reasoning. Both revised
discriminator runs used the new heading, preserved the required outcome,
factuality boundary, and user approval boundary, and made neither `jq` nor
bullet lists mandatory. Both prior and revised control runs omitted the
optional section and left the sorting method open. No named outcome or hard
constraint loss was observed. Case definitions, variant hashes, target
configuration, observations, and the directional Claim Ceiling are recorded in
`baseline-cases.md`.

The revised source passed `skills-ref` 0.1.5 at 95 lines. Two disposable
template instances also passed: one retained `Outcome and constraints` because
it carried nonduplicative requirements, while a simple sorting skill omitted
the section. Their `SKILL.md` SHA-256 values were
`b9ea76f5d53ad1201ba746c4e96a56f9192a622465d89750376c8dc307afb5d7`
and `8067394f08b430b1a63276ad20a88c3191a54252b152ef429915ad64506e2453`,
respectively.

Skills CLI 1.5.20 installed the revised package from the current local source
into fresh project-local Codex and Claude Code destinations. `diff -qr` was
clean for both installed directories, and the source and installed `SKILL.md`
files shared SHA-256
`71416c5a4c314eeeec4a7fc2b6cbe512ee48274598291f6d0a0d21212d684941`.
The description and trigger boundary did not change in this follow-up, so the
listing and native-trigger suites were not rerun and earn no new evidence from
this section.

### Independent-review and evidence-quality follow-up

Date: 2026-07-27. Frozen prior: `5af34de`. Revised `SKILL.md` SHA-256:
`9d9352e5776b1bd8bb77459c614f1f612de5bc79fe0395c6b8d2e5f5333add26`.
The target was `gpt-5.6-sol` at xhigh reasoning effort in Codex CLI 0.145.0,
verified from the agents' recorded session metadata. This record covers that
one model-harness target and makes no cross-model claim.

Every execution and judgment used a separate agent started with no inherited
conversation turns. The prior and revised policy outputs came from
`case1_prior_executor` and `policy_revised_final`; the mechanical control came
from `case2_prior_executor` and `case2_revised_rerun`. The independent matched
grader was `policy_grader_final`. The table below is the canonical retained
record of the per-case evidence and conclusions.

| Case | Frozen check | Prior excerpt | Revised excerpt | Independent conclusion |
| --- | --- | --- | --- | --- |
| Grading policy discriminator | Require a grader independent of the author and artifact producers to inspect the actual artifact and trace; keep the grade unverified when no independent context is available. | `case1_prior_executor`: “The workflow does not require a separate independent or blinded grader.” | `policy_revised_final`: “A separate fresh-context agent that neither authored the revision nor produced the artifacts grades each matched result.” It also required direct artifact and trace inspection, concrete pass evidence, review of weak checks, and an unverified handoff when an independent context is unavailable. | `policy_grader_final`: intended delta observed, with no loss in the supplied answer. Policy recall does not prove artifact-level compliance. |
| Mechanical-validation control | Keep structural validation deterministic and do not require an agent review for a mechanical validator run. | `case2_prior_executor`: “A separate review agent is not required. Run `npx skills-ref validate <skill-directory>`.” | `case2_revised_rerun`: “No separate review agent is required. Use `npx skills-ref validate skills/creating-portable-skills`.” | `final_behavior_grader`: materially stable; both variants kept mechanical validation deterministic. |

The grader found no observed loss in the two supplied answers. It limited the
result to a directional comparison and noted that policy recall does not prove
artifact-level compliance.

An artifact-level probe tested that limitation. The executor summary claimed a
report passed, while the complete artifact was `# Recommendations` followed by
`Rename the service.` The trace said `Did not open incidents.csv because the
likely risks were obvious.`
`artifact_grade_prior` and `artifact_grade_revised` both rejected the claimed
pass, cited the artifact and trace, and identified the filename and heading
checks as insufficient. `artifact_comparison_reviewer` judged the result
materially the same. This probe shows correct behavior for one case. It does
not establish general reliability or non-regression.

Three additional matched cases used the same clean-context separation:

| Case | Frozen check | Prior excerpt | Revised excerpt | Independent conclusion |
| --- | --- | --- | --- | --- |
| Trigger-query realism | Vary detail, formality, implied intent, abbreviations, and minor errors while preserving the intended trigger boundary. | `trigger_prior_executor`: “Audit this batch of vendor invoices for duplicate charges.” The set stayed mostly formal and direct. | `trigger_revised_executor`: “pls review this batch of AP invoices, i think one freight fee got billed twice”. The set varied detail, formality, implied intent, and minor errors. | `resource_comparison_grader`: intended delta observed; two terse queries could name vendor or AP invoices more explicitly. |
| Fixed-query classification control | Keep eight fixed invoice queries in their three should-trigger and five near-miss classes without rewriting them. | `trigger_control_prior`, commit `5af34de`: classified duplicate freight, invoice-to-PO mismatch, and supplier-tax audits as should-trigger; paying, negotiating, creating, entering, and summarizing invoice work stayed near-miss. | `trigger_control_revised`, `SKILL.md` hash `9d9352e5776b1bd8bb77459c614f1f612de5bc79fe0395c6b8d2e5f5333add26`: returned the same eight classifications. | `resource_control_grader`: materially stable with no changed classification. This controls trigger-query realism only. |
| Conditional method and destructive confirmation | Prefer the method that exposes canonical identities and deletion semantics, re-resolve destructive targets, and preserve user approval. | `template_prior_executor`: “Use an available shell command or API and keep the method open.” | `template_revised_executor`: prefer the workspace API when it exposes canonical identities and deletion semantics, otherwise use a shell inspection; re-resolve targets against the owning system before deletion. | `resource_comparison_grader`: intended delta observed with the approval boundary and method flexibility preserved. |
| Non-destructive one-tool control | Read UTF-8 text, sort it with Python's standard library, write to a distinct path, and verify the exact result without adding a tool menu or approval step. | `template_control_prior`, commit `5af34de`: used the required Python path, preserved the input, wrote UTF-8, reread the output, and compared it with the expected lines. | `template_control_revised`, `SKILL.md` hash `9d9352e5776b1bd8bb77459c614f1f612de5bc79fe0395c6b8d2e5f5333add26`: preserved the workflow and added regular-file and no-overwrite safeguards. | `resource_control_grader_final`: materially stable with no observed loss; it treated the extra file safeguards as outside the candidate instruction group. |
| Resource-placement control | Keep copied output in `assets/`, branch reading in `references/`, deterministic helpers in `scripts/`, and structural validation unchanged. | `template_control_prior`: copied output to `assets/`, branch reading to `references/`, and deterministic helpers to `scripts/`. | `template_control_revised`: preserved the same mapping and validator. | `resource_control_grader_final`: materially stable with no observed loss. |

Structural validation passed:

```text
npx skills-ref validate skills/creating-portable-skills
Valid skill: skills/creating-portable-skills
```

Skills CLI 1.5.20 installed the local source into fresh project-local Codex and
Claude Code destinations under `<independent-review-disposable-workspace>/project`.
`diff -qr` returned no differences for either installed package.

| Initial independent-review package file | SHA-256 |
| --- | --- |
| `SKILL.md` | `9d9352e5776b1bd8bb77459c614f1f612de5bc79fe0395c6b8d2e5f5333add26` |
| `assets/baseline-test-template.md` | `53ff7485f6ee63274d33d16b73d0258db2cba3fb984d8f4d16d2194a9b948b6a` |
| `assets/skill-template.md` | `88f38f6898893ab491b14a3d1cd1232a056c8dab4799abc1d001af3ac8d1b294` |
| `assets/trigger-queries-template.md` | `700d844b3361f1dfd2fd22a825a8b6eabc186e66ca9378e85f63c02794cba1bb` |
| `references/portability.md` | `7b349942cee171f2bc25a1e3084db2695ee689e8b54b8c09cb12f15620ed9d31` |
| `references/review-checklist.md` | `36e21e8e0529f5a0a92b13c218b941aedfb4cbdc752e7e93196b3fbe0e128b1e` |

The skill description did not change, so listing and native-trigger tests were
not rerun. Native discovery, load, and trigger at this new package hash remain
unverified. Earlier native results apply only to their recorded package hashes.

A later clean-context `no-ai-slop` review found three clarity defects in the
package: optional-sounding independent-grading language, a reversed
inspect-and-grade sequence, and the undefined phrase `raw-enough` in the
trigger evidence template. The final package makes the user-owned independent
review rule explicit and requires a result summary plus either an excerpt that
supports it or a durable reference.

A matched follow-up used separate prior, revised, and grading agents. The
reviewer-definition case made the distinct final reviewer explicit. The
evidence-field case stopped treating a missing transcript reference as a
provenance failure when a supporting excerpt was present. The resource-placement
control remained stable. These results are directional for the supplied cases
only.

The retained excerpts are:

| Case | Prior excerpt | Revised excerpt | Independent conclusion |
| --- | --- | --- | --- |
| Reviewer definition | “The final package review must use another fresh context.” | “Final package review must use a different fresh-context reviewer.” | `prose_fix_grader`: the author, matched-case grader, and final reviewer were unambiguous; this tests policy wording, not orchestrator compliance. |
| Evidence field | `PASS`, a supporting excerpt, and “no durable context or transcript reference exists, so fresh-context provenance is unverified.” | `PASS` with the same supporting excerpt; no transcript reference was required because the excerpt supplied the result evidence. | `prose_fix_grader`: intended delta observed without inventing a provenance limitation. |
| Resource placement | Copied output to `assets/`, branch material to `references/`, and deterministic helpers to `scripts/`. | Preserved the same mapping. | The independent grader found the control materially stable. |

The final package passed `skills-ref` validation at 100 lines. Skills CLI
1.5.20 installed it from local source into fresh project-local Codex and Claude
Code destinations, and `diff -qr` found no differences from source.

| Final package file | SHA-256 |
| --- | --- |
| `SKILL.md` | `a466934c86175d84fddfa611dd0fdce8f39c8ee8e3142128aac3ca63871812bd` |
| `assets/baseline-test-template.md` | `53ff7485f6ee63274d33d16b73d0258db2cba3fb984d8f4d16d2194a9b948b6a` |
| `assets/skill-template.md` | `88f38f6898893ab491b14a3d1cd1232a056c8dab4799abc1d001af3ac8d1b294` |
| `assets/trigger-queries-template.md` | `3c80a1c652e9edab1e2b839f217f8e1bfa63bc90500f32d7215252a6de96830b` |
| `references/portability.md` | `7b349942cee171f2bc25a1e3084db2695ee689e8b54b8c09cb12f15620ed9d31` |
| `references/review-checklist.md` | `d96af1066b12a2038335452fd8341978a37fc4906fa916dc360241858558b975` |

### Current state after the independent-review follow-up

| Evidence layer | Current state |
| --- | --- |
| Structural validation | Passed at the current package hash |
| Independent-grading policy comparison | Directional candidate for the recorded cases |
| Evidence-record wording comparison | Directional candidate for the recorded case |
| Artifact and trace grading probe | Same correct behavior in prior and revised; no improvement claim |
| Trigger-query construction comparison | Directional candidate for the recorded case |
| Conditional method and destructive-confirmation comparison | Directional candidate for the recorded case |
| Project-evidence grounding and conditional-example guidance | User-approved authoring guidance; behavioral effect unverified |
| Context target and long-reference navigation | Current package satisfies the stated size conditions; behavioral effect unverified |
| Mechanical-validation control | Materially stable |
| Local-source install and content identity | Passed in disposable Codex and Claude Code project paths; all six files matched |
| Listing and native discovery, load, and trigger | Not rerun at the current package hash; unverified for this follow-up |

Current conclusion: **directional comparison** for the four named candidate
groups only, with one smoke probe and the unverified authoring guidance listed
above. This follow-up does not establish causal improvement, non-regression,
equivalent behavior across models or harnesses, or behavior outside the
recorded cases.

## 2026-07-28 writing-great-skills follow-up

The frozen prior was commit `bc36fe1`. Fresh executors
`great_skills_prior`, `great_skills_revised`, and `read_only_revised_rerun`
produced the compared outputs; `great_skills_grader` and
`read_only_grader_rerun` graded them in separate contexts with no inherited
conversation turns.

The final package passed `skills-ref` 0.1.5 validation at 94 `SKILL.md` lines. Its
six file hashes were:

| Package file | SHA-256 |
| --- | --- |
| `SKILL.md` | `4693702db6766235049e34df7bf95baea77c1de24108307c09e0da5a809754fe` |
| `assets/baseline-test-template.md` | `82656e8d47635a5bbc1e181a79caaf921f703428b61f175dab7e87347acac8e5` |
| `assets/skill-template.md` | `e5cbfe744d93ba1c92c9a2a4dd97dbde00f51032ffe0563b95433683788f8458` |
| `assets/trigger-queries-template.md` | `f0294f045b56cdd0ddf7b1edfd104e34c3a995a6f9c14c66ad773b6e2bebdee3` |
| `references/portability.md` | `9cce3630326a7b01f455c241ae104550f0029d8a9d1ab9b672c6f57b015def6c` |
| `references/review-checklist.md` | `25fd4b36af18a891d03b3b1fa90ec907a94a114a630cb41a5e844b050a73d231` |

Skills CLI 1.5.20 installed the local working tree into fresh project-local
Codex and Claude Code paths under
`<writing-skills-disposable-workspace>`. `diff -qr` reported no
differences from the canonical package, and the installed `SKILL.md` hashes
matched the source.

| Check | Codex / `gpt-5.6-sol` | Claude Code / `claude-opus-5` |
| --- | --- | --- |
| Structural validation | passed | passed |
| Listing proxy | passed | passed |
| Local-source install | passed | passed |
| Installed-content identity | passed | passed |
| Native discovery | passed | passed |
| Native load | passed | passed |
| Native trigger | passed | passed |

The Codex native run used Codex CLI 0.145.0, high reasoning, and read-only
mode. An implicit reusable-skill request selected and read the project-local
`.agents/skills/creating-portable-skills/SKILL.md`, then quoted its first body
sentence. The fresh session ID was
`019fa99b-b285-77b3-bf43-1703f90fd667`.

The Claude Code native run used version 2.1.220, `claude-opus-5`, high effort,
project settings, no session persistence, and only the native `Skill` tool.
The initiating query was “Turn this repeated Agent Skill review prompt into a
reusable skill.” It did not name `creating-portable-skills`. The trace then
showed the assistant selecting the native `Skill` tool with
`skill: creating-portable-skills`; the tool returned `Launching skill:
creating-portable-skills` and the project-local
`.claude/skills/creating-portable-skills` base directory. The fresh session ID
was `d6eb7c3d-6a91-40ff-8777-574bb59da428`.

| Case | Frozen check | Retained evidence | Independent conclusion and limit |
| --- | --- | --- | --- |
| Read-only audit | Deliver findings and stop without asking for approval or beginning revision. | Prior terminal excerpt: “approve or reject the proposed material fix scope”. Revised rerun ended with the scoped review limitation and did not ask for approval, editing, or revision. | Intended delta observed after one revision and rerun. A later read-only pair was `same`; finding quality and repeatability remain unverified. |
| Generated trigger contract | Keep the description positive and omit a body section that merely repeats its trigger contract. | Prior description ended with `Do not use for paying invoices or negotiating with vendors` and added `## When to use`. Revised description stayed positive and omitted the body-level trigger echo. | Intended delta observed in one generated skeleton; activation was tested separately. |
| Evidence doctrine | Reserve evidence labels for matched cases and require a recorded Claim Ceiling. | Prior assigned a smoke label to one execution and found no Claim Ceiling field. Revised reserved labels for matched evidence, defined the Claim Ceiling, and named its baseline-record field. | Intended delta observed in the owning files; no completed evidence record was adjudicated in this case. |
| Matched-comparison ownership | Keep case construction, candidate decisions, labels, waivers, and the Claim Ceiling in the completed baseline record. | Prior found policy split across the skill and checklist. Revised identified the completed baseline record as the sole owner of case construction, candidate decisions, evidence labels, waivers, and Claim Ceiling recording. | Intended delta observed; textual ownership does not establish behavioral effectiveness. |
| Resource placement control | Preserve the existing resource mapping and validator. | Both variants mapped copied output to `assets/`, branch reading to `references/`, deterministic helpers to `scripts/`, and validation to `skills-ref`. | Materially stable. |

The result is a **directional comparison** for those named cases only. It does
not establish general reliability, causal improvement, non-regression, or
behavior outside the recorded cases and target configurations.

## 2026-07-28 verification-mode choice follow-up

The skill now asks the user to choose between ordinary personal skill
verification and public or unusually load-bearing skill verification before a
new skill is drafted or an approved revision is edited. The choice changes only
the listing-query tier. The skill does not ask the question during read-only
audits.

Fresh matched cases showed the intended choice in new-skill and
approved-revision flows, while a read-only control remained materially stable.
An independent grader assigned `DirectionalCandidate` with no material loss
observed. The conclusion remains bounded to the recorded cases and target.

| Case | Prior observation | Revised observation | Independent conclusion |
| --- | --- | --- | --- |
| New skill | `/root/mode_new_prior`: continued intent and resource work without asking about verification. | `/root/mode_new_revised`: asked the user to choose a mode and recommended ordinary personal verification. | Intended delta observed. |
| Approved revision | Session `019fa9c2-177e-77d3-ad71-2f183b67f454`: continued target and resource scoping before editing. | Session `019fa9c2-17a2-7992-a95c-0d03a1983ce8`: asked for the verification choice before editing and made a recommendation. | Intended delta observed. |
| Read-only audit control | Session `019fa9c2-177e-7823-89e9-65c7cce63d84`: requested the missing package, made no edits, and did not ask about verification mode. | Session `019fa9c2-177f-7342-854c-16c1b7764ef0`: preserved the same behavior. | Materially stable. |

The independent grader `/root/mode_new_prior/independent_grader` inspected the
outputs and source in a separate context. It found no material loss and limited
the result to a directional comparison. The frozen prior was commit `88c362e`
with `SKILL.md` SHA-256
`4693702db6766235049e34df7bf95baea77c1de24108307c09e0da5a809754fe`.

The tested `SKILL.md` SHA-256 for this behavior change was
`576ce3410270fffd81baa0bb7f8c4149a36fbb0e07a7700d1699776136175821`.
Structural validation passed. Skills CLI 1.5.20 installed an identical copy in
a fresh Codex project. In native session
`019fa9e3-c7dd-7be0-a749-05892984f6d4`, the agent selected and read that
installed skill, then asked the user to choose a verification mode. Because the
description was unchanged, the listing-query test was not rerun; the existing
evidence remains description-bound. The matched comparison and native run in
this historical follow-up targeted `gpt-5.6-sol` in Codex CLI 0.145.0. The
corresponding `claude-opus-5` behavior and native cells were unverified at this
package hash.

## 2026-07-28 pre-PR evidence-contract fixes

This follow-up closes the five evidence gaps found during pre-PR review while
keeping the deleted parallel follow-up files deleted. The canonical record
above now retains the supporting cases, excerpts, independent conclusions,
limits, and context references that remain relevant.

The matched comparison used frozen prior commit `949eddf` and the final
working-tree package hashes recorded in `baseline-cases.md`. Fresh Sol and Opus
executors evaluated both variants, then the separate fresh-context grader
`/root/prepr_fix_independent_grader` inspected the exact files and cases.

| Change | Result in both targets | Independent grade |
| --- | --- | --- |
| Routine listing pass rule | Both variants rejected an activating near-miss; the revised rule made the target-level failure direct. | Same final answer; clearer operational rule. |
| Loaded-copy provenance (historical rule) | Both variants kept unattributed native load unverified; the tested revision accepted path, hash, or distinctive-body evidence after collision inventory and rejected install identity alone. | Same final answer under the then-current rule; the stricter deterministic-provenance change below was not part of this run. |
| Revision-bound native evidence | Both variants treated earlier native evidence as inapplicable to the edited package; the revision made invalidation and rerun explicit. | Same final answer; direct invalidation rule. |
| Unavailable required target | Both variants withheld an overall directional conclusion; the revision closed the literal no-observed-loss loophole. | Same final answer; unavailable cells cannot qualify. |
| Unavailable listing judgment | Both variants returned `unverified`; the final rule made the three-state transition direct instead of inferential. | Same final answer; clearer operational rule. |
| Disposable installation | Only the revision defaulted to a disposable project and required approval for user-level or overwrite actions. | Intended delta observed. |
| Fully evidenced control | Expected listing and native states kept their separate pass eligibility and claim limits. | Materially stable. |
| Verification-mode control | Both variants asked before new-skill drafting and not during a findings-only audit. | Materially stable. |

No named invariant loss was observed. The combined comparison earns no
evidence label because five discriminating cases produced the same final
answer. The candidate decision is `Retained`: keep the explicit safeguards,
but do not claim overall behavioral improvement, non-regression, causal
improvement, or behavior outside the recorded cases.

The last natively tested package was commit `af7861b`. Structural validation
passed for that package with `skills-ref` 0.1.5. Skills CLI 1.5.20 found the
repository's four published skills, selected only `creating-portable-skills`,
and copied that package into both project-local destinations under disposable
workspace `<final-portable-skill-disposable-workspace>`. `diff -qr` returned no
differences for either installed package.

The final unavailable-listing edit reran its affected comparison cells. Fresh
Sol agents `/root/listing_unavailable_sol_final` and
`/root/listing_final_affected_controls_sol` and fresh Opus sessions
`a3d63c53-2d69-41e8-b189-0da2763ed4f4` and
`a5e27559-8046-43b0-942e-070869b7afe5` returned `unverified` for the missing
judgment, `failed` for the activating near-miss, and a stable pass-eligible
control with native states still separated. Independent grader
`/root/listing_unavailable_independent_grader` found the discriminating results
`same`, the control materially stable, and no invariant loss. This did not
raise the evidence label or candidate decision.

| Last natively tested package file (`af7861b`) | SHA-256 |
| --- | --- |
| `SKILL.md` | `7530e42fe64c306cc86f97c17b223dd1385ce3b9256a94b57b9708c2a93120df` |
| `assets/baseline-test-template.md` | `34865482c1c6bf4b7c05b5ddbb3af8b3dd11e57c8244d011d29ff0b7e4877270` |
| `assets/skill-template.md` | `e5cbfe744d93ba1c92c9a2a4dd97dbde00f51032ffe0563b95433683788f8458` |
| `assets/trigger-queries-template.md` | `ba79352f96e35c1d0c3ac2812335ca266887ad1ec11acde4b15b7aa5b03630c7` |
| `references/portability.md` | `83636d76ee143090ec33eff9affea1cd953a9601d441b4ef35e847e232dfeb8d` |
| `references/review-checklist.md` | `25fd4b36af18a891d03b3b1fa90ec907a94a114a630cb41a5e844b050a73d231` |

Same-name user copies existed in both `~/.agents/skills` and
`~/.claude/skills`, each with a different `SKILL.md` hash. Those historical
native checks therefore required exact loaded-copy attribution:

- Codex ran `gpt-5.6-sol` at high reasoning in fresh thread
  `019faa6c-4a59-7b01-a832-a44492b3b130`. The implicit creation request
  selected the skill and read
  `<final-portable-skill-disposable-workspace>/.agents/skills/creating-portable-skills/SKILL.md`,
  which supplied deterministic exact-path load provenance. Its distinctive
  first body sentence only corroborated that provenance.
- Claude Code 2.1.220 ran `claude-opus-5` at high effort in fresh session
  `6e03ff90-7bfe-48fe-afd3-587b9154a1bb`, with project settings and only the
  native `Skill` tool available. Initialization listed the project skill, the
  tool launched it, and the result identified
  `<final-portable-skill-disposable-workspace>/.claude/skills/creating-portable-skills/SKILL.md`
  as deterministic exact-path load provenance. The same sentence only
  corroborated that provenance.

For the `af7861b` package, local-source install and installed-content identity
passed for both package harnesses. Native discovery, load, and trigger passed
for the two separately declared native target cells at the hashes recorded
above. The safe-mode Opus cell belongs to the matched comparison and was not
used as native evidence.

| PR-head package file (`c9eb5e1`) | SHA-256 |
| --- | --- |
| `SKILL.md` | `1ba4b97ad9e5a9fcbb3d27e4e69070d46683716fdb29d959709ffe90bf99af0f` |
| `assets/baseline-test-template.md` | `3e36f320bf53870672daa2a6d7e59bdb52e2ff0542f4e43d13638d998be838cf` |
| `assets/skill-template.md` | `e5cbfe744d93ba1c92c9a2a4dd97dbde00f51032ffe0563b95433683788f8458` |
| `assets/trigger-queries-template.md` | `a486e99101002d5bf531bc62a9008c8e3f7ad9fff548712dd2ab412a6ee3a960` |
| `references/portability.md` | `83636d76ee143090ec33eff9affea1cd953a9601d441b4ef35e847e232dfeb8d` |
| `references/review-checklist.md` | `6baf044506a96c614d8cd14515f50942438e38e99b1269e351ec07d157307654` |

Substantive package edits after `af7861b` invalidated its package-harness and
native model-harness cells. The current hashes above were therefore rechecked
from the local source at `c9eb5e1`. Skills CLI 1.5.20 copied the package into
both project-local destinations under disposable workspace
`<post-review-portable-skill-disposable-workspace>`. `diff -qr` returned no
differences for either installed package.

Codex CLI 0.145.0 ran `gpt-5.6-sol` at high reasoning in fresh ephemeral thread
`019faaa7-f98c-7633-9457-7f4a1e3b28d0`. Its tool trace read the exact installed
`.agents/skills/creating-portable-skills/SKILL.md`. That exact path supplied
deterministic exact-path load provenance. The response asked for the
verification-mode decision; its first-body-sentence quote only corroborated
that provenance.
Claude Code 2.1.220 ran `claude-opus-5` at high effort in fresh
non-persistent session `5b144a80-c9fe-43ac-89ee-392ad3716d1c`, with project
settings and only the native `Skill` tool. Initialization listed the skill, the
tool launched it from the exact installed `.claude/skills` base directory. That
base directory supplied deterministic load provenance. The response asked for
the same first decision; its body-sentence quote only corroborated that
provenance.

For the `c9eb5e1` package, local-source install and installed-content identity
passed for both package harnesses. Native discovery, load, and trigger passed
for the declared `gpt-5.6-sol`/Codex and `claude-opus-5`/Claude Code cells. The
description did not change, so the existing complete listing-query results
remain the applicable description-bound evidence.

Claim Ceiling: these checks support the `c9eb5e1` package, the named harness
configurations, and the recorded native query. They do not establish behavior
for other revisions, models, harnesses, configurations, or tasks.

## 2026-07-28 current review-fix state

Review feedback changed three package resources after the `c9eb5e1` native
recheck. The current resource hashes are:

| Current package file | SHA-256 |
| --- | --- |
| `SKILL.md` | `1ba4b97ad9e5a9fcbb3d27e4e69070d46683716fdb29d959709ffe90bf99af0f` |
| `assets/baseline-test-template.md` | `1d6a33ed6686aadced84e920378f64e9a852fbaffda6c7bfabc57c03ea13c21f` |
| `assets/skill-template.md` | `e5cbfe744d93ba1c92c9a2a4dd97dbde00f51032ffe0563b95433683788f8458` |
| `assets/trigger-queries-template.md` | `ea30d1dbf024548c23ddfad2dab8d2e26b2e7f794ec44e65cf807ac58120a2ef` |
| `references/portability.md` | `28a862532a0ab0db75a8d0d47525bbd25ec47fe54f303fbd2726ab597157e84d` |
| `references/review-checklist.md` | `6baf044506a96c614d8cd14515f50942438e38e99b1269e351ec07d157307654` |

The description did not change. The final listing-query observations remain
applicable and pass the current public-tier rule because every near-miss in the
later full rerun received three categorical `no` judgments.

The resource edits invalidate the `c9eb5e1` package-harness and native
model-harness states for the current package. Local-source installation,
installed-content identity, native discovery, native load, and native trigger
are therefore **unverified** until the current package reruns. No native check
was attempted in this review pass; unavailable deterministic load provenance
is unverified, not failed. The changed evidence-contract wording also has no
new frontier matched comparison in this pass, so its behavioral effectiveness
remains unverified. Historical pass states above remain scoped to their exact
recorded package revisions and traces.
