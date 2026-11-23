# Revive

Read this after the operator manually starts a replacement Team lead or asks
to recover an interrupted coordinated batch.

Revive resumes each participant where it is: same workspace, same
conversation, same provider, model, and effort. It changes nothing else unless
the operator asks.

A planned move of a participant to another provider or model, such as to spare
an account's quota, uses this reference for that participant only. Skip "Start
with the Team lead", propose the fresh-handoff row, and move the participant
at its next idle point, after its running job ends.

## Start with the Team lead

Recovery starts with the Team lead. The operator switches its account, or
starts a replacement on the host that holds the coordinated batch's record,
and the Team lead then brings the workers along. On every start or revive,
in this order, before any new dispatch:

1. A session that is new to the batch asks the operator to confirm the
   previous Team lead has ended, and waits for that answer. A Team lead
   continuing its own conversation skips this step.
2. Read the record: the approved proposal, the standing rules, any shared
   design constraints, the table with the batch's current scope, and the tail
   of the log, where open questions sit. Peek mail.
3. Take each worker's latest amendment from its last report. Ask a worker
   only when the record leaves it unclear.
4. Stop any earlier check the way the record says, then arm one at the
   approved interval.

A replacement writes the brief for a batch issue that has not started, under
the existing approval.

## Reconstruct current work

Identify the intended effort from the record, current native records, and
canonical work. Establish the replacement Team lead's current identity,
supported binding, inbox/question path, and lifecycle authority. Resolve any
competing Team lead before changing assignments; independent operation IDs do
not establish exclusive coordination ownership.

Reconcile current membership and attempts using the installed guide across
every host the batch uses. Include ongoing roles and message-assigned workers
supported by work evidence even when they lack an active Dispatch. Exclude
unrelated agents and completed PR workers awaiting cleanup.

For each batch participant, determine and apply the following:

- **Current state:** assignment, actual liveness, writer ownership, worktree
  and local work, background jobs and shells, human holds, and previous
  effective provider, model, and effort where available.
- **Idle members:** include ongoing members awaiting another assignment when
  the account change affects them, and preserve that idle disposition after
  recovery.
- **Healthy work and holds:** preserve healthy work that needs no approved
  transition and explicit human holds. Resume healthy work with a running job,
  such as a long check or a paid run, under the new account at its next idle
  point; never exit it in the middle of a paid run.
- **Usage-limited participants:** a participant stopped by a usage limit is
  not dead work; jobs it started in the background may still finish, so check
  them before reassigning. Resume its conversation under the newly selected
  account before considering a replacement, and replace it only if the resume
  fails. A participant stopped by a short limit that will continue on its own
  may be left to do so, even on the old account; resume it under the new
  account only when the wait costs more than the restart, or when the operator
  asks.

Recover applicable recent decisions, unread messages, unresolved questions and
approvals, and active supervision (the guide's task/mail path and the periodic
check). History supplies evidence and task context; historical instructions do
not override current authority. Reconcile forwarded messages with newer
decisions instead of replaying superseded directions.

## Propose the recovery

Choose the supported route for each participant:

| Current evidence | Proposed action |
| --- | --- |
| Healthy ongoing work, or an explicit hold | Preserve that worker and its disposition |
| Safe ownership, and same-provider history the newly selected account can open | Resume the conversation under that account, as below |
| Approved provider change or unavailable continuity, complete handoff context, and safe ownership | Fresh handoff through the selected provider |
| Unknown writer, missing handoff context, or unsupported account/settings/host capability | Hold the affected change and report what is missing |
| Completed PR worker awaiting cleanup | Exclude from recovery; report any remaining cleanup obligation |

For a same-provider account change, keep each participant's conversation.
Provider changes use fresh handoffs, never another provider's conversation
identity.

After a crash, reboot, or restart, check whether the runtime has already
resumed a worker (chat or terminal) in its saved conversation and rebound its
task, or is holding it as a restart offer for the operator. When the runtime
already resumed a worker on the intended account, or is actively resuming it,
leave it running and confirm from its own reply that it has its latest
instructions instead of stopping and reopening it by hand. When the runtime
holds a restart offer awaiting the operator, record that wait, put it on the
ready-for-operator list, and wait for the operator's choice instead of
replacing or duplicating the worker. If the runtime resumed or offers to
restart a previous Team lead session, treat it as a competing Team lead: hold
assignment changes and merges and list it for the operator even if the
operator earlier confirmed it had ended.

