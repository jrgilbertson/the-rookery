# Revive

Read this after the operator manually starts a replacement Coordinator or asks
to recover an interrupted arrangement. The entry skill owns shape, shared
approval, worker lifetime, the record, and completion requirements.

## Start from the record

A replacement Coordinator starts on the host that holds the arrangement's
record. On every start or revive, before any new dispatch:

1. Read the record: the approved proposal, the standing rules, the open
   questions, and the tail of the decisions.
2. Confirm from each worker's own reply which amendment it is working from.
3. Re-arm the stall sweep at the approved interval, after checking that no
   earlier sweep is still installed. A sweep that lived in the previous
   session ended with it.

## Reconstruct current work

Identify the intended effort from the record, current native records, and
canonical work. Establish the replacement Coordinator's current
identity, supported binding, inbox/question path, and lifecycle authority.
Resolve any competing Coordinator before changing assignments; independent
operation IDs do not establish exclusive coordination ownership.

Reconcile current membership and attempts using the installed guide, including
complete execution-host coverage where needed. Include ongoing roles and
message-assigned workers supported by work evidence even when they lack an
active Dispatch. Nearby workspaces, historical dispatches, and role labels are
hints, not membership proof. Exclude unrelated agents and completed PR workers
awaiting cleanup. Leave a participant the entry skill does not describe
running as you found it.

Determine each participant's assignment, actual liveness, writer ownership,
worktree and local work, background jobs and shells, human holds, and previous
effective provider/model/effort where available. Include ongoing members
awaiting another assignment when the account change affects them; preserve
that idle disposition after recovery. Preserve healthy work that needs no
approved transition and explicit human holds. Healthy work with a running job,
such as a long check or a paid run, moves at its next idle point; never exit
it in the middle of a paid run. The guide's safety rules govern what silence,
a timeout, or an unreachable host prove. A participant stopped by a usage
limit is not dead work: jobs it started in the background may still finish, so
check them before reassigning.

Recover applicable recent decisions, unread messages, unresolved questions and
approvals, and needed monitoring. History supplies evidence and task context;
historical instructions do not override current authority. Reconcile forwarded
messages with newer decisions instead of replaying superseded directions.

## Propose the recovery

Choose the supported route for each participant:

| Current evidence | Proposed action |
| --- | --- |
| Healthy ongoing work, or an explicit hold | Preserve the appropriate current worker and disposition |
| Safe ownership, and same-provider history the newly selected account can open | Resume the conversation under that account, as below |
| Approved provider change or unavailable continuity, sufficient task context and safe ownership | Fresh handoff through the selected provider |
| Unknown writer, essential missing context, or unsupported account/settings/host capability | Hold the affected change and report what is missing |
| Completed PR worker awaiting cleanup | Exclude from recovery; report any relevant remaining cleanup obligation |

For a same-provider account change, keep each participant's conversation.
Provider changes use fresh handoffs, never another provider's conversation
identity.

First read each participant's effective account from its running agent. The
runtime may already have carried a participant to the newly selected account
with its conversation intact. This has been observed for agents running as
chats, while agents running in terminals kept the account they were launched
with. A participant already on the new account needs no move: confirm from
its own reply that it has its latest instructions, and leave it running.

Move each participant still on the old account by hand. Check first, without
changing anything:

- which account is now selected on the participant's host;
- that the new account can open the participant's conversation;
- whether the new account already trusts the participant's workspace;
- the participant's unpushed and uncommitted work and its running jobs.

Then, as approved:

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

Show the entry skill's proposal with previous and proposed settings, exact
intended recovery effects, unchanged participants, and unresolved branches.
Include communication/address changes and restoration of needed supervision.
The operator can approve with specific row edits in one reply; exploratory
changes do not authorize execution.

Go ahead without a new approval only when every row keeps an approval already
in the record and the only change is the Coordinator's own identity or
account. Moving, replacing, or changing the settings of any worker still needs
approval.

## Recover approved effects

Re-read affected current ownership and attempts before acting. If an old writer
or Coordinator may still be active without a supported ownership transition,
hold that branch. Approval does not convert unknown liveness into proof of exit.

Use the native continuation, retry, or fresh-handoff path for each approved
effect. In a fresh handoff, carry scope, branch/worktree, preserved local work,
verification evidence, applicable decisions, remaining step, and current
authority from their owning records. Insufficient essential context blocks that
handoff without blocking an independent approved recovery. In a continuation
or fresh handoff, carry the assignment's brief with all its amendments, and
have the resumed worker confirm the latest amendment it is working from.

Follow the guide's reconciliation path for uncertain results before repeating
anything. Repeated revive must not duplicate workers, assignments, or timers.
After a resume, check that a worker with an open question to the Coordinator
can still receive the reply.

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

Restore needed supervision through the current native workflow. Inspect existing
watchers and services through their owning lifecycle before changing them;
retained local services may still be needed by another role. Revive is not an
automatic destructive cleanup sweep.

Verify assignment/disposition, applicable decisions, return communication,
settings evidence, and supervision under the entry skill's completion rules.
Retain a participant as blocked when only transport acceptance or a heartbeat
is established. Report partial recovery accurately and preserve original work,
receipts, and the minimal unfinished context needed by the next invocation.
