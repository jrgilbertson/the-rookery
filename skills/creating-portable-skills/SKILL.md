---
name: creating-portable-skills
description: Use when creating a new agent skill, or when reviewing, updating, or migrating a skill between collections, including fixing a skill's description, triggers, structure, or portability. Produces portable, installable skills that work across models and harnesses. Do not use for building plugins, designing standalone eval suites, or reviewing prose that is not a skill.
license: MIT
---

# Creating Skills

Skill authoring here is one disciplined loop, and the loop enforces four things ad-hoc authoring reliably skips on any model. Portability gates keep the package canonical. A delete test keeps every instruction earning its tokens through observed evidence. Trigger testing makes the description a real contract. One consistent process carries the work from intent to installed package.

Skills produced here follow the [Agent Skills format](https://agentskills.io/specification): a self-contained directory with a `SKILL.md` (frontmatter plus body) and optional `references/`, `assets/`, and `scripts/`. Canonical frontmatter uses only the portable fields (`name`, `description`, `license`, `compatibility`, `metadata`). Read [references/portability.md](references/portability.md) when authoring frontmatter or targeting a specific harness.

## Routing

- A durable eval suite (graders, rubrics, datasets, calibration) is a different job. Recommend installing the `design-evals` skill (`npx skills add jrgilbertson/the-rookery --skill design-evals`).
- For deep review vocabulary beyond the built-in checklist, recommend the `writing-great-skills` skill ([mattpocock/skills](https://github.com/mattpocock/skills)).
- Neither companion is required. When one is absent, use the built-in step here and tell the user which deeper pass was skipped.

## The loop

Creating a new skill: start at step 1. Reviewing, updating, or migrating an existing skill: start at step 0.

### 0. Audit (existing skills only)

Read the whole skill, then check it against [references/review-checklist.md](references/review-checklist.md). Produce a prioritized fix list where each item names what is wrong, why it matters, and the risk of fixing it. Present the list and get the user's approval on a fix scope before editing anything.

Completion: the user approved a fix scope. Continue at step 1 to capture the intent of the approved changes, then run the loop from step 2 on the revised skill, since a revision can change what earns bundling too.

### 1. Interview

Pin down, asking one question at a time:

- The one job the skill does. If describing it needs "and", it is probably two skills.
- The triggering conditions, meaning the phrasings that should activate it and the near-misses that must not.
- Expected outputs and what "done" looks like.
- Which decisions stay with the user, such as scope approvals, waivers, and taste calls. Many skills should run fully automatic. A skill that touches judgment or taste names its steering points.
- Real environment requirements (commands, network, credentials), if any.
- Two or three concrete usage examples, ideally from tasks the user has actually done.

Completion: you can state the skill's job in one sentence and list its triggers, near-misses, and examples.

### 2. Plan resources

Decide what earns bundling before drafting. Templates the outputs will copy go in `assets/`, material read on demand goes in `references/`, and deterministic helpers belong in `scripts/` only where instructions cannot be reliable. Everything else stays out. Skills are standalone, with no reaching outside the skill directory and no depending on another skill being installed. Check the host repository's conventions now (contributing docs, agent instruction files, a changelog, validator scripts), since they decide where files go and which rules apply to everything the loop creates.

Completion: a file list with a one-line reason per file, plus the host conventions that apply.

### 3. Draft

For a new skill, copy [assets/skill-template.md](assets/skill-template.md) into the skill's directory, created at the host repo's skill discovery path (see [references/portability.md](references/portability.md)) or wherever the host keeps its skills. For a revision, preserve a loadable copy of the prior version before editing (the last commit suffices in a versioned repo), then edit the existing skill in place; for a migration between collections, first copy the source package into the destination's skill location and revise that copy, leaving the source collection untouched. While writing:

- Run the delete test on every line. Would the agent get this wrong without it? If not, cut it.
- Match specificity to fragility, with exact steps for fragile operations and a heuristic plus the why for open-ended ones. Explain reasoning ("do X because Y") over bare commands.
- Keep the body near 200 lines and never past 500. Push branch-specific detail one level deep with an explicit read-trigger ("Read references/x.md when Y"), not a bare "see references/".
- Write capability-based prose instead of harness product names. Say "present a structured confirmation and wait for a choice" rather than naming a vendor tool.
- Keep every path relative and inside the skill directory, and every name and reference public. Nothing may assume your machine or private repos.

Completion: a draft with frontmatter, body, and every planned resource written.

### 4. Validate

Run `npx skills-ref validate <skill-directory>`. If `npx` cannot run here (no Node runtime or no network), perform the same checks manually and state that the validator was skipped. The manual checks: `name` at most 64 chars, lowercase kebab-case, no leading, trailing, or consecutive hyphens, matching the directory name; `description` 1 to 1024 chars; body at most 500 lines; portable frontmatter fields only; `compatibility`, when present, at most 500 chars; `metadata`, when present, string values only. Fix and re-check until clean.

Completion: validation clean, by tool or by named manual check.

### 5. Baseline test

Copy [assets/baseline-test-template.md](assets/baseline-test-template.md) to wherever the host repo keeps test records (`tests/<skill-name>/` when it has no convention) and fill it there. If a prior run's record already exists there, append a new dated entry or write a new dated file rather than overwriting the earlier evidence and any recorded waiver. For a new skill, run 2 or 3 realistic prompts with and without the skill. For a revision, run the prior version against the revised one. Run every prompt in a fresh agent context with the right variant loaded, using your harness's native mechanism for a clean context (a subagent, a CLI exec, a new session). If you have no way to produce one, say so plainly and ask the user to run the prompts in a fresh session.

A substantive change means any change to instruction semantics, the trigger description, or bundled resources. It must not ship without this comparison or an explicit recorded waiver from the user. Typo, formatting, and link-only fixes are exempt. This gate holds for the rest of the loop. Any later edit that is substantive under this rule, whether from step 6's subtract pass, a step 7 review fix, or step 8 description tuning, routes back through step 4's validation and this comparison before the skill packages.

Completion: a recorded comparison showing the skill changes behavior as intended, or a recorded waiver.

### 6. Subtract

Where the with/without runs showed no behavioral difference, those instructions are not earning their tokens. Remove them and re-check. If results plateau while you add rules, the skill is over-constrained, so remove instead of adding.

Completion: every surviving instruction traces to an observed difference or a named fragile operation.

### 7. Review

Run [references/review-checklist.md](references/review-checklist.md) top to bottom. Recommend the companions from Routing for anything deeper. When a companion is absent, the checklist is the floor and you name what was skipped.

Completion: every checklist item passes or has a recorded, deliberate exception, and any substantive fix has re-entered step 5's gate.

### 8. Test the description

Copy [assets/trigger-queries-template.md](assets/trigger-queries-template.md) next to the baseline record. Build 5 should-trigger phrasings (include at least one non-obvious wording) and 5 near-misses, then judge each once in a fresh context using the same clean-context mechanism as step 5 (if you have none, say so and ask the user to run them). Activation is judged at the listing level. Show the context only the skill's name and description alongside the query and ask whether it would activate, requiring a plain yes, no, or unsure; a live harness-discovery run, where available, is stronger evidence.

Passing: every should-trigger activates and no near-miss does. An unsure or hedged judgment counts as borderline. On a miss or a borderline call, tune by front-loading trigger words and describing when to use the skill, never by summarizing the workflow, then re-judge the full query set on both tables, since an edit can newly activate a near-miss (two extra runs for any that stay borderline, majority wins). A tuning edit changes the trigger description, so the last one re-enters step 5's gate. Scale up to the template's full-rigor tier (8 to 10 queries each side, 3 runs per query) only when the skill ships to a public collection or triggering is unusually load-bearing.

Completion: the query set passes.

### 9. Package

Re-verify the host conventions found in step 2 (contributing docs, agent instruction files, a changelog, validator scripts), confirm the loop's outputs still follow them, and say which conventions you followed. In a repo with none, use the generic path and say so. Either way, confirm the directory is self-contained, then verify a clean install through the repo's documented install path (or by copying the directory into the harness's skill home, where a repo-level discovery path counts when the user home is out of reach) and confirm the skill loads and triggers.

Completion: an installed copy loads and triggers in one harness for a skill staying out of public collections; when the skill ships to a public collection, or its description or compatibility field names specific harnesses, verify a clean install in each named harness (mirroring step 8's full-rigor tier). The portable-frontmatter and capability-prose gates carry the general cross-harness claim.

## Gotchas

- The description carries the entire triggering burden. Body content never rescues a weak description. Err on the pushy side, since agents under-trigger.
- Skills drift longer and degrade with every ungated edit. The baseline gate exists for edit seven, not edit one.
- A description that summarizes the workflow makes agents follow the summary and skip the body. Describe when to use it, not what the steps are.
- Weaker models need slightly more detail than frontier ones. A portable skill is tuned for the floor it claims, not the strongest model you happen to use.
- Check the target collection and the vendor system skills for name collisions before settling a name. Verb-led gerund names (`creating-portable-skills`, not `skill-creator`) collide less and describe the job.

## Credits

The review vocabulary distills [writing-great-skills](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-great-skills) by Matt Pocock (MIT) and [writing-skills](https://github.com/obra/superpowers/blob/main/skills/writing-skills/SKILL.md) by Jesse Vincent (MIT). Format, evaluation, and description doctrine follow the [Agent Skills specification](https://agentskills.io) and its skill-creation guides.
