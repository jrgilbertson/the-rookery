# Acceptance evidence: creating-portable-skills

Recorded runs for the plan's Verification Contract (`docs/plans/2026-07-16-001-feat-creating-skills-plan.md` (the plan keeps its pre-rename filename as a point-in-time record)). Date: 2026-07-16. Tool versions this run: `skills-ref` 0.1.5, `skills` CLI 1.5.19, Codex CLI 0.144.4, Grok CLI 0.2.101, Claude Code (Fable 5 session; judge runs also on Haiku 4.5 and Sonnet).

## Gate results

| Gate | Result | Evidence |
| --- | --- | --- |
| Static validation | Pass | `npx skills-ref validate skills/creating-portable-skills` → "Valid skill", clean after every edit round |
| Line budget | Pass | `SKILL.md` at 107 lines (ceiling 500, target ~200) |
| Same-door sweep | Pass | Zero hits for home-directory paths and owner-environment identifiers across `skills/creating-portable-skills/` and `tests/creating-portable-skills/` |
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
| Listing proxy | passed in both target cells | Full tables in `trigger-queries.md`; 10/10 should-trigger at 3/3 `yes` in each target and zero near-miss `yes`; Opus recorded two `unsure` judgments on one near-miss |

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

Both native runs returned the exact first body sentence:
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
workspace `/tmp/rookery-frontier-retune.YP9X0t/final-install.tQBkI2`:

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
| Native trigger | passed; the final included the exact first body sentence | passed; the final included the exact first body sentence |

The exact sentence observed in both finals was:
`Create or revise a skill from its intent, hard constraints, authority
boundaries, success criteria, and output contract.`

### U2 template-instantiation verification

At disposable root `/tmp/rookery-template-instantiation.NYOZiH`, the current
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
npx skills-ref validate /tmp/rookery-template-instantiation.NYOZiH/template-instantiation-smoke
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
| Listing proxy | passed in both target cells |
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
record of the per-case conclusions.

| Case | Prior | Revised | Independent conclusion |
| --- | --- | --- | --- |
| Grading policy discriminator | Said the workflow did not require a separate independent grader | Required a fresh grader independent of the author and artifact producers, direct artifact and trace inspection, evidence for every pass, review of weak checks, human or blind review for subjective qualities, and an unverified handoff when an independent context is unavailable | Intended delta observed |
| Mechanical-validation control | Kept `skills-ref` and manual checks script-driven without a separate reviewer | Preserved the same decision and mechanism | Materially stable |

The grader found no observed loss in the two supplied answers. It limited the
result to a directional comparison and noted that policy recall does not prove
artifact-level compliance.

An artifact-level probe tested that limitation. The executor summary claimed a
report passed, while the report contained only a heading and one unsupported
recommendation, and the trace admitted that `incidents.csv` was not opened.
`artifact_grade_prior` and `artifact_grade_revised` both rejected the claimed
pass, cited the artifact and trace, and identified the filename and heading
checks as insufficient. `artifact_comparison_reviewer` judged the result
materially the same. This probe shows correct behavior for one case. It does
not establish general reliability or non-regression.

Structural validation passed:

```text
npx skills-ref validate skills/creating-portable-skills
Valid skill: skills/creating-portable-skills
```

Skills CLI 1.5.20 installed the local source into fresh project-local Codex and
Claude Code destinations under `/tmp/rookery-surgical.zLTYcU/project`.
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
`/private/tmp/rookery-writing-skills-final2.Wnsy5N`. `diff -qr` reported no
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

The read-only audit, generated trigger contract, evidence-doctrine, and
single-owner cases showed their intended deltas. The resource-placement control
remained materially stable. The result is a **directional comparison** for those
named cases only. It does not establish general reliability, causal improvement,
non-regression, or behavior outside the recorded cases and target
configurations.

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

The tested `SKILL.md` SHA-256 for this behavior change was
`576ce3410270fffd81baa0bb7f8c4149a36fbb0e07a7700d1699776136175821`.
Structural validation passed. Skills CLI 1.5.20 installed an identical copy in
a fresh Codex project. In native session
`019fa9e3-c7dd-7be0-a749-05892984f6d4`, the agent selected and read that
installed skill, then asked the user to choose a verification mode. Because the
description was unchanged, the listing-query test was not rerun; the existing
evidence remains description-bound.
