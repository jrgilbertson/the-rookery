# Baseline comparison: [skill-name]

Use this record for a small, routine matched comparison. It can earn only
**directional comparison**. It cannot establish non-regression, causal
improvement, or behavior outside the predeclared cases.

This template is the authoritative source for routine case construction,
candidate decisions, evidence labels, matched-comparison waivers, and Claim
Ceiling recording.

For a new skill, compare without-skill against with-skill. For a revision,
compare the frozen prior version against the revised version. Run each prompt
and variant in a fresh agent context with the intended variant actually loaded.
Have a separate fresh-context agent grade the matched outputs. The grader must
not have authored the change or produced either artifact. Mechanical checks may
use deterministic scripts.

Predeclare the required outcome and hard constraints. If an exploratory run
makes the need for another objective check clear, add or refine that check,
freeze it, and rerun both variants before using it in the comparison. Keep
subjective qualities in human review or an explicit blind comparison rather
than forcing them into binary checks.

## Declaration

- Mode: [new skill / revision]
- Candidate instruction group: [one scoped group; do not batch unrelated changes]
- Required outcome: [observable result and done state, including any required artifact or handoff]
- Hard constraint under test: [authority boundary, exact format, deterministic check, or fragile operation that must survive]
- Input files: [relative paths and identity, or none]
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
- Input files: [relative paths and identity, or none]
- Predeclared expectation: [for a discriminating case, the intended delta; for a control, the behavior that should remain materially stable]
- Objective outcome and constraint checks: [specific, observable checks fixed before grading]
- Subjective review focus: [qualities for human or blind review, or none]

Duplicate this target block for every declared target. Keep target observations
separate; do not average conflicting outcomes.

### Case 1 target: [target-cell-id]

- Actual date: [YYYY-MM-DD]
- Actual model: [exact model ID, not a family name or alias when the exact ID is available]
- Actual harness: [name and version]
- Actual configuration: [reasoning/effort settings, tools, permissions, and other material settings]
- Fresh-context mechanism: [new session, CLI execution, subagent, or equivalent]
- Prior executor: [agent or session identity]
- Revised executor: [agent or session identity]
- Independent grader: [separate agent and its clean-context mechanism]
- Prior variant actually loaded: [identity and how loading was confirmed]
- Revised variant actually loaded: [identity and how loading was confirmed]
- Prior observation: [what happened]
- Revised observation: [what happened]
- Observed losses: [none observed, or every material loss]
- Artifacts inspected: [actual files or outputs the grader examined]
- Raw evidence: [per-check artifact or trace evidence, with concise excerpts or durable references]
- Trace observation: [wasted path, ambiguity, ignored instruction, repeated helper work, or none]
- Subjective feedback: [specific human feedback or blind result, or not applicable]
- Case result: [intended delta observed / materially stable control / same / worse / material invariant loss / unavailable]
- Evidence state: [passed / failed / unverified]
- Limitation: [what this run does not show]

## Case 2: [one-line summary]

- Role: [control / discriminating; the routine set needs at least one of each]
- Prompt: [full prompt text]
- Input files: [relative paths and identity, or none]
- Predeclared expectation: [expected delta or stable behavior]
- Objective outcome and constraint checks: [specific, observable checks fixed before grading]
- Subjective review focus: [qualities for human or blind review, or none]

### Case 2 target: [target-cell-id]

- Actual date: [YYYY-MM-DD]
- Actual model: [exact model ID]
- Actual harness: [name and version]
- Actual configuration: [material settings, tools, and permissions]
- Fresh-context mechanism: [mechanism]
- Prior executor: [agent or session identity]
- Revised executor: [agent or session identity]
- Independent grader: [separate agent and its clean-context mechanism]
- Prior variant actually loaded: [identity and confirmation]
- Revised variant actually loaded: [identity and confirmation]
- Prior observation: [what happened]
- Revised observation: [what happened]
- Observed losses: [none observed, or every material loss]
- Artifacts inspected: [actual files or outputs the grader examined]
- Raw evidence: [per-check artifact or trace evidence]
- Trace observation: [wasted path, ambiguity, ignored instruction, repeated helper work, or none]
- Subjective feedback: [specific human feedback or blind result, or not applicable]
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
- Earned evidence label: [none / directional comparison]
- Conclusion: [state only what the predeclared cases showed]
- Overall limitation: Behavior outside the predeclared cases remains unverified. [Add target-specific limitations.]
- Claim Ceiling: [state the strongest conclusion this record permits]

The Claim Ceiling is the strongest conclusion supported by the declared
targets, cases, earned evidence label, observed losses, unavailable cells, and
limitations.

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
  has an available case result with no named invariant loss. A missing or
  unavailable required cell earns no directional label. Say exactly that; do
  not say the revision is reliably better, proven, non-regressing, or causally
  improved.
- A pass requires direct evidence of substantive completion. The grader also
  checks whether each objective check is discriminating, verifiable from the
  available artifacts, and complete enough to cover the required outcome.
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
