# Linear provider and synchronization path

Load this reference for Linear reads, discovery, previews, effects, or
synchronization identity. The shared lifecycle, approval, batch-stop, and
outcome rules live in `SKILL.md`.

Pass every command through a structured process API, with each value as one
argument. Never interpolate tracker text into a shell command. Send multiline
body content through stdin when the installed command supports it.

## Resolve the installed command surface

Resolve the Orca executable once per session using the installed `orca-linear`
discovery stub: honor `ORCA_CLI_COMMAND`; otherwise use `orca-dev` in an
`ORCA_DEV_REPO_ROOT` checkout; otherwise use `orca-ide` on Linux outside an
Orca-managed terminal; otherwise use `orca`. Reuse that exact executable and do
not fall through to another binary after an error.

Before constructing any Linear command, load the full version-matched guide:

```text
ORCA skills get orca-linear
```

`ORCA` is the resolved executable placeholder, not a literal command or shell
variable. The returned guide is the only authority for current Linear read and
write syntax. Do not reconstruct commands from this reference or memory.

If and only if the binary explicitly reports `skills get` as unknown, it is a
confirmed pre-guide binary. Its bounded bootstrap permits reads only: provider status,
Linear help, and a full read of the current issue, exactly as listed by the
installed discovery stub. It cannot produce an executable write preview. An
absent guide, incompatible guide, failed selected executable, failed
authentication, or write surface that cannot express the approved effect stops
before an executable preview.

## Authenticate, resolve, and discover

Follow the loaded guide to confirm Orca provider status. Successful
authentication supplies provider identity.

Discover the exact workspace, team, workflow states, labels, and members needed
for the requested effect using the guide's JSON commands. Require one workspace
and one team matching the normalized target. Prefer stable IDs; accept a name
only when it matches exactly and uniquely within its provider scope. Linear
priority is the native provider value; estimates apply only to implementation
leaves; readiness uses an exact discovered label identity, never workflow
status.

Read the canonical issue, including material fields and relationships, through
the guide before preview, immediately before its write, and immediately after
the accepted write. Require the returned workspace, team, issue ID, identifier,
and URL to match the normalized target and selector exactly. A workspace or team
mismatch is not a canonical issue and permits no write.

Require successful JSON/RPC results and inspect any provider warnings or partial
section metadata. A missing or capped requested section is unknown rather than
empty. Exhaust direct-child pages for each parent with the guide's supported
parent filter, following every nonempty next cursor. Require every child page's
`workspaceErrors` to exist and be empty. Require every relationship read's
`includeErrors` to exist and be empty and its relationship `capReached` value
to be exactly false. A failed page, empty or repeated cursor before exhaustion,
missing field, warning, or cap makes coverage partial. Follow
`graph-and-completion.md` for family traversal and the shared node limit.

## Creates, surgical updates, and lifecycle

Construct commands only after loading the guide. Prefer its field-specific
status, priority, estimate, label, assignee, and relationship mutations for
surgical updates. Prefer label add/remove to whole-set replacement. If only a
whole-record save or whole-label-set operation can express an approved effect,
reread the complete current set immediately before writing and show the exact
resulting set in the preview; any drift stops the batch.

A create may set approved node metadata atomically when the loaded guide
supports it, but cannot attach graph edges. Supply a unique write identity when
the guide supports one. Accept the response only when it returns an exact issue
identity tied to that attempt; read it back and require exact workspace, team,
identifier, and URL matchback. Managing Issues applies every effect once: even
if the general Orca guide offers a retry for an unconfirmed write, an
unconfirmed Managing Issues create is `indeterminate` and is never retried or
similarity-matched.

For a graph batch, require the loaded guide to expose every needed parent,
child, blocker, and inverse or removal effect before previewing any node. Use
only that version-matched syntax. After nodes have exact readbacks, apply each
approved relationship once and read both endpoints back. If the guide cannot
express any required edge or its readback, the graph is unsupported and no
graph node is written.

Use the guide's field-specific status operation for reversible lifecycle
changes. Select only an exact discovered state whose type represents the
approved transition. Cancellation targets a canceled state. Completion targets
a completed state only after `graph-and-completion.md` proves completion. Read
back the exact state and type.

## Synchronization identity and write direction

The optional repository-relative synchronization mapping has this fixed
identity shape:

```json
{"version":1,"github_to_linear":{"OWNER/REPO#NUMBER":"TEAM-123"}}
```

The config validator owns parsing and validation. The top-level config provider
alone selects write direction, so either provider may be canonical. Resolve one
exact mapping entry in the approved direction. Missing, malformed,
contradictory, or ambiguous identity writes neither provider. Never infer an
identity from title, body, branch, search result, or synchronized marker.

Write and read back only the canonical record. The projection may be read for
identity or lag evidence but never mutated, repaired, or used as fallback after
a canonical provider failure.
