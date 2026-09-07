# A routing question uses the exact Questions card

Provenance: exact-output invariant — a receiver must distinguish a routing
question from a ready route without interpreting prose variants.

## Prompt

> `$route-work` If `route-work` is not present in the active skill catalog, do
> not search for or reconstruct it. Otherwise, read only its installed package.
> Route this issue-shaped request. It could mean canonical tracker cleanup or
> implementation of an accepted change; no discriminator is supplied.

## Expected behavior

- [ ] The final answer is exactly one card beginning with the bold line
      `**Questions**`.
- [ ] Asks one numbered question that distinguishes tracker truth from
      implementation, with a separate `Recommended:` line giving one concrete answer,
      and ends after it with no recommended owner. Never says "no default".
- [ ] Contains no kickoff, second question, heading, or fence. A later answer
      may receive another Questions card.
