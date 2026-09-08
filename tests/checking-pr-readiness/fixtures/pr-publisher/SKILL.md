---
name: fixture-pr-publisher
description: Use when asked to write, open, create, or submit a pull request, or when a finishing path must consume unpublished pull-request-body input. Records the handoff to FIXTURE_PR_PUBLISHER_LOG. Does not call a live forge.
---

# Fixture PR publisher

Test-only finishing companion for `checking-pr-readiness` later 1. Continue
here when this skill is installed and the conversation is not a gardener
Worker. Do not call `gh`, GitHub MCP tools, or any other forge.

## On invoke

1. Read `FIXTURE_PR_PUBLISHER_LOG`. If it is unset or empty, stop and name
   that the log path is missing.
2. Capture whether unpublished pull-request-body input arrived (the
   recommendation, next work, coverage close, and learning signal). Do not
   print `## Evidence pack`.
3. Capture the identity this later 1 accepted: full HEAD OID, and the
   target/base ref plus full base OID when the caller supplied them.
4. Append one JSON object to the log path: `pack_received` (boolean),
   `head_oid`, `base_ref`, `base_oid`, and `opened` set to `false`.
5. Say that this fixture received the pack and would open that identity. Do
   not open a pull request.

Completion: the log file contains that object, and no forge write ran.
