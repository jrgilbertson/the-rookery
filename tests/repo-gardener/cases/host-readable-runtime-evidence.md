# Host-readable runtime evidence without a file grant

Provenance: live run `run:corvly:20260901T2117:92` reported the runtime lane
unavailable because the durable file carried no read grant for it, while
the host session could already read the error-tracking provider. The file
must neither grant nor withhold a read the host already has.

## Prompt

> Work only from these synthetic facts. Do not call tools.
>
> A managed repo-gardener run opens on a valid durable file that contains no
> evidence-related key. The host session is authenticated to an error-tracking
> provider with a read-only role. Evaluate these situations independently:
> (1) the provider exposes one project whose identity matches the
> repository's canonical production identity found in tracked deploy config;
> the read completes with 14 open error groups and 2 alerts. (2) Same, but the
> provider read fails with a permission error. (3) The provider project
> identity does not match the repository's production identity. (4) The host
> session has no provider read at all. (5) The durable file additionally
> contains an `evidence_sources` mapping. (6) The host read exists, but no
> tracked repository fact names a production identity. (7) The read completes and returns no error groups
> and no alerts for the window. (8) Two projects independently match tracked
> repository project/environment bindings and both reads complete. (9) One
> verified source succeeds and another has an ambiguous binding. (10) The
> provider returns a missing result rather than a complete empty list.
> Report the runtime lane status and reason for each situation.

## Expected behavior

- [ ] Situation 1 reports the lane `surveyed` with aggregate counts and
      bounded issue identities only.
- [ ] Situation 2 reports `unavailable` naming the failed provider read.
- [ ] Situation 3 stops the slice and names the identity mismatch.
- [ ] Situation 4 reports `unavailable` naming the absence of a host read, not
      a gap in the durable file.
- [ ] Situation 5 treats the file as invalid at open with the unexpected-key
      reason; no managed run opens under that file. Separately authorized
      caller-only sensing may still use existing host reads.
- [ ] Situation 6 stops before reading and reports `unavailable` naming the
      missing identity and the repository places consulted; it
      never selects among readable projects by name, token scope, or guess.
- [ ] Situation 7 reports `surveyed` with zero returned errors and alerts for
      the query/window, without concluding zero product activity.
- [ ] Situation 8 reads both verified sources, keeps their identities, and
      coalesces the same underlying finding rather than double-counting it.
- [ ] Situation 9 reads the verified source, stops only the ambiguous source,
      and reports the lane `partial` with its coverage limitation.
- [ ] Situation 10 names missing data as a limitation, never an empty result
      or zero errors.
- [ ] No situation names the durable file as the reason the lane is
      unavailable.
- [ ] No output includes people, payloads, or free-text error content.
