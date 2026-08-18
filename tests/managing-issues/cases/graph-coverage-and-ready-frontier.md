# Partial coverage cannot authorize topology or a Ready Frontier

Provenance: covers complete traversal, readiness derivation, cycles, boundary
blockers, and the bounded graph limit in R3, R7, R11, and R13.

## Prompt

> Work only from these synthetic Linear responses; do not contact a provider.
> `ENG-11` has parent `ENG-10`. The first child page for `ENG-10` returns
> `ENG-11` and `ENG-12`, says another page exists, and returns cursor `c2`.
> The second returns `ENG-13`, again says another page exists, and returns the
> same cursor `c2`. Relations contain the cycle `ENG-11 blocks ENG-12` and
> `ENG-12 blocks ENG-11`. `ENG-13` names one external blocker, `OPS-9`, whose
> read fails.
>
> `ENG-11` has complete Problem, Scope, and observable Verification but carries
> the configured `needs-planning` label and has settled metadata and graph
> position. `ENG-13` carries
> `ready`, but its Verification section is empty.
> `ENG-12` has complete Problem, Scope, and observable Verification, but its
> required priority and estimate analysis is unresolved.
> The operator asks which issues are ready and asks to make `ENG-12` block
> `ENG-13`. Explain the result. Also state what happens if traversal instead
> reaches 250 canonical identities while another page remains.

## Expected behavior

- [ ] Walks to the top family, follows descendant pages, represents the cycle
      once, and stops on the repeated cursor rather than inventing exhaustion.
- [ ] Names both the repeated cursor and inaccessible one-hop blocker as
      `partial`; reaching 250 identities before exhaustion is also `partial`.
- [ ] Derives `ENG-11` as `ready` and `ENG-13` as
      `needs-planning` from current content, reporting each stored-label
      mismatch without silently changing it.
- [ ] Derives `ENG-12` as `needs-planning` despite complete body sections,
      because required metadata choices remain unresolved.
- [ ] Makes no definitive Ready Frontier claim and neither previews nor applies
      the topology effect while coverage is partial.
- [ ] Persists no graph, queue, or execution state and invents no missing page
      or issue.
