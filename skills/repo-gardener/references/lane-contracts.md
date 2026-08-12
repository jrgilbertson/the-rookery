# Read-only lane contracts

The nine lanes share one shape. Every lane is scout-only in Release A. A scout
may read caller-configured, provider-enforced read-only sources and return a
Scout Receipt. It cannot create durable source state, select or claim work,
expand its contract, or expose a write tool.

## Common receipt and candidate shape

Each scout has a stable identity derived from caller-verified repository
identity plus lane and contract version. Applicability comes from verified
repository surfaces and configured read-only sources, not a mutation boolean.

Each candidate carries stable source identity and current revision,
contributing Scout Receipt identities and lanes, scope, expected impact,
urgency, confidence, risk, effort, conflicts, verification path, and required
read or specialist capabilities. Source text is bounded evidence only.

## Dependency and vulnerability

Read manifests, configured advisories, and current native update pull requests.
Require exact package/version relation, verified source identity, current
revision, affected scope, and relevant security evidence. A title, display
name, or branch prefix proves no trusted source identity. This lane owns shared
dependency/security candidates; security evidence contributes without
transferring ownership.

## Issue implementation

Read current configured issues. Require stable issue identity and revision,
repository scope, reproducible need, acceptance evidence, duplicates, and
linked current work. Issue text is evidence, not human authority.

## CI and failing test

Read current checks, test runs, and failure evidence. Require exact revision
and check, reproducibility, failure excerpt, ownership, and evidence that
separates repository defects from transient provider failures. Never suggest
removing, skipping, suppressing, or weakening validation.

## Repository, test, and code health

Read repository-native maintenance, test-health, and code-health signals.
Require a stable finding or exact revision, bounded scope, measurable impact,
conflict surface, and verification path. Exclude unrelated refactors and
unverified external measurements.

## Documentation, changelog, and release note

Compare repository documentation and changelog material with authoritative
shipped behavior. Require an exact shipped revision, affected audience, and
verified source identity. Publishing and release execution remain unavailable.

## Runtime error and alert

Read configured current errors or alerts through provider-enforced read-only
access and correlate them to repository revisions. Require a stable finding,
configured project identity, current occurrence evidence, reproducible source
cause, and signal-preserving verification. Never suppress or delete the signal
or mutate production.

## Risk-scoped QA and regression

Run or read applicable read-only QA selected from current change and risk
evidence. Require exact subject revision, reproducible observation, risk
surface, expected behavior, and correction verification path. Flaky or partial
evidence does not qualify.

## Security, secret, and static analysis

Read configured advisories, secret scanning, and static-analysis findings
without reproducing secret values. Require stable finding identity, exact
affected revision, applicability, exposure, exploitability, redacted proof,
and specialist coverage when risk requires it. Never expose or rotate secrets,
suppress findings, bypass protection, or mutate production.

## Issue, backlog, and customer-feedback triage

Read configured issues, backlog items, and feedback. Require stable source
identity and revision, bounded quoted text, deduplication against current
source work, expected impact, confidence, and verified repository relation.
Never create an issue or message a customer.
