# Applying the two tracker records

The parent uses the existing `effect-v1` preparation and verification path
exactly twice: once for `run-opened`, then once for `run-closed`. It performs no
other managed tracker operation for that run ID.

## Require one tracker writer

Before `run-opened`, the caller must ensure exclusive tracker-write ownership
or atomic serialization such that only one parent may mutate this tracker. A
model decision, lease check, or liveness read cannot establish that guarantee.
This skill defines no wrapper or lock. When the guarantee is absent or unknown,
stop before any tracker write. Read-only work may be reported to the caller,
but the parent must not mutate the tracker.

## Prepare and write

Normalize a complete raw tracker snapshot first. Prepare one operation with
`effect-v1` and keep its returned body and comment bytes immutable. Before the
first provider mutation, persist that exact prepared object in caller-approved
external or private run state outside repository source, where a recovery
parent can read it after a process failure. If that state is unavailable, stop
before writing. This is recovery material, not another tracker record or a
custom provider wrapper. The caller alone decides whether its configured GitHub
capability may apply those exact bytes. This skill defines no wrapper, provider
client, credential, or planning authority.

The prepared tracker content may contain ordinary text and links. `effect-v1`
checks the final issue body and comment, rejecting notification-capable
`@mentions` and Markdown or HTML image embedding before either write. Do not
sanitize rejected content into a different prepared operation.

After the write, obtain the complete issue and every comment page. Verify the
immutable prepared object against the same pre-read and the full post-read.
Accept only `observed` or `already satisfied` before continuing. `failed` and
`ambiguous` stop the dependent tracker sequence.

## Recover an uncertain write

Never retry blindly. Reuse the original prepared object and operation ID.
Load them from the caller-owned recovery state when the original parent is not
available. Retain uncertain material for owner/recovery inspection; discard it
only after exact verification proves the operation complete or not invoked.

- If body and comment already match, perform zero writes.
- If the body is the exact prepared body and its anchor is exactly one receipt
  ahead, append the exact prepared comment once, then read every page again.
- Any other partial, changed, foreign, comment-ahead, or multi-gap state remains
  ambiguous and permits no repair.

## Check the closed run

After exact closing verification, invoke `run-records-v1` with exact input
`{schema, run_id, closed, post_read}`: the exact prepared closing object and raw
final snapshot. The command validates the durable opening from final history,
then checks only the managed receipt chain, uniqueness, order, matching run and
repository identities, exact prepared closing material, and final readback. A
success returns `register_closed_consistently: true`.

Do not pass candidates, recommendations, risk judgments, PR-readiness claims,
policy claims, or authority booleans to this checker. It neither accepts nor
derives them. Existing older CLI commands remain compatibility interfaces for
previously recorded Release A material; the nightly workflow does not use them
to make or certify planning decisions.
