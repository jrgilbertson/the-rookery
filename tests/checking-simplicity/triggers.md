# Trigger contract: checking-simplicity

Judge each query per [`tests/README.md`](../README.md) in a fresh context that
sees only the skill name, description, and query. A should-trigger query needs
`yes`; every near miss needs `no`.

## Should trigger

| Query | Reason |
| --- | --- |
| Simplify this implementation plan before we start coding | Explicit plan-to-build simplicity review. |
| Choose the smallest reliable implementation among these approaches | Right-sizing an approach before implementation. |
| This completed approach adds a cache. Before coding, check whether existing request memoization already satisfies the requirements. | Tests reuse before adding a new implementation, with a reviewable subject. |
| Right-size this completed design draft without dropping its required behavior | Requests a smaller approach with a preservation constraint and current subject. |
| Review this draft plan, then implement it only if it is not overengineered | Places the checkpoint before the first edit. |
| Before coding, challenge the proposed adapter, queue, and configuration layer | Names complexity-bearing concepts in a proposed approach. |
| This build is about to add persistent state and a new dependency; check the approach first | In-build decision point before new machinery. |
| Our requirements and approach brief is complete and proposes a queue plus provider adapter. Before deepening it into an implementation plan, continue the workflow. | Completed early-planning handoff with assessable mechanism choices, without explicit simplicity language. |
| The approved requirements brief is ready. Before creating the technical implementation plan, continue the workflow. | Completed requirements handoff where scope can be checked without inventing implementation details. |
| The implementation plan is ready at `/tmp/archive-plan.md`. Hand it off to execution. | Completed implementation-plan handoff before the first write, without explicit simplicity language. |

## Near misses: should not trigger

| Query | Expected owner |
| --- | --- |
| Simplify this already-implemented function without changing behavior | Settled-code simplification. |
| Review this pull request for bugs and regressions | Code review. |
| Explain this architecture in simpler language | Explanation, not design reduction. |
| Make the settings page look visually simpler | Interface design. |
| Debug the failing synchronization test | Debugging. |
| Is this branch ready to open a pull request? | PR readiness. |
| Read the repository and explain how the export pipeline works; do not change anything | Read-only work has no plan-to-build decision. |
| Rename `retryCount` to `attemptCount` everywhere, exactly as specified | Prescribed mechanical edit with no design choice. |
| Plan and implement a small behavior change to add an archive action | No reviewable plan or approach exists yet; the planning or build workflow may route here after producing one. |
| We are still brainstorming whether an archive action is needed and what outcome it should produce | Requirements are unfinished; brainstorming owns the current task. |
| Before coding this behavior change, does the existing repository mechanism already satisfy it? | No completed requirements draft, plan, approach, or concrete in-build decision is present. |
| The unchanged implementation plan already has an independent PASS with no owner decision. Continue to implementation. | The checkpoint is complete; the executor owns the newly reached task. |
