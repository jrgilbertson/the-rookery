# Trigger contract: [skill-name]

The description is a tested activation API: at the fire-or-skip decision the
agent sees only the skill's name and description. This template tests that
metadata. [references/skills.md](../references/skills.md) owns the
`evals/eval_queries.json` format, the run count, the pass thresholds, and the
tuning split; this template owns the procedure.

## Build the query set

- Choose dimensions where misrouting is likely, such as intent, phrasing, and
  context. Draft tuples that cross them, then write one query per tuple.
- Should-trigger queries represent work where the skill should change
  execution or output. Include non-obvious phrasings, abbreviations, and minor
  typing mistakes.
- Near misses share the skill's topic, artifact, or common wording but belong
  to a different owner. Name that owner in `owner`.
- The file holds the current contract only; run results go in the run
  archive.

## Screen

- Optionally, before activation runs, judge each query in a fresh context
  through an independent grader, as the skill workflow defines one. Show it
  only the skill name, description, and one query; require a plain yes or no.
- Record the screen as a listing proxy, never as activation evidence. A
  judgment that cannot run is recorded as not run, never as a pass.

## Run

- Install the skill from the current local source into a disposable project
  on each target harness. Run each query in a fresh session and record from
  the trace whether the skill activated.

## Tune

- Fix failures by front-loading trigger words and describing when to use the
  skill. Prefer a pushier description; add an exclusion only where runs show
  the skill taking another owner's work.
- Tune on the train split only. Keep every tuning query out of the validation
  set and the fresh check.
- After any description edit, rerun the complete query set; an edit that
  fixes one query can activate a near miss.

## Smoke check (packaging or install-path changes)

- The roster is the harness target set declared in step 2 of the skill
  workflow — the harnesses the skill is expected to install into.
- Install the skill from the current local source into a disposable project
  on each roster harness, ask one should-trigger query, and confirm from the
  run's trace that the copy which activated is the just-installed one (its
  path or base directory). When a same-name copy exists in a user or system
  location and the activated copy's provenance cannot be confirmed, record
  the result as inconclusive rather than pass.
- Record one result per harness in the run archive and in the round's
  benchmark `notes`; when a roster harness is unavailable, record
  `not run — harness unavailable`.
- After a packaging change merges to the branch installers pull from, repeat
  the probe once against that published state — local-source success does
  not prove remote resolution — and record that result too.
