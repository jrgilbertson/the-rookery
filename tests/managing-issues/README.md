# Managing Issues checks

`fixtures/run-config-checks.py` runs the skill's shipped configuration
validator, `skills/managing-issues/scripts/config_check.py`, against the
fixture configs in `fixtures/config`, the starter templates, and this
repository's own config, and checks its results. It also checks the priority
and estimate lookup tables in `references/prioritization.md` against the rule
they stand for. It is this skill's only runner. Run it through the complete
repository gate:

```sh
lefthook run pre-push --force
```

The gate tests that validator; it does not show that an agent obeys the skill,
and nothing for this skill in the gate runs a model.
