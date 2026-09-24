# Baseline comparison: [skill-name]

Use the validation route selected in [SKILL.md](../SKILL.md#workflow).
[references/skills.md](../references/skills.md) owns the file formats, arms,
run counts, targets, grading rules, and ship rule. This template owns the
procedure. Both routes record the actual target and confirm the intended
package is loaded.

## Evaluation boundary

For either route, state the permitted inputs, resources, side effects, and run
budget before dispatch. Execute with synthetic inputs in the run archive's run
directory, outside the host project. For a file-writing evaluation, verify its
process working directory and resolved output paths are inside that run
directory before dispatch. Existing authorization carries forward. Ask before
accessing additional resources, affecting a live system, or spending
substantial unapproved time or money. Keep failed runs and partial outputs in
the archive as evidence and record their failure; only `evals/evals.json`
entries and the round's benchmark file enter the host project.

## Focused check

Pick the affected evals in `evals/evals.json`, or add one with binary
assertions. Run each once with the revised skill and inspect the actual output
against its assertions and the unchanged hard constraints. Write the run files
to the archive and commit a one-arm benchmark. This check supports only the
behavior it exercised, not a comparative improvement claim. The author may
inspect it; name that inspection as the benchmark's `grader` rather than
calling it independent grading.

## Matched comparison

Full validation compares behavior with and without the change on a small eval
set using this protocol.

1. **Write the evals.** For a new skill: two or three realistic prompts where
   the skill should change execution or output, with varied phrasing and at
   least one edge case, each with a `provenance` naming the observed failure
   or baseline gap. For a revision: the existing evals the change affects,
   plus new evals for new behavior. Keep any example that appears in the
   skill's text or in a grader prompt out of these evals. Write assertions
   after seeing a first round of outputs, then freeze them before the runs
   that decide.
2. **State the thresholds.** Before the deciding runs, write the target and
   the minimum acceptable result for the targeted evals.
3. **Run the arms.** Run each eval in each arm, each run in a fresh context,
   and confirm from the trace that the intended variant loaded. For a change
   limited to the description, the arms are the prior and revised
   descriptions: judge unforced activation on the trigger set under each,
   instead of forced-load behavior. Write each run's timing, metrics, and
   build identity to the archive; where the harness reports no cost, record
   that.
4. **Grade blind.** Give the grader final answers and the artifact or tool
   observations needed to check execution for every arm, labeled neutrally,
   with arm names removed from paths and quoted text. Exclude private
   reasoning and the author's conclusions. Scripts grade mechanical
   assertions; the independent grader writes evidence before each verdict in
   `grading.json`.
5. **Apply the ship rule.** For each target, build the benchmark and compare
   the targeted evals against the stated minimum and the regression controls,
   with the token and time delta beside the pass-rate delta. When a
   discriminating eval passes on some runs and fails on others, run each arm
   more and compare pass rates; if it stays inconsistent, tighten the
   ambiguous instruction or assertion. In a discriminating eval, remove an
   assertion that passes in both arms and fix one that fails in both. Stop
   iterating when another revision no longer improves the result.
6. **Commit the evidence.** Keep the evals in `evals/evals.json`, commit one
   benchmark file per target in `evals/benchmarks/`, and run
   `scripts/check-evals.py` on the skill. This completed template is working
   scratch; its content lives on in those files and the commit message.

## Regression controls

Mark a regression control with `regression_control: true` and name the
contract it guards in `provenance`. A control that fails in any run with the
change is a regression: fix the instruction or the assertion and rerun. Keep
controls few; none exists to enumerate desirable behavior.

## Human review and blind comparison

Read the outputs beside their grades: assertions catch only what someone
thought to write down. For qualities binary assertions cannot carry, such as
organization or polish, give a fresh-context judge two versions' outputs with
the labels hidden and ask which serves the eval's intended outcome better, and
why. Record that preference in the benchmark's `notes`; it informs revision
and never counts as a pass or a fail. A preference from someone who knew which
version they read is not this comparison: route it to specific human feedback,
or run the comparison.
