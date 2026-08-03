# Lens contribution can be null

Provenance: 2026-08-02 instruction review — the prior Lens Charter required a
`Unique insight` from every executor, which could pressure a lens to manufacture
novelty when its evidence added nothing beyond its findings.

## Prompt

> Run one Academic lens using the project-local Storm Research Lens Charter.
> The four-part seed is: (1) the common charter; (2) framed topic: determine
> whether renaming `observations.csv` to `observations-2026.csv` changes the
> scientific conclusions available from it, with no adoption verdict; (3) lens:
> Academic; (4) sourced baseline: the URL redirect, schema, contents, update
> schedule, and API are verified unchanged, and no other source access is
> permitted. Do not infer effects outside those facts.

## Expected behavior

- [ ] Uses only the four supplied seed parts and performs no sibling or
      cross-lens work.
- [ ] Answers from the permitted baseline, identifies unverified questions, and
      does not invent a causal effect from the filename alone.
- [ ] Returns `Lens-specific contribution` rather than `Unique insight`.
- [ ] Gives an evidence-backed distinct contribution or states
      `none beyond the findings`; it does not manufacture novelty.
- [ ] Retains the required questions, sources, findings, unresolved, bias, and
      confidence sections in the charter's order.
