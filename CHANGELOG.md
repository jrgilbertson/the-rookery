# Changelog

All notable changes to The Rookery are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
at the repository level. One version describes the whole collection.

Because installs pull from `main`, this file is the "what changed since you last
looked" surface. GitHub Releases mirror its entries.

## [Unreleased]

### Added

- Repository text checks reject concrete local home-directory paths, with
  file-scoped exceptions for reviewed portable setup examples.
- `coordinating-work`, an optional Orca-first skill for collaboration setup and
  revive, with editable approval, task-scoped PR workers, and recovery of
  context, communication, and supervision through existing native workflows.
- An automation catalog with prompts, schedules, prerequisites, and Orca setup
  instructions for session, test, CI, codebase design, and coding standards
  reviews. README, workflow, testing, product, and contribution guidance now
  explain how scheduled reviews fit into the working system.
- Shared run state for the automations: every prompt reads and writes one
  private Git repository, cloned on each host, so runs on different machines
  see earlier findings and the owner's decisions. `automations/README.md`
  explains why and carries the run contract as a template to copy.

### Removed

- `repo-gardener`; recurring repository reviews now use Orca automations, and
  approved changes use the existing Compound Engineering workflow.
- Repository-specific GitHub issue forms and the pull request template, so
  issues and pull requests can use freeform bodies.
- `reviewing-ai-sessions`; the Sessions audit automation supplies the recurring
  review prompt directly.
- The custom `creating-portable-skills` evaluation harness, exporter, dedicated
  tests, and runner-specific instructions, along with the speculative cases
  and judges. Behavioral evaluation uses the evals plugin's `evals-start`
  routing and selects a runner when needed.

### Changed

- The Sessions audit prompt starts with `/retro`, because `retro` hides itself
  from model invocation, and runs `checking-simplicity` on each draft
  recommendation before the `ce-pov` review. The Analytics gap audit loads
  `instrument-product-analytics` through the PostHog MCP instead of an
  installed plugin skill.
- The Weekly codebase design, Coding standards audit, Optimize CI, Test audit,
  and Analytics gap audit prompts also run `checking-simplicity` on each draft
  recommendation before the `ce-pov` review, matching Sessions audit, and list
  `checking-simplicity` among their requirements.
- Agents no longer install a skill candidate locally before merge. The
  `coordinating-work` test notes drop their pre-merge install step, the Install
  Probe runs after merge as a maintainer step, and the release checklist has
  the maintainer install from `main` and confirm every bundled helper is still
  executable in the installed copy.
- Global agent guidance permits Compound Engineering reviews through existing
  sign-in accounts after naming the model, while excluding credentials and
  personal data.
- Test audit recommendations are prioritized by risk and impact without a fixed
  finding limit, so material findings are not omitted to keep the report small.
- Global agent guidance asks for an independent review from a different model
  family on changes to authorization, approval, destructive-action guards, money,
  data deletion, privacy boundaries or release gates, a failing-first test for
  each confirmed bypass, and a second review when fixes change the logic.
- Global agent guidance lets an agent merge a pull request when the user asked
  for the merge, in the task or in standing instructions, and its required
  checks pass with no open review thread. Deploying and force-pushing still
  need the user, and repository guidance can grant exceptions only for spending.
- `coordinating-work` assignment briefs name only commands confirmed on the
  worker's host, carry current decisions rather than declined proposals, and
  ask workers to wait for long-running checks inside their own turn. Operator
  decisions go to the canonical tracker before the Coordinator acts on them.
- `coordinating-work` starts task workers through Orca's supervised launch,
  so the runtime can flag a worker that stops without reporting, and revive
  tells a worker with an open assignment to continue it in the same turn.
- `coordinating-work` freezes an assignment's brief once it is dispatched.
  Only the Coordinator changes it, through a dated amendment that names what
  it supersedes, and each worker re-reads its amendments at every step
  boundary and names in its reports the latest one its work follows. Revive
  carries the brief with its amendments, and the resumed worker confirms the
  latest one.
- `coordinating-work` starts each assignment on a fresh branch from the
  latest default branch and has workers update their branch before each
  verification run, names the message type for questions, blockers,
  completions, and progress, and has the Coordinator wake the Planner by
  message instead of a timer.
- `coordinating-work` lets the Coordinator run an operator-approved stall
  sweep that nudges only idle participants with an unheld open assignment, no
  running job, and no completion report, open question, or escalation since
  that assignment, and still bans any other second scheduler. It
  confirms that an idle participant read a message and reads the effective
  account from the running agent rather than launch metadata. Briefs say a
  returning helper skill does not end a worker's turn, and on a shared host
  heavy jobs are limited by measured CPU and memory. Cleanup checks unpushed
  work against the default branch and pull request head, not the upstream
  alone. Revive lists background jobs and relaunches only those confirmed
  stopped unfinished, lets running paid work reach an idle point, and checks a
  usage-limited participant's background jobs before reassigning it.
- `coordinating-work` briefs ask that a security re-review prompt state its
  threat model, and that a worker whose last two review rounds found only new
  instances of one class fix that class structurally or ask the Coordinator,
  instead of patching each new instance.
- `coordinating-work` setup adopts an agent already working on the objective,
  such as a chat started for a batch. When the guide cannot attach a
  supervised Task to it, the Coordinator keeps it as a message-assigned worker
  reached through the guide's reference lookup and includes it in the stall
  sweep.
