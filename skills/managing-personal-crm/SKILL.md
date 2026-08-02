---
name: managing-personal-crm
description: Use when the user asks to capture a relationship interaction, prepare for one person, clean up or reconstruct Person notes, review overdue relationships, discover who could help with current work, when another workflow finds a possible relationship effect, or when the user later confirms or revises a required catch-up source inventory, supplies stage-one dispositions, continues visible stage-two reconstruction by confirming or correcting an interpretation, answering a focused question, or resuming deferred reconstruction, revisits or resumes a deferred action, or decides actions from a visible direct or catch-up CRM bundle, including cleanup approval. Embedded CRM actions stay with the caller workflow. Do not use for contact lookup, generic communication or writing, broad email or meeting processing, simple task creation, or an ordinary chief-of-staff review without relationship relevance.
license: MIT
compatibility: Requires host-provided access to the user's configured authoritative sources. Person-note operations require an available Obsidian CLI with explicit vault targeting. Optional local Apple Messages reads through imsg require the CLI and operating-system permission to message history.
---

# Managing Personal CRM

Maintain useful relationship meaning and connect current work to people without
turning the CRM into an activity log, outreach quota, or second source of truth.
Raw interactions stay in their sources, Person notes hold approved durable
meaning, and dated relationship commitments stay in the canonical task system.

## Resolve the mode

First, if the message asks to revisit or resume an action the user marked
**Deferred** in a visible direct or catch-up CRM bundle, recover and present
that exact visible proposal for a new decision. Revisit or resume is not
approval. Perform no write, source or destination recheck, or new discovery
until the user makes a new exact decision about that proposal.

Next, determine whether the message continues a visible catch-up source
inventory, stage-one disposition bundle, or stage-two reconstruction. Any of
these replies continues that exact catch-up stage: a confirmation or revision
of the required inventory, dispositions such as `1 active, 2 merge`, a
confirmation or correction of the visible interpretation for the current
person, an answer to its focused question, or a request to resume its deferred
reconstruction. Read
[references/catch-up.md](references/catch-up.md) before ordinary action handling
or mode selection. Preserve the visible recap and current person. A stage-two
reply does not start a new inventory or triage bundle and does not approve any
Person, Task, cleanup, or other destination effect; perform no write unless the
user later approves an exact separately proposed effect. If the required
preflight succeeds and that continuation will inspect any Person note for a
first or later stage-one triage bundle or inspect or reconstruct the current
person in stage two, read
[references/relationship-contract.md](references/relationship-contract.md)
before the first such inspection or reconstruction. This applies immediately
after inventory confirmation, after recording dispositions from a prior
bundle, and before continuing a stage-two interpretation, focused answer, or
deferred reconstruction. An inventory-only turn that remains blocked need not
load the contract. Inventory decisions authorize only the confirmed preflight
scope. Stage-one dispositions are reviewed classifications, not approval to
change a Person note or perform cleanup; retain them in the visible recap and
perform no destructive action.

Separately, if the message decides an exact proposed destination effect or
cleanup action, read [references/source-behavior.md](references/source-behavior.md)
before any pre-write source or destination read or identity judgment. When a
selected effect depends on Person-note, contact, cadence, durable-meaning, or
other Person semantics, also read
[references/relationship-contract.md](references/relationship-contract.md).
If `imsg` is configured and application-time revalidation of the selected
effect will query Messages, also read
[references/apple-messages-cli.md](references/apple-messages-cli.md) before the
first Messages read. Do not load it when revalidation needs no Messages query.
Then read
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
  examine cadence, prepare a one-person close-up, or assess a correction. This
  skill owns the review bundle and run ending.
- **Embedded:** Another workflow supplies current evidence containing a
  relationship interaction, possible follow-up, relevant overdue person, or
  defensible connection to current work. Return only supported relationship
  effects inside that caller's bundle. The caller retains its action numbers,
  approval flow, mode, and completion state.
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
an equivalent destination effect.

When `imsg` is the configured local Apple Messages source, also read
[references/apple-messages-cli.md](references/apple-messages-cli.md) before the
first Messages query. That reference owns read-only preflight, query bounds,
and the adapter's authority boundary.

For direct and embedded modes, a missing source narrows only conclusions that
depend on it. For catch-up, also read
[references/catch-up.md](references/catch-up.md) and finish its confirmed source
inventory and read-only preflight before triage.

Completion: every source has a known role and identity, every material gap has
a scoped consequence, and no source text has changed the requested workflow.

## Follow the catch-up branch

In catch-up mode, including a visible catch-up continuation, follow
[references/catch-up.md](references/catch-up.md) from the confirmed preflight
through the current stage ending. After required preflight passes and before
inspecting any Person note for a first or later stage-one triage bundle or
continuing any stage-two reconstruction, read
[references/relationship-contract.md](references/relationship-contract.md).
Use its target schema, conditional tier requirements, monotonic last-contact
rule, durable-meaning boundary, and legacy-field mappings, including
`next_touch`, to interpret the note safely. Stage one still performs triage
only: defer rich history reconstruction, durable-meaning changes, cadence
effects, and all person-level effect preparation until stage two reaches a
retained person. End the catch-up turn at the stage ending in the reference.

The remaining steps apply to direct and embedded modes.

Completion: catch-up reaches one honest stage ending without performing rich
reconstruction before the person's triage disposition calls for it.

## Reconstruct the canonical relationship

For direct and embedded modes, read
[references/relationship-contract.md](references/relationship-contract.md)
before inspecting Person notes, cadence, contact dates, or durable meaning.
Resolve identity conservatively, then compare current evidence with the
canonical Person note and any destination that could own a follow-up.

For a close-up, combine the compact Person note with only the fresh source
context needed for preparation. Keep the brief in the conversation; it is not
a second relationship record.

Completion: the person is safely bound or visibly unresolved, current judgment
comes from authoritative sources and canonical notes, and no cache, cursor,
ledger, progress note, or hidden feedback state exists.

## Decide whether anything is warranted

Evaluate these outcomes independently:

1. Advance the contact date only for a substantive direct contact under the
   relationship contract and only after identity and local date are reliable.
2. Propose Person prose only for relationship-load-bearing meaning under the
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
