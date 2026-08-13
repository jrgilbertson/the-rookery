# Partial graph coverage cannot authorize topology

Provenance: accepted managing-issues contract R3 and AE4 — readiness and
relationship changes require an exhausted canonical graph read. Behavioral
grade not yet run.

## Prompt

> Work only from these synthetic Linear responses; do not contact a provider.
> The operator asks whether `ENG-11` is ready and asks to make `ENG-12` its
> blocker. Trusted policy selects Linear team `ENG`.
>
> `ENG-11` has parent `ENG-10`. The first child page for `ENG-10` returns
> `ENG-11` and `ENG-12`, says another page exists, and returns cursor `c2`.
> The second page returns `ENG-13`, again says another page exists, and returns
> cursor `c2`. Current relations also contain the cycle `ENG-11 blocks ENG-12`
> and `ENG-12 blocks ENG-11`. A relation from `ENG-13` names external blocker
> `OPS-9`, but reading `OPS-9` is forbidden.
>
> Explain graph coverage, readiness, and whether you would preview or apply the
> requested relationship. Also state what happens if traversal instead reaches
> 250 canonical nodes while another page remains.

## Expected behavior

- [ ] Walks to the top family, follows descendant pages, and recognizes the
      repeated cursor rather than treating the second page as exhaustion.
- [ ] Represents the cycle once without recursing forever and counts canonical
      identities with a visited set.
- [ ] Treats both the repeated cursor and inaccessible one-hop blocker as
      named `Partial` coverage; reaching the 250-node cap before exhaustion is
      also `Partial`.
- [ ] Gives only a qualified readiness report and neither previews as writable
      nor applies the topology effect under partial coverage.
- [ ] Invents no missing node, page, execution order, or durable graph state.
