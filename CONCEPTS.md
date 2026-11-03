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

## Issue management

### Canonical Tracker

The one issue system authorized to own a repository's issues and receive changes
to them. A cross-tracker request may reach its canonical record only through one
exact provider-native link; otherwise Managing Issues asks for the canonical
issue or stops. An issue in another tracker is not a second write target.

### Implementation Leaf

One issue whose deliverable and Verification boundary fit one independently
deliverable, reviewable pull request. A stacked PR series is one leaf only when
no PR in the stack delivers independently observable behavior; otherwise each
such PR is its own leaf. A single-leaf change needs no artificial parent.

### Ready Frontier

The implementation leaves in a requested issue family whose derived readiness
is `ready` and whose current native blockers and declared prerequisites are
satisfied. It is determined from a fresh read of the canonical tracker before a
handoff. It is never stored as a separate record of work status.

## Shipping and verification

### Install Probe

The per-harness smoke check proving that an exact skill revision installs
through the repository's documented path and activates on one trigger query.
A passing probe establishes installability and activation for that harness
only; it is not behavioral evidence. Runs before merge from the local source
and again after merge against the published state.

### Installation Parity

The maintainer installs from this repository exactly the way a visitor does.
Nothing in the [published catalog](skills/README.md) may depend on context
that exists only on the maintainer's machine, including absolute paths, private
names, or personal-environment assumptions. The repository text check rejects
local home-directory paths in tracked files; review covers private names and
other personal-environment assumptions. The rule binds from the moment the
repository declares itself public-bound, regardless of its current hosting
visibility.

### Release Snapshot

An immutable semantic-version tag and GitHub Release that identify one validated
state of the published catalog. It is a historical checkpoint with release
notes, not an installation pin: ordinary installs continue to follow `main`, and
a correction receives a new release tag instead of moving an existing one.

### Unmeasured

An evaluation result that was not collected or cannot be trusted, kept distinct
from both pass and fail. An Unmeasured result never counts toward a pass rate,
and an earlier run is not reclassified later to fill the gap.

## Research synthesis

### STORM Research

A deep, source-backed investigation that establishes what is already known,
assigns independent research perspectives, preserves their disagreements, and
combines the findings for the requested purpose. It asks questions about facts,
assumptions, constraints, mechanisms, system relationships, change over time,
and downstream effects without requiring a separate named question type. It may
inform a decision, but unlike `ce-pov`'s compact, project-grounded verdict it
preserves a multi-perspective research record as the primary result.
