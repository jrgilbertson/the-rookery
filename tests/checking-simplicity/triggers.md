# Trigger contract: checking-simplicity

Judge each query per [`tests/README.md`](../README.md) in a fresh context that
sees only the skill name, description, and query. A should-trigger query needs
`yes`; every near miss needs `no`.

## Should trigger

| Query | Reason |
| --- | --- |
| Simplify this implementation plan before we start coding | Explicit plan-to-build simplicity review. |
| Choose the smallest reliable implementation among these approaches | Right-sizing an approach before implementation. |
| Before coding this behavior change, does the existing repository mechanism already satisfy it? | Tests reuse before adding a new implementation. |
| Which parts of this architecture anticipate only hypothetical future needs? | Challenges speculative complexity in a proposed architecture. |
| Right-size this design without dropping required behavior | Requests a smaller approach with a preservation constraint. |
| Review this draft plan, then implement it only if it is not overengineered | Places the checkpoint before the first edit. |
| Plan and implement a small behavior change to add an archive action | Ordinary behavior-changing work gets the final pre-edit checkpoint. |
| Before coding, challenge the proposed adapter, queue, and configuration layer | Names complexity-bearing concepts in a proposed approach. |
| This build is about to add persistent state and a new dependency; check the approach first | In-build decision point before new machinery. |

## Near misses: should not trigger

| Query | Expected owner |
| --- | --- |
| Simplify this already-implemented function without changing behavior | Settled-code simplification. |
| Review this pull request for bugs and regressions | Code review. |
| Explain this architecture in simpler language | Explanation, not design reduction. |
| Make the settings page look visually simpler | Interface design. |
| Debug the failing synchronization test | Debugging. |
| Reduce the JavaScript bundle size | Metric-driven performance optimization. |
| Is this branch ready to open a pull request? | PR readiness. |
| Should I merge this reviewed pull request? | Merge readiness. |
| Read the repository and explain how the export pipeline works; do not change anything | Read-only work has no plan-to-build decision. |
| Rename `retryCount` to `attemptCount` everywhere, exactly as specified | Prescribed mechanical edit with no design choice. |
