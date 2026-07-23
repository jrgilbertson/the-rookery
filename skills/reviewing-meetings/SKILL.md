---
name: reviewing-meetings
description: Use when the user asks to review, process, import, catch up on, or check for newly completed meetings from a configured meeting source, including Granola; when a scheduled post-meeting review invokes it; or when the user later approves, edits, defers, or skips visible meeting-review actions. Do not use for preparing an upcoming meeting, taking live notes, maintaining a CRM, or directly creating tasks, issues, or calendar events without meeting review.
license: MIT
compatibility: Requires meeting data with stable source IDs, an approved-note source with live template and naming guidance, and an authoritative ownership map for downstream actions. Pending suppression requires retrievable conversation history. When Obsidian owns a target, its CLI must be available.
---

# Reviewing Meetings

Turn completed meetings from the configured source into grounded proposals for
review. Granola is one supported source, not part of the workflow's identity.
Scheduled and manual entry use this same workflow. A schedule supplies timing,
not extra authority: every run remains read-only until the user reviews a
proposal.

## Select the source scope

For a manual request, use the named meeting or time range. If neither is given,
use the inclusive 168-hour interval ending at the query time. For a scheduled
request, use the supplied range or the same 168-hour default. Compare boundary
times as absolute instants. The overlap is intentional because eligibility
comes from observable source state, not a last-run cursor.

Read [references/source-interpretation.md](references/source-interpretation.md)
before retrieving meeting data.

Completion: the run has a bounded source window and has loaded the source
interpretation rules.

## Discover and classify meetings

Retrieve meetings in the source scope, then classify every returned meeting
from observable source state. Once a meeting is source-ready, use its source
name and stable native ID as its exact identity. A waiting meeting may not have
a stable ID yet. A meeting is eligible only when it has ended, has a stable ID,
and contains enough source material for a grounded proposal.

Use the disposition definitions and precedence in the source-interpretation
reference. Compare exact source names and IDs against approved notes and, when
retrievable, visible pending and dismissed proposals in this conversation.

Completion: every discovered meeting has one observable disposition, and no
cursor, ledger, database, state file, transcript archive, or generated marker
was created.

## Prepare only new proposals

Before preparing any newly proposed meeting, read
[references/action-routing.md](references/action-routing.md)
and [assets/review-bundle.md](assets/review-bundle.md). Use the asset for every
meeting proposal and the reference to resolve one authoritative destination for
each supported action. Populate every applicable field in the asset, shape the
preview with the configured live template, and leave unsupported details
explicitly unresolved.

Keep the proposal inside the conversation. Do not create or edit a meeting note
while preparing it. Present all newly proposed meetings from this run together,
grouped by meeting. Later runs append only newly eligible meetings; they do not
repeat, renumber, or recompute older pending proposals. They may add one terse
count or reminder that older work remains pending.

If current conversation history is unavailable, disclose that pending and
dismissed suppression cannot be verified. Continue using exact source-and-ID checks
against approved notes, and do not claim the result is free of pending
duplicates.

Completion: the bundle contains every and only newly proposed meeting from this
run, or states that there is no new meeting to review.

## Route and bind proposed actions

Follow the action-routing reference and review-bundle asset. They define the
supported categories, canonical ownership checks, proposal fields, numbering,
dependencies, and approval presentation. Omit any category whose evidence or
destination is unresolved.

Completion: every proposed action is complete enough to approve independently,
has one authoritative destination, and exposes every prerequisite.

## Apply only exact approvals

On a later user response, follow
[references/applying-approved-actions.md](references/applying-approved-actions.md)
before writing. That reference owns approval binding, pre-write rereads,
atomicity, dependency order, readback, retry boundaries, and application
outcomes.

Completion: each decided action has one readback-backed outcome or an explicit
safe stop, and no action was redirected, duplicated, or retried blindly.

## End explicitly

End the read-only run as one of:

- **Ready for review:** one or more new meeting proposals are waiting for the
  user.
- **Nothing new:** every discovered meeting was already pending, already
  approved, or dismissed in this conversation.
- **Waiting for source:** no meeting is ready, but at least one may become
  eligible when source processing or the meeting finishes.
- **Partial:** useful proposals were prepared, but a named source or continuity
  gap limits part of the result.
- **Unable to prepare:** the run could not establish trustworthy meeting
  identity or content.

When outcomes are mixed, use **Partial** if at least one useful proposal exists
and another meeting or continuity check is limited. With no useful proposal,
prefer **Waiting for source** when every unresolved meeting may become ready
later; use **Unable to prepare** when any collision or required check needs
intervention. Use **Nothing new** only after a successful query with no new or
unresolved meeting.

Summarize the count for each observed disposition. A scheduled run stops after
presenting the read-only result and waits for the user; firing the schedule does
not approve any durable change.

Completion: the ending matches the classified meetings, identifies any limit,
and leaves every durable change unapplied.
