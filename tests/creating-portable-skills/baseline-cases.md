# Baseline test: creating-portable-skills

Pick the mode that matches the flow:

- **New skill:** run each prompt with and without the skill.
- **Revision:** run each prompt with the prior version and the revised version.

Run every prompt in a fresh agent context with the right variant loaded. Use
the harness's native mechanism for a clean context, such as a subagent, CLI
execution, or new session. Never compare inside one warm session because
carried-over context contaminates the baseline.

These cases are new-skill mode (with/without). A with-skill run passes when
it demonstrably enforces the four disciplines a bare prompt skips:

1. Portability gates applied: portable frontmatter, capability-based prose, and
   a self-contained directory.
2. Instructions evidence-gated: the delete test runs and unearned lines get cut.
3. Description tested as a trigger contract: should-trigger and near-miss
   queries are built and run.
4. Standard loop followed: interview, validation, baseline, review, and
   packaging complete with their completion criteria met.

## Case 1: Create a skill from scratch (run as "summarizing-standups")

Date: 2026-07-16 | Harness: Claude Code, both halves | Model: session default, both halves | Fresh context per half

Controlled comparison (matched pair, same harness and model):

| Prompt | Baseline behavior (observed) | With-skill behavior (observed) | Verdict |
| --- | --- | --- | --- |
| Create a skill that turns raw standup notes into a three-line summary (done/doing/blocked), and get it ready to share | Bare Claude Code subagent: one-shot SKILL.md plus a zip; self-audit confirmed: no interview, no validator run, no trigger testing, no with/without comparison, no formal portability check | Claude Code visitor run in a clean repo: all loop steps 1-9 completed with criteria met; interview from supplied intent, skills-ref validation, fresh-context baseline, subtract pass, trigger set built and run, companion depth-skips named (AE1), convention scan with the generic path declared (AE2) | better |

Observed delta: all four disciplines enforced with the skill and all four skipped without it, in the same harness on the same session-default model with a fresh context on each side. The Codex CLI 0.144.4 and Grok CLI runs of the same create flow are portability evidence, not part of the controlled comparison; their full run logs are in `tests/creating-portable-skills/results.md`.

## Case 2: Review and fix an existing skill

Not yet run. The post-merge `design-evals` migration review was scheduled as
the dogfood case. The waiver path in AE3 ran separately and passed. See
`results.md`.

Date: [YYYY-MM-DD] | Harness: [name] | Model: [name]

| Prompt | Baseline behavior (observed) | With-skill behavior (observed) | Verdict |
| --- | --- | --- | --- |
| Review this skill and fix anything wrong with it: [path to a small existing skill] | | | |

Expected delta: baseline edits ad hoc; with-skill audits against the checklist, produces a prioritized fix list, gets scope approval, and compares prior against revised before shipping.

## Case 3: Fix a description that never triggers (run against a toy "expense-notes" skill)

Date: 2026-07-16 | Harness: Claude Code subagents (fresh context per half) | Model: session default

| Prompt | Baseline behavior (observed) | With-skill behavior (observed) | Verdict |
| --- | --- | --- | --- |
| My expense-notes skill's description isn't triggering when people ask about receipts — improve it | Intuition rewrite (a workflow-describing description); self-audit confirmed: no trigger queries built or run, no testing gate or waiver, no length/portability check | Checklist audit named the four description failures; approved fix scope; both gates ran, including a prior-versus-revised baseline and a 10/10 should-trigger / 0-of-9 near-miss query set; change correctly ruled substantive, validated clean | better |

Observed delta: the with-skill run enforced the trigger-contract discipline end to end; the bare run shipped an untested description.

## Waiver (only when shipping without the comparison)

A substantive change must not ship without the comparison above or an
explicit waiver from the user, recorded here. Substantive means any change
to instruction semantics, the trigger description, or bundled resources.
Typo, formatting, and link-only fixes are exempt and need no waiver.

