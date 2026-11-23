# Operate

Read this while running an established coordinated batch, with or without the
operator present, under the approved setup proposal.

## Running the batch

When a worker is still starting, waits at a one-time trust or setup prompt, or
has its brief or restart continue prompt held behind a dialog, keep its live
assignment open and record that wait (`starting` or `prompt/dialog`) in the
table (never submit input into the dialog or restart it as a failed start).
Tell the operator when a prompt or dialog needs their answer, hold only that
assignment, and follow the runtime notice once it is cleared. Revive covers
the workspace-trust prompt a resumed worker's new account raises. Recover any
start whose live state reports failure or timeout through the guide, and put
what it cannot recover on the ready-for-operator list.

After every decision, dispatch the next issue from the batch's Ready Frontier
that the batch has not yet assigned, briefing it under [Briefs](briefs.md), in
its leverage order unless host capacity or the operator's instruction says
otherwise, and at the concurrency you judge best. Dispatch only an issue that has its four scores, and list an
unscored one for the operator. Measure the whole host before a heavy job. When
it is busy, leave the issue for the next check. When a merge changes what a
later issue should assume, say so in that issue's brief. When nothing is
ready, say so on the ready-for-operator list with what each remaining issue
waits on; the batch is finished only when every issue in scope is done or the
operator ends it. Scope grows only as [Shape](../SKILL.md#shape) says. When
work outside scope would help the batch, such as a flaky test that blocks
merges, draft it as an issue and list it for the operator.

## The merge checklist

A worker asks when its `ce-babysit-pr` run reports looks merge-ready. Merge
only when every line below is true. Line 2 is the worker's report, taken on
the worker's word because the worker runs the watch. Lines 3 and 4 are facts
you read yourself when you decide. In a batch with no task workers, you run
`lfg` and the continuous `ce-babysit-pr` watch yourself, and line 2 reads the
first line of your own watch report and the head commit it covered. Apply the
UX and UI work guidance in [Briefs](briefs.md) to your own assignments too.

1. **Approval.** The record holds the approved setup proposal and any change
   the operator made to the scope, merge bar, or held changes. Together they
   show the current merge bar and held changes, and this pull request's issue
   is in the batch's recorded scope. Every condition the approved merge bar
   adds beyond this list is true for this pull request.
2. **Report.** The worker quoted the first line of `ce-babysit-pr`'s
   continuous-watch report, that line says the pull request looks merge-ready
   under the approved merge bar, with no other condition such as a position in
   a stack, and the worker gave the head commit that report covered. For a
   cautious report, read the other external review on that head yourself.
   A closing phrase that leaves the merge to the reader is not a condition.
3. **Routine and done.** Every condition below holds:
   - The diff touches no held change and the issue is not scored 3 on
     verification effort. The exceptions are a held change the record shows
     the operator pre-authorized for this issue, under a bar this pull request
     meets, and a pull request the operator has told you, in their own
     recorded words, to merge. A change that relates to a held change at all,
     wording and tests included, touches it.
   - The pull request body has no unticked item under `lfg`'s unapplied review
     findings.
   - The record shows no item, at any point, that `ce-babysit-pr` parked for a
     human about the change itself.
   - Merging it starts only what the proposal showed.
   - The pull request body sets evidence beside each of the issue's
     verification criteria as the issue reads now. Compare and do not
     interpret. A criterion met in part, with an exception, or in other words
     is unproven.
   - Any choice the worker declared in the pull request body fits the batch's
     recorded design constraints. A declared choice that contradicts a
     recorded constraint makes this line false (reply with what to align, or
     hold the pull request). A declared choice that only changes what another
     in-scope issue should assume satisfies this line once you record the
     change, amend every affected open assignment in full, and note it for
     upcoming briefs before merging.
4. **Current.** Read the pull request now: its head is the reported commit,
   at least one check passed on that head and every check finished without
   failing, no review thread is open, no review requests changes, and the code
   host reports it mergeable under the repository's own rules. Where the
   repository merges through a queue or enforces up-to-date branches itself,
   that decides currency. Neutral or skipped checks count as non-failing.
   Read the default branch's latest required checks. If any are failing,
   route the fix or revert first. If it needs a merge to restore the default
   branch, ask the operator to land it. Tell the worker this merge must wait,
   record the wait, and rerun the checklist after recovery.
5. **Merge.** Merge that head now, as an ordinary merge the repository
   accepts, with the merge conditional on the reported commit, and read the
   pull request once more to confirm it landed. Where the repository merges
   through a queue, the merge is an enqueue, and it has landed once the pull
   request reads merged.

False, unreadable, unclear, or unlisted conditions block merging. For blockers
other than a default branch wait:

- when the worker can make the line true, reply with what to do, such as
  fixing a failed check, resolving a thread, or running the continuous watch
  and asking again;
- when the worker cannot and you could, make one more attempt: amend the brief
  and reassign it, start one follow-on assignment, or do the work yourself.
  When you do it yourself, run the continuous `ce-babysit-pr` watch on the new
  head yourself, and line 2 reads your own report. Run the checklist again on
  the result;
- otherwise, or when that attempt also falls short, leave the pull request
  open, add it to the ready-for-operator list with the line that failed, and
  reply that it is held for the operator. A pull request that will be held
  anyway is held straight away.

A deviation the worker declared in the pull request body is yours to judge.
When the result still solves the issue's Problem, accept it by editing the
issue as [Changing an issue](../SKILL.md#changing-an-issue) allows, then run
the checklist against the edited text. Otherwise reply with what to fix, or
hold the pull request. A criterion that is unmet and undeclared is a false
line: reply with what to fix, and leave the issue as it is. In a batch with no
task workers, a deviation in your own work is not yours to accept; hold the
pull request for the operator.

A parked item that is only about a reviewer or tool being unavailable, such
as a review bot out of quota, says nothing about the change. Log it, answer
the worker with the default, and let the checklist decide.

Leave a held pull request as it is and stop its watch. Assign further work
when the operator asks.

After a merge lands, record it and reply merged. An issue whose pull request
you merged is done: read the issue, and when the tracker left it open, close
it through `managing-issues`. An issue you could not close goes on the
ready-for-operator list with the reason.

## Never wait for an answer

Keep the batch moving whether or not the operator is present. Decide a default
and write every question to the record with that default instead of opening a
blocking question dialog. When the operator is talking to you, raise what is
open then. You wait only for the operator's own approvals (of a proposal, a tracker write
`managing-issues` needs approved, or a runtime prompt or restart offer only
the operator can answer) and a new session's confirmation that the previous
Team lead has ended. Each holds only the work that depends on it.

On a judgment call the brief, the record, and the standing rules do not settle,
decide a default and write the question and that default to the record. A
two-way door is a call that can be undone later; a one-way door is one that
cannot. Decide a two-way door yourself and proceed when it stays inside the
merge approval. For a one-way door, or any call that touches the merge
approval, run `ce-pov` for the default, log it, and hold only the work that
depends on the answer. When a worker's question offers options that all
deliver its issue as briefed, default to the option that resolves the cause,
even when it is the wider fix. When an option adds an outcome the issue does
not name or changes a constraint in the brief, treat it as an issue edit:
change the issue's Scope when solving its Problem needs the change, and
otherwise answer with an in-scope option and list the addition as a proposed
follow-up.

A logged question, a held pull request, or a parked item stops only the work
that depends on it. So does an outside service that is down, such as the
tracker. Record the pending write, continue independent work, and retry it at
each check after checking whether an earlier attempt landed. A timed-out write
is not proof it failed. Answer every question a worker sends, by a default or
by holding its work, so each worker always has its reply.

## The ready-for-operator list

Give the operator one list, complete and unfiltered, read from the record's
log and table, with every report and whenever they ask for open questions or
an update. Lead with a short Progress, Plans, Problems summary, then what
needs the operator first:

- every held pull request, with the checklist line that held it and any
  unticked review items;
- every open question, and every decision you made by default since the last
  report, each with the default taken and what proceeded on it;
- every issue edit, with the old text, the new text, and why, and each
  follow-up it proposes;
- every relayed message you acted on or refused;
- every unscored issue, and every new child of a handed epic that is not in
  scope;
- every parked item awaiting the operator, with the pull request it blocks;
- every worker or chat that needs the operator: one to move, replace, or
  re-account, one waiting at a prompt, and one only the operator can close;
- every merge made, with the pull request and the head merged, and each
  follow-up its worker proposed;
- every issue you could not close after its merge, with the reason.

## Standing rules

Keep the coordinated batch's standing rules in the record. When an incident
shows workers need a rule the briefs lack, add it without asking: one dated
rule, tied to the named incident that caused it. Send it to affected workers
as an amendment, and list each new rule in your next report to the operator.
A standing rule only adds a restriction on how workers operate.

## The check

The table names each wait: a worker start or dialog, a running job, a
usage-limit reset, a merge queue, default branch recovery, or the operator.
Read the worker's live state after a stop, model-retry, model-wait, or
background-task wait notice; non-stop notices do not mean the worker exited.
If live state shows the recorded wait or an active job with new output or
advancing state, leave the worker alone. Intervene through the guide when the
agent has stopped, failed, or shows no new output or state change across a
wait notice or repeated checks.

The runtime reports a worker's stop once and stays quiet about its later idle
turns. One check, at the interval the operator approved, covers what nothing
else reports. Peek mail, read the table against live state, and act on what
changed:

- answer any question still unanswered;
- note pull requests the code host shows opened or merged since the last
  check, and stamp the table with the time;
- when a wait has ended, or its end cannot be determined, take the next step:
  continue the worker, reply merged, or return a pull request the queue
  ejected to its worker;
- when a worker waits at a usage-limit prompt, choose no paid option unless
  the approved proposal lets you, since that is spending. Once the limit
  clears, cancel the prompt and tell the worker to continue. That is part of
  the check, not a Revive;
- when the cause of a hold placed for the operator is verifiably gone, such
  as a prompt the operator has since answered, continue that assignment.
  Held changes and merge decisions stay held;
- tell a worker to continue when its assignment is open, as [Briefs](briefs.md)
  defines it, with nothing it is waiting on;
- read the Ready Frontier again, and dispatch an issue that became ready or
  was left for this check when the host now has room;
- list for the operator a worker that has not acknowledged its last reply
  by the following check.

The check belongs to the Team lead's own session. It ends with that session,
or when no assignment is open or waiting at a prompt the operator can answer,
nothing in scope is left to dispatch or waiting on anything but the operator,
and no recorded write is pending. The record says how to stop it. A scheduler
that starts a new agent session is a second Team lead, so the check uses the
session's own timer.

Moving, replacing, or switching the account of a worker happens only in
Revive, at the operator's request.
