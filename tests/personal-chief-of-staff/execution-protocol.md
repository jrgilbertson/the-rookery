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
and keep the synthetic user home outside the repository. An external test adapter
may substitute `Path.home()` only in the bundled map helper's process. Do not
change `HOME`, add test controls to the shipped helper, or expose the map location
in a discovery prompt. Record the adapter and loaded package with the original
session and native-source traces. A native discovery smoke omits any skill path
from the request; a forced-load case proves behavior after loading only.

Record each result at the scope actually exercised. Fixture behavior, conceptual
decisions, and provider implementation are distinct claims. A demonstrated wrong
approval, ordering, or reporting decision remains a defect. When the accepted
change explicitly requires a provider, its unavailable test environment leaves
that acceptance requirement incomplete; neither another provider nor fixture
success substitutes for it. Run official provider CLIs through subscription
authentication when required by the test session; never fall back to API billing.
