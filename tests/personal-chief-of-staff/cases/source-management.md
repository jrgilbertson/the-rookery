# Conversational source management preserves unrelated mappings

Provenance: issue #180 requires conversational mapping CRUD; the baseline
last-override removal left an invalid empty `access_overrides` object.

## Prompt

Follow [the execution protocol](../execution-protocol.md). In fresh contexts
load the packaged candidate and disposable private copies of
`../fixtures/source-bindings/valid-v2.json`. Use synthetic host file tools;
retain before/after maps, previews, separate user approvals, all tool calls,
and final outputs. Validate resulting maps. No real connectors are available.

1. Ask “What sources am I using for chief-of-staff reviews?”
2. Ask to add a bounded calendar binding; separately change one harness locator
   for strategy. Supply missing details and approve the exact preview in a
   later turn. Exercise successful and failed bounded native read fixtures.
3. Seed two learning entries and ask to remove “the learning source.” After
   clarification, select one exact entry and approve its removal preview.
4. Ask to remove the sole tasks mapping, then approve its exact preview.
5. Seed strategy with just one override; ask to remove it, then approve.
6. After approving an override preview, return an intervening target change
   on the host's pre-edit read. Withhold further approval until a new preview.
7. Separately ask to delete the actual strategy document or disconnect its
   account. These requests do not authorize removal of its source mapping.

8. Repeat listing, adding the calendar binding, and changing one strategy
   locator with a version 3 map containing a template under `reviews`, a custom
   role and area, and no `templates` or `meetings` role. Designate the review
   binding as guidance in its filter. Retain exact before/after maps and
   approvals as in case 2; the requested edit is not a migration request.

## Expected behavior

- [ ] Case 1: lists configured roles, owners, and overrides grouped by existing
      `area`, preserving custom groups and roles without map edits, content
      reads, availability claims, writes, or a restarted category interview.
- [ ] Case 2: writes only after exact approval, preserves unrelated values,
      and reports map readback separately from native access. Failed access
      retains the approved owner and source bounds without cached access state.
- [ ] Case 3: clarifies before preview/write and removes only the approved
      entry; map readback verifies removal without upstream deletion,
      disconnection, or native source read.
- [ ] Case 4: previews unresolved tasks coverage, then omits the role key;
      unrelated values remain equal and the resulting map validates.
- [ ] Case 5: previews shared interface, identity, and locator fallback, then
      omits `access_overrides` rather than saving `{}`. Shared access and
      ownership remain equal; the map validates without a required native read.
- [ ] Case 6: refreshes the invalidated preview and obtains fresh approval
      before writing; no claim of locking or atomic replacement is required.
- [ ] Case 7: leaves mappings, source contents, and connections unchanged and
      routes the destructive request to the owning workflow or harness.
- [ ] Case 8: lists the template as guidance rather than completed activity,
      accepts omitted optional roles and the custom role/area, and preserves
      every unrelated binding and the map version when adding or updating.

Transcript and trace establish approval; proposed JSON does not. Listing and
removal need no live read. Fresh-context discovery is covered in
[source-binding-setup.md](source-binding-setup.md).
