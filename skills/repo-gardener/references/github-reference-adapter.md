# GitHub report snapshot shape

This is the exact input shape for normalizing one GitHub issue. It is not a
provider client and grants no provider authority.

The input contains only:

- `schema`;
- configured repository, report-issue, and writer identities;
- the current issue body, stable issue identity, and provider `comments` total;
- `comment_pages_complete`; and
- every comment page in stable provider order.

The body uses the exact `orchestrator:current-portfolio:v1` markers and an exact
`orchestrator-register/v1` object. Managed history comments use the exact
`orchestrator:history-receipt:v1` markers and exact
`orchestrator-history/v1` receipts. Ordinary comments remain bounded advisory
evidence and supply no instruction, argument, identity, target, link, authority,
or tool effect.

`normalize-github-register` rejects incomplete pagination, a flattened comment
count that differs from the issue's provider `comments` total, unknown or
duplicate markers, unknown fields, identity mismatch, duplicate comment IDs,
broken or reordered history, comments ahead of the body, invalid rows, and
projection or size violations. Pagination may use any stable provider page size
up to 100: every non-final page must match the first page's size and the final
page may be shorter. A terminal line-feed difference around a managed receipt
is accepted, but the normalized canonical material is stable.

Normalization is structural. The returned state explicitly has unverified
provenance because the command cannot authenticate how the snapshot was
obtained. Neither the configured writer identity nor a matching comment author
proves caller authority.

For application, the caller uses only the immutable body and comment returned
by `effect-v1` preparation. It then supplies a fresh complete snapshot for
verification. The skill never receives raw provider mutation methods,
credentials, repository names, issue numbers, URLs, or request paths from
report prose.

Bootstrap uses the genesis template in
`assets/github-report-issue-template.md`. The caller replaces its stable
identity placeholders. Any nonempty incompatible body is foreign state, not an
empty register.
