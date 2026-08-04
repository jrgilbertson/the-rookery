Consumers occasionally enqueue the same scheduled job twice — retries on
their side, double-clicks on ours. This deduplicates scheduled jobs that
share an idempotency key within a 10-minute window.

- New `idempotency_key` column with a partial unique index over the
  dedupe window.
- The scheduler checks for an existing key before inserting; duplicates
  are dropped with a `jobs_deduplicated` counter metric.
- Keys are optional; jobs without one behave exactly as before.
