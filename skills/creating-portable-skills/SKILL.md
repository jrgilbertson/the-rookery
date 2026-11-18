---
name: creating-portable-skills
description: Create, revise, migrate, or audit portable Agent Skills packages. Use when the user requests skill authoring or explicitly invokes this skill to review instructions, structure, or portability.
license: MIT
---

# Creating Portable Skills

Produce an installable package that does the user's reusable job and follows the
[Agent Skills specification](https://agentskills.io/specification). A portable
skill works the same in any harness and with any agent that supports the
specification, so prefer the specification over one harness's conventions.

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

## Validate

Use `skills-ref validate <skill-directory>` from an available trusted install.
If it is unavailable, check the specification's frontmatter rules, name-directory
match, body, and local resource links directly, and record the limitation. Exercise
bundled helpers with realistic inputs in disposable storage outside the host
project; preserve existing inputs and outputs.

Package checks, helper tests, and applicable authorized smoke checks run for
every package.

## Improve from real use

Improve a skill from real use and demonstrated failures. The first time a
failure appears, fix the instruction and say what was observed in the fix's
commit message. Keep a repeatable pass/fail case only when the same failure
returns after that fix. Write a check before any failure only when code can
decide the rule and the check has been seen to fail once. Check observable
behavior, never wording, headings, or text patterns, and do not turn one past
failure into a universal requirement.

When a wrong run of the skill would be costly, such as one that merges,
deletes, spends, or sends, run a forward test: give a fresh agent a realistic
request and the skill, without the expected answer, in a disposable workspace,
then read what it did. One forward test inside the current session with no
outside effects needs no separate approval. A batch of runs, a run billed per
call, or a run against a live system needs the skill owner's approval first.

No runner is required. When a kept case needs rerunning, a plain script or
[Promptfoo](https://www.promptfoo.dev/) is enough. This package ships no runner
configuration.

## Deliver

Check the final package's local links, dependencies, and host conventions.
Report the package location, the checks observed, and anything unverified, and
claim only what was observed. For public migrations, replace private examples
with synthetic inputs that preserve the behavior and difficulty being tested,
and inspect the whole copy for leaks. Keep the expected result of any kept case
outside the runtime instructions. Follow the host's release and installation
process.

## Sources

The [Agent Skills specification](https://agentskills.io/specification) owns the
package format. The approach draws on Anthropic's `skill-creator` and Codex's
`skill-creator`. Where either differs from the specification or from this
package, this package governs.
