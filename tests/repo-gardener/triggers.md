# Trigger contract: repo-gardener

Judged under [`tests/README.md`](../README.md): name + description + one query,
fresh context, binary judgment.

This skill starts only on an explicit invoke. Topic matches about overnight
maintenance, CI, or issues do not activate it.

## Should trigger

| Query | Reason |
| --- | --- |
| $repo-gardener | Named skill invoke. |
| /repo-gardener | Named skill invoke. |
| Run repo-gardener on this repository | Names the skill. |
| Set up repo-gardener on this repository | Names the skill for first-use. |
| Continue last night's repo-gardener run and post its report | Names the skill for recovery. |
| Why did last night's repo-gardener run skip an Executor PR? | Names the skill for interpreting a run. |
| Run repo-gardener now and post the report to issue 3521 | Names the skill with a report target. |

## Near misses: should not trigger

| Query | Expected owner |
| --- | --- |
| Run tonight's repository gardening automation | Topic match; no skill name. |
| Let the nightly gardener open unmerged PRs if current evidence warrants it | Topic match; no skill name. |
| Do a repository-health pass and deepen the strongest findings | Topic match; no skill name. |
| Reconcile the tracker and inspect all maintenance lanes | Topic match; no skill name. |
| Implement issue 123 in a new worktree | General implementation workflow. |
| Review this branch for bugs | Code review. |
| Is this branch ready for a PR? | `checking-pr-readiness`. |
| Merge the dependency update | Merge workflow. |
| Create a GitHub issue for this customer request | Issue-authoring workflow. |
| Turn on a scheduled workflow | Automation configuration. |
| Fix the failing CI job | Debugging or implementation. |
| Publish a release and update the changelog | Release workflow. |
