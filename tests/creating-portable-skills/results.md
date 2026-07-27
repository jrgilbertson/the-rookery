# Acceptance evidence: creating-portable-skills

Recorded runs for the plan's Verification Contract (`docs/plans/2026-07-16-001-feat-creating-skills-plan.md` (the plan keeps its pre-rename filename as a point-in-time record)). Date: 2026-07-16. Tool versions this run: `skills-ref` 0.1.5, `skills` CLI 1.5.19, Codex CLI 0.144.4, Grok CLI 0.2.101, Claude Code (Fable 5 session; judge runs also on Haiku 4.5 and Sonnet).

## Gate results

| Gate | Result | Evidence |
| --- | --- | --- |
| Static validation | Pass | `npx skills-ref validate skills/creating-portable-skills` → "Valid skill", clean after every edit round |
| Line budget | Pass | `SKILL.md` at 107 lines (ceiling 500, target ~200) |
| Same-door sweep | Pass | Zero hits for home-directory paths and owner-environment identifiers across `skills/creating-portable-skills/` and `tests/creating-portable-skills/` |
| Historical 2026-07-16 install probe | Historical partial pass: local-source probe passed; remote probe (from jrgilbertson/the-rookery) remained pending post-merge (see caveat) | `npx skills add . --skill creating-portable-skills --agent claude-code --agent codex -g -y --copy` installed to both `~/.claude/skills/` and `~/.agents/skills/`; skill registered live in the running harness. This remote publication follow-up is non-gating for the 2026-07-27 final-source U4 result |
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

- **Historical 2026-07-16 remote publication follow-up (non-gating for the 2026-07-27 final-source U4 result).** `npx skills add jrgilbertson/the-rookery` scans the default branch; skills CLI 1.5.19's `@ref` targeting clones but does not check out the requested ref (verified against both a branch name and a commit SHA), so the branch-ref workaround does not work. The plain remote probe was deferred until the change reached `main`.
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

### Final 2026-07-27 state

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
behavior outside the recorded cases. The remote default-branch install probe
remains a post-merge publication confirmation and is not used as pre-merge
evidence.

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
