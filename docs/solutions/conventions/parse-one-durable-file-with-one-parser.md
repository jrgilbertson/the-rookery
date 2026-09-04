---
title: "Parse one durable file with one parser"
date: 2026-08-24
category: conventions
module: "skills/repo-gardener"
problem_type: convention
component: tooling
severity: medium
applies_when:
  - "A skill keeps one durable config file and more than one helper reads it"
  - "A review thread keeps finding indent, flow-style, or scalar-spelling splits between helpers"
  - "A second helper is about to regex a YAML or JSON file the validator already parses"
tags: [skills, yaml, pyyaml, fail-closed, durable-file, parser-unification]
---

# Parse one durable file with one parser

## Context

Repo Gardener's live authority is one durable yaml file in the target
repository, not a file this catalog keeps.
`config_check.py` used to parse it with a hand-rolled loader. `lanes` in
`release_a_contract.py` inventoried the same `lanes:` section with a
two-space regex. Review on #78 (unmerged as of this writing) kept finding
cases one grammar accepted and the other rejected: extra indent, flow
`{mutation: true}`, trailing commas, `Null`/`NULL`. Fixing the regex did not
end the split.

## Guidance

Parse the durable file once. Validate with the field schema. Have every other
helper read that mapping.

Gardener now does that with PyYAML `SafeLoader` plus an allowlist: boolean
`true`/`false` only, decimal integers, fail-closed tags, aliases, merge keys,
nulls, and duplicate keys. The second reader is gone: the `lanes`
subcommand was removed and the config fixture pins the flow-style,
deeper-indent, and duplicate-key grammar cases against the validator
itself. SafeLoader is not the
schema; `yes`, `0x10`, and overwrite-on-duplicate still have to be refused
in code.

Developer-installed skills may take a library when the alternative is a
second grammar. Do not add PyYAML to helpers that still ship JSON.

## Why This Matters

Two parsers of one file create a review treadmill. Each indent or flow-style
fix is real, and none of them close the gap. Callers then see different
answers from the validator and the inventory for the same bytes.

## When to Apply

- A second helper is about to read a file the validator already parses.
- Review comments keep naming grammar splits rather than field-schema bugs.
- The install audience is developers, so a baseline library is acceptable.

## Examples

Before: `config_check.py` accepted any consistent indent; `lanes` required
exactly two spaces on lane keys. A valid four-space `lanes:` mapping failed
inventory.

After: both paths load through `parse_yaml_mapping`
(`skills/repo-gardener/scripts/config_check.py`). Fixtures cover four-space
indent, flow mappings, `yes` as a non-boolean, and duplicate keys.

## Related

- [Ship bundled skill helpers with an executable falsifiability contract](../workflow-issues/falsifiability-contracts-need-executable-tests.md)
- [policy-and-entry-modes.md](../../../skills/repo-gardener/references/policy-and-entry-modes.md)
