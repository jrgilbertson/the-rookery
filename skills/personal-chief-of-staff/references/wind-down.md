# Wind-down

Use this mode to close one local day through the user's canonical daily journal
and authoritative sources, leave tomorrow ready, and deliver light coaching.
Scheduled and manual wind-down follow the same workflow. This is the sole daily
chief-of-staff path.

## Contents

- [Establish the day](#establish-the-day)
- [Daily CRM Scan](#daily-crm-scan)
- [Begin with one broad reflection](#begin-with-one-broad-reflection)
- [Phase 1: Run the Administrative Sweep](#phase-1-run-the-administrative-sweep)
- [Phase 1: Review, apply, and read back](#phase-1-review-apply-and-read-back)
- [Phase 2: Prepare tomorrow](#phase-2-prepare-tomorrow)
- [Phase 2: Ask on the evidence frontier](#phase-2-ask-on-the-evidence-frontier)
- [Phase 2: Coach](#phase-2-coach)
- [Phase 2: Record tomorrow's meaningful commitments](#phase-2-record-tomorrows-meaningful-commitments)
- [Phase 2: Complete the existing journal together](#phase-2-complete-the-existing-journal-together)
- [Phase 2: Promote only durable signal](#phase-2-promote-only-durable-signal)
- [Phase 2: Review, write, and verify](#phase-2-review-write-and-verify)

Wind-down runs in two visible phases. Phase 1 presents and resolves every
non-journal correction the day's evidence supports. Phase 2 plans tomorrow,
coaches, records meaningful commitments, and drafts the journal from the state
Phase 1 left behind.

Once Phase 1 has proposed its bundle, open no further source until every
approved action is applied and read back or classified as unapplied. This binds
the first move of a resumed or continued run: when the reconstruction and
reflection already happened, the next act is resolving Phase 1. A source opened
early returns the state Phase 1 was about to correct, and every later judgment
inherits it.

## Establish the day

Resolve the local date and review window. If the run time or the user's wording
makes the day being closed ambiguous, as can happen just after midnight,
resolve the intended journal date before drafting. Treat the following local
date as the commitment target day. Through the Obsidian CLI, find the configured
daily-journal template and the closing-date journal, if one exists. Read the
existing journal before drafting so manual content, frontmatter, links, embeds,
and unresolved thoughts remain intact.

When a prior daily journal that would help is missing, mention it without
judgment and offer an interactive catch-up only if it could recover useful
context. Continue with today's close by default. After one or several missed
days, offer at most one catch-up and never create a backlog of journals to
reconstruct. Do not treat a missing journal as proof that nothing happened.

Query only sources that can clarify what happened or what changed: meetings,
active tasks, project or repository state, available capacity evidence, the
canonical strategy note, and relevant canonical learning notes. When the
companion is available, do **not** treat relationship interaction sources
(Messages, relationship mailboxes, X) as this generic pass. Route them through
the **Daily CRM Scan** below. Query each visible personal and work calendar
separately for the day and retain its calendar identity in the evidence.
Calendar visibility supplies no work-email coverage. Separate:

- observed outcomes, events, decisions, commitments, and source changes;
- reasonable inferences that still need confirmation; and
- subjective meaning that cannot be observed.

When the companion relationship capability is available, finish the **Daily CRM
Scan** below before the initial reconstruction. Calendar, mailbox, or
reflection naming a person is not a prerequisite for that scan.

Completion: the review window, existing journal state, and material non-CRM
evidence gaps are known without writing anything, with at most one optional
catch-up; then Daily CRM Scan when the companion is available.

## Daily CRM Scan

Run this step when the companion is available. It is required relationship
coverage for wind-down, separate from prepare-tomorrow's cadence exceptions.

1. **Window.** Default: closing local day only. Short miss: if the prior one
   local daily journal is missing, window = that day ∪ closing day; if the
   prior two are missing, window = those two ∪ closing day; if more than two
   prior journals are missing, still expand only the two local days immediately
   before the closing day (plus closing day). Exhaustive history, CRM catch-up
   mode, and a close ledger are out of scope. Deeper history only if the user
   asks later.
2. **Sources.** Require the companion to cover each configured relationship
   interaction source for that window: Apple Messages when `imsg` is configured
   (companion loads its Messages adapter before any Messages query), each
   authorized mailbox within its identity boundary, authenticated X under its
   current source contract when available. Calendar visibility is not mailbox
   coverage. Unavailable sources are Partial for dependent conclusions only. Do
   not invoke `imsg` as CoS-owned tooling outside the companion path.
3. **Evaluate.** Use embedded companion mode. Attribute messages by sender
   handle. Evaluate substantive direct contact (including targeted group
   participation and unanswered outgoing directed attempts) for each bindable
   person under the companion relationship contract. Ambient activity,
   reactions, and broadcasts stay out of scope, and unknown handles stay
   unresolved. Also evaluate substantive direct contacts already named by
   non-scan day evidence (calendar, meetings, journal-observed interactions). One group may produce
   effects for some people and none for others.
4. **Bundle.** Zero effects is valid. Novel contact-date, Person prose, Task,
   and communication effects are separate actions in the Phase 1 bundle. The
   contact-date, Person, and communication effects are that bundle's CRM and
   communication sweep rows, so one record still gets one action. Report
   Already satisfied in coverage when the canonical date is equal or newer.
   Keep one Person write per record and keep raw history in the source. Write
   nothing while preparing.

Completion: scan window set; each configured relationship source for the window
covered or marked Partial; every bindable substantive direct contact from the
scan, other day evidence, or (later) reflection has a contact-date outcome
(novel action, Already satisfied in coverage, or identity/time unresolved);
unknown handles unresolved; no write performed.

## Begin with one broad reflection

Present a short evidence-based reconstruction that includes Daily CRM Scan
findings when the companion ran, then ask one broad invitation such as: “What
stands out about today, including anything the sources would miss?” Wait for
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

Read [references/administrative-sweep.md](administrative-sweep.md) and run the
sweep it describes. The Wind-down window is the closing day and the target day.
That file owns sweep membership, the task rows, the resolutions each row
proposes, and the degraded behavior when the canonical task workflow is
unavailable.

Do not hide a sweep correction inside the journal or create a second task list.
A sweep row that proposes a resolution stays independently approvable. A
due-tomorrow row is context that feeds the next-day plan, and it becomes its own
action only when that plan cannot hold it. The journal is a Phase 2 action
rather than a member of this sweep.

For one active sequential critical path, a precise restart cue may be useful.
Capture only the next concrete operation and keep it with the canonical task or
approved next-day plan. Do not add restart metadata to every task.

Completion: the sweep has run over the closing day and the target day, and
every row it proposes is one the user can approve, edit, defer, or skip on its
own.

## Phase 1: Review, apply, and read back

Present the sweep as the Phase 1 review bundle under "Prepare one review
bundle" in `references/source-behavior.md`, then wait for the user's decisions.
Apply each approved action under "Revalidate, apply, and read back" in that
same reference, classify each outcome there, and name every action the user
edited, deferred, or skipped. An outcome that blocks its own action under
"Revalidate, apply, and read back" blocks only that action; the rest of Phase 1
and all of Phase 2 continue.

A scheduled run with the user absent stops here and ends **Paused** with
nothing applied, as that reference's scheduled-run rule requires. It composes
the bundle from canonical role reads only. Do not touch a proposed target's own
write interface while waiting, not even to re-read it; that re-read belongs to
the approved action and happens after the user replies. When the user
replies later, apply the resume rule in "End and resume honestly" before any
action applies, then continue into Phase 2. Wind-down's journal keeps the
closing date it originally had; only the sweep window and the target day
re-resolve.

A zero-row sweep needs no bundle ceremony. Say the sweep found nothing and
continue. On a scheduled run with the user absent the stop above still wins,
because Phase 2 cannot plan, coach, or draft without the user's reflection and
decisions. Report the empty sweep and end **Paused**.

Completion: every approved Phase 1 action has a readback-backed outcome or an
indeterminate stop, every unapplied action is named, and Phase 2 begins from
the re-read state rather than from the pre-sweep evidence.

## Phase 2: Prepare tomorrow

Phase 2 opens the sources it needs only after every approved Phase 1 action has
been applied and read back, or classified as unapplied. The boundary rule at the
top of this file governs, including the case where orienting is the temptation.

Establishing the day and the Daily CRM Scan run before Phase 1 and keep their
own reads. Those reads happen once, at the top of the run. Establishing the day
opens the journal to learn whether it exists and what manual content it holds,
not to supply values for drafting. A run that resumes or continues after the
reflection has already established the day, so it does not repeat those reads
to orient; it resolves Phase 1 first. The journal's own target is re-read again
immediately before its write, under "Revalidate, apply, and read back" in
`references/source-behavior.md`.

Plan from the state Phase 1 left behind, not from the pre-sweep evidence, and
re-read a source rather than reusing a value an approved action changed. A
due-tomorrow row the sweep surfaced enters this plan instead of becoming its
own action.

Read each visible personal and work calendar separately for the next day,
retaining its calendar identity, along with relevant active tasks, strategy,
and learnings. Use the actual day's outcomes, unresolved commitments, known
capacity, and current constraints to propose a realistic plan. Distinguish
fixed commitments from flexible blocks using their context rather than
assuming either.

Name the critical path and the few protected outcomes when useful. Calendar
edits, task changes, and communications remain separate review actions. Size
the plan to the free capacity tomorrow's calendars show.

Express each proposed outcome or priority through the shared intention
contract: connect its current authoritative basis or labeled user premise to
the outcome the user owns or approves, or to an agent-proposed outcome clearly
awaiting approval, and the future observable evidence that would close it.
Keep this natural and compact rather than turning tomorrow's plan into a
repeated form.

### Tomorrow judgment items

Choose no more than three **tomorrow** judgment items. An item earns attention
only when the user's judgment or presence could materially improve a decision,
commitment, risk, opportunity, relationship, or outcome **next day**. Apply the
shared judgment factors without turning them into a score.

For each item:

- state the answer or concern first;
- explain why it matters for tomorrow;
- point to current authoritative evidence;
- distinguish fact, inference, and uncertainty; and
- name the decision, preparation, or action that needs the user.

Zero judgment items is valid. Include an item only when tomorrow's outcome
changes if the user attends to it, and frame each around tomorrow's decision.

### Validate tomorrow's time-blocked day

Compare tomorrow's calendars with the proposed plan, active tasks, strategy,
relevant learnings, and realistic capacity. Interpret each event through its
purpose, participants, flexibility, and surrounding commitments.

Surface only consequential calendar issues, such as:

- one meeting that needs preparation or relationship context;
- a fixed commitment that conflicts with the critical path;
- a flexible block that no longer serves tomorrow's most important outcome;
- a stale waiting or blocked commitment that now needs a decision; or
- a restart cue whose canonical task is still active and important.

Meaningful commitments do not require calendar blocks to be created, renamed,
or mapped to them. Generate a preparation capsule only for a meeting whose outcome depends on it.
Calendar edits remain separate proposed actions. Preserve commitments
established as fixed. Resolve conflicts only through separately approvable
changes to events or blocks whose flexibility is established; if flexibility
is unknown, ask before proposing an edit.

### Relationship exceptions for tomorrow

When the companion relationship capability is available, inspect active
relationships whose derived cadence may be overdue and search current work,
writing, reading, decisions, and meetings for a defensible person connection
useful **tomorrow**. This is a bounded exception check, not a general CRM
review or catch-up, and is separate from the Daily CRM Scan above.

An overdue person earns attention only when the current evidence explains why
contact could be useful soon and suggests a plausible action. A strong
contextual connection may surface regardless of routine cadence when the
reason is specific. Keep any optional broader connection clearly separate and
do not create an action for it unless the user promotes it.

Return no relationship item when the evidence supports none. If a relationship
item belongs among tomorrow judgment items, count it within the zero-to-three
limit and route any proposed effect through the shared bundle. When the
companion is unavailable, omit the relationship conclusion and mention reduced
coverage only when material.

Completion: the next-day proposal reflects the sources as Phase 1 left them,
makes its tradeoffs visible without writing to them, and contains zero to three
defensible tomorrow judgment items with no filler.

## Phase 2: Ask on the evidence frontier

Ask the round described in "Ask on the evidence frontier" in
`references/source-behavior.md`. That contract owns the entry bar, the numbered
plain-chat format and its cap, the ordering, and how a reply is read. The
broad reflection above always comes first and is never replaced by a round.

Ask only what the next-day plan, the coaching judgment, or tomorrow's
commitments would actually turn on. A round with zero questions is valid. An
answer that changes the next-day plan produces a revised plan before coaching.

Completion: every question asked could have changed the plan, the coaching
judgment, or a commitment, and an unanswered question stayed open rather than
being resolved by assumption.

## Phase 2: Coach

After evidence, user reflection, and prepare-tomorrow inputs are available—and
**before** Meaningful Commitments are finalized—deliver one short coaching
judgment. Test whether one relevant rule from the configured strategy or
learning roles, or one supported current hypothesis, should change tomorrow's
actual choice. Apply at most one; do not force a rule or hypothesis merely to
produce coaching.

Use the shared longitudinal-evidence contract. Distinguish a one-day state or
hypothesis from evidence of recurrence, and inspect material counterevidence
or an alternate explanation in the bounded Wind-down look-back. Keep the dated
observations, the agent's inference, material uncertainty, and the user's
subjective judgment distinct. Do not supply the user's judgment; ask them to
confirm or correct the evidence and interpretation.

When the evidence supports an intervention, give it the shape required by
"Ground longitudinal coaching in durable evidence" in
`references/source-behavior.md`, tied to tomorrow's actual choice of plan,
commitment, or boundary. An evidence-backed recommendation to keep the current
plan qualifies when it resolves the live choice; generic task restatement does
not. Focus, stop, more, and less may be useful lenses, but they are not
required slots. Deliver the beat as one observation, one inference, and one recommendation.

Apply the shared intention contract whether the recommendation changes the
plan or deliberately preserves it. An honest no-material-intervention result
is not an intention.

When no material intervention is supported, say so concisely and continue to
Meaningful Commitments without filler advice or a strategy or learning
proposal. Coaching itself authorizes nothing: a revised commitment, its exact
text and rationale, any journal effect, and any strategy or learning effect
remain proposed until approved through their existing separate actions.

Completion: before commitments lock, the user has received either one
evidence-grounded recommendation tied to tomorrow's actual choice or a concise
no-material-intervention result, with an invitation to correct the judgment.

## Phase 2: Record tomorrow's meaningful commitments

When the live daily-journal template contains a `Tomorrow’s Meaningful
Commitments` section, use it as the configured place for reviewed next-day
intent. Draft three to five numbered plain-Markdown bullets in the closing-date
journal.
Each bullet uses one to three sentences that naturally combine a concrete
user-supplied or approved outcome (or a conditional candidate awaiting
approval), its current authoritative basis or labeled user premise, an
observable future finish line, and one short user-approved reason tied to
strategy, an obligation, or an avoided cost. Do not require literal intention
labels or a repeated three-bullet form. Collaborate to refine an activity label
such as “development,” “meetings,” or “work on X” into a concrete outcome by
default.
If the user explicitly approves broad or incomplete wording unchanged, preserve
it verbatim, identify the missing element, and treat it as nonconforming source
content rather than claiming it satisfies the three-element condition.

Use the day's outcomes, unresolved work, next-day capacity, fixed commitments,
active tasks, current strategy, the coaching beat, and the user's judgment to
draft the list. Apply material conflict, invalid-premise, and capacity quality
gates against next-day evidence: when evidence invalidates a draft bullet, show
the intended commitment, the evidence, and the recommendation; leave unaffected
bullets unchanged. Every bullet's outcome, finish line, and rationale
traces to the user's words or an approved draft. A commitment names an
outcome; a calendar block names time. Do not
create a separate morning reaffirm step.

The user supplies or explicitly approves every rationale. Write each commitment as a plain-Markdown bullet.

The commitments express reviewed intent. They do not replace canonical task
state or calendar capacity, and they do not require calendar blocks to be
created, renamed, or mapped to individual commitments. Keep the journal action
separate from every task, calendar, communication, CRM, or repository action.

When the configured section exists in the live template but the closing-date
journal lacks it, propose a narrow insertion that preserves all manual content,
frontmatter, links, embeds, and views. When the journal already contains the
section, report **Already satisfied** if its bullets exactly match the approved
content. Otherwise show an exact section-only merge or replacement, including
which existing text is retained or removed; preserve unrelated journal
structure and never discard a user edit without explicit approval. Revalidate
the section immediately before writing. When the live template lacks the
section, keep the ordinary next-day proposal above and do not invent or write a
new journal structure without separate approval. If user-authored commitment
content is incomplete and has not been explicitly approved unchanged, surface
the missing element and collaborate rather than padding, truncating, or
inventing subjective content.

Completion: when the configured section exists, the proposed journal contains
three to five reviewed bullets with quality gates applied. Bullets that satisfy
the three-element condition are recorded as conforming intent; any bullet the
user explicitly approved incomplete is preserved verbatim, labeled
nonconforming in the proposal, and is not claimed as a complete three-element
commitment. When the section is absent, ordinary next-day planning continues
without an invented journal write.

## Phase 2: Complete the existing journal together

Draft from the state Phase 1 left behind. A task, calendar, CRM, or repository
fact the journal reports comes from the re-read result of an applied action.
An action carrying any other outcome under "Revalidate, apply, and read back" in
`references/source-behavior.md` is described as it actually stands, and an
outcome that section leaves unknown is described as unconfirmed rather than as
applied or unapplied.

Follow the configured daily-journal template rather than inventing a recap
format. The agent may draft substantial objective material from verified
evidence and the user's free-form thoughts. The user supplies or explicitly
approves:

- what felt difficult and why;
- gratitude;
- meaning and causal interpretation;
- the key learning; and
- any other statement that claims an internal experience or personal judgment.

Treat optional pulse or rating fields as aids to noticing, not grades, streaks,
or required feedback. Keep objective evidence distinct from interpretation.
Prefer a few meaningful outcomes and frictions over a chronological activity
dump. Preserve the template's existing vault-activity views instead of copying
their contents into prose.

When the closing-date journal already contains manual writing, propose a narrow
merge that preserves it. Never replace the whole note with a cleaner
agent-authored version.

Completion: the proposed journal follows the live template, preserves existing
content, reflects the applied Phase 1 state, and clearly identifies every
subjective statement awaiting approval.

## Phase 2: Promote only durable signal

When a high-signal insight may help an audience, offer one writing seed without
creating a quota, draft, or publication action automatically. Keep central
thinking and the rough draft human-led unless the user asks for more help.

Propose a change to the canonical learning notes or the canonical strategy note
when the user explicitly requests it or when the day (including the coaching
beat) adds evidence to a repeated, behavior-changing pattern. By default, a
one-day observation stays in the daily journal. For a user-requested learning
or strategy update, propose a separately numbered action that labels the
observation as isolated and does not claim recurrence. A learning or strategy
update the day's dated evidence already supported belongs to the Phase 1 sweep
and was proposed there; one that arises from the Phase 2 coaching beat is a
separate action in the Phase 2 bundle. Never auto-write strategy or learnings;
the user must approve the exact durable update independently.

Apply the shared intention contract to each learning or strategy proposal. Do
not promote an inferred outcome to the user's intention.

Completion: optional writing, learning, and strategy proposals are selective,
sourced, and independently reviewable.

## Phase 2: Review, write, and verify

Present the Phase 2 review bundle. It carries the journal, any learning or
strategy action the coaching beat produced, the meaningful-commitments edit,
and any other Phase 2 effect.

A reply deciding the Phase 1 bundle resolves those actions and then continues
this run into Phase 2. It is not an action-only response and needs no separate
review request. A reply deciding this Phase 2 bundle ends the run.

A run that applied Phase 1 actions and then read Phase 2 sources renders one
Source Access Audit covering both, separating the **Action access** from the
**Review discovery** reads. Reporting only the pre-write reread and
post-write readback would describe this as an action-only response and leave
every source Phase 2 actually opened unnamed.

The bundle does not repeat a Phase 1 action, and its action numbers continue
from Phase 1 under "Prepare one review bundle" in
`references/source-behavior.md`. Apply only approved actions under the shared
source rules. Each action uses the bundle's intention shape; another action
cannot close it.

For an approved journal action, re-read the target through the Obsidian CLI.
Re-read the configured template as well when the action adds or changes the
meaningful-commitments section. Create from the current template or edit the
existing journal through the CLI with explicit configured-vault targeting.
Preserve manual content, frontmatter, links, embeds, and views, do not lint, and
read the result back through the CLI before reporting it as applied. If the
template or any content in the target journal changed after approval, present a
revised proposal instead of applying stale content.

End explicitly using the core run endings. A completed wind-down normally ends
in the reviewed daily journal plus any independently approved source changes,
not in a generated brief or internal run record. The closing recap names the
actions from both bundles, including every action that was edited, deferred,
skipped, or left unapplied in either phase.

Completion: the reviewed journal is visible in its canonical note, every other
action from both phases has an independent outcome, tomorrow's plan reflects
the final sources, and no unapproved or unverifiable change is reported as
complete.
