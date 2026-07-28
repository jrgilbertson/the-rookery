---
name: creating-portable-skills
description: Use when creating a new agent skill, or when reviewing, updating, or migrating a skill between collections, including fixing its description, triggers, structure, or portability. Produces portable, installable Agent Skills packages. Do not use for building plugins, designing standalone eval suites, or reviewing prose that is not a skill.
license: MIT
compatibility: Requires isolated agent contexts or separate sessions for agent grading and review.
---

# Creating Skills

Create or revise a skill from its intent, required outcome, and only the hard constraints that define acceptable completion or remain under user authority. The result is a self-contained Agent Skills package with structural validation, appropriately scoped behavioral evidence, and separate trigger and installation checks.

Skills produced here follow the [Agent Skills format](https://agentskills.io/specification): a directory with a `SKILL.md` (frontmatter plus body) and optional `references/`, `assets/`, and `scripts/`. Canonical frontmatter uses only `name`, `description`, `license`, `compatibility`, and `metadata`. Read [references/portability.md](references/portability.md) when authoring frontmatter, choosing an install location, or making a harness-specific claim.

An independent reviewer did not participate in the authoring discussion or produce the artifact under review. One independent grader inspects each matched case; a different fresh-context reviewer performs the final package review. If the current environment cannot start those independent contexts, prepare a self-contained handoff for a separate session and keep the affected grade or review unverified until that session completes it. Do not substitute the author's own review.

## Workflow

Creating a new skill starts at step 1. Reviewing, updating, or migrating an existing skill starts at step 0.

### 0. Audit an existing skill

Have a separate fresh-context agent that has not participated in the current authoring work read the whole package and the host repository's instructions. Give it the skill, the review checklist, and the stated intent without the author's conclusions. Have it apply [references/review-checklist.md](references/review-checklist.md) top to bottom, then present a prioritized fix list where each item names the problem, impact, and change risk. Get the user's approval for the material fix scope before editing.

Completion: the user has approved the fix scope, including any authority or taste decisions that stay with them.

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

Keep the body at most 500 lines and aim below 5,000 tokens. Treat the token figure as an authoring target because tokenizers vary, not as a portable structural claim. Put branch-specific detail one level deep behind an explicit read-trigger, and add a table of contents to references longer than 300 lines. Write capability-based prose and keep every bundled reference relative and inside the skill directory. Host-project paths the skill operates on are allowed; owner-machine paths and private dependencies are not.

Completion: the draft and every planned resource implement the intent and required outcome with every System-Owned Invariant protected.

### 4. Validate structure

Run `npx skills-ref validate <skill-directory>`. If it cannot run because the environment lacks Node or network access, state that limitation and manually check: `name` is at most 64 characters, lowercase kebab-case, has no leading, trailing, or consecutive hyphens, and matches the directory; `description` is 1 to 1024 characters; the body is at most 500 lines; frontmatter uses only the canonical fields; `compatibility`, when present, is at most 500 characters; and `metadata`, when present, contains string values only.

Completion: the validator passes, or every named fallback check passes with the tool limitation recorded.

### 5. Compare behavior

Treat changed instruction semantics, a changed trigger description, or a changed bundled resource as substantive. Copy [assets/baseline-test-template.md](assets/baseline-test-template.md) to the host's test-record location (`tests/<skill-name>/` when no convention exists), preserving earlier dated evidence. Typo, formatting, and link-only edits are exempt.

Predeclare at least two matched realistic cases: one discriminating case where the change should affect behavior and one control where it should not. For a new skill, compare without-skill and with-skill behavior; for a revision, compare the frozen prior and revised versions. Run each variant in a fresh context. Have a separate fresh-context agent that did not author the change or produce the artifact grade each matched result. Mechanical checks may use deterministic scripts. When multiple targets are declared, run the same cases separately in every target cell and preserve each result.

The grader must inspect the actual artifacts and relevant trace and cite concrete evidence for every pass. It must also flag checks that are trivial, unverifiable, or missing part of the required outcome. Keep subjective qualities out of binary checks; route them to specific human feedback or, when the claim requires it, a blind comparison by another fresh-context agent.

Routine evidence earns only **smoke-tested** for one observed execution or **directional comparison** for a small matched comparison. State observations, losses, unavailable cells, and limits. If the user requests non-regression or causal improvement, explain that deeper evaluation must isolate the changed variable, account for ordinary run variation, and use repeatable outcome judgments; do not upgrade the routine record.

This comparison is a shipment gate for substantive changes. An unavailable required cell remains unverified; a user waiver may authorize shipping only when the candidate decision remains supported under the checklist, and cannot raise the evidence label.

Completion: the template records every declared target and predeclared case, the evidence it earned, and what remains unverified.

### 6. Decide and review

Have a separate fresh-context agent apply the candidate-decision and divergence rules in [references/review-checklist.md](references/review-checklist.md), then run the rest of that checklist top to bottom. Give the reviewer the skill, intended outcome, hard constraints, artifacts, traces, and evidence record without the author's conclusions. Use its findings to identify wasted paths, ambiguous or unused instructions, recurring corrections that belong in `Gotchas`, and helper logic repeatedly reinvented across runs that belongs in `scripts/`. Any substantive follow-up edit returns through structural validation and every affected comparison cell.

Completion: each candidate is retained or supported within the recorded Claim Ceiling, every checklist item passes or has a user-approved deliberate exception, and no target conflict is collapsed into a pass.

### 7. Test the description

Copy [assets/trigger-queries-template.md](assets/trigger-queries-template.md) beside the baseline record. Test at least five should-trigger phrasings, including one non-obvious wording, and five near-misses. Vary length, formality, detail, implied intent, and natural typing such as abbreviations or minor mistakes. Use concrete tasks where the skill should change execution or output. Near-misses should share its topic, artifact, or common wording but require a different job. Each judgment comes from a separate fresh-context agent that did not author the description and sees only the skill name, description, and one query. Use the template's expanded tier for a public collection or unusually load-bearing trigger contract.

Treat listing judgments as a description-routing proxy, separate from native discovery, loading, and triggering. After a description edit, rerun the whole query set and the affected behavioral comparison.

Completion: every should-trigger query passes, no near-miss activates, and the result is recorded as listing-proxy evidence rather than native behavior.

### 8. Package and install

Recheck the host conventions from step 2 and confirm the canonical directory is self-contained. Install from the current local source through each declared harness's documented path, verify the installed content identity, and record native discovery, loading, and triggering separately for every applicable target cell.

An unavailable native check stays unverified. An explicit user waiver may authorize shipping an unverified candidate, but cannot turn a proxy into native evidence, raise the evidence label, or support an otherwise unsupported instruction change.

Completion: the source validates; each required structural, install, identity, discovery, load, and trigger state is recorded independently; and any shipped claim stays within those states.

## Gotchas

- The description carries the triggering burden. Describe when to use the skill, not a summary that encourages skipping the body.
- A later substantive edit invalidates the affected comparison even when an earlier draft passed.
- Check the target collection and system-provided skills for name collisions. Verb-led gerund names (`creating-portable-skills`, not `skill-creator`) are usually more specific.

## Credits

The review vocabulary distills [writing-great-skills](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-great-skills) by Matt Pocock (MIT) and [writing-skills](https://github.com/obra/superpowers/blob/main/skills/writing-skills/SKILL.md) by Jesse Vincent (MIT). Format, evaluation, and description doctrine follow the [Agent Skills specification](https://agentskills.io), its skill-creation guides, and Anthropic's [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) (Apache 2.0).
