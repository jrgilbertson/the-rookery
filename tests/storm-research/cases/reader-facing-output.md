# Reader-facing briefing output

Provenance: 2026-08-03 live Pangram briefing review — the useful answer was
buried beneath mandatory analytical sections and an execution manifest written
for a workflow auditor rather than the human reader.

## Prompt

> Produce a full research briefing for a human editor on how to respond when a
> fictional detector flags an article as machine-written. Use only this
> synthetic source packet: the vendor reports a 0.01% false-positive rate on
> articles over 500 words; an independent audit confirms strong performance on
> news but does not test academic prose; the detector performs poorly on text
> under 100 words; version history is available; the publisher permits grammar
> correction but prohibits generated paragraphs. Use the five canonical lenses.
> Write the briefing for the editor rather than exposing internal workflow
> telemetry.

## Expected behavior

- [ ] The Overview carries the editor-facing answer, practical next steps, and
      material risks or confidence limits; later sections support that lead
      rather than introducing the decision for the first time.
- [ ] The briefing integrates research depth into its overview, baseline,
      perspective scan (subsection per lens), key tensions, reliability, and
      guidance instead of creating standalone first-principles or
      systems-thinking sections.
- [ ] The reader-facing briefing omits the internal lens, isolation, queue,
      source-access, and fidelity manifest.
- [ ] Any material research limitation appears in the Overview so it frames how
      the rest should be read.
- [ ] The response remains a multi-perspective evidence review rather than a
      detector verdict or a compact project-opinion memo.
