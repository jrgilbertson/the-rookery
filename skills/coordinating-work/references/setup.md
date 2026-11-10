# Setup

Read this when establishing collaboration or adopting an existing arrangement.
The entry skill owns shared authority, worker lifetime, working context, and
outcome requirements.

## Establish the intended arrangement

Use the invoking session as Coordinator unless the operator requested another
arrangement. Establish its actual runtime identity and supported coordination
authority; do not launch a duplicate Coordinator because this one lacks a
terminal handle.

Read the supplied objective, canonical work and project instructions, current
participants, and any existing coordination context. If several arrangements
plausibly match, obtain the missing selection before changing them. Adopt useful
existing roles, assignments, holds, and working context rather than recreating
them. An agent already working on the objective before setup, such as a chat
started for a batch, is a participant to adopt. When the guide cannot attach a
supervised Task to it, keep it as a message-assigned worker reached through the
guide's reference lookup, and include it in the stall sweep.

Propose only the roles and initial assignments the requested work needs. Planner,
Coordinator, and implementation workers are available roles, not a mandatory
hierarchy or fixed roster. Use a Planner for priority and brief work when chosen;
let the Coordinator turn approved work into assignments and return outcomes to
the Planner. Additional ongoing roles need a concrete responsibility, such as
maintaining a test environment or integrating a batch.

Use existing plans or the workflow that owns unresolved product planning. Setup
does not create a competing roadmap, issue database, or mandatory outer plan
for an ordinary CE task. Staffing, isolation, concurrency, and resource use
follow the native workflow and the operator's existing limits. On a shared
execution host, limit concurrent heavy jobs, such as verification, builds, and
browser runs, by measured CPU and memory rather than by participant count. Each
brief names the project's own metering helper, or, when the project has none, a
host command confirmed to measure CPU and memory.

## Propose before establishing

Inspect available provider/model/effort choices and placement support on each
execution host the guide can reach. Recommend where heavy workers run,
preferring a reachable host kept for development work over the operator's own
machine, and show the measured CPU and memory behind the recommendation; the
operator chooses the placement. Distinguish the Coordinator already running from
participants that need starting. Preserve evidenced settings for existing
participants; show the supported choices for new ones.

Present the entry skill's proposal, including reused participants, their task
ownership, initial workers to start, and the needed communication and supervision
arrangement. Do not start workers, allocate new tasks, create worktrees, install
ongoing monitoring, or change the team while the proposal is under discussion.
Read-only inspection and disposable proposal notes may proceed.

Resolve explicit edits in the same proposal interaction. Apply only after its
final effects are approved under the entry skill's approval rules.

## Establish and check

Immediately before affected changes, reconcile current ownership and any work
that completed during the discussion. Use the supported native operations for
the approved roles, assignments, settings, and execution placements. If the
current Coordinator lacks the required binding or authority, report that path
blocked instead of manufacturing a takeover.

Preserve native operation identities and receipts when an outcome is uncertain;
use the current guide's reconciliation path before another attempt. A partial
startup does not authorize duplicating successful workers or changing the
approved arrangement. Report unsupported branches separately.

Provide each participant its bounded assignment and access to canonical
context, current decisions, and the correct communication path. Establish the
ordinary native supervision the arrangement needs, reconciling any existing
monitoring first. The one periodic check allowed is a stall sweep at an
interval the operator approves. It looks only for a participant whose open
assignment has no hold or named dependency, that is idle at its prompt, with
no running job and no completion report, open question, or escalation since
its last assignment, and sends that participant a plain continue nudge. A
progress or status report does not exempt a participant. A participant that
stops after a helper returns sends no message, so no message-driven wait wakes
for it. Anything beyond that sweep is a second scheduler or a fixed tick
cadence; do not add one.

A Planner keeps no timer of its own. The Coordinator wakes it by message when a
pull request merges, a worker is freed or needs its next assignment, the
operator decides something that changes the plan, or a worker is stuck long
enough to put the plan at risk, and for anything else at its own judgment. The
Planner messages the Coordinator only with a ready brief, a risk, or a question
for the operator.

Verify the entry skill's individual outcomes, effective settings, communication,
and supervision. Leave only the missing recoverable context and its discoverable
reference for a future replacement Coordinator. Everyday work then continues
under existing authority; setup is not rerun for each issue or wave.
