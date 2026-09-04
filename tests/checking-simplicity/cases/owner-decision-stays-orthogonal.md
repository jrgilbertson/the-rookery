# A product decision is not disguised as a simplicity verdict

Provenance: a bare fresh-context baseline on 2026-08-26 found the material
client-lifetime decision but omitted the binding assessment contract; this case
preserves the decision while verifying that it stays orthogonal to the verdict.

## Prompt

> Review a plan for `POST /reports/:id/rebuild`. The requirement says the
> request starts a rebuild and returns its result. It does not say whether the
> rebuild must continue after the client disconnects. The proposed plan adds a
> durable job queue, worker pool, retry state machine, dead-letter store, and
> job-status endpoint. Pick the simplest safe approach.

## Expected behavior

- [ ] Asks the user to decide whether the rebuild must survive client
      disconnect or continue asynchronously, with four options and the
      smallest safe option the evidence supports marked as recommended, as
      the lead or directly after reductions that are safe under every answer.
- [ ] Does not print a binary verdict, receipt, subject replay, reviewer context
      label, or owner-decision field.
- [ ] If synchronous lifetime is acceptable, names a direct request-scoped
      rebuild as the smallest approach and removes the job system.
- [ ] If durable asynchronous work is required, protects only the minimum
      queue and status behavior justified by that requirement.
