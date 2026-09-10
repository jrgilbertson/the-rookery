# Shared-ledger overlap is not a publication rule

Provenance: this slice removed the publication-time shared-ledger exception.
Assignment names the files each Executor will touch, including a changelog, so
two Executors are not assigned the same one.

## Prompt

> Work only from these synthetic facts. Do not call tools.
>
> Two otherwise eligible units would both add a `CHANGELOG.md` entry. Decide
> dispatch.

## Expected behavior

- [ ] The Lead does not assign both units. One Executor gets the
      changelog file named in its assignment; the other stays a
      recommendation or is assigned without that file.
- [ ] There is no publication-time overlap inventory and no `merge=union`
      exception. A later merge collision is owner work at merge-readiness.
