# Eval: release notes for version 2.4.0

Synthetic eval for the `drafting-release-notes` skill. Each run received this
prompt:

> Draft release notes for version 2.4.0 from these merged changes: fix the CSV
> export timeout on large reports (ticket OPS-418); add dark mode to the
> dashboard (ticket UI-77); remove the v1 REST API (ticket API-9).

Assertions:

1. Groups the entries under Added, Fixed, and Removed headings.
2. Marks the v1 REST API removal as a breaking change.
3. Contains no internal ticket identifiers.
