---
title: Gate on host-readable facts, not config grants
category: design-patterns
module: skills/repo-gardener
problem_type: design_pattern
date: 2026-09-02
last_updated: 2026-09-02
tags: [repo-gardener, policy, permissions, simplicity]
---

# Gate on host-readable facts, not config grants

## Problem

A durable policy file grew optional keys that restated facts the host could
already read: `evidence_sources` mirrored provider credentials the session
held, and `shared_ledger_paths` mirrored a git `merge=union` attribute. Each
key was framed as a grant. A live unattended run then reported its runtime
lane `unavailable` because the file lacked the key, while the host was
authenticated to the provider the whole time. The file had become a second
permission system that could only be wrong.

## Guidance

Before adding a key to a policy file, ask what the key adds beyond the fact
the host can already read. If the answer is "a way to say no when the host
says yes" or "a place to restate the fact", do not add it. Read the fact at
the point of use (`git check-attr --source=<base OID> merge -- <path>`, the
host's authenticated read) and define the statuses that read can produce,
including the missing and ambiguous cases. Keep grants only for authority the
host does not hold on its own, such as owner approval to execute repository
commands.

Test for it by grepping the contract for "configured" next to a noun the host
already knows, and by asking whether a missing key would ever be reported as
unavailability.

## Related

- [Separate scout and measurement stages from authoring capacity](../architecture-patterns/separate-scout-measurement-stages-from-authoring-capacity.md)
