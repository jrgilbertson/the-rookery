# Configure the canonical tracker

Read this reference before the first tracker mutation when the repository has
no valid `.agents/managing-issues.json`. A missing or invalid config does not
block reading or drafting issues. Preserve the original request while setup
resolves the canonical provider, target and metadata mappings.

Load [github.md](github.md) or [linear.md](linear.md) for each provider used,
before provider discovery or constructing any metadata effect. Their authentication,
matchback, capabilities and structured-data requirements apply to setup too.

Discover the available authenticated GitHub and Linear choices only when the request does not
already select a provider and target, then let the operator select the canonical
provider and exact repository or workspace/team target. Repository setup has
exactly one durable file, `.agents/managing-issues.json`. It records the
canonical provider, exact target, and metadata mappings.

Load the selected provider's starter config from
[GitHub starter](../assets/config-template-github.json) or
[Linear starter](../assets/config-template-linear.json).
Discover that target's current priority, estimate, label, readiness, and
score choices, its assignable members and projects, and the capability to
create any missing metadata.

Present every recommended key and provider representation from the selected
starter template beside exact discovered alternatives; list each one rather
than summarizing a family. Linear recommends an exclusive readiness group;
GitHub recommends prefixed flats, because Linear groups enforce one child and
GitHub labels have no grouping surface. The four scores map to Number issue
fields on GitHub and to single-select label groups on Linear, as each provider
reference describes. For each family, let the operator accept the
recommendations, map selected existing values, or define custom representations;
never treat existing metadata as the preferred answer. Linear priority is the
one exception: Linear fixes its priority names, so `urgent`, `high`, `medium`,
and `low` each map to the Linear priority of the same name and the operator has
nothing to choose there.
The operator may leave general-label mappings empty. Every other family is
fixed: priority maps `urgent`, `high`, `medium`, and `low`; estimate maps `1`,
`2`, `3`, `5`, and `8`; readiness maps `needs-discovery`, `needs-planning`, and
`ready`; and scores map `impact`, `confidence`, `verification_effort`, and
`undo_cost`. Apart from Linear priority, the operator chooses each one's
provider representation. These are available choices, never defaults applied
to an issue.

The starter templates also carry two optional settings. `assignee.default`
names one exact identity from the discovered members, a GitHub login or a
Linear user. It is the only configured default the skill applies to an issue.
`project.required` set to `true` means no issue may be created without a
project. The operator may keep, change, or remove either one. Without
`assignee.default`, a create assigns the person the request names, or else the
requester, and a run whose request names no one and has no human requester
leaves the assignee empty with a stated reason. A team that wants every new issue to have an owner, including
issues from scheduled runs, sets `assignee.default` to the person who triages
new work. Without `project.required`, a project may stay empty with a stated
reason.

If the chosen representations do not exist, show their exact provider metadata
effects as a complete setup batch with its own direct approval. Apply and read
back that batch before rendering the config. Then preview the exact
`.agents/managing-issues.json` content for separate approval. Write only that
displayed path, validate the config, and resume the original request with a
fresh canonical read, complete tracker preview, and its own direct approval
question. An incompatible config follows the same replacement path. Render
schema-required fields and the operator's chosen optional settings in the replacement preview. State all three
decisions explicitly:
provider-metadata approval approves only those metadata effects, repository-
setup approval approves only the displayed file, and the resumed tracker batch
needs its own direct approval. The validator owns schema-version guidance; do
not copy it into prose.

Repository-setup approval is separate from tracker approval. Before the
approved file write, verify that the displayed repository-relative destination
and each existing path component are contained and are not symlinks. Write only
that destination, validate it, then resume the original request. Saving the
setup file approves no tracker effect.
