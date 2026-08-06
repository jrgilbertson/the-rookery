---
title: Wind-down needs a required day-window CRM scan, not candidate-triggered only
date: 2026-08-06
category: workflow-issues
module: personal-chief-of-staff managing-personal-crm
problem_type: workflow_issue
component: development_workflow
severity: medium
applies_when:
  - "Designing wind-down or other daily close relationship coverage"
  - "Balancing smallest-slice source rules against proactive relationship management"
  - "Evaluating Apple Messages group threads for contact-date outcomes"
tags:
  - daily-crm-scan
  - wind-down
  - personal-crm
  - agent-skills
  - smallest-slice
---

# Wind-down needs a required day-window CRM scan, not candidate-triggered only

## Context

Wind-down already captured relationship effects when the day's evidence or the user's reflection named a substantive direct interaction, and it already ran a separate cadence / useful-tomorrow exception check. Shared source rules also preferred the smallest slice that confirms a candidate. Together that meant relationship sources such as Apple Messages could be skipped when nothing else first identified a person. A same-day group exchange with a bindable speaker could never enter the review.

## Guidance

1. **Required day-window coverage.** When the CRM companion is available, wind-down finishes a **Daily CRM Scan** before the initial reconstruction. Default window is the closing local day. After a short miss (one or two immediately prior missing daily journals), expand over those days plus the closing day as a catch-up breath—not CRM catch-up mode.
2. **Companion owns adapters.** CoS requires coverage; the companion loads Messages (`apple-messages-cli.md`) and X adapters before those queries. Do not treat `imsg` as CoS-owned tooling outside that path.
3. **Per-person in groups.** Attribute by sender handle. Evaluate substantive direct contact (including targeted group participation and unanswered outgoing directed attempts) for each bindable person under the relationship contract. Unknown handles stay unresolved.
4. **Union of paths.** Scan results plus non-scan day evidence (calendar/meetings) plus reflection-missed contacts all feed the same evaluation rules. Keep prepare-tomorrow cadence exceptions separate.
5. **Smallest-slice exception.** A caller-required day-window scan covers each configured relationship source for the window first, then keeps per-conversation history narrow. Catch-up breadth stays catch-up-only.
6. **Safety unchanged.** Zero effects is valid. No durable writes while preparing the wind-down bundle. No nested CRM bundle.

## Why This Matters

Candidate-triggered-only reads quietly drop real relationship work on busy days that live mostly in Messages. A named, bounded Daily CRM Scan restores proactive coverage without opening exhaustive history or catch-up import.

## When to Apply

- Adding or revising wind-down relationship behavior
- Reconciling "smallest source slice" with daily relationship management
- Designing Messages day-window enumeration vs catch-up breadth probes

## Examples

**Before:** Wind-down only evaluated CRM after calendar, mailbox, or reflection named a person. A bindable speaker in a same-day group Messages thread could be missed.

**After:** Daily CRM Scan runs first for the closing day (or short-miss window), attributes group messages by sender, proposes contact-date for bindable speakers when contact is substantive, and leaves unbound handles unresolved.

**Short miss:** Missing yesterday's journal expands the scan over yesterday ∪ today so a yesterday-only exchange still yields a contact-date outcome without CRM catch-up inventory.

## Related

- Issue: https://github.com/jrgilbertson/the-rookery/issues/34
- Plan: `docs/plans/2026-08-06-001-feat-full-crm-scan-during-wind-down-plan.md`
- Skill owners: `skills/personal-chief-of-staff/references/wind-down.md`, `skills/managing-personal-crm/references/apple-messages-cli.md`
- Discriminator case: `tests/personal-chief-of-staff/cases/wind-down-daily-crm-scan.md`
