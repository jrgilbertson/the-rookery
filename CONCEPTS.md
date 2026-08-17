# Concepts

Shared domain vocabulary for this project, including entities, named processes,
and statuses with a project-specific meaning. Prefer an established industry
term or a plain description. Add a project term only when it carries a precise
contract used in more than one place or names persisted compatibility data. Do
not capitalize ordinary workflow phrases merely to turn them into concepts.
This is a glossary, not a specification or catch-all.

## Personal workflows

### Meaningful Commitment

A reviewed next-day intention recorded during wind-down. It visibly connects the current authoritative evidence or labeled user premise, the user-owned desired outcome, and the future observable evidence that will show completion, with a concise rationale for why it matters. These meanings may read as natural prose rather than labeled fields. Exact user wording that omits one remains visible as nonconforming input and is not certified as a complete commitment. When the live daily-journal template includes a configured Meaningful Commitments section, that journal carries three to five of them as next-day intent; without the section, ordinary next-day planning continues. They express intent without replacing canonical task state or calendar capacity, and they do not require a separate morning reaffirm step.

### Source Access Audit

A required, conversation-only account of the relevant source roles considered for one visible personal-chief-of-staff response. For each role, it records the bounded current-response access attempt and result (`Accessed — evidence found`, `Accessed — no relevant evidence`, or `Attempted — unavailable or failed`), or an explicit no-attempt classification (`Not configured`, `Declined`, or `Not needed`), plus the effect on that response's findings. It is reconciled from those attempts and classifications, rendered after the answer-first synthesis, and discarded after the response. It is not a source registry, claim-provenance ledger, approval, freshness record, or new source of truth.

### Daily CRM Scan

Required wind-down pass over configured relationship interaction sources for the active scan window, run before the initial reconstruction whether or not a candidate person already surfaced. Default window: closing local day. After a short miss of one or two immediately prior local days (missing prior journals), expand over those days plus the closing day as a catch-up breath. Attribute messages by sender; evaluate substantive direct contact for each bindable person; leave unknown handles unresolved. Covers contact-date outcomes and selective durable meaning. Separate from prepare-tomorrow’s overdue / useful-tomorrow exception check. Excludes CRM catch-up mode, exhaustive history, and indiscriminate Person-note creation.

## Workflow processes

### Delivery Sequence

The five-job path from Research through Plan, Design, Build, and Ship. Each job
transforms a named input into an artifact the next job can use. Design is
conditional for interface work and continues through later delivery rather
than existing only as an isolated stop.

### Repository Learning Loop

The Maintain feedback path that observes recurring signals across the Delivery
Sequence and encodes each lesson at the strongest durable layer that can hold it,
preferring enforceable layers when available. It improves future work
throughout the system rather than beginning only after Ship.

### Personal Learning Loop

The Learn feedback path that turns experience into linked personal knowledge,
names the gap that remains, and returns a better question to Research. It is
distinct from the Repository Learning Loop because it improves the operator's
understanding rather than the repository's safeguards and procedures.

### Grilling Session

A targeted, stateless interview for resolving one coherent decision tree whose
answers depend on one another. The agent recommends answers and looks up
discoverable facts. The user makes each decision.

## Issue management

### Canonical Tracker

The one issue system authorized to own and receive mutations for a repository.
When another tracker synchronizes the same issue, that copy is a projection or
alias used for identity and readback evidence, not a second write target.

### Ready Frontier

The required open leaf issues in the canonical parent-and-blocker graph whose
current native blockers and declared prerequisites are satisfied. It is
derived from a fresh canonical read for a handoff and is never stored as a
parallel work state.

## Shipping and verification

### Published Catalog

The skills available for individual installation from this repository.
Installers read the default branch, so anything merged there becomes available
immediately. That branch stays install-clean. A skill is published once it
appears in the catalog and installs on its own.

### Install Probe

The per-harness smoke check proving that an exact skill revision installs
through the repository's documented path and activates on one trigger query.
A passing probe establishes installability and activation for that harness
only; it is not behavioral evidence. Runs before merge from the local source
and again after merge against the published state.

### Installation Parity

The maintainer installs from this repository exactly the way a visitor does.
Nothing in the published catalog may depend on context that exists only on the
maintainer's machine, including absolute paths, private names, or
personal-environment assumptions. A verification sweep enforces the rule
across shipped files. The rule binds from the moment the repository declares
itself public-bound, regardless of its current hosting visibility.

### Release Snapshot

An immutable semantic-version tag and GitHub Release that identify one
validated state of the Published Catalog. It is a historical checkpoint and
release-notes surface, not an installation pin: ordinary installs continue to
follow `main`, and a correction receives a new release tag instead of moving an
existing one.

## Readiness checkpoints

### Evidence Pack

The structured record a readiness checkpoint composes when the owner approves:
plan-vs-delivered status, checks run with results, the explicit not-verified and
attested list, sweep findings, UI critique scores when present, and the durable
learning signal. The checkpoint only composes the pack into its readout;
durability begins when the finishing path renders it into the pull request
description, which is its durable home — the pre-merge checkpoint reads it back
from there. Nothing is written to the tracked tree or any local state store.

### Merge Readiness Review

The pre-merge readout `checking-merge-readiness` composes before the owner
merges. It first checks whether review is complete enough to assess and whether
the host's merge rules pass. It then reviews the full change from pull-request
open to tip for intent drift, graded Risk Drivers, redesign pressure, and
follow-up debt. Those findings produce one recommendation: merge, debug, or do
not merge. The review lives in the conversation and changes nothing, so the
owner still does the merging.

