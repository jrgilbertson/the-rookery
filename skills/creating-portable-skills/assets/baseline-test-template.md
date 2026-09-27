# Regression check: [skill-name]

[references/skills.md](../references/skills.md) owns formats, run counts,
targets, grading, costs, human inspection, value assessment, the execution
boundary, and the ship rule. This template owns the procedure.

## Evaluation boundary

Declare permitted inputs, resources, side effects, targets, and the caller's
cross-provider budget before dispatch. Apply the **Execution boundary** in
[references/skills.md](../references/skills.md) before native executor, trigger,
grader, or reviewer calls. Record the effective settings, include the harmless
rejected operation in the authorized smoke, and stop the affected role when
the native controls cannot show the boundary. Use synthetic
inputs in the archive's run directory outside the host project. Before
file-writing execution, verify that its working directory and resolved outputs
are inside that directory.
Existing authorization carries forward; additional resources or live effects
need authority. Keep failed runs and partial outputs as isolated evidence.
Only public-safe eval definitions and benchmarks enter the host project.

## Inspect with the human

Follow **Human inspection** in [references/skills.md](../references/skills.md).

1. Before calls on a value assessment, or when the cases are newly proposed,
   present the prompts, inputs, expected outcomes, assertions, and provenance,
   and wait for approval of that round. Reuse an already frozen case set for
   an affected regression.
2. After grading, present each case's paired results, original grades, quality,
   time, tokens, cost, and trace links. Keep activation evidence in its own
   record, apart from output quality.
3. Save agreement or disagreement and any note under that section's feedback
   rule. Write the disposition beside the original grade.
4. When no inspection surface is available, record this step incomplete and
   keep any feedback already saved.

## Value assessment

Follow **Value assessment** in [references/skills.md](../references/skills.md)
when the question is whether the skill helps.

1. Freeze the approved cases through the inspection step above.
2. Run one matched `with_skill` and `without_skill` pair per case per declared
   Executor target in fresh contexts. Save the run-archive records, including
   build identity.
3. Grade both arms blind under **Grading and independence**.
4. Record a value conclusion for the matched set. Leave shipping to the ship
   rule, and leave an unresolved hold unresolved.

## Check and diagnose

1. **Select affected evals.** Use existing cases touched by the change and add
   realistic cases for new behavior. A new skill starts with two or three
   realistic prompts, including an edge case. Freeze one or two sharp
   assertions per eval, or one per numbered independent scenario, before the
   check. Put mechanical validation in scripts.
2. **Run the changed skill.** Run each selected eval once per declared Executor
   target in fresh contexts and confirm the installed variant from the trace.
   Save outputs, transcripts, usage, duration, metrics, and build identity under
   the **Run archive** layout. The host collects isolated per-call usage and
   prices the complete work under **Cost and budget**; unknown usage or prices,
   exhausted budget, or subscription quota stop further calls.
3. **Grade blind.** Give an independent different-model grader the packet
   specified under **Grading and independence** in [references/skills.md](../references/skills.md),
   with sensitive values replaced by typed placeholders before transfer.
   Keep each original `grading.json`; evidence lost to safe redaction is a
   capture gap, not a pass.
4. **Inspect every failure.** Read the original transcript, distinguish behavior
   failure, grader/assertion error, and capture gap, and explain corrections in
   notes without overwriting grades. Compare or rerun the prior skill only on
   failing evals to attribute the failure. On this regression path, use a
   no-skill run to diagnose a failure. A behavior check does not wait on a
   no-skill baseline. Unresolved attribution stays unverified.
5. **Record and decide.** Write a benchmark for the changed check and a separate
   one-arm diagnostic benchmark when needed. Compare only matched cohorts;
   leave an aggregate delta against a failing-only baseline subset unreported.
   Apply the ship rule, the repeat rule, and the one independent review in
   [references/skills.md](../references/skills.md).
6. **Validate evidence files.** Keep evals in `evals/evals.json`, benchmarks in
   `evals/benchmarks/`, and raw evidence outside the repository. Run
   `scripts/check-evals.py` on the target skill directory. This completed
   template is temporary working material, not a maintained repository report.

For description-only changes, use unforced activation checks in
[assets/trigger-queries-template.md](trigger-queries-template.md), rather than
forced-load behavior. Cosmetic changes may skip behavioral evaluation.

## Human review and blind comparison

Read outputs beside their grades: assertions cover only their named outcomes.
For qualities such as organization or polish, use specific human feedback or a
blind comparison of two outputs. Record preferences as notes, never binary
passes or fails. A value assessment records its matched comparison on its own.
A regression check or diagnostic baseline subset establishes the behavior
exercised. Comparative claims stay inside the matched cases and targets.
