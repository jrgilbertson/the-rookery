# Trigger contract: personal-chief-of-staff

Judged per the protocol in [`tests/README.md`](../README.md): fresh context,
name + description + query only, binary judgment, any near-miss `yes` fails.

## Should trigger

| Query | Reason |
| --- | --- |
| Help me wind down, reflect on today, and prepare tomorrow. | Daily closing review. |
| I am ready to complete today's journal with you. | Interactive journal and next-day flow. |
| Run my daily chief-of-staff review. | Generic daily wording selects wind-down. |
| Run the scheduled wind-down and wait for my reflection. | Scheduled wind-down invocation. |
| Help me complete this week's review from my current sources. | Explicit weekly review. |
| I skipped a few weekly reviews. Resume with the current week, not a backlog. | Weekly resumption. |
| Run my weekly chief-of-staff review and help me choose next week's outcomes. | Weekly review with forward planning. |
| Help me complete the current Quarterly Review from the evidence that exists. | Explicit quarterly review. |
| My quarterly reviews lapsed. Help me examine strategy and set the next quarter. | Quarterly resumption and strategy. |
| Run the scheduled quarterly review and wait for my judgment. | Scheduled quarterly invocation. |
| Approve action 2 and defer action 3 from the wind-down chief-of-staff bundle above. | Decides visible chief-of-staff actions. |
| Resume the paused weekly bundle above and revisit action 2. | Resumes a visible chief-of-staff bundle. |
| While processing this email, use my current chief-of-staff context to judge its priority. | Another workflow requests cross-source context; the email stays caller-owned. |

## Near misses: should not trigger

| Query | Expected owner |
| --- | --- |
| Give me my morning chief-of-staff review. | No published owner (Morning mode removed). |
| What needs my attention today? Check my live context and help me decide. | No published owner (Morning mode removed). |
| Run my scheduled morning review, but do not invent work if nothing matters. | No published owner (morning schedule removed). |
| Create a personal task to renew my passport next month. | Task workflow. |
| Turn this implementation request into a GitHub issue. | Issue-writing workflow. |
| Process my inbox and draft replies. | Email-processing workflow. |
| Move tomorrow's dentist appointment to Friday. | Calendar workflow. |
| Analyze whether my sleep affects afternoon focus. | Health-analysis workflow. |
| Help me plan this feature implementation. | Planning workflow. |
| Critique this article draft in my writing style. | Writing workflow. |
| Prepare me for my customer meeting at 2 PM. | Meeting-preparation workflow. |
| Approve the reply action from the email-processing bundle above. | Email-processing workflow owns its visible actions. |
