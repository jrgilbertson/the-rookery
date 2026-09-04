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

## Issue management

### Canonical Tracker

The one issue system authorized to own and receive mutations for a repository.
A cross-tracker request may reach its canonical record only through one exact
provider-native link; otherwise Managing Issues asks for the canonical issue or
stops. An issue in another tracker is not a second write target.

### Owned Issue Graph

The canonical issue family relevant to one requested outcome: its top parent,
all reachable descendants, and the native blocks or blocked-by relationships
that affect their readiness or completion. Relevant nodes outside the
repository's authority remain read-only boundary nodes rather than silently
disappearing from the graph.

### Implementation Leaf

One issue whose deliverable and Verification boundary fit one independently
deliverable, reviewable pull request. A stacked PR series is one leaf only when
no PR in the stack delivers independently observable behavior; otherwise each
such PR is its own leaf. A single-leaf change needs no artificial parent.

### Issue Readiness Posture

The issue's IDE-neutral information state: `needs-discovery` when the problem or
outcome is not understood, `needs-planning` when the outcome is understood but
Scope, Verification, decomposition, required metadata choices, or native
relationships remain unsettled, or `ready` when those facts are settled for its
role as a parent or leaf. It does not name or invoke a particular skill and
remains separate from dependency readiness, so a ready leaf may remain blocked
and outside the Ready Frontier.

### Ready Frontier

The implementation leaves in an Owned Issue Graph whose Issue Readiness Posture
is `ready` and whose current native blockers and declared prerequisites are
satisfied. It is derived from a fresh canonical read for a
handoff and is never stored as a parallel work state.

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

A record added to the pull request description after option 1 approves a
readiness review. It is an actionable brief: the recommendation, material next
work, a coverage close, and the learning signal, not a census of every sweep
class or inspected path.

The review instantiates it on later 1 as silent pull-request-body input.
It becomes durable only when the finishing workflow writes it into the
pull request description.

### Merge Readiness Review

The pre-merge review produced by `checking-merge-readiness`. It checks whether
review is complete and merge rules pass, then examines the full pull request
for intent drift, Risk Drivers, redesign pressure, and follow-up debt.

It recommends merge, debug, or do not merge, then waits for a numbered reply.
Gather, grade, and readout stay read-only. Option 1 is Proceed to merge.
Before merging, it confirms the pull request has not moved, then kicks off
the forge merge. A match is silent; a mismatch names what moved and rebuilds
rather than merging. It still does not mutate the tracker. The skill does
not pick option 1 in the same turn that wrote the menu.

### Risk Driver

A low, medium, or high risk the owner should weigh before merging, tied to one
specific finding about the change or its review. A Merge Readiness Review uses
the named risks to recommend merge, debug, or do not merge.

## Repository gardening

### Repository Maintenance Run

One `repo-gardener` pass through `Sense -> Decide -> Act -> Verify -> Learn`.
An Orchestrator surveys nine maintenance areas and may assign multiple
Workers, each taking one independently deliverable, reviewable pull request.
When that work is an issue, it is an Implementation Leaf.

### Orchestrator

The agent of a Repository Maintenance Run that senses, decides, assigns
Workers, writes the Gardening Tracker, and produces the morning summary.
It does not implement, push, or merge.

*Avoid:* parent, gardener parent

A run has one Orchestrator. It selects a non-overlapping set of pull-request-sized
units, then starts Workers in parallel up to that run's ceiling.

### Worker

An isolated worktree agent assigned one independently deliverable, reviewable
pull request. It owns that work through an unmerged pull request. The pull
request may be an existing one the run adopts; the Worker then owns that PR's
branch for the run. When the work is an issue, that issue is an Implementation
Leaf.

*Avoid:* child, gardener child

A Worker may use helpers for scouting, simplification, review, pull-request
readiness, and merge readiness. Helpers do not own a pull request. One Worker
ships at most one pull request. Merge remains a later human step.

### Census

A cheap listing of one source population, such as issues, pull requests, or
alerts. It runs during a Repository Maintenance Run and during caller-only
sensing. Census totals are reported separately from candidates. Completing a
census is not reading bodies and is not emitting candidates.

### Gardening Tracker

The GitHub issue holding append-only run history for one repository. Its body
is setup information; each Repository Maintenance Run writes one opened comment
and one closed comment containing the morning report. Native pull requests
remain authoritative for authored work.

### Run History

The append-only comment history on the Gardening Tracker. Each Repository
Maintenance Run adds one opened record and one closed record. History supplies
visibility, not a lock, queue, authority grant, or planning-quality verdict.

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

## Flagged ambiguities

- "Parent" and "child" in gardener talk meant Orchestrator and Worker. Those
  words remain Orca worktree roles and issue-graph relationships; they are not
  gardener roles.
