# Fidelity Check

The orchestrator starts one independent reviewer in a clean context. Give the
reviewer these instructions, the final briefing, sourced baseline (`p0`), source
audit, every raw lens return, and the execution manifest. Do not include the
orchestrator's synthesis reasoning. The reviewer checks the briefing against the
research record, not the reasoning that produced it.

If the context inherited the orchestrator's conversation or earlier review
work, stop and return `FIDELITY CONTEXT NOT INDEPENDENT`. The execution manifest
identifies intended, completed, and failed lenses; use it to identify the
available returns, not to speculate about work a failed lens might have done.

Review whether the synthesis preserved the research. Do not recommend a
different conclusion, grade the prose, or add your own analysis. Answer these
two questions from the supplied artifacts:

1. **Which disagreements present in the raw returns are lost from the briefing,
   and which disagreements in the briefing were invented?**
2. **Is every material analytical assumption, mechanism, and causal-chain link
   evidence-traceable or explicitly labeled as inference with calibrated
   confidence?**

For this check, material means capable of changing the answer, confidence, or
next action. Evidence-traceable means the briefing identifies the supporting
claim in the sourced `p0`, source audit, or a raw return. You check whether that
trace or inference treatment exists, not whether the conclusion is correct.

## What counts as disagreement

Two lenses disagree when they reach incompatible conclusions or recommend
materially incompatible actions from their own evidence. The loss may be:

- **Contradicted:** the briefing presents one conclusion as settled without
  the opposing conclusion.
- **Flattened:** the briefing replaces both positions and their evidence with a
  generic hedge.
- **Softened:** the disagreement remains but the strongest evidence for one
  side disappears.
- **Dropped:** the disagreement is absent.

A lens covering more ground than another is not disagreement. Absence of a
claim is not dissent. A failed lens is missing coverage, not evidence of
agreement or disagreement.

Also check the inverse: a conflict in the briefing that does not exist in the
raw returns. Treat invented tension as seriously as lost tension.

## Analytical traceability

Inspect the `First-principles analysis` and `Systems thinking and higher-order
effects` sections, plus any material analytical claim preserved elsewhere in a
short or custom form. Treat each assumption and mechanism separately. Split a
causal chain into direct, second-order, and higher-order links and inspect every
material link; one sourced endpoint does not support the links between
endpoints.

Report a defect when a material element has no identifiable evidence trace and
is not explicitly labeled as inference with confidence, or when an inference
has no calibrated confidence. A factual restatement is not a traced
relationship or mechanism merely because both sentences cite the same source.

## Report

For each lost or invented disagreement, report:

- **Claim:** an exact quote from the return.
- **Lens:** the lens that made it.
- **Opposing claim and lens:** an exact quote and its lens; for invented
  tension, state which claimed side has no supporting return.
- **Briefing treatment:** contradicted, flattened, softened, dropped, or
  invented, with an exact quote from the briefing or `absent`.
- **Decision effect:** whether the defect would change what a reader does.

For each analytical traceability defect, report:

- **Analytical element:** an exact quote from the briefing.
- **Kind:** assumption, mechanism, or causal-chain link.
- **Material effect:** how it could change the answer, confidence, or next
  action.
- **Briefing treatment:** the missing evidence trace, inference label, or
  calibrated confidence.

Do not suggest rewrites or judge whether the conclusion is right. If both
questions are clean, report `FIDELITY CLEAN` and stop.
