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

Record each result at the scope actually exercised. Fixture behavior, conceptual
decisions, and provider implementation are distinct claims. A missing environment
for testing a provider is not a skill-readiness blocker; a demonstrated wrong
approval, ordering, or reporting decision in the skill remains a defect.
