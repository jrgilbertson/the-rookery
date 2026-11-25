# Reviewing PRs checks

`fixtures/run-standin-checks.py` checks the synthetic GitHub that the
[Reviewing PRs Skill Eval](../../evals/reviewing-prs/README.md) runs against:
the `gh` stand-in in `evals/reviewing-prs/stand-ins/` and every fixture world
in `evals/reviewing-prs/fixtures/`. It calls the stand-in the way an agent
would and confirms that each fixture answers the skill's discovery and read
commands, that a merge pinned to the wrong commit fails, that writes outside
the stand-in's contract are refused and traced, and that a state directory
inside a repository is rejected. `fixtures/review-requests-world.json` is a
small world outside the Eval Cases. It checks the skill's own commands for
collaborator repositories and review requests, and removing the operator
from a review request.

`fixtures/run-template-checks.py` checks the review page template in
`skills/reviewing-prs/assets/`. It fills the template with
`fixtures/sample-round.json`, whose titles include a hostile one, using the
same shell steps the skill prescribes. It then confirms the security policy
and its nonce, that the template builds no HTML from strings and loads
nothing external, and that the page's data block matches the escaped data
file byte for byte and still parses. It then runs the page's own script in
Node against a minimal stand-in for the DOM and checks where each pull request
lands: which side of the hold line, in what order, and whether a sensitive
kind is named. It also clicks Not applicable on the first block and
checks the Verdict line the page builds. It needs `node` on `PATH`, and it cannot tell whether the page
looks right.

Run both through the complete repository gate:

```sh
lefthook run pre-push --force
```

The gate tests the stand-in, which the Eval Records' evidence depends on. It
does not show that an agent obeys the skill, and nothing here runs a model.
