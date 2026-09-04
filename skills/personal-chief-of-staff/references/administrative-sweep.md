# Administrative Sweep

Wind-down and Weekly read this before composing their sweep. Quarterly does
not run a sweep and does not read this file.

Modes that correct sources run one sweep over the canonical records the review
touches. Propose exactly one independently approvable action for every record
the window's evidence shows is now wrong or now needs a decision, and list
nothing that is healthy. Zero rows is a valid result and is reported as such.

Reporting the sweep's coverage is not the same as listing what it cleared. Name
the record kinds the sweep covered and say that none qualified. Then stop.

How many records the sweep covered is useful and may be said. Which ones they
were is a task-list dump. "None of the three open
tasks qualified" reports coverage. "The three open tasks are due 2026-09-24,
2026-10-02, and 2026-10-15, none overdue" identifies each healthy record and is
the failure. A healthy record's title, date, or other
identifying detail belongs in neither the sweep nor the bundle.

The mode supplies the window as two dates: a closing day and a target day.
Read the row definitions below against those two dates as the window's start
and end. A mode whose window spans a range still supplies a single closing
day and a single target day for that range; it is not forced to pretend the
range is a single closing moment.

Cover these records:

- Tasks, as the rows defined below.
- Calendar drift, where an event's time, participants, or existence no longer
  matches the evidence.
- CRM contact dates and Person effects, routed through the companion below.
- Communication text the evidence shows is owed or now wrong.
- Repository and issue records whose state no longer matches observed work.
- Strategy or learning updates that dated durable evidence already supports.

Read open tasks through the caller's configured canonical task or issue
workflow, and cover:

- open tasks due before the closing day;
- open tasks due on the target day;
- tasks whose follow-up date falls on or before the closing day, treated like
  overdue tasks;
- later-dated tasks that are at risk, meaning the task's remaining work cannot
  fit the free capacity between the target day and its due date as read from
  the calendars. State that calendar or capacity evidence in the row;
- an open task whose due date has passed while its earliest-begin property
  (`not_before` in that workflow) is still in the future. This is a
  due-date-conflict row with its own proposed resolution, not an ordinary
  overdue row.

Each overdue, follow-up-due, or due-date-conflict row proposes one resolution:
a new due date, mark done, cancel, remove the due date, or record waiting
context. Cite the window's evidence when it explains the choice, and label the
resolution as the agent's inference when no evidence explains it. A
due-tomorrow row feeds the next-day plan instead; propose an action for it only
when that plan cannot hold it.

Some resolutions need content the canonical task workflow requires before it
accepts the write: a completed definition of done plus a result or deliverables
section to close a task, a cancellation reason to cancel one, and both a
waiting party and a follow-up date to record waiting. Draft that content inside
the row's proposed effect so the user approves the exact content before the
write. Do not split the row into a draft action and a separate write action;
one record still gets one action.

Read and write task state only through that configured canonical workflow.
Never create a second task list. If the workflow, the exact target, or its
write or readback path is unavailable or ambiguous, report the task rows
**Manual**, name the gap, treat coverage for task-dependent conclusions as
**Partial**, and continue the rest of the mode from the evidence that remains.
Never invent a due date, status, or waiting context as a substitute.

Completion: every record the window's evidence shows is wrong or undecided has
exactly one proposed action, nothing healthy is listed, and a zero-row sweep or
an unavailable task workflow is reported honestly.
