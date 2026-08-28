---
title: "Lead source audits with a capsule, then a details-wrapped table"
date: 2026-08-27
category: best-practices
module: personal-chief-of-staff
problem_type: best_practice
component: documentation
severity: medium
applies_when:
  - "Condensing an owner-facing source or access census without reducing coverage"
  - "Issue text requires a supported accessible disclosure in the same response"
  - "Routine successful rows would otherwise share visual weight with failures"
symptoms:
  - "A row-per-source table gives routine successes the same weight as failures"
  - "Material limits are only visible after expanding a disclosure"
  - "An always-visible recovered table still occupies the default reading path"
tags:
  - skill-authoring
  - owner-facing-readouts
  - presentation-contract
  - source-access-audit
---

# Lead source audits with a capsule, then a details-wrapped table

## Context

A complete role-by-role source receipt still has to be recoverable in the
same response. Printing that census unwrapped keeps every successful row
on the default path. HTML `<details>` is the disclosure issue 101 named.
Some TUI hosts dump the inner table or show raw tags. That residual is
accepted. The capsule still leads, so claim-changing limits are visible
without opening anything.

## Guidance

Keep two surfaces in one response, both required:

1. **Capsule** after the audit heading, outside details: overall coverage,
   then every material limitation with the claim category it limits and
   the exact access result. Promote attempted failures, truncated or
   partial reads, unconfigured or declined roles, Partial or Insufficient
   coverage, and failed required rereads or readbacks. Complete,
   non-truncated **Accessed — evidence found** discovery stays out of this
   surface.
2. **Recovered table** inside HTML `<details>` with a short summary. Leave
   it closed unless an auto-expand class is present, then add `open`:
   attempted failure, partial or truncated read, **Not configured**,
   **Declined**, Partial or Insufficient coverage, failed required reread
   or readback, or claim-changing **Accessed — no relevant evidence**. Put
   a blank line after `</summary>` and before `</details>` so the GFM
   table still parses. Pre-write reread and post-write readback stay
   separate rows even when they share a source.

Do not print a spoken caption that the table is the census. Do not add a
second mini-table. Put Phase only on the recovered table for combined
action-and-discovery responses.

`personal-chief-of-staff` ships this shape in
`skills/personal-chief-of-staff/assets/review-bundle.md`. Grade the
capsule from the text after the heading and before the first `<details>`.
Grade the table from the GFM inside details. Do not require a click.

## Why This Matters

The owner needs claim-changing gaps without opening anything. The grader
and a later reader still need every role in the same raw response,
including children of a closed details block.

## When to Apply

- Owner-facing skills that report source or tool access across many roles
- When issue text requires a supported accessible disclosure in the same
  response
- When an always-visible table would leave routine successes on the
  default path

## Examples

Before: one GFM table is the default view, so a failed mailbox row sits
beside ten successful ones.

After:

```markdown
### Source Access Audit

Coverage: Partial.
Mailbox: Attempted — unavailable or failed — limits reply-commitment claims.

<details open>
<summary>Full source receipt</summary>

| Source or role | Result | Scope or window | Effect on claim categories |
| --- | --- | --- | --- |
| Mailbox | Attempted — unavailable or failed | current bounded window | Prevents reply-commitment claims |
| Calendar | Accessed — evidence found | current day | Supports scheduled-commitment claims |

</details>
```

## Related

- `docs/solutions/best-practices/answer-first-natural-prose-for-owner-facing-skill-readouts.md`
- `docs/solutions/conventions/keep-the-test-seam-out-of-the-shipped-skill.md`
- `CONCEPTS.md` Source Access Audit
