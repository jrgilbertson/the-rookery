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
> home, let helper save/readback succeed, then make its native read fail.

## Expected behavior

- [ ] Native routing activates the just-installed skill from the request for
      setup, without forcing its path in the user message.
- [ ] Setup loads its shared source behavior and source binding guidance,
      uses the supplied synthetic guidance/template facts, and selectively
      checks relevant mode material without loading unrelated mode instructions
      or beginning a new review's discovery reads.
- [ ] Before previewing each role being actively bound, obtain its decision,
      current owner, modes, read condition, bounds, and absence/conflict rule.
      Ask for missing information and accept answers already supplied by the
      user. Explicitly deferred roles remain named gaps; their full interview
      can wait. A template prompt or available connection does not become an
      owner on its own.
- [ ] Unowned or deferred roles remain explicit gaps. The agent does not
      invent a source, probe guessed native role tokens before designation,
      write a map, or claim setup complete from a proposal.
- [ ] A changed role follows an exact user-visible preview and matching
      approval before helper write. The saved entry is read back and its
      native bounded source read is attempted; a save alone is not access.
- [ ] Completion names each saved-and-read role separately from unresolved or
      failed roles, with no new review or unapproved source mutation. A sole
      saved role whose native read fails ends Partial, keeps its owner, and
      does not claim source access or require another ownership interview.
