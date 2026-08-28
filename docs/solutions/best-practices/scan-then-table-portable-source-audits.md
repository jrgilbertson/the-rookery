---
title: "Lead source audits with a short coverage paragraph"
date: 2026-08-28
category: best-practices
module: personal-chief-of-staff
problem_type: best_practice
component: documentation
severity: medium
applies_when:
  - "Condensing an owner-facing source or access census without reducing coverage"
  - "HTML details would dump inner text or raw tags on markdown-only or TUI hosts"
  - "A role-by-role table would give routine successes the same weight as failures"
symptoms:
  - "A row-per-source table gives routine successes the same weight as failures"
  - "HTML details tags render as raw markup or expand fully on TUI and markdown-only hosts"
  - "An always-visible recovered table still occupies the default reading path"
tags:
  - skill-authoring
  - owner-facing-readouts
  - presentation-contract
  - source-access-audit
---

# Lead source audits with a short coverage paragraph

## Context

A complete current-response role census still has to be recoverable in the
same response. A GFM table gives every successful row the same weight as a
failure. HTML `<details>` looks like a disclosure, but markdown-only clients
and several TUI hosts dump the inner table or the tags, so the default path
is not shorter.

## Guidance

Write the Source Access Audit as a short paragraph of a few sentences. No
table, no HTML details, and no em dashes.

1. Lead with coverage: Sufficient, Partial, or Insufficient. An action-only
   response has no review coverage verdict.
2. Name every relevant role and how the read finished, in ordinary words:
   accessed with evidence, accessed with no relevant evidence, attempted
   and failed, not configured, declined, not needed.
3. Successful reads may share one sentence. A limit gets its own clause or
   sentence, with a "so" only when that result omits, qualifies, or prevents
   a claim.
4. If the roster is long, use two or three sentences: coverage and limits
   first, then the remaining successes.
5. Keep pre-write reread and post-write readback as separate operations.
   In a combined action-and-discovery response, distinguish action access
   from review or context discovery in the same paragraph.

Grade the paragraph after the heading. A correct trace does not excuse a
missing role. A named available role may not be silently omitted or labeled
not needed.

`personal-chief-of-staff` ships this shape in
`skills/personal-chief-of-staff/assets/review-bundle.md`.

## Why This Matters

The owner needs claim-changing gaps in the default reading path. The grader
and a later reader still need every role in the same raw response, including
on hosts that cannot fold HTML.

## When to Apply

- Owner-facing skills that report source or tool access across many roles
- When the skill must stay readable on markdown-only and TUI hosts
- When an always-visible table would leave routine successes on the
  default path

## Examples

Before: one GFM table is the default view, so a failed mailbox row sits
beside ten successful ones.

After:

```markdown
### Source Access Audit

Coverage is partial because the mailbox read was attempted and failed, so
there are no reply-commitment claims from this window. Calendar was accessed
with evidence for the current day.
```

## Related

- `docs/solutions/best-practices/answer-first-natural-prose-for-owner-facing-skill-readouts.md`
- `docs/solutions/conventions/keep-the-test-seam-out-of-the-shipped-skill.md`
- `CONCEPTS.md` Source Access Audit
