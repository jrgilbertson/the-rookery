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

Date: 2026-07-16 | Harness: Claude Code subagent (baseline), Codex CLI 0.144.4 + Grok CLI + Claude Code subagent (with-skill) | Model: session defaults per harness

| Prompt | Baseline behavior (observed) | With-skill behavior (observed) | Verdict |
| --- | --- | --- | --- |
| Create a skill that turns raw standup notes into a three-line summary (done/doing/blocked), and get it ready to share | One-shot SKILL.md plus a zip; self-audit confirmed: no interview, no validator run, no trigger testing, no with/without comparison, no formal portability check | All three harnesses ran the full loop: interview from supplied intent, validation (skills-ref, or the manual fallback when Codex's sandbox denied network), fresh-context baselines, subtract pass cutting unearned rules, trigger sets 100% pass, companion skips named | better |

Observed delta: all four disciplines enforced with the skill and all four skipped without it. Full run logs: `tests/creating-portable-skills/results.md`.

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
