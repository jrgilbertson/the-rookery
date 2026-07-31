---
title: Daily Meaningful Commitments - Plan
type: feat
date: 2026-07-30
topic: daily-meaningful-commitments
artifact_contract: ce-unified-plan/v1
artifact_readiness: implementation-ready
product_contract_source: ce-brainstorm
execution: code
---

# Daily Meaningful Commitments - Plan

## Goal Capsule

- **Objective:** Give wind-down a durable, lightweight way to record tomorrow's three to five most meaningful commitments and give morning a concise way to reaffirm them.
- **Product authority:** The configured Daily Journal owns reviewed daily intent, while canonical tasks own work state and calendars own reserved capacity.
- **Execution profile:** Extend the existing markdown-based Chief-of-Staff workflow and its behavioral evidence; add no parser, state machine, task mirror, or new storage layer.
- **Stop conditions:** Stop U4 if the configured template cannot be read through its authoritative interface or the proposed private edit cannot be shown exactly for approval. Stop all public work if it requires a private vault name, path, or content.
- **Tail ownership:** The public skill and regression evidence remain in this repository. The configured template remains private and is updated only as a separately approved external action.
- **Open blockers:** None.

---

## Product Contract

**Product Contract preservation:** Unchanged.

### Summary

Wind-down will preserve the existing reflective Daily Journal and add a structured section for tomorrow's three to five meaningful commitments.
Morning will briefly restate each reviewed commitment's outcome, finish line, and rationale before presenting other attention items.

### Problem Frame

The current wind-down can propose a next-day critical path and a few protected outcomes, but the configured Daily Journal has no durable place to retain them.
Broad calendar blocks such as development or meetings reserve capacity without saying which outcomes matter most.
The missing record weakens next-morning continuity and deprives later Chief-of-Staff coaching of the rationale behind the user's choices.

### Key Decisions

