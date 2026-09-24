# Baseline comparison: [skill-name]

Use this protocol when creating a new skill or making a substantive revision
(changed instruction semantics, trigger description, or bundled resource;
typo, formatting, and link-only edits are exempt). It compares behavior with
and without the change on a small case set and produces the suite's durable
artifacts.

## Protocol

1. **Declare cases before running.** For a new skill: realistic prompts where
   the skill should change execution or output, each named for the observed
   failure or baseline gap that motivates it. For a revision: the existing
   cases the change affects, plus new cases for new behavior. Keep the set
   small: discriminating cases prove the change, and the section on
   regression controls covers a case the baseline already passes.
2. **Run matched pairs in fresh contexts.** Each case runs without the change
   (bare model, or the frozen prior version for a revision) and with it.
   Confirm the intended variant is actually loaded for with-skill runs. For a
   change limited to the description, the matched pair is the prior
   description against the revised one: judge unforced activation on the
   trigger set under each, instead of forced-load behavior. Record tokens
   and duration for each run where the harness reports them, and
   `cost not available` where it does not.
3. **Grade binary.** Deterministic scripts grade mechanical items. An
   independent grader, as the skill workflow defines one, grades the rest
   against the case's expected-behavior checklist — pass or fail per item, a
   case fails if any item fails, and each verdict quotes the output span it
   rests on. One grader scores both variants of a case on a target, so the
   comparison holds the grader constant. When a second model is available,
   the grader is a different model from the one that wrote the outputs;
   otherwise name the grader in the log. Give the grader the final answer
   only, and hide the variant: label outputs neutrally and remove variant
   names from paths and text the outputs quote. A second grader is an
   optional spot-check on a contested item and never decides a pass; when
   the two disagree, the item is soft and gets fixed.
4. **Decide.** Ship only when no case regresses and every discriminating
   case shows a settled improvement on at least one named target; on any other
   target where that case is unsettled or unchanged, withhold its claim. A
   regression, or a discriminating case with no settled improvement on any
   target, returns the change to correction; rerun the affected cases after
   fixing.
   State the cost delta beside the pass delta, so the decision shows what the
   change costs against what it buys. A checklist item that passes in both
   halves proves nothing: remove it, or keep its case only as a regression
   control.
   **Settle a case that varies.** One matched pair per case stays the default.
   A variant is settled when every run of it on one named target (model and
   harness) agrees, and mixed once two of its runs there disagree; further
   runs confirm a settled variant and never unmix a mixed one. When a run
   fails, either take that failure as the case's result under the rule
   above, so a failing control is a regression, or rerun both variants and
   read every run together. A case with a
   mixed variant is `unsettled` on that target, neither a pass nor a
   regression: it shows no improvement, and a control mixed without the
   change detects no regression. Fix a checklist item that grades what its
   prompt never asks for, reduce ambiguity in the instructions under test, or
   ship with that target's claim withheld and one `unsettled` log line
   naming the withheld claim. Withholding a claim applies only to an
   unsettled case: a control settled as passing without the change and
   failing with it blocks shipping.
5. **Emit the durable artifacts.** One case file per kept case in
   `tests/<skill-name>/cases/` and one log line per graded run in
   `tests/<skill-name>/log.md` (line format: `date | git rev | check |
   result | note`, with the run's cost in the note). This completed template
   is working scratch — its content lives on in the case files, log lines,
   and the commit message; do not keep it as a separate record.

## Regression controls

A regression control is a case the baseline already passes, kept because it
protects one named load-bearing contract. Its `Provenance:` line names that
contract and labels the case a regression control. It proves the contract did
not regress and never that the change improved anything, so a discriminating
case still has to carry the improvement. It runs in the matched pair like
every case, and a control that passes without the change and fails with it is
a regression under step 4. Keep controls few: each prevents one named
regression, and none exists to enumerate desirable behavior.

## Blind version comparison (optional)

Use this for qualities binary items cannot carry, such as organization or
polish. Give a fresh-context judge the outputs of two versions with the labels
hidden and ask which serves the case's intended outcome better, and why. Log
the preference as a note. It informs revision and never counts as a pass or a
fail. A preference from someone who knew which version they read is not this
comparison: route it to specific human feedback, or run the comparison.

## Case file shape

Each case file: a title, one `Provenance:` line naming the motivating failure
or baseline gap, or a regression control's contract, a self-contained
`## Prompt`
(blockquote, synthetic data only), and `## Expected behavior` as binary
`- [ ]` checklist items, each grading only what the prompt asks for. Fold near-duplicate variants into one battery case
(numbered scenarios in the prompt, one checklist item per scenario). Keep each
file under ~45 lines.

## Honest claims

A graded pass shows that case, in that context, at that revision — not
reliability across models, harnesses, or untested behavior. Record what
actually ran and nothing more.
