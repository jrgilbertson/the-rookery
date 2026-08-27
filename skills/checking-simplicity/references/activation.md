# Activating the simplicity checkpoint

The checkpoint is most valuable at the plan-to-build boundary, before the
first implementation edit. There are three useful activation levels.

## Explicit invocation

Ask for `checking-simplicity` after a draft approach exists and before coding.
Use the harness's ordinary skill syntax when it has one, such as
`$checking-simplicity`, or say the skill name directly. For the strongest
separation, have a fresh context review the draft and return its assessment to
the implementation context.

Examples that should route here include:

- "Simplify this plan before we build it."
- "Choose the smallest reliable implementation."
- "Which parts of this architecture solve only hypothetical future needs?"
- "Check whether the existing mechanism already satisfies this request."
- "Right-size this approach without dropping required behavior."

The skill description makes these semantic requests discoverable. It is not a
literal keyword scanner, and description routing remains model-selected rather
than guaranteed.

## Persistent caller policy

When the checkpoint must happen even if the user never says "simple," put the
scheduling rule in the caller's repository instructions. Keep one canonical
copy and import or mirror it only where a harness cannot read the same file.

```text
Before the first implementation edit for a behavior change, invoke
checking-simplicity in a fresh context after requirements are clear and a draft
approach exists. Skip only read-only work and prescribed mechanical edits with
no design choice. Re-run it if required behavior or implementation scope
materially changes. Revise the approach before implementation when the result
is CHANGES_NEEDED, and resolve any owner decision before implementation. Use a
new uninvolved context for each recheck.
```

This policy observes the transition that matters. Complexity words in the
original prompt do not: the agent often invents the abstraction or workflow
later, while drafting its approach.

## Caller-owned sequencing

An automated caller can enforce the same boundary as three explicit stages:

1. produce a draft approach without editing implementation files;
2. run `checking-simplicity` in an independent context; and
3. allow implementation only after `PASS` with
   `Owner decision required: no`. Resolve any owner decision, or revise a
   `CHANGES_NEEDED` approach, then check the resulting approach again in a new
   uninvolved context.

This three-stage design makes ordering observable without a harness-specific
hook.

## Why there is no bundled hook

Git hook managers such as Lefthook run around version-control commands, after
the planning decision this skill is meant to influence. They remain useful for
deterministic tests, linting, and repository gates, not as the primary planning
checkpoint.

Codex lifecycle hooks can add context at prompt, tool, and stop events, but
those events do not mean "the draft plan is complete and implementation has
not started." A prompt hook sees the request before the agent invents its
approach. An `update_plan` tool hook sees intermediate and repeated updates,
and some valid plans never use that tool. Hook output can remind an agent to
invoke a skill; it does not directly invoke the skill inside the active turn.
See the current [Codex Hooks documentation](https://developers.openai.com/codex/hooks/).

Do not install a prompt scanner, `update_plan` hook, stop hook, or Lefthook AI
job by default. Revisit a hook adapter only after observed runs show that the
explicit and policy routes miss material plan-to-build checkpoints, and only
when the harness exposes a stable semantic event for that transition.
