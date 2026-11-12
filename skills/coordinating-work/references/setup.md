# Setup

Read this when establishing an arrangement or adopting an existing one. The
entry skill owns shape, shared authority, worker lifetime, the record, and
outcome requirements.

## Establish the intended arrangement

Use the invoking session as Coordinator unless the operator requested another
arrangement. Establish its actual runtime identity and supported coordination
authority; do not launch a duplicate Coordinator because this one lacks a
terminal handle.

Read the supplied objective, canonical work and project instructions, current
participants, and any existing record. If several arrangements plausibly
match, obtain the missing selection before changing them. Adopt useful
existing assignments, holds, and working context rather than recreating them.
An agent already working on the objective before setup, such as a chat started
for a batch, is a participant to adopt. When the guide cannot attach a
supervised Task to it, keep it as a message-assigned worker reached through the
guide's reference lookup, and include it in the stall sweep.

Propose only the initial assignments the requested work needs. Dispatch from
the canonical tracker's ready issues, with the issue as the source of each
brief. Setup does not create a competing roadmap, issue database, or mandatory
outer plan for an ordinary CE task. Staffing, isolation, concurrency, and
resource use follow the native workflow and the operator's existing limits. On
a shared execution host, limit concurrent heavy jobs, such as verification,
builds, and browser runs, by measured CPU and memory rather than by
participant count. Each brief names the project's own metering helper, or,
when the project has none, a host command confirmed to measure CPU and memory.

## Propose before establishing

Inspect available provider/model/effort choices and placement support on each
execution host the guide can reach. Recommend where heavy workers run,
preferring a reachable host kept for development work over the operator's own
machine, and show the measured CPU and memory behind the recommendation; the
operator chooses the placement. Distinguish the Coordinator already running from
participants that need starting. Preserve evidenced settings for existing
participants; show the supported choices for new ones.

Present the entry skill's proposal, including reused participants, their task
ownership, and initial workers to start. The proposal also states, so that one
approval covers them:

- **The batch.** List the issues this arrangement may dispatch. The
  Coordinator dispatches nothing outside it.
- **What a merge starts.** State what merging to the default branch triggers
  here, such as a deploy, a release, a migration, or a paid job.

- **The merge bar and the hold classes.** Show the defaults from
  [Operate](operate.md). When the project's own guidance defines a merge bar
  or hold classes, show those instead and say where they came from. The
  operator may edit either.
- **The standing instruction not to wait.** State it as the operator's
  instruction: the Coordinator never stops for an answer, decides a default
  as Operate describes, and logs the question. An installed guide that says
  to ask the user first yields to this instruction once it is approved.
- **Where the record lives.** Name a durable, private location on the
  Coordinator's host, as the entry skill requires.
- **The stall-sweep interval.**

Approval of the proposal is the standing merge grant for this arrangement and
records the instruction not to wait. Write the approved proposal to the record
before starting anything.

Do not start workers, allocate new tasks, create worktrees, install ongoing
monitoring, or change the team while the proposal is under discussion.
Read-only inspection and disposable proposal notes may proceed. Resolve
explicit edits in the same proposal interaction. Apply only after its final
effects are approved under the entry skill's approval rules.

## Establish and check

Immediately before affected changes, reconcile current ownership and any work
that completed during the discussion. Use the supported native operations for
the approved assignments, settings, and execution placements. If the current
Coordinator lacks the required binding or authority, report that path blocked
instead of manufacturing a takeover.

A partial startup does not authorize duplicating successful workers or changing
the approved arrangement. Follow the guide's reconciliation path before another
attempt, and report unsupported branches separately.

Provide each participant its bounded assignment by the brief the entry skill
describes. Establish the ordinary native supervision the arrangement needs,
reconciling any existing monitoring first.

The one periodic check allowed is a stall sweep at the interval the operator
approved. The runtime reports a supervised worker's stop once, with the
worker's last output, and does not report that worker's later idle turns or a
message-assigned participant at all. The sweep covers what nothing else
reports, by the wait rule in Operate: it acts on each recorded wait that has
ended and on each open assignment with no recorded wait, hold, or running job.
A progress or status report does not exempt a participant. The sweep reads
state without consuming the Coordinator's inbox. Anything beyond that sweep is
a second scheduler or a fixed tick cadence; do not add one.

Verify the entry skill's individual outcomes, effective settings, communication,
and supervision. Everyday work then continues under Operate; setup is not rerun
for each issue or wave.
