# Applying report effects

Release A has one built-in effect surface: deterministic preparation and
structural verification of a report-register operation. The skill does not
invoke GitHub or any other provider. Source effects remain unavailable.

## Prepare

First run `normalize-github-register` over a complete GitHub snapshot as a
preflight. Then pass that same raw complete snapshot to `effect-v1` with
`schema: repo-gardener-effect-input/v2`, `phase: prepare`, and exactly one
report operation. Preparation normalizes the snapshot again inside its own
validation path.

The operation contains a history kind, run identity, bounded payload, the full
next row set, and the human projection. Preparation deterministically derives
the repository-qualified operation ID from stable identities, the current
revision/head, kind, and payload. It returns immutable prepared body and
comment strings, the operation fingerprint, and exact expected transitions.
Do not edit or regenerate those strings after preparation.

The caller alone decides whether it is authorized to invoke its GitHub tools.
Caller booleans, verdicts, report text, observed state, and marker claims are
not accepted as authority inputs. This package defines no custom wrapper,
provider client, credential, or cryptographic service.

## Verify

After any caller action, obtain a complete issue including its provider comment
total and all comment pages. The flattened page count must equal that total;
otherwise verification remains ambiguous and permits no one-tail repair. Run
`effect-v1` again with `phase: verify`, the immutable prepared object, the
original complete pre-read, the complete post-read, and one write-attempt
classification: `none`, `denied-before-write`, or `possible`.

The result is exactly one terminal outcome:

- `observed`: pre-read matches the prepared base and post-read contains the
  exact prepared body and comment;
- `already satisfied`: both reads already contain that exact target and the
  write attempt was `none`;
- `failed`: the write was denied before execution and exact pre/post snapshots
  are unchanged; or
- `ambiguous`: every other state, including unavailable reads, incomplete
  pagination, foreign changes, uncertain deduplication, or partial application.

All normalized snapshots report `provenance: unverified`. A positive structural
match proves only that the expected report material is present. It never grants
source, provider, pull-request, merge, or PostHog authority.

## Recovery

There is no blind retry. Reuse the original prepared object and operation ID.
If the target is already exact, perform zero writes. If the body is exact and
its anchor is exactly one receipt ahead of history, append the exact prepared
comment once without rewriting the body, then perform a complete readback. Any
other mismatch, changed precondition, comments-ahead state, or multiple gap
remains ambiguous and permits no repair.

## Completion

`reconciliation-v2` combines the verified report outcome with the exact
nine-lane manifest, nine terminal lane receipts, and a disjoint completion
partition containing the report operation plus all nine lane operation
identities. `run-closed`, a positive internal effect verification, and all
lanes complete or not applicable advance the run to `Learn`. Otherwise stop at
the last proven stage and preserve blocked or ambiguous work explicitly.
