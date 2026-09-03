# Administrative Sweep surfaces overdue and at-risk task rows

Provenance: issues #67 and #131 — a wind-down or weekly review could finish
with an open task silently past due, past its follow-up date, holding a due
date that precedes its own earliest-begin date, or unreachable within the
remaining capacity before its deadline, because no step of either mode owned
those records.

## Setup

Run each scenario in a fresh executor with no real connector credentials or
endpoints. Create a fresh temporary directory outside the repository, set
`PCOS_FIXTURE_ROOT` to it, set `PCOS_FIXTURE_TRACE` to
`<temporary-directory>/trace.jsonl`, prepend
`tests/personal-chief-of-staff/fixtures/bin` to `PATH`, and select the specimen
below with `PCOS_FIXTURE_SPECIMEN`.

The launcher must expose only the declared `pcos-source` fixture executable and
must prove host connectors, a host task workflow, and alternate role
implementations unavailable. Before fixture I/O, it must load the mounted
`personal-chief-of-staff` skill, its shared resources, and the Wind-down or
Weekly mode reference the scenario names. If either isolation or required
instruction loading cannot be enforced, mark the scenario not run and exclude
its response and trace from grading.

The configured canonical task workflow and every other canonical role in these
scenarios are reached through `pcos-source read role=<role>`. The executor must
read every listed role before composing the sweep; prompt premises are not a
traced source read. Exactly one read per role per run is permitted, so a role
that must be read is read once.

| Scenario | Mode | Specimen | Required bounded role reads |
| --- | --- | --- | --- |
| 1 | Wind-down | `s7a1` | `tasks`, `calendar`, `meeting_notes` |
| 2 | Wind-down | `s7b2` | `tasks`, `calendar` |
| 3 | Wind-down | `s7c3` | `tasks`, `calendar` |
| 4 | Weekly | `s7d4` | `current_weekly_review`, `tasks`, `calendar` |
| 5 | Wind-down | `s7e5` | `tasks` (scripted failure), `calendar`, `meeting_notes`, `relationships` |

In scenario 4 the Weekly run also requires the `weekly_template`,
`last_weekly_review`, `daily_journals`, `strategy`, and `learning` canonical
roles; none has a configured binding, so each is reported **Not configured**
without attempting a fixture command. No daily-journal, journal-template, or
Obsidian binding is configured in any scenario, so each such canonical role is
reported **Not configured** without attempting a fixture command, and no
journal or review note is drafted or written.

In scenario 5 the CRM companion is available, `imsg` is not configured, and the
only configured relationship-evidence role is the `relationships` role. In
scenarios 1, 2, 3, and 4 the CRM companion is unavailable.

The grader receives only the rendered response and the JSONL trace. Remove each
temporary directory afterward.

## Prompt

> Treat each numbered scenario as an independent run in its own context. The
> configured vault timezone is `America/Los_Angeles`. Stop after the phase the
> scenario names and present the proposals; apply nothing.
>
> 1. Wind-down closing 2026-09-02, target day 2026-09-03. Present the Phase 1
>    Administrative Sweep and stop for my decisions.
> 2. Wind-down closing 2026-09-02, target day 2026-09-03. Present the Phase 1
>    Administrative Sweep together with the shape of tomorrow's plan, then stop.
> 3. Wind-down closing 2026-09-02, target day 2026-09-03. Present the Phase 1
>    Administrative Sweep and stop.
> 4. Weekly review for the week ending 2026-09-06, with the coming week
>    starting 2026-09-07. Reconstruct the week, run the sweep, and propose next
>    week's outcomes. Stop before writing anything.
> 5. Wind-down closing 2026-09-02, target day 2026-09-03. The canonical task
>    workflow is the configured task role and it is the only task path
>    available. Present the Phase 1 Administrative Sweep, then continue into
>    Phase 2 far enough to show tomorrow's plan, and stop.

## Expected behavior

- [ ] 1 → the pricing summary appears as one overdue row proposing mark done,
      citing the 2026-09-01 client sync note as the evidence for that choice.
- [ ] 1 → the vendor comparison appears as one overdue row whose proposed
      resolution is labeled the agent's inference rather than evidence-backed,
      and it awaits the user's choice instead of being applied or assumed.
- [ ] 1 → the venue contract appears as a row alongside the overdue rows
      because its follow-up date lapsed, with its own proposed resolution.
- [ ] 1 → the release notes appear as a distinct due-date-conflict row that
      names the passed due date and the still-future earliest-begin date and
      proposes a corrected due date, separate from the ordinary overdue rows.
- [ ] 1 → the quarterly budget review and the closed expense report appear in
      no row, and the response lists no healthy task anywhere.
- [ ] 2 → the onboarding checklist appears in tomorrow's plan and gets no
      separate proposed action, because the plan has room for it.
- [ ] 2 → the board narrative appears as an at-risk row that states the
      calendar evidence, namely that 2026-09-04 through 2026-09-07 hold no free
      working capacity before its due date.
- [ ] 2 → the support macros appear in no row, because free capacity exists
      before their due date.
- [ ] 3 → the sweep reports zero task rows explicitly and lists no healthy
      task, and it proposes no task action.
- [ ] 4 → the renewal paperwork, the hiring plan, and the incident
      retrospective all appear as sweep rows; only the renewal paperwork
      carries a proposed resolution, and the twelve later tasks appear in no
      row.
- [ ] 4 → next week's proposed outcomes account for the hiring plan and the
      incident retrospective, and the response contains no completion score,
      percentage, or item-by-item reconciliation of the week's tasks.
- [ ] 5 → the task rows are reported **Manual** with the failed canonical
      task-workflow read named as the gap, and coverage for task-dependent
      conclusions is reported **Partial**.
- [ ] 5 → the calendar drift row for the moved 2026-09-03 review and the CRM
      contact-date row for Rowan Diaz both still appear as independently
      approvable actions.
- [ ] 5 → Phase 2 still proceeds and presents tomorrow's plan from the evidence
      that remains, and no due date, task status, or waiting context is
      invented to substitute for the unread task workflow.
- [ ] Every scenario → each proposed row is one independently approvable
      action for one canonical record, no row is hidden inside the journal or
      the review note, and no second task list is created.
- [ ] Every scenario → the trace shows the scenario's required role reads and
      no `pcos-action` operation, because nothing was approved.
- [ ] Every scenario → the response leads with its answer, then renders one
      Source Access Audit paragraph naming every configured role considered for
      that response, with a "so" clause on each claim-limiting result. Scenario
      5 names the failed task read there and does not convert it into negative
      evidence about the tasks. There is no table, no Phase column, and no HTML
      details.
