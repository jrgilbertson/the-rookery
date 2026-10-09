---
title: "Isolate native state for ephemeral Codex evals"
date: 2026-10-04
last_updated: 2026-10-09
category: best-practices
module: "creating-portable-skills skill verification"
problem_type: best_practice
component: testing_framework
severity: high
applies_when:
  - "Capturing a native Codex eval while retaining the operator's subscription authentication"
  - "Using ephemeral threads or a private trace directory as evidence of isolation"
tags: [codex, evals, sqlite, isolation, native-state, ephemeral, capture]
---

# Isolate native state for ephemeral Codex evals

## Context

The issue [#192](https://github.com/jrgilbertson/the-rookery/issues/192)
capture investigation found that an ephemeral Codex thread could still produce
SQLite log rows. Moving the trace bundle and disabling rollout history did not
isolate the harness's state and log databases. This behavior was verified with
native Codex 0.160.0; recheck it when changing versions.

The relevant native setting is `sqlite_home`. In the pinned source,
[configuration resolution](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/core/src/config/mod.rs#L4088-L4093)
falls back to `CODEX_SQLITE_HOME` and then the Codex home, while
[SQLite path construction](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/state/src/sqlite.rs#L148-L159)
uses that location for both state and logs. A separate fresh database can also
trigger ingestion of existing rollout metadata: the
[startup backfill gate](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/rollout/src/state_db.rs#L130-L160)
returns early when the stored status is complete, otherwise it attempts backfill.

## Guidance

Treat native storage as a separate boundary from model tool permissions and
trace capture. For a run that keeps existing subscription authentication:

1. Pass a private, absolute `sqlite_home` through the native launch configuration.
   Record the exact argv and effective configuration. Keep the store outside
   the model's readable workspace and the public repository.
2. Initialize that store with the same pinned native binary, using an isolated,
   empty home and no authentication or model turn. Let Codex create its own
   migrations and complete its empty-history backfill. Do not forge migration
   rows or set the completion flag manually.
3. Prove the seed's behavior using synthetic history. The seeded store must
   skip the marker; a fresh, unseeded control must ingest the same marker.
   A missing marker without a positive control does not prove isolation.
4. Before process startup and again before the model turn, require the expected
   successful migration versions, complete backfill status, and no persisted
   thread rows. Check every database and sidecar entry with `lstat`; reject
   symlinks, shared hardlinks, directories, and unexpected names. Version-bound
   allowlists should fail closed when the native schema changes.
5. After shutdown and log flush, count rows for the actual captured thread in
   the private and normal log stores. Require private persistence where expected
   and no matching normal-store rows. Avoid reading unrelated session contents.

When reusing a store between processes, account for native temporary files.
Codex 0.160.0 [opens `.sqlite-maintenance.lock` for advisory ownership](https://github.com/openai/codex/blob/rust-v0.160.0/codex-rs/state/src/runtime/reclamation.rs#L115-L130).
A strict allowlist can reject this file after a completed turn. Investigate it
after the producing process exits. For a verified empty, regular, single-link
marker, acquire an exclusive nonblocking file lock before moving it to a private
archive outside the store. Preserve the databases and the frozen launch plan;
never bypass an unknown entry or move a lock held by a live process.

These checks establish a bounded storage claim. They do not establish that the
native CLI never writes anything under the operator's home; helper staging and
other native runtime behavior need their own evidence. Record instrumentation
that can alter inference history separately from model and catalog defaults.

**Current suite.** The Promptfoo suite's `prepare` step in
`tests/creating-portable-skills/promptfoo_suite.py` gives each Codex run a
fresh private `CODEX_HOME` with linked authentication, plus a private
`sqlite_home` and `log_dir`. It does not run the seed-and-control or row-count
checks above, so it claims private paths rather than proven storage
isolation. Apply this procedure when a run must reuse an existing Codex home,
or during the decision record's dependency-upgrade recheck.

## Why This Matters

An ephemeral flag describes a conversation's persistence behavior, not every
store opened by its host. Likewise, a fresh SQLite directory is not necessarily
empty after native initialization. Keeping these boundaries explicit prevents
both accidental copying of existing session metadata and false isolation claims.

## When to Apply

Use this pattern when subscription-authenticated native capture must keep
generated evidence private. Reverify the source, seed control, effective
configuration, and actual persistence whenever the binary or storage schema
changes. Storage success still does not establish tool-call provenance or
criterion success; those remain separate capture and grading checks.

## Examples

The bounded native verification initialized an empty private store, demonstrated
seeded-skip and fresh-control ingestion with synthetic history, and then ran one
real ephemeral model turn. Its thread's log rows appeared in the private store
and had no matches in the normal store. Independent disposable-copy attacks also
confirmed that linked database files and previously ingested thread rows were
rejected before the model turn.

## Related

- [Put the test seam in the environment](../conventions/keep-the-test-seam-out-of-the-shipped-skill.md)
  describes the launcher as a separate isolation boundary.
- [Blind cross-model grading through native schema flags](blind-cross-model-grading-through-native-schema-flags.md)
  covers independent configuration and output-schema controls.
- [Cross-harness dogfood testing](cross-harness-dogfood-testing.md) separates
  installed identity, native loading, and behavior evidence.
- [Use Promptfoo for portable skill evaluations](../../decisions/promptfoo-for-portable-skill-evaluations.md)
  pins the native providers and requires a private-storage recheck on
  dependency upgrades.
