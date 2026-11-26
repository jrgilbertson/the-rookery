---
type: llm
focus: trace
weight: 1
---

In the first turn the Captain starts a worker for #527 and none for #525 or #526. It says #525 waits for the active worker on #520, which holds app/billing/invoice.ts, and #526 waits for open pull request #530, which changes app/views/settings.tsx even though no fleet session owns it.
