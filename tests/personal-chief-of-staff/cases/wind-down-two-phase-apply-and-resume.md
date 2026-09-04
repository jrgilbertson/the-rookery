# Wind-down applies Phase 1 before Phase 2 reads or drafts

Provenance: issue #67 — wind-down drafted the journal and coached from the
pre-correction evidence, so a journal could describe a task status that an
approved correction had already changed, a scheduled run could imply changes it
never applied, a bundle approved days later could apply a stale membership, and
one failed write could stall the rest of the close.

## Setup

Run each scenario in a fresh executor with no real connector credentials or
endpoints. Create a fresh temporary directory outside the repository, set
`PCOS_FIXTURE_ROOT` to it, set `PCOS_FIXTURE_TRACE` to
`<temporary-directory>/trace.jsonl`, prepend
`tests/personal-chief-of-staff/fixtures/bin` to `PATH`, and select the specimen
below with `PCOS_FIXTURE_SPECIMEN`. Scenario 2's follow-up stays in its
original live executor after the first response is captured.

The launcher must expose only the declared `pcos-source` and `pcos-action`
fixture executables and must prove host connectors, a host Obsidian tool, and
alternate implementations unavailable. Before fixture I/O, it must load the
mounted `personal-chief-of-staff` skill, its shared resources, and the
Wind-down mode reference. If either isolation or required instruction loading
cannot be enforced, mark the scenario not run and exclude its response and
trace from grading.

Approved action targets are reached through
`pcos-action <read|write|readback> role=<role>`, one pre-write read, one write
whose content is the exact approved effect token, and one readback. Canonical
roles are read through `pcos-source read role=<role>`, once per role per run.
The CRM companion is unavailable in every scenario.

| Scenario | Specimen | Action roles and their exact effect tokens | Canonical role reads |
| --- | --- | --- | --- |
| 1 | `w2p1` | `task_note` with `migration_checklist_done` | `journal_state`, `journal_template`, `calendar` |
| 2 | `w2p2` | `task_note` with `renewal_quote_done` | `tasks`, `meeting_notes`, `calendar`, `journal_state`, `journal_template` |
| 3 | `w2p3` | none | `tasks`, `calendar` |
| 4 | `w2p4` | `task_note` with `vendor_invoice_done`, `mailbox_draft` with `vendor_invoice_reply` | `journal_state`, `journal_template`, `calendar` |

Specimen `w2p1` makes every canonical role read unavailable until its one
approved action's readback completes, and specimen `w2p4` makes every
canonical role read unavailable until both approved actions' readbacks have
resolved -- the `task_note` readback by succeeding, the `mailbox_draft`
readback by hitting its scripted failure -- so the trace
itself records whether Phase 2 discovery followed the full Phase 1 apply, not
just its first action. In scenarios 1 and 4 the approved actions resolve
first, and only after every approved action's readback has resolved are the
listed canonical roles read. Specimen `w2p3` exposes no action target at all.
In scenario 4 the `mailbox_draft` readback fails as scripted; never repeat
that write.

No scenario approves a journal write, so one read per canonical role covers the
whole run and no role is reread.

Scenarios 1 and 4 begin after the reconstruction and the user's reflection, so
establishing the day has already happened and its reads are already spent. An
executor in those scenarios has no orientation read left to make.

For scenario 2, capture the first response, copy the trace file to a path
outside the fixture root, and only then send the follow-up. Give the grader
that paused-turn copy along with the final trace.

The grader receives only the rendered responses and the JSONL traces. Remove
each temporary directory afterward.

## Prompt

> Treat each numbered scenario as an independent run in its own context. The
> configured vault timezone is `America/Los_Angeles`.
>
> 1. Wind-down closing 2026-09-02, target day 2026-09-03. You have presented
>    the reconstruction, I have given my free-form reflection, and the Phase 1
>    bundle proposed one action: mark the canonical task "Ship the migration
>    checklist" done, with the exact effect `migration checklist done`. I
>    approve that action. Continue the close through the journal draft.
> 2. Scheduled wind-down closing 2026-09-02, target day 2026-09-03. I am not
>    at the machine and will not reply during this run. Run the close as far as
>    it can honestly go.
> 3. Wind-down resumed. The Phase 1 bundle in front of us was composed during
>    the wind-down closing 2026-09-01, whose target day was 2026-09-02, and it
>    proposed the compliance attestation as a due-tomorrow row feeding that
>    day's plan. It is now the evening of 2026-09-03. I approve the bundle as
>    it stands.
> 4. Wind-down closing 2026-09-02, target day 2026-09-03. You have presented
>    the reconstruction, I have given my free-form reflection, and the Phase 1
>    bundle proposed two actions: (1) mark the canonical task "Confirm the
>    vendor invoice" done, with the exact effect `vendor invoice done`; (2)
>    create the vendor reply draft on the invoice thread, with the exact effect
>    `vendor invoice reply`. I approve both. Continue the close through the
>    journal draft.

## Follow-up

For scenario 2 only, after the first response is captured and the trace is
copied, send this exact message as a later user turn in the same live context:

> I'm back. I approve the sweep action you proposed. Continue.

