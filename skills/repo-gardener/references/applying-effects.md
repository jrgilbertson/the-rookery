# Applying report effects

This reference owns the trusted-effect and recovery protocol for Release A's
only possible write: one report-register operation through the caller's narrow
wrapper. Source effects and raw provider methods remain unavailable.

## Authority boundary

The report write is unavailable unless caller-produced evidence proves:

- one repository-scoped executor holds exclusive ownership across every entry;
- the wrapper allowlists verb, repository, report, and exact prepared target
  outside the model;
- raw provider tools and write credentials are absent from model, repository,
  hook, test, scout, child, and worktree contexts;
- report continuity and complete-history retention are valid;
- an intended-effect receipt is durable and read back before invoke;
- an authoritative register post-read follows invoke; and
- exactly one terminal outcome is durable and read back under the same logical
  operation identity.

Missing, stale, partial, or inferred proof means zero invoke. A missing optional
scout blocks dependent work; a missing global write boundary blocks all report
writes.

Name every missing invoke boundary separately in the decision: exclusive
executor, continuity, retention, runtime-scope proof, narrow wrapper,
intended-receipt readback, authoritative post-read, and terminal-receipt
readback. Any one missing global boundary independently blocks invoke; do not
compress several missing proofs into a generic authority failure.

When evaluating authority, report each boundary above rather than collapsing
the proof to examples. In particular, verify raw provider tools and write
credentials are absent from every model, repository, hook, test, scout, child,
and worktree context; omission of any one context is missing scope proof.

## Stable logical operation identity

The logical operation identity is the repository-qualified pair
`(repository_id, operation_id)`, never `operation_id` alone. Mint one stable
`operation_id` before the first attempt for the verified repository, render
both components together, and reuse the complete pair after ambiguity, crash
recovery, or a proven-absence retry. Mutable source, policy, row, register, and
history-head revisions are preconditions, not part of a replacement identity.
If either identity component is absent or invalid before the first attempt,
return `failed` with zero invokes; no later receipt or post-read can repair an
operation whose initial identity was incomplete.

Cross-repository reuse fails closed. If stored state contains the same
`operation_id` for another repository, preserve the requested
repository-qualified identity, render the conflicting stored pair separately,
return `failed` with zero invokes, and mint no replacement identity. The
foreign pair neither proves deduplication nor changes the requested pair.

## Receipt model and order

Persist and read back one intended-effect receipt binding the
repository-qualified operation identity, operation kind, repository, report
target, allowlisted verb and wrapper scope, initiating run, and separate
mutable preconditions.

In every effect decision, render stable `repository_id`, stable `operation_id`,
and mutable `preconditions` as separate fields before reporting an invoke. A
table or compact `operation_identity: (repository_id, operation_id)` field is
also valid when it visibly preserves both identity components. Do not leave
repository qualification or the identity/precondition separation implicit in
a general authority summary. In particular, render stable `operation_id` and
mutable `preconditions` as separate fields; repository qualification adds to
that established separation rather than replacing it.

Then perform this order exactly:

1. obtain exclusive caller ownership;
2. re-read the current register and policy preconditions;
3. persist and completely read back the intended-effect receipt;
4. return an existing compatible terminal outcome with zero writes, or fail
   closed on an incompatible duplicate;
5. invoke the narrow wrapper at most once;
6. perform an authoritative complete register post-read;
7. persist and read back exactly one terminal outcome; and
8. stop on ambiguity, leaving the unmatched intent for reconciliation before
   new selection.

Terminal outcomes are exactly:

- `observed` — the authoritative post-read proves the intended result;
- `already satisfied` — the desired result already holds without a new write;
- `failed` — the wrapper or provider returned a definitive denial or error; or
- `ambiguous` — timeout, authentication-disguised absence, uncertain
  deduplication, unavailable post-read, rate limit without proof, or any other
  outcome that is not proven success, absence, or failure.

Preserve those classifications through recovery. An ambiguous operation stays
`ambiguous` while absence, authority, or changed preconditions are being
reconciled; retry eligibility does not turn it into a pending or `none`
outcome. An authority or identity collision proven before invoke is `failed`
with zero invokes. Use `terminal_outcome` only for a logical report operation,
not for an unrelated delegation or coverage disposition. For those non-report
facts, omit `terminal_outcome` instead of filling it with `not applicable`,
`pending`, or another value outside the four-outcome vocabulary.

When rendered, the `terminal_outcome` field contains only one exact canonical
token: `observed`, `already satisfied`, `failed`, or `ambiguous`. Put reasons,
persistence caveats, and next actions in separate fields or prose; never append
them to the terminal-outcome value.

For every rendered report-operation scenario, state separately whether the
terminal receipt was read back. Do not call an `observed` or `already
satisfied` operation completed or persisted unless that readback is proven;
without it, the operation remains `ambiguous`. This mapping applies even when
the authoritative post-read found the desired state: missing terminal readback
overrides both success tokens.

## Reconciliation and retry

Before discovery, reconcile every unmatched intent by stable target identity
against both current source facts and the current register. Record a terminal
outcome through the report wrapper only when those authoritative facts prove
one. Ambiguity blocks blind retry and dependent work only.

Retry is allowed only when source-native register evidence proves absence of
the prior effect, the original repository-qualified pair is reused, current
authority and preconditions still match, and the wrapper allowlists are
unchanged. A changed precondition returns to refresh without minting another
identity.

Render retry proof as four distinct facts: proven source-native absence,
original repository-qualified identity reuse (showing both `repository_id` and
`operation_id`), current authority unchanged or re-proven, and mutable
preconditions unchanged. Wrapper-scope continuity does not substitute for the
authority fact.

The single-tail repair applies only to exactly one valid anchored receipt ahead
of history. Multiple receipt gaps remain `ambiguous`, permit no invoke or
repair, and wait for authoritative reconciliation.

Whenever repair states are requested, state the single-tail mechanics in full:
append that exact stored receipt once, do not rewrite the body, then perform the
complete readback. Report the multiple-gap state separately as `ambiguous` with
no repair or invoke.

## Completion partition

For any ambiguous operation, `affected_work` contains that operation and every
dependent work item exactly once. `remaining_unblocked_work` contains every
independent item exactly once as `continued`, `delegated` with durable readback
of destination/executor/exact work, or `gated` by its own prerequisite. The two
fields are disjoint and exhaustive; use `none` only for an empty side.

Name the ambiguous report operation itself in `affected_work`; listing only
its dependent items is incomplete.

Return the core completion fields plus:

```text
repository_id: <verified repository component of the logical identity>
operation_id: <stable logical operation identity>
terminal_outcome: <observed | already satisfied | failed | ambiguous>
```

Never invent a second operation identity to escape ambiguity, and never claim
a report effect without the terminal receipt readback.
