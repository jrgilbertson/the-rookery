# Trigger queries: managing-personal-crm

These synthetic listing-level queries define the portable trigger boundary.
The full-rigor set has nine should-trigger and nine near-miss queries. Judge
each in three fresh contexts using only the skill name, description, and query.

## Should invoke

| Query | Expected route | Judgments | Reason |
| --- | --- | --- | --- |
| I just caught up with Sam. Update our relationship context and note when we spoke. | Direct capture | Yes, yes, yes | Explicit relationship interaction capture. |
| Prepare me for coffee with Priya using her Person note and any useful recent context. | Direct close-up | Yes, yes, yes | Requests one-person relationship preparation. |
| Start the one-time cleanup of my Person notes and triage the first batch. | Catch-up | Yes, yes, yes | Explicit CRM catch-up and triage. |
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
and query set. All 27 should-trigger judgments were `yes`; all 27 near-miss
judgments were `no`. No description tuning or borderline rerun was required.
