# Reviewing PRs checks

`fixtures/run-standin-checks.py` checks the synthetic GitHub that the
[Reviewing PRs Skill Eval](../../evals/reviewing-prs/README.md) runs against:
the `gh` stand-in in `evals/reviewing-prs/stand-ins/` and every fixture world
in `evals/reviewing-prs/fixtures/`. It calls the stand-in the way an agent
would and confirms that each fixture answers the skill's discovery and read
commands, that a merge pinned to the wrong commit fails, that writes outside
the stand-in's contract are refused and traced, and that a state directory
inside a repository is rejected. Run it through the complete repository gate:

```sh
lefthook run pre-push --force
```

The gate tests the stand-in, which the Eval Records' evidence depends on. It
does not show that an agent obeys the skill, and nothing here runs a model.
