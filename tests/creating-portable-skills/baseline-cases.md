# Baseline test: creating-portable-skills

Mode rule — pick the mode that matches the flow:

- **New skill:** run each prompt with and without the skill.
- **Revision:** run each prompt with the prior version and the revised version.

Run every prompt in a fresh agent context with the right variant loaded —
use the harness's native mechanism for a clean context (a subagent, a CLI
exec, a new session). Never compare inside one warm session; carried-over
context contaminates the baseline.

These cases are new-skill mode (with/without). A with-skill run passes when
it demonstrably enforces the four disciplines a bare prompt skips:

1. Portability gates applied — portable frontmatter only, capability-based prose, self-contained directory.
2. Instructions evidence-gated — the delete test runs; unearned lines get cut.
3. Description tested as a trigger contract — should-trigger and near-miss queries built and run.
4. The standard loop followed — interview through validation, baseline, review, and package, with completion criteria observed.

## Case 1: Create a skill from scratch (run as "summarizing-standups")

Date: 2026-07-16 | Harness: Claude Code, both halves | Model: session default, both halves | Fresh context per half

Controlled comparison (matched pair, same harness and model):

| Prompt | Baseline behavior (observed) | With-skill behavior (observed) | Verdict |
| --- | --- | --- | --- |
| Create a skill that turns raw standup notes into a three-line summary (done/doing/blocked), and get it ready to share | Bare Claude Code subagent: one-shot SKILL.md plus a zip; self-audit confirmed: no interview, no validator run, no trigger testing, no with/without comparison, no formal portability check | Claude Code visitor run in a clean repo: all loop steps 1-9 completed with criteria met; interview from supplied intent, skills-ref validation, fresh-context baseline, subtract pass, trigger set built and run, companion depth-skips named (AE1), convention scan with the generic path declared (AE2) | better |

Observed delta: all four disciplines enforced with the skill and all four skipped without it, in the same harness on the same session-default model with a fresh context on each side. The Codex CLI 0.144.4 and Grok CLI runs of the same create flow are portability evidence, not part of the controlled comparison; their full run logs are in `tests/creating-portable-skills/results.md`.

## Case 2: Review and fix an existing skill

Not yet run — scheduled as the post-merge dogfood (the design-evals migration review). The waiver path (AE3) was exercised separately and passed; see results.md.

Date: [YYYY-MM-DD] | Harness: [name] | Model: [name]

| Prompt | Baseline behavior (observed) | With-skill behavior (observed) | Verdict |
| --- | --- | --- | --- |
| Review this skill and fix anything wrong with it: [path to a small existing skill] | | | |

Expected delta: baseline edits ad hoc; with-skill audits against the checklist, produces a prioritized fix list, gets scope approval, and compares prior against revised before shipping.

## Case 3: Fix a description that never triggers (run against a toy "expense-notes" skill)

Date: 2026-07-16 | Harness: Claude Code subagents (fresh context per half) | Model: session default

| Prompt | Baseline behavior (observed) | With-skill behavior (observed) | Verdict |
| --- | --- | --- | --- |
| My expense-notes skill's description isn't triggering when people ask about receipts — improve it | Intuition rewrite (a workflow-describing description); self-audit confirmed: no trigger queries built or run, no testing gate or waiver, no length/portability check | Checklist audit named the four description failures; approved fix scope; both gates ran — prior-vs-revised baseline and a 10/10 should-trigger / 0-of-9 near-miss query set; change correctly ruled substantive, validated clean | better |

Observed delta: the with-skill run enforced the trigger-contract discipline end to end; the bare run shipped an untested description.

## Waiver (only when shipping without the comparison)

A substantive change must not ship without the comparison above or an
explicit waiver from the user, recorded here. Substantive means any change
to instruction semantics, the trigger description, or bundled resources.
Typo, formatting, and link-only fixes are exempt and need no waiver.

- Waived by the user: [yes — quote or paraphrase the user's explicit waiver]
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
