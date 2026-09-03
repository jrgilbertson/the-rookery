# Trigger contract: checking-simplicity

Judge each query per [`tests/README.md`](../README.md) in a fresh context that
sees only the skill name, description, and query. A should-trigger query needs
`yes`; every near miss needs `no`.

## Should trigger

| Query | Reason |
| --- | --- |
| Simplify this implementation plan before we start coding | Explicit plan-to-build simplicity review. |
| Choose the smallest reliable implementation among these approaches | Right-sizing an approach before implementation. |
| Compare our current queued export architecture with the smaller direct synchronous design for its only caller. No formal requirements document survives, but the current behavior and constraints are known. | Existing-system architecture comparison with an informal but sufficient decision frame. |
| Review this existing service architecture for overengineering before we add another component | Read-only system-design assessment before more machinery is added. |
| Look at how the import path uses Kafka and find opportunities to safely simplify it | Explicit assessment of a named technology in an existing technical area. |
| I am still brainstorming the export architecture. Point out opportunities to safely simplify this area before we settle on a design. | Targeted simplification during brainstorming, with an area to assess. |
| This completed approach adds a cache. Before coding, check whether existing request memoization already satisfies the requirements. | Tests reuse before adding a new implementation, with a reviewable subject. |
| Right-size this completed design draft without dropping its required behavior | Requests a smaller approach with a preservation constraint and current subject. |
| Review this draft plan, then implement it only if it is not overengineered | Places the checkpoint before the first edit. |
| Before coding, challenge the proposed adapter, queue, and configuration layer | Names complexity-bearing concepts in a proposed approach. |
| This build is about to add persistent state and a new dependency; check the approach first | In-build decision point before new machinery. |
| We have the core implementation working. Next I am adding a parser and schema for internal reviewer notes, a three-reviewer protocol, and fresh proof workspaces before and after every edit. Continue with that step. | Natural in-build decision advances ungrounded process machinery without an explicit simplicity request. |
| Our requirements and approach brief is complete and proposes a queue plus provider adapter, but no stated requirement or current consumer is tied to either mechanism. Before deepening it into an implementation plan, continue the workflow. | Completed early-planning handoff advances ungrounded durable machinery without an explicit simplicity request. |
| The owner asked for a direct export. The agent-authored requirements brief instead adds a queue, job table, provider adapter, and operator configuration that no approved requirement names. Before technical design or implementation planning begins, continue the workflow. | Narrow automatic backstop before agent-authored scope expansion enters technical planning. |
| The owner asked for a direct export. The agent-authored implementation plan newly adds a queue, persistent job table, and operator configuration that no approved requirement names. Hand it off to execution. | Narrow automatic backstop before unapproved durable machinery in a finished plan enters execution. |
| While implementing a direct owner-requested archive action, the agent newly proposes a dependency, persistent state, and a background worker as its next edit; none appears in the approved scope. Continue with that step. | Narrow automatic backstop immediately before unapproved agent-authored machinery is built. |
| Before coding this behavior change, does the existing repository mechanism already satisfy it? | Concrete reuse question on an inspectable technical area. |

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
| Plan and implement a small behavior change to add an archive action. No plan or approach exists yet; begin with planning, not a separate review. | The planning workflow owns the current step and may route here only after producing a reviewable subject. |
| We are still brainstorming whether an archive action is needed and what outcome it should produce | Requirements are unfinished; brainstorming owns the current task. |
| Implement the decided refactor now: replace the existing queue with a direct call while preserving behavior. Do not reassess the approach. | Prescribed implementation after the simplicity decision is settled. |
| The unchanged implementation plan already has a clean simplicity result recommending it proceed as written, with no open user question. Continue to implementation. | The assessment is complete; the executor owns the newly reached task. |
| The approved requirements brief is ready. Before creating the technical implementation plan, continue the workflow. | The planner owns an ordinary completed-brief handoff. |
| The implementation plan is ready at `/tmp/archive-plan.md`. Hand it off to execution. | The executor owns an ordinary finished-plan handoff. |
| Walk me through the tradeoffs between queues and direct calls for export systems. We are discussing the architecture, not deciding or implementing it yet. | Architecture explanation or brainstorming owns a discussion without simplification intent or an imminent implementation decision. |
| The approved design requires an audit log and a queue for regulated delivery, and the implementation plan maps those requirements directly. Hand it off to execution. | The executor owns implementation of owner-approved durable machinery. |
| While implementing the approved archive action, extract a small local helper for the existing validation call. | Ordinary implementation owns a non-durable code-level choice. |
