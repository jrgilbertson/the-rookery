# Wind-down

Use this mode to close one local day through the user's canonical daily journal
and authoritative sources, leave tomorrow ready, and deliver light coaching.
Scheduled and manual wind-down follow the same workflow. This is the sole daily
chief-of-staff path. Apply [Make every intention verifiable](review-reasoning.md#make-every-intention-verifiable)
whenever a plan, commitment, coaching intervention, or durable proposal first
appears.

## Contents

- [Establish the day](#establish-the-day)
- [Daily CRM Scan](#daily-crm-scan)
- [Begin with one broad reflection](#begin-with-one-broad-reflection)
- [Phase 1: Run the Administrative Sweep](#phase-1-run-the-administrative-sweep)
- [Phase 1: Review, apply, and read back](#phase-1-review-apply-and-read-back)

Wind-down runs in two visible phases. This file owns Phase 1: establishing the
day, running the Daily CRM Scan, gathering broad reflection, and presenting and
resolving every non-journal correction the day's evidence supports. Phase 2
plans tomorrow, coaches, records next-day commitments, and drafts the journal
from the state Phase 1 left behind; load it through `SKILL.md` only after Phase
1 resolves.

Once Phase 1 has proposed its bundle, resolve it before opening sources for
Phase 2. The only discovery exception is recomputing a bundle resumed on a
later local day under [the resume rule](source-access.md#end-and-resume-honestly).
Per-action revalidation and readback still run. Early Phase 2 reads would
return the state Phase 1 was about to correct.

## Establish the day

Resolve the local date and review window. If the run time or the user's wording
makes the day being closed ambiguous, as can happen just after midnight,
resolve the intended journal date before querying the bounded day slice or
drafting. For a new review, complete
[the review baseline](review-reasoning.md#retrieve-the-review-baseline) before the
first recommendation. Treat the following local date as the commitment target
day. Read the configured daily-journal template and the closing-date journal,
if one exists, through each binding's native interface under
[source bindings](source-bindings.md#resolve-before-recommending). Read the
existing journal before drafting so manual content, frontmatter, links, embeds,
and unresolved thoughts remain intact.

If a missing journal could supply useful context, offer at most one interactive
catch-up and continue today's close by default. Never reconstruct a backlog
or treat a missing journal as evidence that nothing happened.

Beyond the baseline, expand into meetings, project state, or capacity when
the day or a proposed choice needs them. Query each relevant visible personal
and work calendar separately and retain its identity. Keep observed evidence,
inference, and subjective meaning distinct.

When the relationship companion is available, route messaging sources,
relationship mailboxes, and public X through the Daily CRM Scan below. Finish
it before the initial reconstruction even when no other evidence names a person.

Completion: the review window, existing journal state, and material non-CRM
evidence gaps are known without writing anything, with at most one optional
catch-up; then Daily CRM Scan when the companion is available.

## Daily CRM Scan

Run this step when the companion is available. It is required relationship
coverage for wind-down, separate from prepare-tomorrow's cadence exceptions in
Phase 2. Because this scan is caller-required, cover each configured
relationship interaction source for the window first even when no other
evidence names a person, then keep per-conversation history and identity
binding narrow; catch-up breadth stays catch-up-only.

1. **Window.** Closing local day plus up to two immediately preceding days
   whose daily journals are missing. A longer lapse still adds only those two
   days. Deeper history requires a later user request; create no close ledger
   or CRM catch-up workflow.
2. **Sources.** Require the companion to cover each configured relationship
   interaction source for that window: configured messaging sources (the
   companion loads its own messaging adapter before any messaging query), each
   authorized mailbox within its identity boundary, and public X under the
   companion's source contract when available (the companion loads its X
   adapter before any X query). Calendar visibility is not mailbox coverage.
   Unavailable sources are Partial for dependent conclusions only. Keep
   messaging and X adapters owned by the companion; do not invoke companion
   messaging tools directly outside the companion path.
3. **Evaluate.** Use embedded companion mode. Attribute messages by sender
   handle. Evaluate substantive direct contact (including targeted group
   participation and unanswered outgoing directed attempts) for each bindable
   person under the companion relationship contract. Ambient activity,
   reactions, and broadcasts stay out of scope, and unknown handles stay
   unresolved. Also evaluate substantive direct contacts already named by
   non-scan day evidence (calendar, meetings, journal-observed interactions).
   One group may produce effects for some people and none for others.
4. **Bundle.** Zero effects is valid. Novel contact-date, Person prose, Task,
   and communication effects are separate actions in the Phase 1 bundle. The
   contact-date, Person, and communication effects are that bundle's CRM and
   communication sweep rows, so one record still gets one action. Report
   Already satisfied in coverage when the canonical date is equal or newer.
   Keep one Person write per record and keep raw history in the source. Do not
   emit a nested CRM bundle, and write nothing while preparing.

Completion: the companion has returned completed relationship judgment before
initial reconstruction; scan window set; each configured relationship source
for the window covered or marked Partial; every bindable substantive direct
contact from the scan or other day evidence has a contact-date outcome (novel
action, Already satisfied in coverage, or identity/time unresolved); unknown
handles unresolved; no write performed and no nested CRM bundle emitted.

## Begin with one broad reflection

Present a short evidence-based reconstruction that includes Daily CRM Scan
findings when the companion ran, then ask one broad invitation such as: "What
stands out about today, including anything the sources would miss?" Wait for
the user's free-form response before targeted follow-ups. Do not open with a
template questionnaire.

Use follow-ups only for material gaps or template completion. The user may
leave any subjective field blank, mark it uncertain, correct the synthesis, or
keep their wording.

If reflection names a substantive direct interaction the scan and other day
evidence missed, evaluate it through the companion with the same rules.

Completion: the user's free-form account of the day is in hand before Phase 1
composes the sweep and before any round is asked, and any reflection-only
contacts have been evaluated.

## Phase 1: Run the Administrative Sweep

Run [Administrative Sweep](administrative-sweep.md) for the closing day and
following target day. It owns row membership, resolutions, and unavailable-task
behavior. Corrections remain separate actions; due-tomorrow context feeds the
plan unless that plan cannot hold it. The journal belongs only to Phase 2.

For one active sequential critical path, a precise restart cue may be useful.
Capture only the next concrete operation and keep it with the canonical task or
approved next-day plan. Do not add restart metadata to every task.

Completion: the sweep has run over the closing day and the target day, and
every row it proposes is one the user can approve, edit, defer, or skip on its
own.

## Phase 1: Review, apply, and read back

Present the sweep as the Phase 1 [review bundle](review-reasoning.md#prepare-one-review-bundle)
and wait for decisions. Use the shared [application rules](action-application.md#revalidate-apply-and-read-back)
for each approved action and its outcome. Apply independently approved rows
even when another row is blocked or undecided. Ask for a decision on undecided
rows before Phase 2; silence is not deferral. A blocked action with a reported
outcome does not block Phase 2.

A zero-row sweep needs only a brief report before continuing directly into
Phase 2. A scheduled run with the user absent instead ends **Paused**, even
with zero rows, and applies nothing.

When the user replies, apply [the resume rule](source-access.md#end-and-resume-honestly)
before applying actions, then continue into Phase 2 without a new review
request (loading Phase 2 via `SKILL.md`). On a later-day resume, use the
current local day for the sweep and its following day as the planning target.
Keep the journal's original closing date.

Completion: every Phase 1 row is explicitly deferred or skipped by the user,
or has an approved action with a reported outcome. Name unapplied and
unconfirmed actions separately. Phase 2 begins from the re-read state.
