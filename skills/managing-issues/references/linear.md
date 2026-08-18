# Linear provider path

Load this reference for Linear reads, discovery, previews, or effects. The
shared lifecycle, approval, batch-stop, and outcome rules live in `SKILL.md`.

## Select one session transport

Repository config selects Linear as the canonical provider but never stores a
transport. Honor an explicit operator choice between connected Linear MCP tools
and the Orca CLI. Otherwise select an available authenticated Linear MCP; use
Orca when MCP is unavailable or the operator chooses it. Select one before
an executable preview. Never switch transports after a failed, indeterminate,
or partially applied effect; a different transport is a new proposal requiring
a fresh canonical read, complete preview, and approval.

For MCP, the runtime-exposed tool schemas are the command authority. Require an
authenticated connection and each exact operation required by the proposed
batch. Preserve tracker text in structured tool fields. A missing operation
makes that effect unavailable; do not reconstruct private API calls or fall
through to Orca.

For Orca, pass every command through a structured process API, with each value
as one argument. Never interpolate tracker text into a shell command. Send
multiline body content through stdin when the installed command supports it.

## Resolve the Orca command surface

Resolve the Orca executable once per session using the installed `orca-linear`
discovery stub: honor `ORCA_CLI_COMMAND`; otherwise use `orca-dev` in an
`ORCA_DEV_REPO_ROOT` checkout; otherwise use `orca-ide` on Linux outside an
Orca-managed terminal; otherwise use `orca`. Reuse that exact executable and do
not fall through to another binary after an error.

Before constructing any Orca Linear command, load the full version-matched
guide:

```text
ORCA skills get orca-linear
```

`ORCA` is the resolved executable placeholder, not a literal command or shell
variable. The returned guide is the only authority for current Linear read and
write syntax. Do not reconstruct commands from this reference or memory.

If and only if the binary explicitly reports `skills get` as unknown, it is a
confirmed pre-guide binary. Its bounded bootstrap permits reads only: provider
status, Linear help, and a full read of the current issue, exactly as listed by
the installed discovery stub. It cannot produce an executable write preview. An
absent guide, incompatible guide, failed selected executable, failed
authentication, or write surface that cannot express the approved effect stops
the selected Orca path before an executable preview.

## Authenticate, resolve, and discover

Use the selected transport to confirm authentication. For MCP, a successful
authenticated tool read supplies provider identity. For Orca, follow the loaded
guide to confirm provider status. Authentication supplies identity only.

Discover the exact workspace, team, workflow states, labels, and members needed
for the requested effect through the selected transport. Require one workspace
and one team matching the normalized target. Prefer stable IDs; accept a name
only when it matches exactly and uniquely within its provider scope. Linear
config stores the canonical priority names `none`, `urgent`, `high`, `medium`,
and `low`, not a transport-specific argument. At the MCP boundary, translate
the chosen name with the runtime schema's documented mapping. For the current
Linear MCP schema that is `none` to `0`, `urgent` to `1`, `high` to `2`,
`medium` to `3`, and `low` to `4`; pass the resulting number, never the config
string, when the schema requires a number. If the runtime schema differs or
does not document an exact conversion, stop before preview rather than guess.
For Orca, use the version-matched guide's documented representation. Estimates
apply only to implementation leaves; readiness uses an exact discovered label
identity, never workflow status.

During first-use setup, present the native priority and estimate choices and
exact existing labels beside the Linear starter recommendations. The operator
chooses the mappings. Do not change the team's native priority or estimation
scheme. When a chosen general or readiness label is absent, offer its creation
only if the selected transport exposes an exact label-create and label-readback
path. For connected MCP this is normally the runtime `create_issue_label` and
`list_issue_labels` surface; for Orca it must come from the loaded guide.
Preview the exact provider effects, apply each approved create once, then
rediscover every chosen label by exact stable identity before rendering the
config. If the selected path lacks either operation, stop setup without a config
write and name the missing capability.

Read the canonical issue, including material fields and relationships, through
the selected transport before preview, immediately before its write, and
immediately after the accepted write. Require the returned workspace, team,
issue ID, identifier, and URL to match the normalized target and selector
exactly. A workspace or team mismatch is not a canonical issue and permits no
write.

Require successful structured results and inspect the selected transport's
error, warning, partial-section, pagination, and cap indicators. A missing or
capped requested section is unknown rather than empty. Exhaust every supported
direct-child page for each parent. For Orca guide reads, require every child
page's `workspaceErrors` to exist and be empty; require every relationship
read's `includeErrors` to exist and be empty and its `capReached` value to be
exactly false. For MCP, follow every cursor or pagination field its runtime
schema exposes; if its tools cannot prove the requested relationship collection
is exhaustive, coverage is partial. A failed page, empty or repeated cursor
before exhaustion, missing field, warning, or cap makes coverage partial.
Follow `graph-and-completion.md` for family traversal and the shared node limit.

## Creates, surgical updates, and lifecycle

Construct effects only after resolving the selected transport's command
authority. Prefer field-specific status, priority, estimate, label, assignee,
and relationship mutations for surgical updates. Prefer label add/remove to
whole-set replacement. If only a whole-record save or whole-label-set operation
can express an approved effect, reread the complete current set immediately
before writing and show the exact resulting set in the preview; any drift stops
the batch.

A create may set approved node metadata atomically when the selected transport
supports it, but cannot attach graph edges. Supply a unique write identity when
the transport supports one. Accept the response only when it returns an exact
issue identity tied to that attempt; read it back and require exact workspace,
team, identifier, and URL matchback. Managing Issues applies every effect once:
even if an Orca guide or MCP client offers a retry for an unconfirmed write, an
unconfirmed Managing Issues create is `indeterminate` and is never retried or
similarity-matched.

For a graph batch, require the selected transport to expose every needed parent,
child, blocker, and inverse or removal effect before previewing any node. Use
only its authoritative runtime schema or version-matched syntax. After nodes
have exact readbacks, apply each approved relationship once and read both
endpoints back. If the selected transport cannot express any required edge or
its readback, the graph is unsupported and no graph node is written.

Use the selected transport's field-specific status operation for reversible
lifecycle changes. Select only an exact discovered state whose type represents
the approved transition. Cancellation targets a canceled state. Completion
targets a completed state only after `graph-and-completion.md` proves
completion. Read back the exact state and type.
