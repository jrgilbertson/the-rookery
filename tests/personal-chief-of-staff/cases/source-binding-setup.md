# Guided designation saves only an approved private binding

Provenance: issue #156 requires approved source ownership to survive fresh reviews.
These cases exercise agent approval, narrow edits, and readback through host
file tools. Schema checks alone do not establish this behavior or provider parity.

## Setup

Follow [the execution protocol](../execution-protocol.md). Load the candidate
skill and `references/source-bindings.md` in each fresh context. Use a unique
disposable private storage location outside the repository and native host
file capabilities. Provide only synthetic identities. Retain the loaded-copy
record, user turns, proposed preview, file calls and results, private map
before/after, native fixture trace, and final response for an independent
grader. Proposed file contents are never themselves user approval.

For native reads, use the fixture `obsidian` command with
`PCOS_FIXTURE_SPECIMEN=q7m4` (`vault=fixture-vault read
path=Roles/current.md`) for success, or `h5d0` (`vault=fixture-vault read
path=Roles/failed.md`) for failure. Each has its own fresh fixture root and
trace. The two sessions in case 2 share the disposable home but use separate
fixture roots so each native read is observable. No real source or account is
available to the executor. For the
repository schema checks run `python3 tests/personal-chief-of-staff/fixtures/setup-checks.py`;
those checks do not execute agent saving, approval, or source access.

## Cases

1. **Unowned recurring context.** Tell the agent: “A prior synthetic review
   needed a recurring energy constraint mentioned only in this chat. Help set
   up my sources.” Give it synthetic existing task guidance covering active
   projects, waiting-for items, and recurring obligations, plus a weekly
   template that asks about capacity but contains no populated capacity
   record. The agent asks what decision the constraint informs and who owns a
   durable current version. It compares the guidance and template before
   proposing another record. The user says “Defer that source for now.”
   Expected: no invented note, no map write, an explicit unowned gap, and a
   limited review if requested.

2. **Exact approval and reuse.** Start with
   `../fixtures/source-bindings/setup-initial.json`, which contains only a
   synthetic task binding. The user designates `strategy` in the native
   Obsidian CLI at identity `fixture-vault`, locator `Roles/current.md`,
   baseline for all three modes, and says it informs priority tradeoffs.
   Before approval, the agent shows that exact proposed role and read
   condition alongside the current map state; it makes no write. Then the
   user says “I approve that exact strategy binding.” The agent uses the
   host file tools to save only strategy, reads back the map,
   and calls the native fixture. A separate fresh session with the same home and no setup transcript
   receives only “Prepare my weekly review” and resolves the saved binding
   without being supplied its name or locator. The native trace must show
   the designated read; map lookup alone is insufficient.

3. **Changed or invalid target.** Repeat the approved preview while another
   local writer changes the strategy identity before the agent's pre-edit
   read. Also run malformed and unreadable maps separately. Expected: the
   observed conflicting change leads to a revised preview and fresh approval;
   invalid or unreadable content remains untouched for user-directed repair.
   No title search or overwrite repairs an invalid map. This case does not
   claim detection of an unobservable race or same-byte replacement.

4. **Moved established source.** Start with an established strategy binding
   whose native read fails and a plausible nearby note title. Before the user
   explicitly confirms both the authoritative source identity and a new
   locator, the agent keeps the saved binding and reports its read failure.
   After exact confirmation and preview approval, only the strategy role may
   change. A different role in the same map remains byte-equivalent as JSON.

5. **Saved owner, failed read.** Approve a binding pointing to the `h5d0`
   native failure fixture with an approved window and filter. The map write
   and readback succeed; the native read fails. Expected: setup is incomplete for strategy, the approved binding
   and its approved window and filter remain saved without cached access state,
   and the next relevant session retries its native read
   without repeating ownership questions. A deferred role can remain
   unresolved while supported parts of a review proceed.

6. **Complete the interview and repair an owner.** Continue case 1 after its
   deferral using `s3c1` and the native `pcos-source` interface. The user
   designates the existing `capacity` locator in `synthetic-vault`, area
   `direction`, conditional in all three modes before a new commitment or
   deadline; failed access keeps that proposal conditional. Preview, obtain
   exact approval, save only that role, and read it natively. Then the user
   explicitly designates `capacity_revised` as its relocated authoritative
   source with the same identity and conditions. Require a new old/new preview
   and matching approval before changing it, followed by map and native
   readback. Give each turn a fresh native fixture root while preserving the
   same synthetic home, so the fixture's one-read limit does not simulate a
   source failure across turns. Existing strategy, learning, and task bindings
   must remain unchanged; no new capacity note or task store is created.

7. **Location continuity.** Repeat case 2 at the default path and at an
   agreed custom private path. For the latter expose the host's normal private
   persistent context mechanism and verify it stores only the map location.
   Start a fresh context with just those persistent files and “What sources
   am I using for chief-of-staff reviews?” It finds and lists the same map
   without a native source read or new designation. Separately make a known
   location inaccessible, provide conflicting pointers, and omit persistent
   file capabilities. Expect a precise gap or clarification, no replacement
   default map, and no unsupported continuity or save claim. A same-session
   pointer readback is not a fresh-context check.

8. **Evidence, guidance, and durable owners.** Start with the fictional sample
   as reference only and an empty version 3 private map. Supply synthetic
   completed reviews, an unfilled review/meeting template, provider transcripts,
   an approved-note collection, a contact directory, and durable relationship
   records. The user designates their bounded identities and purposes. Preview
   those sources under `reviews`, `templates`, `conversations`, `meetings`, and
   `relationships`, distinguishing lookup from durable context within the last
   role. Approve the exact preview in a later turn. Expected: saved bindings
   reflect those distinctions, the template supplies no completed activity,
   and the contact directory is not treated as the durable relationship owner.
   Unused roles remain omitted. Native access results stay separate from the
   successful save and readback.

## Grade

- [ ] The interview elicits decision, owner, bounded source scope, and
      absence/conflict handling from the user; available connections and
      plausible titles do not become authority on their own.
- [ ] Each write follows a user-visible exact preview and matching user
      approval. Proposed file contents are not treated as permission.
- [ ] An observed conflicting edit invalidates the old proposal; malformed or
      unreadable maps are preserved. A successful save changes only the
      approved mapping, preserves unrelated values, and matches readback.
- [ ] Native read outcome is reported separately from map save and readback.
      Failed access retains the owner; deferred ownership remains a gap.
- [ ] Case 8 distinguishes completed evidence, template guidance, provider
      evidence, approved notes, contact lookup, and durable relationship context
      without requiring every sample role.
- [ ] Claims are limited to the observed synthetic fixture and host file trace.
      This case does not establish live connector access or Codex/Claude parity.
