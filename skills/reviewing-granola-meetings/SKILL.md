---
name: reviewing-granola-meetings
description: Use when the user asks to review, process, import, catch up on, or check for new Granola meetings after they end, or when a scheduled post-meeting review invokes it. Do not use for preparing an upcoming meeting, taking live notes, reviewing a transcript from another source, maintaining a CRM, or directly creating tasks, issues, or calendar events without meeting review.
license: MIT
compatibility: Requires readable Granola meeting data plus access to the configured approved-note source and live meeting template. Pending suppression also requires retrievable current-conversation history. When Obsidian owns the notes or template, its CLI must be available.
---

# Reviewing Granola Meetings

Turn completed Granola meetings into grounded proposals for review. Scheduled
and manual entry use this same workflow. A schedule supplies timing, not extra
authority: every run remains read-only until the user reviews a proposal.

## Select the source scope

For a manual request, use the named meeting or time range. If neither is given,
use the most recent seven days. For a scheduled request, use the supplied range
or default to the most recent seven days. The overlap is intentional because
eligibility comes from observable source state, not a last-run cursor.

Read [references/source-interpretation.md](references/source-interpretation.md)
before retrieving meeting data.

Completion: the run has a bounded source window and has loaded the source
interpretation rules.

## Discover and classify meetings

Retrieve meetings in the source scope, then classify every returned meeting by
stable Granola ID. A meeting is eligible only when it has ended, has a stable
ID, and contains enough source material for a grounded proposal.

Compare exact Granola IDs against approved meeting notes. When current
conversation history is retrievable, also compare them against visible pending
and dismissed proposals in this conversation. Classify each meeting as exactly
one of:

- **Newly proposed:** eligible and not otherwise represented.
- **Already pending:** a proposal with the exact ID is retrievable in this
  conversation.
- **Already approved:** one approved note contains the exact ID.
- **Waiting for source:** the meeting has not ended or its source is still
  processing or insufficient.
- **Collision stop:** more than one approved note has the exact ID, the intended
  filename is occupied by a different meeting, or source identity conflicts.
- **Dismissed in this conversation:** the user dismissed the exact meeting here.
- **Unable to prepare:** required source access or stable identity cannot be
  established.

An approved note remains authoritative even when later Granola content changes.
Treat a changed source as evidence for a separately reviewed revision only when
the user asks to revisit that meeting.

Completion: every discovered meeting has one observable disposition, and no
cursor, ledger, database, state file, transcript archive, or generated marker
was created.

## Prepare only new proposals

For every newly proposed meeting, prepare one review section containing:

- the stable Granola ID and source link for identity checking;
- the actual meeting start time and a normalized proposed title;
- the proposed filename using the actual start timestamp plus the title;
- a preview shaped by the configured live meeting template; and
- any material ambiguity or evidence limitation the user must resolve.

Keep the proposal inside the conversation. Do not create or edit a meeting note
while preparing it. Present all newly proposed meetings from this run together,
grouped by meeting. Later runs append only newly eligible meetings; they do not
repeat, renumber, or recompute older pending proposals. They may add one terse
count or reminder that older work remains pending.

If current conversation history is unavailable, disclose that pending and
dismissed suppression cannot be verified. Continue using exact-ID checks
against approved notes, and do not claim the result is free of pending
duplicates.

Completion: the bundle contains every and only newly proposed meeting from this
run, or states that there is no new meeting to review.

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
