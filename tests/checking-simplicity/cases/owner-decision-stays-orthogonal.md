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

- [ ] Uses the compact assessment contract with one binary `Verdict`, a
      `Review context`, bound `Subject`, `Owner decision required`, findings,
      and protected complexity.
- [ ] Asks exactly the material owner decision: whether the rebuild must
      survive client disconnect or continue asynchronously.
- [ ] Keeps `Owner decision required` separate from `PASS` or
      `CHANGES_NEEDED`; it does not invent a third verdict.
- [ ] If synchronous lifetime is acceptable, names a direct request-scoped
      rebuild as the smallest approach and removes the job system.
- [ ] If durable asynchronous work is required, protects only the minimum
      queue and status behavior justified by that requirement.
