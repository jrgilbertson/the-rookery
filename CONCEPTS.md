# Concepts

Shared domain vocabulary for this project, including entities, named processes,
and statuses with a project-specific meaning. Prefer an established industry
term or a plain description. Add a project term only when it names a precise
requirement used in more than one place or stored data needed for compatibility.
Do not capitalize ordinary workflow phrases merely to turn them into concepts.
This is a glossary, not a specification or catch-all.

## Personal workflows

### Meaningful Commitment

A reviewed next-day intention that connects current evidence or an explicit user
premise, a user-chosen outcome, and observable proof of completion.

It may be written as natural prose. If the user's exact wording omits one part,
preserve it but do not present it as complete. It records intent without
replacing task or calendar state.

### Source map

A private map from chief-of-staff information roles to user-designated sources.
It records ownership, native access details, and user-approved source
restrictions, not source contents or access results. Workflows select which
roles to read and when, within those restrictions.

### Access override

A complete native access description for one explicitly identified harness in
a source binding. It changes how that harness reaches the designated source;
ownership and shared read bounds remain with the binding.

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

### Administrative Sweep

A check of canonical records during a wind-down or weekly review. It proposes
exactly one action that can be approved separately for every record the evidence
shows is wrong or needs a decision. This includes overdue, follow-up-due, and
at-risk tasks. Upcoming tasks normally feed the plan instead: tasks due tomorrow
in Wind-down or in the coming week in Weekly. The sweep proposes an action for
an upcoming task only when the plan cannot accommodate it. Wind-down runs the
sweep as its first phase and applies and reads back approved actions before
coaching or journal drafting begins. Weekly runs the sweep while reconstructing
the week and carries its rows into the single review bundle presented at the end
of the run. It lists nothing that is healthy and never creates a second task
list.

### Frontier Round

One numbered batch of at most five independent questions, each with a
recommended answer, presented in plain chat and answered in one reply. A
question enters only when its answer could materially change the
recommendation, plan, or interpretation and its prerequisites are settled;
dependent questions wait for the next round. A round with zero questions is
valid.

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

### Owning Workflow

The one existing workflow responsible for resolving a request's current
uncertainty or producing the lasting result it asks for. A route assessment
names exactly one first owner based on the work requested, rather than how the
request arrived. Later workflows take over only if needed and do not share
current ownership.

## Issue management

### Canonical Tracker

The one issue system authorized to own a repository's issues and receive changes
to them. A cross-tracker request may reach its canonical record only through one
exact provider-native link; otherwise Managing Issues asks for the canonical
issue or stops. An issue in another tracker is not a second write target.

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
satisfied. It is determined from a fresh read of the canonical tracker before a
handoff. It is never stored as a separate record of work status.

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

An immutable semantic-version tag and GitHub Release that identify one validated
state of the Published Catalog. It is a historical checkpoint with release
notes, not an installation pin: ordinary installs continue to follow `main`, and
a correction receives a new release tag instead of moving an existing one.

### Unmeasured

An evaluation result that was not collected or cannot be trusted, kept distinct
from both pass and fail. An Unmeasured result never counts toward a pass rate,
and an earlier run is not reclassified later to fill the gap.

## Repository gardening

### Repository Maintenance Run

One unattended `repo-gardener` pass that senses one repository, dispatches
Executors, and reports. CI remains the merge gate. A report with no
Executor is a complete run.

### Coordinator

The agent of a Repository Maintenance Run that senses, decides, assigns
Executors, and produces the morning summary. It does not implement, push, or
merge.

*Avoid:* Orchestrator, parent, gardener parent

A run has one Coordinator. The overnight pattern is Coordinator + Executors.
The Coordinator selects a non-overlapping set of pull-request-sized units, then starts
Executors in parallel up to that run's ceiling.

### Executor

An isolated worktree agent assigned one independently deliverable, reviewable
pull request. It owns that work through an unmerged pull request it authors.
When the work is an issue, that issue is an Implementation Leaf.

*Avoid:* Worker, child, gardener child

An Executor may dispatch Scouts for evidence. It verifies its unit, publishes
through Compound Engineering, and runs babysit when publication has not already
handed off monitoring. It reports the PR URL, CI state, babysit result, and
unresolved decisions to the Coordinator. A pipeline result does not prove that
the interactive monitoring period completed or that the PR merged. Scouts and
Reviewers do not own a pull request. One Executor ships at most one pull
request. Merge remains a later human step.

### Gardening Tracker

The optional GitHub issue (`report_issue`) that receives one plain report
comment per Repository Maintenance Run. It holds no managed records or
markers. Native pull requests remain authoritative for authored work.

## Research synthesis

### STORM Research

A deep, source-backed investigation that establishes what is already known,
assigns independent research perspectives, preserves their disagreements, and
combines the findings for the requested purpose. It asks questions about facts,
assumptions, constraints, mechanisms, system relationships, change over time,
and downstream effects without requiring a separate named question type. It may
inform a decision, but unlike `ce-pov`'s compact, project-grounded verdict it
preserves a multi-perspective research record as the primary result.

## Instruction and workflow contracts

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

This check asks one question for every line: would the agent get this wrong
without it? A line that restates default model behavior fails and is cut whole.
The test decides only whether to keep the line. The separate operationalize-the-qualifier check makes remaining vague qualifiers specific enough to guide the
agent consistently. The skill review checklist names this check No-ops.

### System-Owned Invariant

A hard constraint that stays explicit because the user or surrounding system
owns it. Examples include portable formats, user authority, deterministic
validation, exact output requirements, and fragile operation order. Generic
reminders to think, narrate, or recheck may be removed when they no longer help.

### Trigger Contract

A Trigger Contract treats a skill's description as the activation API the
harness shows when deciding whether to load the skill. Should-trigger
phrasings must load it, and near-misses must not. A listing proxy judges the
name and description alone. Native activation observes the harness's load
decision, with training, validation, and fresh queries kept distinct.

## Flagged ambiguities

- "Parent" and "child" in gardener talk meant Coordinator and Executor. Those
  words remain Orca worktree roles and issue-graph relationships; they are not
  gardener roles. `ROUTING.md` describes Planner, Executor,
  Reviewer, and Design/taste as model profiles, not a separate routing process.
- A session coordinating ordinary work may also implement it; a gardener
  Coordinator never implements. Shared role names do not imply identical
  responsibilities across workflows.
