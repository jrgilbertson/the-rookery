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
  - checking-pr-readiness
last_updated: 2026-08-31
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
5. **Close coverage without a census.** After the reasons, say gather
   completed and every applicable check is verified, not applicable, or
   named as next work. Incomplete gather cannot offer Approve or recommend
   merge. A check named as next work does not by itself withhold Approve.
   Do not print a status-word inventory or a sweep-class table.
6. **List only live options.** Print currently available numbered options
   after the brief. Name a check or path in the brief only when it drives
   the recommendation. A non-terminal Show the checks option lists each
   applicable check and its status from the captured gather, then the
   brief and menu again. Omit it when there is no captured gather.

The end-of-run API (menu, wait, later `1`) is a separate contract. See
[Do not split human and agent skill products](../conventions/do-not-split-human-and-agent-skill-products.md).

## Related

- Implementation: [pull request #33](https://github.com/jrgilbertson/the-rookery/pull/33)
- Skills: `skills/checking-merge-readiness/SKILL.md` step 6,
  `skills/checking-pr-readiness/SKILL.md` step 7
- [Do not split human and agent skill products](../conventions/do-not-split-human-and-agent-skill-products.md) — end-of-run API (menu and wait), not pyramid shape
- Battery log: `tests/checking-merge-readiness/log.md` (conciseness and
  blind re-grade sections)
