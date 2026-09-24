# Single-vendor model advice stays out of the portable rules

Provenance: regression control for the contract that portable rules take no
change on one vendor's model claim. Both variants passed it on 2026-09-19,
so it proves no improvement. The motivating risk is vendor skill guidance
that advises deleting test-run instructions because one model runs tests
unprompted.

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
- [ ] Gives at least one reason to keep the line that does not depend on any
      model's behavior, for example that it defines when the release may be
      reported ready.
- [ ] If it proposes evaluating removal of the requirement to run tests
      before reporting release readiness, requires comparing the skill with
      and without that requirement. Pass if it proposes no such evaluation.
- [ ] If it proposes evaluating removal of that requirement, limits any
      conclusion to the models and harnesses evaluated; evidence from one
      vendor's model does not establish the result for other targets.
      Pass if it proposes no such evaluation.
- [ ] The skill text it proposes, including "no change", contains no
      model- or vendor-named instruction or exception.