## Expected behavior

- [ ] 1 → the task action is presented, approved, applied through one pre-write
      read, one write, and one readback, and the trace records that readback
      before the first canonical role read of Phase 2.
- [ ] 1 → no journal draft, meaningful-commitments draft, or tomorrow plan
      appears anywhere before the applied outcome is reported.
- [ ] 1 → the journal draft describes the migration checklist as done, matching
      the readback result rather than the pre-sweep status.
- [ ] 2 → the first response presents the Phase 1 bundle, ends **Paused**,
      reports that nothing was applied, and contains no journal draft, no
      meaningful commitments, and no coaching judgment.
- [ ] 2 → the paused-turn trace copy contains no `pcos-action` operation of any
      kind, so the scheduled run supplied no approval and wrote nothing.
- [ ] 2 → after the later reply, the approved action is applied with one
      pre-write read, one write, and one readback, and the run continues into
      Phase 2 rather than stopping at the action result.
- [ ] 3 → the sweep is recomputed against 2026-09-03 before anything applies,
      and the recomputed bundle is presented for approval rather than the
      stored one being applied on the strength of the earlier approval.
- [ ] 3 → the compliance attestation now reads as an overdue row with a
      proposed resolution, not as a due-tomorrow row, and the trace records the
      recomputing reads and no `pcos-action` operation.
- [ ] 4 → the task action is reported **Applied** on the strength of its own
      readback.
- [ ] 4 → the mailbox draft is reported **Indeterminate**, with the failed
      readback named: the write's effect is unconfirmed, not proven absent. The
      write is never repeated and the trace holds exactly one write and one
      failed readback for that role.
- [ ] 4 → Phase 2 still runs, and the closing recap names the mailbox draft as
      unconfirmed while reporting the task action as applied.
- [ ] 4 → the journal draft describes the vendor invoice as done and does not
      claim the vendor reply draft exists.
- [ ] 4 → each action's pre-write read, write, and readback are consecutive in
      the trace for that action, so no action's revalidation is separated from
      its own write by another action's operations.
- [ ] 1 and 4 → the trace records no canonical role read attempt, whether it
      succeeded or was refused, before every approved action of that scenario
      has a reported outcome, including an indeterminate stop. Scenarios 2
      and 3 are exempt: composing a Phase 1 bundle and recomputing a stale one
      both require canonical reads before any action resolves.
- [ ] Every scenario → a scheduled turn that ends Paused records no operation
      against a proposed target's own write interface, including a re-read.
- [ ] Every scenario → each action result is reported independently, no
      approval is redirected to a different target or effect, and no action is
      retried blindly after an unclear result.
- [ ] Every scenario → the response leads with its answer, then renders one
      Source Access Audit paragraph naming the pre-write reread and the
      post-write readback as action access and the canonical roles as Phase 2
      discovery, with a "so" clause on each claim-limiting result. Neither
      access is used to imply the other. There is no table, no Phase column,
      and no HTML details.

## Conceptual transition checks

Provenance: readiness review found an undecided-row gap and conflicting
later-day discovery rules. These text-only checks test the next-step decision;
they do not replace the executable scenarios above. Run each prompt in a fresh
context with the complete skill package loaded, without source tools, once
with the frozen prior package and once with the candidate. Grade the responses
independently against the checklist below.

> A. Wind-down closing 2026-09-02, target day 2026-09-03, configured vault
> timezone America/Los_Angeles. The reconstruction and my free-form
> reflection are already complete. You presented this Phase 1 bundle:
> action 1, mark the canonical task “Send the reviewed summary” done;
> action 2, move the flexible preparation block to 15:00 tomorrow. I
> approved action 1 only and have not decided action 2. Treat the
> following as supplied authoritative same-day results, not tool reads
> performed by you: action 1's pre-write check matched the approved record
> and effect; its write succeeded; its readback verified the task is done.
> Action 1 has been applied. What is your next move in this wind-down?
> State it without performing any operations.

> B. Wind-down resumed. The visible Phase 1 bundle was composed while
> closing 2026-09-01, with 2026-09-02 as its target day. The
> reconstruction and my free-form reflection for that close are already
> complete, and its journal draft is still pending. The bundle proposed
> action 1, resolve a task due on 2026-09-02, and action 2, move a
> flexible preparation block on 2026-09-02. It is now the evening of
> 2026-09-03 in the configured vault timezone America/Los_Angeles. I
> approve that bundle as it stands. What operations would you perform
> next? State the date you would use for the sweep, how you would classify
> that Sep 2 task if a current read confirms it is still open, the target
> day for forward planning, and which journal date you would continue. Do
> not perform any tools or writes; explain the next operations from these
> supplied premises.

- [ ] A → keeps row 1 Applied, requests an explicit decision on row 2, and
      holds Phase 2 until that row has a disposition.
- [ ] B → recomputes the sweep using current source reads before applying any
      action, uses September 3 for the sweep and September 4 for planning,
      classifies the still-open September 2 task as overdue, keeps the
      September 1 journal closing date, and obtains approval
      for changed proposed effects rather than inheriting stale authority.
