# Changelog

All notable changes to The Rookery are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
at the repository level. One version describes the whole collection.

Because installs pull from `main`, this file is the "what changed since you last
looked" surface. GitHub Releases mirror its entries.

## [Unreleased]

### Added

- Added `route-work`, which returns one Route, Resume, or Questions card for an
  explicit routing request. Route cards select the first workflow, size a
  roster of roles, models, and effort for the expected run, and provide a
  standalone kickoff that preserves supplied authority. A public routing
  contract owns the behavior, with an exact parity check for its packaged
  reference.
- Added `checking-simplicity`, a read-only assessment that finds safe
  simplification opportunities in named technical areas, questions, proposed
  or existing designs, plans, code-level approaches, and in-build decisions.
  The assessment runs in one dispatched subagent that did not author or
  implement the subject. Lifecycle and Git hooks remain deliberately absent.

### Changed

- Repo Gardener is rewritten as one short skill for unattended runs. It
  starts only on an explicit invoke by name, reads a small
  `.agents/repo-gardener.yaml` (scope, protected paths,
  `maximum_workers`, approved scans, approved `verify` argv, optional
  report issue), runs the approved scans, senses five areas, and
  dispatches Executors that ship one PR each through `ce-work`,
  `ce-simplify-code`, `ce-code-review`, `checking-pr-readiness`,
  `ce-commit-push-pr`, and `ce-babysit-pr`, with
  `checking-merge-readiness` giving the final verdict in one plain
  morning report. Role names match `ROUTING.md`: Lead, Executor, Scout,
  Reviewer.

- Route kickoffs now require official provider CLIs with subscription
  authentication and report a blocker instead of using API-key billing.
  Astra at low replaces Sol at high as the secondary Lead profile.
  Sol at medium replaces Terra at high as the tertiary Executor profile.
  Astra at low replaces Sol at high as the secondary Design/taste profile.

- Routing templates now use square-bracket placeholders so Orca can open the
  routing contract in its rich Markdown editor.

- `checking-pr-readiness` and `checking-merge-readiness` spoken answers
  are the brief and numbered options only. The wait still happens; the
  owner no longer hears a closing paragraph about the skill, its headings,
  or why work has not started. The remaining-work follow-up uses the same
  bound.
- CI tool installation now runs from a shell script, avoiding actionlint
  deadlocks when local pipe buffers cannot hold the inline bootstrap code.
- After a `checking-pr-readiness` Approve, the option-1 reply follows
  `references/finishing.md`, which invokes the installed PR-opening skill
  once. An Executor is a run already executing the Executor contract; that
  file branches on that fact. An Executor uses `mode:pipeline` on the
  publisher, then `ce-babysit-pr mode:pipeline`. A non-Executor uses the
  default publisher. Title and body follow Compound Engineering. After
  babysit looks merge-ready, cautiously looks ready, or pipeline `success`,
  a non-Executor run starts `checking-merge-readiness` in a fresh Reviewer
  that owns the merge menu wait; an Executor reports to the Lead, which
  starts that Reviewer.
  Approve 1 does not merge. Before publishing, an Executor confirms every
  committed path is inside its brief's allowed files and outside
  protected paths. There is no gardener-only publisher.
- `checking-simplicity` now treats "check for simplicity as well" and
  unsolicited mid-build durable machinery as first-class triggers, instead of
  waiting for an explicit simplify request.
- `creating-portable-skills` also covers edits to an existing skill's
  `SKILL.md`, evals, graders, and trigger queries. Gotchas now keep host-repo
  rules out of portable skills and require evals and cases to shrink with the
  skill's intent.
- Ship workflow documents `no-ai-slop`, `humanize`, and
  `writing-for-agents` in the finishing sequence, with credit. Merge still
  waits for a human.
- `checking-pr-readiness` keeps one first-menu option for remaining work.
  Picking it does not start work. The follow-up's first action does all
  remaining items named in the brief; later actions are those items grouped
  by similar work and ordered by impact; leave is last and ends that
  wait. Unrun code review
  or simplify appear there only when they drove the recommendation. Run a
  missing step is no longer a sibling leftover-work row.
  `checking-merge-readiness` already uses one remaining-work option
  (Debug); Debug, redesign, and capture stay distinct action types, not
  item slots.
- `checking-merge-readiness` treats stale source-issue wording as
  informational when owner-approved scope, the PR description, and delivered
  work agree. Missing required work, incorrect closure claims, and authority
  or verification gaps still block merge.
- `checking-pr-readiness` treats reviewer file limits as informational.
  Unknown or exceeded limits alone no longer block PR approval or require
  vendor-plan research. Complete change inventory, actual required-review
  coverage, and exact identity checks still govern readiness.
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
- `managing-issues` first-use now recommends a Linear exclusive readiness group
  (`readiness` / `needs-discovery` / `needs-planning` / `ready`) and keeps
  GitHub prefixed flats. The config schema is unchanged. Already-configured
  repos are not migrated.
- Working plans, brainstorms, raw dogfood notes, and point-in-time reports now
  stay as ignored worktree artifacts. PR readiness rejects tracked or durably
  cited transient material, and merge readiness verifies issue stewardship
  against the final delivered scope without requiring a completion diary.
- `managing-issues` now handles authenticated GitHub and Linear creates, updates,
  relationships, readiness, and completion through one canonical tracker.
  First-use setup records only the provider, target, and metadata vocabulary.
  Cross-tracker requests require one exact provider-native link, and the skill
  writes only the canonical tracker. Linear uses connected MCP tools when
  available and keeps Orca as an explicit session choice.

### Removed

- Repo Gardener's managed-run machinery: the two-record tracker protocol
  and its scripts, caller-only mode, liveness reconciliation, revision
  check points, per-area mutation grants, the declared-audit sandbox, and
  the separate Executor contract. Existing `.agents/repo-gardener.yaml`
  files need the new keys.

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
