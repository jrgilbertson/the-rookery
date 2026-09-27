---
name: creating-portable-skills
description: Use when creating, updating, or migrating a skill, when editing a skill's SKILL.md, evals, graders, or trigger queries, or when finding problems in its description, triggers, structure, portability, or evidence. Produces prioritized findings or a portable, installable skill package. Explanation-only requests stay with general reasoning.
license: MIT
compatibility: Behavioral validation requires a different-model blind grader and an independent review context.
---

# Creating Skills

Create, revise, migrate, or audit a skill from its intent, required outcome, and only the hard constraints that define acceptable completion or remain under user authority.

Skills produced here follow the [Agent Skills format](https://agentskills.io/specification). Read [references/portability.md](references/portability.md) when checking frontmatter against its canonical-package rule, choosing an install location, adding harness-specific metadata, or making a claim about a harness. [references/skills.md](references/skills.md) is the convention for frontmatter fields, eval files, arms and runs, human inspection, targets, grading, the run archive, and committed evidence; read it before steps 2, 5, 6, 7, and 8.

An independent reviewer took no part in authoring the change and did not produce the artifact under review; an agent auditing a skill it did not write qualifies. Behavioral grading uses an independent context on a different model from the executor. One independent review checks the package and evidence. The author never supplies required independent grades or review, even provisionally. If either is unavailable, prepare a self-contained handoff with assertions, outputs, tool traces, and available child readouts; the missing judgment stays unverified and the change does not ship.

## Workflow

A substantive change gets one regression check on affected evals, once per declared Executor target, under [references/skills.md](references/skills.md). New skills check realistic cases. Description changes also follow step 7. Cosmetic edits (typos, formatting, links, or moving eval files without changing their meaning) may skip behavior checks and use step 4 and `scripts/check-evals.py`.

When the question is whether the skill helps, use the value-assessment procedure in [assets/baseline-test-template.md](assets/baseline-test-template.md). A later correction uses the affected regression check. Human inspection, repeats, native activation, package identity, the execution boundary, and the ship rule live in [references/skills.md](references/skills.md).

A read-only audit starts and ends at step 0. Authorized revisions and new skills start at step 1; an additional audit before implementation is not required. Existing authorization for the material fix scope carries forward. Further rounds follow the repeat rule in [references/skills.md](references/skills.md). Broader cross-model sweeps are separate work.

### 0. Audit an existing skill

Have an independent reviewer apply [references/review-checklist.md](references/review-checklist.md) to the whole package and the host repository's instructions, with the inputs the checklist names, and present its prioritized fix list.

Read-only completion: the evidence-backed review, its prioritized fix list, and a final verdict are delivered, with no file changed. Revision begins only in a separate user-authorized request.

Change completion: the user has authorized the material fix scope and settled any authority or taste decisions that stay with them. Continue at step 1.

### 1. Resolve the intent

Ground the reusable guidance in real work already available: the conversation, the existing package, user corrections, successful task history, input and output examples, project documentation, schemas, review comments, issues, version history, and resolved failures. Name only the hard constraints, including decisions that remain with the user, and only real environment requirements. When a missing decision could materially change the result, scope, or authority and the available context leaves it open, ask one focused question at a time.

Completion: the job is written as one sentence, and the triggering conditions, near-misses, intended outcome, observable done state with any required artifact or handoff, hard constraints, environment requirements, and representative examples are each written down with a value or `not applicable`.

### 2. Scope targets and resources

Take the target set from the **Targets** section of [references/skills.md](references/skills.md); structural portability alone does not require expanding it.

Choose only resources with repeatable value. Outputs copied by the workflow belong in `assets/`. Reference material that only some paths need belongs in `references/`. Deterministic helpers belong in `scripts/` when prose cannot reliably protect the result. Check the host repository's contribution docs, agent instructions, changelog policy, skill discovery path, and validators.

Completion: the target set and applicable host conventions are recorded, with a file list and one-line reason for every bundled file.

### 3. Draft

For a new skill, copy [assets/skill-template.md](assets/skill-template.md) to the host's skill discovery path or documented skill location. For a revision, preserve a loadable prior version before editing; the last commit is sufficient in a versioned repository. For a migration, copy the source package to the destination collection and revise the copy without changing the source.

Before drafting, read the **System-Owned Invariants**, **Information hierarchy**, **Instruction economy**, and **Portability** sections of [references/review-checklist.md](references/review-checklist.md) and apply them as authoring constraints; they also govern relaxing an existing instruction. Use the least-prescriptive instruction that reaches the required outcome within its hard constraints: keep every System-Owned Invariant explicit, and leave the agent its reasoning and implementation path everywhere else.

Completion: every file in step 2's list exists, and each hard constraint from step 1 appears in the draft.

### 4. Validate structure

Run the Agent Skills reference validator, `skills-ref validate <skill-directory>` ([specification](https://agentskills.io/specification#validation)), from a trusted install, and record its version and source; some published builds name the same command `agentskills validate`. Do not use the similarly named npm package; it is not the reference validator. If the reference validator is not already available, ask before installing it from a pinned `agentskills/agentskills` commit, or run the fallback checks: every field matches the **Package format** table in [references/skills.md](references/skills.md), no other field appears, `metadata` holds string values only, and the body is at most 500 lines. Either way, check the canonical-package rule in [references/portability.md](references/portability.md), which the validator does not enforce.

Completion: the validator passes, or every named fallback check passes with the tool limitation recorded, and the canonical-package rule holds.

### 5. Check behavior

Use [assets/baseline-test-template.md](assets/baseline-test-template.md) for the affected regression check, blind grading, and failure diagnosis. When the question is whether the skill helps, use that template's value-assessment section. Before calls, establish the caller's budget and the host's per-call usage and pricing support under **Cost and budget** in [references/skills.md](references/skills.md), and declare the **Execution boundary** in that file. The host owns runner automation and configuration; this package stays runner-free.

Completion: affected checks ran on every declared target, every failure was inspected against its original transcript and classified, and any needed prior-skill diagnosis is recorded. A value assessment, and any round with newly proposed cases, has those cases inspected and frozen before calls. A value assessment also has its matched pairs, human-inspection record, and a value conclusion separate from the ship decision. An affected regression of an already frozen case set reuses that set. Eval definitions, raw archive records, and the round's benchmark exist, and `scripts/check-evals.py` exits 0 on the target skill. Missing authorized runs, an unavailable inspection surface on a round that requires inspection, or unresolved attribution remain unverified. Cosmetic-only edits record behavior checks as not applicable.

### 6. Decide and review

Apply the ship rule in [references/skills.md](references/skills.md). Have one independent reviewer apply [references/review-checklist.md](references/review-checklist.md) to the package, assertions, artifacts, and evidence. This review checks that assertions are decidable from the grader's packet and no stricter than the contract. It does not require a separate pre-spend review or a repeated final-review cycle.

A substantive follow-up edit returns through step 4 and the affected evals. Recheck evals whose outcomes could change under the revised package or test material, including changed instructions, executable helpers, bundled resources, prompts, inputs, or assertions. Preserve previous artifacts and grades under their original revision labels. Diagnose failures using the prior skill only where needed; do not combine unmatched cohorts into a delta.

Completion: structural checks pass, required independent grading and review are complete, every failure has an evidence-backed disposition, and none is attributable to the change under test. The value conclusion is recorded separately. An unresolved hold stays unresolved. Claims stay within the exercised cases and targets; unresolved attribution remains unverified.

### 7. Test the description

For a new skill, or whenever the description changed, follow [assets/trigger-queries-template.md](assets/trigger-queries-template.md).

Completion: for a new or description-changed skill, the query set has run under the trigger rules in [references/skills.md](references/skills.md), every failure has been inspected, and the recorded attribution satisfies its ship rule; otherwise, a diff of the description against the preserved prior version is empty. A judgment that cannot be run is recorded as not run and never counted as a pass.

### 8. Package and install

For a new package, or a change to packaging or the install path, recheck the host conventions from step 2, confirm the canonical directory is self-contained, and run the smoke check in [assets/trigger-queries-template.md](assets/trigger-queries-template.md) on each harness in step 2's target set. Using a user-level skill location or overwriting an existing same-name installation requires explicit user approval.

If packaging exposes a defect that changes the package, apply step 6's re-entry rule before completing this step.

Completion: the source validates, and each harness in step 2's target set records a smoke pass for the exact `package_hash` and `install_path` under test, or a not run with the user's recorded decision to ship without it. Global installation and publication require their own approval. The package stays runner-free.

## Gotchas

- Check the target collection and system-provided skills for name collisions. Verb-led gerund names (`creating-portable-skills`, not `skill-creator`) are usually more specific.
- Keep a host repository's local rules, such as changelog policy, tracker choice, and CI vendor, in that repository rather than in the portable skill.
- When the skill's intent shrinks, update `evals/evals.json` and `evals/eval_queries.json` in the same change rather than leaving a one-off exception.

## Credits

Format, evaluation, and description doctrine follow the [Agent Skills specification](https://agentskills.io), its skill-creation guides, and Anthropic's [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) (Apache 2.0).
