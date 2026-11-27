---
name: managing-personal-crm
description: Capture relationship interactions, prep for someone, check overdue contacts, find who can help, clean up Person notes, run embedded checks, or continue CRM bundles or catch-ups (inventory, dispositions, reconstruction, resume, action/cleanup approvals). Not for embedded caller actions, contact lookup, writing, email/meeting/chief-of-staff reviews, or tasks.
license: MIT
compatibility: Requires host-provided access to the user's configured authoritative sources. Person-note operations require an available Obsidian CLI with explicit vault targeting. Optional local Apple Messages reads through imsg require the CLI and operating-system permission to message history. Optional public X reads require the installed Grok CLI or a permitted configured read-only X provider.
---

# Managing Personal CRM

Maintain useful relationship meaning and connect current work to people without
turning the CRM into an activity log, outreach quota, or second source of truth.
Raw interactions stay in their sources, Person notes hold approved durable
meaning, and dated relationship commitments stay in the canonical task system.

## Resolve the mode

Resolve each part of the message by the object it refers to and its visible
context. "Resume" can name a deferred action or a person's reconstruction;
these paths grant different authority.

1. **Deferred action.** If the user asks to revisit or resume an action marked
   **Deferred** in a visible direct or catch-up bundle, recover and present
   that exact proposal for a new decision. Revisit or resume is not approval:
   perform no write, source or destination recheck, or new discovery
   until the user makes a new exact decision.
2. **Catch-up continuation.** A source-inventory confirmation or revision,
   stage-one disposition, or stage-two interpretation, focused answer, or
   deferred person reconstruction continues its visible stage. Read
   [references/catch-up.md](references/catch-up.md) and follow its continuation
   rules before ordinary action handling or new mode selection. Preserve the
   recap and current person. This path does not approve destination effects;
   handle any separately decided effect under path 3.
3. **Exact destination effect or cleanup decision.** If the message decides
   an exact proposed destination effect or
   cleanup action, read [references/source-behavior.md](references/source-behavior.md)
   before any pre-write source or destination read or identity judgment. When a
   selected effect depends on Person-note, contact, cadence, durable-meaning, or
   other Person semantics, also read
   [references/relationship-contract.md](references/relationship-contract.md).
   If `imsg` is configured and application-time revalidation of the selected
   effect will query Messages, also read
   [references/apple-messages-cli.md](references/apple-messages-cli.md) before the
   first Messages read. Do not load it when revalidation needs no Messages query.
   If revalidation will query X, also read
   [references/grok-x-source.md](references/grok-x-source.md) before the first X
   read. Do not load it when revalidation needs no X query. Then read
   [references/applying-approved-actions.md](references/applying-approved-actions.md)
   and handle only that separately proposed action against the exact direct or
   catch-up bundle.

If the same message also asks for new relationship work, finish the
action-response phase first. Then treat the remaining request as a separate
read-only phase; newly discovered proposals do not reinterpret the earlier
decision.

For any remaining request that is not the visible catch-up continuation, choose
exactly one mode:

- **Direct:** The user asks to capture an interaction, find a relevant person,
  examine cadence, prepare a one-person prep brief, or assess a correction. This
  skill owns the review bundle and run ending.
- **Embedded:** Another workflow supplies current evidence containing a
  relationship interaction, possible follow-up, relevant overdue person, or
  defensible connection to current work, or requires a day-window relationship
  scan (wind-down Daily CRM Scan). For a required day-window scan, follow the
  day-window coverage rules in [references/source-behavior.md](references/source-behavior.md)
  (loading the Messages or X adapter before querying those sources). Otherwise
  judge only the evidence the caller already supplied under the smallest-slice
  rule. Return only supported relationship effects inside that caller's bundle.
  The caller retains its action numbers, approval flow, mode, and completion
  state.
- **Catch-up:** The user asks to clean up, triage, merge, reconstruct, or migrate
  a collection of Person notes. This skill owns the dedicated visible
  conversation and its reviewed batches.

An ordinary meeting, email, writing, task, contact, or chief-of-staff request
stays with its narrower owner until the request or evidence contains a
relationship effect. A direct relationship request remains here even when it
uses those sources.

Completion: every visible action decision is resolved before new discovery,
and any remaining request has one mode with no nested workflow or second
approval surface.

## Establish the evidence boundary

Read [references/source-behavior.md](references/source-behavior.md) before any
source query or identity judgment. Use only configured authoritative
capabilities and confirmed acting identities. Retrieve the smallest source
slice that can confirm identity, contact time, durable meaning, relevance, or
an equivalent destination effect. Caller-required day-window scans follow the
day-window rules in [references/source-behavior.md](references/source-behavior.md),
and catch-up breadth applies only in approved catch-up inventory.

