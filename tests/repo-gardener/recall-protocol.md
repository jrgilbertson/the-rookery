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
`date | git rev | recall probe (run N) | hits: A…; new-unlisted: … | note`.

Scoring rules:

1. A hit is the same underlying defect — same mechanism, not same wording.
   Example: the reference row "quota recomputed from owner-deletable rows" is
   hit by a candidate that names deletable source rows behind a quota, even if
   it cites a different entry point; it is not hit by a generic "audit quota
   logic" recommendation.
2. Per-run recall is expected to be low: the health lane reads one rotation
   slice per run, so recall accumulates across runs. The signal that matters
   is a run whose slice contains reference rows and reports none of them.
3. `live`-surface rows are context only and never scored as misses. The
   recall denominator is the set of non-`live` rows still valid at the scored
   revision; re-verify a row before scoring a miss against it, and mark
   expired rows in the machine-local reference so they leave the denominator.
4. Anti-findings score precision: a run reporting one as a defect is a false
   positive.
