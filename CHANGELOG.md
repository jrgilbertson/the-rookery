# Changelog

All notable changes to The Rookery are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
at the repository level. One version describes the whole collection.

Because installs pull from `main`, this file is the "what changed since you last
looked" surface. GitHub Releases mirror its entries.

## [Unreleased]

## [0.3.0] - 2026-10-15

This Release Snapshot records the catalog at one validated state. Ordinary
installs continue to follow rolling `main`. Before `1.0.0`, skill interfaces
and workflows may change between releases.

### Added

- `checking-simplicity` assesses safe ways to simplify a design, plan, codebase,
  or in-progress approach through one independent, read-only reviewer. It also
  handles explicit mid-build simplicity checks and proposed durable machinery
  that is not justified by the current need.
- `reviewing-ai-sessions` reviews session history for recurring friction and
  proposes evidence-backed changes to skills, rules, and enforcement. Maintain
  includes the review; applying specific proposals requires approval.
- `GLOBAL-AGENTS.md` publishes the maintainer's global guidance. The one-way
  sync script and opt-in pre-push freshness check keep it aligned with the
  configured local source.
- `SKILLS.md` defines repository package conventions and the evaluation workflow.
  A bounded `creating-portable-skills` suite uses stock Promptfoo providers for
  activation and a read-only portability audit in Claude and Codex. Subjective
  judgments remain provisional; strict capture and human calibration remain
  Unmeasured, and other packages await revalidation.
- `TESTING.md` explains project-owned verification, agent permissions,
  end-to-end checks, independent review, cache boundaries, and durable safeguards.
  New README and workflow illustrations introduce Huginn and Muninn and show
  delivery, maintenance, and learning.

### Changed

- `managing-issues` uses one canonical GitHub or Linear tracker for issue
  updates, parent and blocker relationships, readiness, and completion.
  First-use setup recommends an exclusive Linear readiness group and GitHub
  prefixed labels; existing configurations are not migrated. Explicit prior
  approval can cover routine reversible bookkeeping and predictable provider
  automation, while complete previews, readback, and approval for expanded
  scope remain required.
- `personal-chief-of-staff` provides guided source setup and a fictional starter
  map through host file tools. Version 3 maps roles to sources with optional
  harness access overrides; existing version 1 and 2 restrictions remain until
  an approved upgrade. Source examples distinguish templates, completed reviews,
  meeting evidence, approved notes, contact lookup, and durable records.
- Chief-of-staff wind-down separates approved corrections from tomorrow's
  planning and journal drafting. Daily and weekly reviews reconcile overdue,
  waiting, carried-over, and conflicting commitments; upcoming work feeds the
  plan. Coaching uses bounded Frontier Rounds, and Source Access Audits give
  concise coverage and claim limits.
- `creating-portable-skills` follows the Agent Skills format and delegates
  evaluation and corpus retuning to pinned upstream `build-eval` and `ce-retune`
  guides. Repository conventions remain in `SKILLS.md`. The review checklist
  and bundled signal scan support portable guidance without importing host
  procedure; required independent judgments cannot be supplied by the author.
- Repo Gardener uses a short policy with `protected_paths`, `max_pull_requests`,
  `scans`, `verify`, and optional `report_issue`. It senses one repository and
  dispatches bounded Executors through Compound Engineering publication and
  babysit; humans merge. Missing policy yields sense-only operation and an
  interactive setup proposal, with a later approval required before writing.
- Public X reads in CRM and chief-of-staff prefer Grok CLI when it provides the
  required capability and accept user-confirmed handles. A configured read-only
  API remains an alternative within the caller's limits.
- `ROUTING.md` is a human-facing role playbook; `WORKFLOWS.md` owns the workflow
  walkthroughs and `docs/model-evaluations.md` owns model-evaluation procedure.
  Ranked rows offer at most one model per provider. Gemini 4 Argon is provisional
  for Planner and Design/taste; Executor retains Opus 5.5 and Sol 6.1 without a
  tertiary. Evaluated effort and the maintainer's usual usage stay distinct.
