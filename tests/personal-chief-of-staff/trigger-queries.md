# Trigger queries: personal-chief-of-staff

These synthetic queries test invocation boundaries. Expected routes are
categorical and can be checked without live source access.

## Should invoke

| Query | Expected mode | Reason |
| --- | --- | --- |
| Give me my morning chief-of-staff review. | Morning | Explicit morning review. |
| Run my daily chief-of-staff review. | Morning | Generic daily wording without evening or wind-down context defaults to Morning. |
| What needs my attention today? Check my live context and help me decide. | Morning | Asks for the evidence-based daily orientation review. |
| Run my scheduled morning review, but do not invent work if nothing matters. | Morning | Explicit scheduled morning mode. |
| Help me wind down, reflect on today, and prepare tomorrow. | Wind-down | Requests the daily closing review. |
| I am ready to complete today's journal with you. | Wind-down | Invokes the interactive journal and next-day flow. |
| Run the scheduled wind-down and wait for my reflection. | Wind-down | Explicit scheduled wind-down mode. |
| Help me complete this week's review from my current sources. | Weekly | Explicit weekly review. |
| I skipped a few weekly reviews. Resume with the current week, not a backlog. | Weekly | Invokes weekly resumption behavior. |
| Run my weekly chief-of-staff review and help me choose next week's outcomes. | Weekly | Explicit weekly mode and forward planning. |
| Help me complete the current Quarterly Review from the evidence that exists. | Quarterly | Explicit quarterly review. |
| My quarterly reviews lapsed. Help me examine strategy and set the next quarter. | Quarterly | Invokes quarterly resumption and strategy discussion. |
| Run the scheduled quarterly review and wait for my judgment. | Quarterly | Explicit scheduled quarterly mode. |
| Approve action 2 and defer action 3 from the morning chief-of-staff bundle above. | Originating visible mode | Decides actions from an identifiable visible chief-of-staff bundle. |
| Resume the paused weekly bundle above and revisit action 2. | Originating visible mode | Resumes and revisits an action from an identifiable visible chief-of-staff bundle. |

## Should not invoke

| Query | Expected owner | Reason |
| --- | --- | --- |
| Create a personal task to renew my passport next month. | Obsidian task workflow | Isolated task creation. |
| Turn this implementation request into a GitHub issue. | Issue-writing workflow | Repository issue, not a review cadence. |
| Process my inbox and draft replies. | Email-processing workflow | Isolated email operation. |
| Move tomorrow's dentist appointment to Friday. | Calendar workflow | Direct calendar edit. |
| Analyze whether my sleep affects afternoon focus. | Health or analysis workflow | Standalone health question without a review cadence. |
| Help me plan this feature implementation. | Ordinary planning workflow | Project planning, not a chief-of-staff review. |
| Critique this article draft in my writing style. | Writing workflow | Isolated writing request. |
| Prepare me for my customer meeting at 2 PM. | Meeting-preparation workflow | One meeting, not a broader review. |
| Approve the reply action from the email-processing bundle above. | Email-processing workflow | The visible action belongs to the calling workflow, not the chief-of-staff context provider. |

## Reach-through query

| Query | Expected route | Reason |
| --- | --- | --- |
| While processing this email, use my current chief-of-staff context to judge its priority. | Email workflow invokes this skill for context | Another workflow explicitly asks for current cross-source priority context without transferring ownership of the email operation. |

## Grading

- **Pass:** The selected mode or owning workflow matches the expected route.
- **Fail:** The chief-of-staff skill overtriggers, undertriggers, or selects the
  wrong cadence.
- **N/A:** The query is changed so materially that the expected route no longer
  applies.

Maintenance: add a concise redacted query when a real invocation error escapes.
Revisit the set when the description, mode boundaries, or downstream workflow
contracts change.
