# Baseline comparison: [skill-name]

Use this protocol when creating a new skill or making a substantive revision
(changed instruction semantics, trigger description, or bundled resource;
typo, formatting, and link-only edits are exempt). It compares behavior with
and without the change on a small case set and produces the suite's durable
artifacts. Within this repository, `tests/README.md` is the canonical
convention; this template restates it for portable use.

## Protocol

1. **Declare cases before running.** For a new skill: realistic prompts where
   the skill should change execution or output, each named for the observed
   failure or baseline gap that motivates it. For a revision: the existing
   cases the change affects, plus new cases for new behavior. Keep the set
   small — cases must discriminate, not enumerate.
2. **Run matched pairs in fresh contexts.** Each case runs without the change
   (bare model, or the frozen prior version for a revision) and with it.
   Confirm the intended variant is actually loaded for with-skill runs. For a
   change limited to the description, compare unforced activation on the
   trigger set instead of forced-load behavior.
3. **Grade binary.** A separate fresh-context agent that did not author the
   change grades each run against the case's expected-behavior checklist —
   pass or fail per item, a case fails if any item fails. Deterministic
   scripts may grade mechanical items.
4. **Decide.** Ship only when every discriminating case shows the intended
   improvement and no case regresses. A regression, or a same-as-baseline
   result on a required discriminating case, returns the change to
   correction; rerun the affected cases after fixing.
5. **Emit the durable artifacts.** One case file per kept case in
   `tests/<skill-name>/cases/` and one log line per graded run in
   `tests/<skill-name>/log.md`. This completed template is working scratch —
   its content lives on in the case files, log lines, and the commit message;
   do not keep it as a separate record.

## Case file shape

Each case file: a title, one `Provenance:` line naming the motivating failure
or baseline gap, a self-contained `## Prompt` (blockquote, synthetic data
only), and `## Expected behavior` as binary `- [ ]` checklist items. Fold
near-duplicate variants into one battery case (numbered scenarios in the
prompt, one checklist item per scenario). Keep each file under ~45 lines.

## Honest claims

A graded pass shows that case, in that context, at that revision — not
reliability across models, harnesses, or untested behavior. Record what
actually ran and nothing more.
