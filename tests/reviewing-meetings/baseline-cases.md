# Baseline test: reviewing-meetings

This is synthetic characterization evidence for a new instruction package. The
three without-skill outputs below were observed before authoring U1. The final
with-skill package was then exercised in three fresh contexts against the same
behavioral cases.

Baseline date: 2026-07-22 | Final run: 2026-07-23 | Harness: Codex desktop fresh-context agents | Model: session default

## Case 1: One new completed meeting

Prompt:

> Check the completed meeting from source `synthetic` with native ID
> `meeting-new-01` and prepare what
> should happen next. It ended on 2026-07-21, started at
> `2026-07-21T10:00:00-07:00`, has the title `Synthetic customer follow-up`,
> and has the source URL `https://example.invalid/meetings/meeting-new-01`.
> Its generated notes contain enough grounded context, discussion, decisions,
> and next steps for a meeting-note proposal and one follow-up, but the
> follow-up's owner and recipient are unclear. The configured live meeting
> template and naming convention are readable. The approved-note search returns
> zero exact source-and-ID matches, the intended filename is unoccupied, and
> this conversation contains no pending proposal or dismissal for the pair. Do
> not write anything yet.

Observed without-skill behavior:

- Correctly recognized the meeting as eligible and kept the response read-only.
- Proposed drafting the note and holding the follow-up until its owner and
  recipient were confirmed.
- Did not define the canonical source identity, exact disposition count,
  readback, or explicit run ending.

Expected with-skill behavior:

- Uses the stable ID and ended state to classify the meeting as **Newly
  proposed**.
- Refines a preview against the configured live meeting template while leaving
  owner and recipient unresolved.
- Keeps the result read-only and ends **Ready for review** with an exact
  disposition count.

Verdict: passed. The fresh with-skill run added the exact disposition, naming,
action boundary, ambiguity handling, disposition counts, and explicit ending
missing from the bare response.

## Case 2: Append only after an earlier proposal

Prompt:

> Earlier in this conversation you proposed Meeting A from source `synthetic`
> with native ID `meeting-pending-a`, and I have not reviewed it. A later completed Meeting B
> with ID `meeting-new-b` is now available. Meeting B ended on 2026-07-21,
> started at `2026-07-21T15:00:00-07:00`, has the title `Synthetic product
> review`, the source URL
> `https://example.invalid/meetings/meeting-new-b`, and generated notes with
> enough grounded context, discussion, decisions, and next steps. The configured
> live meeting template and naming convention are readable. Approved-note
> searches return zero exact source-and-ID matches for A and B, Meeting B's
> intended filename is unoccupied, and this conversation has no dismissal for
> either pair. Run the next post-meeting check.

Observed without-skill behavior:

- Correctly left Meeting A pending and unchanged and proposed Meeting B
  separately.
- Did not name the two exact dispositions, the append-only invariant, or an
  explicit run ending.

Expected with-skill behavior:

- Classifies Meeting A as **Already pending** from the retrievable exact
  source-and-ID proposal.
- Presents only Meeting B as **Newly proposed**, without repeating,
  recomputing, or renumbering Meeting A.
- May add one terse note that one earlier proposal remains pending.
- Ends **Ready for review** with one newly proposed and one already pending.

Verdict: passed. The fresh with-skill run appended only Meeting B, preserved
Meeting A and its numbering, returned both exact dispositions, and ended
explicitly.

## Case 3: Ambiguous transcript attribution

Prompt:

> The configured source's summary says Alex owns a consequential follow-up, but the only
> transcript labels are `Speaker` and `Microphone`. The completed meeting has
> the stable ID `meeting-attribution-01`, started at
> `2026-07-21T13:00:00-07:00`, has the title `Synthetic planning discussion`,
> and has the source URL
> `https://example.invalid/meetings/meeting-attribution-01`. Its generated notes
> contain enough grounded context, discussion, decisions, and next steps; only
> the owner attribution is ambiguous, and the relevant transcript turns are
> available for selective inspection. The configured live meeting template and
> naming convention are readable. The approved-note search returns zero exact
> source-and-ID matches, the intended filename is unoccupied, and this
> conversation contains no pending proposal or dismissal for the pair. Prepare
> a grounded meeting proposal and resolve only what the evidence supports.

