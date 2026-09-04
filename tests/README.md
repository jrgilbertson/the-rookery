# Skill Test Suites

Conventions for every `tests/<skill-name>/` directory. This file is the
canonical statement of the testing convention; the templates in
`skills/creating-portable-skills/assets/` restate it for portable use and defer
to it inside this repository.

## Repository checks

Run the same deterministic door used by CI before pushing:

```bash
lefthook run pre-push --force
```

The group validates the published catalog, repository text and configuration,
current-tree secrets, and the explicit deterministic fixture roster. GitHub
Actions runs this same non-empty group as the required `Tests Status` job.
The local invocation grades the current tracked and untracked working tree;
run it from a clean candidate checkout when binding release evidence to a
commit. The hosted job grades its checked-out revision and is the authoritative
revision-bound result.
Behavioral cases and install probes remain release evidence and are selected by
the change-based cost guidance below; they are not silently treated as part of
the deterministic door.

## Artifacts

Each skill keeps exactly three artifacts, plus `fixtures/` when cases need
input files:

- `triggers.md` — the trigger contract: should-trigger and near-miss query
  tables with expected judgments and one-line reasons. Current contract only,
  no run history.
- `cases/<case-name>.md` — one runnable behavioral case: the full prompt, any
  input files by relative path, a binary expected-behavior checklist, and one
  provenance line naming the observed failure or baseline gap that motivated
  the case, or the load-bearing contract protected by a labeled regression
  control.
- `log.md` — one line per run or check: `date | git rev | check | result |
note`. The `git rev` field names the commit the run's working tree was
  based on — the parent commit when the change under test is not yet
  committed. An archive-pointer line identifies where prior history lives,
  so git remains the archive.
- optional `<name>-protocol.md` — a per-suite scoring or measurement protocol
  for recurring checks the suite runs against external or machine-local
  evidence. The protocol document defines how a check is scored; its results
  still land in `log.md` as ordinary convention-compliant lines, and any
  detailed bookkeeping the protocol needs lives with the evidence, outside
  these artifacts.

## Rules

- Binary pass/fail everywhere. A case fails if any checklist item fails.
  Trigger judgments are yes or no.
- A case enters a suite when a baseline run showed the bare model failing the
  behavior or an observed failure motivated it — named in the provenance line.
  A case that both variants pass stays only as an explicitly labeled
  regression control, whether it guards a safety or privacy invariant or
  another load-bearing contract, and a suite keeps only a small number of
  them. Labeled controls never count as discriminating evidence for a new
  skill or behavior change.
- Roughly 10–15 active cases per skill is a ceiling for initial mining, not a
  target; steady-state suites grown by the observed-failure rule are expected
  to stay smaller.
- Git is the archive. Beyond the log format's required `git rev` field, no
  hand-recorded hashes, session IDs, evidence labels, or run ledgers in
  these artifacts.
- Name the independent-review mechanism in the log line, such as a fresh
  session, CLI run, or subagent. Do not record context identifiers. Naming the
  mechanism does not replace the output or trace evidence behind the judgment.

## Cost hierarchy

| Tier | Check                                          | Runs when                        |
| ---- | ---------------------------------------------- | -------------------------------- |
| 1    | structural validation (`skills-ref` validator) | every skill change               |
| 2    | trigger suite                                  | skill description change         |
| 3    | affected behavioral cases                      | skill behavior change            |
| —    | per-harness smoke check                        | packaging or install-path change |

## Running

- **Trigger suite.** Judge each query in a fresh context that sees only the
  skill name, description, and that query; require yes or no. One run per
  query. A first judgment that is `unsure` or hedged is borderline: run that
  query twice more. `unsure` counts as neither vote — a should-trigger query
  passes only with two categorical `yes` votes, a near miss only with two
  categorical `no` votes, and a completed three-run set without two
  categorical same-side votes fails. Any near-miss `yes` fails the suite
  immediately.
- **Behavioral case.** Fresh agent context, skill installed from current
  source, no other conversation state. The case file is self-contained: run
  its prompt, resolve fixture paths relative to the case file, grade each
  checklist item pass or fail, and record one log line.
- **Matched comparison (new skills and behavior-changing revisions).** A
  single-variant run only regression-checks an unchanged skill. A new skill
  or substantive revision runs its affected cases as matched pairs — without
  the skill (or the frozen prior version) and with the revised version, each
  in a fresh context — and ships only when the discriminating cases show the
  intended improvement with no regression. Log one line per graded variant.
- **Smoke check.** Install the skill from source into a disposable project on
  each roster harness — Claude Code and Codex CLI — ask one trigger query, and
  confirm from the run's trace that the copy which activated is the
  just-installed one (its path or base directory). When a same-name copy
  exists in a user or system location and the activated copy's provenance
  cannot be confirmed, log the result as inconclusive rather than pass. One
  log line per harness; if a roster harness is unavailable, log
  `not run — harness unavailable`. After a packaging change merges, repeat
  the probe once against the published default branch — installers pull
  from it, and local-source success does not prove remote resolution — and
  log that line too.

## Honest claims

A trigger-suite pass is a listing proxy, not proof of native triggering in a
harness — only a smoke check shows that. A log line states only what its run
actually checked.

## Privacy

No private meeting content, participant identities, account identifiers,
source URLs, vault names, or local absolute paths in any tracked test
artifact. Cases use synthetic data.