- Working plans, brainstorms, raw dogfood notes, and point-in-time reports stay
  ignored. Durable outcomes belong in code, canonical docs, issues, ADRs, or
  maintained solutions. CI tool bootstrapping runs from a script to avoid an
  actionlint/ShellCheck pipe-buffer deadlock.

### Fixed

- Chief-of-staff reviews keep supplied results unverified, explain excluded
  source calls, and finish relationship judgment, task and inbox reconciliation,
  action dispositions, and calendar decisions before claiming completion.
- CRM uses bounded supported contact lookup after an empty unsupported phone
  search without weakening identity binding. Public X sandbox recovery requires
  fresh host approval and unchanged public query scope; turn exhaustion remains
  final, and unavailable reads retain Partial coverage.
- The portable-skill signal scan detects attached pressure markers, preserves
  whole-word text matching, and counts each matching line once. Unreadable
  inputs or reference traversal failures return errors instead of incomplete
  successful scans. The checklist keeps factual domain sentences even when
  they contain change words.

### Removed

- `checking-pr-readiness` and `checking-merge-readiness`, their helpers, and
  dedicated tests. Use Compound Engineering publication and babysit directly;
  Repo Gardener preserves verification, allowed-file boundaries, and human merge.
- `route-work`, introduced and retired between snapshots, and its bundled routing
  contract. Use `ROUTING.md` and invoke the chosen workflow or orchestration tools
  directly. For these three retired skills, interactive `npx skills update`
  detects upstream removals and offers to remove tracked local installations.
  Manually installed copies require separate removal.
- Repo Gardener's managed-run protocol, tracker records, scripts, and separate
  Executor contract. Existing `.agents/repo-gardener.yaml` files need the new
  policy keys; `maximum_workers` becomes `max_pull_requests`.
- Legacy behavioral suites, trigger lists, benchmarks, custom eval runners,
  schema checks, review server, cost tools, and simulators. Historical evidence
  remains in Git, but does not validate the replacement suite. Deterministic
  shipped-helper checks and safe synthetic fixtures remain.

## [0.2.0] - 2026-08-14

### Added

- Added the public OSS foundation: documentation, an MIT license, community
  templates, private security reporting, and a maintainer release checklist.
- Added a shared Lefthook `pre-push` check group and a read-only GitHub Actions
  workflow with the required check name `Tests Status`.
- Added repository and workflow banners with optimized GitHub display assets.
- Added `managing-issues` for GitHub and Linear issue relationships, readiness,
  approved updates, and evidence-based completion checks.
- Added `repo-gardener` for scheduled repository-health reviews that may carry
  one bounded improvement to an unmerged pull request.
- Added `storm-research` for source-backed research through independent
  practitioner, academic, skeptic, economist, and historian perspectives.
- Added `checking-merge-readiness` for a read-only whole-change review and a
  merge, debug, or do-not-merge recommendation.
- Added `checking-pr-readiness` for comparing a finished branch with its plan,
  checking the evidence, and surfacing unresolved risks before a pull request.
- Added `creating-portable-skills` for creating, revising, testing, and
  verifying the installation of skills across supported agent tools.
- Added `personal-chief-of-staff` for daily wind-down, weekly, and quarterly
  reviews with source checks and approval before changes are written.
- Added `managing-personal-crm` for relationship context, conversation prep,
  follow-ups, and staged note cleanup without a separate CRM database.
- Added `reviewing-meetings` for turning completed meetings into grounded notes
  and independently approved follow-up actions.

### Changed

- Expanded `WORKFLOWS.md` into the seven-job playbook and made the README the
  single public catalog for individually installable skills.
- Standardized skill tests around trigger contracts, runnable behavioral cases,
  concise run logs, matched comparisons, and per-tool installation checks.
- Defined `main` as the rolling install source and semantic-version Release
  Snapshots as immutable historical checkpoints rather than install pins.

## [0.1.0] - 2026-07-10

### Added

- Repository scaffolding: community files, issue and pull-request templates,
  the skills catalog layout, and the seven-job workflow map.
- The first repository rules for a curated catalog, rolling `main`, and
  installation parity.
