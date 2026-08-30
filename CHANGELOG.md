# Changelog

All notable changes to The Rookery are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
at the repository level. One version describes the whole collection.

Because installs pull from `main`, this file is the "what changed since you last
looked" surface. GitHub Releases mirror its entries.

## [Unreleased]

### Changed

- Repo Gardener can treat configured, repository-proven union-merge ledger
  paths as an assignment-only overlap exception while requiring each Worker to
  retain base entries and add its own attributable entry; the Orchestrator
  never writes the shared ledger.
- Repo Gardener now assesses PR readiness directly or through a report-only
  merge-readiness review, then can return a current, actionable finding to the
  same Worker without exposing a merge path.
- Repo Gardener now rereads native state after Worker responses and either
  gives a focused next instruction or explains why it stops.
- Assessment-only `checking-pr-readiness` now reports same-session exact-head
  findings and rejects a moved native head without requiring receipt packaging.
  An ownerless `repo-gardener` Worker may open one PR only on that readable
  ready result; otherwise its commit remains `saved_without_pr` with the gap.
- `personal-chief-of-staff` Source Access Audits are now a short paragraph:
  coverage first, then every relevant role and how the read finished, with a
  "so" clause only when a result limits a claim. No table and no HTML
  details. Successful reads may share a sentence.
- Interactive `checking-merge-readiness` option 1 (Proceed to merge) now
  kicks off one forge merge after the existing fingerprint and host-policy
  re-check, using the repository's default merge method. A cold "merge this
  PR" activates the skill but still requires that menu choice. Unattended
  `repo-gardener` runs still never select option 1 and still never merge.
- `managing-personal-crm` can recover one bounded public X read after a
  sandbox network or session-state denial only with fresh host approval and
  enforced read-only capabilities. It rejects private-derived query scope,
  keeps turn exhaustion final, and preserves Partial coverage when X is
  unavailable.
- README and `WORKFLOWS.md` now describe the catalog as a portable skill
  set inside a personal loop: `repo-gardener` listings stay two sentences,
  Orca is the IDE this workflow runs in rather than a requirement, `ce-plan`
  and grilling match their current upstream contracts, and
  `creating-portable-skills`, `personal-chief-of-staff`, `reviewing-meetings`,
  and `managing-personal-crm` appear in the walkthrough.
- `repo-gardener` can run exact owner-declared audit commands in its five
  eligible sensing lanes, with evidence-based setup recommendations, bounded
  direct execution, and existing candidate and reporting rules preserved.
- `repo-gardener` declared audits now consume an Orca Setup receipt only when
  the host exposes one: configured terminals wait, `not_configured` is a no-op,
  and compatible no-receipt hosts proceed without waiting. They preserve their
  approved argv and record a missing package runner or nested executable
  locally while sensing and independently qualified Worker selection continue.
- `repo-gardener` now creates each fresh Worker through supervised Orca
  dispatch with repository setup enabled, waits for configured setup before
  repository work, and requires a clean native Git status immediately before
  the first mutation without adding setup or Git-state machinery.
- `repo-gardener` now retains the supervised Orca worker-start receipt in the
  Orchestrator, so a Worker that starts while setup runs uses its existing
  current-Dispatch observation as a one-time gate and pre-Worker start
  failures remain caller-owned without retrying setup.
- `repo-gardener` now uses native Orca setup only to gate repository work:
  after a successful or no-op receipt, Workers run relevant documented
  verification commands unchanged as ordinary gates and report each actual
  pass, failure, or unavailable result without installing or substituting an
  environment.
- `repo-gardener` list-style censuses of issues, pull requests, and alerts
  keep listing while remaining items are knowable and the count is under
  10,000, once per population, rather than stopping at a stated page bound.
  A named bound or omission keeps the affected lanes partial. An
  empty-complete census is absence evidence for a zero-item population. The
  dependency lane consumes the Orchestrator open-PR identifier census. The health lane
  consumes the issue-source census when that source exists. Overlap rereads
  list current native PRs instead of that sensing census. Scout census
  handoff is compact rows or a per-run temporary file outside the worktree.
- `repo-gardener` first-use now writes `.agents/repo-gardener.yaml` and creates
  a gardening tracker the way Managing Issues writes its config. A scheduled or
  manual run uses one Orchestrator that may assign parallel Workers, each with
  one unmerged pull request, up to `maximum_workers`. Depth has no count.
  Opened and closed tracker comments are the production records; a hash-linked
  register is not required. Unattended Workers open PRs only through
  assessment-only `checking-pr-readiness`. In-run `checking-merge-readiness` is
  read-only feedback and never merges.
- `repo-gardener` now parses `.agents/repo-gardener.yaml` once with PyYAML
  SafeLoader and the existing field schema. Lane inventory uses that mapping
  instead of a second regex grammar. Tags, aliases, merge keys, nulls, and
  duplicate keys still fail closed. Developer installs need PyYAML.
- `managing-issues` first-use now recommends a Linear exclusive readiness group
  (`readiness` / `needs-discovery` / `needs-planning` / `ready`) and keeps
  GitHub prefixed flats. The config schema is unchanged. Already-configured
  repos are not migrated.
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
