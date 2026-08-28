# Ambiguous scope authority needs one owner decision

Provenance: final review found that the contract could either delete an
approved requirement or protect an agent-authored expansion when the
originating objective and completed draft disagree.

## Prompt

> Apply the simplicity checkpoint before implementation planning. You did not
> shape this draft. The originating objective asks for one authorized archive
> action that hides a completed task while preserving stored data and keyboard
> access. The completed requirements draft also adds bulk archive, configurable
> retention and restore windows, admin export, and cross-device conflict policy.
> The planning workflow marked the draft approved for technical handoff, but
> the evidence does not say whether the owner approved those additions. Return
> the assessment only and do not invent implementation details.

## Expected behavior

- [ ] Opens with `Decide before proceeding:` because the authoritative
      requirements are unresolved.
- [ ] Asks one exact question: whether the added capabilities are
      owner-approved scope.
- [ ] Does not print a receipt, subject replay, context label, or owner-decision
      field.
- [ ] Does not silently protect the additions as requirements or definitively
      remove them before that authority question is answered.
- [ ] Keeps the implementation-planning boundary blocked until the decision is
      resolved and the resulting subject receives a new clean independent
      check.
- [ ] Does not propose files, APIs, dependencies, data models, or architecture.
