# Changelog

All notable changes to The Rookery are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
at the repository level. One version describes the whole collection.

Because installs pull from `main`, this file is the "what changed since you last
looked" surface. GitHub Releases mirror its entries.

## [Unreleased]

### Added

- Added `checking-simplicity`, a read-only assessment that finds safe
  simplification opportunities in named technical areas, questions, proposed
  or existing designs, plans, code-level approaches, and in-build decisions.
  The assessment runs in one dispatched subagent that did not author or
  implement the subject. Lifecycle and Git hooks remain deliberately absent.

### Changed

- `checking-pr-readiness` treats reviewer file limits as informational.
  Unknown or exceeded limits alone no longer block PR approval or require
  vendor-plan research. Complete change inventory, actual required-review
  coverage, and exact identity checks still govern readiness.
- `repo-gardener` requires five explicit maintenance areas: dependency
  maintenance, engineering health, issues and feedback, documentation, and
  runtime reliability. Each repair has one owner by its intended remedy;
  security and measurement remain cross-cutting evidence. Retired `lanes`
  policies are rejected, with no inferred grants. Replacement requires review
  of the complete policy and its five mutation grants, preserving tracker history.
- `repo-gardener` permits concurrent independent additions to shared ledger-like
  files marked `merge=union` at the captured base, including unrelated branches
  and assignments. Complete native branch/PR inventories and overlapping diffs
  must prove every base entry is preserved at dispatch and each publication
  gate. No peer registry is required; ownership, adoption authority, scope,
  and publication leases remain unchanged. The Orchestrator never writes the
  shared ledger; later integration conflicts remain owner work.

- `repo-gardener` writes append-only opening and closing comments; the closing
  comment contains the morning report and the issue body remains setup text.
  The complete report renders literally in a helper-generated fence, preserving
  technical names and inert markup. Canonical nested JSON payloads survive
  serialization and exact readback.
  Tracker writes no longer coordinate a body update with a comment or carry
  operation hashes. Run IDs use a fresh UUID instead of a minute-resolution
  timestamp. A full tracker stops new openings before verification input
  capacity is exhausted and requires owner-managed replacement. Before
  upgrading a test install, stop its scheduler,
  confirm old Orchestrators and Workers have terminated, and use a fresh
  tracker if its records use the retired format.
- `repo-gardener` accepts area mappings in any YAML order and uses PyYAML's
  native parser for syntax checks. Issue admission rests on trusted ownership,
  current blockers, and a small, low-risk, verifiable PR scope; estimates and
  readiness labels are hints. Runtime reads verify each source independently
  and distinguish empty results from missing data. Bot adoption reports the
  risk of stopped updates or overwritten edits without promising bot behavior.
  Worker briefs bind the expected repository identity.
- `repo-gardener` adopts an open same-repository update PR with a
  Worker-closable gap as a Worker unit: the Worker checks out the PR head at
  the captured OID, pushes under an expected-remote-OID lease, keeps one
  unmerged PR, and never merges. Initial adoption requires a non-draft PR with
  bot- or app-authored head commits; default and provider-protected heads cannot
  be adopted. Authorized Worker pushes advance the lease expectation after
  exact readback while the original scope baseline stays fixed. Adopted PR titles and descriptions stay unchanged; readiness
  evidence goes into the run report. Overlap is changed-path intersection with
  other native branches and PRs; an intersection that fails the shared-ledger
  exception, including substantive lockfile overlap, stops the dependent action.
  The runtime reliability area reads any error or alert source the host can
  already read and confirms identity from repository facts. A blocked
  opening still senses and reports with one `caller-only` run outcome.
- `personal-chief-of-staff` wind-down now runs in two visible phases. Phase 1
  sweeps the day's corrections and resolves each row, applying approved
  actions with readback, before Phase 2 begins. Phase 2 plans tomorrow, coaches, records
  commitments, and drafts the journal from the state Phase 1 left behind, so
  the journal describes the sources as they now stand. A scheduled run stops
  at the Phase 1 bundle and ends Paused with nothing applied.
- `personal-chief-of-staff` wind-down and weekly reviews now sweep the task
  source. An open task due on or before the closing day, past its follow-up date,
  at risk against the remaining capacity, or holding a due date
  that precedes its own earliest-begin date becomes one approvable row with a
  proposed resolution. Zero rows is a valid result, and an unreachable task
  workflow reports the rows Manual rather than stalling the review. Upcoming
  tasks enter tomorrow's plan or the whole coming week's plan, including its
  first and last days; they need correction rows only when capacity cannot
  hold them. Capacity checks start on the first planning day or the task's
  later earliest-begin date. Due-date conflicts qualify even before either date
  has passed.
