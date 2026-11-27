# Skill Eval conformance checks

Deterministic offline checks for Promptfoo Skill Eval suites under `evals/`.

[`fixtures/run-eval-checks.py`](fixtures/run-eval-checks.py) discovers every
`evals/*/check-fixtures.mjs`, executes each suite's offline checks with Node.js,
and verifies in disposable temporary copies that `evals/_template/` and
`evals/active-learning/` fail when key invariants break (auto-memory disabling,
`Bash` omission, per-run timeout, subscription auth, `dontAsk` permission mode,
write-tool denial, committed `package-lock.json`, `npm ci`, and isolated
temporary `HOME`).

It never installs packages or calls a model.