### Risk Driver

A named, graded (low / medium / high) finding in a Merge Readiness Review: one
specific thing about the change or its review that an owner
would want to weigh before merging. Principle-tension classes cover
complexity accretion, knowledge duplication, and speculative generality.
Other classes cover unresolved review items, cross-round fix interaction,
material security concerns, and PR text that tries to steer the assessment.
Drivers roll up into one merge-risk grade; a word grade traceable to a named
driver is used instead of a numeric score.

## Repository gardening

### Repository Maintenance Run

One repository-scoped execution of `Sense -> Decide -> Act -> Verify -> Learn`.
The parent surveys nine lanes, may deepen current signals, and may supervise a
live-policy-bounded child through an unmerged pull request. The model owns
qualitative judgment; deterministic code checks only tracker-record closure.

### Current Portfolio

A legacy report projection retained for history-chain compatibility during
early dogfooding. It is not a queue or ownership database. Native pull requests,
branches, heads, checks, and states are authoritative for authored work.

### Run History

The complete structurally hash-linked receipt history from genesis, with
unverified provenance. New gardening runs add only `run-opened` and
`run-closed` receipts. Legacy kinds remain readable. History supplies
visibility, not a lock, queue, authority grant, or planning-quality verdict.
The full readable kind inventory is `decision`, `effect`, `evidence`,
`manifest`, `release`, `run`, `run-opened`, `run-closed`, and `scout`.

### Scout Receipt

A legacy per-lane terminal record retained in older history. Current runs place
all nine lane results in the consolidated closing record instead of writing
nine separate managed comments.

### Register Revision

A monotonic body version stored as `register_revision` and used to detect stale
preparation and bad readback. It is not an atomic provider precondition,
compare-and-swap, or distributed lock.

### Effect Receipt

The intended-effect and terminal-outcome evidence for one stable,
repository-qualified logical report operation, stored with the `effect` receipt
kind. Its identity is the pair `(repository_id, operation_id)`, not the
operation ID alone. The intended receipt is read back before invoke; the
terminal receipt is read back after the authoritative post-read. Ambiguity
blocks blind retry.

### Attention State

The report projection `Action required`, `Merge-ready`, `Watching`, or
`Routine`. Attention communicates current handling; it is not a persisted work
state or authority grant.

### Completion Partition

The disjoint, exhaustive pair `affected_work` and
`remaining_unblocked_work`. Every named item appears exactly once, and every
unblocked remainder is continued, durably delegated, or gated by its own named
prerequisite.

## Research synthesis

### STORM Research

Deep, source-backed investigation that establishes a baseline, dispatches
independent research lenses, preserves their disagreements, and synthesizes the
result for the requested purpose. It asks questions about facts, assumptions,
constraints, mechanisms, system relationships, change over time, and
downstream effects without requiring a separate named question type. It may
inform a decision, but unlike
`ce-pov`'s compact, project-grounded verdict it preserves a multi-perspective
research record as the primary result.

## Skill quality gates

### Baseline Comparison

A Baseline Comparison checks whether a skill changes agent behavior in the
intended direction. New skills run realistic prompts with and without the skill;
revisions compare the frozen prior and revised versions, each in a fresh
context with the intended variant confirmed loaded. Cases are binary
pass/fail, and a substantive revision ships only when the discriminating
cases show the intended improvement with no regression. The repository's
testing convention owns the protocol.

### Independent Review Context

An Independent Review Context is a fresh session in which the reviewing agent
neither saw the artifact's authoring discussion nor produced the artifact.

One context may grade a matched case, while another performs the final holistic
review. Deterministic scripts remain appropriate for mechanical checks. If an
independent context is unavailable, the affected result stays unverified and
moves to a separate session through a self-contained handoff.

The run's log line names the fresh-context mechanism used (a fresh session,
CLI execution, or subagent); recorded context identifiers are not kept in
test artifacts. The named mechanism does not replace artifact or trace
evidence for the judgment made in that run.

### Degradation Path

A skill's defined behavior when something it prefers is absent, such as a
validator that cannot run, a companion skill that is not installed, or a tool
without a clean-context mechanism. The skill uses the best available substitute
and states what was skipped.

### Disposition List

A Disposition List is the per-item record a prune or restructure leaves in its
commit message: each removed item marked kept, folded into a named survivor,
or dropped with a reason. It is a checkable contract, not a narrative — a
folded claim must point to the surviving line that carries the contract, a
dropped claim must hold against its rationale, and a retired claim must
survive a search for live references. Verified dispositions are what make
git-as-archive recovery trustworthy.

### Delete Test

The instruction-economy check asks one question for every line: would the agent
get this wrong without it? A line that restates default model behavior fails and
is cut whole. The test decides only whether to keep the line. The separate
operationalize-the-qualifier check handles words that survive but still steer
unpredictably.

### System-Owned Invariant

A hard constraint that stays explicit because the user or surrounding system
owns it. Examples include portable formats, user authority, deterministic
validation, exact output requirements, and fragile operation order. Generic
reminders to think, narrate, or recheck may be removed when they no longer help.

### Trigger Contract

A Trigger Contract treats a skill's description as a tested activation API,
not documentation. At the fire-or-skip decision, the agent sees only the
skill's name and description. Test this metadata with should-trigger phrasings
that must activate and near-misses that must not, judged in fresh contexts
under the repository's testing convention.
