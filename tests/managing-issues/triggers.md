# Trigger contract: managing-issues

Judged under [`tests/README.md`](../README.md): name + description + one query,
fresh context, binary judgment. This file records the contract, not run results.

## Should trigger

| Query | Reason |
| --- | --- |
| Read GitHub issue #42 and tell me its current scope | Explicit issue read. |
| Draft a bug issue with clear verification criteria | Issue drafting and required shape. |
| Create this Linear issue after showing me the exact fields | Issue creation. |
| Update the assignee and priority on this issue | Surgical issue update. |
| Break this delivery issue into native sub-issues | Native relationship graph change. |
| Which unblocked leaves in this issue family are ready now? | Graph readiness assessment. |
| Add this issue as a blocker of the release leaf | Native blocker relationship change. |
| Does this Done issue actually satisfy its Verification section? | Completion check against evidence. |
| Cancel this obsolete issue without deleting it permanently | Reversible lifecycle operation. |

## Near misses: should not trigger

| Query | Expected owner |
| --- | --- |
| Implement GitHub issue #42 in this codebase | General implementation workflow. |
| Open a pull request for the issue I just fixed | Pull-request publishing workflow. |
| Rewrite this pull request description | Pull-request authoring workflow. |
| Review this PR for bugs and regressions | Code-review workflow. |
| Is this branch ready to open a PR? | `checking-pr-readiness`. |
| Merge the approved pull request | Merge workflow. |
| Create a Linear project roadmap for the quarter | Project-planning workflow. |
| Configure automatic two-way sync for every repository issue | Integration configuration workflow. |
| Pick workers and models for these five issues | Execution orchestration workflow. |
