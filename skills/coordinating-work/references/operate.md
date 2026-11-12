# Operate

Read this while running an established arrangement, with or without the
operator present. The entry skill owns shape, authority, briefs, and the
record. Setup produced the approved proposal this file acts under.

## Defaults the proposal shows

**Merge bar.** `ce-babysit-pr` gave its plain looks-merge-ready report on the
pull request's current head. A cautious ready report does not clear the bar,
and neither does a report that tells whoever merges to update the branch.

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

## Deciding a merge-ready question

A worker asks when its `ce-babysit-pr` run reports looks merge-ready. Decide in
this order, and answer the worker each time.

1. **Does the report clear the bar?** If it is cautious, tells the merger to
   update the branch, or names an open item, do not merge. Reply with what is
   missing.
2. **Is the pull request held?** Classify it from its changed files, even when
   the issue was classified at dispatch. Hold it when it falls in a hold
   class, when you cannot tell, or when its body carries an unticked item
   under `lfg`'s unapplied review findings. Leave a held pull request open,
   add it to the ready-for-operator list with the reason and any unticked
   items, and reply that it is held for the operator.
3. **Is it still what the worker reported?** Re-read the pull request
   immediately before merging. Required checks still pass, no review thread is
   open, the branch is not behind its base, and the head is the commit the
   report covered. If any of these fails, return the pull request to its
   worker.
4. **Merge that head.** Make the merge conditional on the reported head
   commit, so a push that lands in between cannot be merged. Confirm the merge
   landed, record it, and reply merged.

Where the repository merges through a queue, enqueue the reported head, record
the pull request as enqueued, and reply merged only once it reads merged. The
stall sweep returns a pull request that left the queue unmerged to its worker.

Hold-class pull requests stay open no matter how clean they are. Then dispatch
the next ready issue.

## Never wait for an answer

Do not open a blocking question dialog and do not stop the arrangement for an
answer, whether or not the operator is present.

On a judgment call the brief, the record, and the standing rules do not
settle, run `ce-pov` to establish a default. Write the question and that
default to the record. When acting on the default is reversible, proceed on
it. When it would deploy, spend, force-push, destroy, or widen any authority,
do not proceed: hold only the work that depends on the answer.

A logged question, a held pull request, or a parked item stops only the work
that depends on it. Keep every independent assignment moving.

When a worker reports an item `ce-babysit-pr` parked, answer it by the same
rule: a default you can decide goes back to the worker as a reply, and one you
cannot goes on the ready-for-operator list with the pull request.

## The ready-for-operator list

Keep one list in the record, complete and unfiltered:

- every held pull request, with why it is held and any unticked review items;
- every open question, with the default taken and whether work proceeded on it;
- every parked item awaiting the operator, with the pull request it blocks;
- every merge made, with the pull request and the head merged.

Do not cap, sample, or summarize it away. It is the operator's whole picture
of the run.

## Standing rules

Keep the arrangement's standing rules in the record. When an incident shows
workers need a rule the briefs lack, add it without asking: one dated rule,
tied to the named incident that caused it. Send it to affected workers as an
amendment, and list each new rule in your next report to the operator.

A standing rule may tighten how workers operate. It never widens merge,
spending, or hold-class authority, and it never removes a hold. When an
incident seems to call for that, log a question instead.

## Stops and waits

A report that a worker stopped is an event, not the worker's current state.
Re-read the worker's live state before acting on it.

When the stopped worker's last line names a running job, such as a
verification run or a `ce-babysit-pr` watch, record a wait and leave the
worker alone. Do not escalate, nudge, or reassign it. The runtime also raises
stops of its own, such as a usage limit with a reset time; these are not
worker blockers, and Revive covers them.

When the last line names no job and the worker has an open assignment with no
hold or dependency, tell it to continue.
