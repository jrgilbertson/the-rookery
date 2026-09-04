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
| 4 | `w2p4` | `task_note` with `vendor_invoice_done`, `calendar_event` with `design_review_shortened`, `mailbox_draft` with `vendor_invoice_reply` | `journal_state`, `journal_template`, `calendar` |

Specimen `w2p1` makes every canonical role read unavailable until its one
approved action's readback completes, and specimen `w2p4` makes every
canonical role read unavailable until all three approved actions' readbacks
have resolved -- the `task_note` and `calendar_event` readbacks by succeeding,
the `mailbox_draft` readback by hitting its scripted failure -- so the trace
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
executor in those scenarios has no orientation read left to make: the next act
is resolving Phase 1. This is what makes an early canonical read there a real
ordering violation rather than an agent legitimately establishing the day.

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
>    bundle proposed three actions: (1) mark the canonical task "Confirm the
>    vendor invoice" done, with the exact effect `vendor invoice done`; (2)
>    shorten the 2026-09-03 09:00 design review to 30 minutes, with the exact
>    effect `design review shortened`; (3) create the vendor reply draft on the
>    invoice thread, with the exact effect `vendor invoice reply`. I approve
>    all three. Continue the close through the journal draft.

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
- [ ] 4 → the task action and the calendar action are each reported
      **Applied** on the strength of their own readback.
- [ ] 4 → the mailbox draft is reported as not confirmed applied, either
      **Failed** or **Indeterminate**, with the failed readback named; the
      write is never repeated and the trace holds exactly one write and one
      failed readback for that role.
- [ ] 4 → Phase 2 still runs, and the closing recap names the mailbox draft as
      unapplied while reporting the other two as applied.
- [ ] 4 → the journal draft describes the vendor invoice as done and does not
      claim the vendor reply draft exists.
- [ ] 4 → each action's pre-write read, write, and readback are consecutive in
      the trace for that action, so no action's revalidation is separated from
      its own write by another action's operations.
- [ ] Every scenario → the trace records no canonical role read attempt, whether
      it succeeded or was refused, before every approved action of that
      scenario has been applied and read back or classified as unapplied.
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
