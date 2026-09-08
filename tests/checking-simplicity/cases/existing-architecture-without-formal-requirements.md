# Existing architecture can be assessed without formal requirements

Provenance: the owner found that architecture is the main source of AI
overengineering, while the prior skill treated formal requirements as a
prerequisite and did not name existing systems as a review subject.

## Prompt

> Assess this existing system architecture for simplicity. No formal
> requirements document survives, and no code cleanup or edit is requested.
> Reports are generated synchronously for one authenticated API caller; the
> caller waits for the result. Preserve authorization, bounded-memory
> streaming, cancellation, and one completion audit event. Failed requests may
> be retried manually. The service runs in one process.
>
> The API currently publishes a command to an event bus. A provider registry
> selects the only report generator, a durable queue and worker execute it, a
> retry state machine and dead-letter store track failures, and a status
> endpoint plus environment policy expose job state. There is one provider, no
> background caller, no restart-survival or automatic-retry requirement, and
> no observed status-endpoint requests. Compare this architecture with a direct
> request-scoped service that reuses the existing authorization, streaming,
> cancellation, and audit helpers. Return the assessment only.

## Expected behavior

- [ ] Does not refuse the assessment merely because no formal requirements
      document exists.
- [ ] Leads with a recommendation to simplify and names the direct
      request-scoped service before its supporting reasons.
- [ ] Compares the whole-system approaches before accounting for individual
      concepts.
- [ ] Removes or defers the event bus, provider registry, queue, worker, retry
      state, dead-letter store, status endpoint, and runtime policy because no
      current consumer or protected boundary needs them.
- [ ] Preserves authorization, bounded-memory streaming, cancellation, one
      completion audit after success, manual retry behavior, and focused tests.
- [ ] Does not edit code, perform behavior-preserving cleanup, or approve
      implementation or shipping.
