# Trigger contract: checking-pr-readiness

Judged per the protocol in [`tests/README.md`](../README.md): fresh context,
name + description + query only, binary judgment, any near-miss `yes` fails.

## Should trigger

| Query | Reason |
| --- | --- |
| I think this branch is ready for a PR | Branch work looks complete and a pull request is the next step. |
| Are we good to open the pull request? | Direct readiness question ahead of opening a PR. |
| Anything else before I ship this? | Pre-ship gate phrased as an open question. |
| Run the pre-PR checklist | Explicit request for the pre-pull-request gate. |
| Is this worktree ready for CI? | Readiness to enter the continuous-integration process. |
| Present your work for final approval | Readout-then-one-owner-decision request at the end of branch work. |
| Is this branch ready for review? | Ready-for-review is the gate's stated trigger phrasing. |
| Check whether everything I planned actually got delivered before I ship | Plan-versus-delivered comparison inside the shipping gate. |
| Did the review and simplify steps actually run on this branch? | Verifying upstream shipping steps from receipts. |
| Gate this change before it goes out | Gating a branch before it leaves the worktree. |
| Assess this exact branch head for PR readiness and return same-session findings | Explicit exact-head assessment without an owner menu. |
| Headlessly assess this commit for PR readiness and return ready or action-required | Unattended same-session result rather than an owner menu. |

## Near misses: should not trigger

| Query | Expected owner |
| --- | --- |
| Resolve the review comments on my PR | PR-feedback resolution on an existing pull request. |
| Review this diff for bugs | Code review. |
| Simplify what I just wrote | Code simplification. |
| Review my plan doc | Document or plan review. |
| Merge the PR | Merge tooling, or a future merge-readiness gate. |
| Why did CI fail? | Debugging a failing run. |
| Write the PR description | Pull-request creation and description tooling. |
| Is this library ready for production use? | General question about a dependency; no branch gate involved. |
| Open a pull request for this branch | Commit, push, and PR-opening tooling. |
| Take screenshots of the new settings page | Browser testing. |
