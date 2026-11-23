# Setup

Read this when establishing a coordinated batch or adopting an existing one.

## Establish the intended coordinated batch

Use the invoking session as Team lead unless the operator requested another
Team lead. Establish its actual runtime identity and supported coordination
authority; do not launch a duplicate Team lead because this one lacks a
terminal handle.

Read the supplied objective, canonical work and project instructions, current
participants, and any existing record. If several arrangements plausibly
match, obtain the missing selection before changing them. Adopt existing
in-scope assignments, holds, and working context rather than recreating them.
An agent already working on the objective before setup, such as a chat started
for a batch, is a participant to adopt. When the guide cannot attach a
supervised Task to it, keep it as a message-assigned worker reached through the
guide's reference lookup, and include it in the check.

Plan the batch with the operator from the tracker. Its scope is the issues and
epics the operator hands over, and its order is the Ready Frontier
`managing-issues` lists, with each issue the source of its brief. When part of
the objective is not yet an issue, draft it and create it through
`managing-issues` under that skill's own approval. Check each issue's
Verification as the entry skill describes before dispatching it. When the
tracker cannot be read through `managing-issues`, report the batch blocked.
Propose only the initial assignments the work needs. Staffing, isolation,
concurrency, and resource use follow the native workflow and the operator's
existing limits. When ready issues in scope edit the same hot files, sequence
them instead of dispatching them in parallel, and record a tracker blocker when
the order must hold across waves. On a shared execution host, limit concurrent
heavy jobs, such as verification, builds, and browser runs, by measured CPU and
memory rather than by participant count. Each brief names the project's own
metering helper, or, when the project has none, a host command confirmed to
measure CPU and memory.

## Propose before establishing

Inspect available provider/model/effort choices and placement support on each
execution host the guide can reach. Recommend where heavy workers run,
preferring a reachable host kept for development work over the operator's own
machine, and show the measured CPU and memory behind the recommendation; the
operator chooses the placement. Distinguish the Team lead already running from
participants that need starting. Preserve evidenced settings for existing
participants; show the supported choices for new ones. "Host default, no
override" is an explicit value when the host's choices cannot be listed.
Unless the runtime fixes their surface on its own, such as starting workers
from a persistent agent home as chats, workers launch on the surface the host
is set to. When the surface they would launch on does not follow an account
change by itself and the guide or observed behavior shows another surface does,
tell the operator which, so they can set the host to it.

Present the proposal table from [SKILL.md](../SKILL.md#proposal-and-authority),
including reused participants, their task ownership, and initial workers to
start. The proposal also states, so that one approval covers them:

- **The batch.** List the issues and epics in scope, with each issue's four
  scores. The Team lead dispatches nothing outside the recorded scope.
- **Issue edits.** State the standing instruction that lets the Team lead
  edit Scope and Verification on issues in scope as
  [Changing an issue](../SKILL.md#changing-an-issue) allows, with stored
  scores kept, and close an issue whose pull request merged through the
  checklist. `managing-issues` applies neither without that recorded
  instruction.
- **What a merge starts.** State what merging to the default branch triggers
  here, such as a deploy, a release, a migration, a paid job, or the tracker
  closing the linked issue.
- **Spending.** Whether the Team lead may choose a paid option, such as at a
  usage-limit prompt. The default is no.
- **The merge bar and the held changes.** Show the defaults from
  [The merge approval](../SKILL.md#the-merge-approval). When the project's own
  guidance defines a merge bar or held changes, show those instead and say
  where they came from. The operator may edit either. Mark each listed issue
  that touches a held change or is scored 3 on verification effort, and each
  later issue it would block. Ask the operator directly whether to hold those
  for review or pre-authorize merging them under a stated bar. With no answer,
  they are held.
- **The standing instruction not to wait.** State it as the operator's
  instruction: the Team lead never stops for an answer, decides defaults for
  two-way doors, uses `ce-pov` and holds only dependent work on one-way doors
  or calls that touch the merge approval, and logs every question. An
  installed guide that says to ask the user first yields to this instruction
  once it is approved.
- **Where the record lives.** Name a durable, private location on the
  Team lead's host, as [The record](../SKILL.md#the-record) requires.
- **The check interval**, for the one periodic check during operation;
  suggest 30 minutes for the operator to approve.

Approval of the proposal is the standing merge approval for this coordinated
batch and records the instruction not to wait. Do not start workers, allocate
new tasks, create worktrees, install ongoing monitoring, or change the team
while the proposal is under discussion; read-only inspection and disposable
proposal notes may proceed. Once approved, write the approved proposal to the
record before starting anything.

## Establish and check

Immediately before affected changes, reconcile current ownership and any work
that completed during the discussion. Use the supported native operations for
the approved assignments, settings, and execution placements. If the current
Team lead lacks the required binding or authority, report that path blocked
instead of manufacturing a takeover.

A partial startup does not authorize duplicating successful workers or changing
the approved coordinated batch. Follow the guide's reconciliation path before
another attempt, and report unsupported branches separately.

Brief each participant following [Briefs](briefs.md). When dispatching to a
remote host that cannot reach or authenticate with the tracker, inline the
issue's Problem, Scope, and Verification in the brief instead of telling the
worker to fetch them. Establish the guide's native supervision, reconciling
any existing monitoring first.

Arm the one periodic check at the approved interval, and write in the record
how to stop it. It is the only periodic work in the batch, and it peeks mail.

Verify outcomes, effective settings, communication, and supervision under
[Verify and report](../SKILL.md#verify-and-report). Everyday work then
continues under [Operate](operate.md); setup is not rerun for each issue or
wave.
