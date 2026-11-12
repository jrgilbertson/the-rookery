# Operate

Read this while running an established arrangement, with or without the
operator present. The entry skill owns shape, the merge grant, briefs, and the
record. Setup produced the approved proposal this file acts under.

## Defaults the proposal shows

**Merge bar.** `ce-babysit-pr` gave its plain looks-merge-ready report on the
pull request's current head.

**Hold classes.** A pull request is held for the operator when it changes:

- access and authorization;
- money;
- data deletion;
- privacy;
- outbound email;
- release gates.

The approved proposal governs. It may replace either default with the
project's own guidance or the operator's edits.

## After starting workers

Follow the installed guide: start the workers, end your turn, and let the
runtime wake you. Do not poll or run watch scripts. The approved stall sweep
is the only periodic check.

## The merge checklist

A worker asks when its `ce-babysit-pr` run reports looks merge-ready. Merge
only when every line below is true. Read each fact yourself when you decide;
do not take it from the worker's message or from memory.

1. **Grant.** The record holds the setup proposal the operator approved, it
   shows a merge bar and hold classes, and this pull request's issue is in
   its batch.
2. **Report.** The first line the worker quoted is the plain looks-merge-ready
   line of `ce-babysit-pr`'s continuous watch, in no other form, and it names
   a head commit.
3. **Routine.** The diff touches no hold class. The pull request body has no
   unticked item under `lfg`'s unapplied review findings. `ce-babysit-pr`
   parked no item on it for a human. Merging it starts only what the proposal
   showed.
4. **Current.** Read the pull request now: its head is the reported commit,
   every check on that head has finished and none failed, no review thread is
   open, and the branch is not behind its base.
5. **Merge.** Merge that head through the repository's normal path, with the
   merge conditional on the reported commit. Confirm it landed.

A line that is false, that you cannot read, or that is unclear means no merge.
So does any situation this list does not describe. Then:

- when the worker can fix it, such as a moved head, a failed check, an open
  thread, or a stale branch, reply with what to fix;
- otherwise leave the pull request open, add it to the ready-for-operator list
  with the line that failed, and reply that it is held for the operator.

Hold-class pull requests stay open no matter how clean they are.

After a merge, record it and reply merged. Where the repository merges through
a queue, the merge is an enqueue: record a wait for that pull request, and
reply merged only once it reads merged.

Then dispatch the next ready issue in the batch the approved proposal lists.
When none remains, dispatch nothing.

## Never wait for an answer

Do not open a blocking question dialog and do not stop the arrangement for an
answer, whether or not the operator is present.

On a judgment call the brief, the record, and the standing rules do not
settle, run `ce-pov` to establish a default. Write the question and that
default to the record. When acting on the default is reversible and stays
inside what the operator already granted, proceed on it. Otherwise hold only
the work that depends on the answer.

A logged question, a held pull request, or a parked item stops only the work
that depends on it. Keep every independent assignment moving. Answer every
question a worker sends, by a default or by holding its work, so no worker is
left waiting for a reply.

## The ready-for-operator list

Keep one list in the record, complete and unfiltered:

- every held pull request, with the checklist line that held it and any
  unticked review items;
- every open question, with the default taken and whether work proceeded on it;
- every parked item awaiting the operator, with the pull request it blocks;
- every worker that needs the operator to move, replace, or re-account it;
- every merge made, with the pull request and the head merged.

Do not cap, sample, or summarize it away. It is the operator's whole picture
of the run.

## Standing rules

Keep the arrangement's standing rules in the record. When an incident shows
workers need a rule the briefs lack, add it without asking: one dated rule,
tied to the named incident that caused it. Send it to affected workers as an
amendment, and list each new rule in your next report to the operator. A
standing rule only adds a restriction on how workers operate.

## Waits

Record every wait in the record with what ends it:

- a worker whose last line names a running job, such as a verification run or
  a `ce-babysit-pr` watch, waits until that job ends;
- a worker stopped by a usage limit waits until the reset time;
- an enqueued pull request waits until it reads merged or leaves the queue;
- a worker that asked a question waits until you reply.

A report that a worker stopped is an event, not the worker's current state.
Re-read the worker's live state before acting on it. When the stop matches a
recorded wait, leave the worker alone: do not escalate, nudge, or reassign it.

The stall sweep acts on two things only. For each recorded wait that has
ended, it takes the next step: continue the worker, reply merged, return an
ejected pull request to its worker, or answer the question. For each open
assignment with no recorded wait, no hold, and no running job, it tells the
worker to continue.

Moving, replacing, or switching the account of a worker waits for the
operator and goes on the ready-for-operator list.
