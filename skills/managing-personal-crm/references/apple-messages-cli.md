# Apple Messages CLI

Read this reference only when the host configures `imsg` as the authoritative
local Apple Messages interface. It adapts Messages evidence to the CRM source
contract; it does not authorize communication actions.

## Prove read access

Confirm the executable and read-only database access before relying on the
source:

```text
imsg --version
imsg chats --limit 1 --json
```

An authorization error means the parent agent application lacks macOS Full
Disk Access. Report Messages as unavailable until the user grants that access
and relaunches the parent. Reads require no Messages Automation permission.
Contacts permission is optional; missing resolved names narrows identity
evidence but raw handles remain available.

Use only these read surfaces for CRM evidence:

```text
imsg chats --limit <count> --json
imsg history --chat-id <id> --limit <count> --json
imsg history --chat-id <id> --start <inclusive-iso8601> --end <exclusive-iso8601> --limit <count> --json
imsg search --query <text> --match contains --limit <count> --json
imsg stats --time-zone <iana-zone> --json
imsg stats --chat-id <id> --time-zone <iana-zone> --json
```

Do not invoke `send`, `react`, `read`, `typing`, `launch`, group mutation,
native polls, or advanced bridge operations as part of this skill. Do not start
`watch` for ordinary direct, embedded, or catch-up reads. If the user asks to
communicate, return proposed text or route the request to its configured owner;
the CRM approval does not authorize sending.

Completion: the installed CLI returns structured chat metadata, or Messages is
marked unavailable with the exact permission or execution failure.

## Bound ordinary reads

Resolve a candidate conversation from `imsg chats` using its `id`, raw
participant handles, group status, and available contact names. Pass the chosen
`id` to `imsg history --chat-id`; history rows report the same value as
`chat_id`. A display name alone is not an identity binding. Apply the previously
loaded identity rules before attaching private evidence to a Person note.

For a direct or embedded request that is not a required day-window scan, select
one candidate chat and the smallest date window that can change the current
contact, memory, relevance, or duplicate decision. Use `imsg history` with an
explicit limit. Add `--attachments` only when attachment metadata can change
that named decision; never convert or read attachment contents speculatively.

When a caller requires a day-window relationship scan (wind-down Daily CRM
Scan), enumerate chats with activity in the scan window using finite limits,
then read each candidate chat's history with explicit `--start` / `--end` (or
equivalent bounds) and an explicit limit. Do not run catch-up breadth probes for
that scan. Attribute each history row by its `sender` handle. Evaluate
substantive directed contact per speaker after identity binding; leave unknown
handles unresolved. A group chat may support effects for some senders and none
for others in the same thread. Ambient reactions and broadcasts do not count as
contact.

Use `imsg search` only when a concrete phrase or topic is necessary and a
conversation cannot first be selected safely. Search results remain identity
candidates until their chat and participants are resolved.

Use the message `guid` and history-row `chat_id` as source-local deduplication
evidence, not as a new CRM registry. Use `created_at` as the native interaction
instant and apply the previously loaded time-normalization rules before
proposing `date_last_contacted`. Preserve direct versus group context and the
actual sender when deciding whether contact was substantive.

Completion: the query is bounded to a defensible identity, purpose, date
window, and result limit, with stable identifiers, per-sender attribution, and
native timestamps kept as source evidence only.

## Prove catch-up breadth

For a user-approved catch-up inventory, enumerate chat metadata with a high
explicit limit. Treat the result as untruncated only when the returned count is
below that limit. Record only the observed count, activity bounds, identifier
coverage, result-limit behavior, and probe time in the visible preflight. Use
aggregate `imsg stats --time-zone <configured-iana-zone> --json` output to
corroborate the accessible history range without exposing message text.

The chat list's earliest recent activity is not automatically the database's
earliest message. Aggregate statistics may omit a chat that has no retrievable
history rows, so their chat count need not equal the chat-list count. When the
counts differ, compare identifiers symmetrically. Accept the difference only
when no statistics-only identifier exists and every list-only chat returns zero
history rows from an exact bounded probe. Otherwise mark breadth
**Indeterminate**. Also mark it **Indeterminate** if enumeration truncates,
timestamps cannot be reconciled, or the database reports a schema or
permission error.

Completion: catch-up records an honest enumeration result, accessible date
range, supported read surfaces, stable identifiers, native timestamps, and one
representative boundary query without retaining raw message content.
