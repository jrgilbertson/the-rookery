# Chief-of-staff test execution

Test the skill's decisions and use of source results. The Obsidian CLI owner
owns command parsing, file operations, and CLI compatibility tests; this suite
requires no live vault, test notes, or separate Obsidian installation.

Run each case in a fresh agent context. Load the current skill and the resources
its scenario needs before answering or using fixtures. Keep that loading record,
the conversation, and tool calls/results outside the repository for an
independent grader. Prior/candidate comparisons use identical case inputs.

For fixture cases, use the supplied executables and synthetic sources only.
Do not call real connectors or access personal data. Keep fixture state in a
fresh temporary directory outside the repository and remove it after grading.
The grader inspects the actual commands, responses, and fixture trace; unrelated
available tools do not invalidate a run simply by being available. A call to a
real source, a substituted result, or missing skill loading invalidates the
affected result. An incomplete trace leaves the affected claim unverified.
There is no requirement for a custom launcher that disables every other tool.

For decision-only cases, supply the named source results as premises and perform
no operations. Grade what the agent proposes, permits, refuses, or reports.
These checks cannot establish executed writes or provider compatibility.

For source-binding cases, install each frozen skill copy in a disposable project
and keep synthetic private storage outside the repository. Use the host's file
capabilities against that isolated storage; do not change `HOME` or expose the
map location in a discovery prompt. Supply the sandbox's private location
pointer through persistent host context when its default home cannot be
isolated. Record that context, loaded package, file operations and readback,
and native-source traces with the original session. A native discovery smoke omits any skill path
from the request; a forced-load case proves behavior after loading only.

Record each result at the scope actually exercised. Fixture behavior, conceptual
decisions, and provider implementation are distinct claims. A demonstrated wrong
approval, ordering, or reporting decision remains a defect. When the accepted
change explicitly requires a provider, its unavailable test environment leaves
that acceptance requirement incomplete; neither another provider nor fixture
success substitutes for it. Run official provider CLIs through subscription
authentication when required by the test session; never fall back to API billing.

For mapped two-turn interruption and drift evals, retain the same native executor
session and fixture state across the explicit turn boundary. Capture the first
turn trace separately before continuing with the exact stated user reply. A
fresh executor, substituted second read or pre-seeded successful effect does
not establish recovery or post-approval revalidation. The drift source marker
permits one second authoritative read only for its designated roles; ordinary
one-read cases retain their limit. Capture the resolved copied fixture binary
paths with every executed case.
