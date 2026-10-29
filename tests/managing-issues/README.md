# Managing Issues checks

The fixture runners check the shipped configuration helper and the published
text contracts. Run them through the complete repository gate:

```sh
lefthook run pre-push --force
```

The runners do not execute an agent or validate the real providers' APIs.

[Graph and lifecycle cases](cases/graph-and-lifecycle.md) preserve the behavioral
expectations separately from the deterministic gate. They are case
definitions, not execution results. Their outcomes remain Unmeasured until
evaluated against the shipped skill.

## Evaluate the skill

Follow [SKILLS.md](../../SKILLS.md#evaluation-workflow) for an authorized native
host run. The repository has no Managing Issues behavioral launcher. Prepare
only the selected cases and obtain the required execution allowance before
model calls. Keep generated configurations, traces, and results outside this
public repository.

Load the unchanged [skill](../../skills/managing-issues/SKILL.md) and applicable
references through normal skill discovery. Give the executor only the case's
request and synthetic provider state. Keep expected observations out of its
input. The case tables describe provider facts, not a prompt-level exemption
from fetching or approval requirements.

For tool-backed cases, the launcher must expose only synthetic provider tools,
with no host connectors or credentials. Prepare those tools and the case state
in a disposable external directory. If a scenario's responses or isolation
cannot be supplied, record it as not run rather than substituting prose claims that reads occurred.
Inject drift and errors at the specified call, not in the executor's prompt.

Review the actual skill-load evidence, provider calls, state before and after,
and final response. A case passes only when those observations support its
expected result. Check presentation and execution separately: an accurate
summary cannot excuse an extra write, and a correct trace cannot excuse a
false completion claim. Record the host and skill revision with each result;
missing execution evidence is Unmeasured. Passing fixture runners never grades
these cases.
