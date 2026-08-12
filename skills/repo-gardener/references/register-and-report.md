# Register and report contract

The live GitHub report is one issue body plus its comments. This package
normalizes that provider snapshot, prepares exact report material, and verifies
the resulting snapshot. It supplies no provider client, credential, lock,
workflow database, or write authority.

## Live grammar

The issue body contains exactly one fenced JSON object between
`orchestrator:current-portfolio:v1:begin` and
`orchestrator:current-portfolio:v1:end`, followed by the human projection. The
object is exact `orchestrator-register/v1` data with repository, report-issue,
and writer identities; revision and last-operation fields; one history anchor;
and zero to seven rows.

Each history comment contains exactly one JSON receipt between
`orchestrator:history-receipt:v1:begin` and
`orchestrator:history-receipt:v1:end`. Receipts form a hash-linked sequence from
`GENESIS`. The body anchor contains the complete latest receipt so an exact
one-comment tail gap can be repaired.

`normalize-github-register` accepts the configured identities, current issue,
and every comment page. It requires complete pagination, exact identity and
schema matches, exact markers, a valid chain, and a byte-stable managed body.
It returns a structurally checked state with `provenance: unverified`.
Structural validity does not authenticate the snapshot and grants no source,
provider, pull-request, merge, or PostHog authority.

## Rows, receipts, and bounds

Current Portfolio is the only ownership view. `To do` and `In process` rows
both consume the seven-row limit. Terminal outcomes belong in Run History; a
terminal row must be released or reported with owner release as its exact next
action.

The installed lane inventory and portfolio limit come only from
`assets/policy-template.yaml`. Every run has exactly nine lane receipts, one
for each lane. Receipt outcomes are `complete`, `not applicable`, or
`incomplete`; missing coverage is never zero findings.

Identity is caller-supplied bounded ASCII, not prose, title, URL, or elapsed
time. Machine identities are limited to 128 characters, display text to 512
Unicode code points, receipt JSON to 16 KiB, and the managed body to 48 KiB.

## Deterministic report operations

`effect-v1` with schema `repo-gardener-effect-input/v2` has two phases:

1. `prepare` consumes one raw complete pre-read snapshot and an operation,
   normalizes the snapshot internally, derives a deterministic
   repository-qualified operation ID, and returns immutable body and comment
   strings plus exact pre- and post-state fingerprints.
2. `verify` consumes that prepared object, the same complete pre-read, a
   complete post-read, and the caller-reported write-attempt class. It compares
   exact material and returns `observed`, `already satisfied`, `failed`, or
   `ambiguous`.

Preparation never invokes a provider. The caller may apply only the returned
body/comment strings under its own separately configured authority. The model
must not reconstruct, edit, or derive provider arguments from report prose.

Terminal newline differences accepted by the normalizer do not change the
canonical prepared material. A matching target already present yields
`already satisfied` and requires zero writes. `failed` is available only when
the caller reports `denied-before-write` and exact pre/post snapshots are
unchanged. Any uncertain, incomplete, or mismatched state is `ambiguous`.

## Recovery

Never retry blindly. Re-run normalization and verification first.

- Exact body and comment match: return the existing result with zero writes.
- Body is exactly the prepared body and its anchor is exactly one receipt ahead:
  append the immutable prepared comment once, do not rewrite the body, then
  read every page and verify again.
- Any other partial, changed, foreign, or multi-gap state: preserve ambiguity
  and perform no write.

No persistence claim is valid without a positive exact verification.
