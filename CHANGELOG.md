# Changelog

All notable changes to The Rookery are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
at the repository level. One version describes the whole collection.

Because installs pull from `main`, this file is the "what changed since you last
looked" surface. GitHub Releases mirror its entries.

## [Unreleased]

### Changed

- Owner-facing readouts for `checking-merge-readiness` and
  `checking-pr-readiness` both use strict Minto pyramid shape (answer first,
  MECE supports, evidence only under load-bearing concerns, menu last) with
  harness-safe plain prose. Each skill carries its own contract; there is no
  shared presentation reference. Pre-PR gate still gathers full checks
  internally; only the spoken decision brief is pyramid.
- `checking-merge-readiness` is reframed as a pre-merge **global pass** (birth
  → tip design health, redesign pressure, follow-up debt) with a thin process
  residual and host merge-rule check (e.g. required conversation resolution).
  Tip movement after the last forge review is residual language at most, not a
  skill-invented hard stop that forces "tag a human." Three-light mapping is
  preserved. `checking-pr-readiness` and WORKFLOWS name complementary
  shipping-lane roles.
- `checking-merge-readiness` digests use Barbara Minto's pyramid principle:
  recommendation first, then only supporting points in natural prose (no em
  dashes). Clean green stays about twelve short lines; debug and do not merge
  grow only around real concerns. Medium risk is framed as **debug** (not a
  soft pause); do not merge is a hard stop that still leads to debug or
  redesign. Open PR state is not labeled redundantly. Skill body tightened;
  battery asserts answer-first order and clean-green length.

### Added

- `storm-research` runs source-backed investigation through isolated
  practitioner, academic, skeptic, economist, and historian lenses. It tests
  foundations, mechanisms, and system relationships during research, then
  returns an Overview-led, reader-focused briefing (action and limits in the
  Overview; later sections support that lead). It adapts to the requested
  deliverable and uses a binding independent check to preserve disagreement and
  keep material causal claims evidence-traceable.
- `checking-merge-readiness` digests a fully reviewed pull request before you
  merge it. It reads the description, diff, and review history, checks
  whether accumulated fixes drifted the change from its original intent, and
  profiles risk as graded named drivers anchored in an engineering-canon
  reference. Those roll into one of three recommendations: merge, debug, or
  do not merge. It is read-only and conversation-only, it treats every
  PR-derived text as untrusted input, and it never merges anything itself.
- `creating-portable-skills` is the first published skill. It creates new Agent
  Skills and helps review, update, or move existing skills. It starts from the
  user's goal, checks the package structure, compares behavior with focused
  tests, and verifies installability and activation with a per-harness smoke
  probe. It works without companion skills.
- `personal-chief-of-staff` guides wind-down (the sole daily close), weekly,
  and quarterly reviews using current data from the user's connected sources.
  It requires review before writing changes, handles Obsidian CLI operations,
  tests its behavior, and includes a versioned specification for three local
  Codex schedules.
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

- `managing-personal-crm` and `personal-chief-of-staff` can use authenticated
  Grok X search as optional, read-only relationship evidence. They prefer a
  known URL or handle when present, otherwise a short slice of the user's own
  recent directed posts and replies. They do not post on X or scan for posts
  to engage with.
- `storm-research` now permits an honest null lens contribution instead of
  forcing novelty, requires a complete material-claim source audit, and loads
  its full-briefing template only for output forms that need it.
- `storm-research` treats systems thinking as evidence-gated research depth
  (larger-system context and patterns over time when they change the answer),
  not a mandatory named report section. Formal models stay optional, and
  intervention stress-tests run only when the purpose calls for them.
- Build's orchestration guidance now treats Compound Engineering as the default
  planner, executor, and multi-agent reviewer inside a worktree. It drops the
  separate plan-execute-review row, warns against standing up a parallel stack
  beside the skills, and keeps other patterns for uncovered gaps; tiny one-off
  changes may still use a solo owner.
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
  opportunities in its wind-down and weekly reviews when Personal CRM is
  available.
- `personal-chief-of-staff` can now record three to five concrete next-day
  commitments with finish lines and user-approved rationales during wind-down
  when the configured journal section is available, apply quality gates at write
  time without a morning reaffirm step, deliver light focus/stop/more/less
  coaching every wind-down, and propose selective durable strategy or learning
  updates under separate approval.
- `personal-chief-of-staff` no longer ships a Morning mode or morning schedule.
  The daily path is wind-down only; generic daily review wording selects
  wind-down, and morning activation phrases are removed from the skill
  description.
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
