# Baseline comparison: [skill-name]

Use this record for a small, routine comparison. It can earn only
**smoke-tested** (one observed execution) or **directional comparison**
(matched prior/revised observations). It cannot establish non-regression,
causal improvement, or behavior outside the predeclared cases.

For a new skill, compare without-skill against with-skill. For a revision,
compare the frozen prior version against the revised version. Run each prompt
and variant in a fresh agent context with the intended variant actually loaded.

## Declaration

- Mode: [new skill / revision]
- Candidate instruction group: [one scoped group; do not batch unrelated changes]
- Required outcome: [observable result and done state, including any required artifact or handoff]
- Hard constraint under test: [authority boundary, exact format, deterministic check, or fragile operation that must survive]
- Prior variant identity: [absent for a new skill, or durable revision/path/hash]
- Revised variant identity: [durable revision/path/hash]
- Declared target set: [target cell IDs]

Record the intended set before running. Do not silently substitute a model,
harness, or configuration.

| Target cell | Exact intended model | Harness and version | Configuration, tools, and permissions | Required cases |
| --- | --- | --- | --- | --- |
| [target-a] | [exact model ID] | [harness, version] | [settings and available tools] | [discriminating, control] |
| [target-b, if declared] | [exact model ID] | [harness, version] | [settings and available tools] | [discriminating, control] |

## Case 1: [one-line summary]

- Role: [discriminating / control]
- Prompt: [full prompt text]
- Predeclared expectation: [for a discriminating case, the intended delta; for a control, the behavior that should remain materially stable]
- Outcome and constraint checks: [specific checks this case exercises]

Duplicate this target block for every declared target. Keep target observations
separate; do not average conflicting outcomes.

### Case 1 target: [target-cell-id]

- Actual date: [YYYY-MM-DD]
- Actual model: [exact model ID, not a family name or alias when the exact ID is available]
- Actual harness: [name and version]
- Actual configuration: [reasoning/effort settings, tools, permissions, and other material settings]
- Fresh-context mechanism: [new session, CLI execution, subagent, or equivalent]
- Prior variant actually loaded: [identity and how loading was confirmed]
- Revised variant actually loaded: [identity and how loading was confirmed]
- Prior observation: [what happened]
- Revised observation: [what happened]
- Observed losses: [none observed, or every material loss]
- Raw evidence: [concise output excerpt or durable transcript reference]
- Case result: [intended delta observed / materially stable control / same / worse / material invariant loss / unavailable]
- Evidence state: [passed / failed / unverified]
- Limitation: [what this run does not show]

## Case 2: [one-line summary]

- Role: [control / discriminating; the routine set needs at least one of each]
- Prompt: [full prompt text]
- Predeclared expectation: [expected delta or stable behavior]
- Outcome and constraint checks: [specific checks]

### Case 2 target: [target-cell-id]

- Actual date: [YYYY-MM-DD]
- Actual model: [exact model ID]
- Actual harness: [name and version]
- Actual configuration: [material settings, tools, and permissions]
- Fresh-context mechanism: [mechanism]
- Prior variant actually loaded: [identity and confirmation]
- Revised variant actually loaded: [identity and confirmation]
- Prior observation: [what happened]
- Revised observation: [what happened]
- Observed losses: [none observed, or every material loss]
- Raw evidence: [concise output excerpt or durable transcript reference]
- Case result: [intended delta observed / materially stable control / same / worse / material invariant loss / unavailable]
- Evidence state: [passed / failed / unverified]
- Limitation: [what this run does not show]

Duplicate the target block for every declared target. Add a third realistic case
only when it discriminates a separate important behavior.

## Comparison decision

| Target cell | Discriminating case | Control case | Observed loss | Target conclusion |
| --- | --- | --- | --- | --- |
| [target-a] | [result] | [result] | [loss or none observed] | [Retained / NewSkillCandidate / DirectionalCandidate / unverified] |
| [target-b, if declared] | [result] | [result] | [loss or none observed] | [Retained / NewSkillCandidate / DirectionalCandidate / unverified] |

- Candidate state: [revision: Retained / DirectionalCandidate; new skill: NewSkillCandidate]
- Shipment status: [not assessed / UnverifiedCandidate]
- Earned evidence label: [none / smoke-tested / directional comparison]
- Conclusion: [state only what the predeclared cases showed]
- Overall limitation: Behavior outside the predeclared cases remains unverified. [Add target-specific limitations.]

Decision rules:

- For a revision, a `same` discriminating-case result is inconclusive, not
  evidence that the instruction is unnecessary. Retain the current instruction.
  An unchanged or materially stable control is expected and does not force
  retention by itself.
- For a revision, retain the current instruction when an affected target is
  unavailable, a material loss appears, or declared targets materially diverge
  and cannot be reconciled without losing the named invariant.
- For a new skill, use `NewSkillCandidate`. It identifies a draft with no prior
  version and implies neither a behavioral claim nor shipment status by itself.
- Assign **directional comparison** only when matched cases show the intended
  delta, the control remains materially stable, and every required target cell
  has no observed named invariant loss. Say exactly that; do not say the
  revision is reliably better, proven, non-regressing, or causally improved.
- A stylistic difference is not a regression when the required outcome and
  hard constraints remain intact.
- Route requests for non-regression or causal-improvement claims to deeper
  evaluation that isolates the changed variable and accounts for run variation.

## Waiver (only when shipping with an unavailable check)

A waiver changes shipment authority only. It does not change an evidence state,
raise the earned label, satisfy a missing target, or authorize removing or
relaxing an instruction whose affected-target comparison is absent or
inconclusive.

- Waived by the user: [yes, quote or paraphrase the explicit waiver]
- Unavailable check and reason: [what could not run and why]
- Evidence state: [unverified]
- Candidate state: [revision: Retained unless the required comparison supports the change / new skill: NewSkillCandidate; never DirectionalCandidate from this waiver]
- Shipment status: [UnverifiedCandidate]
- Earned evidence label: [unchanged; do not raise]
- Date: [YYYY-MM-DD]
