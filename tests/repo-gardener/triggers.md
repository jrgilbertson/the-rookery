# Trigger contract: repo-gardener

Judged under [`tests/README.md`](../README.md): name + description + one query,
fresh context, binary judgment.

## Should trigger

| Query | Reason |
| --- | --- |
| Run tonight's repository gardening automation | Explicit scheduled run. |
| Reconcile the repo gardener tracker and inspect all maintenance lanes | Core manual run. |
| Continue the interrupted repo-gardener parent and close its run | Recovery of the same workflow. |
| Why did last night's repository-gardener run skip a child PR? | Interpret a run decision. |
| Do the nine-lane repository-health pass and deepen the strongest current findings | Exact breadth/depth workflow. |
| Let the nightly gardener open one safe PR if current evidence warrants it | Bounded child-authoring workflow. |
| Check product-data trust as part of this repo-gardener run | Cross-cutting measurement path. |
| Prepare the morning report from the retained repository-gardener parent | Explicit run handoff. |

## Near misses: should not trigger

| Query | Expected owner |
| --- | --- |
| Implement issue 123 in a new worktree | General implementation workflow. |
| Review this branch for bugs | Code review. |
| Is this branch ready for a PR? | `checking-pr-readiness`. |
| Merge the dependency update | Merge workflow. |
| Create a GitHub issue for this customer request | Issue-authoring workflow. |
| Turn on a scheduled workflow | Automation configuration. |
| Fix the failing CI job | Debugging or implementation. |
| Publish a release and update the changelog | Release workflow. |
