# Changelog

All notable changes to The Rookery are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
at the repository level. One version describes the whole collection.

Because installs pull from `main`, this file is the "what changed since you last
looked" surface. GitHub Releases mirror its entries.

## [Unreleased]

### Changed

- `repo-gardener` now returns safe, actionable readiness findings to the
  owning Worker in progress-bound repair batches before and after PR creation.
  Each reassessment is bound to a new exact head, repeated findings keep their
  fingerprint across irrelevant commits, process-only caps remain recorded,
  and `checking-merge-readiness mode:agent` returns a report-only structured
  assessment that cannot present an owner choice or merge. Worker-owned
  shipping now uses a secretless broker that revalidates the exact delivery
  tuple, while uncertain PR creation accepts only one OPEN PR matching the
  exact host/repository, head repository, Worker branch, and authorized full
  head OID; all stale, closed, unavailable, or mismatched results remain saved
  pushed state without a retry. Agent-mode actionability now binds the complete
  protected-path policy identity and revision, preserves the certified full
  host/owner/name identity, and rechecks its gathered snapshot before return.
  Repeated readiness-gap keys are now equality-only correlation evidence, so
  another bounded repair cycle requires LLM judgment of keyed findings, exact
  diff, repair explanation, and fresh verification rather than key recurrence;
  empty, irrelevant, unsafe, unauthorized, unknown, or unverified progress
  still stops truthfully, including a regression or invalid evidence/effects.
- `repo-gardener` now supervises Workers from current native branch, HEAD,
  process, PR, check, and result facts. TUI idle is only a scheduling hint;
  bounded no-progress analysis becomes a local stall, head drift refreshes
  assessment evidence, uncertain pushes reconcile the remote before retry,
  unavailable remote-head reads remain `UNKNOWN` without retry or settlement,
  and other unavailable recovery facts remain `UNKNOWN`.
- Assessment-only `checking-pr-readiness` now checks every known automated-
  reviewer cap independently. Exact-head no-cap evidence records the resolved
  reviewer, authoritative source, and successful lookup outcome as process-
  only summary evidence without an unresolved sweep finding or material gap;
  it cannot mask another reviewer's excess. Unresolved identities, failed or
  incomplete lookups, unmeasurable surfaces, and unknown effects remain
  fail-closed.
- Assessment-only `checking-pr-readiness` now emits
  `checking-pr-readiness-assessment/v2` material gaps as minimal,
  producer-owned `{key, message}` objects. Keys are equality-only correlation
  evidence for atomic, independently repairable receipt and evidence
  obligations: they remain stable across exact heads and message rewrites,
  while a malformed outer assessment claim with a missing, empty, duplicate,
  extra-field, or malformed key produces one valid `UNKNOWN` envelope; inner
  evidence receipt gaps remain unchanged.
- Assessment-only `checking-pr-readiness` now separates substantive exact-head
  evidence from receipt packaging. One complete same-session bundle may carry
  digest-matched evidence and results outside the assessed commit, and missing
  published per-kind schema documentation or an alternate result location is
  no longer a stop by itself. Inline evidence/result bytes bind the exact
  repository, subject, revision, bundle, and receipt identity, so missing,
  stale, mixed, cross-boundary, or unsupported evidence remains
  `action-required`.
- `repo-gardener` now carries portable Worker lineage facts: source
  Orchestrator identity, exact Git base, setup result, Worker branch, and
  returned native identifiers. Orca records a parent-worktree link when it is
  available; other harnesses record `lineage capability unavailable` while
  preserving the same facts, and mismatches stop before implementation.
- `repo-gardener` now treats declared gate-prerequisite health as a setup
  outcome. A required unhealthy prerequisite blocks only its dependent gate and
  work, while an unavailable optional environment blocks only its affected
  gate; exact-head readiness rechecks the Worker environment without skipping,
  weakening, or substituting a gate.
- `repo-gardener` now verifies setup with a byte-aware clean snapshot. It
  reports exact staged, unstaged, non-ignored untracked, tracked-byte, and
  `skip-worktree` or `assume-unchanged` flag changes without repairing them;
  ignored runtime output remains allowed and unrelated safe work continues.
- `repo-gardener` now runs the exact owner-approved `setup_command` once in
  every fresh Orchestrator and Worker worktree, after instruction discovery and
  before repository-dependent audits or implementation. Worker envelopes carry
  the argv unchanged; setup failure remains local, setup-argv drift stops
  before execution, and a skipped or failed base-ref refresh is a named host
  gap rather than authority to substitute a command or base.
- `repo-gardener` policy now requires one owner-approved, normalized direct
  `setup_command`. First-use review carries it unchanged into later
  fresh-worktree setup, refuses invalid or unapproved commands locally, and
  leaves unrelated safe sensing available after an affected audit fails. Its
  command-string-wrapper refusal continues past documented or ambiguous
  wrapper launch operands without treating them as a script boundary, while
  documented no-operand flags and inline operands preserve script mode;
  BSD `env -P` is modeled as a path operand, and Node `data:` import or loader
  sources are refused before their nominal script file. Setup recursively
  unwraps leading `env` wrappers and rejects every pre-utility operand with a
  nonempty name before `=` rather than allowing it to configure a runtime
  before the approved command;
  PowerShell command-mode aliases and accepted prefixes are refused too across
  native one-dash, two-dash, and slash switch markers.
  Windows PowerShell requires explicit file mode, while PowerShell 7 retains
  positional file mode and recognizes documented file-mode aliases.
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
