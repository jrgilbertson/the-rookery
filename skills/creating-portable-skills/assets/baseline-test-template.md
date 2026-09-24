# Baseline comparison: [skill-name]

Use this protocol when creating a new skill or making a substantive revision
(changed instruction semantics, trigger description, or bundled resource;
typo, formatting, and link-only edits are exempt). It compares behavior with
and without the change on a small case set and produces the suite's durable
artifacts.

## Protocol

1. **Write the cases.** For a new skill: two or three realistic prompts where
   the skill should change execution or output, with varied phrasing and at
   least one edge case, each named for the observed failure or baseline gap
   that motivates it. For a revision: the existing cases the change affects,
   plus new cases for new behavior. Write each checklist after seeing a first
   round of outputs, then freeze it before the runs that decide.
2. **Run matched pairs in fresh contexts.** Each case runs without the change
   (bare model, or a snapshot of the prior version for a revision) and with
   it. Confirm the intended variant is actually loaded for with-skill runs. For
   a change limited to the description, the matched pair is the prior
   description against the revised one: judge unforced activation on the
   trigger set under each, instead of forced-load behavior. Record tokens
   and duration for each run where the harness reports them, and
   `cost not available` where it does not.
3. **Grade binary.** Deterministic scripts grade mechanical items. An
   independent grader grades the rest against the case's checklist: pass or
   fail per item with the output span it rests on quoted, and a case fails if
   any item fails. One grader scores both variants of a case on a target.
   When a second model is available, the grader is a different model from the
   one that wrote the outputs; otherwise name the grader in the log. Give the
   grader final answers only, labeled neutrally, with variant names removed
   from paths and quoted text.
4. **Compare and decide.** For each target, count passing cases per variant
   and state the token and time delta beside the pass delta. The change ships
   when it raises the pass count on the cases it targets, no regression
   control fails with it, and the gain is worth its cost. Claim an
   improvement only on the targets that showed it. When a case passes on some
   runs and fails on others, run each variant a few more times and compare
   pass rates rather than counting one lucky run; if it stays inconsistent,
   tighten the ambiguous instruction or the item. Remove an item that passes
   in both variants, fix one that fails in both, and stop iterating when
   another revision no longer improves the result.
5. **Emit the durable artifacts.** One case file per kept case in
   `tests/<skill-name>/cases/` and one log line per graded run in
   `tests/<skill-name>/log.md` (line format: `date | git rev | check |
   result | note`, with the run's cost in the note). This completed template
   is working scratch — its content lives on in the case files, log lines,
   and the commit message; do not keep it as a separate record.

## Regression controls

A regression control is a case the baseline already passes, kept because it
protects one named load-bearing contract. Its `Provenance:` line names that
contract and labels the case a regression control. It never shows an
improvement. A control that fails in any run with the change is a regression:
fix the instruction or the item and rerun. Keep controls few; none exists to
enumerate desirable behavior.

## Human review and blind comparison

Read the outputs beside their grades: checklists catch only what someone
thought to write down. For qualities binary items cannot carry, such as
organization or polish, give a fresh-context judge two versions' outputs with
the labels hidden and ask which serves the case's intended outcome better, and
why. Log that preference as a note; it informs revision and never counts as a
pass or a fail. A preference from someone who knew which version they read is
not this comparison: route it to specific human feedback, or run the
comparison.

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
