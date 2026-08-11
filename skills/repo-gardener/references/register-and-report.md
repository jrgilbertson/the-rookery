# Register and report contract

Use this contract only through the caller's repository-scoped report wrapper
inside its shared executor. The package defines records, operations, checks,
rendering, and recovery. It supplies no hosted service, provider client,
portable lock, compare-and-swap claim, or workflow database.

## Canonical model

One canonical record set supplies the machine read and human report:

- `register` carries stable repository/report/writer identities, a nonnegative
  `register_revision`, history anchor, last logical operation markers, and zero
  to seven rows;
- `portfolio_row` carries stable row and source identities, source revision,
  bounded display description, exactly one state (`To do` or `In process`),
  lane, rationale, risk, budget use, evidence identities, exact next action,
  and nonnegative row revision;
- authenticated `history_receipt` records run, manifest, scout, reconciliation,
  decision, effect, and terminal facts; and
- report projection assigns `Action required`, `Merge-ready`, `Watching`, or
  `Routine`.

`repo-gardener-register/v1` is exact, not an open property bag. A row contains
only row/source identities, source revision, description, state, lane,
rationale, risk, budget use, nonempty evidence identities, exact next action,
and row revision. A history receipt contains only sequence/previous hash,
repository/writer/provider receipt/operation identities, kind, run identity,
and receipt hash. The anchor contains only sequence, head, and the complete
`latest_receipt` repair object. The top-level last-operation markers are the
stable operation identity plus a lowercase SHA-256 fingerprint. Missing or
additional fields, or an unknown version, block the register read.

Current Portfolio is the only ownership view. Both work states consume the
seven-row ceiling. Terminal outcomes belong in Run History. A terminal row is
released in the same logical update or projects `Action required` with owner
release as its exact next action. It may not silently consume capacity.

Disabled-lane projections are exactly `Routine (disabled lane)` and `Action
required (lane disabled)`.

`assets/policy-template.yaml` is the single machine source for the portfolio
limit. The deterministic contract reads `repository_portfolio_limit` from that
asset for validation and rendering; callers and tests do not carry an
independent numeric limit.

## Stable identities and bounds

Treat identity as opaque caller-verified ASCII, not title, branch, display text,
URL, elapsed time, report prose, or comment content. Bound each identity at 128
ASCII characters, untrusted display at 512 Unicode code points, a receipt at 16
KiB canonical UTF-8, and the managed body at 48 KiB. Reject over-limit machine
data; escape and truncate display-only evidence with an omission marker.

Mint one run identity per invocation and one repository-qualified logical
operation identity `(repository_id, operation_id)` before an effect. Keep
revisions and heads as mutable preconditions. Construct links only from
verified provider fields and caller configuration.

Enforce these bounds with `scripts/release_a_contract.py` before accepting a
register, receipt, Scout Receipt collection, or managed body. Prose-only size
checks are not sufficient.

## Portable operations

Every read returns either `integrity: valid` or a blocking reason plus stable
identities, schema, complete history sequence/head, body anchor, register
revision, canonical rows, and authenticated receipts. Unknown schema,
malformed data, incomplete pagination, identity discontinuity, or integrity
damage is not an empty register.

The narrow interface provides:

1. complete integrity/revision read;
2. reconcile facts on exactly one existing row without changing its stable
   identity;
3. release exactly one existing row;
4. append exactly one authenticated receipt;
5. deterministic report rendering from canonical records; and
6. authoritative complete readback of one expected logical result.

Row creation, reservation, and replacement are unavailable in Release A.
Recommendations remain an ephemeral report projection and never become owned
portfolio state.

Only the report wrapper's register writer can invoke mutations, and only while
the current invocation owns the shared caller executor. A losing invocation
writes no receipt. Run History is visibility, not a lock.

## Body/history pair

Every authenticated history append is one logical register operation composed
of a prepared body replacement and one comment append. It is not an atomic
transaction or distributed lock.

The writer:

1. validates the complete body and authenticated history from genesis;
2. checks expected register/row revision or history head, stable identities,
   capacity, source/policy preconditions, operation identity, and wrapper scope;
3. returns an existing compatible anchored result with zero writes, while an
   incompatible duplicate blocks;
4. prepares one canonical next receipt and one body whose revision increments
   once and whose anchor stores that complete receipt prospectively;
5. re-reads, replaces the body at most once, and reads it back; and
6. appends that exact anchored receipt at most once, then reads back the
   complete body and history chain.

No persistence claim is valid until the chain exactly matches the anchor.
Revision and fingerprints detect stale preparation and bad readback; they are
not provider-level compare-and-swap preconditions.

## Minimal repair

Repair starts only after caller exclusivity and a complete integrity read. It
reuses the original repository-qualified operation identity and exact prepared
data. A same-named operation from another repository is a foreign pair, not a
replacement or compatible result.

- If the body anchor is exactly one valid receipt ahead of the authenticated
  chain, append that exact stored receipt once without rewriting the body, then
  read everything back.
- If the body marker and anchor are unchanged and current preconditions still
  match, the exact prepared body operation may be invoked once.
- If body and history already match, return the existing logical result with
  zero writes.

Multiple gaps, in-chain deletion or reorder, comments ahead of the body,
incompatible anchors, forged markers, mixed identities, or incompatible
duplicate operations block. Repair never invents payload, changes unrelated
rows, overwrites foreign edits, or exceeds seven rows.

## Reporting and unavailable state

The caller's deterministic renderer owns section/column order, attention order,
escaping, truncation, LF line endings, and the exact machine block. Compare the
body projection byte-for-byte. A mismatch is a foreign edit and blocks writes.

Lane coverage derives only from the current authenticated manifest and Scout
Receipts. A missing expected receipt renders `incomplete (no receipt)` with
`Action required`. No authenticated current run renders `no run recorded`, not
zero findings.

If either required register read or write is unavailable, read-only sensing may
continue in memory while selection and writes stop. Return the core completion
fields with `last_safe_stage: Sense`, `attention_state: Action required`, the
missing continuity proof, and `persistence: not persisted — report register
unavailable`.
