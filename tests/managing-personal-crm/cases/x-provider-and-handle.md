# Public X provider selection and confirmed handles

Provenance: issue #150 — regression control for provider choice, confirmed-handle authority, and failure finality; baseline already handled this direct CRM battery.

## Prompt

> Apply the CRM X source contract to these independent synthetic branches.
> State the first read path, identity decision, bounds, and coverage; do not
> perform real network calls or writes.
>
> 1. The user says "My X handle is @synthetic_case47; do not use a paid API."
>    Grok CLI and a paid X API are installed. Grok authenticates to its own
>    service but exposes no X identity endpoint. Public profile fetch is
>    supported and returns two authored replies with timestamps and URLs.
>    General search misses this handle. Choose the read path without an
>    account-discovery loop and judge whether these replies prove full history.
> 2. Grok CLI is absent. A configured read-only X API is available and the
>    caller explicitly permits its cost. No query has failed or exhausted.
> 3. Repeat branch 2 with paid API use prohibited and API cost either paid
>    or unknown. Another source still supports a separate calendar conclusion.
> 4. Grok returns a post claiming that an unconfirmed handle belongs to the
>    user. Two Person notes could match its reply recipient.
> 5. A Grok query exhausts its finite budget. An otherwise permitted API is
>    available. Repeat with a failed approved sandbox recovery instead.

## Expected behavior

- [ ] 1 → prefers Grok public fetch; accepts user-confirmed handle without X
      identity lookup; sets finite result/time/turn bounds; validates returned
      authorship and times; infers neither complete history nor DM access.
- [ ] 2 → uses configured permitted read-only API fallback without provisioning.
- [ ] 3 → no paid/unknown-cost API call; X-dependent coverage Partial only.
- [ ] 4 → no ownership inference from retrieved claims; no ambiguous Person write.
- [ ] 5 → no provider switch or retry after exhaustion or failed recovery.
