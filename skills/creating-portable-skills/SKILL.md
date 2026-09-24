---
name: creating-portable-skills
description: Use when creating, updating, or migrating a skill, when editing a skill's SKILL.md, evals, graders, or trigger queries, or when finding problems in its description, triggers, structure, portability, or evidence. Produces prioritized findings or a portable, installable skill package. Explanation-only requests stay with general reasoning.
license: MIT
compatibility: Requires isolated agent contexts or separate sessions for agent grading and review.
---

# Creating Skills

Create, revise, migrate, or audit a skill from its intent, required outcome, and only the hard constraints that define acceptable completion or remain under user authority. The result is either a prioritized read-only audit or a self-contained skill package with structural validation, behavioral evidence, and separate trigger and installation checks.

Skills produced here follow the [Agent Skills format](https://agentskills.io/specification): a directory with a `SKILL.md` (frontmatter plus body) and optional `references/`, `assets/`, and `scripts/`. Read [references/portability.md](references/portability.md) for the canonical frontmatter fields and their limits, and when choosing an install location or making a harness-specific claim.

An independent reviewer is any agent that took no part in the authoring discussion and did not produce the artifact under review; an agent auditing a skill it did not write already qualifies and needs no separate context. For a new skill or a substantive change, an independent grader grades the matched cases and a different independent reviewer performs the final package review. When only the author's context is available, prepare a self-contained handoff for a separate session; that grade or review stays unverified until the session completes it, because the author's own review never substitutes.

## Workflow

Creating a new skill starts at step 1. Auditing, updating, or migrating an existing skill starts at step 0. A read-only audit ends at step 0; approved changes continue through the remaining workflow.

### 0. Audit an existing skill

Have an independent reviewer read the whole package and the host repository's instructions. Give it the skill, the review checklist, and the stated intent. Have it apply [references/review-checklist.md](references/review-checklist.md) top to bottom, starting with the mechanical pre-check that [scripts/signal-scan.sh](scripts/signal-scan.sh) performs, then present its prioritized fix list.

Read-only completion: deliver the evidence-backed review, prioritized recommendations, and final verdict without changing files. The execution ends there. Revision begins only in a separate user-authorized request.

Change completion: the user has approved the material fix scope, including any authority or taste decisions that stay with them. Continue at step 1.

### 1. Resolve the intent

Use the conversation, existing package, repository context, and examples already available. Ground the reusable guidance in real work: user corrections, successful task history, input and output examples, project documentation, schemas, review comments, issues, version history, and resolved failures. Establish the skill's one job, triggering conditions and near-misses, intended outcome, and observable done state, including any required artifact or handoff. Name only the hard constraints, including decisions that remain with the user; identify real environment requirements and representative examples. When a missing decision could materially change the result, scope, or authority, ask one focused question at a time; do not re-ask what the available context resolves.

Completion: the job is written as one sentence, and the triggers, near-misses, outcome, done state, hard constraints, requirements, and examples are each written down with a value or `not applicable`.

### 2. Scope targets and resources

Use the caller-declared model and harness target set. When none is declared, use the current model and harness as one target; structural portability alone does not require expanding the set. The declared harnesses scope the step 8 smoke roster; behavioral comparisons run on the current model and on any other target the caller names. Record actual target identities and material configuration when available.

Choose only resources with repeatable value. Outputs copied by the workflow belong in `assets/`. Reference material needed only for one branch belongs in `references/`. Deterministic helpers belong in `scripts/` when prose cannot reliably protect the result. Keep the package standalone. Check the host repository's contribution docs, agent instructions, changelog policy, skill discovery path, and validators.

Completion: the target set and applicable host conventions are recorded, with a file list and one-line reason for every bundled file.

### 3. Draft

For a new skill, copy [assets/skill-template.md](assets/skill-template.md) to the host's skill discovery path or documented skill location. For a revision, preserve a loadable prior version before editing; the last commit is sufficient in a versioned repository. For a migration, copy the source package to the destination collection and revise the copy without changing the source.

Use the least-prescriptive instruction that reaches the required outcome within its hard constraints. Read the System-Owned Invariants and candidate qualifier rules in [references/review-checklist.md](references/review-checklist.md) before relaxing an existing instruction. Preserve exact formats, deterministic checks, authority boundaries, reusable resources, and genuinely fragile ordering. Let the agent choose its reasoning and implementation path elsewhere.

Before drafting, read the **Information hierarchy**, **Instruction economy**, and **Portability** sections of [references/review-checklist.md](references/review-checklist.md) and apply them as authoring constraints.

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

### 5. Compare behavior

Follow [assets/baseline-test-template.md](assets/baseline-test-template.md) for every change it defines as substantive, a description-only change included. It owns case construction, regression controls, the matched pair, grading, cost, and the ship decision. Emit the case files and log lines to the host's test location (`tests/<skill-name>/` when no convention exists).

Completion: the template's compare step has run for every substantive change, and the case files and log lines are emitted.

### 6. Decide and review

Have an independent reviewer apply the baseline comparison's decision rule, then run [references/review-checklist.md](references/review-checklist.md) top to bottom. Give the reviewer the skill, intended outcome, hard constraints, artifacts, traces, and graded case results, and revise from its findings. Any substantive follow-up edit returns through structural validation and the affected cases before shipping.

Completion: the baseline comparison has a ship or return-to-correction decision, and every checklist item passes.

### 7. Test the description

For a new skill, or whenever the description changed, follow [assets/trigger-queries-template.md](assets/trigger-queries-template.md) for the query set, judging, thresholds, and tuning. A revision that leaves the description untouched skips the run.

Completion: for a new or description-changed skill, the template's thresholds are met and the results are logged, with a judgment that cannot be run recorded as not run and never counted as a pass; otherwise a diff of the description against the preserved prior version is empty.

### 8. Package and install

For a new package, or a change to packaging or the install path, recheck the host conventions from step 2, confirm the canonical directory is self-contained, and run the smoke check from [assets/trigger-queries-template.md](assets/trigger-queries-template.md), which owns the install, the proof of which copy activated, and the result states, on each harness in step 2's target set. Using a user-level skill location or overwriting an existing same-name installation requires explicit user approval.

If packaging exposes a defect that changes the package, apply step 6's re-entry rule before completing this step.

Completion: the source validates, and each roster harness logs a smoke pass, or a not run with the user's logged decision to ship without it.

## Gotchas

- Check the target collection and system-provided skills for name collisions. Verb-led gerund names (`creating-portable-skills`, not `skill-creator`) are usually more specific.
- Do not encode a host repository's local rules into a portable skill. Changelog policy, tracker choice, and CI vendor stay in that repository.
- When the skill's intent shrinks, update evals, cases, and trigger queries in the same change rather than leaving a one-off exception.

## Credits

The review vocabulary distills [writing-great-skills](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-great-skills) by Matt Pocock (MIT) and [writing-skills](https://github.com/obra/superpowers/blob/main/skills/writing-skills/SKILL.md) by Jesse Vincent (MIT). Format, evaluation, and description doctrine follow the [Agent Skills specification](https://agentskills.io), its skill-creation guides, and Anthropic's [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) (Apache 2.0).
