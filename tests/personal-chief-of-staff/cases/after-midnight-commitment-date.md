# After-midnight wind-down preserves the closing-date journal

Provenance: daily-commitment A/B test (2026-07-31). The prior skill resolved
the wall-clock local date but did not guarantee that a late wind-down used the
day being closed, or that morning recovered the ordered list outside the
foreground cap.

## Prompt

> It is 12:20 AM Wednesday, but I am winding down Tuesday. Tuesday's Daily
> Journal already contains my reflection, and the configured template includes
> `## Tomorrow’s Meaningful Commitments`. Prepare three reviewed Wednesday
> commitments in Tuesday's journal, but write nothing until I approve the exact
> journal action. Then assume it is Wednesday morning and give me the briefing
> from the journal that should contain them.

## Expected behavior

- [ ] Resolves Tuesday as the closing-date journal and Wednesday as the target
      day before drafting or writing.
- [ ] Preserves Tuesday's existing journal and keeps the exact insertion
      separately approvable.
- [ ] Wednesday morning recovers all three reviewed commitments from Tuesday's
      journal in order, including their finish lines and rationales.
- [ ] The commitments appear before and outside the separate zero-to-three
      foreground-attention limit.
