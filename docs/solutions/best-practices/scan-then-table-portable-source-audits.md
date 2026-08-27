---
title: "Lead portable source audits with scan lines, then an unwrapped table"
date: 2026-08-27
category: best-practices
module: personal-chief-of-staff
problem_type: best_practice
component: documentation
severity: medium
applies_when:
  - "Condensing an owner-facing source or access census without reducing coverage"
  - "A disclosure widget would hide claim-changing limits on a TUI or CLI host"
  - "HTML details or similar collapse markup is tempting as the recovery surface"
symptoms:
  - "A row-per-source table gives routine successes the same weight as failures"
  - "Material limits are only visible after expanding a disclosure"
  - "HTML details tags render as raw markup or stay expanded on Codex TUI, Gemini CLI, or Grok TUI"
tags:
  - skill-authoring
  - owner-facing-readouts
  - presentation-contract
  - portability
  - source-access-audit
---

# Lead portable source audits with scan lines, then an unwrapped table

## Context

A complete role-by-role source receipt still has to be recoverable in the
same response. Collapsing that census behind HTML `<details>` looks like
the accessible disclosure that keeps routine rows off the default path, but
several agent hosts do not render that widget. On those hosts the owner
either sees raw tags or never gets a collapsed default, so the condensation
fails or the markup leaks.

## Guidance

Keep two surfaces in one response, both required, neither wrapped in HTML
disclosure tags:

1. **Scan lines** after the audit heading: overall coverage, then every
   material limitation with the claim category it limits and the exact
   access result. Promote attempted failures, truncated or partial reads,
   unconfigured or declined roles, Partial or Insufficient coverage, and
   failed required rereads or readbacks. Complete, non-truncated
   **Accessed — evidence found** discovery stays out of this surface.
2. **Recovered table** immediately after: today's unwrapped GFM census of
   every relevant role, using the skill's exact result labels. Pre-write
   reread and post-write readback stay separate rows even when they share a
   source.

Do not print a spoken caption that the table is the census. Do not add a
second mini-table. Put Phase only on the recovered table for combined
action-and-discovery responses.

`personal-chief-of-staff` ships this shape in
`skills/personal-chief-of-staff/assets/review-bundle.md`. Grade it from
scan lines versus the recovered table as separate fields, not from a
collapsed disclosure.

## Why This Matters

The owner needs claim-changing gaps without opening anything. The grader
and a later reader still need every role. A host that cannot collapse HTML
must not be the reason either surface disappears.

## When to Apply

- Owner-facing skills that report source or tool access across many roles
- Any condensation that would otherwise depend on `<details>`, accordions,
  or host-specific fold widgets
- When issue text asks for a disclosure and research shows that widget is
  not portable on the skill's roster harnesses

## Examples

Before: one GFM table is the default view, so a failed mailbox row sits
beside ten successful ones.

After:

```markdown
### Source Access Audit

Coverage: Partial.
- Mailbox: Attempted — unavailable or failed — limits reply-commitment claims.

| Source or role | Result | Scope or window | Effect on claim categories |
| --- | --- | --- | --- |
| Mailbox | Attempted — unavailable or failed | current bounded window | Prevents reply-commitment claims |
| Calendar | Accessed — evidence found | current day | Supports scheduled-commitment claims |
```

## Related

- `docs/solutions/best-practices/answer-first-natural-prose-for-owner-facing-skill-readouts.md`
- `docs/solutions/conventions/keep-the-test-seam-out-of-the-shipped-skill.md`
- `CONCEPTS.md` Source Access Audit
