# Set up and manage source mappings

Read this reference for first setup, listing or changing mappings, replying to
a binding preview, or proposing a map-location or access repair. Read
[source-bindings.md](source-bindings.md) first for map location, owning-system
access, schema, existing-version rules, and harness access selection. Apply
[source-access.md](source-access.md) before any source read or write. Routine
reviews use those resolution rules without repeating this setup interview.

## Discover connections and designate sources

For first setup, inspect the current harness's exposed capabilities and
available account metadata before recommending integrations. Keep three
facts separate: an integration is exposed, an access check succeeded, and the
user designated a source. Inventory and account checks need no content reads.
If inventory is unavailable, explain that limit and ask where the user keeps
the relevant information; do not report that no connections exist. Keep
personal and work identities distinct.

Start with relevant existing connections and systems the user already uses.
When a needed system is not connected, recommend a suitable integration and,
after the user chooses it, use the host's supported connection assistance.
The harness owns installation, authentication, consent, and reconnection.
Explain any step it cannot perform, allow deferral, and repeat discovery after
connection assistance. Store none of those connection states in the map.

Use [the fictional sample](../assets/sources.example.json) to explain the
schema, not as active configuration. Its identities and locators are
placeholders to replace with approved sources. Categories organize the
conversation; `roles` holds bindings, and absent roles remain unresolved.
The JSON is flat: each binding's `area` supplies its group. Present the starter
and configured bindings grouped by that field, using the labels below where
applicable. Keep custom area values visible under their own labels. This is a
presentation rule, not a nested JSON format or a reason to rewrite a map.
Shared access describes the usual route; optional complete harness overrides
reach the same designated source. [The map schema](source-bindings.md#schema) owns all field rules.

Walk through these categories one at a time, explaining the decisions they
support and allowing each to be skipped or deferred. Existing users requesting
a specific mapping operation go directly to [Manage mappings](#manage-mappings).

| Category / `area` | Decision supported | Starter roles and information needs |
| --- | --- | --- |
| Direction / `direction` | What matters and what should take priority? | `strategy`: values, goals, responsibilities, priorities and boundaries. |
| Commitments and time / `commitments` | What outcomes, actions and scheduled time need attention? | `projects`: outcomes and milestones; `tasks`: actions; `calendar`: scheduled time and availability. |
| People and communication / `relationships` | Who needs attention, and what has been communicated? | `relationships`: contact lookup and durable relationship context; `conversations`: relevant email, messages and provider meeting evidence; `meetings`: approved meeting notes. |
| Knowledge and reflection / `reflection` | What knowledge and experience should inform decisions? | `learning`: durable knowledge and decisions; `journal`: dated observations; `reviews`: completed reviews; `templates`: review and meeting guidance. |
| Resources and operations / `resources` | What resources and arrangements need attention? | `finances`: financial context; `operations`: personal and work operating information, preferences and arrangements. |
| Health and wellbeing / `health` | What supports health, energy and recovery? | `health`: user-selected health and wellbeing context. |
| Leisure and interests / `leisure` | What would I enjoy doing, watching or reading? | `leisure`: movie, TV, book, hobby and recreation recommendations. |

These are optional coverage prompts, not mutually exclusive source categories,
an exhaustive partition of someone's life, or a closed list of roles.
Organize by the information's primary purpose, not its file format or app.
Projects, tasks and calendar share a group but answer different questions.
Capacity can come from strategy or calendar; writing can come from projects or
tasks, with an additional source when draft content adds useful context.
A leisure reading list need not be a learning source, and a health appointment
can appear in calendar while its health context comes from the health source.
Give each binding one primary presentation group and reuse existing records.
Existing custom roles and area values remain valid; the starter does not
rename or consolidate a user's private map without approval.

Different communication channels and meeting providers can be separate bindings
under `conversations`; `meetings` can designate the durable destination for
approved notes. Under `relationships`, distinguish a contact directory used
for identity lookup from the designated owner of durable relationship context
and interaction history. A directory alone does not establish that owner.
The sample separates completed `reviews` from `templates`. Maps with templates
under `reviews`, custom roles, or omitted roles remain usable without migration:
use each binding's designation and filter to distinguish guidance from completed
activity. Template prompts are not evidence of completed work.
The starter prescribes no task statuses or productivity methodology. Add bounds
and detail as the user designates sources, using the documented map fields and
source-native metadata rather than inventing required fields. Inbox triage and
reservation booking are actions, not source roles: communication belongs under
`conversations`, and reservation preferences or arrangements can belong under
`operations`. A binding provides source context, not authorization to act.

Personal and work are source scopes within each area, not competing categories.
Use separate bindings when accounts or owners differ, keeping their scope in
`source`, `identity`, and bounds. One system can serve several roles; designate
each role's owner and avoid counting the same evidence twice. The sample is a
menu: omit unused roles rather than copying every example into a live map.
Its interface labels are placeholders to replace with capabilities discovered
in the user's harness, not required products or installation instructions.

For leisure, offer to map the user's existing content recommendation system,
watchlist, or reading list as a `leisure` role with `area: leisure`. Designate
its owner and bounded collection like any other source. Read only the relevant
shortlist when leisure choices matter to the review, not the full library on
every run. The map points to that system; it does not copy its recommendations
or replace it with a new recommendation engine. Leisure can be deferred.

Use supplied or configured task guidance and applicable review templates to
identify information needs before proposing new records. Read only the
requirements relevant to setup; full mode instructions belong to a selected
review. A template prompt establishes a need, not a populated source.

For each role being configured, establish the decision it informs, its
user-designated owner, bounded locator or query, any source restrictions,
and material effect of absence or conflict. Reuse answers already supplied.
Do not ask users to assign workflows to each source in a new map.
Ask which owner is primary when scopes overlap.

If the user needs help locating a source, first obtain their selected
account/system and bounded search scope. Search only within those bounds and
return candidates for designation; neither search results nor matching titles
establish ownership. Clarify ambiguous scope before content search. Without a
selected scope, ask rather than probing guessed role tokens or locations.
Leave deferred roles absent without blocking approved roles or a limited
review supported by other evidence.

## Manage mappings

Read the map and identify the requested entry by role, source, and access
details. Clarify only when multiple entries match. For **list**, group bindings
by their existing `area` and show roles, designated owners, shared access,
and overrides from the map; no native
source read or availability claim is needed.

For **add** or **update**, gather only missing designation or access details
and follow [Save an approved binding](#save-an-approved-binding). Target an
individual binding or override and preserve unrelated settings. Changing an
access description does not itself change ownership.

For **remove**, preview the exact binding or override to remove and the
resulting coverage. Removing the final binding omits the role, leaving it
unresolved. Removing an override makes shared access applicable for that
harness; show those shared details in the preview. Omit the override object
when its final member is removed. Follow the same approval, pre-edit check,
and save/readback procedure below. Removal changes the map only, never source
content or a harness connection. Readback verifies removal; a native read is
not required unless separately requested.

## Save an approved binding

Read the current map before previewing a change. An absent map can be created;
an invalid or unreadable map remains untouched pending user-directed repair.
Show the exact current and proposed source designation, shared access,
overrides, bounds, and any existing-map read rules affected by the change, including any
version upgrade. A failed read or moved note alone does not authorize a new
owner or locator. Obtain approval for the exact proposed change.

Use the map's owning interface to save the approved change, including the
Obsidian CLI for a vault-owned map. Inspect current content immediately before
editing. If an observed intervening change invalidates the approved proposal,
show a revised preview and obtain fresh approval. Make the smallest supported
edit and preserve unrelated entries. Read the saved map back and compare it with the
approved change and the preserved settings. Report failed or unavailable
saving/readback rather than claiming persistence. Host tools may provide
stronger safeguards; the skill does not guarantee locking, atomic replacement,
or detection of changes that the host tools cannot observe.

For added or changed access, after the saved binding reads back, follow
[Resolve harness access](source-bindings.md#resolve-harness-access), then read
the approved
bounded source through the selected interface and report that result
separately, naming the access description actually exercised. A successful
read verifies only that description. When an edited override belongs to another
harness, or edited shared access is hidden by the current harness's override,
report the change as saved but its access unverified; setup remains Partial
until a relevant harness selects and successfully reads that route. Preserve
current-runtime selection rather than reading another harness's override to
satisfy this check. A successful map write does not establish source access. If the
native read fails, retain the approved binding, mark setup incomplete for that role, and retry its read on
the next relevant session without repeating settled ownership questions.

Report the saved location. When establishing or changing it, preview the exact
map-location and pointer or caller changes for approval, including what
happens to the previous map file; propose removing it so no stale copy remains
for a later run to find at the default or an old pointer. Moving the map does
not change its bindings or authorize moving the sources it references. Keep
one canonical map, and update only the scoped pointers or explicit callers
the user authorizes. An explicit caller location or a pointer in a scoped
instruction or configuration file the host loads is sufficient; do not require
a global instruction entry or write one unless the user explicitly requests
it. An already moved map needs its current location and affected callers
reconciled, not another copy at the default. Propose new pointers only in such
files, never in note content.

Verify discovery in a fresh context without the setup transcript through the
chosen entry point: the caller's explicit location, an approved scoped or
private-context pointer, or the generic default. Read the map through its
owning interface. If this check is unavailable, say continuity is unverified;
pointer readback in the same conversation alone does not establish it.
Routine binding edits need no new continuity check. If the selected interface
cannot save or read back the change, provide a preview and explain the limit
without claiming it was saved. No change to a live caller is implied by a
skill-package update.

Completion: approved changes match map readback, added or changed access has
a separate native read result, and deferred roles and persistence or discovery
limits are named.

## Finish standalone setup

Standalone setup or management opens no review mode. When setup occurs inside
a new review, that review's ending governs instead. Judge completion by the
requested operation: listing requires a valid map read, removal requires saved
map readback, and added or changed access requires saved map readback plus a
successful bounded native read of that access description. A preview is not persistence, and persistence
is not source access. Failed access retains the saved owner.

Use one core run ending:

- **Complete:** all requested operations meet their completion checks.
- **Nothing material:** the requested bindings already match and their
  requested checks succeed, so no change was needed.
- **Partial:** some work finished, but a requested role is deferred or
  unresolved, access failed, or persistence/discovery remains unverified.
- **Unable to prepare reliably:** the map cannot be read or validated, so the
  requested operation cannot safely proceed.
- **Paused:** a preview awaits approval, designation is still pending, or the
  user intends to continue later.
- **Skipped:** the user chose not to perform the requested operation.

Recap configured mappings and verified changes separately from access results,
deferred or unresolved roles, and location/discovery limits. For listing or
removal, say native access was not checked. Include no review coverage
verdict, synthesis, recommendation, or review action.

Completion: the ending and recap match the requested operations and observed
results, with no preview, map save, or connection inventory treated as source
access or fresh-conversation continuity.
