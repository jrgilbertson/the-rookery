# Recall probe protocol

The dogfood host keeps a machine-local recall reference in its private
automation state; the operator's session context supplies its location, and a
scoring agent that lacks that context asks rather than searching. It is a
table of known-real findings from an owner-run deep audit
of the dogfood target, each tagged with the sensing surface expected to
rediscover it (`code` inspection, dependency signals, CI reads, or `live`
runtime probing), plus a short list of audit-rejected anti-findings. The
reference never enters any repository working tree, run report, issue, or PR,
because its rows describe unpatched weaknesses.

After each dogfood run, compare the run's candidates and recommendations
against the reference and append one line to this directory's `log.md`:
`date | skill rev | target rev | recall probe (run N) | hits: A…;
new-unlisted: <count> | note`, where the target revision is the exact commit
of the dogfood target the run sensed, so a hit or miss stays auditable after
the target moves. The tracked log carries only opaque row IDs, counts, and
non-sensitive notes; descriptions of new unlisted findings are recorded in
the machine-local reference alongside the rows, never in the tracked log.

Scoring rules:

1. A hit is the same underlying defect — same mechanism, not same wording.
   Fictional illustration (not a reference row): a row reading "the widget
   exporter trusts a client-supplied page size" is hit by a candidate naming
   unbounded client-controlled pagination in that exporter, even from a
   different entry point; it is not hit by a generic "audit the exporter"
   recommendation.
2. Per-run recall is expected to be low: the health lane reads one rotation
   slice per run, so recall accumulates across runs. The signal that matters
   is a run whose slice contains reference rows and reports none of them.
3. `live`-surface rows are context only and never scored as misses. The
   per-run denominator is the set of non-`live` rows whose tagged surface the
   run actually exercised — for `code` rows, only rows inside the inspected
   slice; cumulative recall across runs uses every non-`live` row still valid
   at the scored target revision. Re-verify a row before scoring a miss
   against it, and mark expired rows in the machine-local reference so they
   leave the denominator.
4. Anti-findings score precision: a run reporting one as a defect is a false
   positive.
