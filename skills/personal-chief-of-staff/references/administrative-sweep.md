# Administrative Sweep

Wind-down and Weekly sweep the configured canonical open tasks and the records
their review touches.
Quarterly runs no sweep. Surface records that evidence shows need correction
or a decision, plus tasks due in the planning window. Omit other sweep-discovered
tasks from the response, including outcomes and capacity explanations, unless
the user selected them or a separately evidenced review priority requires them.
Spare capacity alone does not make a task relevant. Report sweep coverage in
aggregate: "None of three open tasks qualified." Zero findings is valid.

## Set the dates

| Mode | Closing day | Planning window, inclusive |
| --- | --- | --- |
| Wind-down | Local day being closed | Following local day |
| Weekly | Last day of the reviewed week | Following day through the last day of the coming week |

Use the planning window's last day as the target day. When a later-day resume
requires recomputing the bundle under "End and resume honestly" in
`source-access.md`, re-establish these dates before recomputing membership.
Wind-down retains its original journal date as its mode reference requires.

## Find corrections and planning context

Cover task state, calendar drift (time, participants, or existence), CRM contact
dates and Person effects through the companion, owed or incorrect
communication text, repository or issue state, and strategy or learning
updates already supported by dated durable evidence.

Complete the configured canonical open-task sweep before treating Wind-down or
Weekly as reviewed. A task read for incidental context is not sweep coverage.
Read open tasks through the configured canonical task or issue workflow:

| Task finding | Condition | Treatment |
| --- | --- | --- |
| Due-date conflict | Due date precedes earliest-begin (`not_before`) | Propose a resolution instead of an ordinary overdue row. |
| Overdue | Due on or before the closing day | Propose a resolution. |
| Follow-up due | Follow-up date on or before the closing day | Treat as overdue and propose a resolution. |
| Upcoming | Due anywhere in the inclusive planning window | Feed the plan; propose an action only when the plan cannot hold it. |
| At risk | Due after the planning window, but remaining work cannot fit the free calendar capacity from the later of the window's first day and earliest-begin (`not_before`, when set) through the due date | State that capacity evidence and propose a resolution. |

For each correction, propose one independently approvable action per record.
Combine overlapping task findings into that row. For an overdue, follow-up-due,
due-date-conflict, or at-risk task, choose a new due date, mark done, cancel,
remove the due date, or record waiting context. Cite evidence explaining the
choice; when it does not settle the choice, label the recommendation as an
inference awaiting approval.

Include content required by the canonical workflow in the proposed effect:
completion needs a completed definition of done and result or deliverables;
cancellation needs a reason; waiting needs a party and follow-up date. Draft
and write are one proposed record change, not separate actions. Never invent
source state to fill these fields.

## Reconcile already-retrieved inbox evidence

Within the already-authorized bounded inbox slice, reconcile important requests,
actual deadlines, and waiting-for changes with configured canonical tasks.
Resolved requests and optional reading create no obligation. For each material
item:

1. Read bounded thread context only when the existing authorized scope permits
   it. Retain the source account, thread identity, and links.
2. Search the configured task workflow for a task with the same complete
   meaning.
3. When one exists, link the item to that canonical record. Propose one
   correction only when the evidence changes its commitment.
4. When none exists, propose a task candidate. When the match stays
   unresolved, report it as uncertain rather than proposing a duplicate.

Apply the overdue and follow-up-due rows above to promised responses and
dependencies from others. Distinguish an evidenced promise or follow-up date
from an inferred expectation; an undated expectation is not an evidenced overdue
promise.

This is part of the current sweep, not standalone triage, inbox ranking, or a
wider mailbox scan.

## Apply through the owning workflow

Task reads and approved writes use the configured canonical workflow; create
no second task list. If that workflow, exact target, write, or readback path is
unavailable or ambiguous, report affected task actions **Manual**, name the
gap, mark task-dependent coverage **Partial**, and continue with the remaining
evidence. Relationship effects use the [companion rules](crm-companion.md).
All effects retain the [exact-approval and readback requirements](action-application.md).

Completion: canonical open-task coverage and bounded inbox reconciliation are
reported at the scope actually inspected; every qualifying correction has one
proposed action, upcoming context feeds the plan, healthy records remain
unlisted, and coverage gaps or zero findings are reported honestly.
