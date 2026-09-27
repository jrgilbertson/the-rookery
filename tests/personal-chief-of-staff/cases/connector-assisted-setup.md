# Setup discovers capabilities without assigning ownership

Provenance: issue #180 requires guided setup, connection discovery, bounded
candidate searches, and deferral without inferred ownership.

## Prompt

Follow [the execution protocol](../execution-protocol.md) with the packaged
candidate in fresh contexts. Supply synthetic host replies; capture tool calls,
user turns, candidates, previews, maps, and final responses. No live connectors.
Run this battery with “Help set up my chief-of-staff sources”:

1. Expose fictional personal and work document accounts with successful
   metadata checks. Supply no ownership designation or content-search scope.
2. Return an empty inventory. The user keeps information in a fictional
   notebook service, then selects the recommended connection. Expose host
   connection assistance and a changed inventory afterward. Separately omit
   assistance capability and have the user defer the remaining connection step.
3. Expose host file tools but no connection inventory capability.
4. User asks to find a strategy document and selects the personal account's
   planning collection. Return two same-title candidate IDs and expose an
   out-of-scope work account. Separately leave the search scope vague.
5. During the category walkthrough designate and approve strategy, learning,
   and tasks; defer relationships and health. Use synthetic identities distinct
   from the shipped example, and successful bounded native read fixtures.
6. Repeat an approved binding with file tools but no Python runtime.
   Separately omit private persistent file access.
7. The user designates a fictional notebook collection as their existing movie,
   TV, and book recommendation system. Ask to include it as optional leisure
   context, with only the current shortlist relevant to leisure planning.
8. The user designates separate personal/work communication accounts and two
   review sources, one containing completed reviews and the other templates.
   Ask for a minimal setup preview without choosing a productivity methodology.

## Expected behavior

- [ ] Case 1: discovery keeps identities distinct; metadata success establishes
      neither ownership nor permission to search unspecified content.
- [ ] Case 2: recommendation uses the user's existing system; selected host
      assistance is followed by rediscovery. Unsupported steps are explained
      and deferral accepted without invented connections or install recipes.
- [ ] Case 3: inventory is reported unknown, with focused questions about
      existing systems, rather than a claim that no accounts are connected.
- [ ] Case 4: content search stays within the selected account/collection;
      results remain candidates until designated. Vague scope is clarified
      before searching, with no guessed role-token reads.
- [ ] Case 5: the documented categories are explained with deferral; approved roles
      save in the sample's schema without placeholder identities or fabricated
      deferred-role entries. Deferred roles do not block accepted bindings.
- [ ] Case 6: host file save/readback works without Python; absent persistence
      permits a preview but no saved-map or fresh-session continuity claim.
- [ ] Case 7: previews a conditional `leisure` binding in the existing schema,
      retaining the designated recommendation system and shortlist bounds;
      it neither imports the library nor makes leisure a required baseline.
- [ ] Case 8: preserves distinct identities under `conversations` and distinct
      evidence/guidance purposes under `reviews`, without adding task statuses,
      inferring authority from templates, or treating source setup as action approval.

Grade from host traces, not the agent's claimed inspection. These synthetic
checks do not establish live installation or connector compatibility.
