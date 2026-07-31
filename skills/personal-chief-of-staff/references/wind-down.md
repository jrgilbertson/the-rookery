# Wind-down

Use this mode to close one local day through the user's canonical daily journal
and authoritative sources. A scheduled and manual wind-down follow the same
workflow.

## Establish the day

Resolve the local date and review window. If the run time or the user's wording
makes the day being closed ambiguous, as can happen just after midnight,
resolve the intended journal date before drafting. Treat the following local
date as the commitment target day. Through the Obsidian CLI, find the configured
daily-journal template and the closing-date journal, if one exists. Read the
existing journal before drafting so manual content, frontmatter, links, embeds,
and unresolved thoughts remain intact.

Query only sources that can clarify what happened or what changed: relevant
messages and meetings, active tasks, relationship context, project or
repository state, and available capacity evidence. Query each visible personal
and work calendar separately for the day and retain its calendar identity in
the evidence. Calendar visibility supplies no work-email coverage. Separate:

- observed outcomes, events, decisions, commitments, and source changes;
- reasonable inferences that still need confirmation; and
- subjective meaning that cannot be observed.

Completion: the review window, existing journal state, and material evidence
gaps are known without writing anything.

## Begin with one broad reflection

Present a short evidence-based reconstruction, then ask one broad invitation
such as: “What stands out about today, including anything the sources would
miss?” Wait for the user's free-form response before asking targeted
follow-ups. Do not turn the template into an opening questionnaire.

Use follow-ups only to resolve material gaps or help complete the current
template. The user may leave any subjective field blank, mark it uncertain,
correct the synthesis, or keep their original wording.

Completion: the user's own account of the day is available before the agent
drafts subjective conclusions.

## Capture relationship effects selectively

When the day's evidence or the user's reflection describes a substantive
direct interaction, use the companion relationship capability when available
to evaluate it. Account for the reliable local interaction date with either a
novel `date_last_contacted` proposal or **Already satisfied** when the canonical
date is equal or newer. Propose Person prose only when the interaction adds
durable meaning likely to improve a future interaction.

Keep the contact-date change and each distinct Person-note, Task, or
communication effect as separate actions in the existing wind-down bundle.
Do not copy a transcript, message thread, meeting recap, or chronological
interaction log into the journal or Person note. When identity or interaction
time is unresolved, show the uncertainty and do not propose the unsafe effect.

Completion: every supported substantive direct interaction has a contact-date
outcome that is either independently reviewable or already satisfied,
distinct durable meaning remains separate, and passive or ambient activity
produces no contact effect.

## Complete the existing journal together

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
content, and clearly identifies every subjective statement awaiting approval.

## Reconcile what changed elsewhere

Compare the day's evidence with the systems that own the resulting truth.
When needed, propose separate actions for:

- a canonical task's status, next step, due date, or waiting context;
- relationship or follow-up context in the canonical CRM;
- a decision, project, repository, or issue record;
- a calendar commitment or next-day time block; or
- another authoritative source whose current record is now inaccurate.

Do not hide these changes inside the journal or create a second task list. A
journal proposal and every source update remain independently approvable.

For one active sequential critical path, a precise restart cue may be useful.
Capture only the next concrete operation and keep it with the canonical task or
approved next-day plan. Do not add restart metadata to every task.

Completion: each changed fact has one proposed canonical destination, or is
explicitly left unchanged.

## Prepare tomorrow

Read each visible personal and work calendar separately for the next day,
retaining its calendar identity, along with relevant active tasks. Use the
actual day's outcomes, unresolved commitments, known capacity, and current
constraints to propose a realistic plan. Distinguish fixed commitments from
flexible blocks using their context rather than assuming either.

Name the critical path and the few protected outcomes when useful. Calendar
edits, task changes, and communications remain separate review actions. Do not
expand the plan merely because more work is discoverable.

Completion: the next-day proposal reflects current sources and makes its
tradeoffs visible without writing to them.

## Record tomorrow's meaningful commitments

When the live daily-journal template contains a `Tomorrow’s Meaningful
Commitments` section, use it as the configured place for reviewed next-day
intent. Draft three to five numbered plain-Markdown bullets in the closing-date
journal.
Each bullet uses one to three sentences that naturally combine a concrete
outcome, an observable finish line, and one short reason tied to strategy, an
obligation, or an avoided cost. Collaborate to refine an activity label such as
“development,” “meetings,” or “work on X” into a concrete outcome by default.
If the user explicitly approves broad or incomplete wording unchanged, preserve
it verbatim, identify the missing element, and treat it as nonconforming source
content rather than claiming it satisfies the three-element condition.

Use the day's outcomes, unresolved work, next-day capacity, fixed commitments,
active tasks, current strategy, and the user's judgment to draft the list. The
user supplies or explicitly approves every rationale. Do not
use task checkboxes or add completion status, scores, streaks, grades, or
mandatory item-by-item reconciliation.

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
three to five reviewed bullets with all three elements; otherwise the existing
next-day planning behavior continues without an invented journal write.

## Promote only durable signal

When a high-signal insight may help an audience, offer one writing seed without
creating a quota, draft, or publication action automatically. Keep central
thinking and the rough draft human-led unless the user asks for more help.

Propose a change to the canonical learning notes only when the user requests it
or the day adds evidence to a repeated, behavior-changing pattern. A one-day
observation normally stays in the daily journal.

Completion: optional writing and learning proposals are selective, sourced,
and independently reviewable.

## Review, write, and verify

Present the journal and all source changes in one review bundle with separate
numbered actions. Apply only approved actions under the shared source rules.

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
not in a generated brief or internal run record.

Completion: the reviewed journal is visible in its canonical note, every other
action has an independent outcome, tomorrow's plan reflects the final sources,
and no unapproved or unverifiable change is reported as complete.