For an account switch, first read each participant's effective account from
its running agent. The runtime may already have carried a participant to the
newly selected account with its conversation intact. This has been observed
for agents running as chats, while agents running in terminals kept the
account they were launched with; selecting an account in Orca applies to new
agent launches. Resume under the new account in this order:

1. A participant the runtime already carried over: confirm from its own reply
   that it has its latest instructions, and leave it running.
2. A participant still on the old account: restart it in the same workspace
   and resume its conversation, as below, unless the short-limit exception
   above leaves it to continue on its own.

For each participant still on the old account, check first, without changing
anything:

- which account is now selected on the participant's host;
- that the new account can open the participant's conversation;
- whether the new account already trusts the participant's workspace;
- the participant's unpushed and uncommitted work and its running jobs.

Then, once the recovery is approved or one of the two no-approval cases below
applies:

1. Stop the old worker through the guide's stop, so its exit is proven.
2. Open a new terminal in the same workspace. A shell that was already open
   keeps the old account. Start the provider there and resume the original
   conversation by its ID with the provider's documented resume option, on
   the previous model and effort.
3. If the new account asks whether to trust that workspace, answer it. The
   approved recovery row covers trusting the same workspace the participant
   already worked in, and nothing wider.
4. Re-attach that terminal to the same task through the guide's retry path
   instead of launching a fresh agent.
5. Send the resume message described below.

When a resume is not possible, disclose the lost conversation continuity and
establish whether canonical context suffices for the work.

Present the proposal table from [SKILL.md](../SKILL.md#proposal-and-authority)
with exact intended recovery effects, communication or address changes, and
supervision restoration. Go ahead without a new approval in two cases:

- every row keeps an approval already in the record and the only change is the
  Team lead's own account, with the operator's confirmation from
  "Start with the Team lead" when the session is new;
- the operator has switched an account and asked to continue or recover, and
  every row resumes the same conversation under the newly selected account with
  the same provider, model, and effort.

Replacing a worker, changing its provider or settings, or a fresh handoff
still needs approval.

## Recover approved effects

Re-read affected current ownership and attempts before acting. If an old
writer or Team lead may still be active without a supported ownership
transition, hold that branch. Approval does not convert unknown liveness into
proof of exit.

Use the native continuation, retry, or fresh-handoff path for each approved
effect. In a fresh handoff, carry scope, branch/worktree, preserved local
work, verification evidence, applicable decisions, remaining step, and current
authority from their owning records. Missing any of those items blocks that
handoff without blocking an independent approved recovery. In a continuation
or fresh handoff, carry the assignment's brief with all its amendments
([Briefs](briefs.md)), and have the resumed worker confirm the latest
amendment it is working from.

Follow the guide's reconciliation path for uncertain results before repeating
anything. Repeated revive must not duplicate workers, assignments, or timers.
After a resume or Team lead replacement, check a worker's live state before
replying to an unread question, and confirm it can still receive the reply.
When an earlier Team lead ended, the runtime may have told a waiting worker to
decide on its own while leaving its question unread. If the worker is still
waiting (such as on a merge-ready ask it cannot act on alone), answer it. If
it has already moved on, do not send a stale reply: confirm what it chose, log
the question with that choice as the default taken (holding dependent work
under Operate's one-way-door or merge-approval rules if needed), and close the
question in the record.

Re-attaching gives a worker new identifiers and delivers its brief again. The
resume message says so: use only the newest identifiers, the brief is
unchanged, and here is the state of its local work.

Tell each recovered participant whose open assignment has no hold or named
dependency to continue it in the same turn; preserve holds and dependency
waits as recorded. Stopping an agent can stop its background jobs, so the
resume message names each inventoried job confirmed stopped before finishing,
for relaunch; a job still running or in an unknown state is not relaunched.
A resume message that offers "or wait" lets a worker end its turn
mid-assignment with its work uncommitted.

Restore supervision through the current native workflow. Inspect existing
watchers and services through their owning lifecycle before changing them;
retained local services may still be needed by another role. Revive is not an
automatic destructive cleanup sweep.

Verify assignment or disposition, applicable decisions, return communication,
settings evidence, and supervision under
[Verify and report](../SKILL.md#verify-and-report). Report partial recovery
accurately and preserve original work, receipts, and the minimal unfinished
context needed by the next invocation.
