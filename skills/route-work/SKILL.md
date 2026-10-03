---
name: route-work
description: Use only when the user explicitly asks to route a work kickoff to its first workflow owner or decide whether a proven in-flight owner should continue.
license: MIT
---

# Route Work

Read [references/routing.md](references/routing.md) through its
`route-work-contract-end` marker before assessing the request. It is the
single source of truth for routing decisions and output. Model-table
maintenance below the marker is not part of a routing invocation.

Assess the request, render exactly one response template with its specified
first line and section labels, and stop after the card.
