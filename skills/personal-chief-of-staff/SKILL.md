---
name: personal-chief-of-staff
description: Use when the user asks what needs attention today, requests a morning or daily chief-of-staff review, wants to complete a daily journal or wind down, requests a weekly or quarterly review, later revisits, resumes, approves, edits, defers, skips, or otherwise decides visible chief-of-staff actions, or another workflow requests current cross-source chief-of-staff context. Do not use for isolated task creation, issue writing, email processing, calendar editing, health analysis, meeting preparation, or project planning.
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
approval state. Read [references/source-behavior.md](references/source-behavior.md)
and the originating mode reference, then follow their existing shared and
mode-specific application rules. For an approved Person-note, relationship
Task, or CRM-derived writing-backlog effect, use the available
`managing-personal-crm` companion in embedded mode and follow its
`references/applying-approved-actions.md` semantics. Apply a writing-backlog
effect only through the configured canonical writing workflow and exact
displayed destination, after a complete-meaning equivalence search, then read
the target back through the same authoritative interface. The chief-of-staff
workflow keeps the action number, approval flow, result, and completion state;
the companion creates no nested bundle. If the companion or the required
canonical destination, search, write, or readback path is unavailable or
ambiguous, report that relationship-derived action **Manual** rather than
applying it under the generic source rules.

An action-only response does not run new review discovery or prepare another
review. It still performs every immediate pre-write target and destination
re-read, equivalence, drift, dependency, and post-write readback check required
by the loaded application rules.

If the same message explicitly requests a new review, finish the visible action
decisions first. Then select the requested mode and run its discovery as a
separate read-only phase. Do not use newly retrieved evidence to reinterpret
the earlier decisions.

Completion: every visible action decision was resolved against its exact
originating bundle and mode before any separately requested review began.

## Select the mode

Choose exactly one mode from the request:

- **Morning:** The user asks what needs attention today, requests a morning
  review or a generic daily chief-of-staff review without explicit evening or
  wind-down context, invokes the scheduled morning mode, or another workflow
  explicitly requests current cross-source priority context. The calling
  workflow retains ownership of its narrower operation.
- **Wind-down:** The user asks to close the day, complete the daily journal,
  reflect, prepare tomorrow, or invokes the scheduled wind-down mode.
- **Weekly:** The user asks to complete or discuss a weekly review.
- **Quarterly:** The user asks to complete or discuss a quarterly review.

An explicit mode wins. When the request does not identify one of these review
contexts, leave it with the narrower workflow that owns it.

Read both shared resources for every mode:

- [references/source-behavior.md](references/source-behavior.md)
- [assets/review-bundle.md](assets/review-bundle.md)

Then read only the selected mode reference:

- Morning: [references/morning.md](references/morning.md)
- Wind-down: [references/wind-down.md](references/wind-down.md)
- Weekly: [references/weekly.md](references/weekly.md)
- Quarterly: [references/quarterly.md](references/quarterly.md)

Completion: one mode and all required shared and mode-specific resources are
selected before source retrieval begins.

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
