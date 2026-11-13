# Operate

Read this while running an established coordinated batch, with or without the
operator present. The entry skill owns shape, the merge approval, briefs, and
the record. Setup produced the approved proposal this file acts under.

## Defaults the proposal shows

**Merge bar.** `ce-babysit-pr` gave its plain looks-merge-ready report on the
pull request's current head.

**Held changes.** A pull request is held for the operator when it changes:

- access and authorization;
- money;
- data deletion;
- privacy;
- outbound email;
- release gates;
- the project's agent instructions, and its merge and review policy.

The approved proposal governs. It may replace either default with the
project's own guidance or the operator's edits.

## Running the batch

When a worker's start waits at a one-time trust or setup prompt, tell the
operator, who answers it once for that agent in that repository, and hold only
that assignment. Revive covers the prompt a resumed worker's new account
raises. Recover any other failed start through the guide, and put what it
cannot recover on the ready-for-operator list.

After every decision, dispatch the next ready issue in the batch the approved
proposal lists, in the order and at the concurrency you judge best. Measure the
whole host before a heavy job. When it is busy, leave the issue for the next
check. When a merge changes what a later issue should assume, say so in that
issue's brief. When no issue remains, note on the ready-for-operator list that
the batch is finished. Adding issues takes an amended proposal the operator
approves, except incidental work inside a class the approved proposal names.
Dispatch each such item as its own pull request.

## The merge checklist

A worker asks when its `ce-babysit-pr` run reports looks merge-ready. Merge
only when every line below is true. Line 2 is the worker's report, taken on
the worker's word because the worker runs the watch. Lines 3 and 4 are facts
you read yourself from the pull request and the record when you decide. In a
batch with no task workers, you run `lfg` and the continuous `ce-babysit-pr`
watch yourself, and line 2 reads the first line of your own watch report and
the head commit it covered.

1. **Approval.** The record holds the setup proposal the operator approved, it
   shows a merge bar and held changes, and this pull request's issue is in
   its batch or inside an approved class of incidental work. Every condition
   the approved merge bar adds beyond this list is true for this pull
   request.
2. **Report.** The worker quoted the first line of `ce-babysit-pr`'s
   continuous-watch report, that line says the pull request looks merge-ready
   and adds no condition, such as a position in a stack, and the worker gave
   the head commit that report covered. A closing phrase that leaves the merge
   to the reader is not a condition.
3. **Routine.** The diff touches no held change, except one the record shows
   the operator pre-authorized for this issue, under a bar this pull request
   meets. A change that relates to a held change at all, wording and tests
   included, touches it. The pull request body has no unticked item under
   `lfg`'s unapplied review findings. The record shows no item, at any point,
   that `ce-babysit-pr` parked for a human about the change itself. Merging
   it starts only what the proposal showed.
4. **Current.** Read the pull request now: its head is the reported commit,
   at least one check passed on that head and every check finished without
   failing, no review thread is open, no review requests changes, and the code
   host reports it mergeable under the repository's own rules. Where the
   repository merges through a queue or enforces up-to-date branches itself,
   that decides currency; otherwise the branch is current with its base. A
   check that finished neutral or skipped has finished without failing.
5. **Merge.** Merge that head now, as an ordinary merge the repository
   accepts, with the merge conditional on the reported commit, and read the
   pull request once more to confirm it landed. Where the repository merges
   through a queue, the merge is an enqueue, and it has landed once the pull
   request reads merged.

A line that is false, that you cannot read, or that is unclear means no merge.
So does any situation this list does not describe. Then:

- when the worker can make the line true, reply with what to do, such as
  fixing a failed check, resolving a thread, updating a stale branch, or
  running the continuous watch and asking again;
- otherwise leave the pull request open, add it to the ready-for-operator list
  with the line that failed, and reply that it is held for the operator. A
  pull request that will be held anyway is held straight away.

A parked item that is only about a reviewer or tool being unavailable, such
as a review bot out of quota, says nothing about the change. Log it, answer
the worker with the default, and let the checklist decide.

A held pull request is left as it is. Bringing one current, or applying an open
finding on it, is work to assign when the operator asks.

After a merge lands, record it and reply merged. Then run the `managing-issues`
completion check on the issue. The issue closes on that result, not on the
merge. A gap the check finds, or a missing `managing-issues`, leaves the issue
open and puts it on the ready-for-operator list.

## Never wait for an answer

Keep the batch moving without the operator, whether or not they are present.
Put every question in the record with a default, and leave blocking question
dialogs unused. The skill asks the operator for exactly two things, and those
are the only waits: approval of a proposal, and a new session's confirmation
that the previous Coordinator has ended.

On a judgment call the brief, the record, and the standing rules do not settle,
decide a default and write the question and that default to the record. A
two-way door is a call that can be undone later; a one-way door is one that
cannot. Decide a two-way door yourself and proceed when it stays inside the
merge approval. For a one-way door, or any call that touches the merge
approval, run `ce-pov` for the default, log it, and hold only the work that
depends on the answer. When a worker proposes something its issue does not
name, the default is the smaller option.

A logged question, a held pull request, or a parked item stops only the work
that depends on it. So does an outside service that is down, such as the
tracker. Record the pending write, continue independent work, and retry it at
each check after checking whether an earlier attempt landed. A timed-out write
is not proof it failed. Answer every question a worker sends, by a default or
by holding its work, so each worker always has its reply.

## The ready-for-operator list

Give the operator one list, complete and unfiltered, read from the record's
log and table, with every report and whenever they ask for open questions or
an update:

- every held pull request, with the checklist line that held it and any
  unticked review items;
- every open question, and every decision you made by default since the last
  report, each with the default taken and what proceeded on it;
- every parked item awaiting the operator, with the pull request it blocks;
- every worker or chat that needs the operator: one to move, replace, or
  re-account, one waiting at a prompt, and one only the operator can close;
- every merge made, with the pull request and the head merged;
- every incidental item dispatched, with its class and pull request;
- every issue a completion check left open, with the gap it found.

## Standing rules

Keep the coordinated batch's standing rules in the record. When an incident
shows workers need a rule the briefs lack, add it without asking: one dated
rule, tied to the named incident that caused it. Send it to affected workers
as an amendment, and list each new rule in your next report to the operator.
A standing rule only adds a restriction on how workers operate.

## The check

The record's table says what each assignment is waiting on: a named running
job, a usage-limit reset time, a merge queue, or the operator. A report that
a worker stopped is an event, so read the worker's live state before acting
on it. When the stop matches what the table says it is waiting on, leave the
worker alone.

The runtime reports a worker's stop once and stays quiet about its later idle
turns. One check, at the interval the operator approved, covers what nothing
else reports. Each time, read the table against live state and act on what
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
- tell a worker to continue when its assignment is open, as the entry skill
  defines it, with nothing it is waiting on;
- dispatch an issue left for this check when the host now has room;
- list for the operator a worker that has not acknowledged its last reply
  by the following check.

The check belongs to the Coordinator's own session. It ends with that session,
or when no assignment is open or waiting at a prompt the operator can answer,
no batch issue is still to dispatch, and no recorded write is pending. The
record says how to stop it. A scheduler that starts a new agent session is a
second Coordinator, so the check uses the session's own timer.

Moving, replacing, or switching the account of a worker happens only in
Revive, at the operator's request.
