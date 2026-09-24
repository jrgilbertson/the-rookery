# Guided designation saves only an approved private binding

Provenance: issue #156 requires approved source ownership to survive fresh reviews.
The existing helper accepted only `read`. The focused setup check first failed
all five cases because `snapshot` was rejected with usage code 2. This is a
discriminating setup case, not evidence of provider parity.

## Setup

Follow [the execution protocol](../execution-protocol.md). Load the candidate
skill and `references/source-bindings.md` in each fresh context. Use a unique
disposable user home outside the repository and the shipped
`scripts/source-bindings.py` against that home. Provide only synthetic
identities. Retain the loaded-copy record, user turns, proposed preview,
helper calls and results, private map before/after, native fixture trace, and
final response for an independent grader. The helper's `write` command receives
JSON through standard input; its payload is never itself user approval.

For native reads, use the fixture `obsidian` command with
`PCOS_FIXTURE_SPECIMEN=q7m4` (`vault=fixture-vault read
path=Roles/current.md`) for success, or `h5d0` (`vault=fixture-vault read
path=Roles/failed.md`) for failure. Each has its own fresh fixture root and
trace. The two sessions in case 2 share the disposable home but use separate
fixture roots so each native read is observable. No real source or account is
available to the executor. For the
mechanical write checks run `python3 tests/personal-chief-of-staff/fixtures/setup-checks.py`;
that suite mocks `Path.home`, invokes the shipped helper, and uses synthetic
`source-bindings/setup-*.json` entries.

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
   preview snapshot and the helper to save only strategy, reads back the map,
   and calls the native fixture. A separate fresh session with the same home
   receives only “Prepare my weekly review” and resolves the saved binding
   without being supplied its name or locator. The native trace must show
   the designated read; map lookup alone is insufficient.

3. **Changed or invalid target.** Repeat the approved preview while another
   local writer replaces the map with the same JSON bytes before the write.
   Also run a symlinked map, a symlinked parent, a malformed map, and an
   unreadable map separately. Expected: the helper rejects each write and
   preserves target bytes or links; the agent reports the precise state and
   seeks a fresh preview where a legitimate change can proceed. No title
   search or overwrite repairs an invalid map.

4. **Moved established source.** Start with an established strategy binding
   whose native read fails and a plausible nearby note title. Before the user
   explicitly confirms both the authoritative source identity and a new
   locator, the agent keeps the saved binding and reports its read failure.
   After exact confirmation and preview approval, only the strategy role may
   change. A different role in the same map remains byte-equivalent as JSON.

5. **Saved owner, failed read.** Approve a binding pointing to the `h5d0`
   native failure fixture. The map write and readback succeed; the native read
   fails. Expected: setup is incomplete for strategy, the approved binding
   remains saved, and the next relevant session retries its native read
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

## Grade

- [ ] The interview elicits decision, owner, modes, bounded condition, and
      absence/conflict handling from the user; available connections and
      plausible titles do not become authority on their own.
- [ ] Each write follows a user-visible exact preview and matching user
      approval. A `write` payload or snapshot is not treated as permission.
- [ ] The helper rejects stale, symlinked, malformed, unreadable, locked, or
      invalid targets; a successful write changes one role, uses user-only
      permissions, and survives a fresh read.
- [ ] Native read outcome is reported separately from map save and readback.
      Failed access retains the owner; deferred ownership remains a gap.
- [ ] Claims are limited to the observed synthetic fixture and helper trace.
      This case does not establish live connector access or Codex/Claude parity.
