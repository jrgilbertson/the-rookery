# Standalone setup routes to source ownership and finishes with a native read

Provenance: issue #156's writing-for-agents revision adds explicit setup and
repair discovery, selective reference loading, and a completion rule for source
setup. The frozen prior description did not activate three setup/repair metadata
queries, while its native setup run read all three full mode references. This
case tests that routing and loading gap. A later unscripted tasks-preview
variant supplies setup-completion evidence, not a matched strategy case.

## Prompt

> Use a fresh synthetic home with no source map. “Help me set up the sources
> my chief-of-staff reviews should use. I want Wind-down, Weekly, and Quarterly
> to draw from the right current owners.” The harness prompt supplies synthetic
> task guidance and review-template capacity facts, with no populated capacity
> owner and no native template token.
> Do not name skill references in the user message. In a later turn, designate
> a synthetic strategy owner via `pcos-source` and ask for an exact preview.
> Then approve that specific preview and ask the agent to finish setup. Keep
> the turns in the same disposable home, with a fresh native fixture root for
> each turn.
> Independent failure branch: approve one exact strategy binding in a fresh
> home, let host file save/readback succeed, then make its native read fail.

## Expected behavior

- [ ] The unforced setup request activates the installed skill and stays in
      setup. It inspects exposed integrations/account metadata, uses relevant
      task/template guidance, and walks the documented categories with deferral;
      it loads shared setup references without unrelated full-mode reads.
      Inventory and template facts do not establish ownership. For each active
      role it asks only for missing decision, owner, modes, condition, bounds,
      and gap effects; deferred roles stay unresolved without guessed reads.
- [ ] A mapping changes only after its exact preview is approved, and the
      response distinguishes saved-map readback from the bounded native read.
      Proposals never count as completion. Saved/read roles and unresolved
      roles are reported separately without starting a review or mutating a
      source. In the independent failed-read branch, the saved owner remains,
      the ending is Partial, and the next read needs no repeated designation.
