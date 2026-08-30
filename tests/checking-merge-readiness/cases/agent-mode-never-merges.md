# Report-only agent mode never merges

## Prompt

> Work only from these synthetic facts. Do not call tools.
>
> A supervising agent asks `checking-merge-readiness` for a report-only
> assessment of open PR 41 at full head `d4`. Its ordinary read-only review
> finds a resolved-test regression and recommends `debug`. Its step 4 intent
> baseline would otherwise require owner confirmation.

## Expected behavior

- [ ] Return `debug`, full head `d4`, and ordinary human-readable findings.
- [ ] Record intent as unverifiable, apply the ordinary debug cap, and continue
      through the step 6 readout without prompting the owner.
- [ ] Do not show an owner decision menu, prepare a merge action, or invoke a
      forge write.
- [ ] Leave the decision whether to direct the Worker to the supervising agent.
- [ ] Use neither a JSON/envelope contract nor a finding key, fingerprint,
      counter, registry, state machine, or progress record.
