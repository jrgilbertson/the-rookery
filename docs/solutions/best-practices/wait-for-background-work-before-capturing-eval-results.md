---
title: Wait for background work before capturing eval results
date: 2026-10-02
category: best-practices
module: skill evaluation
problem_type: workflow_issue
component: testing_framework
severity: high
applies_when:
  - "An eval executor can launch background agents or shell commands"
  - "A runner closes the executor session before grading its artifacts"
tags: [skill-evals, background-tasks, transcript-integrity, cost-accounting]
---

# Wait for background work before capturing eval results

## Context

A native-CLI skill evaluation produced a final parent response while background
work was still running. The capture helper interpreted the parent's `end_turn`
as completion, copied the workspace, and closed the terminal. That stopped
unfinished work and left a plausible answer and partially populated artifacts
that could still pass grading.

Waiting for background agents fixed one captured failure, but a later shell
command exposed the same problem through a different launch mechanism. Its
tool result acknowledged a background task rather than reporting its outcome.
An agent counter alone did not cover that task.

Earlier investigation also selected an older transcript from the same
workspace and lost a separate watcher under memory pressure (session history).
Neither a transcript found by workspace name nor a stopped watcher establishes
the state of the actual execution.

## Guidance

Separate three observations: the parent finished speaking, launched work
finished, and the parent processed its result. Before taking the final snapshot
or closing a session:

1. Select the transcript belonging to this execution, using run identity and
   start time. Retain the raw events, including tool calls and native task
   metadata.
2. Track each observed background launch by the native task or tool identity.
   Treat a launch acknowledgment as pending work. Require an authoritative
   completion record for that same identity, or a current native pending-agent
   observation where that mechanism supplies one.
3. If a background result arrives after the parent response, wait for a new
   parent response that follows and processes it. A repeated event, stale
   timestamp, or replay of the earlier message is not evidence of this step.
4. Capture the final workspace, transcript, and available usage only after
   these observations agree. Missing identities, unsupported task formats, or
   contradictory completion records leave completion unverified.

This is a check of the tasks the harness observed through its native tools. It
does not prove that every possible detached process has stopped. Inspect the
actual event shapes in the installed harness, and keep unknown shapes visible
rather than assuming another harness emits the same fields.

Preserve interrupted attempts and their original grades. Report the capture
limitation separately and exclude them from claims based on completed runs.
Missing capture leaves completion unverified. The current repository workflow
is selected through [SKILLS.md](../../../SKILLS.md#evaluation-workflow).
Replacement evidence needs the same frozen package, inputs, assertions, target,
and material settings. Apply the completion check to both comparison arms.

Collect available parent, background-agent, nested-command, and simulator usage
before teardown. Keep recovered partial usage and mark missing cost evidence
as unknown. A scored result and a complete cost record are separate claims.

## Why This Matters

Premature teardown changes the execution being measured. A passing artifact
check can describe a partial workspace, and a failure can reflect killed work
rather than the skill's behavior. Comparing those captures with completed runs
can therefore misstate both quality and cost.

## When to Apply

- The executor delegates work or launches a command in the background.
- The runner uses a parent response or tool result to decide when to close a
  terminal and grade artifacts.
- Historical results contain final prose alongside unfinished task evidence.

## Examples

| Observed sequence | Capture decision |
| --- | --- |
| Parent final response; native agent count still positive | Wait. The parent turn ended while delegated work remained. |
| Background shell launch returns a task ID; parent final response | Wait. The task ID acknowledges launch. |
| Matching shell completion; parent has not responded again | Wait for the parent to process the result. |
| Matching completion; genuinely later parent response; no other observed work pending | Capture the final artifacts and usage. |
| Task identity missing or completion refers to a different task | Preserve evidence and mark completion unverified. |

Test the completion detector against actual failing transcript prefixes and
small event-sequence controls. Include replayed messages, stale zero counters,
mismatched task IDs, and a positive sequence with a later parent response. A
fixed sleep or an idle terminal is not a substitute for completion evidence.

## Related

- [Blind cross-model grading through native schema flags](blind-cross-model-grading-through-native-schema-flags.md)
  covers the integrity of the returned grade; execution capture needs its own
  evidence before that grade can support a comparison.
- [Reuse the shipping pipeline instead of a managed run protocol](../architecture-patterns/reuse-the-shipping-pipeline-instead-of-a-managed-run-protocol.md)
  explains why this finite task check should not grow into a parallel workflow
  registry or an impossible proof about the whole process tree.
