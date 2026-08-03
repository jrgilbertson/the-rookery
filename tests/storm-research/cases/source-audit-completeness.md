# Source audit completeness

Provenance: 2026-08-02 instruction review — the prior source-audit step named
the right fields but did not define completion across every material claim.

## Prompt

> Read the project-local Storm Research skill. A draft has just been emitted,
> and its pre-analysis audit has complete rows for claims 1–3 and 5–6 but no
> row for claim 4, which synthesis introduced. Follow the workflow until the
> source audit is ready for fidelity review; return the reconciled audit and
> any unverified markers, without doing new research. Material draft claims:
> (1) downtown entries fell 18% during the pilot; (2) peak bus ridership rose
> 12%; (3) traffic on boundary roads rose 9%; (4) faster downtown trips justify
> permanent adoption; (5) a vendor model predicts net benefits using demand
> elasticity 0.3; (6) bus capacity cannot expand for 12 months. Sources: the
> official pilot count supports claims 1–3 but reports no causal design; a
> controlled trip-time study supports only faster downtown trips and did not
> measure emissions; the vendor report supports claim 5 but says its elasticity
> is uncalibrated; the transit agency capital plan supports claim 6. No source
> establishes claim 4, and no other source access is permitted.

## Expected behavior

- [ ] Accounts for all six material claims, grouping only claims that share the
      same source, risk, counter-source need, and confidence.
- [ ] Gives every represented claim a best source, source type, bias or tone
      risk, missing counter-source, and confidence, using a complete unverified
      row rather than a bare marker when no source supports the claim.
- [ ] Marks the permanent-adoption claim unverified rather than treating the
      trip-time study as sufficient support.
- [ ] Identifies the vendor's incentive risk and the uncalibrated elasticity as
      a confidence limit.
- [ ] Does not invent sources, causal identification, emissions evidence, or
      benefits that are absent from the record.
