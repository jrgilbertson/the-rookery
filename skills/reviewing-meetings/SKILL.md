---
name: reviewing-meetings
description: Use when the user asks to review, process, import, catch up on, or check for newly completed meetings from a configured meeting source, including Granola, or when a scheduled post-meeting review invokes it. Do not use for preparing an upcoming meeting, taking live notes, maintaining a CRM, or directly creating tasks, issues, or calendar events without meeting review.
license: MIT
compatibility: Requires readable meeting data with stable source IDs plus access to the configured approved-note source and live meeting template. Pending suppression also requires retrievable current-conversation history. When Obsidian owns the notes or template, its CLI must be available.
---

# Reviewing Meetings

Turn completed meetings from the configured source into grounded proposals for
review. Granola is one supported source, not part of the workflow's identity.
Scheduled and manual entry use this same workflow. A schedule supplies timing,
not extra authority: every run remains read-only until the user reviews a
proposal.

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
its source name and stable native ID. A meeting is eligible only when it has
ended, has a stable ID, and contains enough source material for a grounded
proposal.

Compare exact source names and IDs against approved meeting notes. When current
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

An approved note remains authoritative even when later source content changes.
Treat a changed source as evidence for a separately reviewed revision only when
the user asks to revisit that meeting.

Completion: every discovered meeting has one observable disposition, and no
cursor, ledger, database, state file, transcript archive, or generated marker
was created.

## Prepare only new proposals

Before preparing any newly proposed meeting, read
[references/action-routing.md](references/action-routing.md),
[references/applying-approved-actions.md](references/applying-approved-actions.md),
and [assets/review-bundle.md](assets/review-bundle.md). Use the asset for every
meeting proposal and use both references for routing, approval, and later
application.

For every newly proposed meeting, prepare one review section containing:

- the source name, stable native ID, and source link for identity checking;
- the actual meeting start time and a normalized proposed title;
- the proposed filename using the actual start timestamp plus the title;
- a preview shaped by the configured live meeting template; and
- any material ambiguity or evidence limitation the user must resolve; and
- only the supported, independently approvable actions defined by the review
  bundle and action-routing reference.

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

## Route and bind proposed actions

Resolve an existing equivalent and one canonical owner for each proposed
outcome. Work for the configured Linear-owned product stays in Linear, other
repository work stays in that repository's GitHub issues, and personal,
relationship, administrative, or cross-system commitments use the configured
Obsidian Tasks source. Do not duplicate Linear or GitHub work into Obsidian
unless the user has a distinct personal commitment.

Keep other people's nonblocking promises in the meeting note. Propose one
`waiting-for` task only when the user has a meaningful dependency and a real
follow-up date. Change durable context only when the meeting materially changes
its canonical record. Propose a calendar block only for ready work that
benefits from reserved human attention. Communication remains editable draft
text; sending is a separate reviewed effect.

Number actions continuously across the visible bundle and include the acting
identity, exact destination and target, visibility when relevant, complete
content or effect, evidence and reason, and explicit dependencies. Omit empty
categories. A vague approval authorizes no write.

Completion: every proposed action is complete enough to approve independently,
has one authoritative destination, and exposes every prerequisite.

## Apply only exact approvals

On a later user response, follow
[references/applying-approved-actions.md](references/applying-approved-actions.md)
before writing. Map approval to exact visible action numbers. Re-read each
target and check for an equivalent effect immediately before application.
Invalidate only actions whose identity, target, content, visibility, or
prerequisites drifted.

Apply supported approved actions once in dependency order and read every
attempted effect back. A failed or indeterminate prerequisite skips its
dependents while unrelated approved actions may continue. Preserve successful
canonical artifacts when a dependent backlink fails; report the partial result
and propose repair without rollback or blind retry.

Report each action as **Applied**, **Already satisfied**, **Failed**,
**Indeterminate**, **Manual**, **Deferred**, or **Skipped**. Available canonical
task or issue workflows may assist with their native contracts, but are never
required dependencies of this skill.

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
