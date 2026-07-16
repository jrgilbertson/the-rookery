---
name: creating-skills
description: Use when creating a new agent skill, or when reviewing, updating, or migrating an existing one — including fixing a skill's description, triggers, structure, or portability, and porting a skill between collections. Runs one loop from intent interview through baseline testing to a packaged, installable skill that works across models and harnesses. Do not use for building plugins, designing standalone eval suites, or reviewing prose that is not a skill.
license: MIT
---

# Creating Skills

Models already know the SKILL.md format. What they skip without this skill is the discipline: portability gates, instructions that earn their tokens through observed evidence, descriptions tested as trigger contracts, and one consistent process from intent to installed package. This skill enforces those four.

Skills produced here follow the [Agent Skills format](https://agentskills.io/specification): a self-contained directory with a `SKILL.md` (frontmatter plus body) and optional `references/`, `assets/`, and `scripts/`. Canonical frontmatter uses only the portable fields — `name`, `description`, `license`, `compatibility`, `metadata`. Read [references/portability.md](references/portability.md) when authoring frontmatter or targeting a specific harness.

## Routing

- A durable eval suite (graders, rubrics, datasets, calibration) is a different job: recommend installing the `design-evals` skill (`npx skills add jrgilbertson/the-rookery --skill design-evals`).
- Deep review vocabulary beyond the built-in checklist: recommend the `writing-great-skills` skill ([mattpocock/skills](https://github.com/mattpocock/skills)).
- Neither companion is required. When one is absent, use the built-in step here and tell the user which deeper pass was skipped.

## The loop

Creating a new skill: start at step 1. Reviewing, updating, or migrating an existing skill: start at step 0.

### 0. Audit (existing skills only)

Read the whole skill, then check it against [references/review-checklist.md](references/review-checklist.md). Produce a prioritized fix list — each item names what is wrong, why it matters, and the risk of fixing it. Present the list and get the user's approval on a fix scope before editing anything.

Completion: the user approved a fix scope. Continue at step 1 to capture the intent of the approved changes, then run the loop from step 2 on the revised skill — a revision can change what earns bundling too.

### 1. Interview

Pin down, asking one question at a time:

- The one job the skill does. If describing it needs "and", it is probably two skills.
- Triggering conditions — the phrasings that should activate it, and the near-misses that must not.
- Expected outputs and what "done" looks like.
- Real environment requirements (commands, network, credentials), if any.
- Two or three concrete usage examples, ideally from tasks the user has actually done.

Completion: you can state the skill's job in one sentence and list its triggers, near-misses, and examples.

### 2. Plan resources

Decide what earns bundling before drafting: templates the outputs will copy (`assets/`), material read on demand (`references/`), deterministic helpers only where instructions cannot be reliable (`scripts/`). Everything else stays out. Skills are standalone — no reaching outside the skill directory, no depending on another skill being installed.

Completion: a file list with a one-line reason per file.

### 3. Draft

Copy [assets/skill-template.md](assets/skill-template.md) into the new skill's directory — create it at the host repo's skill discovery path (see [references/portability.md](references/portability.md)) or wherever the host keeps its skills — or edit the existing skill in place for a revision. While writing:

- Run the delete test on every line: would the agent get this wrong without it? If not, cut it.
- Match specificity to fragility — exact steps for fragile operations, a heuristic plus the why for open-ended ones. Explain reasoning ("do X because Y") over bare commands.
- Keep the body near 200 lines and never past 500. Push branch-specific detail one level deep with an explicit read-trigger ("Read references/x.md when Y"), not a bare "see references/".
- Write capability-based prose, not harness product names: "present a structured confirmation and wait for a choice", not a named vendor tool.
- No absolute paths, no personal-environment assumptions, no private names.

Completion: a draft with frontmatter, body, and every planned resource written.

### 4. Validate

Run `npx skills-ref validate <skill-directory>`. If `npx` cannot run here (no Node runtime or no network), perform the same checks manually — `name` ≤64 chars, lowercase kebab-case, matching the directory name; `description` 1-1024 chars; body ≤500 lines; portable frontmatter fields only — and state that the validator was skipped. Fix and re-check until clean.

Completion: validation clean, by tool or by named manual check.

### 5. Baseline test

Copy [assets/baseline-test-template.md](assets/baseline-test-template.md) to wherever the host repo keeps test records (`tests/<skill-name>/` when it has no convention) and fill it there. For a new skill, run 2-3 realistic prompts with and without the skill; for a revision, prior version against revised. Run every prompt in a fresh agent context with the right variant loaded — use your harness's native mechanism for a clean context (a subagent, a CLI exec, a new session). If you have no way to produce one, say so plainly and ask the user to run the prompts in a fresh session.

A substantive change — any change to instruction semantics, the trigger description, or bundled resources — must not ship without this comparison or an explicit recorded waiver from the user. Typo, formatting, and link-only fixes are exempt.

Completion: a recorded comparison showing the skill changes behavior as intended, or a recorded waiver.

### 6. Subtract

Where the with/without runs showed no behavioral difference, those instructions are not earning their tokens: remove them and re-check. If results plateau while you add rules, the skill is over-constrained — remove instead of adding.

Completion: every surviving instruction traces to an observed difference or a named fragile operation.

### 7. Review

Run [references/review-checklist.md](references/review-checklist.md) top to bottom. Recommend the companions from Routing for anything deeper; when a companion is absent, the checklist is the floor and you name what was skipped.

Completion: every checklist item passes or has a recorded, deliberate exception.

### 8. Test the description

Copy [assets/trigger-queries-template.md](assets/trigger-queries-template.md) next to the baseline record. Build 8-10 should-trigger phrasings (include non-obvious ones) and 8-10 near-misses. Run each 3 times in a fresh context, using the same clean-context mechanism as step 5 (if you have none, say so and ask the user to run them). Activation is judged at the listing level: show a fresh context only the skill's name and description alongside the query and ask whether it would activate; a live harness-discovery run, where available, is stronger evidence. Passing: each should-trigger query activates in at least half its runs; any near-miss activation is a failure. Tune by front-loading trigger words and describing when to use it — never by summarizing the workflow — then re-run.

Completion: the query set passes.

### 9. Package

Follow the host repository's own conventions when they exist — look for contributing docs, agent instruction files, a changelog, and validator scripts; use what you find and say which conventions you followed. In a repo with none, use the generic path and say so: confirm the directory is self-contained, then verify a clean install through the repo's documented install path (or by copying the directory into the harness's skill home — a repo-level discovery path counts when the user home is out of reach) and confirm the skill loads and triggers.

Completion: an installed copy loads and triggers in at least one harness.

## Gotchas

- The description carries the entire triggering burden — body content never rescues a weak description. Err on the pushy side; agents under-trigger.
- Skills drift longer and degrade with every ungated edit. The baseline gate exists for edit seven, not edit one.
- A description that summarizes the workflow makes agents follow the summary and skip the body. Describe when to use it, not what the steps are.
- Weaker models need slightly more detail than frontier ones. A portable skill is tuned for the floor it claims, not the strongest model you happen to use.
- Do not name-collide: check the target collection and the vendor system skills before settling a name. Verb-led gerund names (`creating-skills`, not `skill-creator`) collide less and describe the job.

## Credits

The review vocabulary distills [writing-great-skills](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-great-skills) by Matt Pocock (MIT) and [writing-skills](https://github.com/obra/superpowers/blob/main/skills/writing-skills/SKILL.md) by Jesse Vincent (MIT). Format, evaluation, and description doctrine follow the [Agent Skills specification](https://agentskills.io) and its skill-creation guides.
