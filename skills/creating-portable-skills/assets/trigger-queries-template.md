# Trigger contract: [skill-name]

[references/skills.md](../references/skills.md) owns the description rules,
the `evals/eval_queries.json` format and seeding method, the run count, the
pass thresholds, and the tuning split; this template owns the procedure.

## Build the query set

- Should-trigger queries represent work where the skill should change
  execution or output. Include non-obvious phrasings, abbreviations, and minor
  typing mistakes.
- Near misses share the skill's topic, artifact, or common wording but belong
  to a different owner. Name that owner in `owner`.

## Screen

- Optionally, before activation runs, have an independent grader, as the
  skill workflow defines one, judge each query in a fresh context. Show it
  only the skill name, description, and one query; require a plain yes or no.
- Record the screen's result as a listing proxy.

## Run

- Install the skill from the current local source into a disposable project
  on each target harness. Run each query in a fresh session and record from
  the trace whether the skill activated.

## Tune

- Revise the description from train-split failures under the **Descriptions
  and triggering** and **Trigger evals** rules in
  [references/skills.md](../references/skills.md), then rerun the complete
  query set; an edit that fixes one query can activate a near miss.

## Smoke check

- The roster is the set of harnesses in the target set from
  [step 2 of SKILL.md](../SKILL.md#2-scope-targets-and-resources).
- On each roster harness, install as **Run** does, ask one should-trigger
  query, and confirm from the run's trace that the copy which activated is
  the just-installed one (its path or base directory). When a same-name copy
  exists in a user or system location and the activated copy's provenance
  cannot be confirmed, record the result as inconclusive rather than pass.
- Record one result per harness in the run archive and in the round's
  benchmark `notes`; when a roster harness is unavailable, record
  `not run — harness unavailable` and ask the user whether to ship without
  it.
- After a packaging change merges to the branch that installers pull from,
  repeat the smoke check once against that published state and record that
  result too. Local-source success does not prove remote resolution.
