# Apple Messages CLI

Read this reference only when the host configures `imsg` as the authoritative
local Apple Messages interface. It adapts Messages evidence to the CRM source
contract; it does not authorize communication actions.

## Prove read access

Confirm the `imsg` executable and read-only database access before relying on
the source (check `imsg --version` and a 1-chat JSON read; consult
`imsg <subcommand> --help` for current flag names).

An authorization error means the parent agent application lacks macOS Full
Disk Access. Report Messages as unavailable until the user grants that access
and relaunches the parent. Reads require no Messages Automation permission.
Contacts permission is optional; missing resolved names narrows identity
evidence but raw handles remain available.

Use only these read-only subcommands for CRM evidence, always requesting JSON
output with explicit finite limits: `chats`, `history`, `search`, and `stats`.

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
`id` to `imsg history`; history rows report that same identifier as `chat_id`.
A display name alone is not an identity binding. Apply the previously loaded
identity rules before attaching private evidence to a Person note.

**Ordinary request** (no day-window scan): select one candidate chat and the
smallest date window that can change the current contact, memory, relevance, or
duplicate decision. Read `imsg history` with an explicit limit. Request
attachment metadata only when it can change that decision; never convert or
read attachment contents speculatively.

**Day-window scan** (wind-down Daily CRM Scan):

1. **Preflight and enumerate chats.** Prove read access, then list chats with
   `imsg chats` using a finite limit. Stop expanding the chat list when it is
   shorter than the limit or the finite chat budget is exhausted; mark Messages
   coverage **Partial** if the budget truncates before full-window confidence.
   Skip catch-up breadth probes and `stats` reconciliation.
2. **Read bounded in-window history.** For each chat, read `imsg history` with
   a finite limit from an inclusive start at the first local midnight of the
   scan window to an exclusive end at the midnight after the last local day in
   the configured vault timezone, each formatted as ISO 8601 including that
   boundary's applicable UTC offset.
3. **Check pagination and completeness.** Treat empty in-window history as no
   activity for that chat only when the returned count is below the limit. If
   the returned count equals the limit, do not treat the chat as fully
   observed; continue with a supported next page or tighter bound when
   available, or mark that chat and dependent Messages coverage **Partial**
   before zero-effect conclusions.
4. **Attribute senders and judge contact.** Attribute incoming rows by
   `sender`. For unanswered outgoing directed attempts, require `is_from_me`
   plus participant or recipient metadata that identifies the contact; leave
   the attempt unresolved when recipient binding is unavailable. After identity
   binding, evaluate substantive direct contact per bindable person under the
   relationship contract (including targeted group participation); leave
   unknown handles unresolved. Ambient reactions and broadcasts are not
   contact.

Use `imsg search` only when a concrete phrase or topic is necessary and a
conversation cannot first be selected safely. Search results remain identity
candidates until chat and participants are resolved.

Use message `guid` and history-row `chat_id` as source-local dedup evidence, not
a CRM registry. Use `created_at` as the native interaction instant and apply the
loaded time-normalization rules before proposing `date_last_contacted`. Keep
direct vs group context and the actual sender when judging contact.

Completion: each query has a defensible identity, purpose, date window, and
result limit; stable identifiers, per-sender attribution, and native timestamps
are retained as source evidence only.

## Prove catch-up breadth

For a user-approved catch-up inventory, enumerate chat metadata with a high
explicit limit. Treat the result as untruncated only when the returned count is
below that limit. Record only the observed count, activity bounds, identifier
coverage, result-limit behavior, and probe time in the visible preflight. Use
aggregate `imsg stats` JSON output in the configured vault timezone to
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
