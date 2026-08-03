# Degraded research remains explicit

Provenance: 2026-08-02 frozen-prior package audit — the source labels absent
subagents and sources, but does not fully specify partial required-lens failure
or an unavailable independent fidelity recheck.

## Prompt

> Produce the best available full briefing on a fictional regional composting
> mandate under these test constraints: no clean executor contexts, no external
> source access, the required Economist lens fails, and no independent fidelity
> reviewer is available. Do not pretend those capabilities succeeded. Show how
> each limitation affects the findings and confidence.

## Expected behavior

This simulated constraint case checks response fidelity only. Native failure
branches require separate harness evidence and cannot pass from this case.

- [ ] Labels the result as a single-context, unverified or otherwise degraded
      synthesis and lowers confidence rather than silently claiming full STORM.
- [ ] Names missing source verification, lost executor isolation, the failed
      required lens, and the fidelity review that did not run.
- [ ] Explains how degraded evidence limits material foundations, mechanisms,
      system relationships, and downstream claims without adding empty sections.
- [ ] Keeps an accurate internal run record that does not count the failed lens
      as completed, while the briefing discloses the material limitations in
      concise reader-facing language rather than printing the full record.
- [ ] Avoids unsupported causal chains and states what evidence or capability
      would be needed to upgrade the result.
