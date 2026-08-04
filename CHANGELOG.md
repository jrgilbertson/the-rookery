# Changelog

All notable changes to The Rookery are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
at the repository level. One version describes the whole collection.

Because installs pull from `main`, this file is the "what changed since you last
looked" surface. GitHub Releases mirror its entries.

## [Unreleased]

### Added

- `storm-research` runs source-backed investigation through isolated
  practitioner, academic, skeptic, economist, and historian lenses. It tests
  foundations, mechanisms, and system relationships during research, then
  returns an Overview-led, reader-focused briefing (action and limits in the
  Overview; later sections support that lead). It adapts to the requested
  deliverable and uses a binding independent check to preserve disagreement and
  keep material causal claims evidence-traceable.
- `creating-portable-skills` is the first published skill. It creates new Agent
  Skills and helps review, update, or move existing skills. It starts from the
  user's goal, checks the package structure, compares behavior with focused
  tests, and verifies installability and activation with a per-harness smoke
  probe. It works without companion skills.
- `personal-chief-of-staff` guides morning, wind-down, weekly, and quarterly
  reviews using current data from the user's connected sources. It requires
  review before writing changes, handles Obsidian CLI operations, tests its
  behavior, and includes a versioned specification for four local Codex
  schedules.
- `managing-personal-crm` keeps relationship context in canonical Person notes
  and Tasks. It captures updates, finds relevant context, prepares for
  conversations with one person, and proposes cleanup in stages. It matches
  identities carefully, proposes changes before writing them, handles mixed
  schemas during migration, and stores no hidden CRM state.
- `reviewing-meetings` reviews completed meeting evidence from any supported
  source. It prevents duplicate notes and tasks, sends each outcome to one
  canonical system, and applies only actions that the user approves
  independently. It also includes behavior tests with sanitized data and a
  versioned specification for the `CoS Meetings` schedule.
- `checking-pr-readiness` gates a branch before the pull request opens. It
  reports the full working surface including untracked files, verifies the
  shipping workflow's upstream steps from receipts rather than assertions,
  compares the plan against what was delivered, and sweeps the finding
  classes that drive repeated automated-review rounds with three falsifiable
  bundled helper scripts — the collection's first skill to ship executable
  helpers. It ends in one owner decision plus an evidence pack rendered into
  the pull request body, and its companions degrade to named skips when
  absent.

### Changed

- `storm-research` now permits an honest null lens contribution instead of
  forcing novelty, requires a complete material-claim source audit, and loads
  its full-briefing template only for output forms that need it.
- `storm-research` treats systems thinking as evidence-gated research depth
  (larger-system context and patterns over time when they change the answer),
  not a mandatory named report section. Formal models stay optional, and
  intervention stress-tests run only when the purpose calls for them.
- Planning now keeps Compound Engineering as the primary route and uses
  targeted grilling only as an optional pressure test for consequential,
  interdependent decisions that remain unclear.
- The skill test suites moved to a lightweight, rerunnable convention: each
  `tests/<skill>/` now holds a trigger contract, individually runnable case
  files with binary checklists, and a one-line-per-run log, with the
  convention itself documented once in `tests/README.md`. The prior evidence
  ledgers (Claim Ceilings, verification tiers, waiver records, hash tables)
  are retired; full history remains in git. `creating-portable-skills`'
  templates and workflow now produce the same lightweight shape, so newly
  authored skills follow it too.
- `creating-portable-skills` now grounds guidance in real project evidence,
  uses separate fresh-context agents for reviews and grading, inspects artifacts
  and execution traces directly, and tests activation with more realistic
  queries.
- `creating-portable-skills` ends read-only audits after delivering the
  review and keeps trigger descriptions positive. (An earlier unreleased
  revision also introduced verification tiers, a Claim Ceiling, and
  centralized evidence records; the lightweight testing convention above
  supersedes those before any release.)
- `personal-chief-of-staff` can now include relationship check-ins and timely
  opportunities in its morning, wind-down, and weekly reviews when Personal CRM
  is available.
- `personal-chief-of-staff` can now record three to five concrete next-day
  commitments with finish lines and user-approved rationales during wind-down
  when the configured journal section is available, reaffirm them in morning
  without creating another task or calendar system, and use repeated rationale
  patterns for selective non-scoring coaching.
- `reviewing-meetings` can now suggest contact dates, save useful relationship
  context, capture personal follow-ups, and surface relevant connections. Each
  meeting still produces one review bundle, and every approved action goes to
  one canonical destination.
- WORKFLOWS.md grew from an index into a full playbook. All seven walkthroughs
  are written from the workflow as it actually runs, connected by handoffs from
  Research through Learn, with a Foundations section, the model-selection
  objective functions, the orchestration table, and the durability ladder. The
  README's workflow bullets deep-link into each section.
- The README gained the guiding principles and the rookery framing, and
  `skills/README.md` now points at the README's list instead of repeating it,
  so the published catalog has one source of truth.

## [0.1.0] - 2026-07-10

### Added

- Repository scaffolding. Community files (MIT license, contributing guide, code of conduct, security policy), issue and PR templates, the skills catalog layout, and the seven-job workflow map across README and WORKFLOWS.md.
- The rules the repo lives by. Curated not collected, main is the install source, and the same-door rule.
