---
title: "Trace native terminal failures before changing capture admission"
date: 2026-10-05
category: best-practices
module: "creating-portable-skills skill verification"
problem_type: best_practice
component: testing_framework
severity: high
applies_when:
  - "A native child result has output but its command lifecycle is missing"
  - "A capture repair could change sandbox denial detection or approval recovery"
tags: [codex, promptfoo, evals, capture, sandbox, telemetry, provenance]
---

# Trace native terminal failures before changing capture admission

## Context

A native tool can return completed output while omitting the execution events
needed to admit an eval. The [issue #192](https://github.com/jrgilbertson/the-rookery/issues/192)
investigation traced this shape in Codex 0.160.0. An ordinary exit 1 after
printing a harmless source comment containing `sandbox` triggered its
[denial heuristic](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/sandboxing/src/denial.rs).
The [early process check](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/core/src/unified_exec/process.rs)
returned a denial before the
[manager's command-start publication](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/core/src/unified_exec/process_manager.rs).
Under approval policy Never, the orchestrator returned the terminal denial;
the exec handler still converted its captured output into a completed tool
result. Recheck this chain when changing native versions.

Removing a broad keyword can fix that comment example while missing a genuine
OS denial whose application catches PermissionError and prints a message such
as `sandbox blocked file access`. A concrete protected-file control exposes
that regression. Denial detection also governs recovery, so a telemetry defect
needs its own repair boundary.

## Guidance

1. Compare child starts/results, native runtime starts/ends, and provider command
   items by call ID. Keep their closed inventory check. Output alone does not
   supply a missing runtime start or prove a native command projection.
2. Trace the native producer before changing the consumer. Reproduce an ordinary
   nonzero exit with the exact captured bytes, plus a genuine sandbox denial
   and an unsandboxed control. Verify the missing events against native code.
3. Publish the terminal failure's lifecycle after approval and retry handling
   finishes, using the native event mechanism and original captured result.
   A failed first attempt followed by successful recovery must use the normal
   success path. An internal retry must not create another public pair for the
   same invocation.
4. Preserve denial classification, authorization, and the returned error.
   Retain the allocated attempt ID without advertising a live resumable process.
   Keep captured bytes and exit code intact. Unified-exec stdout represents its
   merged terminal stream; it does not identify which child stream wrote a byte.
5. Exercise the producer with native integration tests using mocked model
   responses. Require exactly one item pair and runtime pair, matching IDs,
   retained fixture bytes, and the original failure status. A protected write
   must remain blocked under Never. Check cancellation between publication
   events independently and state the limits of the check.

The native [session event path](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/core/src/session/mod.rs)
records legacy command events for rollout tracing, and the
[trace converter](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/rollout-trace/src/protocol_event.rs)
maps those events into runtime pairs. Repairing that producing path can restore
both kinds of evidence. Preserve unknown timing and attribution as limitations;
do not present zero duration as measured elapsed time.

## When to Apply

Use this approach for native telemetry omissions with an output-bearing terminal
result. It does not establish a new creator execution, admit an old incomplete
capture, or prove arbitrary shell reads. Command support is a separate check:
the historical parser accepted one literal cat read and could not establish
compound-command provenance. The current skill suite uses stock Promptfoo SDK
assertions and no strict capture gate or upstream fork. Its skill-use observations
do not establish this stronger proof. Historical unsupported captures remain
Unmeasured.

## Related

- [Isolate native state for ephemeral Codex evals](isolate-native-state-for-ephemeral-codex-evals.md)
  covers the separate native storage boundary.
- [Put the test seam in the environment](../conventions/keep-the-test-seam-out-of-the-shipped-skill.md)
  keeps eval instrumentation out of the shipped skill.
