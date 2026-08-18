# Concepts

Shared domain vocabulary for this project, including entities, named processes,
and statuses with a project-specific meaning. Prefer an established industry
term or a plain description. Add a project term only when it carries a precise
contract used in more than one place or names persisted compatibility data. Do
not capitalize ordinary workflow phrases merely to turn them into concepts.
This is a glossary, not a specification or catch-all.

## Personal workflows

### Meaningful Commitment

A reviewed next-day intention that connects current evidence or an explicit user
premise, a user-chosen outcome, and observable proof of completion.

It may be written as natural prose. If the user's exact wording omits one part,
preserve it but do not present it as complete. It records intent without
replacing task or calendar state.

### Source Access Audit

A temporary record, shown with one response, of which relevant sources were
checked, what each check found, and how access gaps affected the answer.

It is discarded after the response. It does not prove a claim, authorize a
change, or create stored state.

### Daily CRM Scan

A required wind-down check of configured relationship sources for the active
date window, run before the day's initial reconstruction.

It attributes interactions to known people and proposes only supported contact
updates or useful context. A short gap expands the date window; it does not
start a full CRM catch-up.

## Workflow processes

### Delivery Sequence

The five-job path from Research through Plan, Design, Build, and Ship. Each job
transforms a named input into an artifact the next job can use. Design is
conditional for interface work and continues through later delivery rather
than existing only as an isolated stop.

### Repository Learning Loop

The Maintain feedback loop that turns recurring repository problems into tests,
rules, reusable procedures, decision records, or documentation. It improves
future work throughout the Delivery Sequence, not only after Ship.

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

The single issue system allowed to receive updates for a repository. Copies
synced to another tracker may help identify or verify the issue, but they are
not a second place to write.

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

A record added to the pull request description after the owner approves a
readiness review. It summarizes plan fit, checks and evidence, unresolved gaps,
review findings, and any learning worth keeping.

The review assembles it in conversation. It becomes durable only when the
finishing workflow adds it to the pull request description.

### Merge Readiness Review

The pre-merge review produced by `checking-merge-readiness`. It checks whether
review is complete and merge rules pass, then examines the full pull request
for intent drift, Risk Drivers, redesign pressure, and follow-up debt.

It recommends merge, debug, or do not merge. It makes no changes; the owner
still decides and merges.

### Risk Driver

A low, medium, or high risk the owner should weigh before merging, tied to one
specific finding about the change or its review. A Merge Readiness Review uses
the named risks to recommend merge, debug, or do not merge.

## Repository gardening

### Repository Maintenance Run

One `repo-gardener` pass through `Sense -> Decide -> Act -> Verify -> Learn`.
It surveys nine maintenance areas and may carry one bounded improvement to an
unmerged pull request.

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

One context may grade a matched case while another performs the final review.
If no independent context is available, the result remains unverified until a
separate session can review a self-contained handoff.

### Degradation Path

A skill's defined behavior when something it prefers is absent, such as a
validator that cannot run, a companion skill that is not installed, or a tool
without a clean-context mechanism. The skill uses the best available substitute
and states what was skipped.

### Disposition List

A per-item record in a prune or restructure commit message that marks each
removed item as kept, folded into a named survivor, or dropped with a reason.
Folded items point to what replaced them, and retired names must disappear from
live references.

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
