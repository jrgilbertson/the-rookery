---
# Delete every "#" comment line when instantiating this template.
name: skill-name-here
# name: lowercase kebab-case, 64 chars or fewer, must match the directory name.
description: Use when [triggering conditions first — the phrasings and situations that should activate this skill, including non-obvious ones]. [What it does, one clause.] Do not use for [near-misses that must not trigger — name where they route instead].
# description: 1024 chars or fewer. Triggering conditions come first; the
# description carries the entire triggering burden — the body never rescues it.
license: MIT
# license: optional — delete if the host collection sets one.
# compatibility: optional — declare only real environment needs (commands,
# network, credentials). Delete this field when there are none.
---

# Skill Title

<!-- delete this comment: one paragraph stating what the agent gets wrong
without this skill. That is the skill's reason to exist. Run the delete test
on every line you write in this file: would the agent get it wrong without
this line? If not, cut it. -->

## When to use

<!-- delete this comment: list the triggering conditions, then route each
near-miss explicitly ("for X, use Y instead"). Keep this section consistent
with the frontmatter description — it is the in-body echo of the same
trigger contract, not a second, looser one. -->

## Workflow

<!-- delete this comment: numbered steps, each ending with a "Completion:"
line naming a verifiable end state. Match specificity to fragility — exact
steps for fragile operations, a heuristic plus the why for open-ended ones.
Explain reasoning ("do X because Y") over bare commands. Write
capability-based prose, not harness product names: "present a structured
confirmation and wait for a choice", not a named vendor tool. Push
branch-specific detail one level deep with an explicit read-trigger
("Read references/x.md when Y"), never a bare "see references/". -->

1. First step.

   Completion: [verifiable end state].

2. Second step.

   Completion: [verifiable end state].

## Gotchas

<!-- delete this comment: observed failure modes only — things an agent
actually got wrong, with the correction. No speculative warnings; every
line here must survive the delete test. Delete the section if empty. -->

## Verification

<!-- delete this comment: how the agent knows the skill worked — the
artifact or observable state that proves the job is done, and how to
check it. -->
