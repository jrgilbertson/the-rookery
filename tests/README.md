# Skill Test Suites

Conventions for the `tests/<skill-name>/` suites and the repository
checks. [`SKILLS.md`](../SKILLS.md) owns skill evals: files in each skill's
`evals/`, their formats, grading, and ship rule. Each suite here follows this
file until its skill's fix pull request moves it into `evals/`.

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
  committed. A behavioral run's note carries its tokens and duration, and the
  complete API-equivalent cost under `SKILLS.md`, or `cost not available` when
  usage or pricing is incomplete. An archive-pointer line identifies where prior history lives,
  so git remains the archive.
- optional `<name>-protocol.md` — a per-suite scoring or measurement protocol
  for recurring checks the suite runs against external or machine-local
  evidence. The protocol document defines how a check is scored; its results
  still land in `log.md` as ordinary convention-compliant lines, and any
  detailed bookkeeping the protocol needs lives with the evidence, outside
  these artifacts.

## Rules

- Use one or two sharp binary assertions per case, or one per numbered
  independent scenario. A case fails if any checklist item fails.
  Trigger judgments are yes or no. A quality that binary items cannot carry
  goes to human feedback or a blind comparison of two versions with the labels
  hidden, and is logged as a note, never as a pass or a fail.
- A case enters a suite when a baseline run showed the bare model failing the
  behavior or an observed failure motivated it — named in the provenance line.
  Realistic required behavior may also motivate a new-skill case without a
  no-skill baseline. A case that both variants pass may remain as an explicitly
  labeled regression control for a named contract; it proves no improvement.
- Roughly 10–15 active cases per skill is a ceiling for initial mining, not a
  target; steady-state suites grown by the observed-failure rule are expected
  to stay smaller.
- Git is the archive. Beyond the log format's required `git rev` field, no
  hand-recorded hashes, session IDs, evidence labels, or run ledgers in
  these artifacts.
- Checklists name data that changes between releases by its place in the
  contract, not by its current value. A `route-work` item says "the Planner
  primary" or "the Executor secondary", meaning that profile's slot in the
  model table of the package under test; the grader resolves the slot from
  that table, quotes the row it used, and expects the card to render it as an
  ordinary name. A prompt that must make a model unavailable names the slot,
  not the model. Provenance lines keep the names that were true when the
  failure was observed.
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

Regression checks and diagnostic comparisons use the baseline template's
Evaluation boundary: declare permitted resources, effects, and budget; use
synthetic inputs in isolated temporary workspaces; preserve existing authority
and ask for any additional authority or substantial unapproved cost. Keep raw
outputs outside the repository, including partial outputs from failed runs.
Execution claims require the final answer, all tool names and inputs, relevant
artifacts and observations, and available child readouts in the blind packet.
Exclude private reasoning and author conclusions; a different model grades.

- **Trigger suite.** Judge each query once by default in a fresh context that
  sees only the skill name, description, and query; require yes or no. A hedged
  or unavailable judgment stays unverified. The operator decides whether more
  evidence is needed within the authorized budget. These judgments are listing
  proxies. Native activation, including the separate training, validation, and
  fresh roles, follows [`SKILLS.md`](../SKILLS.md).
- **Behavioral case.** Fresh agent context, skill installed from current
  source, no other conversation state. The case file is self-contained: run
  its prompt, resolve fixture paths relative to the case file, grade each
  checklist item pass or fail, and record one log line.
- **Value assessment.** When the question is whether the skill helps, follow
  the matched with-skill and without-skill rule in [`SKILLS.md`](../SKILLS.md).
  Record that conclusion separately from shipping. An unresolved hold stays
  unresolved.
- **Regression check.** Follow `skills/creating-portable-skills/SKILL.md` and
  its baseline template: affected cases once per declared Executor target,
  with independent different-model blind grading. Inspect every failure against
  the original transcript and classify behavior failure, grader/assertion
  error, or capture gap. Retain original grades and explain corrections. A
  behavior check does not wait on a no-skill baseline.
- **Diagnostic comparison.** Compare or rerun the prior skill only on failing
  cases to attribute the change. Unresolved attribution remains unverified.
  A single-arm check or baseline subset proves no improvement, and unmatched
  cohorts get no aggregate delta. One independent review checks the package
  and evidence. A further round first inspects existing evidence and repairs
  grading, capture, or attributable skill failures, then names the decision,
  the result that would change it, the cases, and a spending limit inside the
  caller's authorized cross-provider budget; see [`SKILLS.md`](../SKILLS.md).
- **Human inspection.** The human inspects frozen cases before spend and the
  results afterward. Feedback preserves the original grades. The host command
  and manifest are
  [tools/eval-review/README.md](../tools/eval-review/README.md), as
  [`TESTING.md`](../TESTING.md) describes.
- **Smoke check.** Install the skill from source into a disposable project on
  each declared target harness (see [`TESTING.md`](../TESTING.md)), ask one
  trigger query, and
  confirm from the run's trace that the copy which activated is the
  just-installed one, including its package hash and install path under
  [`SKILLS.md`](../SKILLS.md). Evidence for a different hash applies to that
  other package. When a same-name copy
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
