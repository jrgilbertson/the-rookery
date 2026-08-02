# Output purpose and compression

Provenance: 2026-08-02 frozen-prior package audit — requested format adaptation
exists, but the prior cannot preserve analytical findings from passes it does
not explicitly run.

## Prompt

> Prepare a one-page negotiation brief for a fictional university deciding
> whether to renew its campus shuttle contract. Use only this synthetic source
> packet: ridership rose 8%, missed trips rose 15% during driver shortages,
> fuel costs can reset quarterly, the contractor proposes a 10% price increase,
> and the university can switch providers only after a nine-month procurement.
> Do the multi-perspective research first. Stay concise, but retain anything
> that changes our negotiating position, confidence, or next action.

## Expected behavior

- [ ] Runs baseline grounding, independent lens research, contradiction
      mapping, and both analytical passes before compression, then runs
      fidelity review on the final compressed deliverable.
- [ ] Returns the requested one-page negotiation form rather than a full
      workflow transcript or mandatory full-section template.
- [ ] Preserves every analytical finding or uncertainty that materially changes
      the answer, confidence, negotiating position, or next action.
- [ ] Keeps evidence and inference distinguishable after compression and does
      not upgrade a weak causal link into a compact factual claim.
- [ ] Ends with negotiation-useful questions or actions, consistent with the
      requested purpose rather than a generic research verdict.
