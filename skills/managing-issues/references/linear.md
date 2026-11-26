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

For every Linear proposal or explanation of why one is unavailable, render:

```text
Linear gate: transport=...; authentication=...; matchback=...; capabilities=...; command-authority=...
```

Fill each value with the confirmed state or `unresolved`. `matchback` names
the exact workspace, team, and issue. `capabilities` is `complete` only when
the selected path exposes every operation needed by the whole proposed batch.
`command-authority` names the runtime tool schemas for MCP or the installed
version-matched `orca-linear` guide. Missing required MCP tools, or a missing
or incompatible Orca guide, stops before building commands.

## Resolve the Orca commands

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

If and only if the binary reports `skills get` as unknown, it is a confirmed
pre-guide binary. Its bounded bootstrap permits reads only: provider status,
Linear help, and a full read of the current issue, exactly as listed by the
installed discovery stub. It cannot produce an executable write preview. An
absent or incompatible guide, a failed executable, failed authentication, or
write tools that cannot express the approved effect stop the selected Orca
path before an executable preview.

## Authenticate, resolve, and discover

Confirm authentication through the selected transport and use the active
account as provider identity only. For MCP, a successful authenticated tool
read confirms it. For Orca, follow the loaded guide to confirm provider status.

Discover the exact workspace, team, workflow states, labels, members, and
projects needed for the requested effect through the selected transport.
Require one workspace and one team matching the normalized target. Prefer
stable IDs; accept a name only when it matches exactly and uniquely within
its provider scope. Linear config maps each priority name `urgent`, `high`,
`medium`, and `low` to itself, not to a transport-specific argument, and the
validator rejects any other value. At the MCP boundary, translate the chosen
name using the runtime schema's documented mapping. In the current Linear MCP
schema, `urgent` is `1`, `high` is `2`, `medium` is `3`, `low` is `4`, and
`0` means no priority is set. Pass the number, never the config string, when
the schema requires a number. If the runtime schema differs or omits an exact
conversion, stop before preview rather than guess. For Orca, use the
version-matched guide's documented representation. Estimates apply only to
implementation leaves; readiness uses an exact discovered label identity,
never workflow status.

During first-use setup, present the native estimate choices and exact existing
labels beside the Linear starter recommendations, and show the four priority
mappings as fixed. Recommend a workspace-scoped readiness group named
`readiness` with kebab-case children `needs-discovery`, `needs-planning`, and
`ready`. Offer the team's members as default-assignee candidates and store the
chosen member's stable user ID. The operator chooses every mapping except
priority. Do not change the team's native priority or estimation scheme.

The four scores are labels in single-select label groups, one group per
factor. Recommend workspace-scoped groups named `impact`, `confidence`,
`verification-effort`, and `undo-cost`, each with three children named for the
factor and the score: `impact-1` to `impact-3`, `confidence-1` to
`confidence-3`, `verification-effort-1` to `verification-effort-3`, and
`undo-cost-1` to `undo-cost-3`. Name each child for its factor because
Linear's GitHub sync mirrors a child under its own name with no group prefix.
Offer existing single-select groups with three children beside these
recommendations.

When a chosen general label is absent, offer a flat label create. When a chosen
readiness or score child is absent, offer the group-then-children recipe: create the
workspace group if it is absent, then any missing children, then rediscover
each chosen child. Apply a child, never the parent. Store a unique child name,
or the label UUID when the name is not unique. Missing group-create must not
block creating a general label such as `bug`.

Offer any of those creates only if the selected transport exposes an exact
label-create and label-readback path. For connected MCP this is normally the
runtime `save_issue_label` and `list_issue_labels` tools; for Orca it must
come from the loaded guide. The current MCP schema creates a workspace group
with `isGroup` true, `groupType` `singleSelect`, and no `teamId`, and children
with `parent` set to the group name and no `teamId`. The current Orca guide
has no label create, so a session on that transport that still needs one
stops as the next sentences describe. If the runtime schema differs, follow it. If the
approved batch still needs a workspace-scoped group or child create the
selected path cannot express, stop setup without a config write and name the
missing capability. Do not fall through to Orca.

The current MCP schema can update, retire, and restore a label but cannot
delete one, and setup never changes an existing label. Preview the exact provider effects, apply
each approved create once, then rediscover every chosen child by exact stable
identity before rendering the config. A failed or partial create uses the
shared first-stop: later effects stay unapplied, config is not written, and
leftover labels are manual cleanup.

For updates and lifecycle changes, read the canonical existing issue, including
material fields and relationships, before preview, immediately before its
write, and immediately after the accepted write. Require the returned
workspace, team, issue ID, identifier, and URL to match the normalized target
and selector exactly. A workspace or team mismatch is not a canonical issue and
permits no write. For creates, require the exact normalized workspace and team
target plus every needed capability and metadata read before preview and again
immediately before the write, then require the exact returned-identity readback
described below.

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
project, and relationship mutations for surgical updates. Use the issue's
native project field. Prefer label add/remove to whole-set replacement. If only a whole-record save or whole-label-set operation
can express an approved effect, reread the complete current set immediately
before writing and show the exact resulting set in the preview; any drift stops
the batch.

Read an issue's scores from its labels: a score is present when the issue
carries exactly one of that factor's three mapped children. No child is an
absent score, and more than one makes that score unreadable. A label read that failed or was capped makes the scores unreadable.
Linear rejects a second child from one single-select group, so change a score
in one update that removes the old child and adds the new one, and show both
in the preview. Set the scores on a create with the create's own labels.

A create may set approved node metadata atomically when the selected transport
supports it. Managing Issues attaches no graph edges at create, though Linear
may add predictable automation such as automatic cycle assignment or a related
link from an issue mention in approved content. Name every issue the approved
content mentions in the preview so the operator sees those links beforehand.
Supply a unique write identity when the transport supports one. Accept the
response only when it returns an exact issue identity tied to that attempt,
then read it back and verify exact workspace, team, identifier, and URL match.

In that readback, request the created issue's parent, direct children, and
other relationships because a default issue read may omit them. For MCP,
`includeRelations` covers blocking, related, and duplicate links; it does not
cover parents or children. Require a parent value (including an empty value
when absent) and an exhaustive direct-child collection, using a separate
provider-native read and all pages when needed. Follow only the selected
transport's authoritative schema or guide for these reads, and never assume
one relation flag covers hierarchy. Missing or partial parent, direct-child,
or other relationship readback is unknown, as for any missing requested
section. Leave the create `applied`, mark later effects `unapplied`, stop
before the next effect, and report the exact unconfirmed fields.

A related link to an issue the approved content mentions is predictable
automation, so report it and continue. Any unapproved parent, child, or other
relationship follows the provider-automation rule in `SKILL.md`. Even if an
Orca guide or MCP client offers a retry for an unconfirmed write, treat an
unconfirmed create as `indeterminate` under `SKILL.md` and never retry it.

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
