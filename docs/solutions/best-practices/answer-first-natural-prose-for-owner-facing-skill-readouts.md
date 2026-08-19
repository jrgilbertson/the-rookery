---
module: checking-merge-readiness
date: 2026-08-04
problem_type: best_practice
component: documentation
severity: medium
applies_when:
  - "Authoring or retuning an owner-facing skill that ends in a recommendation or decision"
  - "Readouts feel like report templates, bullet catalogs, or soft stop labels that do not name next work"
  - "Battery or review rounds keep asking for clearer merge decisions"
symptoms:
  - "Owner digests bury the recommendation under themes, drift, and driver tables"
  - "Medium risk is labeled pause, so the owner idles instead of investigating"
  - "Em dashes and section headers (Themes / Intent / Risk) make prose feel like a form"
  - "Redundant PR state labels such as (open) on every pre-merge review"
root_cause: inadequate_documentation
resolution_type: documentation_update
related_components:
  - testing_framework
tags:
  - skill-authoring
  - owner-facing-readouts
  - minto-pyramid
  - presentation-contract
  - checking-merge-readiness
---

# Answer-first natural prose for owner-facing skill readouts

## Context

`checking-merge-readiness` already graded drivers and mapped them to three
lights, but the spoken digest still read bottom-up: themes, then drift, then
risk, then the verdict. Medium risk was framed as pause, which sounds like
stop-and-wait. Real owner digests stayed long even when the judgment was
green.

The conciseness pass on branch
`jrgilbertson/Merge-readiness-conciseness` rewrote the presentation contract
and re-ran the skilled battery with a blind re-grade.

## Guidance

When a skill briefs an owner at a decision point:

1. **Pyramid as logic, not labels.** Lead with the recommendation. Follow
   with the reasons that support it in continuous sentences. Put evidence
   only under concerns that drove the call. Do not print section headers
   such as Themes, Intent, Risk, or Drivers.
2. **Name next work, not idle states.** Prefer **debug** (investigate or fix
   the named concern) over **pause** when medium risk or a cap removes
   merge. Keep **do not merge** as a hard stop on shipping; that path still
   offers debug or redesign, not a soft wait.
3. **Operationalize length and register.** Cap clean-green digests with a
   checkable bound (for example about twelve non-blank short lines). Ban
   em dashes in spoken prose; use commas, periods, colons, or parentheses.
   Omit bare open PR state when the digests are pre-merge; name draft,
   merged, or closed when those apply.
4. **Prove with the production path.** Update battery checklists for the
   new shape, run skilled digests through the real fetch path, then blind
   re-grade so presentation contracts are not author-graded only.

## Related

- Plan: `docs/plans/2026-08-04-002-refactor-merge-readiness-conciseness-plan.md`
- Skill: `skills/checking-merge-readiness/SKILL.md` step 5
- Battery log: `tests/checking-merge-readiness/log.md` (conciseness and
  blind re-grade sections)
