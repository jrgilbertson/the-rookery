---
name: creating-portable-skills
description: Use when creating, updating, or migrating an Agent Skill, or when finding problems in its description, triggers, structure, portability, or evidence. Produces prioritized findings or a portable, installable Agent Skills package. Explanation-only requests stay with general reasoning.
license: MIT
compatibility: Requires isolated agent contexts or separate sessions for agent grading and review.
---

# Creating Skills

Create, revise, migrate, or audit a skill from its intent, required outcome, and only the hard constraints that define acceptable completion or remain under user authority. The result is either a prioritized read-only audit or a self-contained Agent Skills package with structural validation, appropriately scoped behavioral evidence, and separate trigger and installation checks.

Skills produced here follow the [Agent Skills format](https://agentskills.io/specification): a directory with a `SKILL.md` (frontmatter plus body) and optional `references/`, `assets/`, and `scripts/`. Canonical frontmatter uses only `name`, `description`, `license`, `compatibility`, and `metadata`. Read [references/portability.md](references/portability.md) when authoring frontmatter, choosing an install location, or making a harness-specific claim.

An independent reviewer must not have participated in the authoring discussion or produced the artifact under review. One independent grader inspects each matched case; a different fresh-context reviewer performs the final package review. If the current environment cannot start those independent contexts, prepare a self-contained handoff for a separate session and keep the affected grade or review unverified until that session completes it. Do not substitute the author's own review.

## Workflow

Creating a new skill starts at step 1. Auditing, updating, or migrating an existing skill starts at step 0. A read-only audit ends at step 0; approved changes continue through the remaining workflow.

### 0. Audit an existing skill

Have a separate fresh-context agent that has not participated in the current authoring work read the whole package and the host repository's instructions. Give it the skill, the review checklist, and the stated intent without the author's conclusions. Have it apply [references/review-checklist.md](references/review-checklist.md) top to bottom, then present a prioritized fix list where each item names the problem, impact, and change risk.

Read-only completion: deliver the evidence-backed review, prioritized recommendations, and final verdict without changing files. The execution ends there. Revision begins only in a separate user-authorized request.

Change completion: the user has approved the material fix scope, including any authority or taste decisions that stay with them. Continue at step 1.

### 1. Resolve the intent

Use the conversation, existing package, repository context, and examples already available. Ground the reusable guidance in real work: user corrections, successful task history, input and output examples, project documentation, schemas, review comments, issues, version history, and resolved failures. Establish the skill's one job, triggering conditions and near-misses, intended outcome, and observable done state, including any required artifact or handoff. Name only the hard constraints, including decisions that remain with the user; identify real environment requirements and representative examples. When a missing decision could materially change the result, scope, or authority, ask one focused question at a time; do not re-ask what the available context resolves.

Completion: the job fits one sentence, and the triggers, near-misses, outcome, done state, hard constraints, requirements, and examples are known or explicitly not applicable.

### 2. Scope targets and resources

Use the caller-declared model and harness target set. When none is declared, use the current model and harness as one target; structural portability alone does not require expanding the set. Record actual target identities and material configuration when available.

Choose only resources with repeatable value. Outputs copied by the workflow belong in `assets/`. Reference material needed only for one branch belongs in `references/`. Deterministic helpers belong in `scripts/` when prose cannot reliably protect the result. Keep the package standalone. Check the host repository's contribution docs, agent instructions, changelog policy, skill discovery path, and validators.

Completion: the target set and applicable host conventions are recorded, with a file list and one-line reason for every bundled file.

### 3. Draft

For a new skill, copy [assets/skill-template.md](assets/skill-template.md) to the host's skill discovery path or documented skill location. For a revision, preserve a loadable prior version before editing; the last commit is sufficient in a versioned repository. For a migration, copy the source package to the destination collection and revise the copy without changing the source.

Use the least-prescriptive instruction that reaches the required outcome within its hard constraints. Read the System-Owned Invariants and candidate qualifier rules in [references/review-checklist.md](references/review-checklist.md) before relaxing an existing instruction. Preserve exact formats, deterministic checks, authority boundaries, reusable resources, and genuinely fragile ordering. Let the agent choose its reasoning and implementation path elsewhere. If the skill names several tools or approaches, give a default or a selection rule instead of an equal menu. Add a concise example only when it resolves a real ambiguity or demonstrates an exact format.

Before drafting, read the **Information hierarchy** and **Portability** sections of [references/review-checklist.md](references/review-checklist.md) and apply them as authoring constraints.

Completion: the draft and every planned resource implement the intent and required outcome with every System-Owned Invariant protected.

### 4. Validate structure

Run `npx skills-ref validate <skill-directory>`. If it cannot run because the environment lacks Node or network access, state that limitation and manually check: `name` is at most 64 characters, lowercase kebab-case, has no leading, trailing, or consecutive hyphens, and matches the directory; `description` is 1 to 1024 characters; the body is at most 500 lines; frontmatter uses only the canonical fields; `compatibility`, when present, is at most 500 characters; and `metadata`, when present, contains string values only.

Completion: the validator passes, or every named fallback check passes with the tool limitation recorded.

### 5. Compare behavior

Treat changed instruction semantics, a changed trigger description, or a changed bundled resource as substantive; typo, formatting, and link-only edits are exempt. Follow [assets/baseline-test-template.md](assets/baseline-test-template.md): declare a small discriminating case set, run matched with/without pairs in fresh contexts, grade binary through an independent grader, and emit the durable case files and log lines to the host's test location (`tests/<skill-name>/` when no convention exists). For a change limited to description or trigger routing, compare unforced activation on the trigger set instead of forced-load behavior.

Completion: every substantive change is covered by graded discriminating cases showing the intended improvement with no regression, and the case files and log lines are emitted.

### 6. Decide and review

Have a separate fresh-context agent apply the baseline comparison's decision rule, then run [references/review-checklist.md](references/review-checklist.md) top to bottom. Give the reviewer the skill, intended outcome, hard constraints, artifacts, traces, and graded case results without the author's conclusions. Use its findings to identify wasted paths, ambiguous or unused instructions, recurring corrections that belong in `Gotchas`, and helper logic repeatedly reinvented across runs that belongs in `scripts/`. Any substantive follow-up edit returns through structural validation and the affected cases before shipping.

The general checklist-exception path does not apply to independent grader or final reviewer availability or context independence. If either role is unavailable or cannot run in an independent context, its state remains unverified and blocks completion until a separate context completes it.

Completion: the baseline comparison has a ship or return-to-correction decision, and every checklist item passes or has a user-approved deliberate exception where the checklist permits one.

### 7. Test the description

For a new skill, or whenever the description changed, follow [assets/trigger-queries-template.md](assets/trigger-queries-template.md): build the should-trigger and near-miss query set, record it in `tests/<skill-name>/triggers.md`, and judge it through separate fresh-context agents using the template's protocol and thresholds. When a revision leaves the description untouched, the existing trigger contract stands — skip the rerun; the routing contract did not change.

After any description edit, rerun the complete query set and the affected behavioral comparison.

Completion: for a new or description-changed skill, every should-trigger query passes and no near miss activates, with results logged (a judgment that cannot be run is recorded as not run, never counted as a pass); otherwise the existing trigger contract is confirmed unchanged.

### 8. Package and install

Recheck the host conventions from step 2 and confirm the canonical directory is self-contained. Run the smoke check from [assets/trigger-queries-template.md](assets/trigger-queries-template.md): install from the current local source into a disposable project on each roster harness — the harness target set declared in step 2 — ask one should-trigger query, confirm the skill activates, and record one log line per harness. Using a user-level skill location or overwriting an existing same-name installation requires explicit user approval.

When a roster harness is unavailable, log it as not run rather than guessing; a failed smoke check returns to correction.

If packaging exposes a defect that changes the package, apply step 6's re-entry rule before completing this step.

Completion: the source validates, and every roster harness has a logged smoke result of pass or not run, with no failure outstanding.

## Gotchas

- The description carries the triggering burden. State its owned trigger branches and reserve workflow details for the body.
- A later substantive edit invalidates the affected comparison even when an earlier draft passed.
- Check the target collection and system-provided skills for name collisions. Verb-led gerund names (`creating-portable-skills`, not `skill-creator`) are usually more specific.

## Credits

The review vocabulary distills [writing-great-skills](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-great-skills) by Matt Pocock (MIT) and [writing-skills](https://github.com/obra/superpowers/blob/main/skills/writing-skills/SKILL.md) by Jesse Vincent (MIT). Format, evaluation, and description doctrine follow the [Agent Skills specification](https://agentskills.io), its skill-creation guides, and Anthropic's [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) (Apache 2.0).
