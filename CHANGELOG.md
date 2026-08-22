# Changelog

All notable changes to The Rookery are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
at the repository level. One version describes the whole collection.

Because installs pull from `main`, this file is the "what changed since you last
looked" surface. GitHub Releases mirror its entries.

## [Unreleased]

### Changed

- `repo-gardener` first-use now writes `.agents/repo-gardener.yaml` and creates
  a gardening tracker the way Managing Issues writes its config. A scheduled or
  manual run uses one Orchestrator that may assign parallel Workers, each with
  one unmerged pull request, up to `maximum_workers`. Depth has no count.
  Opened and closed tracker comments are the production records; a hash-linked
  register is not required. Unattended Workers open PRs only through
  assessment-only `checking-pr-readiness`. In-run `checking-merge-readiness` is
  read-only feedback and never merges.
- Working plans, brainstorms, raw dogfood notes, and point-in-time reports now
  stay as ignored worktree artifacts. PR readiness rejects tracked or durably
  cited transient material, and merge readiness verifies issue stewardship
  against the final delivered scope without requiring a completion diary.
- `repo-gardener` issue lanes now read their tracker from the repository's
  `.agents/managing-issues.json` when the managing-issues validator accepts it,
  and the issue-implementation lane limits candidates to issues whose mapped
  readiness is `ready`, whose mapped leaf estimate is a number at most 2, and
  which have no open native blocker. With no config file the lanes read the
  repository's own issues unmapped and name the absent config as their room
  for improvement; a config the run cannot validate, or a provider it cannot
  read, makes the lanes unavailable rather than substituting another tracker.
- `managing-issues` now handles authenticated GitHub and Linear creates, updates,
  relationships, readiness, and completion through one canonical tracker.
  First-use setup records only the provider, target, and metadata vocabulary.
  Cross-tracker requests require one exact provider-native link, and the skill
  writes only the canonical tracker. Linear uses connected MCP tools when
  available and keeps Orca as an explicit session choice.

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
