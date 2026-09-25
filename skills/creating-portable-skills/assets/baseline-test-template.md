# Baseline comparison: [skill-name]

Use the validation route selected in [SKILL.md](../SKILL.md#workflow).
[references/skills.md](../references/skills.md) owns the file formats, arms,
run counts, targets, grading rules, and ship rule. This template owns the
procedure.

## Evaluation boundary

For either route, state the permitted inputs, resources, side effects, and run
budget before dispatch. Execute with synthetic inputs in the run archive's run
directory, outside the host project. For a file-writing evaluation, verify its
process working directory and resolved output paths are inside that run
directory before dispatch. Existing authorization carries forward. Ask before
accessing additional resources, affecting a live system, or spending
substantial unapproved time or money. Keep failed runs and partial outputs
isolated in the archive as evidence and record their failure; only the
skill's `evals/` files enter the host project.

## Focused check

Pick the affected evals in `evals/evals.json`, or add one with binary
assertions. Run them as [SKILL.md](../SKILL.md#workflow) defines the focused
check and grade them as step 4 below describes. Write the run files to the
archive and commit a one-arm benchmark that names the grader.

## Matched comparison

Full validation compares behavior with and without the change on a small eval
set using this protocol.

1. **Write the evals.** For a new skill: two or three realistic prompts where
   the skill should change execution or output, with varied phrasing and at
   least one edge case, each with a `provenance` naming the observed failure
   or baseline gap. For a revision: the existing evals the change affects,
   plus new evals for new behavior. Add a regression control only to guard
   one named contract, and keep controls few. Write and freeze assertions as
   the `assertions` rule in [references/skills.md](../references/skills.md)
   directs.
2. **Settle thresholds and review.** Before the deciding runs, confirm each
   targeted eval's minimum under [references/skills.md](../references/skills.md)
   and complete the pre-spend review that
   [SKILL.md](../SKILL.md#5-check-behavior) requires.
3. **Run the arms.** Run each eval in each arm, each run in a fresh context,
   and confirm from the trace that the intended variant loaded. For a change
   limited to the description, the arms are the prior and revised
   descriptions: judge unforced activation on the trigger set under each,
   instead of forced-load behavior. Write each run's files to the archive in
   the **Run archive** layout of [references/skills.md](../references/skills.md).
4. **Grade blind.** Give the grader final answers and the artifact or tool
   observations needed to check execution for every arm, labeled neutrally,
   with arm names removed from paths and quoted text. Exclude private
   reasoning and the author's conclusions. Grading is done when every run
   has a `grading.json` in the shape that **Grading and independence** in
   [references/skills.md](../references/skills.md) defines.
5. **Apply the ship rule.** For each target, build the benchmark and apply
   the ship rule and the regression-control rule in
   [references/skills.md](../references/skills.md). If a targeted eval's
   changed arm passes some runs but misses its minimum, tighten the
   ambiguous instruction or assertion. In a targeted eval, remove an
   assertion that passes in both arms and fix one that fails in both. Stop
   iterating when another revision no longer improves the result.
6. **Commit the evidence.** Keep the evals in `evals/evals.json`, commit one
   benchmark file per target in `evals/benchmarks/`, and run this skill's
   `scripts/check-evals.py` on the target skill directory until it exits 0.
   This completed template is working scratch; its content lives on in those
   files and the commit message.

## Human review and blind comparison

Read the outputs beside their grades: assertions catch only what someone
thought to write down. For qualities binary assertions cannot carry, such as
organization or polish, give a fresh-context judge two versions' outputs with
the labels hidden and ask which serves the eval's intended outcome better, and
why. Record that preference in the benchmark's `notes` to inform revision. A
preference from someone who knew which version they read is not this
comparison: route it to specific human feedback, or run the comparison.
