---
type: llm
focus: trace
weight: 1
---

The block for acme/ledger-app#441 includes a situation whose result the rounding change alters, such as a same-price plan switch mid-cycle that goes from $0.00 to $0.01, marked as not described, and shows the Math.floor and Math.ceil lines from app/billing/proration.ts as the code behind it.
