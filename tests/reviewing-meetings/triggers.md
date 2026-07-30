# Trigger contract: reviewing-meetings

Judged per the protocol in [`tests/README.md`](../README.md): fresh context,
name + description + query only, binary judgment, any near-miss `yes` fails.

## Should trigger

| Query | Reason |
| --- | --- |
| Review my new meetings. | Explicit post-meeting review. |
| Process the Granola call that just ended, but do not write anything yet. | Completed meeting intake with review boundary. |
| Check whether any completed meetings need importing from my configured source. | Source-independent new-meeting detection. |
| Catch me up on unprocessed meetings from the last week. | Manual overlapping-window recovery. |
| Prepare a reviewed meeting-note proposal from this completed call. | Requests the skill's durable proposal. |
| Run the scheduled post-meeting review now. | Explicit scheduled invocation. |
| Did any calls finish since the last meeting review? Use stable source IDs, not a cursor. | Non-obvious eligibility phrasing. |
| Revisit this completed meeting and tell me whether it is already approved or still pending. | Requests exact disposition. |
| I missed the earlier meeting batch. Find only newly eligible meetings and leave old proposals alone. | Explicit append-only catch-up. |
| Approve action 2 from the meeting review. | Applies a visible meeting-review action. |
| Change action 1's due date to Friday, then approve it. | Edits and approves a visible meeting-review action. |
| Defer action 3 until next week. | Defers a visible meeting-review action. |
| Skip action 4. | Dismisses a visible meeting-review action. |
| Resume the deferred CRM-derived action 5 from the visible meeting-review bundle. | Revisits a deferred relationship effect without leaving the meeting workflow. |

## Near misses: should not trigger

| Query | Expected owner |
| --- | --- |
| Prepare me for tomorrow's customer meeting. | Meeting-preparation workflow. |
| Take live notes during this call. | Live note-taking or recording workflow. |
| Summarize this uploaded interview transcript. | Generic document or transcript workflow. |
| Update this person's CRM record. | Personal CRM workflow. |
| Create a task to send the proposal Friday. | Task workflow. |
| Turn this requirement into a GitHub issue. | Issue-writing workflow. |
| Block two hours on my calendar for focused work. | Calendar workflow. |
| Clean up the formatting in this existing meeting note. | Note-editing workflow. |
| Search all historical meeting notes for duplicate titles. | Historical note audit, not new-meeting review. |
