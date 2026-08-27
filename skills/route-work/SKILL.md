---
name: route-work
description: Use only when the user explicitly asks to route a work kickoff to its first workflow owner or decide whether a proven in-flight owner should continue.
license: MIT
---

# Route Work

Read [references/routing.md](references/routing.md) through its
`route-work-contract-end` marker before classifying the request. It is the
single source of truth for every routing decision and output; do not recreate
its tables here.

## Assess, render, stop

1. Confirm the request has explicit routing intent. Inspect only the request,
   the single named primary artifact when present, directly cited repository
   instructions, and authoritative metadata already supplied in the current
   context, as bounded by the reference.
2. Apply the reference to decide whether this attempt ends in a ready route,
   continuation, clarification, or named stop. Use the first unresolved effect
   rather than the request's carrier.
3. Render exactly one of the reference's Markdown cards without changing its
   heading or field labels. Copy stable locators and decisive facts rather than
   full artifacts, and include only the optional fields that are material.
4. Stop immediately after the card. The selected owner controls any later
   work, conditional handoff, or topology revision.

One routing attempt may span the initial turn and one clarification answer.
When clarification is necessary, the initial turn emits the reference's single
question and exits. On the answer, combine it with the original evidence still
visible in the conversation, perform one final assessment, and return a route,
continuation, or named stop. Use `Insufficient input` when the answer still
does not resolve an owner. Ask no second question and persist no routing state.

## Authority boundary

Preserve only authority the operator supplied. The assessment and response are
read-only. Stop after routing and leave discovery, diagnosis, planning,
research, implementation, and every external or mutating action to a later
authorized workflow. Do not invoke or load that workflow, probe quota or model
catalogs, or select a higher effort without the operator's approval.

Workflow names in the card are portable capability labels; using this skill
does not require those workflow packages to be installed.
