# Cross-cutting measurement integrity

Use this preflight during reconciliation when the repository has product or
operating metrics and a configured provider-enforced read role can inspect a
reporting sink. It contributes evidence to the nine lanes; it is not a tenth
lane, a separate schedule, or an authority to mutate either source.

## Establish the contract

Read the repository's canonical strategy, product, and data definitions; its
executable event or metric schemas; generated lineage references; and the
declared durable system of record. Prefer executable definitions over generated
references and generated references over descriptive research. A reporting
sink is evidence, never product truth, unless the repository explicitly and
mechanically establishes otherwise.

For each metric inspected, require an explicit purpose, grain, entity identity,
time window and timezone, exclusions, durable authority, reporting
representation, and late-arrival or freshness rule. Run reconciliation only
when these are sufficient for a like-for-like comparison. Otherwise return
`metric contract missing` with the exact missing fields and an issue-ready
recommendation; do not guess a denominator, cohort, conversion, retention,
revenue, or cost definition.

## Run the bounded preflight

Use the repository's existing validation commands first. Then, within available
read-only roles and a bounded current window, check:

- executable schema, generated-reference, and observed event/property
  agreement, including required fields, types, enums, environment or release,
  and internal/test actor exclusions;
- freshness and ingestion lag, future timestamps, stable-event duplicates,
  identity continuity, and unexpected new or disappeared events or properties;
- observed property names against repository privacy rules, reporting only the
  prohibited category and bounded evidence reference rather than raw payloads;
- reporting facts against the same-grain durable facts for metrics whose
  authority and window are explicit; and
- currency, unit, refund, credit, and provider-cost consistency when a durable
  billing or cost ledger exists.

Classify each mismatch as expected consent or privacy exclusion, ingestion lag,
historical or backfill caveat, duplicate, identity mismatch, instrumentation
defect, or unknown. Blank reporting data is `blank reporting data`, not zero
product activity. At low volume, exact schema, privacy, duplication, and
reconciliation failures remain actionable; distributions and rate changes stay
hypotheses with their sample size, denominator, window, and uncertainty.

## Feed reconciliation

Return one cross-cutting result inside the reconciliation decision evidence,
not another Scout Receipt. For every inspected metric, report its disposition,
authority, window and timezone, grain, numerator, denominator, exclusions,
uncertainty, reconciliation result, and bounded evidence references; use `not
supplied` for unavailable observed values. Include every `metric contract
missing` result and state `blank reporting data is not zero product activity`
whenever the reporting read is blank. Attach each material finding to every
contributing lane and assign its owning lane from the remediation it actually
requires.
When the relevant measurement slice fails, its behavior data cannot support a
product hypothesis or conclusion. A defect that prevents reconciliation of a
canonical metric or blocks a critical flow or trusted decision qualifies as a
deep target unless it is coalesced with the same underlying investigation.
Missing optional read access reduces only measurement coverage.

The report contains aggregates, bounded evidence identities, and secure
provider links. It contains no customer identity, raw event payload, free text,
secret, prompt, transcript, resume, or recording, and it performs no customer
outreach. An authorized owner may inspect affected identities later through the
source system.
