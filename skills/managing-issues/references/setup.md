# Configure the canonical tracker

Read this reference before the first tracker mutation when the repository has
no valid `.agents/managing-issues.json`. A missing or invalid config does not
block reading or drafting issues. Preserve the original request while setup
resolves the canonical provider, target, and metadata mappings.

Load [github.md](github.md) or [linear.md](linear.md) for each provider used,
before provider discovery or building any metadata effect. Their
authentication, identity-check, capability, and structured-data rules apply to
setup too.

Discover available authenticated GitHub and Linear choices only when the
request does not already select a provider and target, then let the operator
choose the canonical provider and exact repository or workspace/team target.
Repository setup writes one durable file, `.agents/managing-issues.json`,
recording the canonical provider, exact target, and metadata mappings.

Load the selected provider's starter config from
[GitHub starter](../assets/config-template-github.json) or
[Linear starter](../assets/config-template-linear.json).
Discover that target's current priority, estimate, label, readiness, and score
choices, its assignable members and projects, and whether the transport can
create missing metadata.

Present every recommended key and provider value from the selected starter
template beside exact discovered alternatives; list each one rather than
summarizing a family. Linear recommends an exclusive readiness group; GitHub
recommends prefixed flat labels because Linear groups enforce one child and
GitHub labels have no label groups. The four scores map to Number issue fields
on GitHub and to single-select label groups on Linear, as each provider
reference describes. For each family, let the operator accept the
recommendations, map selected existing values, or define custom values; never
treat existing metadata as the preferred answer. Linear priority is the one
exception: Linear fixes its priority names, so `urgent`, `high`, `medium`, and
`low` each map to the Linear priority of the same name and the operator has
nothing to choose there.

The operator may leave general-label mappings empty. Every other family is
fixed: priority maps `urgent`, `high`, `medium`, and `low`; estimate maps `1`,
`2`, `3`, `5`, and `8`; readiness maps `needs-discovery`, `needs-planning`, and
`ready`; and scores map `impact`, `confidence`, `verification_effort`, and
`undo_cost`. Apart from Linear priority, the operator chooses each one's
provider value. These are available choices, never defaults applied to an
issue.

The starter templates also carry two optional settings. `assignee.default`
names one exact identity from the discovered members (a GitHub login or a
Linear user) and is the only configured default applied to new issues; see
[prioritization.md](prioritization.md) for the full assignee fallback order.
A team that wants every new issue to have an owner, including issues from
scheduled runs, sets `assignee.default` to the person who triages new work.
`project.required` set to `true` blocks creating an issue without a project;
without it, a project may stay empty with a stated reason. The operator may
keep, change, or remove either setting.

Setup uses three separate direct approvals:

1. **Provider metadata.** If any chosen metadata value does not exist, preview
   its exact creation effects and obtain direct approval. Apply and read back
   that batch before rendering the config.
2. **Repository config.** Preview the exact `.agents/managing-issues.json`
   file (including schema-required fields and chosen optional settings) for
   separate approval. An incompatible config follows this same replacement
   path. Before writing, verify that the displayed repository-relative path
   and each existing path component stay inside the repository and are not
   symlinks. Write only that destination and validate it; the validator owns
   schema-version guidance, so do not copy it into prose. Saving the setup
   file approves no tracker effect.
3. **Resumed tracker batch.** Resume the original request with a fresh
   canonical read, complete preview, and its own direct approval question.
