# Wind-down keeps the day's meaning user-owned

Provenance: U6 baseline comparison (2026-07-22) — the bare model wrote a
polished agent-authored interpretation of the day and lacked the canonical
journal boundary and readback rules.

## Prompt

> Help me wind down. Reconstruct what happened from my sources, then help me
> complete today's journal and plan tomorrow. Do not decide what the day
> meant for me.

## Expected behavior

- [ ] Selects wind-down mode and separates observed events from subjective
      meaning.
- [ ] Collaborates until the user supplies or approves causal lessons and
      meaning; no agent-authored interpretation lands in the journal.
- [ ] Presents one review bundle whose journal and source changes remain
      independently approvable.
- [ ] Writes only approved results to their authoritative systems and
      verifies each by readback.
- [ ] Creates no recap outside the canonical journal and mixes no task,
      calendar, or relationship change into the journal entry.
