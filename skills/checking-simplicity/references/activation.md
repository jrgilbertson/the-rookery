# Activating the simplicity checkpoint

The checkpoint is most valuable before complexity hardens: when a completed
requirements or approach draft moves into implementation planning, when an
implementation plan moves into execution, and at an in-build decision to add
machinery.

## Description-owned discovery

The skill description owns normal automatic routing. It names both planning
handoffs so a harness can select the skill when the current request contains a
reviewable subject and reaches either transition, even if the user does not say
"simple." Keep those transition cues in the description rather than in
always-loaded repository instructions.

Description routing is semantic and model-selected. It is a discovery path,
not deterministic enforcement. In a staged workflow, each caller should route
the newly reached task against the available skill catalog instead of assuming
that skill selection from an earlier stage still applies.
After the current unchanged subject receives an independent `PASS` with
`Owner decision required: no`, the newly reached task belongs to the next
planner or executor. Do not route the same subject back through this checkpoint.

## Explicit invocation

Ask for `checking-simplicity` after a draft approach exists and before coding.
Use the harness's ordinary skill syntax when it has one, such as
`$checking-simplicity`, or say the skill name directly. For an independent
result, have a fresh context review the draft and return its assessment to the
implementation context.

Examples that should route here include:

- "Simplify this finished implementation plan before we build it."
- "Choose the smallest reliable implementation for this completed approach."
- "Which parts of this architecture proposal solve only hypothetical future
  needs?"
- "For this completed approach, check whether the existing mechanism already
  satisfies the requirements."
- "Right-size this current plan without dropping required behavior."
- "Check this completed requirements draft before implementation planning,
  without inventing how to build it."

These requests are discoverable but not guaranteed to activate the skill.

## Caller-owned sequencing

An automated caller can enforce either planning handoff as three explicit
stages:

1. produce a reviewable requirements draft, approach, or implementation plan
   without crossing into the next planning or execution stage;
2. run `checking-simplicity` in an independent context; and
3. cross that boundary only after `PASS` with `Owner decision required: no`.
   Resolve any owner decision, or revise a `CHANGES_NEEDED` subject, then check
   the resulting subject again in a new uninvolved context.

These stages make ordering observable without a harness-specific hook.
Apply these recheck rules explicitly:

- after an owner decision, check the resulting subject through a new context
  uninvolved with that decision or any revision;
- treat a result from anyone whose earlier review shaped the subject as
  unverified, then use a context with no prior involvement; and
- after `CHANGES_NEEDED`, revise the subject and use a new context uninvolved
  with the prior findings or revision.

In every branch, state and enforce that the boundary stays blocked until the
current resulting subject receives an independent `PASS` with
`Owner decision required: no`. Sending it for another review is not permission
to proceed.

When an independent clean result already covers the current unchanged subject,
the checkpoint is complete. Continue with the next planner or executor. A new
checkpoint is required when required behavior, a protected constraint, or an
implementation concept under review changes. A caller using the result as a
gate must also treat any subject-content change as stale, including a copy edit.

Use native fresh-context dispatch when the harness provides it. Otherwise stop
before implementation and prepare a separate-session handoff containing the
complete requirements and exact plan or implementation subject from the
skill's `Subject` contract. Keep the checkpoint unverified until that session
returns the full assessment. Before proceeding, the caller re-reads the
complete subject and confirms that neither its content nor its binding changed.
If either changed, the caller sends the updated subject through another
independent review before implementation.

A same-context assessment remains advisory; it is not the fallback.

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
description, explicit, and caller-owned routes miss material checkpoints, and
only when the harness exposes a stable semantic event for that transition.
