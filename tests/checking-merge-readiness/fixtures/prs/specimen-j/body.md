The org permission lookup runs on every authenticated request and accounts for
most of the p95 on the gateway. It hits the same three rows for the life of a
session and almost never changes between them.

This caches the resolved permission set per (user, org) with a 10 minute TTL,
in the process cache we already run for feature flags. Cold path is unchanged;
a miss does exactly what the request did before.

- `permissions.resolve_for(user, org)` now reads through `PermissionCache`.
- The cache is the existing `TTLCache` from `gateway/cache.py`, a second
  instance with its own size cap. No new dependency, no shared eviction.

Out of scope: caching the org record itself, cross-process invalidation, and
the session-token lookup, which has a different lifetime and belongs in its
own change.
