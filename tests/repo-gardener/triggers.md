# Trigger contract: repo-gardener

Judged under [`tests/README.md`](../README.md): name + description + one query,
fresh context, binary judgment.

## Should trigger

| Query | Reason |
| --- | --- |
| Initialize read-only repository gardening for this repo | Explicit initialize branch. |
| Propose an all-off policy for daily repo maintenance | Policy-proposal setup stays read-only. |
| Run today's repository reconciliation | Explicit scheduled/manual reconcile branch. |
| Reconcile the current maintenance portfolio without changing source work | Core read-only control loop. |
| Why did the repo gardener report incomplete scout coverage? | Continues interpretation of a repo-gardener run. |
| Build the seven-slot gardening report from current source facts | Exact report outcome. |
| Check the current automation register before rediscovering candidates | Reconciliation-order request. |
| Do a cheap daily scan of maintenance lanes and update only the report register | Report-register-only Release A effect. |

## Near misses: should not trigger

| Query | Expected owner |
| --- | --- |
| Implement this repository issue | General implementation workflow. |
| Merge the dependency update | Merge or PR workflow. |
| Turn on a scheduled workflow | Caller or automation configuration. |
| Create a backlog issue from this customer comment | Issue-authoring workflow. |
| Review this branch for bugs | Code review. |
| Is this branch ready for a PR? | `checking-pr-readiness`. |
| Fix the failing CI job | Debugging or implementation. |
| Publish a release and update the changelog | Release workflow. |
