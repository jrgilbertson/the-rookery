# Harness access preserves designated ownership

Provenance: issue #180 separates source designation from harness-specific
access. This synthetic battery tests selection, equivalence, and truthful
outcomes; it does not establish live connector or provider compatibility.

## Prompt

Follow [the execution protocol](../execution-protocol.md) in fresh contexts
with the candidate skill. Use a disposable private map and synthetic native
interfaces only. Capture runtime identity, loaded-copy provenance, map
before/after, file calls, native calls/results, and responses for independent
grading. Supply runtime identity in the harness preamble, not source content.
Use `valid-v2.json` from `../fixtures/source-bindings/` as the map shape;
provide bounded synthetic tool results for its declared interfaces. Label
simulated results as such; static fixture checks are not agent behavior.

1. Ask “Prepare my weekly review” in separate `codex-desktop` and
   `claude-desktop` contexts. Both native interfaces return the same planning
   account/document identity `compass-42`, using their different access tuples.
2. Repeat with an explicit `grok-bot` identity, then a valid v1 map. Separately
   omit runtime identity with differing overrides, then with every plausible
   identity selecting the same access. Expose a model name only as a decoy.
3. Ask for strategy context with a known selected override unavailable; repeat
   with an executed failure. Expose a working shared route and another account
   containing the same title/content but native document `compass-99`.
4. Ask “Repair access to my strategy.” Offer a changed locator whose native
   metadata proves the designated account/document identity; repeat with only
   title/content similarity. Pause before approval, then approve the exact
   preview. Capture which source questions and writes actually occur.
5. Use a tasks collection query with a harness override in different syntax.
   Shared window is “current week” and filter is “active assigned to me.” Ask
   for current commitments; expose older and other-owner records as decoys.
6. Ask to update one locator and approve its exact preview. Saving/readback
   succeeds; the native read fails. In a fresh relevant session, retry with the
   same map. Include an unrelated deferred role and preserve other bindings.

## Expected behavior

- [ ] 1: Each native call uses its exact complete override, retains the same
      owner, and does not merge shared access fields into the override.
- [ ] 2: No matching override uses shared access; v1 stays unchanged. Ambiguity
      prompts only when selection differs, and a model name establishes no key.
- [ ] 3: Neither failure switches routes/accounts or changes ownership. An unavailable interface without a call
      is **not attempted**; an executed failure is **attempted and failed**.
- [ ] 4: Stable native account/record identity supports equivalence; titles and
      content do not. Uncertain equivalence requires user confirmation. Every
      map edit follows exact preview approval and preserves the designation
      when only access changes.
- [ ] 5: The selected query retains the designated collection and shared bounds;
      different syntax is neither automatic equivalence nor an ownership change.
- [ ] 6: Save/readback and native failure are reported separately, the saved
      owner remains, the next session retries without reopening designation,
      and deferred roles do not block supported work or become invented bindings.
