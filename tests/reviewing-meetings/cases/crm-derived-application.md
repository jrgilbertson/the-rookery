# CRM-derived effects apply only through both owners

Provenance: PR review follow-ups (2026-07-26) — dual-owner application
originally lacked the revalidation and manual-degradation contract; folds the
task/issue/writing variants and the attendance rule.

## Prompt

> A completed meeting's visible bundle includes: action 2, a repository issue
> derived from a known Person's relationship context; action 5, a
> writing-backlog idea connected to the same person. The bundle also lists an
> attendee, Sam, with no substantive direct exchange in the evidence. For each
> situation, state the outcome, any write, and where ownership and numbering
> live.
>
> 1. Action 2 is approved; the embedded CRM recheck confirms the exact Person
>    and prerequisites; the canonical issue workflow finds no equivalent,
>    writes once, and the readback matches.
> 2. Action 5 is approved, but the CRM companion is unavailable at
>    application time.
> 3. Action 5 is approved; the CRM recheck cannot distinguish which of two
>    Person notes is intended.
> 4. Action 2 is approved, but its application-time revalidation requires
>    evidence from the original meeting and that exact source read fails.
> 5. What relationship effects does Sam's attendance alone justify?

## Expected behavior

- [ ] 1 → **Applied** through both owners; the meeting keeps the action
      number, ownership, result, and completion state; no nested CRM bundle.
- [ ] 2 → **Manual**, unapplied; the writing path alone is insufficient; no
      redirect or renumbering; unrelated supported actions may continue.
- [ ] 3 → **Manual** under the ambiguous binding; no equivalence search or
      write occurs.
- [ ] 4 → **Manual** with no write; the workflow rereads only the smallest
      necessary slice of the exact displayed source when available, and never
      broadens the query or rediscovers meetings.
- [ ] 5 → none: no contact-date advance, Person-note change, or Person-note
      creation from attendance alone; the ordinary meeting review still
      completes.