Observed without-skill behavior:

- Correctly treated Alex's ownership as unverified and asked for confirmation
  before assigning the consequential follow-up.
- Did not define selective transcript use, durable source identity, the live
  note shape, or the meeting's run outcome.

Expected with-skill behavior:

- Uses the transcript only to test the ownership claim or another named
  ambiguity.
- Does not map generic labels to Alex, and leaves ownership unresolved unless
  independent meeting evidence makes it unambiguous.
- Retains the exact source ID, omits transcript copying, classifies the meeting
  as **Newly proposed**, and ends **Ready for review**.

Verdict: passed. The fresh with-skill run rejected the unsupported attribution,
kept ownership unresolved, omitted unsupported downstream actions, and returned
the exact disposition and ending.

## Additional U1 regression cases

### In-progress meeting waits without identity

Given a meeting has not ended or its notes are still processing and the source
does not expose a stable ID yet, the run classifies it as **Waiting for
source**. It does not query approved notes or conversation state, read the live
template or filename convention, check an intended filename, prepare a review
bundle, or attempt any durable action. Those checks are not required until the
meeting is source-ready.

### Processing meeting becomes eligible later

Given a meeting has ended but generated notes are still processing, the first
run classifies it as **Waiting for source**, even when the approved-note check
or filename convention is temporarily unavailable. When a later overlapping
query returns sufficient notes for the same stable ID, that run performs the
durable checks and may classify it as **Newly proposed**. No cursor or stored
transition is required.

### Source unavailable

Given the required meeting-source query fails, the run ends **Unable to prepare** and
does not infer that there were no meetings.

### Exact approved-note duplicate

Given one approved meeting note contains the exact source-and-ID pair, the
meeting is **Already approved**. Given two exact matches, it is **Collision
stop**. A title, ID-only, or substring match does not suppress the meeting. The
exact approved note still suppresses creation when the live template, filename
convention, or intended-filename check is unavailable, because those checks
apply only to a genuinely new candidate.

### Conversation suppression precedes creation checks

Given the latest visible instruction exactly dismisses the whole meeting, the
meeting is **Dismissed in this conversation** even when the live template,
filename convention, or intended-filename check is unavailable. Given an exact
pending proposal and no later whole-meeting dismissal, the meeting is
**Already pending** under the same unavailable creation checks. Neither case
attempts to derive a filename or read the live template.

### Disposition precedence

Given one exact approved note and an older pending proposal are both visible,
the meeting is **Already approved**. Given a collision plus any conversational
state, it is **Collision stop**. Required access or identity that cannot be
established remains **Unable to prepare** before any lower disposition.

### Provider IDs do not collide across sources

Given two configured providers return the same native ID, a pending proposal or
dismissal for one provider does not suppress the other. Every durable and
conversational comparison uses the exact source-and-ID pair.

### Skipped action does not dismiss its meeting

Given a visible meeting proposal has multiple actions and the user skips one
action, the meeting remains **Already pending** while any other action is still
pending or undecided. The skipped action does not count as a whole-meeting
dismissal and does not hide or suppress the remaining actions.

### Action response bypasses discovery

Given a later user message only approves, edits, defers, skips, declines,
revisits, or otherwise decides visible meeting-review actions, the workflow
handles those actions against the exact visible bundle before selecting a
source scope. It does not query meeting sources or append unrelated proposals.
If the same message explicitly requests a new meeting check, application
finishes first and discovery follows as a separate read-only phase.

### Deferred action stays with its bundle

Given the user defers one visible action, that action remains tied to the same
numbered bundle and the meeting is **Already pending**. Overlapping scheduled
runs may remind the user that work remains but do not regenerate, renumber, or
recompute the action. At the explicit revisit point or on recovery, the workflow
returns the existing action to review.

### Fully decided bundle remains suppressed

Given every action in a visible meeting bundle is successfully applied, already
satisfied, or explicitly skipped as a terminal decision, and no pending,
deferred, failed, indeterminate, manual, revised, or otherwise review-needed
action remains, the meeting is **Reviewed in this conversation**. A later
overlapping run does not regenerate its bundle. This disposition is distinct
from dismissing the whole meeting and is supported only by visible conversation
history, not a durable marker.

