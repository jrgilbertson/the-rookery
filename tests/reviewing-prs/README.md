# Reviewing PRs checks

`fixtures/run-template-checks.py` checks the review page template in
`skills/reviewing-prs/assets/`. It fills the template with
`fixtures/sample-round.json`, whose titles include a hostile one, using the
same shell steps the skill prescribes. It then confirms the security policy
and its nonce, that the template builds no HTML from strings and loads
nothing external, and that the page's data block matches the escaped data
file byte for byte and still parses. It then runs the page's own script in
Node against a minimal stand-in for the DOM and checks where each pull request
lands: which side of the hold line, in what order, and whether a sensitive
kind is named. It checks that each card opens its body with the pull
request's summary as text, hostile markup included, and draws nothing for a
pull request without one. It also clicks Not applicable on the first block and
checks the Verdict line the page builds. It needs `node` on `PATH`, and it cannot tell whether the page
looks right.

Run it through the complete repository gate:

```sh
lefthook run pre-push --force
```

The gate tests the shipped review page template and runs the offline
`evals/reviewing-prs/check-fixtures.mjs` conformance suite through
[`tests/evals/fixtures/run-eval-checks.py`](../evals/README.md). It does not
show that an agent obeys the skill, and nothing here runs a model.
