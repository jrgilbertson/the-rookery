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
against the reference, record the full result in the machine-local reference
state (row IDs hit and missed, the exact target revision sensed, and any new
unlisted findings with their descriptions), and append one ordinary line to
this directory's `log.md` in its standard format: `date | git rev | recall
probe | result | note`, where the note carries only counts (for example
"3 hits, 1 miss, 2 new-unlisted; detail in machine-local reference"). The
result is binary: the probe passes when no row on an exercised surface was
missed and no anti-finding was reported as a defect; any exercised-surface
miss or any anti-finding false positive fails the probe. Low cumulative
recall by itself neither passes nor fails a run — it is tracked in the
machine-local reference, not graded per probe. The
tracked log never carries row IDs, extra hashes, run ledgers, or finding
descriptions — auditable detail lives with the reference, which records the
target revision per probe.

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
   positive — but each anti-finding binds to the revision the audit rejected
   it at. Re-verify an anti-finding still holds at the scored target revision
   before counting the false positive; a mechanism that has since become a
   real defect expires as an anti-finding and is marked expired in the
   machine-local reference.