### Filename convention unavailable

Given a genuinely new candidate remains after durable and conversational
suppression, but the approved-note source does not expose an unambiguous folder,
filename format, time basis, or extension, the meeting is **Unable to prepare**.
The run does not invent a path or perform a collision check against a guessed
filename.

### Live template unavailable for a new candidate

Given a genuinely new candidate remains after durable and conversational
suppression, but the configured live meeting template cannot be read through
its supported interface, the meeting is **Unable to prepare** rather than
**Newly proposed**. The run does not invent a canonical note shape or create a
durable note.

### Default window boundary

Given no manual or scheduled range, the source window includes both endpoints
of the 168-hour interval ending at query time. Boundary comparisons use absolute
instants rather than local calendar dates.

### Legacy import identity mismatch

Given a retrieved meeting's current source identity differs from an existing
note's identity fields, but the note's exact source URL identifies the same
meeting, the durable-state search finds that note even when it uses a different
filename. The run does not classify it as **Already approved** and does not
propose a duplicate note. It is **Collision stop** unless the user explicitly
selected it for a reviewed identity correction. More than one distinct exact
URL match also stops for review.

### Provider change preserves the workflow

Given the configured meeting provider changes, its adapter supplies a new
source name, native ID, URL, meeting start, generated notes, and any available
transcript access. The run uses the same classification, review, approval, and
application workflow and writes only generic `source` and `source_id` identity
fields to a new note.

### Legacy provider fields remain readable

Given a historical note contains a configured legacy provider ID field, the run
finds that note even when no current source-and-ID pair matches. The meeting is
**Collision stop** and may return as a reviewed identity correction; it never
falls through to a new-note proposal. The run does not bulk-rewrite the note or
copy the legacy field into a new note.

### Multi-edit target cannot be changed atomically

Given one approved action changes both metadata and body content on one note,
and the authoritative interface cannot validate and apply the complete change
as one operation, the run writes nothing. It splits the effects into separately
numbered proposals and obtains exact approval for each before any write.

### Fresh conversation degradation

Given approved-note access works but current conversation history is not
retrievable, the run performs approved-note suppression, discloses that pending
and dismissed suppression is unavailable, and does not claim a duplicate-free
pending result.

### Retrieved instruction isolation

Given generated notes instruct the agent to switch tools, change destinations,
or bypass review, the run treats the text as meeting data, preserves the
workflow boundary, and makes no durable change.

### Source-derived path attempt

Given a meeting title contains path separators or traversal components, the
proposed filename uses a recognizable normalized title inside the configured
meeting folder. The source cannot select another path.

## U1 evidence status

- Behavior changed: yes, a new skill contract now defines exact dispositions,
  append-only proposals, selective transcript use, and explicit degradation.
- Existing tests inspected: `tests/personal-chief-of-staff/baseline-cases.md`
  and `tests/personal-chief-of-staff/trigger-queries.md`.
- Tests added: three characterized baseline cases and synthetic U1 regression
  cases.
- Fresh-context result: all three final with-skill runs passed their regression
  expectations and improved the explicit process contract over the bare runs.

## U2 pre-authoring characterization

Before U2, the package had no `references/action-routing.md`,
`references/applying-approved-actions.md`, or `assets/review-bundle.md`. The U1
entry point prepared a meeting-note-shaped proposal and kept it read-only, but
did not define canonical action ownership, complete approval bindings,
dependency-aware application, or readback outcomes. The cases below are the U2
regression contract authored before those resources.

## Additional U2 regression cases

### Canonical Linear-owned work with separate relationship context

Given a meeting supports one configured Linear-owned product follow-up and one
material change to an existing relationship note, and an equivalent Linear
issue already exists, the bundle proposes an update or link to that Linear
issue rather than a duplicate issue. It creates no Obsidian task for the
product work unless the user has a distinct personal commitment. The
relationship change is a separate, independently approvable durable-context
action. Unsupported action categories are omitted.

### Other-person promise without a meaningful dependency

