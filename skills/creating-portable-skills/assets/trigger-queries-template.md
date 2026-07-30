# Trigger contract: [skill-name]

The description is a tested activation API: at the fire-or-skip decision the
agent sees only the skill's name and description. This template tests that
metadata. Within this repository, `tests/README.md` is the canonical
convention; this template restates the protocol for portable use.

## Build the query set

- Write 5–10 should-trigger phrasings, including non-obvious ones. Vary
  length, formality, detail, implied intent, abbreviations, and minor typing
  mistakes. Each must represent work where the skill should change execution
  or output.
- Write 5–10 near misses that share the skill's topic, artifact, or common
  wording but belong to a different owner. Name that owner.
- Record both sets in `tests/<skill-name>/triggers.md` as two tables (query +
  one-line reason, query + expected owner). Current contract only — run
  results go in the log, not this file.

## Judge

- Judge each query in a fresh context through a separate agent that did not
  author the description. Show it only the skill name, description, and one
  query; require a plain yes or no.
- One run per query. A first judgment that is `unsure` or hedged is
  borderline: run that query twice more and take the majority.
- Every should-trigger query needs a yes. Any near-miss yes fails the set.

## Tune

- Fix failures by front-loading trigger words and describing when to use the
  skill. Do not summarize the workflow in the description — agents follow the
  summary and skip the body.
- After any description edit, rerun the complete query set; an edit that
  fixes one query can activate a near miss.

## Smoke check (packaging or install-path changes)

- The roster is the harness target set declared in step 2 of the skill
  workflow — the harnesses the skill is expected to install into (in the
  home repository of this template: Claude Code and Codex CLI).
- Install the skill from the current local source into a disposable project
  on each roster harness, ask one should-trigger query, and confirm the
  skill activates.
- Record one log line per harness in `tests/<skill-name>/log.md` (line
  format: `date | git rev | check | result | note`); when a roster harness
  is unavailable, log `not run — harness unavailable`.
- A listing-proxy pass is not proof of native triggering in a harness; only
  the smoke check shows that. Keep the two claims distinct.
