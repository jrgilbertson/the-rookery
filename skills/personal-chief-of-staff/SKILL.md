---
name: personal-chief-of-staff
description: Use when the user wants to complete a daily journal or wind down, requests a daily chief-of-staff review, requests a weekly or quarterly review, later revisits, resumes, approves, edits, defers, skips, or otherwise decides visible chief-of-staff actions, or another workflow requests current cross-source chief-of-staff context. Do not use for isolated task creation, issue writing, email processing, calendar editing, health analysis, meeting preparation, or project planning.
license: MIT
compatibility: Requires access to the user's chosen authoritative sources. Obsidian workflows require a running Obsidian app and its CLI.
---

# Personal Chief of Staff

Turn live personal and work evidence into an interactive review that helps the
user orient, act, reflect, and learn. The user's existing systems remain
authoritative; this skill adds no database, run ledger, cache, or generated
brief archive.

## Resolve visible action responses first

Before selecting a mode, determine whether the current message approves, edits,
defers, skips, declines, revisits, or otherwise decides actions from a visible
chief-of-staff bundle. Resolve the response against that exact bundle and its
originating mode. Do not infer an action from a bare number when the visible
context does not identify it.

For each decided action, use its displayed identity, target, effect, and
approval state. Read both shared resources,
[references/source-behavior.md](references/source-behavior.md) and
[assets/review-bundle.md](assets/review-bundle.md), plus the originating mode
reference, then follow their existing shared and mode-specific application
rules. For an approved Person-note, relationship Task, CRM-derived unrelated
work, or CRM-derived writing-backlog effect, use the available
`managing-personal-crm` companion in embedded mode and follow its
`references/applying-approved-actions.md` semantics. Route CRM-derived
unrelated work through the caller's configured canonical task or issue
workflow and exact displayed destination; route a writing-backlog effect only
through the configured canonical writing workflow and exact displayed
destination. For either, search that destination for complete-meaning
equivalence immediately before mutation. Report an equivalent that has
appeared as **Already satisfied**; otherwise apply once and read the exact
target back through the same authoritative interface. The chief-of-staff
workflow keeps the action number, approval flow, result, and completion state;
the companion creates no nested bundle. If the companion or the required
canonical workflow, exact destination, search, write, or readback path is
unavailable or ambiguous, report that relationship-derived action **Manual**
rather than applying it under generic source rules or another destination.

For CRM-derived communication text, keep the exact displayed text in the
conversation only. Never send it, create a draft, or create another artifact.
If approved unchanged, report the chief-of-staff action **Already satisfied**
because the editable text is already visible. An edit produces a revised
proposal under the same chief-of-staff action number and requires a new exact
approval. Keep its result and completion state with this workflow; do not use a
generic mutation fallback or let the companion create a nested bundle.

An action-only response does not run new review discovery or prepare another
review. It still performs every immediate pre-write target and destination
re-read, equivalence, drift, dependency, and post-write readback check required
by the loaded application rules. Its answer-first action-result narrative stays
separate from the Source Access Audit, which reports only current target or
destination reread and verification readback access. It does not repeat access
from the originating bundle.

If the same message explicitly requests a new review, finish the visible action
decisions first. Then select the requested mode and run its discovery as a
separate read-only phase. Do not use newly retrieved evidence to reinterpret
the earlier decisions. Render one Source Access Audit with a Phase column that
separates action access from review discovery.

Completion: every visible action decision was resolved against its exact
originating bundle and mode before any separately requested review began.

## Supply cross-source context without a review mode

When another workflow explicitly requests current cross-source chief-of-staff
priority or context—and the message is not an action response or a request for
wind-down, weekly, or quarterly review—do not select a review mode. Read
[references/source-behavior.md](references/source-behavior.md) and
[assets/review-bundle.md](assets/review-bundle.md). Retrieve only the evidence
needed for the caller's judgment, distinguish fact from inference, and return
priority context in the conversation with the answer-first Source Access
Audit. The calling workflow retains ownership of its narrower operation. Do
not open Wind-down, Weekly, or Quarterly, and do not invent a Morning path.

Completion: the caller has usable cross-source judgment without a chief-of-staff
mode run or unrequested durable writes.

## Select the mode

Choose exactly one mode from the request:

- **Wind-down:** The user asks to close the day, complete the daily journal,
  reflect, prepare tomorrow, run a daily chief-of-staff review, or invokes the
  scheduled wind-down mode. Generic daily review wording without weekly or
  quarterly context selects Wind-down.
- **Weekly:** The user asks to complete or discuss a weekly review.
- **Quarterly:** The user asks to complete or discuss a quarterly review.

An explicit mode wins. When the request does not identify one of these review
contexts and is not a cross-source context request above, leave it with the
narrower workflow that owns it.

Read both shared resources for every mode:

- [references/source-behavior.md](references/source-behavior.md)
- [assets/review-bundle.md](assets/review-bundle.md)

Then read only the selected mode reference:

- Wind-down: [references/wind-down.md](references/wind-down.md)
- Weekly: [references/weekly.md](references/weekly.md)
- Quarterly: [references/quarterly.md](references/quarterly.md)

Completion: one mode and all required shared and mode-specific resources are
selected before source retrieval begins, or the cross-source non-mode path was
used instead.

## Collaborate on judgment

Continue interactively rather than publishing a report and ending. The agent
may retrieve, organize, compare, and draft substantial objective content. The
user owns or explicitly approves subjective meaning, causal lessons, strategic
judgment, and central published thinking.

Use the shared source behavior and review-bundle shape throughout the
conversation. Present proposed external changes as one bundle with
independently approvable actions.

Completion: the user has had a clear opportunity to correct the review and to
approve, edit, defer, or skip every proposed action independently.

## End explicitly

End the run as exactly one of:

- **Complete:** The review and all approved actions finished.
- **Nothing material:** The evidence supported the review and no attention or
  action was warranted.
- **Partial:** A useful review completed with named evidence limits.
- **Unable to prepare reliably:** Evidence was insufficient for a trustworthy
  review.
- **Paused:** The user intends to continue later.
- **Skipped:** The user chose not to conduct the review.

When resuming, refresh time-sensitive evidence. Resume in the same conversation
when available; otherwise reconstruct from canonical sources, disclose that
uncommitted conversational input is unavailable, and ask only for the missing
human judgment.

Close with a short recap of what changed and what remains unapplied.

Completion: the ending is explicit, accurate, and consistent with the durable
artifacts that now exist.