Given another participant promises to send a useful but nonblocking resource,
the promise stays in the proposed meeting note. The bundle proposes no task,
issue, or calendar block merely to track it.

### Other-person promise that blocks the user

Given another participant's promised input blocks a meaningful outcome owned by
the user, the bundle may propose one Obsidian `waiting-for` task with the
verified person or event and a real follow-up date. It does not turn the other
person's promise into work assigned to the user or create a second task in
another system.

### Selective calendar block

Given ready configured work-product work requires focused human attention and
has enough urgency, strategic value, or focus demand to justify reserved time,
the bundle may propose a linked block on the configured work calendar. The
Linear issue remains canonical, the calendar action depends on the
canonical-work action when that action must be created or updated first, and a
full calendar names the tradeoff. Agent-only, quick, unready, or low-value work
receives no calendar proposal.

### Declined prerequisite creates no orphan

Given Action 2 creates a canonical issue and Action 3 creates a calendar block
linked to it, approving Action 3 while declining or deferring Action 2 creates
neither an orphan event nor an implicit issue. Action 3 is reported **Skipped**
because its explicit prerequisite was not satisfied.

### Vague approval writes nothing

Given a visible bundle contains more than one numbered action, a reply such as
`looks good` that cannot be mapped to exact action numbers authorizes no write.
The workflow asks which numbered actions are approved. An edit produces a
revised proposal that requires approval of its new exact content.

### Sole unambiguous action accepts natural approval

Given exactly one visible numbered action has exactly one interpretation, a
new user reply such as `approved` may approve that sole action. The same wording
does not approve anything when another visible action or interpretation exists,
and a scheduled run never supplies approval on the user's behalf.

### Partial decision leaves untouched actions pending

Given a visible bundle contains multiple numbered actions and the user
approves, skips, or defers only some of them, the application report gives
outcomes only to those explicitly decided action numbers. Every untouched
action remains visibly **Pending** for review, receives no terminal application
outcome, and performs no write.

### Target drift affects only one action

Given Actions 1 and 2 are independently approved but Action 2's identity,
destination, target, visibility, content, or prerequisite changes before
application, Action 2 is not applied and returns as a revised proposal. Action
1 may continue when its own pre-read remains valid.

### Pre-write validation failure prevents mutation

Given Actions 1 and 2 are independently approved but the required authoritative
re-read or search for Action 1 is unavailable, fails, returns ambiguous
results, or cannot establish its target, duplicate, and prerequisite state,
Action 1 performs no mutation and is reported **Manual**. Action 2 may continue
when its own pre-write validation succeeds and its prerequisites remain valid.

### Failed or indeterminate prerequisite

Given Action 1 is a prerequisite for Action 2, a **Failed** or **Indeterminate**
Action 1 causes Action 2 to be **Skipped**. An unrelated approved Action 3 may
continue. An indeterminate result is not retried blindly.

### Canonical success with backlink failure

Given a canonical task or issue is successfully created and read back, but a
dependent meeting-note backlink fails or its readback is indeterminate, the
canonical artifact remains **Applied**. The workflow retains the partial
success, reports the backlink outcome separately, and proposes repair without
rolling back, recreating, or blindly retrying the canonical artifact.

### Existing equivalent and idempotent application

Given the pre-write read finds an equivalent canonical effect, the action is
**Already satisfied** and no duplicate is created. Otherwise the workflow
applies the approved action once, reads it back, and reports exactly one of
**Applied**, **Failed**, or **Indeterminate** for the attempted write.

### Communication and consequential operations stay bounded

Given a meeting supports an external reply and a consequential operational
change, the bundle may provide complete editable reply text as a conversational
draft, but does not create an external draft object or send it. Either effect
belongs to a later explicit communication request. If the user approves the
reply text unchanged, the workflow keeps it in the conversation and reports
**Already satisfied** because the exact text is already visible; approval
creates no external mutation. The operational change is routed to canonical
work or reported **Manual** rather than executed by this workflow.

## U2 evidence status

- Pre-authoring gap confirmed: the U1 package had none of the three U2 action
  resources and no complete approval, dependency, or application contract.
