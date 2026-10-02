---
name: creating-portable-skills
description: Create, revise, migrate, or audit portable Agent Skills packages. Use when the user requests skill authoring or explicitly invokes this skill to review instructions, structure, or portability.
license: MIT
---

# Creating Portable Skills

Produce an installable package that does the user's reusable job and follows the
[Agent Skills specification](https://agentskills.io/specification), with useful
evaluation cases and a grading method built through the upstream workflow.

For a read-only audit, apply [references/review-checklist.md](references/review-checklist.md)
and return prioritized findings with file evidence and a verdict. For authorized
creation, revision, or migration, use the workflow below. Existing authorization
and the host project's constraints carry forward.

## Author the package

Ground the skill in the user's intent, existing package, representative inputs
and outputs, and corrections from real work. Identify the outcome and hard
constraints that make completion acceptable. Check the host's contribution
rules, discovery path, and existing owners before adding a workflow or helper.

For a new skill, use [assets/skill-template.md](assets/skill-template.md). For a
revision, the last commit can preserve the prior version. For a migration,
revise a copy and preserve the source. Read
[references/portability.md](references/portability.md) when choosing frontmatter,
bundling dependencies, or removing harness-specific assumptions.

Keep one instruction set for the job. Separate changing facts from reusable
instructions when that lets the next update change one source. Put conditional
guidance in `references/`, copied outputs in `assets/`, and deterministic helpers
in `scripts/` when an existing mechanism cannot meet the requirement. Bundle
everything the package needs, or declare its actual environment dependencies.

Apply [references/review-checklist.md](references/review-checklist.md) while
drafting. Preserve user authority, exact formats, privacy requirements, and
fragile operation order; leave reasoning and implementation choices open.

## Validate and evaluate

Use `skills-ref validate <skill-directory>` from an available trusted install.
If it is unavailable, check the specification's frontmatter rules, name-directory
match, body, and local resource links directly, and record the limitation. Exercise
bundled helpers with realistic inputs in disposable storage outside the host
project; preserve existing inputs and outputs.

For new skills and behavior changes, read and follow the pinned upstream
`build-eval` guide in [references/evaluation.md](references/evaluation.md). Reuse
existing cases, runner, and grader when they still measure the intended outcome.
Before delivering a new skill, include the user-approved eval inputs and grading
method; these are part of the package's delivery, even when execution is not
authorized. If a sign-off or required guide is unavailable, report that missing
step. The host owns execution, storage, budget, and release requirements.
Preserve its required independent judgments and approvals; missing evidence
stays unverified.

Retuning a corpus after a model upgrade is a separate measurement workflow.
[references/evaluation.md](references/evaluation.md) points to `ce-retune` and
explains when it applies. Updating factual model recommendations alone is an
ordinary revision.

## Deliver

Check the final package's local links, dependencies, host conventions, and
applicable evaluation evidence. Report the package location, observed checks,
and anything unverified. For public migrations, replace private examples with
synthetic inputs that preserve the behavior and difficulty being tested, and
inspect the whole copy for leaks. Keep answers and grading material outside the
runtime instructions. Follow the host's release and installation process.

## Sources

The [Agent Skills specification](https://agentskills.io/specification) owns the
package format. Evaluation uses Anthropic's maintained guides; corpus retuning
uses Compound Engineering's `ce-retune`. Their pinned sources and availability
requirements are in [references/evaluation.md](references/evaluation.md).
