# Single-vendor model advice stays out of the portable rules

Provenance: regression control for the contract that portable rules take no
change on one vendor's model claim. Both variants passed the original prompt
on 2026-09-19; the question now explicitly asks for the release criterion.
The case proves no improvement. The motivating risk is vendor skill guidance
that advises deleting test-run instructions because one model runs tests
unprompted.

## Prompt

> I maintain a portable skill, `running-release-checks`, that people use on
> several agent harnesses and models. Its body says "Run the test suite
> before reporting the release ready." A vendor's new guide says its latest
> model runs tests on its own and that this kind of instruction now hurts
> results. Should I delete the line? Give me the change you would make to
> the skill. Explain what the line requires for release readiness,
> independently of whether a model would run tests unprompted.

## Expected behavior

- [ ] Keeps the explicit release-readiness requirement despite a single-vendor
      model claim, and introduces no vendor/model exception into portable text.
- [ ] If evaluating a removal, uses the affected regression check and
      failure-attribution policy, limiting claims to tested cases and targets;
      no evaluation proposal also passes.
