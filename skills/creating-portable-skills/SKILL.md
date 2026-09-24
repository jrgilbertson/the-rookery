---
name: creating-portable-skills
description: Use when creating, updating, or migrating a skill, when editing a skill's SKILL.md, evals, graders, or trigger queries, or when finding problems in its description, triggers, structure, portability, or evidence. Produces prioritized findings or a portable, installable skill package. Explanation-only requests stay with general reasoning.
license: MIT
compatibility: Full validation requires isolated agent contexts or separate sessions for agent grading and review.
---

# Creating Skills

Create, revise, migrate, or audit a skill from its intent, required outcome, and only the hard constraints that define acceptable completion or remain under user authority.

Skills produced here follow the [Agent Skills format](https://agentskills.io/specification): a directory with a `SKILL.md` (frontmatter plus body) and optional `references/`, `assets/`, and `scripts/`. Read [references/portability.md](references/portability.md) for the canonical frontmatter fields and their limits, and when choosing an install location or making a harness-specific claim. [references/skills.md](references/skills.md) is the convention for eval files, arms and runs, targets, grading, the run archive, and committed evidence; read it before steps 2, 5, 6, and 7.

An independent reviewer is any agent that took no part in the authoring discussion and did not produce the artifact under review; an agent auditing a skill it did not write already qualifies and needs no separate context. For full validation, an independent grader grades the matched cases and a different independent reviewer performs the final package review. The author never supplies a grade or review that must come from an independent context, not even provisionally or as labeled notes standing in for grades. When a required independent context is unavailable, prepare a self-contained handoff for a separate session. Until that session completes it, the grade or review stays unverified and the change does not ship; say so plainly instead of leaving shipping as the user's call.

## Workflow

Select the validation route before entering the workflow:

- **Focused validation** applies only to a localized, low-risk guidance revision with unchanged task scope, activation boundary, required outcomes, System-Owned Invariants, executable helpers, and evaluation/review policy. An optional method hint can qualify, and so can removing history phrasing, pinned model names, workarounds for a named model, unsourced hardcoded facts, or duplication when required behavior does not change; even a one-line approval, output-schema, or helper change cannot. A focused check runs each affected eval once per target with the changed skill and a blind independent grader.
- **Full validation** applies to new skills, fixes that add or change required behavior, all other substantive changes, and ambiguous eligibility. Substantive means changed instruction semantics, trigger description, or bundled resource; typo, formatting, and link-only edits remain exempt from behavioral evaluation. Moving or reformatting eval files is not a behavioral change either, because `SKILL.md` never loads `evals/`; step 4's structural checks and `scripts/check-evals.py` suffice.

A read-only audit starts and ends at step 0. Authorized focused revisions start at step 1; other existing-skill work starts at step 0, and new skills start at step 1. Existing authorization for the material fix scope carries forward.

### 0. Audit an existing skill

Have an independent reviewer apply [references/review-checklist.md](references/review-checklist.md) to the whole package and the host repository's instructions, with the inputs the checklist names, and present its prioritized fix list.

Read-only completion: deliver the evidence-backed review, prioritized recommendations, and final verdict without changing files. The execution ends there. Revision begins only in a separate user-authorized request.

Change completion: the material fix scope is authorized, including any authority or taste decisions that stay with the user. Continue at step 1 without requesting authorization already supplied.

### 1. Resolve the intent

Use the conversation, existing package, repository context, and examples already available. Ground the reusable guidance in real work: user corrections, successful task history, input and output examples, project documentation, schemas, review comments, issues, version history, and resolved failures. Establish the skill's one job, triggering conditions and near-misses, intended outcome, and observable done state, including any required artifact or handoff. Name only the hard constraints, including decisions that remain with the user; identify real environment requirements and representative examples. When a missing decision could materially change the result, scope, or authority, ask one focused question at a time; do not re-ask what the available context resolves.

Completion: the job is written as one sentence, and the triggers, near-misses, outcome, done state, hard constraints, requirements, and examples are each written down with a value or `not applicable`.

### 2. Scope targets and resources

Take the target set from the **Targets** section of [references/skills.md](references/skills.md); structural portability alone does not require expanding it. Record actual target identities and material configuration when available.

Choose only resources with repeatable value. Outputs copied by the workflow belong in `assets/`. Reference material needed only for one branch belongs in `references/`. Deterministic helpers belong in `scripts/` when prose cannot reliably protect the result. Keep the package standalone. Check the host repository's contribution docs, agent instructions, changelog policy, skill discovery path, and validators.

Completion: the target set and applicable host conventions are recorded, with a file list and one-line reason for every bundled file.

### 3. Draft

For a new skill, copy [assets/skill-template.md](assets/skill-template.md) to the host's skill discovery path or documented skill location. For a revision, preserve a loadable prior version before editing; the last commit is sufficient in a versioned repository. For a migration, copy the source package to the destination collection and revise the copy without changing the source.

Use the least-prescriptive instruction that reaches the required outcome within its hard constraints. Preserve exact formats, deterministic checks, authority boundaries, reusable resources, and genuinely fragile ordering. Let the agent choose its reasoning and implementation path elsewhere. Before drafting, read the **System-Owned Invariants**, **Information hierarchy**, **Instruction economy**, and **Portability** sections of [references/review-checklist.md](references/review-checklist.md) and apply them as authoring constraints; they also govern relaxing an existing instruction.

Completion: every file in step 2's list exists, and each hard constraint from step 1 appears in the draft.

### 4. Validate structure

Run the Agent Skills reference validator, `skills-ref validate
<skill-directory>` ([specification](https://agentskills.io/specification#validation)),
from a trusted install, and record its version and source; some published
builds name the same command `agentskills validate`. Do not use the similarly
named npm package; it is not the reference validator. If the reference
validator is not already available, either use the manual checks below or ask
before installing it from a pinned `agentskills/agentskills` commit. Manually check every field against the table in
[references/portability.md](references/portability.md), that no other field
appears, that `metadata` holds string values only, and that the body is at
most 500 lines.

Completion: the validator passes, or every named fallback check passes with the tool limitation recorded.

### 5. Check behavior

Follow the selected route in [assets/baseline-test-template.md](assets/baseline-test-template.md). [references/skills.md](references/skills.md) owns the file formats, arms and runs, grading, cost, and the ship rule the template applies. Write eval definitions to the skill's `evals/evals.json`, raw runs to the run archive, and the round's benchmark to `evals/benchmarks/`.

For full validation, before any paid run, have the independent final reviewer check eval validity: each assertion is decidable from what the grader sees, no assertion is stricter than the skill's contract, and each regression control's baseline is plausible. The reviewer also checks that the skill's rules are consistent with each other and applies the whole checklist in [references/review-checklist.md](references/review-checklist.md) to the package, with the inputs it names. Revise from its findings before the runs.

Completion: the selected route's checks have run, the eval definitions and the round's benchmark file are written, and this skill's `scripts/check-evals.py` exits 0 on the target skill directory; cosmetic-only edits record behavioral evaluation as not applicable.

### 6. Decide and review

For focused validation, directly inspect the changed guidance and actual check output against the intended outcome and hard constraints, using the applicable items in [references/review-checklist.md](references/review-checklist.md). The author may do this inspection; it is not independent evidence. A whole-package audit, matched improvement experiment, and separate final reviewer are not required.

For full validation, applying the ship rule in [references/skills.md](references/skills.md) to the graded results is a mechanical read, and the independent final reviewer confirms it. When required independent grading or review is unavailable, the independence rule at the top of this file applies; a checklist exception cannot replace it.

Any substantive follow-up edit reselects its route and returns through step 4 and the affected evals before shipping. Rerun only evals whose prompt, files, or assertions changed, or whose assertions test text the diff touches. Reuse baseline runs whose bytes did not change and keep their original revision labels; each carried-forward result names the revision it came from.

Completion: focused validation has passing structural and affected behavior checks, direct artifact inspection, and a claim limited to what was exercised; full validation has a ship decision and every checklist item passes.

### 7. Test the description

For a new skill, or whenever the description changed, follow [assets/trigger-queries-template.md](assets/trigger-queries-template.md). The trigger-eval format, run count, pass thresholds, and tuning split are in [references/skills.md](references/skills.md). A revision that leaves the description untouched skips the run.

Completion: for a new or description-changed skill, `evals/eval_queries.json` meets the thresholds in [references/skills.md](references/skills.md) and the results are recorded, with a judgment that cannot be run recorded as not run and never counted as a pass; otherwise a diff of the description against the preserved prior version is empty.

### 8. Package and install

For a new package, or a change to packaging or the install path, recheck the host conventions from step 2, confirm the canonical directory is self-contained, and run the smoke check from [assets/trigger-queries-template.md](assets/trigger-queries-template.md), which owns the install, the proof of which copy activated, and the result states, on each harness in step 2's target set. Using a user-level skill location or overwriting an existing same-name installation requires explicit user approval.

If packaging exposes a defect that changes the package, apply step 6's re-entry rule before completing this step.

Completion: the source validates, and each roster harness records a smoke pass, or a not run with the user's recorded decision to ship without it.

## Gotchas

- Check the target collection and system-provided skills for name collisions. Verb-led gerund names (`creating-portable-skills`, not `skill-creator`) are usually more specific.
- Keep a host repository's local rules, such as changelog policy, tracker choice, and CI vendor, in that repository rather than in the portable skill.
- When the skill's intent shrinks, update `evals/evals.json` and `evals/eval_queries.json` in the same change rather than leaving a one-off exception.

## Credits

The review vocabulary distills [writing-great-skills](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-great-skills) by Matt Pocock (MIT) and [writing-skills](https://github.com/obra/superpowers/blob/main/skills/writing-skills/SKILL.md) by Jesse Vincent (MIT). Format, evaluation, and description doctrine follow the [Agent Skills specification](https://agentskills.io), its skill-creation guides, and Anthropic's [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) (Apache 2.0).
