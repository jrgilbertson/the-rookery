# Skill Test Suites

Conventions for every `tests/<skill-name>/` directory. This file is the
canonical statement of the testing convention; the templates in
`skills/creating-portable-skills/assets/` restate it for portable use and defer
to it inside this repository.

## Artifacts

Each skill keeps exactly three artifacts, plus `fixtures/` when cases need
input files:

- `triggers.md` — the trigger contract: should-trigger and near-miss query
  tables with expected judgments and one-line reasons. Current contract only,
  no run history.
- `cases/<case-name>.md` — one runnable behavioral case: the full prompt, any
  input files by relative path, a binary expected-behavior checklist, and one
  provenance line naming the observed failure or baseline gap that motivated
  the case.
- `log.md` — one line per run or check: `date | git rev | check | result |
  note`. An archive-pointer line identifies where prior history lives, so git
  remains the archive.

## Rules

- Binary pass/fail everywhere. A case fails if any checklist item fails.
  Trigger judgments are yes or no.
- A case enters a suite only when a baseline run showed the bare model failing
  the behavior, or an observed failure motivated it — named in the provenance
  line. Exception: a safety or privacy invariant may keep one case even when
  the bare model currently passes it.
- Roughly 10–15 active cases per skill is a ceiling for initial mining, not a
  target; steady-state suites grown by the observed-failure rule are expected
  to stay smaller.
- Git is the archive. No hand-recorded hashes, session IDs, evidence labels,
  or run ledgers in these artifacts.

## Cost hierarchy

| Tier | Check | Runs when |
| --- | --- | --- |
| 1 | structural validation (`skills-ref` validator) | every skill change |
| 2 | trigger suite | skill description change |
| 3 | affected behavioral cases | skill behavior change |
| — | per-harness smoke check | packaging or install-path change |

## Running

- **Trigger suite.** Judge each query in a fresh context that sees only the
  skill name, description, and that query; require yes or no. One run per
  query. A first judgment that is `unsure` or hedged is borderline: run that
  query twice more and take the majority. Any near-miss `yes` fails the suite.
- **Behavioral case.** Fresh agent context, skill installed from current
  source, no other conversation state. The case file is self-contained: run
  its prompt, resolve fixture paths relative to the case file, grade each
  checklist item pass or fail, and record one log line.
- **Smoke check.** Install the skill from source into a disposable project on
  each roster harness — Claude Code and Codex CLI — ask one trigger query, and
  confirm the skill activates. One log line per harness; if a roster harness
  is unavailable, log `not run — harness unavailable`.

## Honest claims

A trigger-suite pass is a listing proxy, not proof of native triggering in a
harness — only a smoke check shows that. A log line states only what its run
actually checked.

## Privacy

No private meeting content, participant identities, account identifiers,
source URLs, vault names, or local absolute paths in any tracked test
artifact. Cases use synthetic data.