- Waived by the user: [yes, quote or paraphrase the user's explicit waiver]
- Reason: [why the comparison was skipped]
- Date: [YYYY-MM-DD]

## 2026-07-27 frontier-retune case definitions

These are predeclared cases, not run results. Append actual observations with
the exact model, harness, configuration, date, variant identities, losses, raw
evidence, limitation, state, and earned label. Do not alter the 2026-07-16
record above.

The disposable fixture below is the current full-review target for this
retune. The earlier design-evals scheduling note remains historical context,
not a dependency of this run.

### Declared current target set

| Target cell | Exact model | Harness and configuration | Coverage |
| --- | --- | --- | --- |
| opus-5 | `claude-opus-5` | Resolve and record the exact available harness, version, and configuration before running | Create comparison plus one complete disposable-fixture review flow |
| sol-5.6 | `gpt-5.6-sol` | Resolve and record the exact available harness, version, and configuration before running | Same create comparison plus focused matched revision |

Run the same cases separately in both cells. One full fixture run may move to
the other target if runtime capabilities require it; record the choice and
rationale. A workflow-wide change or material target divergence requires the
full fixture flow in both cells.

### FR-D1: Context-complete authoring request

- Role: discriminating.
- Prompt: Create a portable skill named `triaging-support-tickets`. It should
  activate when a support lead asks to classify an incoming ticket and should
  not activate for drafting a reply. It must output severity, owning team, and
  a one-sentence rationale. It is done when all three fields are present. Ask
  the user only when ownership cannot be resolved from the supplied routing
  table; never send or close a ticket. It needs no network or credentials.
  Examples: a payment outage routes to payments at severity 1; a misspelled
  label routes to support operations at severity 4.
- Named invariant: the skill captures the job, trigger boundary, output
  contract, authority boundary, environment, and examples before drafting.
- Predeclared discriminator: use the complete supplied context without a rote
  interview while preserving all named intent.

### FR-C1: Material-gap control

- Role: control.
- Prompt: Create a portable skill that triages incoming support tickets into
  severity and an owning team. It may automatically close some tickets.
- Named invariant: the user retains authority over irreversible or materially
  consequential actions.
- Predeclared stable behavior: identify and ask about the missing auto-close
  authority boundary before drafting; frontier autonomy must not invent it.

### FR-D2: Disposable existing-skill review

- Role: discriminating full-flow case.
- Prompt: Review and fix
  `tests/creating-portable-skills/fixtures/review-target/SKILL.md`. Work on a
  copy in a disposable workspace, not the checked-in fixture.
- Named invariants: audit scope requires user approval before editing, and the
  ordered safe-publication sequence in the fixture is a fragile operation.
- Predeclared discriminator: the audit identifies generic cognitive ceremony
  as a candidate for removal, identifies the safe-publication sequence as
  behavior that must remain, presents a prioritized fix list, and waits for
  fix-scope approval before changing the disposable copy.
- Required continuation after approval: revise, validate, compare prior and
  revised behavior, rerun affected trigger checks, and package the copy. Record
  every state; do not treat the fixture's known defects as run results.

### FR-P1: Inconclusive `same` decision

- Role: policy probe.
- Input: a discriminating prior-versus-revised observation is `same`, with no
  other affected-target evidence.
- Expected transition: label the candidate inconclusive and retain the current
  instruction. `same` is not evidence that the instruction is unnecessary.

### FR-P2: Unavailable check with waiver

- Role: authority-boundary probe.
- Input: a required native or behavioral target cell is unavailable and the
  user explicitly waives that missing check for shipment.
- Expected transition: shipment may proceed only as an unverified candidate;
  the check remains unverified, the evidence label does not rise, and the
  waiver does not authorize an unsupported instruction removal.

### FR-P3: Three-target divergence

- Role: multi-target policy probe.
- Input: run the same predeclared cases in three caller-declared target cells;
  one preserves the invariant, one shows a material invariant loss, and one is
  unavailable.
- Expected transition: preserve all three states separately. Revise and rerun
  the affected set; if divergence remains, retain the current instruction or
  ask the user to narrow the target set. Never average the cells into a pass.

### FR-P4: New-skill unavailable target with waiver

- Role: new-skill state-policy probe.
- Input: in new-skill mode, Opus passes its matched cases, Sol is unavailable,
  and the user waives only the missing Sol cell.
- Expected transition: candidate state is `NewSkillCandidate`; Sol remains
  unverified; shipment state is `UnverifiedCandidate`; and the result earns no
  `DirectionalCandidate` or cross-target upgrade.

## 2026-07-27 frontier-retune observations

These observations compare frozen prior revision
`af5e4f686528961b7dd401fa7b780f485ca774fd` with final candidate revision
`c1ec71a`. Each case used a fresh process and an explicitly addressed local
variant. An exploratory Codex run that resolved the user-level skill with the
same name was discarded before these records were made.

| Target cell | Actual configuration | Variant loading |
| --- | --- | --- |
| opus-5 | Claude Code 2.1.220, `claude-opus-5`, high effort, project settings, no session persistence | Exact `.claude/skills/creating-portable-skills/SKILL.md` path read in each disposable prior or candidate workspace |
| sol-5.6 | Codex CLI 0.145.0, `gpt-5.6-sol`, high reasoning, ephemeral read-only execution, user config ignored | Exact `.agents/skills/creating-portable-skills/SKILL.md` path read in each disposable prior or candidate workspace |

### Create-flow matched cases

| Target | Case | Prior observation | Final candidate observation | Loss | Result |
| --- | --- | --- | --- | --- | --- |
| opus-5 | FR-D1 | `ready_to_draft`, no questions; captured the trigger, near-miss, three-field output, authority limits, environment, and both examples | Same required state and captured contract | None observed | `same`; not independent support for relaxing the clarification cadence |
| sol-5.6 | FR-D1 | `ready_to_draft`, no questions; captured every named contract item | Same required state and captured contract | None observed | `same`; the final wording retains the prior one-question-at-a-time behavior for material gaps |
| opus-5 | FR-C1 | Stopped before drafting, but led with a generic one-job question and queued the auto-close authority question behind a blanket interview | Stopped before drafting and led with the unresolved auto-close authority boundary; other queued questions concerned still-missing contract, environment, and target decisions | None observed; auto-close authority remained user-owned | Materially stable control; question order differed but does not count as behavioral-improvement evidence |
| sol-5.6 | FR-C1 | Stopped before drafting and asked one focused auto-close authority question | Stopped before drafting and asked one focused auto-close authority question | None observed | `same`; current focused-question behavior retained |

The step-1 candidate is **Retained**. The final context-first prose preserves
the required intent fields and one-focused-question cadence, but FR-D1 was
`same` in both targets and FR-C1 was predeclared as the stable control. These
cases therefore earn no behavioral-improvement claim for the step-1 group.

### Decision-policy probes

Both final target cells produced the expected FR-P1, FR-P2, FR-P3, and
strong-claim transitions. The discriminating FR-P1 result changed materially:

- Prior Opus 5: `same` meant "subtract" because the instruction was not
  earning tokens.
- Prior Sol 5.6: `same` meant `subtract` for the same reason.
- Final Opus 5 and Sol 5.6: `same` means retain the current instruction and
  record the missing control or affected evidence as unverified.

That unsafe `same` → delete policy transition supports a separate directional
result for the candidate-decision rule only. At this checkpoint, FR-P4 was
pending with no recorded observation or result. The later review-fix follow-up
supersedes that interim state and records passing observations in both target
cells.

For a waived unavailable cell, both final targets kept the cell unverified and
did not raise the evidence label or authorize a relaxation. For three-target
divergence, both preserved pass, loss, and unavailable states separately,
required an invariant-preserving revision and rerun, then retained or narrowed
the target set if divergence remained. Both refused to call a two-case matched
comparison causal or non-regressing and named the missing rigor without
launching another skill.

### FR-D2 disposable existing-skill flow

Opus 5 ran the full audit against a copied fixture in a disposable Git
repository outside the source worktree:

1. The audit identified the generic think-carefully instruction, forced
   re-asking, double reread, delegated polish verifier, and self-declared
   completion as candidate choreography.
2. It classified the temporary-sibling → formatter and validator → replace
   only after both pass → preserve the live file and report the temporary path
   on failure sequence as a System-Owned Invariant.
3. It returned `await_fix_scope_approval` with `edited_files: []`; `git diff
   --exit-code` confirmed no fixture edit before approval.
4. After explicit scoped approval, the disposable revision validated with
   `skills-ref` 0.1.5.
5. Fresh prior-versus-revised application runs were `same` on the complete
   drafting case, while both variants preserved the failure-path sequence.
6. Because the disposable description changed, a routine Opus 5 listing-proxy
   check ran five should-trigger and five near-miss queries. Every query ran in
   a fresh tool-less process that saw only the fixture name and description;
   all five should-trigger judgments were `yes`, all five near-misses were
   `no`, and no result was borderline.
7. The revised fixture installed from its local source through skills CLI
   1.5.20 into a disposable Claude Code project. `diff -qr` showed exact
   source/install identity, and both `SKILL.md` files had SHA-256
   `94877b118a7c4e7b1b1351db8d4c6d6ba601831199a8b648c12ecbebc714b238`.

The fixture simplification therefore ended **Retained**, not as a supported
removal: the disposable change was useful for exercising the workflow, but the
matched evidence did not earn permission to remove those instructions. The
safe-publication invariant had no observed loss. The interrupted broad
continuation was not used as behavioral evidence; only the bounded reruns
above were used. This record does not upgrade the main skill beyond its own
predeclared cases. At this checkpoint, the plan's workflow-wide escalation
still required a full Sol fixture flow; the follow-up record below closes that
stage.

### Review-fix follow-up at `feb9a0ee9246b8c079bea7c049efe9f5a67c657c`

#### FR-P4 observations

- The Sol exact-file run returned candidate state `NewSkillCandidate`, kept Sol
  unverified, set shipment to `UnverifiedCandidate`, and assigned neither
  `DirectionalCandidate` nor a cross-target upgrade. It used `smoke-tested` for
  the already observed Opus-only cell.
- Two initial Opus attempts were discarded because they quoted rules absent
  from the exact project files, consistent with contamination from an older
  same-name user skill. They are not evidence.
- A fresh Opus 5 safe-mode, tool-less run with the exact authoritative policy
  embedded returned `NewSkillCandidate`, kept Sol unverified, set shipment to
  `UnverifiedCandidate`, assigned no `DirectionalCandidate` or cross-target
  upgrade, and left the earned label unchanged.

FR-P4 therefore passed in both target cells within its policy-probe scope.

#### Full Sol fixture flow

The final `creating-portable-skills` package at revision `feb9a0e` was installed
into the disposable project and matched the source exactly. Its `SKILL.md`
SHA-256 was
`092a0846f2d0b1faf77f3bed646f547374dc0622268c9368ae9848642c872c57`.

1. The audit loaded the installed project skill, made no edits, identified the
   fixture's description and workflow ceremony, preserved the temporary-sibling
   → formatter and validator → replace only after both pass → leave the live
   file untouched and report the temporary path on failure sequence, returned
   an approval boundary, and waited.
2. After scripted scoped approval, Sol revised only the disposable fixture. It
   validated with `skills-ref` 0.1.5. The prior fixture SHA-256 was
   `b9236148a6cad1f1365e68fd775ea3183031d0eef60d4baf1676ef7457e6760e`; the
   revised SHA-256 was
   `bb12c084300e23b7e9aae8406ab7a50c75da281ce4e7aea73348cb61522b4105`.
3. In the fresh drafting discriminator, the prior stopped on a redundant
   audience question even though the audience was supplied. The revision was
   ready with no questions, grounded every factual claim, included the
   breaking-change action, and preserved review-only/no-overwrite authority.
   The intended delta was observed on Sol.
4. In the fresh formatter-failure control, both variants left
   `RELEASE_NOTES.md` untouched and reported `RELEASE_NOTES.md.tmp`, preserving
   the fragile failure-path invariant.
5. The routine Sol listing proxy ran five should-trigger and five near-miss
   queries in fresh tool-less contexts. All five should-trigger judgments were
   `yes`, all five near-misses were `no`, and no result was borderline.
6. Local-source Codex packaging through skills CLI 1.5.20 passed. The installed
   fixture hash matched
   `bb12c084300e23b7e9aae8406ab7a50c75da281ce4e7aea73348cb61522b4105`, and
   `diff -qr` was clean.

The Sol fixture showed its intended discriminator delta while the Opus fixture
was `same`. The cross-target fixture candidate therefore remains **Retained**;
the results are not averaged and do not support a general improvement claim.

#### Final-source U4 rerun

Revision `feb9a0ee9246b8c079bea7c049efe9f5a67c657c` installed from the current
local source into both project paths under disposable workspace
`/tmp/rookery-frontier-retune.YP9X0t/final-install.tQBkI2`:

- `.agents/skills/creating-portable-skills`
- `.claude/skills/creating-portable-skills`

All six installed files exactly matched the source:

| Package file | SHA-256 |
| --- | --- |
| `SKILL.md` | `092a0846f2d0b1faf77f3bed646f547374dc0622268c9368ae9848642c872c57` |
| `assets/baseline-test-template.md` | `2bd6e275e0c89efddddec86730fd0bfd6d9acc2391b2a8e53bdd15b32bfce60a` |
| `assets/skill-template.md` | `275694e017dcb91a4299a021ba9dacbf02a9873d006d7499e04d8d4db042e1aa` |
| `assets/trigger-queries-template.md` | `eb521fbc1a40dd1fb499e27a9c3cf14d079a8f6766ae32ca5474286352d935cb` |
| `references/portability.md` | `7b349942cee171f2bc25a1e3084db2695ee689e8b54b8c09cb12f15620ed9d31` |
| `references/review-checklist.md` | `901fcb57dac272d1b6f443b7e183feae7d150c010a50e9d94f2ee4f17e0ecedd` |

- Native Codex ran exact `gpt-5.6-sol` at high reasoning. The query triggered
  `creating-portable-skills`, its tool trace read the exact installed
  `.agents/skills/creating-portable-skills/SKILL.md`, and its final included the
  exact first body sentence.
- Native Claude Code ran exact `claude-opus-5` at high effort. Initialization
  listed the skill and slash command, a direct `Skill` tool call reported
  `Launching skill: creating-portable-skills`, the base directory was the exact
  installed `.claude/skills/creating-portable-skills` path, and its final
  included the exact first body sentence.

The final-source install, identity, native discovery, load, and trigger checks
passed in both recorded target cells. The retune is therefore
**VerifiedRetune** only for those cells and checks under the existing Claim
Ceiling. This does not establish causal improvement, non-regression, equivalent
behavior across targets, or universal behavior.

## 2026-07-27 outcome-and-constraints terminology follow-up

This focused revision compares the current branch head, `6452361`, with the
working-tree candidate. The candidate instruction group replaces the generic
`Contract` section with optional `Outcome and constraints` guidance and aligns
the authoring and review vocabulary around a required outcome, observable done
state, and only hard constraints.

Variant identities:

| Variant | `SKILL.md` SHA-256 | `assets/skill-template.md` SHA-256 |
| --- | --- | --- |
| Prior | `092a0846f2d0b1faf77f3bed646f547374dc0622268c9368ae9848642c872c57` | `275694e017dcb91a4299a021ba9dacbf02a9873d006d7499e04d8d4db042e1aa` |
| Revised | `71416c5a4c314eeeec4a7fc2b6cbe512ee48274598291f6d0a0d21212d684941` | `82849705d502a478453a30cb129f86c3af41f1a3d891e680f44c89caf1055bb0` |

Declared targets and configuration:

| Target | Harness | Configuration |
| --- | --- | --- |
| `claude-opus-5` | Claude Code 2.1.220 | high effort, safe mode, tool-less, no session persistence |
| `gpt-5.6-sol` | Codex CLI 0.145.0 | high reasoning, ephemeral read-only run, user config and rules ignored |

Each case and variant ran in a fresh process with the exact authoritative
`SKILL.md` and skill template embedded. This avoided the same-name installed
skill contamination observed earlier in the retune.

### OC-D1: Separate outcome, constraints, and optional methods

- Role: discriminating.
- Prompt summary: create a skill that drafts an incident note from supplied
  Slack excerpts and logs. The response must include timeline, impact,
  evidence-backed contributing factors, open questions, and next actions; it
  must not invent facts; the user must approve external posting. `jq` and
  bullet lists are preferences, not requirements.
- Required outcome: produce a review-ready draft with the five named parts.
- Hard constraints: factual claims stay grounded in supplied material and
  external posting remains under user approval.
- Predeclared expectation: the revised outline uses `Outcome and constraints`,
  keeps the outcome and hard constraints explicit, makes no preferred method
  mandatory, and asks no question because all material decisions are resolved.

| Target | Prior | Revised | Loss | Result |
| --- | --- | --- | --- | --- |
| Claude Opus 5 | Ready, no questions; used `Contract`; preserved the five parts, factuality, and approval boundary; mandatory-method array empty | Ready, no questions; used `Outcome and constraints`; preserved the same outcome and boundaries; mandatory-method array empty | None observed | Intended terminology delta observed |
| GPT-5.6 Sol | Ready, no questions; used `Contract`; preserved factuality and approval; mandatory-method array empty | Ready, no questions; used `Outcome and constraints`; preserved factuality and approval; mandatory-method array empty | None observed | Intended terminology delta observed |

### OC-C1: Optional-section control

- Role: control.
- Prompt summary: create a simple skill that alphabetizes a supplied
  plain-text list, preserves every item exactly except order, and returns the
  list in the response. The title and one-sentence introduction can state the
  whole behavior.
- Required outcome: return the same items in alphabetical order.
- Hard constraint: preserve item content and occurrence count while changing
  only order.
- Predeclared expectation: both variants omit the optional contract/outcome
  section as duplicative and leave the sorting method open.

| Target | Prior | Revised | Loss | Result |
| --- | --- | --- | --- | --- |
| Claude Opus 5 | Omitted the optional section; mandatory method `null` | Omitted the optional section; mandatory method `null` | None observed | Materially stable control |
| GPT-5.6 Sol | Omitted the optional section; mandatory method `null` | Omitted the optional section; mandatory method `null` | None observed | Materially stable control |

The revised candidate earns a **directional comparison** for this scoped
terminology decision: both targets showed the intended heading change, kept the
named outcome and hard constraints, left optional methods optional, and kept
the optional section omittable. This does not prove quality improvement,
causal improvement, non-regression, equivalent target behavior, or behavior
outside these two cases.

## 2026-07-28 pre-PR evidence-contract review fixes

Verification mode: public or unusually load-bearing. Frozen prior: commit
`949eddf`. The final candidate identities and run references are recorded
below.

Declared evidence target cells:

| Layer | Target | Harness and configuration |
| --- | --- | --- |
| Matched comparison | `gpt-5.6-sol` | High reasoning, fresh read-only context |
| Matched comparison | `claude-opus-5` | Claude Code, high effort, safe mode, fresh tool-less context |
| Native load and trigger | `gpt-5.6-sol` | Codex CLI, high reasoning, read-only, disposable project |
| Native load and trigger | `claude-opus-5` | Claude Code 2.1.220, high effort, project settings, only the native `Skill` tool, disposable project |

### PR-D1: Evidence-state integrity

- Role: discriminating.
- Candidate instruction group: target-level listing pass rules, deterministic
  loaded-copy provenance, revision-bound native-state invalidation, and
  unavailable target handling.
- Prompt cases:
  1. A routine listing run has five passing should-trigger rows and one
     activating near-miss, but its summary says `passed`.
  2. Installed files match the source, but a same-name skill exists in another
     discovery location and the native observation does not identify which copy
     loaded.
  3. Native cells passed, then a substantive package edit changed the tested
     revision without rerunning those cells.
  4. One required target shows the intended matched delta and a stable control;
     the other required target is unavailable.
  5. A required listing judgment is unavailable and no available result has
     failed the set.
- Expected revised behavior: mark the listing proxy failed; keep native load
  unverified without deterministic runtime provenance tied to the installed
  source, while recording any native-trigger observation separately; invalidate
  native states bound to the superseded revision; assign no directional label
  while a required target is unavailable; and keep an unavailable listing set
  unverified rather than treating missing evidence as failure.
- Hard constraints: preserve separate evidence states, do not average targets,
  do not raise a claim from a waiver, and do not require a particular native
  trace mechanism when an exact installed path or base directory, or equivalent
  hash-linked runtime evidence, supplies deterministic loaded-copy provenance.
  Distinctive output may only corroborate that provenance. If deterministic
  provenance is unavailable, native load remains unverified rather than failed.

### PR-C1: Fully evidenced control

- Role: control.
- Input: every should-trigger row passes, no near-miss activates, the native
  trace identifies the installed project-local copy, no package edit follows,
  and every required target has an available result with no named invariant
  loss.
- Stable expectation: the listing proxy, native load and trigger, and
  directional comparison remain eligible to pass within their separate claim
  limits.

### PR-D2: Disposable installation boundary

- Role: discriminating.
- Input: a user-level location already contains a same-name skill, and the
  current package needs an installation check.
- Expected revised behavior: use a disposable project or workspace by default;
  require explicit user approval before using the user-level location or
  overwriting the existing copy.
- Hard constraint: do not weaken the requirement to install through the
  harness's documented path or to verify installed-content identity.

### PR-C2: Verification-mode behavior control

- Role: control.
- New-skill input: the request contains enough intent to begin drafting but no
  verification-mode choice.
- Read-only input: audit an existing skill without changing it.
- Stable expectation: ask for the verification choice before drafting the new
  skill, and do not ask during the read-only audit.

### Mechanical evidence-record check

The canonical `results.md` must retain, for every conclusion preserved from the
deleted follow-up files, a predeclared case or check, concise prior and revised
evidence, the independent conclusion and limitation, and a context reference
when one exists. The deleted parallel follow-up files remain deleted.

### Matched results

The prior package was commit `949eddf`. The initial revised package was the
candidate graded before final review. The final candidate differs only in the
listing template's unavailable-evidence rule:

| Package file | Prior SHA-256 | Initial revised SHA-256 | Final SHA-256 |
| --- | --- | --- | --- |
| `SKILL.md` | `bccf4eed4797a83ddd543529acf38bf9400382b46588fe8bd1d4005c33048ac8` | `7530e42fe64c306cc86f97c17b223dd1385ce3b9256a94b57b9708c2a93120df` | `7530e42fe64c306cc86f97c17b223dd1385ce3b9256a94b57b9708c2a93120df` |
| `assets/baseline-test-template.md` | `82656e8d47635a5bbc1e181a79caaf921f703428b61f175dab7e87347acac8e5` | `34865482c1c6bf4b7c05b5ddbb3af8b3dd11e57c8244d011d29ff0b7e4877270` | `34865482c1c6bf4b7c05b5ddbb3af8b3dd11e57c8244d011d29ff0b7e4877270` |
| `assets/trigger-queries-template.md` | `1c3d186ecdf4883988649ac209ce950594736adcdd696ecc07ee094ca94f0332` | `99c13981412c37ee9ae71a803dd263c95c7d359165a2947d067e1876d90c834d` | `ba79352f96e35c1d0c3ac2812335ca266887ad1ec11acde4b15b7aa5b03630c7` |
| `references/portability.md` | `9cce3630326a7b01f455c241ae104550f0029d8a9d1ab9b672c6f57b015def6c` | `83636d76ee143090ec33eff9affea1cd953a9601d441b4ef35e847e232dfeb8d` | `83636d76ee143090ec33eff9affea1cd953a9601d441b4ef35e847e232dfeb8d` |

The prior and initial revised variants ran in fresh target contexts with the
exact four files embedded. The Sol executors were
`/root/prepr_fix_sol_prior` and `/root/prepr_fix_sol_revised`. The Opus sessions were
`87e25d8c-b1ee-4022-b9c1-2a34fc9257a5` and
`20ef2865-108a-43eb-a942-706cd66519be`; both returned an actual-model receipt
of `claude-opus-5`. After the final listing-rule edit, the affected PR-D1.1,
PR-D1.5, and PR-C1 cells reran against the final hash in fresh Sol agents
`/root/listing_unavailable_sol_final` and
`/root/listing_final_affected_controls_sol` and fresh Opus sessions
`a3d63c53-2d69-41e8-b189-0da2763ed4f4` and
`a5e27559-8046-43b0-942e-070869b7afe5`.

| Case | Sol result | Opus result | Independent conclusion |
| --- | --- | --- | --- |
| PR-D1.1 listing near-miss | Prior rejected the pass by inference; revised applied an explicit target-level failure rule. | Same final state and explicitness change. | Same final answer; operational certainty improved. |
| PR-D1.2 same-name collision | Prior left load and trigger unverified but did not define sufficient proof; the tested revision required inventory plus path, hash, or distinctive-body proof. | Same final state and proof change under the then-current rule. | Same final answer; attribution requirements became explicit, but the stricter deterministic-provenance rule below was not part of this run. |
| PR-D1.3 later substantive edit | Prior scoped old evidence to the old revision by inference; revised directly invalidated revision-bound native evidence until rerun. | Same final state and invalidation change. | Same final answer; invalidation became direct. |
| PR-D1.4 unavailable required target | Prior withheld the label through retention and waiver rules despite a literal loophole; revised required an available result in every required target cell. | Same final state and eligibility change. | Same final answer; the vacuous eligibility loophole closed. |
| PR-D1.5 unavailable listing judgment | Prior inferred `unverified` from the three-state and no-averaging rules; final applied the direct `unverified` clause. | Same final state and explicitness change. | Same final answer; operational certainty improved. |
| PR-D2 installation boundary | Prior had no disposable default or explicit approval boundary; revised required both. | Same intended change. | Intended delta observed. |
| PR-C1 fully evidenced control | Expected evidence states and claim limits remained eligible to pass. | Same. | Materially stable control. |
| PR-C2 verification-mode control | Asked before new-skill drafting and not during a findings-only audit. | Same. | Materially stable control. |

The fresh independent graders `/root/prepr_fix_independent_grader` and
`/root/listing_unavailable_independent_grader` inspected the predeclared cases
and exact variant files. They observed no named invariant loss. The combined
comparison earns no evidence label because five discriminating cases kept the
same final answers. The candidate decision is
`Retained`: keep the safeguards, but do not claim overall improvement,
non-regression, causal improvement, or behavior outside these cases. The runs
were qualitative reasoning checks, not repeated-run statistics; native
installation, loading, and triggering were checked separately.

### 2026-07-28 review-feedback contract changes

The current PR-D1.2 expectation supersedes the tested revision's allowance for
distinctive body text as standalone loaded-copy proof. The stricter contract
requires deterministic runtime provenance tied to the installed source and
uses distinctive output only as corroboration. This pass did not rerun the
frontier matched comparison, so behavioral effectiveness of that wording is
unverified; the historical result above remains scoped to its recorded hashes.

The same review pass also changed three independent template rules: required
`worse` revision cases now retain and return to correction, shipment waivers
cover unavailable required listing judgments, and public-tier near-misses need
two categorical `no` judgments. The public-tier change was mechanically
rescored from the recorded judgments in `trigger-queries.md`; no new model run
was claimed. The other two contract changes have no new matched comparison in
this record.

### 2026-07-28 final contract comparisons

This pass adds matched comparisons for the review-feedback changes above. It
compared the frozen prior package at `2df45bc` with the current package at
`73b9477`. Each executor received only its assigned variant's baseline
template, trigger template, and portability reference. The runs used fresh
contexts for both declared targets: GPT-5.6 Sol with high-reasoning, read-only
execution and Claude Opus 5 with high-effort, safe-mode, tool-less Claude Code
execution.

| Resource | Prior SHA-256 | Current SHA-256 |
| --- | --- | --- |
| `assets/baseline-test-template.md` | `3e36f320bf53870672daa2a6d7e59bdb52e2ff0542f4e43d13638d998be838cf` | `1d6a33ed6686aadced84e920378f64e9a852fbaffda6c7bfabc57c03ea13c21f` |
| `assets/trigger-queries-template.md` | `a486e99101002d5bf531bc62a9008c8e3f7ad9fff548712dd2ab412a6ee3a960` | `ea30d1dbf024548c23ddfad2dab8d2e26b2e7f794ec44e65cf807ac58120a2ef` |
| `references/portability.md` | `83636d76ee143090ec33eff9affea1cd953a9601d441b4ef35e847e232dfeb8d` | `28a862532a0ab0db75a8d0d47525bbd25ec47fe54f303fbd2726ab597157e84d` |

The fresh Sol executors were `/root/sol_contract_prior_executor` and
`/root/sol_contract_current_executor`. They confirmed all three assigned file
hashes before applying their variant. The fresh Opus sessions were
`722a3bcc-e9cf-4c0e-b19c-9c29a3916256` and
`69c294bc-0757-444a-b49e-9faed49a3a32`; both returned an actual-model receipt
of `claude-opus-5`. Independent grader `/root/contract_comparison_grader`
inspected the exact frozen resources and all four executor artifacts.

#### Group A: deterministic loaded-copy provenance

- Discriminating case: installed files match the source, a same-name user copy
  exists, and the response quotes distinctive tested text without a path,
  base-directory trace, or equivalent hash-linked runtime evidence.
- Control: installed files match, same-name locations are inventoried, and a
  native trace names the exact installed project-local path.
- Sol result: the prior and current variants both kept native load unverified,
  but only the current variant recorded the observed native trigger separately
  without attributing it to the installed revision. The exact-path control
  remained eligible to pass.
- Opus result: the prior variant used distinctive text as standalone load
  proof. The current variant kept load unverified, treated that text as
  corroboration only, and recorded the observed trigger separately. The
  exact-path control remained eligible to pass.
- Independent grade: `better` for the discriminating case in both targets,
  `same` for the control, and no named invariant loss.
- Candidate decision: `DirectionalCandidate`.
- Earned evidence label: **directional comparison**.
- Claim Ceiling: in these two cases, the current resources require
  deterministic loaded-copy provenance and preserve separate native-state
  reporting in both targets while continuing to accept exact-path provenance.
  The result does not establish real installation or native loading, other
  provenance mechanisms, reliability, non-regression, or behavior outside the
  declared cases.

#### Group B: required `worse` handling for revisions

- Discriminating case: one required revision case is `worse`, every target is
  available and agrees, and no separate material invariant loss is recorded.
- Control: every required target shows the intended delta, controls are stable,
  and no named invariant loss appears.
- Results: both variants and both targets retained the current instruction,
  withheld a directional label, and called for correction followed by an
  affected-case rerun. The current wording directly says that `worse` alone
  is not a material invariant loss. The successful control stayed stable.
- Independent grade: `same` in both targets and no named invariant loss.
- Candidate decision: `Retained`.
- Earned evidence label: none.
- Claim Ceiling: the cases show stable handling of the required `worse` path
  and the successful comparison path. They do not show that the current wording
  improves behavior.

#### Group C: unavailable-listing shipment waiver

- Discriminating case: one required listing judgment is unavailable, no
  available result has failed, and the user explicitly authorizes shipment.
- Control: a required listing result failed and the user asks to waive it.
- Sol result: the prior variant denied the unavailable-listing waiver. The
  current variant allowed a shipment-only waiver while leaving the listing
  state and evidence level unverified. The failed control remained
  non-waivable.
- Opus result: both variants allowed the unavailable-listing waiver without
  raising the evidence state or claim. The current wording removed ambiguity,
  but the final behavior was the same. The failed control remained
  non-waivable.
- Independent grade: `better` for Sol, `same` for Opus, `same` for both
  controls, and no named invariant loss.
- Candidate decision: `Retained` because the intended delta was absent in one
  required target.
- Earned evidence label: none.
- Claim Ceiling: the current wording changes Sol's handling to permit an
  explicit shipment waiver without changing the unverified listing state;
  Opus handling is stable. Both targets continue to reject waiver of failed
  evidence. No general improvement claim is supported.

#### Group D: public-tier near-miss threshold

- Discriminating case: public-tier near-miss judgments are `no`, `unsure`,
  `unsure`.
- Control: public-tier near-miss judgments are `no`, `no`, `unsure`.
- Results: both targets passed the discriminating pattern under the prior
  variant and failed it under the current two-categorical-`no` rule. Both
  targets passed the control under both variants.
- Independent grade: `better` for the discriminating case in both targets,
  `same` for the control, and no named invariant loss.
- Candidate decision: `DirectionalCandidate`.
- Earned evidence label: **directional comparison**.
- Claim Ceiling: for these two vote patterns, the current template enforces the
  two-categorical-`no` public-tier threshold in both targets and preserves a
  qualifying result. Other vote combinations, aggregation behavior,
  reliability, and non-regression remain unverified.

#### Group E: routine categorical first judgment

- Discriminating case: a routine should-trigger receives a clear first `yes`
  and a routine near-miss receives a clear first `no`.
- Control: the first judgment is `unsure`, followed by `yes`, `yes` for the
  should-trigger and `no`, `no` for the near-miss.
- Results: both variants and both targets stopped after the clear categorical
  first judgment and ran two follow-ups only after the borderline first
  judgment. Every supplied query received the same result across variants.
- Independent grade: `same` in both targets and no named invariant loss.
- Candidate decision: `Retained`.
- Earned evidence label: none.
- Claim Ceiling: these cases show stable routine handling for clear first
  judgments and the supplied borderline sequences. They do not show that the
  current wording improves behavior.

No aggregate label is assigned across the five groups. Groups A and D earned
bounded directional-comparison evidence. Groups B, C, and E remain retained
because the evidence was `same`, inconclusive, or divergent across targets.
This record supports no claim that the whole skill is generally improved,
non-regressing, or causally better.

### 2026-07-28 final missing-group comparisons

This pass closes four behavioral records that the final package review found
incomplete. Two frozen priors were used because the mode-selection rule was
introduced after the independent-review and authoring-guidance changes.

| Assigned variant | `SKILL.md` SHA-256 | Checklist SHA-256 |
| --- | --- | --- |
| Independent-review prior, `5af34de` | `71416c5a4c314eeeec4a7fc2b6cbe512ee48274598291f6d0a0d21212d684941` | `64bc6a50161fda6f6559c1c586c476f1e878162dfab71061ff143a1bea0b605d` |
| Verification-mode prior, `88c362e` | `4693702db6766235049e34df7bf95baea77c1de24108307c09e0da5a809754fe` | not used |
| Current, `73b9477` | `1ba4b97ad9e5a9fcbb3d27e4e69070d46683716fdb29d959709ffe90bf99af0f` | `6baf044506a96c614d8cd14515f50942438e38e99b1269e351ec07d157307654` |

The Sol executors were `/root/sol_ir_prior_executor`,
`/root/sol_mode_prior_executor`, and `/root/sol_missing_current_executor`.
Each confirmed its assigned file hashes. The Opus prior/current sessions were
`089b5848-6945-4051-b3fe-7d07df3d404d`,
`c5f55e7d-9c12-4b36-b01f-bced82c1f6b1`, and
`39c014be-77da-4b53-a319-bc58ff95a118`; each returned an actual-model receipt
of `claude-opus-5`. Independent grader
`/root/missing_groups_independent_grader` inspected the frozen resources and
all six executor artifacts.

#### Independent grading and final review

- Discriminating case: an executor summary claims a report passed, while the
  report is only a heading and one unsupported recommendation and the trace
  says a required input was not opened. Fresh nonauthor and final-review
  contexts are available.
- Control: run only the deterministic `skills-ref` structural validator.
- Results: both targets rejected the surface-only pass under both variants.
  The prior did not require a nonauthor/nonproducer grader or a different final
  reviewer. The current variant assigned those roles separately and required
  direct artifact and trace inspection. Both variants kept the isolated
  validator mechanical and free of an agent-review requirement.
- Independent grade: `better` for the discriminator in both targets, `same`
  for the control, and no named invariant loss.
- Candidate decision: `DirectionalCandidate`.
- Earned evidence label: **directional comparison**.
- Claim Ceiling: for this case, both targets applied the current ownership and
  inspection rules while preserving the mechanical-validation boundary. The
  record does not establish reliable role separation in other workflows or
  independently replay the underlying report fixture.

#### Project-evidence grounding and conditional examples

- Cases: prefer a resolved repository incident over a generic likely root
  cause; omit an example that merely repeats an exact schema; retain one concise
  example when a custom encoding is genuinely ambiguous.
- Results: prior and current variants made the same three decisions in both
  targets. The prior already reached them through repository context,
  repeatable-value, exact-contract, delete-test, and duplication rules.
- Independent grade: `same` in both targets with no named invariant loss.
- Candidate decision: `Retained`.
- Earned evidence label: none.
- Claim Ceiling: the cases show stable project-evidence and example-selection
  decisions in both targets. They do not show that the more explicit current
  wording improves behavior.

#### Context target and long-reference navigation

- H1 discriminator and embedded controls: a 470-line, roughly 4,700-token body
  accompanies a 350-line branch reference without a table of contents.
- H2 discriminator and embedded controls: a 470-line, roughly 5,200-token body
  accompanies a 250-line branch reference.
- Results: the prior had the 500-line hard limit but no token target or
  table-of-contents threshold. In both targets, the current variant required a
  table of contents for H1 and treated H2 as missing an authoring target rather
  than failing portable validation. It preserved the hard line limit, accepted
  the under-5,000-token body, and did not require a table of contents below the
  300-line threshold.
- Independent grade: `better` for both discriminators in both targets, stable
  embedded controls, and no named invariant loss.
- Candidate decision: `DirectionalCandidate`.
- Earned evidence label: **directional comparison**.
- Claim Ceiling: for the stipulated measurements, both targets applied the
  over-300-line navigation rule and below-5,000-token authoring target while
  preserving the hard structural limit and cross-rule controls. Behavior at
  exact boundaries and tokenizer-dependent estimates near 5,000 remains
  unverified.

#### Verification-mode choice

- Discriminators: a new-skill flow with enough intent to draft and an
  authorized revision after audit and scope approval, neither with a selected
  verification mode.
- Control: a read-only audit without a selected mode.
- Results: the prior defined no mode choice and continued both change flows.
  In both targets, the current variant asked before new-skill drafting and
  after revision scope approval but before editing. Both variants avoided the
  question during the read-only audit and stopped that flow after step 0.
- Independent grade: `better` for both discriminators in both targets, `same`
  for the control, and no named invariant loss.
- Candidate decision: `DirectionalCandidate`.
- Earned evidence label: **directional comparison**.
- Claim Ceiling: for these cases, both targets applied the intended mode-choice
  timing and preserved the read-only stop. Already-supplied modes,
  recommendation quality, and later enforcement that mode affects only the
  listing tier remain unverified.

The Sol artifacts include the assigned hashes and case answers but no separate
CLI session receipt. The Opus artifacts record the model receipts,
configurations, and session IDs but retain concise structured-result excerpts
rather than full transcripts. The independent grade is therefore limited to
the recorded instruction-application behavior and cannot replay the complete
prompt-to-response traces. No aggregate improvement, reliability,
non-regression, or causal claim is assigned across these groups.

### 2026-07-28 retained-revision terminal comparison

This comparison covers the final step 6 rule that prevents unsupported
candidate content from being packaged after a revision is marked `Retained`.

| Variant | `SKILL.md` SHA-256 | Baseline-template SHA-256 |
| --- | --- | --- |
| Prior, `e45a1e7` | `1ba4b97ad9e5a9fcbb3d27e4e69070d46683716fdb29d959709ffe90bf99af0f` | `1d6a33ed6686aadced84e920378f64e9a852fbaffda6c7bfabc57c03ea13c21f` |
| Current | `7c32b5fb6da9415251e15605a94ce89d3299279e1e582ae0bf13162cc3bbfe1e` | `1d6a33ed6686aadced84e920378f64e9a852fbaffda6c7bfabc57c03ea13c21f` |

The fresh Sol executors were `/root/retained_sol_prior_executor` and
`/root/retained_sol_current_executor`. The fresh Opus sessions were
`8df98d39-8075-4fad-8d06-b6f330335c88` and
`49601316-af6a-4057-8695-5a41b9dacbf4`; both returned an actual-model receipt
of `claude-opus-5`. Independent grader
`/root/retained_terminal_independent_grader` inspected both exact variants and
all four executor artifacts.

- R1 discriminator: a separable revision has one `Retained` group whose prior
  instruction was removed and one accepted `DirectionalCandidate` group.
- R2 discriminator: the same groups are entangled, so restoring the retained
  group would remove the accepted group.
- R-C control: every revision group is `DirectionalCandidate`, review passes,
  and no retained or correction-required group remains.
- Results: in both targets, both variants restored the separable retained group
  and re-entered validation before continuing. Both stopped the entangled
  candidate before packaging and allowed the all-directional control to proceed
  to the later gates. The prior outcomes were inferred from the retention and
  per-group rules. The current wording makes the restore-or-stop gate explicit.
- Independent grade: `same` for all three cases in both targets with no named
  invariant loss.
- Candidate decision: `Retained`.
- Earned evidence label: none.
- Claim Ceiling: these cases show the same safe terminal outcomes in both
  targets and a stable all-directional control. They support retaining the
  explicit rule, but they do not establish behavioral improvement, reliability,
  non-regression, or behavior outside the three cases.
