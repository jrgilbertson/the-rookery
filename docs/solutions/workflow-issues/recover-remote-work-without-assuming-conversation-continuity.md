---
title: "Recover remote work without assuming conversation continuity"
date: 2026-10-14
category: workflow-issues
module: "Remote agent orchestration"
problem_type: workflow_issue
component: development_workflow
severity: medium
applies_when:
  - "Remote agent panes survive but terminal handles or conversation state have changed"
  - "Preserved worktrees and task receipts can reconstruct unfinished work"
tags: [orca, remote-development, recovery, orchestration, worktrees]
---

# Recover remote work without assuming conversation continuity

## Context

An Orca paired-server recovery investigation found reachable remote workspaces
and agent panes whose current terminal handles differed from saved dispatch
receipts. Ordinary identity check-ins reached several agents in those panes,
but their replies described fresh first-message conversations without the
original task, findings, or authority. Pane continuity had survived; conversation
continuity had not.

This was observed with Orca 1.4.223 on the client and server. The investigation
recovered enough context from preserved worktrees, Git state, task logs, and
verification receipts to prepare bounded continuation briefs. It did not
establish a fix for the original routing or dispatch-identity failures.

## Guidance

1. **Reacquire handles on the execution host.** Read the current version-matched
   Orca guides and list its current terminals. Check the returned runtime,
   execution host, coverage, and truncation before interpreting an absent
   handle. Match saved panes through supported identifiers and receipts;
   a checkout path alone does not identify an agent.
2. **Confirm what the current agent knows.** A successful input receipt proves
   delivery or turn acceptance, according to its fields. Read the actual reply
   before claiming retained context, active execution, or ownership. A current
   handle for the same pane does not restore the old Task or Dispatch binding.
3. **Reconstruct the work from durable artifacts.** Record the exact checkout,
   branch, commit and tree, dirty changes, verification inputs and results,
   remaining scope, and current authority. Preserve uncommitted changes and
   other recovery evidence outside public source. Use original conversation
   logs when available; their absence need not block a continuation whose
   requirements and evidence are otherwise complete.
4. **Resolve writing ownership before continuation.** Name one writer for each
   source checkout and exclude uncertain agents from the assignment. If an old
   writer's status remains unknown, preserve its checkout. With scoped
   authorization, a separate worktree and branch from a verified recovered base
   can provide isolation. Verify that the base includes the recovered work and
   preserve dirty differences before proceeding. Isolation prevents checkout
   contention; it does not prove the old writer exited or recover missing work.
5. **Keep the transport model explicit.** A paired remote server owns its
   workspaces and agents. SSH relay sessions have a different disconnect and
   lease model. Apply the installed guide for the actual connection mode rather
   than transferring an SSH grace-period assumption to a paired server.

## Why This Matters

Terminal handles, pane identity, conversation context, and task ownership are
separate pieces of evidence. Treating any one as proof of the others can send
work to a fresh agent with incomplete instructions or create competing writers.
Conversely, requiring the original conversation after a complete artifact-based
reconstruction can hold up work for an optional recovery step.

A missing current binding remains unknown unless supported host coverage and
lifecycle evidence resolve it. A point-in-time process lookup with no match is
not proof that a historical writer exited or cannot write again. Session-history
resume can start another process; it must be evaluated separately from repairing
an orchestration binding.

## When to Apply

Use this approach when remote source and receipts remain available but a client
reconnect, changed handle, or fresh conversation makes old coordination state
unreliable. It does not justify replacing unknown agents, changing access,
enabling history indexing, or editing internal orchestration records.

## Examples

In the observed recovery, one coordinator resumed a bounded finish-only task
from saved review artifacts. Two others completed read-only reconstruction and
prepared scoped continuation briefs. One then verified its immutable base and
preserved dirty changes before attempting a separate native worker launch; that
launch reported an agent-readiness timeout and changed identity, so source
execution remained unconfirmed at the documentation checkpoint. Another
confirmed a proposed sole writer was ready, with implementation still awaiting
its scoped assignment.

Owner-confirmed cleanup also removed eligible archived worktrees while retaining
uncertain, dirty, active, and evidence-bearing resources. These were recovery and
cleanup outcomes, not proof that routing had been repaired. The client quit was
canceled after a running-process warning, so this investigation did not test
recovery across an actual client restart.

## Related

- [Stop only the work a missing fact blocks](stop-only-the-work-a-missing-fact-blocks.md)
- [Trace native terminal failures before changing capture admission](../best-practices/trace-native-terminal-failures-before-changing-capture-admission.md)
- [Orca CLI reference](https://www.onorca.dev/docs/cli/reference), for runtime-scoped handles and host coverage
- [Orca remote servers](https://www.onorca.dev/docs/remote-servers), for paired-server ownership
- [Orca SSH connections](https://www.onorca.dev/docs/ssh), for relay behavior
- [Orca session history](https://www.onorca.dev/docs/agents/session-history), for resume behavior
