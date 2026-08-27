# Changelog

All notable changes to The Rookery are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
at the repository level. One version describes the whole collection.

Because installs pull from `main`, this file is the "what changed since you last
looked" surface. GitHub Releases mirror its entries.

## [Unreleased]

### Changed

- `repo-gardener` policy now requires one owner-approved, normalized direct
  `setup_command`. First-use review carries it unchanged into later
  fresh-worktree setup, refuses invalid or unapproved commands locally, and
  leaves unrelated safe sensing available after an affected audit fails. Its
  command-string-wrapper refusal continues past documented or ambiguous
  wrapper launch operands without treating them as a script boundary, while
  documented no-operand flags and inline operands preserve script mode;
  BSD `env -P` is modeled as a path operand, and Node `data:` import or loader
  sources are refused before their nominal script file. Setup `env` wrappers
  now also reject every prefix `NAME=value` assignment rather than allowing it
  to configure a runtime before the approved command;
  PowerShell command-mode aliases and accepted prefixes are refused too across
  native one-dash, two-dash, and slash switch markers.
  Windows PowerShell requires explicit file mode, while PowerShell 7 retains
  positional file mode and recognizes documented file-mode aliases.
- README and `WORKFLOWS.md` now describe the catalog as a portable skill
  set inside a personal loop: `repo-gardener` listings stay two sentences,
  Orca is the IDE this workflow runs in rather than a requirement, `ce-plan`
  and grilling match their current upstream contracts, and
  `creating-portable-skills`, `personal-chief-of-staff`, `reviewing-meetings`,
  and `managing-personal-crm` appear in the walkthrough.
- `repo-gardener` can run exact owner-declared audit commands in its five
  eligible sensing lanes, with evidence-based setup recommendations, bounded
  direct execution, and existing candidate and reporting rules preserved.
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
