# Trigger queries: reviewing-meetings

These full-rigor synthetic queries define the listing-level invocation
boundary. They are ready for three fresh judgments per query after the complete
skill package is available. U1 records expected routes but does not claim an
unrun activation result.

Date: 2026-07-22 | Planned harness: fresh agent contexts | Model: session default

## Should trigger

| Query | Expected judgment | Reason |
| --- | --- | --- |
| Review my new meetings. | Yes | Explicit post-meeting review. |
| Process the Granola call that just ended, but do not write anything yet. | Yes | Completed meeting intake with review boundary. |
| Check whether any completed meetings need importing from my configured source. | Yes | Requests source-independent new-meeting detection. |
| Catch me up on unprocessed meetings from the last week. | Yes | Manual overlapping-window recovery. |
| Prepare a reviewed meeting-note proposal from this completed call. | Yes | Requests the skill's durable proposal. |
| Run the scheduled post-meeting review now. | Yes | Explicit scheduled invocation. |
| Did any calls finish since the last meeting review? Use stable source IDs, not a cursor. | Yes | Non-obvious eligibility phrasing. |
| Revisit this completed meeting and tell me whether it is already approved or still pending. | Yes | Requests exact disposition. |
| I missed the earlier meeting batch. Find only newly eligible meetings and leave old proposals alone. | Yes | Explicit append-only catch-up. |
| Approve action 2 from the meeting review. | Yes | Applies a visible meeting-review action. |
| Change action 1's due date to Friday, then approve it. | Yes | Edits and approves a visible meeting-review action. |
| Defer action 3 until next week. | Yes | Defers a visible meeting-review action. |
| Skip action 4. | Yes | Dismisses a visible meeting-review action. |
| Resume the deferred CRM-derived action 5 from the visible meeting-review bundle. | Yes | Revisits a deferred relationship effect without leaving the meeting workflow. |

## Near misses: should not trigger

| Query | Expected judgment | Expected owner |
| --- | --- | --- |
| Prepare me for tomorrow's customer meeting. | No | Meeting-preparation workflow. |
| Take live notes during this call. | No | Live note-taking or recording workflow. |
| Summarize this uploaded interview transcript. | No | Generic document or transcript workflow. |
| Update this person's CRM record. | No | Personal CRM workflow. |
| Create a task to send the proposal Friday. | No | Task workflow. |
| Turn this requirement into a GitHub issue. | No | Issue-writing workflow. |
| Block two hours on my calendar for focused work. | No | Calendar workflow. |
| Clean up the formatting in this existing meeting note. | No | Note-editing workflow. |
| Search all historical meeting notes for duplicate titles. | No | Historical note audit, not new-meeting review. |

## Evaluation protocol

Show each fresh judge only the skill name, description, and one query. Require
`yes`, `no`, or `unsure`. Run every query three times. A should-trigger query
passes with at least two `yes` judgments. Any `yes` on a near miss fails the
set. Treat `unsure` as borderline, tune only the description, and rerun every
affected query.

Status: passed on 2026-07-23. Three fresh listing-level judges evaluated the
original 18 queries using only the final skill name and description. Every judge
marked all nine intended queries `yes` and all nine near misses `no` (54 of 54
correct, with no `unsure` judgments). Each of the four later action-response
queries was then evaluated in three new listing-only contexts; all 12 judgments
were `yes`. Combined evidence is 66 of 66 correct judgments with no `unsure`
result. Three fresh judges then invoked for the deferred CRM-derived
meeting-action resume and rejected a direct-CRM-bundle near-miss, for 6 of 6
passing judgments.
