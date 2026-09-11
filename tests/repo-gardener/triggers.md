# Trigger contract: repo-gardener

Judged under [`tests/README.md`](../README.md): name + description + one query,
fresh context, binary judgment.

This skill starts only when named: the skill name, its slash or dollar
form, or a plain request to run, continue, set up, or explain the
repository gardening automation or the nightly gardener. Topic
matches about maintenance, CI, health, trackers, or issues do not activate it.

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
| Run tonight's repository gardening automation | Names the gardening automation in plain words. |
| Let the nightly gardener run and open its pull requests | Names the gardener as the thing to run. |

## Near misses: should not trigger

| Query | Expected owner |
| --- | --- |
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
