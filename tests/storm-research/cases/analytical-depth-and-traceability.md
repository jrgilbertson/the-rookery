# Analytical depth and traceability

Provenance: 2026-08-02 frozen-prior run — the briefing preserved evidence and
disagreement but omitted both named analyses and link-level causal
traceability; the graded result is recorded in the suite log.

## Prompt

> Produce a full briefing on whether fictional Bellwether should introduce
> downtown congestion pricing. Use only this synthetic source packet: a pilot
> recorded 18% fewer downtown car entries, 12% more peak bus riders, and 9%
> more traffic on boundary roads; a controlled study found faster downtown
> trips but did not measure emissions; a resident survey found shift workers
> had the fewest transit alternatives; the vendor's benefits model assumes an
> uncalibrated 0.3 demand elasticity; bus capacity cannot expand for 12 months,
> while charge revenue arrives after 6 months. The council wants a
> recommendation but rejects hidden assumptions or unsupported causal links.

## Expected behavior

- [ ] Grounds the briefing in the supplied evidence and distinguishes verified
      facts, assumptions, irreducible constraints, and inference.
- [ ] Includes a distinct `First-principles analysis` that states a causal
      mechanism and the conditions required for its main claim to hold.
- [ ] Includes a distinct `System dynamics and higher-order effects` analysis
      with a useful boundary, time horizon, material actors, incentives,
      resources, and constraints.
- [ ] Presents every material multi-step effect as a causal chain and ties each
      uncertain link to evidence or labels it as inference with confidence.
- [ ] Accounts for every material user-facing claim in a source audit with its
      best source, source type, bias risk, missing counter-source, and confidence,
      including complete low-confidence rows for unsupported claims introduced
      during analysis or synthesis.
- [ ] Preserves material cross-lens disagreement and gives decision support
      without treating fluent analytical language as evidence.