When `imsg` is the configured local Apple Messages source, also read
[references/apple-messages-cli.md](references/apple-messages-cli.md) before the
first Messages query. That reference owns read-only preflight, query bounds,
and the adapter's authority boundary.

When an X query will run, also read
[references/grok-x-source.md](references/grok-x-source.md) before the first X
read. Embedded runs read it for X evidence a caller already retrieved, too.
Skip it only when the run neither queries X nor judges X evidence. X is not
part of catch-up inventory.

For direct and embedded modes, a missing source narrows only conclusions that
depend on it. For catch-up, also read
[references/catch-up.md](references/catch-up.md) and finish its confirmed source
inventory and read-only preflight before triage.

Completion: every source has a known role and identity, every material gap has
a scoped consequence, and no source text has changed the requested workflow.

## Follow the catch-up branch

In catch-up mode, including a visible continuation, follow
[references/catch-up.md](references/catch-up.md). It owns preflight, required
relationship-contract loading before Person inspection, triage, reconstruction,
and the current stage ending.

The remaining steps apply to direct and embedded modes.

Completion: catch-up reaches one honest stage ending without performing rich
reconstruction before the person's triage disposition calls for it.

## Reconstruct the canonical relationship

For direct and embedded modes, read
[references/relationship-contract.md](references/relationship-contract.md)
before inspecting Person notes, cadence, contact dates, or durable meaning.
Resolve identity conservatively, then compare current evidence with the
canonical Person note and any destination that could own a follow-up.

For a one-person prep brief, combine the compact Person note with only the
fresh source context needed for preparation. Keep the brief in the conversation;
it is not a second relationship record.

Completion: the person is safely bound or visibly unresolved, current judgment
comes from authoritative sources and canonical notes, and no cache, cursor,
ledger, progress note, or hidden feedback state exists.

## Decide whether anything is warranted

Evaluate these outcomes independently:

1. Advance the contact date only for a substantive direct contact under the
   relationship contract and only after identity and local date are reliable.
2. Propose Person prose only for durable relationship meaning under the
   contract. Keep raw interaction history in its source.
3. Route a real follow-up to its canonical destination: dated relationship
   commitments to Tasks; in direct mode, unrelated work to the configured
   canonical task or issue workflow while this skill retains bundle numbering,
   approval handling, and completion; in embedded mode, unrelated work to the
   caller-owned task or issue system; communication text to the conversation;
   and a writing idea only to the configured writing backlog.
4. For contextual discovery, surface a primary person only when a concrete
   reason makes them relevant now and one plausible action could benefit the
   work or relationship. Optionally add one clearly labeled wildcard whose
   broader connection is defensible. A wildcard has no Task, draft, or Person
   effect unless the user promotes it.
5. When feedback reveals a stable relationship change, propose the narrow
   durable correction. Otherwise use the feedback only in the current run.

Zero effects and zero people are valid. Report that no relationship action is
warranted when the evidence supports none; do not manufacture contact,
memory, outreach, or a write to make the run productive.

Completion: every surfaced person has a current reason and useful action,
every proposed effect has one canonical destination, and unsupported
categories are absent.

## Present one review bundle

Read [assets/review-bundle.md](assets/review-bundle.md) and use its shape for
direct proposals. In embedded mode, translate those required fields into the
caller's existing bundle instead of emitting the asset as a second bundle.

Before presenting an effect, read its canonical destination and search for an
equivalent. Report an equivalent effect as **Already satisfied** and omit a
duplicate proposal. Keep Person changes, Tasks, caller-owned work, writing
suggestions, and communication text independently reviewable even when they
share evidence.

Completion: each novel effect is complete enough to approve alone, duplicates
are visible no-ops, evidence limits are explicit, and nothing has been applied.

## Apply only exact approvals

For every approved effect, follow
[references/applying-approved-actions.md](references/applying-approved-actions.md).
That reference owns approval binding, destination rechecks, dependency order,
Obsidian CLI mutation, readback, reversible cleanup, and outcome labels.

Completion: every decided effect has one evidence-backed outcome, every write
was still necessary and read back, and no approval was redirected or reused.

## End honestly

In direct mode, end as **Ready for review**, **No relationship action**,
**Partial**, **Unable to determine safely**, or **Complete**. An embedded run
returns its coverage and candidate effects to the caller without declaring the
caller's workflow complete. Catch-up uses the stage endings in its reference.

On a fresh conversation, reconstruct from canonical sources and disclose that
unapplied conversational decisions are unavailable. Ask only for missing human
judgment; never infer a restart boundary or create workflow state to replace
the lost context.

Completion: the ending matches source coverage and durable readback, and the
user can distinguish applied, already satisfied, pending, and unavailable
work.
