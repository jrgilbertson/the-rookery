# Regression check: [skill-name]

[references/skills.md](../references/skills.md) owns formats, run counts,
targets, grading, costs, and the ship rule. This template owns the procedure.

## Evaluation boundary

Declare permitted inputs, resources, side effects, targets, and the caller's
cross-provider budget before dispatch. Use synthetic inputs in the archive's
run directory outside the host project. Before file-writing execution, verify
that its working directory and resolved outputs are inside that directory.
Existing authorization carries forward; additional resources or live effects
need authority. Keep failed runs and partial outputs as isolated evidence.
Only public-safe eval definitions and benchmarks enter the host project.

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
3. **Grade blind.** Give an independent different-model grader neutral packets
   containing the final answer, all tool names and inputs, relevant observations
   and artifacts, and available child readouts. Remove variant labels, private
   reasoning, and author conclusions. Keep each original `grading.json`.
4. **Inspect every failure.** Read the original transcript, distinguish behavior
   failure, grader/assertion error, and capture gap, and explain corrections in
   notes without overwriting grades. Compare or rerun the prior skill only on
   failing evals to attribute the failure. For new skills, use a no-skill check
   only if needed for diagnosis. Unresolved attribution stays unverified.
5. **Record and decide.** Write a benchmark for the changed check and a separate
   one-arm diagnostic benchmark when needed. Compare only matched cohorts;
   never report an aggregate delta against a failing-only baseline subset.
   Apply the ship rule and obtain the one independent PR review. The operator
   decides whether to revise or stop within the authorized budget.
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
passes or fails. A regression check or diagnostic baseline subset does not
establish improvement; comparative claims need matched evidence and remain
limited to the cases and targets exercised.
