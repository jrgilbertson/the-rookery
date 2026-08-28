# Assessment-only fail-closed variants

Provenance: Observed failure where stale, cross-boundary, partial, and bypassed receipt chains were narrated as ready.

## Prompt

> Grade the independent variants of the synthetic assessment bundle defined
> by `../fixtures/assessment-spec.json`: missing code-review receipt; code-review
> receipt with no evidence reference; stale simplification receipt; testing
> receipt for another subject; plan receipt for another revision; unresolved
> receipt reference; staged-only dirt; renamed branch; detached and ambiguous
> live subjects; unresolved targeted-sweep finding; and preflight bypass request.
> Also distinguish no configured automated reviewer, known under-cap and
> over-cap reviewers, a resolved reviewer with a successful authoritative
> no-cap lookup, an unresolved reviewer identity, and failed or incomplete
> cap lookups. Verify that a no-cap reviewer cannot hide another reviewer that
> exceeds its known cap. Include self-asserted repository-gate,
> code-review, and testing documents that omit producer, scope, executable
> command, outcome, or inspectable result references. Also include a null
> receipt element, duplicate receipt kinds, a receipt with a non-string kind,
> a non-string evidence path, and a non-string assessment receipt reference.
> Include an outside-tree bundle transport with a missing, altered, or
> cross-revision evidence or result document.
> Include same-kind evidence/result bytes and their digests copied from an old
> revision into a new-revision bundle, and from one Worker/session bundle into
> another bundle at the same head.
> At the real evaluator boundary, include caller assessment gaps with a missing
> key, an empty key, duplicate keys, and an extra field; also supply missing,
> null, and other non-object outer assessment members. Move the same invalid
> receipt member from the first list position to the last position, and compare
> real producer output rather than calling a gap helper directly.
> Return one assessment receipt per variant without an owner menu.

## Expected behavior

- [ ] Malformed receipt transport and substantive receipt or evidence defects
  return `action-required`; invalid outer assessment claims return one valid
  `UNKNOWN` envelope; neither path returns `pass`.
- [ ] Gaps name missing or unresolved receipts, unreferenced substitutes, missing file evidence, stale evidence, cross-subject/cross-revision bindings, dirty or unresolved live subjects, unresolved findings, and bypass requests.
- [ ] Narrative completion and owner attestation are not upgraded to exact-revision evidence.
- [ ] The variants remain independent; a gap or receipt from one is not carried into another.
- [ ] No variant writes to the checkout, presents an owner menu, stages, commits, pushes, or opens a pull request.
- [ ] Class 11 is `not applicable` only when discovery proves no automated reviewer is configured. Each known cap is evaluated independently, a no-cap lookup cannot hide an exceeded cap, and only a resolved identity plus a successful authoritative no-cap lookup is process-only `cap unverified` evidence that names the reviewer, source, and lookup outcome.
- [ ] Unresolved identities and failed, incomplete, unreadable, or otherwise unknown cap lookups remain named fail-closed gaps rather than successful no-cap evidence.
- [ ] Name-only tests, zero-finding review assertions, and owner/status-only gate tuples fail their exact per-kind evidence schemas.
- [ ] Null receipt elements, duplicate or invalid receipt kinds, invalid evidence paths, and invalid assessment references return normal `action-required` receipts with their exact structural gaps.
- [ ] Outside-tree transport is accepted only when its complete evidence and
  result documents are digest-matched and bound to this exact repository,
  subject, and revision; a missing, altered, stale, or mixed transport fails
  closed.
- [ ] Same-kind inline evidence/result documents copied from another revision or
  Worker/session bundle fail even when mutable outer transport labels are
  changed to the recipient head and bundle.
- [ ] Each material gap uses only a nonempty producer-owned key and a
  human-readable message. Caller claims with malformed gap keys, or a missing,
  null, or other non-object outer assessment member, return one valid `UNKNOWN`
  envelope. A moved finding retains its opaque equality key without relying on
  its list position.