- `personal-chief-of-staff` finds a source map moved into a designated vault
  or workspace through an approved pointer in an instruction or configuration
  file the host loads for that workspace, after any location the caller
  supplies. A named location that cannot be read is a gap rather than a
  reason to use the default, and moving the map proposes removing the previous
  copy. Vault-owned maps are `.json` files read
  and saved through the Obsidian CLI, and `reviewing-meetings` reads a supplied
  map through its owning system the same way.
- Global agent guidance tells a delegating agent to rely on a delegate's watch
  and to report a merge-queue enqueue instead of polling it. The paid-call
  exception for live browser testing moves to the repositories that grant it;
  the rule to mock models in automated tests stays global.
- Evaluation policy allows targeted synthetic discovery, precise-constraint
  checks, and useful regression coverage while keeping evaluator investment
  proportional to observed failures and cost. New skill delivery does not
  require an invented corpus, grader, or case count. Concrete eval work retains
  input/grading approval and execution limits.
- Repository agent guidance points skill changes to the package and evaluation
  policy, and directs implementation and debugging to relevant prior solutions.
- Managing Issues explicitly checks a newly created Linear issue's parent,
  direct children, and other relationships before continuing an approved batch.
- Model routing explains cost per pass and effort gains, separates evaluation
  sources from role selection, and distinguishes calculation inputs from
  supporting evidence. Current recommendations record subscription and access
  overrides and identify provisional Planner choices.
- Setup and automation guidance calls for initial setup or recovery and repeat
  operation checks in the first implementation slice, with pending activation
  tracked explicitly.
- Testing guidance names the repository-owned commands as completion evidence
  and asks filtered check output to keep the check's own exit status.
- Checking Simplicity no longer requires four options for every question.
- Creating Portable Skills reviews flag opaque prose: instructions a new reader
  cannot follow, internal classifications, and security jargon.
- Managing Issues fixture checks no longer carry synthetic provider adapters
  that only tested themselves. Graph and lifecycle expectations are retained as
  behavioral case definitions awaiting native-host evaluation; incidental prose
  changes no longer fail graph checks.
- `GLOBAL-AGENTS.md` matches the maintainer's current global guidance.
  Non-trivial work names a verifiable end state without a completion
  template. Long work uses the workflow's durable task state, and scratch
  work stays disposable. The published copy no longer specifies a work-folder
  checklist, a headless `ce-compound` pass, or a version-control section.
  Stop and ask before reducing scope, merging, deploying, spending money,
  or force-pushing.
- `GLOBAL-AGENTS.md` asks agents to judge a check by its own exit status,
  since a filtered pipeline such as `check | tail` reports the filter's status
  unless `pipefail` is set.
- `GLOBAL-AGENTS.md` lets active browser testing make paid model calls on
  non-production keys without asking. Automated test suites still mock the
  model, and evals, batch model runs, and production work still need approval.
- `SKILLS.md` lists what retiring a skill includes, including closing or
  re-scoping its open issues in the same change.
- Personal Chief of Staff fixture checks validate the shipped source-map
  sample directly instead of a test-only copy of the schema.
- Repository docs keep one owner per rule. `creating-portable-skills`'s
  `references/evaluation.md` owns evaluation policy, and the other docs link to
  it; `SKILLS.md` keeps only this repository's evidence rules. `CONCEPTS.md`
  drops ten terms used in at most one other file and states what checks
  Installation Parity. Stale pointers, a restated sync-script header, and a
  duplicate `checking-simplicity` summary are gone. `SKILLS.md` notes that
  this repository rejects `allowed-tools` and adds uninstalling from each host
  to retiring a skill.
- Automation schedules all use America/Los_Angeles, and starts on the same
  host sit at least an hour apart (Weekly codebase design moves to Saturday
  04:00). Test audit runs `ce-simplify-code` as a report of what it would
  change, ordered by priority, instead of applying fixes. The README lists
  Analytics gap audit. CI no longer installs PyYAML, which no
  Python check imports.

### Fixed

- The opt-in `GLOBAL-AGENTS.md` freshness check compares the configured source
  with the copy on `origin/main`, and with `HEAD` only when the branch edits the
  copy. Branches started before the copy was refreshed on `main` no longer fail.
- `coordinating-work` asks for operator decisions to be recorded in their
  owning record, says a worker's question is sent with the `ask` command, and
  has workers wait for long-running checks with a tracked background wait.
  The automation run contract template no longer calls itself canonical.
- Automation prompts now tell each run to update the shared run-state
  repository and follow its README, which owns the run contract. The README
  template names reports in UTC with seconds, matching the live contract.
- Repository verification bounds malformed inline-link scanning and treats YAML
  filenames as data. Guidance synchronization replaces destination symlinks
  safely, skill scans preserve pathname boundaries, and evaluation imports
  reject nonregular or oversized setup records.
- Managing Issues reads back a new Linear issue's relationships. A
  relationship Linear adds on its own, which nobody approved, stops the batch
  before the next write and comes with a removal preview awaiting approval.
- Repository verification rejects tracked files under the root `outputs/`
  directory, which may hold private generated artifacts.
- Repository tests now fail when the issue-configuration label, duplicate,
  control-character, or size guards are removed, when the README skill list
  or a skill name drifts from `skills/`, or when a test runner is missing from
  the fixture roster.

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
