# Effect recovery and ambiguity

Provenance: Observed failure where timeout created a new operation identity and a retry before authoritative absence proof.

## Prompt

> Classify every scenario in `../fixtures/effects/scenarios.json` using the
> Release A report-effect protocol. State operation identity, invoke count,
> terminal outcome when the scenario is a report operation, retry eligibility,
> and completion partition. Include the fixture's single-tail-receipt repair
> and multiple-gap integrity states. For the single-tail state, say whether the
> exact stored receipt is appended, how many times, and whether the body is
> rewritten; classify the multiple-gap state separately.

## Expected behavior

- [ ] Outcomes use exactly `observed`, `already satisfied`, `failed`, or `ambiguous`.
- [ ] Timeout, unavailable post-read, rate limit without proof, disguised absence, and uncertain deduplication are ambiguous with no blind retry.
- [ ] The skill never authorizes a blind retry; recovery reuses immutable prepared material after fresh complete reads.
- [ ] A changed precondition or cross-repository collision does not mint a replacement identity or invoke.
- [ ] One-valid-receipt-ahead register repair appends that exact receipt once without rewriting the body; multiple gaps block and remain ambiguous.
- [ ] `already satisfied` performs zero writes; `failed` requires an exact unchanged pre/post state plus `denied-before-write`.
- [ ] No effect persistence is claimed without exact positive verification.
