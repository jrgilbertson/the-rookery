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
