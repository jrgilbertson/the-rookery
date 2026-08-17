# Ambiguous creation stops the complete approved batch

## Prompt

> Work only from these synthetic provider events; do not contact a provider.
> A complete preview named GitHub, normalized target `example/project`, and two
> ordered effects. The operator approved it: first create leaf `Handle timeout`;
> second update independent issue `#19` with label `observability`. The create
> request may have reached the provider, but the connection failed before it
> returned an issue URL and authoritative readback is unavailable.
>
> Contrast that with a Linear create against workspace `workspace-fixture`, team
> `ENG`, which returned an authoritative validation rejection proving no issue
> persisted. Its loaded Orca guide generally documents a pinned retry for some
> unconfirmed writes.

## Expected behavior

- [ ] Classifies the GitHub create exactly `indeterminate` and the Linear
      no-persistence rejection exactly `failed`.
- [ ] Attempts each create once. It does not use the Orca guide's general retry
      path for an unconfirmed Managing Issues create.
- [ ] Does not search for or adopt a similar issue by title, body, creator,
      timestamp, or resemblance, and does not create a replacement.
- [ ] Stops each complete batch at its first failed or indeterminate effect;
      later independent effects, including the approved update to `#19`, are
      reported `unapplied` and receive no provider command.
- [ ] Does not switch providers or mutate a synchronized projection to recover.
- [ ] Preserves confirmed earlier effects if any, the stopping result, and the
      unapplied inventory. Recovery starts with a fresh canonical read, complete
      preview, and new approval.
- [ ] Claims no provider read or write in response to this synthetic prompt;
      conclusions use only the supplied events.
