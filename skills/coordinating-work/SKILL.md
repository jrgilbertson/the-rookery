---
name: coordinating-work
description: "Establish or revive an Orca collaboration arrangement, including Planner, Coordinator, and task workers. Use when explicitly asked to set up a team or recover existing collaboration after an account or session interruption. Ordinary CE execution and small child-worktree delegation keep their existing workflows."
license: MIT
compatibility: "Requires Orca, access to its version-matched CLI and orchestration guides, and authenticated providers supported on the execution host."
---

# Coordinating Work

Establish or recover a working collaboration arrangement through one editable
proposal. The result is an approved arrangement with verified individual
outcomes and a working communication and supervision loop.

## Choose the operation

- For a new arrangement or adoption of an existing one, read
  [Setup](references/setup.md).
- For interrupted collaboration, read [Revive](references/revive.md).

This is an optional entry point. Ordinary issue execution, a small delegation,
and a plain handoff retain their existing owners. A continuing arrangement does
not make each implementation worker permanent.

## Runtime and work ownership

Load the installed `orca-cli` and `orchestration` skills by name and retrieve
their version-matched guides from the executable selected for this session.
When companion skills are absent, use the runtime's supported guide-discovery
interface. If the required guide or capability cannot be reached, report the
affected operation blocked; do not reconstruct commands from historical scripts.

The current guides own placement, launch, Run/Task/Dispatch authority, messaging,
liveness, retries, monitoring, release, and worktree operations. Inspect the
execution host and supported surface: a chat worker is not necessarily a
terminal, and worker chat support does not prove replacement Coordinator
authority. A role name, workspace title, or nearby agent does not establish
membership or ownership.

The canonical tracker owns issue state. CE owns issue-specific planning,
execution, verification, and shipping. The Planner, when chosen, shapes the
agreed roadmap and briefs from those records; the Coordinator owns assignments,
supervision, and relaying decisions. Give each assignment one current writer
and avoid separate Planner and Coordinator instructions competing for it.

## Proposal and authority

Before setup or revive changes, present one concrete proposal covering:

| Participant / assignment | Current state | Previous provider, model, effort | Proposed provider, model, effort | Execution placement | Intended action |
| --- | --- | --- | --- | --- | --- |
| Each affected role or worker | Evidence and any hold | Observed values, unknown, or no previous participant | Explicit values or evidenced preservation | Host, workspace and owning assignment | Keep, start, continue, fresh handoff, or blocked |

Include the current Coordinator, relevant participants left unchanged, and
needed communication or supervision changes. State unresolved membership or
capability gaps that affect the proposal. Use current supported choices; do
not embed a changing model catalog. An actual prior setting differs from a
configured default. Unknown prior values stay unknown.

Obtain approval of the final effects. An explicit approval with fully specified
edits approves that edited proposal once. An exploratory question is not an
approval. Apply only the approved supported effects; if material state drift
or a rejected setting changes them, pause that branch and present an amended
proposal. Preserve independent approved successes.

This confirmation belongs to setup and revive. Routine assignments and worker
starts continue under existing project authority without rerunning setup or
adding a staffing confirmation for every task. Existing approval requirements
still apply; this skill grants no merge, spending, trust, or destructive-action
authority. Account selection and manually starting a replacement Coordinator
remain with the operator. Do not silently switch accounts or substitute settings.

## Worker lifetime and cleanup

Default to task-scoped PR workers, normally one worktree per PR. Keep the
Coordinator, Planner, or another role while it has a concrete ongoing
responsibility. An ongoing member can be idle awaiting another assignment;
do not invent filler work to keep it busy.

Retire a completed PR worker after its delivery and monitoring obligations.
Use the native release procedure. After merge, clean eligible worktrees through
the repository and Orca lifecycle within existing authority. A merged branch
alone does not prove removal is safe: preserve needed local work, evidence,
services, unfinished ownership, and human holds. Name the remaining obligation
when cleanup must wait, and continue independent work. Do not turn uncertainty
into forced removal or add a separate cleanup system.

## Assignment briefs

Build each brief from the project's own instructions and the installed guides.
Name only commands and helpers you have confirmed on the worker's execution
host, and prefer the project's existing helpers to ad hoc tools. Carry the
operator's current decisions from their owning record, never a proposal the
operator declined.

Tell each worker to wait for long-running checks inside its own turn, using a
bounded foreground wait, and to end a turn only with a question or a completion
report. A turn that ends while a background watcher still runs reads as a
stopped worker and wakes the Coordinator for nothing.

## Recoverable working context

Reuse canonical issues, plans, worktrees, and current native records. Preserve
only otherwise-unrecoverable coordination context in private disposable working
files, such as an interrupted approved operation and its original receipt.
Keep a discoverable reference through the arrangement's existing work record;
name the base of relative references and how other participating worktrees
reach them. Ignored files in one checkout are not automatically shared with
another checkout or machine. No fixed directory bundle or universal state
schema is required.

Account-specific conversation memory must not be the only way to discover
unfinished work. When the operator confirms a plan or answers a decision round,
record the decisions in the canonical tracker before acting on them; a usage
limit can end the session without warning. Report existing backup coverage and its gaps without promising
host-loss restoration. Keep private identities, transcripts, and credentials
out of public source; preserve lasting outcomes in their owning records and
let temporary context expire when no longer useful.

## Verify and report

Account for every intended participant as responsive, idle awaiting assignment,
waiting on a named dependency, explicitly held, or blocked. These are report
descriptions, not invented native status values. Identify excluded completed
workers or unresolved candidates when they affect the outcome.

Confirm the participant's current assignment or deliberate disposition and
applicable recent decisions, a working return path to the current Coordinator,
and needed supervision. A queued message, heartbeat, live process, or successful
script exit alone does not establish recovery. No new code or paid work is
required merely to prove communication. Verify effective settings where the
runtime exposes them; distinguish requested settings from observed values.

Lead with what is established and what still needs action. Give evidence and
the next action for each exception. Unsupported capabilities and unknown
ownership block their affected actions, not independent approved work. Never
describe a partial recovery as complete.
