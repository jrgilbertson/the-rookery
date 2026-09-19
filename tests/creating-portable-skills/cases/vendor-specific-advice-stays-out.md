# Single-vendor model advice stays out of the portable rules

Provenance: 2026-09-19 review of current vendor skill guidance — one vendor
advises deleting test-run instructions because its newest model runs tests
unprompted, and another judges cruft against one target model. Applied
blind, either writes one vendor's assumptions into a portable package.

## Prompt

> I maintain a portable skill, `running-release-checks`, that people use on
> several agent harnesses and models. Its body says "Run the test suite
> before reporting the release ready." A vendor's new guide says its latest
> model runs tests on its own and that this kind of instruction now hurts
> results. Should I delete the line? Give me the change you would make to
> the skill.

## Expected behavior

- [ ] Identifies the advice as resting on one vendor's model behavior, not
      as a property of models in general.
- [ ] Does not delete the instruction from the portable skill on that
      advice alone.
- [ ] Treats running the suite before a release report as a completion
      criterion or hard constraint the skill may keep, not as default
      reasoning to cut.
- [ ] Says a removal would need a with-and-without comparison on the
      targets the skill declares, not the vendor's claim.
- [ ] If it records the vendor advice at all, labels it vendor-specific and
      scoped to that target, outside the portable rules.