- **Store tomorrow's commitments in the journal completed during that evening's wind-down.** Governs R1, R5. (session-settled: user-directed — chosen over pre-creating tomorrow's note: wind-down should close the current day and carry reviewed intent forward.)
- **Use a lightweight commitment record rather than an accountability ledger.** Governs R4, R8, R13, R14. (session-settled: user-approved — chosen over copied planned-versus-actual statuses: the goal is clearer intent and coaching, not another task tracker.)
- **Keep a flexible three-to-five list with three semantic elements per commitment.** Governs R2, R3. (session-settled: user-directed — chosen over fixed slots and outcome-only bullets: flexibility fits changing capacity, while outcome, finish line, and rationale improve execution and coaching.)
- **Keep calendar capacity separate from journal intent.** Governs R12. (session-settled: user-directed — chosen over mapping commitments onto calendar blocks: the calendar should continue to reserve time without requiring one-to-one alignment.)
- **Repeat the full commitment briefly in morning.** Governs R9, R10. (session-settled: user-approved — chosen over silently using the rationale: the commitments belong in the existing daily briefing as the day's most important outcomes.)
- **Extend the existing reflection instead of adding another retrospective list.** Governs R1. (session-settled: user-directed — chosen over a paired outcome ledger or replacing What went well?: the current prompt preserves meaningful unplanned personal and relationship moments without duplicate writing.)

### Actors

- A1. The user chooses, corrects, and approves the commitments and any subjective rationale.
- A2. The personal Chief of Staff retrieves evidence, proposes commitments, reaffirms reviewed intent, and offers selective coaching.
- A3. The configured Daily Journal stores the reviewed reflection and next-day commitments without becoming the canonical task or calendar system.

### Requirements

**Journal shape and content**

- R1. The Daily Journal retains its existing retrospective reflection and gains a distinct forward-looking section for commitments governing the following day.
- R2. A completed wind-down records three to five commitments in that forward-looking section.
- R3. Every commitment naturally includes a concrete outcome, an observable finish line, and a concise rationale for why it matters, without requiring labeled subfields.
- R4. The commitment section contains no mandatory completed, changed, unfinished, score, streak, or grade fields.

**Wind-down behavior**

- R5. Wind-down proposes the commitments after considering the day's outcomes, unresolved work, known capacity, fixed commitments, current strategy, and the user's judgment.
- R6. The proposed journal and every task, calendar, communication, CRM, or repository effect remain independently approvable under the existing review-bundle rules.
- R7. Commitments use concrete results rather than activity labels such as “development,” “meetings,” or “work on X.”
- R8. When yesterday's commitment and today's outcome diverge meaningfully, wind-down may surface the difference through the existing reflection or coaching flow without requiring per-item reconciliation.

**Morning behavior and source boundaries**

- R9. Morning reads the prior reviewed commitments and briefly repeats each outcome, finish line, and rationale as the day's most important intended outcomes.
- R10. Morning preserves the reviewed list unless current evidence reveals a material conflict, invalid premise, or capacity change that warrants a user-reviewed revision.
- R11. The existing zero-to-three morning foreground limit remains a separate filter for matters requiring the user's judgment or presence and does not cap or replace the three-to-five commitment list.
- R12. The Chief of Staff does not create, rename, or map calendar blocks merely to align the calendar with the commitments.
- R13. Canonical tasks continue to own work state; commitments may refer to canonical work but do not duplicate its status or create a second task list.

**Coaching and portability**

- R14. The Chief of Staff may use prior commitment rationales and later reflections to surface recurring prioritization, sizing, carry-forward, or strategic-alignment patterns without producing a completion score.
- R15. The public skill uses an explicitly configured forward-commitment section when available and does not depend on a personal vault name, private path, or unpublished template.
- R16. When the configured template lacks a suitable forward-commitment section, the Chief of Staff preserves the existing next-day planning behavior and does not invent or write a new journal structure without separate approval.

### Key Flows

- F1. Evening commitment capture
  - **Trigger:** The user begins or resumes wind-down.
  - **Actors:** A1, A2, A3
  - **Steps:** The Chief of Staff reconstructs the day, collaborates on the existing reflection, reviews tomorrow's constraints, proposes three to five commitments under R2–R7, and presents the journal change for approval.
  - **Outcome:** The approved current-day journal contains both the day's reflection and reviewed intent for tomorrow.

- F2. Morning reaffirmation
  - **Trigger:** Morning review finds reviewed commitments in the prior Daily Journal.
  - **Actors:** A1, A2, A3
  - **Steps:** The Chief of Staff validates the commitments against current evidence, repeats the three elements concisely, and proposes a revision only under R10.
  - **Outcome:** The user begins with a stable account of the day's intended outcomes before considering separate foreground items.

- F3. Reflective coaching
  - **Trigger:** A later wind-down, weekly review, or other owned review finds a repeated pattern across commitments and reflections.
  - **Actors:** A1, A2
  - **Steps:** The Chief of Staff distinguishes observed history from inference, offers the pattern for correction or discussion, and avoids mechanical scoring under R14.
  - **Outcome:** The user receives coaching grounded in both chosen rationale and subsequent experience.

### Acceptance Examples

- AE1. **Covers R2, R3, R5, R7.** Given tomorrow has mixed fixed commitments and flexible capacity, when wind-down prepares the journal, then it proposes three to five concrete outcomes and gives each an observable finish line and short rationale.
- AE2. **Covers R3, R7.** Given a candidate commitment says “Dev,” when the Chief of Staff prepares the list, then it collaborates on a finishable result rather than preserving the activity label.
- AE3. **Covers R4, R8, R14.** Given one prior commitment did not happen, when wind-down reviews the day, then it discusses the divergence only when meaningful and does not add mandatory status fields or a completion score.
- AE4. **Covers R9, R10.** Given the prior journal contains four reviewed commitments and nothing material changed overnight, when morning runs, then it briefly repeats all four with their outcome, finish line, and rationale without reprioritizing them.
- AE5. **Covers R6, R10.** Given overnight evidence invalidates one commitment, when morning runs, then it explains the conflict and keeps any journal, task, or calendar change separately reviewable.
- AE6. **Covers R11.** Given morning finds four reviewed commitments but no matter requiring the user's judgment, when it prepares the briefing, then it repeats the four commitments and returns zero foreground attention items.
- AE7. **Covers R12, R13.** Given the calendar contains a broad development block and a commitment refers to canonical work, when morning reaffirms the commitment, then it neither renames the block nor duplicates the task's status.
- AE8. **Covers R15, R16.** Given another user's configured template lacks a forward-commitment section, when wind-down runs, then the public skill preserves its existing planning behavior and does not write a personal template convention without approval.

### Success Criteria

- A completed wind-down with the configured forward section leaves three to five reviewed commitments whose three fields are specific enough to guide action the next day.
- Morning recovers and restates the prior intent without silently regenerating it or conflating it with foreground attention items.
- The existing journal continues to support reflective personal, relationship, and unplanned meaning without duplicate retrospective entry.
- Later coaching can cite the user's stated rationale and observed reflection while remaining non-scoring and user-correctable.
- The public skill remains installable and useful without access to any personal vault name, path, or private template.

### Scope Boundaries

- No per-item completion ledger, productivity grade, streak, synthetic score, or mandatory retrospective reconciliation.
- No automatic calendar creation, renaming, rescheduling, or commitment-to-block mapping.
- No replacement for canonical tasks, due dates, project records, or waiting context.
- No pre-creation of tomorrow's Daily Journal as part of wind-down.
- No broad redesign of the Pulse, reflection prompts, vault-activity views, weekly review, or quarterly review.

### Dependencies and Assumptions

- The configured note system exposes the Daily Journal template and prior journal through its authoritative interface.
- The private template can be updated through that interface without storing its path or contents in this public repository.
- Existing review-bundle approval, source ownership, and readback rules remain authoritative.

### Sources

- `skills/personal-chief-of-staff/references/wind-down.md` — current journal, source-reconciliation, and tomorrow-planning behavior.
- `skills/personal-chief-of-staff/references/morning.md` — prior-intent consumption and the separate foreground-attention limit.
- `skills/personal-chief-of-staff/references/source-behavior.md` — canonical ownership, approval, portability, and authoritative-interface rules.
- `skills/personal-chief-of-staff/assets/review-bundle.md` — independently approvable review shape.
- `tests/personal-chief-of-staff/cases/` — runnable behavioral cases and adjacent regression coverage.

---

## Planning Contract

### Key Technical Decisions

- KTD1. **Use plain Markdown as the complete commitment record.** A configured `Tomorrow’s Meaningful Commitments` section contains three to five numbered bullets. Each bullet uses one to three sentences that naturally combine the concrete outcome, observable finish line, and rationale without literal subfield labels. The records use no task checkboxes, hidden metadata, parser, or lifecycle fields. (session-settled: user-directed — chosen over a commitment state model: durable nightly evidence is sufficient and easier to inspect.) Governs R1-R4, R7, R13, R15-R16.
- KTD2. **Treat the nightly journal as append-only historical intent.** Morning reads the immediately previous local-date journal and repeats its commitment records. If current evidence materially conflicts, morning shows the original commitment, the new evidence, and the current recommendation without rewriting the prior journal or persisting an amended commitment state. (session-settled: user-approved — chosen over persisted morning amendments: preserve durable evidence without introducing a state machine.) Governs R9-R10.
- KTD3. **Extend existing source and approval behavior.** Wind-down uses the configured-template and current-journal reads, subjective-content approval, narrow merge, approval-time revalidation, and readback rules already defined by the skill. Each bullet's rationale is proposed or captured as subjective content and requires the user's approval. Governs R3, R5-R6, R15-R16.
- KTD4. **Keep commitments separate from task, calendar, and foreground state.** Commitments are briefing context. They neither consume the zero-to-three foreground limit nor cause task duplication, calendar renaming, or calendar mapping. Governs R11-R13.
- KTD5. **Add only a narrow coaching seam.** Wind-down or weekly review may compare prior rationales with later reflections when the repeated pattern is decision-useful. The output distinguishes evidence from inference and adds no score, streak, or reconciliation ledger. Governs R8, R14.
- KTD6. **Verify behavior, not unchanged discovery metadata.** Use focused prior-versus-candidate cases, independent fresh-context review, structural validation, and a public/private boundary scan. Do not rerun broad trigger-listing coverage while `SKILL.md` description and trigger contract remain byte-identical. (session-settled: user-directed — chosen over broad public-tier retesting: the change is behavioral, so durable behavioral evidence is the load-bearing proof.)

### Existing Patterns to Extend

- `skills/personal-chief-of-staff/references/wind-down.md` already owns configured-template discovery, subjective approval, source separation, next-day planning, narrow Obsidian writes, and readback.
- `skills/personal-chief-of-staff/references/morning.md` already reads prior reviewed intent before applying the separate foreground-attention limit.
- `skills/personal-chief-of-staff/references/weekly.md` already reads Daily Journals and discusses divergence between intention and observed behavior.
- `skills/personal-chief-of-staff/references/source-behavior.md` remains authoritative for configured-role discovery, separate approvals, drift revalidation, CLI-only mutation, and indeterminate readback handling.
- `tests/personal-chief-of-staff/cases/` and `tests/personal-chief-of-staff/log.md` are the repository's behavioral specification and durable evaluation record.

### Implementation Constraints

- Resolve the Daily Journal template and journals by configured canonical role. Do not hard-code a personal vault, note path, or private template content.
- Use the exact generic section heading and natural bullet shape from KTD1 as the opt-in convention. If the live template does not contain that section, preserve the existing next-day planning behavior and do not invent a journal structure.
- Do not reuse an older journal after a missed day. Morning reads only the immediately previous local-date journal for commitments intended for the current local date.
- If wind-down runs after midnight and the journal date is ambiguous, resolve the intended journal date before drafting commitments.
- Do not silently pad, truncate, normalize, or invent fields in user-authored records. Collaborate toward R2-R3 and preserve an explicit user override as nonconforming source content.
- Keep scheduled morning and wind-down runs read-only until the user approves each source mutation.
- If approval-time content drift or an indeterminate write occurs, follow the existing revalidation and readback rules. Never repeat an indeterminate write.

### Sequencing

1. Define the public wind-down, morning, and narrow coaching behavior against the existing source and approval contracts.
2. Add matched behavioral cases and evaluate the candidate skill in fresh contexts before changing the private template.
3. Update the private configured template as a separate approved action and verify it through the same authoritative interface.

### Risks and Mitigations

- **Activity labels masquerade as commitments.** Operationalize a meaningful commitment as an outcome with an observable finish line; require revision of labels such as `Dev` or `Meetings` before calling the section conformant.
- **Morning turns into a second planning system.** Preserve the nightly record, explain material new evidence, and leave persistence to canonical tasks, calendars, or the next wind-down.
- **Private configuration leaks into the public repository.** Keep external source identifiers and content out of fixtures, results, plans, and command transcripts; run the repository's same-door review before completion.
- **A template edit damages manual content.** Use a narrow approved insertion with pre-read, approval-time re-read, and post-write readback; preserve frontmatter, reflections, links, embeds, and vault-activity views.
- **Fresh-context evidence runs against the wrong skill copy.** Verify local-source installation identity before accepting native-harness results.

---

## Implementation Units

### U1. Capture meaningful commitments during wind-down

- **Goal:** Extend wind-down so the approved current-day journal records tomorrow's reviewed intent in the configured section.
- **Requirements:** R1-R8, R12-R13, R15-R16; KTD1, KTD3, KTD4.
- **Files:** `skills/personal-chief-of-staff/references/wind-down.md`.
- **Approach:** Extend the existing `Prepare tomorrow` and journal-update behavior. Read the live template and current journal, draft three to five concrete records, treat every rationale as subjective content, and present the journal merge independently from task, calendar, communication, CRM, or repository actions. Use the existing narrow-write, drift-revalidation, and readback pattern. Preserve ordinary next-day planning when the configured section is absent.
- **Patterns:** Follow configured-template discovery, subjective approval, source separation, and approved Obsidian update behavior in the same reference.
- **Test scenarios:**
  - Given mixed fixed commitments and flexible capacity, propose four records whose outcomes are concrete, whose finish lines are observable, and whose rationales connect to strategy, obligation, or avoided cost.
  - Given a candidate labeled `Dev`, collaborate toward a finishable outcome instead of writing the activity label.
  - Given an existing journal created before template enablement, add the configured section through one approved narrow merge while preserving manual prose, frontmatter, links, embeds, and views.
  - Given a configured template without the section, keep the existing protected-outcomes planning and make no journal-structure write.
  - Given approval-time section drift, discard the stale proposal and present a revised one.
  - Given an indeterminate write, retry only readback and never repeat the write.
- **Verification:** Matched fresh-context wind-down cases show the proposal, approval boundary, preservation behavior, and fallback without task or calendar side effects.

### U2. Reaffirm intent in morning and support selective coaching

- **Goal:** Make the prior night's commitments the first durable intent context in morning while preserving history and the existing foreground limit.
- **Requirements:** R8-R14; KTD2, KTD4, KTD5.
- **Files:** `skills/personal-chief-of-staff/references/morning.md`, `skills/personal-chief-of-staff/references/weekly.md`.
- **Approach:** Add a compact commitment surface before foreground attention items. Read only the immediately previous local-date journal, repeat every valid bullet and its outcome, finish line, and rationale, and leave the prior journal unchanged. When current evidence invalidates a commitment, explain the evidence and current recommendation without persisting commitment state. Add one narrow coaching rule to the existing weekly or wind-down reflection path for repeated rationale-versus-outcome patterns.
- **Patterns:** Follow prior-intent recovery and missing-journal handling in morning, and evidence-versus-inference language in weekly review.
- **Test scenarios:**
  - Given four valid commitments and no material overnight change, repeat all four with their outcome, finish line, and rationale and return zero foreground items when none require judgment.
  - Given commitments plus three foreground matters, keep the two surfaces visually distinct and retain all items.
  - Given overnight evidence that invalidates one commitment, preserve the historical wording, explain the conflict, and offer a current recommendation without rewriting the journal or reordering the unaffected records.
  - Given no immediately previous journal but an older journal with commitments, do not revive the stale list.
  - Given an absent, empty, partial, or malformed section, continue the briefing without inventing outcomes or rationales.
  - Given repeated cross-day evidence that stated rationales and observed outcomes diverge, offer a sourced, user-correctable coaching observation with no score or mandatory reconciliation.
- **Verification:** Matched fresh-context morning and coaching cases demonstrate faithful restatement, date anchoring, conflict explanation, graceful degradation, and non-scoring coaching.

### U3. Record durable public verification and documentation

- **Goal:** Make the changed behavior reviewable and reproducible without capturing private configuration.
- **Requirements:** All requirements; KTD6.
- **Files:** `tests/personal-chief-of-staff/cases/`, `tests/personal-chief-of-staff/log.md`, `CONCEPTS.md`, `CHANGELOG.md`.
- **Approach:** Add the focused scenarios from U1-U2 to the behavioral specification. Run matched prior-versus-candidate evaluations in independent fresh contexts and append dated evidence with harness, model, loaded-package identity, result, and limitations. Keep the existing `Meaningful Commitment` glossary entry and record the user-visible workflow change. State that trigger-listing evidence was not rerun because the skill description and trigger boundary did not change.
- **Test scenarios:**
  - Candidate outputs satisfy each new scenario while prior outputs establish the changed behavior rather than merely a favorable one-off sample.
  - A bare or differently configured environment does not invent the configured section or any private convention.
  - The recorded result identifies the exact local skill revision used by the evaluator.
  - Public artifacts contain no private vault name, path, or copied template content.
- **Verification:** Structural validation passes, links remain valid, changed markdown has no whitespace errors, the local-source install matches the candidate content, and the durable results record is complete.

### U4. Enable the private Daily Journal template

- **Goal:** Add the forward-looking section to the configured template without placing private artifacts in the repository.
- **Requirements:** R1-R4, R6, R15-R16; KTD1, KTD3.
- **Files:** External configured Daily Journal template; no repository path.
- **Dependencies:** U1-U3.
- **Approach:** Through the authoritative Obsidian interface, pre-read the configured template with explicit vault targeting, propose the exact insertion location and narrow change for approval, re-read before applying, and read back after the write. If the section is already present, report `Already satisfied`. If the interface cannot safely edit or read back the template, classify only this external action as manual or partial; do not use direct filesystem access.
- **Test scenarios:**
  - Approved insertion creates the heading and natural one-to-three-sentence bullet shape while preserving all existing template content.
  - Approval-time drift produces a revised proposal rather than a stale write.
  - An unavailable or indeterminate interface produces no repeated or alternative filesystem write.
  - No live Daily Journal is written merely to test the template migration.
- **Verification:** Pre-read, approved mutation, and post-read use the same explicit target and show the exact section present with surrounding content preserved; no private output is copied into repository artifacts.

---

## Verification Contract

| Gate | Applies to | Required evidence |
|---|---|---|
| `npx skills-ref validate skills/personal-chief-of-staff` | U1-U3 | The skill package validates successfully after public edits. |
| `git diff --check` | U1-U3 | Changed repository files contain no whitespace errors. |
| Matched fresh-context behavioral evaluation | U1-U3 | Prior and candidate skill revisions are evaluated against every new substantive scenario; an independent context judges the outputs against the acceptance criteria. |
| Local-source identity and native load | U3 | The installed package matches the candidate source before native discovery/load evidence is accepted. Trigger-listing coverage is documented as unchanged when `SKILL.md` metadata is byte-identical. |
| Same-door review | U1-U4 | Public skill, tests, automation configuration, glossary, changelog, and this plan contain no private source identifiers or copied template content. |
| Obsidian pre-read and readback | U4 | The separately approved private edit is applied through the authoritative interface and surrounding template content remains intact. |

Any substantive instruction edit after evaluation invalidates the affected prior-versus-candidate cell and requires that cell to run again. Structural validation alone cannot satisfy the behavioral gate.

---

## Definition of Done

- U1 is done when wind-down proposes and, only after approval, stores three to five plain-Markdown commitments in the configured section while preserving existing journal content and all source boundaries.
- U2 is done when morning faithfully restates the immediately prior night's records, explains material changes without rewriting history, keeps commitments outside the foreground cap, and supports narrow non-scoring coaching.
- U3 is done when the focused regression cases, fresh-context results, glossary, and changelog provide durable public evidence and all repository validation gates pass.
- U4 is done when the configured template contains the approved section and natural bullet guidance, authoritative readback confirms surrounding content is preserved, and no private detail enters the repository.
- The implementation adds no commitment parser, lifecycle state, duplicated task status, calendar synchronization, or agent-only store.
- All temporary install targets, evaluation scratch files, and abandoned experimental edits are removed before completion.
- The final diff contains only the intended public source, behavioral evidence, glossary, changelog, and plan changes; the private template remains outside version control.
