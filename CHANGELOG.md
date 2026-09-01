# Changelog

All notable changes to The Rookery are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
at the repository level. One version describes the whole collection.

Because installs pull from `main`, this file is the "what changed since you last
looked" surface. GitHub Releases mirror its entries.

## [Unreleased]

### Changed

- Repo Gardener's Worker mutation boundary is now host-neutral: it requires an
  isolated worktree at the authoritative base, host-provided setup when
  available, supervised completion, and a Worker-owned branch with one
  unmerged PR. Setup must succeed before repository work, and a clean native
  Git status is required before the first mutation; unavailable safe mutation
  falls back to a truthful read-only report.

- `checking-pr-readiness` and `checking-merge-readiness` now split gather from
  the spoken brief. Helper inventories go to an owner-only temp directory
  outside the target repository. The brief is an executive recommendation
  plus numbered live options, a coverage close, and named next work instead
  of a receipt-vouch or a per-class census. A non-terminal Show the checks
  option lists each applicable check and its status on request. There is
  one process: wait for a numbered reply from whoever is talking. A turn is one reply: this reply
  writes the menu and stops; the next message is the pick. This turn ends
  when the menu is on screen. Option 1 is Approve or Proceed. Before that
  choice is accepted, identity is re-read, including staged, unstaged, and
  untracked content for PR readiness.
  Matching identity compares stay silent; a moved head or working-tree
  content change rebuilds. A check named as next work, including code
  review with no receipt, does not by itself withhold Approve. Spoken next
  work is remaining owner work after the decision. On approve that is
  opening the pull request and babysitting it, not unrun review or
  simplify. Live options are numbered from 1, each number once. On
  approve, Run a missing step is omitted rather than listed once per gap.
  Reasons in the brief are about the change under review, not how the gate
  runs. Captured as
  `docs/solutions/conventions/do-not-split-human-and-agent-skill-products.md`.
- Repo Gardener now completes its issue identifier census before every
  issue-facing lane uses purpose-ranked, admission-bounded reads, preserving
  trusted-principal and lane limits. Mapped readiness now prioritizes those
  reads rather than excluding a `needs-planning` estimate-2 issue whose
  repository evidence supports a safe Worker brief, and the Ready Frontier
  remains fresh after an authorized issue refinement.
- Repo Gardener now has a default-off `issue_refinement` policy grant that can
  delegate one caller-authorized canonical issue batch to Managing Issues while
  preserving its existing pre-read, apply-once, first-stop, and exact-readback
  safeguards.
- Repo Gardener can treat configured ledger paths as an assignment-only overlap
  exception after repository proof of conflict-safe additive merging, while
  requiring each Worker to retain base entries and add its own attributable
  entry; the Orchestrator never writes the shared ledger or resolves later
  native merge or rebase conflicts.
- Repo Gardener now gives every unattended Worker the normal
  `checking-pr-readiness` process: its menu reply ends that turn, and only the
  Orchestrator may authorize option 1 when Approve was offered and recommended
  for that exact head. Named Worker-owned gaps from one brief all go back to
  that Worker; owner-needed briefs stop without a PR. After a PR exists, the
  scheduled ownerless run invokes merge-readiness and never selects Proceed to
  merge.
- `personal-chief-of-staff` Source Access Audits are now a short paragraph:
  coverage first, then every relevant role and how the read finished, with a
  "so" clause only when a result limits a claim. No table and no HTML
  details. Successful reads may share a sentence.
- Interactive `checking-merge-readiness` option 1 (Proceed to merge) now
  kicks off one forge merge after the existing fingerprint and host-policy
  re-check, using the repository's default merge method. A cold "merge this
  PR" activates the skill but still requires that menu choice.
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
  register is not required. An unattended Worker stops after the normal
  `checking-pr-readiness` menu; the Orchestrator authorizes option 1 only from
  an approve brief for that exact head, or sends named Worker-owned gaps back.
  After a PR exists, the scheduled ownerless run invokes merge-readiness and
  never selects Proceed to merge.
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
