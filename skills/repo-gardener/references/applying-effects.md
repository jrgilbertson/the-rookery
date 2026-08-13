# Applying the two tracker records

The parent uses the existing `effect-v1` preparation and verification path
exactly twice: once for `run-opened`, then once for `run-closed`. It performs no
other managed tracker operation for that run ID.

## Prepare and write

Normalize a complete raw tracker snapshot first. Prepare one operation with
`effect-v1` and keep its returned body and comment bytes immutable. The caller
alone decides whether its configured GitHub capability may apply those exact
bytes. This skill defines no wrapper, provider client, credential, or planning
authority.

After the write, obtain the complete issue and every comment page. Verify the
immutable prepared object against the same pre-read and the full post-read.
Accept only `observed` or `already satisfied` before continuing. `failed` and
`ambiguous` stop the dependent tracker sequence.

## Recover an uncertain write

Never retry blindly. Reuse the original prepared object and operation ID.

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