- `personal-chief-of-staff` coaching follow-ups now arrive as a Frontier Round:
  a numbered plain-chat batch of at most five independent questions, each with
  a recommended answer, ordered by how much the answer would change the
  recommendation. Dependent questions wait for a later round. Weekly asks one
  round rather than two, Quarterly presents its dispositions the same way, and
  a supported coaching claim names the pattern, its cost, the recommended
  boundary, the smallest intervention, and the evidence that would settle it.
- Skill test suites may retain a small number of explicitly labeled regression
  controls for load-bearing behavior that the bare and skilled variants both
  pass; those controls never count as evidence of improvement.
- `checking-pr-readiness` now inventories solution simplicity, the
  independent approach-level result from `checking-simplicity`, as a sixth
  upstream step and late backstop, and `checking-merge-readiness` requires a
  fresh whole-change reviewer before it can recommend merge.
- A later reply of 1 on a `checking-pr-readiness` Approve menu continues into the
  installed finishing path in the same conversation. The evidence pack is
  silent pull-request-body input, not another wait. If no finishing path is
  installed, the run names that once and stops without re-asking Approve.
- `checking-pr-readiness` and `checking-merge-readiness` keep option 1 as the
  reserved Approve or Proceed slot. When that action cannot be taken, number
  1 stays and names why. The remaining actions have a print order, not fixed
  menu numbers. Live later options are numbered from 2 without gaps. Each
  option is a natural sentence rather than a label. Show the checks lists
  the checks this review ran. File or capture follow-up appears only when
  the brief named leftover work to park. Request changes stays on every
  PR-readiness menu as the numbered alternative to Approve. `ce-pov` stays
  a merge-readiness action only on do not merge when that skill is present.
  A typed 1 on a withheld option-1 row is not Proceed or Approve.

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
- Repo Gardener completes a quick available-input pass across all five areas
  before dispatch, using native filters and selective body reads, then deepens
  decision-relevant investigations while Workers progress. Issue discovery
  starts with open, ready work at mapped estimates 1–2 and broadens when useful;
  missing estimates or readiness mappings do not permanently exclude work.
  Reports state query filters, windows, limits, counts, and inspected coverage
  without claiming backlog exhaustion. The Ready Frontier uses current evidence
  and fresh native blocker reads. Tracker reads and conflict inventories remain
  complete at their required gates.
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
- `repo-gardener` can run exact owner-declared audit commands in dependency
  maintenance, engineering health, and documentation, with evidence-based setup
  recommendations, bounded direct execution, and existing candidate and reporting
  rules preserved.
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
  SafeLoader and the existing field schema. Area inventory uses that mapping
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
- `repo-gardener` issue discovery now reads its tracker from the repository's
  `.agents/managing-issues.json` when the managing-issues validator accepts it,
  and issue-requested implementation requires trusted ownership, a safe Worker
  brief, and no open native blocker. With no config file it reads the
  repository's own issues unmapped and names the absent config as a limitation;
  a config the run cannot validate, or a provider it cannot read, makes
  issue-source coverage unavailable rather than substituting another tracker.
- `managing-issues` now handles authenticated GitHub and Linear creates, updates,
  relationships, readiness, and completion through one canonical tracker.
  First-use setup records only the provider, target, and metadata vocabulary.
  Cross-tracker requests require one exact provider-native link, and the skill
  writes only the canonical tracker. Linear uses connected MCP tools when
  available and keeps Orca as an explicit session choice.

### Removed

- `repo-gardener` no longer accepts `issue_refinement`, `evidence_sources`, or
  `shared_ledger_paths` in `.agents/repo-gardener.yaml`. Remove those keys on
  upgrade. Follow-up issues remain owner proposals for Managing Issues outside
  the nightly run; Managing Issues no longer accepts gardening delegation
  envelopes as approval. The shared-ledger overlap exception is keyed on the
  git `merge` attribute being `union` at the authoritative base. The references are one owner per rule:
  `applying-effects.md`, `github-reference-adapter.md`, and
  `register-and-report.md` became `tracker-records.md`; everything a Worker
  follows lives in `worker-contract.md`, which also defines overlap; revision
  check points are listed once. `release_a_contract.py` exposes three
  subcommands (`normalize-github-tracker`, `effect`, `run-records`) with no
  version suffix in any name; only the unversioned `orchestrator:run-record`
  markers are recognized.
  Gone: the external recovery-state persistence before a tracker write, the
  host execution-profile test (declared audits now run in an explicit child
  environment built from nothing), the code-health rotation cursor,
  per-candidate label-provenance reads, and the `#3336`, Current Portfolio,
  and presentation-cap pilot residue.

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
