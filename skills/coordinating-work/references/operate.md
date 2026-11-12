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

When a worker fails to start, follow the guide's recovery path. Read the
cause, retry once on the same task when the cause was transient, and
otherwise put the assignment on the ready-for-operator list. Never route
around the guide's retry limit.

## The merge checklist

A worker asks when its `ce-babysit-pr` run reports looks merge-ready. Merge
only when every line below is true. The worker's message is a claim: line 2
checks what it claims, and lines 3 and 4 are facts you read yourself from the
pull request when you decide, never from the message or from memory.

1. **Grant.** The record holds the setup proposal the operator approved, it
   shows a merge bar and hold classes, and this pull request's issue is in
   its batch.
2. **Report.** The worker quoted the first line of `ce-babysit-pr`'s
   continuous-watch report, that line says the pull request looks merge-ready
   and adds no condition, such as updating the branch or a position in a
   stack, and the worker gave the head commit that report covered. A closing
   phrase that leaves the merge to the reader is not a condition.
3. **Routine.** The diff touches no hold class; a change that relates to a
   class at all, wording and tests included, touches it. The pull request
   body has no unticked item under `lfg`'s unapplied review findings.
   The record shows no report from its worker that `ce-babysit-pr` parked an
   item on it for a human. Merging it starts only what the proposal
   showed.
4. **Current.** Read the pull request now: its head is the reported commit,
   checks have reported on that head and every one finished without failing,
   no review thread is open, no review requests changes, and the branch is
   not behind its base. A check that finished neutral or skipped has finished
   without failing.
5. **Merge.** Merge that head with the merge conditional on the reported
   commit, and read the pull request once more to confirm it landed. Never
   use an override or bypass a protection: a merge the repository refuses
   fails this line.

A line that is false, that you cannot read, or that is unclear means no merge.
So does any situation this list does not describe. Then:

- when the worker can make the line true, reply with what to do, such as
  fixing a failed check, resolving a thread, updating a stale branch, or
  running the continuous watch and asking again;
- otherwise leave the pull request open, add it to the ready-for-operator list
  with the line that failed, and reply that it is held for the operator. When
  a pull request will be held anyway, hold it without first sending fixable
  lines back.

Nobody keeps a held pull request current. Its entry on the list says it may
have fallen behind its base. Bringing a held pull request in the batch
current, or applying an open finding on it, is allowed work to assign when
the operator asks for it.

Hold-class pull requests stay open no matter how clean they are.

After a merge, record it and reply merged. Where the repository merges through
a queue, the merge is an enqueue: record a wait for that pull request, and
reply merged only once it reads merged.

After every decision, merged or not, dispatch the next ready issue in the
batch the approved proposal lists. When none remains, dispatch nothing and
note on the ready-for-operator list that the batch is finished.

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

Give the operator one list, complete and unfiltered, read from the record's
log and table:

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
- an enqueued pull request waits until it reads merged or leaves the queue.

A question a worker asked is not a wait. It is your work, and the worker is
waiting on you.

A report that a worker stopped is an event, not the worker's current state.
Re-read the worker's live state before acting on it. When the stop matches a
recorded wait, leave the worker alone: do not escalate, nudge, or reassign it.

The stall sweep takes its worker and pull request identifiers from the
record's table each time it runs, never from its own stored prompt, and is
cancelled when no assignment is open. It does three things. It answers every question still
unanswered. For each recorded wait that has ended, or whose end it cannot
determine, it takes the next step: continue the worker, reply merged, or
return an ejected pull request to its worker. For each open assignment with
no recorded wait, no hold, and no running job, it tells the worker to
continue.

Moving, replacing, or switching the account of a worker waits for the
operator and goes on the ready-for-operator list.