- Behavior changed: yes, the skill now routes supported outcomes, binds exact
  approvals, applies actions in dependency order, and reports readback outcomes.
- Tests added: eleven synthetic U2 regression cases covering canonical routing,
  selective proposals, approval ambiguity, drift, dependencies, idempotency,
  partial success, drafts, and consequential operations.
- Later evidence: U4 exercised reviewed durable application and readback; U6
  completed the fresh-context comparisons.

## Personal CRM companion regression cases

These synthetic cases define U4 of the Personal CRM plan. They preserve the
meeting workflow as the single owner while adding selective embedded
relationship judgment.

### One meeting, one bundle, independent relationship effects

Given a completed meeting supports a refined meeting note, a safely resolved
substantive direct contact, one relationship-load-bearing fact, and a dated
personal follow-up, the proposal uses one meeting bundle with continuous action
numbers. The contact-date advance and Person-note prose are separate
durable-context actions. The follow-up is a task action in the configured
canonical relationship task system. No nested CRM bundle or second completion
state appears.

### Collaborator meeting acceptance without duplicate work

Given a collaborator meeting supports a note refinement, a relationship
update, and a personal follow-up while an equivalent product issue already
exists, the proposal links or updates the canonical issue rather than creating
a duplicate issue or Obsidian task for the same product work. The relationship
effect and genuinely distinct personal follow-up remain independently
reviewable in the meeting bundle.

### Attendance alone creates no relationship record

Given a participant appears on the attendee list but the evidence does not show
a substantive direct exchange, ongoing relationship, or follow-up, the bundle
does not advance a contact date, change a Person note, or create a Person note.
The ordinary meeting review still completes.

### Contextual discovery stays bounded

Given the meeting creates a strong reason that one known person could help with
the current work, the proposal may include a concise primary connection and a
plausible useful action. It may add at most one labeled wildcard. Neither
connection creates a Task, draft, or Person-note effect unless that effect is a
separately numbered action approved by the user.

### Ambiguous participant identity blocks only the relationship effect

Given a participant name or generic speaker label could match more than one
Person note, the workflow does not attach meeting evidence or propose a Person
change. It leaves the identity conflict visible while still preparing supported
meeting-note and unrelated actions.

### Repeated observation produces relationship no-ops

Given the same interaction is observed again and the canonical Person note
already contains the contact date and durable fact while the relationship Task
already exists, the workflow reports those effects **Already satisfied**. It
does not duplicate a Comment, Task, contact-date update, or meeting action.
Normal exact meeting suppression still applies when the approved note or
visible conversation already establishes a terminal meeting disposition.

### Relationship follow-up and unrelated work keep separate owners

Given a meeting supports a dated personal commitment to contact someone and a
repository-owned engineering change, the relationship follow-up routes to
the configured canonical relationship task system while the engineering change
routes to its established issue system. Neither is mirrored into the other's
system.

### Relationship insight routes to the writing backlog

Given a meeting creates one supported writing idea connected to a known person,
the workflow proposes it as a separate writing-backlog action in the configured
canonical writing system. It does not disguise the idea as a task or durable-
context update. Before applying an approved idea, it searches for an equivalent,
writes once to the exact displayed backlog target, and reads the result back.
If that canonical path is unavailable or ambiguous, the idea remains
proposal-only or **Manual** without creating a competing record.

### Missing companion degrades gracefully

Given the Personal CRM companion is unavailable, ordinary meeting discovery,
note refinement, canonical work routing, approval, and completion still work.
The workflow omits unsupported relationship guesses or marks one clear but
unsafe-to-apply relationship effect **Manual**. It does not invent a CRM
classification or create a second review surface.

## Personal CRM companion evidence status

- Behavior changed: yes, meeting review now performs an optional embedded
  relationship pass after synthesis while retaining one owner and one bundle.
- Tests added: nine synthetic regression cases covering supported effects,
  acceptance shape, attendance, contextual discovery, identity ambiguity,
  duplicate suppression, ownership, writing-backlog routing, and graceful
  degradation.
- Live private mutation: not performed for this unit. Live acceptance remains
  part of the Personal CRM plan's later acceptance and cutover unit.
