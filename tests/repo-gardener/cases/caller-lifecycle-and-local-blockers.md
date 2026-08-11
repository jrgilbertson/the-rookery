# Caller lifecycle and local blockers

Provenance: Observed failures conflated scheduling/liveness/ownership, stopped unrelated work, and settled an assignment before its one-shot terminal report.

## Prompt

> Evaluate four synthetic caller states. (1) Scheduling is paused, the current
> invocation is live, and it owns the repository executor. (2) One report
> effect is ambiguous while an independent read-only audit can continue. (3)
> The invocation is cancelled and has no executor receipt. (4) A one-shot
> terminal-report capability remains active after all work; two follow-on
> decisions need durable gates, and both this assignment and its caller could
> persist them.

## Expected behavior

- [ ] Scheduling, invocation liveness, and executor ownership are separate caller facts; no receipt substitutes for another.
- [ ] The local ambiguity stops only the report operation and dependents; independent audit is `continued`.
- [ ] The cancelled invocation performs no write and does not infer ownership release from cancellation.
- [ ] State 4 assigns each decision exactly once: the current assignment may persist it only with proven wrapper readback; every unpersisted decision is carried in exactly one terminal report for the caller.
- [ ] It keeps the capability active and does not settle itself first; it stops only after caller acceptance.
