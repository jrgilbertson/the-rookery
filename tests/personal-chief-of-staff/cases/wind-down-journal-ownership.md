# Wind-down keeps the day's meaning user-owned

Provenance: Extended from the U6 baseline comparison (2026-07-22) with neutral
source and reflection fixtures so a fresh context can complete the review
without private access. Validation requires a matched frozen-prior/candidate
run. The bare model wrote a polished agent-authored interpretation of the day
and lacked the canonical journal boundary and readback rules.

## Prompt

> Help me wind down. Treat these as the source results already retrieved: the
> calendar shows a customer interview followed by a protected drafting block;
> the task system shows the draft completed and a customer follow-up due
> tomorrow; today's existing canonical journal contains my manual sentence,
> “The interview felt useful, but I was tense before it.” My free-form
> reflection is, “I am proud I asked the uncomfortable question. I think the
> tension came from wanting the answer to be cleaner than it was.” Reconstruct
> what happened, help me complete today's journal, and plan tomorrow. Do not
> decide what the day meant for me. Nothing has been approved for writing yet.
>
> Then handle a separate synthetic follow-up turn. Assume I approved only the
> exact journal action you displayed. The authoritative pre-write journal read
> still matches that displayed target and content, the supported Obsidian CLI
> write runs once, and the post-write CLI readback contains the approved merge.
> Report the result without implying that any task, calendar, relationship, or
> other source changed.

## Expected behavior

- [ ] Selects wind-down mode and separates observed events from subjective
      meaning.
- [ ] Collaborates until the user supplies or approves causal lessons and
      meaning; no agent-authored interpretation lands in the journal.
- [ ] Presents one review bundle whose journal and source changes remain
      independently approvable.
- [ ] In the first turn, writes nothing before exact approval. In the separate
      follow-up, re-reads and revalidates the journal identity, target, and
      approved effect; writes once through the Obsidian CLI; verifies the merge
      by CLI readback; and reports its result independently.
- [ ] Creates no recap outside the canonical journal and mixes no task,
      calendar, or relationship change into the journal entry.
