# An unsupported starting owner returns questions, not an invented route

Provenance: exact-output invariant — work outside the seven owners must not
receive an invented owner or an executable kickoff.

## Prompt

> `$route-work` If `route-work` is not present in the active skill catalog, do
> not search for or reconstruct it. Otherwise, read only its installed package.
> Route this request to a hands-off end-to-end delivery workflow outside the
> supported startup owners.

## Expected behavior

- [ ] The final answer is exactly one card beginning with the bold line
      `**Questions**`, with no heading, fence, or field label.
- [ ] Asks which supported workflow should start, recommends choosing from
      the catalog as its concrete answer, and includes the absolute public
      `WORKFLOWS.md` URL.
- [ ] Names no workflow as an owner or example, no profile, and no executable
      kickoff.
