# Report-only agent assessment

Use this form when a supervising agent needs a readiness assessment for the
current pull request, not an owner decision. It may be useful after a Worker
response; a supervisor may instead assess the freshly read facts directly.

Run the ordinary read-only assessment through step 6. Return one of `merge`,
`debug`, or `do not merge`, the full current head OID, and ordinary
human-readable findings that explain the recommendation. Keep the report
plain prose rather than a receipt or machine protocol.

Stop before step 7. Do not show a decision menu, prepare a merge action, or
invoke a forge write. This report never changes the pull request; its caller
decides whether a named finding warrants a focused Worker instruction.
