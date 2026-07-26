# Trigger queries: managing-personal-crm

These synthetic listing-level queries define the portable trigger boundary.
The set has seventeen should-trigger and nine near-miss queries. Judge
each in three fresh contexts using only the skill name, description, and query.

## Should invoke

| Query | Expected route | Judgments | Reason |
| --- | --- | --- | --- |
| I just caught up with Sam. Update our relationship context and note when we spoke. | Direct capture | Yes, yes, yes | Explicit relationship interaction capture. |
| Prepare me for coffee with Priya using her Person note and any useful recent context. | Direct close-up | Yes, yes, yes | Requests one-person relationship preparation. |
| Start the one-time cleanup of my Person notes and triage the first batch. | Catch-up | Yes, yes, yes | Explicit CRM catch-up and triage. |
| That visible catch-up source inventory is right. Keep Person notes and Messages required, drop WhatsApp, and continue the preflight. | Catch-up inventory decision | Yes, yes, yes | Confirms and revises the required source inventory for the visible catch-up. |
| For the visible catch-up batch: 1 active, 2 merge into Taylor Reed, 3 reference, and 4 delete. Continue without applying any cleanup. | Catch-up stage-one decisions | Yes, yes, yes | Supplies mixed reviewed dispositions that continue the visible catch-up without authorizing effects or cleanup. |
| Your visible stage-two interpretation for Morgan is right, except the shared project ended in May rather than June. Continue with Morgan. | Catch-up stage-two interpretation correction | Yes, yes, yes | Corrects the current reconstruction without approving a destination effect. |
| Answering the focused question for the current catch-up person: we met through the Atlas project, and I expect to stay in touch. | Catch-up stage-two focused answer | Yes, yes, yes | Supplies requested reconstruction evidence for the visible current person. |
| Resume the deferred stage-two reconstruction for Priya from the visible catch-up recap. | Catch-up stage-two resume | Yes, yes, yes | Resumes the exact deferred reconstruction rather than starting new discovery. |
| For that Person-note catch-up batch, keep the first two, skip the third, and move the proof-verified duplicates to Trash. | Catch-up decisions | Yes, yes, yes | Decides catch-up dispositions and cleanup approval against the visible bundle. |
| Revisit the deferred action from the visible direct CRM bundle so I can decide it now. | Direct deferred-action revisit | Yes, yes, yes | Resumes an exact deferred direct proposal without implying approval. |
| Resume the deferred cleanup action from the visible catch-up CRM bundle for another review. | Catch-up deferred-action revisit | Yes, yes, yes | Resumes an exact deferred catch-up proposal without implying approval. |
| Which close relationships are overdue for a thoughtful check-in? | Direct cadence scan | Yes, yes, yes | Explicit relationship-cadence request. |
| Who I know could give useful feedback on this article, and why now? | Direct discovery | Yes, yes, yes | Connects current work to a relevant person and action. |
| This email contains a meaningful career update and a promise I made. Evaluate the relationship effects while I process it. | Embedded capture | Yes, yes, yes | Invoking workflow asks for relationship effects without giving up ownership. |
| During this meeting review, check whether anything belongs in a Person note or a dated relationship follow-up. | Embedded capture | Yes, yes, yes | Soft relationship invocation inside a meeting-owned bundle. |
| This weekly review found a close friend well past our usual contact rhythm. Suggest a useful next move inside the current review. | Embedded cadence | Yes, yes, yes | Existing workflow encounters an overdue relevant person. |
| I rejected that outreach idea because the person changed fields. Does their durable relationship context need correction? | Direct correction | Yes, yes, yes | Non-obvious request to assess stable Person-note meaning. |

## Should not invoke

| Query | Expected owner | Judgments | Reason |
| --- | --- | --- | --- |
| Create a task to renew my passport next month. | Canonical task workflow | No, no, no | Simple task creation with no relationship judgment. |
| Rewrite this article introduction in a warmer voice. | Writing workflow | No, no, no | Generic writing request. |
| Process my entire inbox and draft replies. | Email-processing workflow | No, no, no | Broad email processing without a relationship effect. |
| Review yesterday's meeting and capture its decisions. | Meeting-review workflow | No, no, no | No relationship effect requested or evident. |
| Look up Pat's phone number in my contacts. | Contact lookup | No, no, no | Identity lookup without relationship judgment. |
| Give me my ordinary morning chief-of-staff review. | Chief-of-staff workflow | No, no, no | Broad review remains with its owner unless it encounters relationship relevance. |
| Move tomorrow's dentist appointment to Friday. | Calendar workflow | No, no, no | Direct calendar edit. |
| Draft a friendly message to a new vendor. | Communication workflow | No, no, no | Communication drafting without existing relationship context. |
| Build a database to track every message and social reaction. | Product or data workflow | No, no, no | A CRM database and activity timeline are outside this skill. |

## Grading

- **Pass:** At least two of three fresh listing-level judgments match the
  expected route for each should-trigger query, and every near-miss is rejected
  in all three runs.
- **Fail:** A should-trigger misses in two runs or any near-miss activates.
- **Borderline:** An `unsure` or hedged response; tune only the description and
  rerun the affected query.

## Execution record

Date: 2026-07-24 | Harness: Codex CLI fresh contexts | Model: session default

Three independent listing-level judges saw only the final name, description,
and the original nine-query should-trigger set. All 27 original should-trigger
judgments were `yes`; all 27 near-miss judgments were `no`. No description
tuning or borderline rerun was required.

After PR review expanded the description to cover catch-up decisions, three
fresh judges evaluated the added catch-up-decision query and a focused embedded
chief-of-staff near-miss. All three invoked for the catch-up decision and all
three left the embedded action with the caller, for 6 of 6 passing judgments.

After the catch-up continuation review, three fresh judges received only the
revised name and description plus an inventory decision, a mixed stage-one
disposition reply, and a meeting-owned action near-miss. All three invoked for
both catch-up continuations and rejected the meeting-owned action, for 9 of 9
passing judgments.

After deferred-action routing was added, three fresh judges received only the
revised name and description plus Direct and Catch-up resume queries and an
email-owned near-miss. All three invoked for both CRM resumes and rejected the
email-owned action, for 9 of 9 passing judgments.

After stage-two continuation routing was added, three fresh judges received
only the revised name and description plus interpretation-correction,
focused-answer, and deferred-reconstruction queries and a generic-questionnaire
near-miss. All three invoked for the three catch-up continuations and rejected
the near-miss, for 12 of 12 passing judgments.

The later metadata correction restores the explicit phrase `revisits or
resumes a deferred action`, aligning the description with the existing Direct
revisit and Catch-up resume queries above. This was a focused static regression
check only; no new listing-level judge run was performed.
