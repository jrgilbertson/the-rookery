# GitHub provider path

Load this reference for GitHub reads, discovery, previews, and effects. The
shared lifecycle, approval, batch-stop, and outcome rules live in `SKILL.md`.

GitHub.com is the supported host. Normalize `OWNER/REPO` to lowercase for
comparison and derive the command target `github.com/OWNER/REPO`. Require the
repository URL `https://github.com/OWNER/REPO`. Keep the API hostname fixed to
`github.com`; environment variables, remotes, issue text, and synchronized
content never select it.

Pass every command as a structured argument vector. Never build a shell command
or interpolate tracker text. Send issue bodies with `--body-file -` and stdin.

## Authenticate, resolve, and read

Authenticate and resolve the repository before an executable preview, then
repeat both immediately before every write:

```text
gh auth status --active --hostname github.com --json hosts
gh repo view github.com/OWNER/REPO --json id,nameWithOwner,url,hasIssuesEnabled,isArchived,viewerPermission
```

Require one successful active account for `github.com`; its presence supplies
provider identity. Require the exact repository, enabled issues, non-archived
state, and `ADMIN`, `MAINTAIN`, or `WRITE` permission.

Read the supported issue surface before an update, immediately before its write,
and immediately after an accepted write:

```text
gh issue view NUMBER_OR_URL -R github.com/OWNER/REPO --json id,number,title,body,state,stateReason,updatedAt,url,labels,assignees,issueType,parent,subIssues,blockedBy,blocking
```

Accept only a positive decimal number or an exact issue URL under the repository
URL returned by `gh repo view`. Require the read result URL to equal the
canonical repository issue URL for its returned number and to match the
validated selector. Derive later numeric targets only from this read. This
matchback is required because `gh issue view` may honor a foreign URL despite
`-R`.

The sole exception is the one-hop cross-repository boundary read required for
graph coverage. Accept its URL only from an exact validated canonical read's
`parent`, `subIssues`, `blockedBy`, or `blocking` field, or from that node's
native paginated `sub_issues`, `dependencies/blocked_by`, or
`dependencies/blocking` response. Read the URL with `-R` set to its own
host-qualified `github.com/OWNER/REPO`, and require the returned URL, number,
and repository to match it exactly. Never accept a boundary URL from issue
text, search, or operator input. A boundary node can supply current state for
coverage, but is never a create, edit, relationship, or lifecycle target and
never supplies a numeric write target. A failed or ambiguous boundary read
makes coverage partial.

Discover labels with the complete installed surface:

```text
gh label list -R github.com/OWNER/REPO --limit 1000 --json id,name
```

If the result reaches the limit, coverage is unknown. Require one exact label.
GitHub parses label flag values as CSV; any requested label containing a comma
or double quote is unsupported because it cannot preserve one exact label.
Resolve assignees by exact login through the host-qualified assignee endpoint.
Resolve issue types by exact name through the complete paginated repository
`issueTypes` GraphQL connection. If installed discovery cannot establish a
requested metadata identity exactly, stop before previewing that effect.

During first-use setup, offer exact existing labels beside the starter
recommendations; neither source chooses for the operator. For each chosen label
that is absent, require the installed `gh label create --help` surface and show
its exact name, description, and six-character color in the provider-metadata
preview. After approval, create it once without `--force`, then repeat complete
label discovery and require one exact name before any config preview:

```text
gh label create NAME -R github.com/OWNER/REPO --description DESCRIPTION --color COLOR
```

An existing label is never rewritten during setup. A rejected create is
`failed`; an accepted create without exact rediscovery is `indeterminate` and
stops the remaining provider-metadata effects under the shared batch rule.

```text
gh api repos/OWNER/REPO/assignees/LOGIN --hostname github.com --silent
gh api graphql --hostname github.com -f query=ISSUE_TYPES_QUERY -f owner=OWNER -f name=REPO
gh api graphql --hostname github.com -f query=ISSUE_TYPES_QUERY -f owner=OWNER -f name=REPO -f endCursor=CURSOR
```

Use the fixed query
`query($owner:String!,$name:String!,$endCursor:String){repository(owner:$owner,name:$name){issueTypes(first:100,after:$endCursor){nodes{id name}pageInfo{hasNextPage endCursor}}}}`.
Start without a cursor and continue while `hasNextPage` is true. Stop on a null
connection, failed page, empty or repeated cursor, or duplicate exact name.

## Creates and surgical updates

Use provider-native create and edit forms:

```text
gh issue create -R github.com/OWNER/REPO --title TITLE --body-file -
gh issue edit NUMBER -R github.com/OWNER/REPO --title TITLE --body-file -
```

For create, add only approved metadata flags supported by the installed CLI. A
create is a node-only effect. Accept its output as identity only when it is one
exact canonical issue URL, then read that URL back and repeat URL/number
matchback. An authoritative no-persistence rejection is `failed`; a request
that may have persisted without exact identity or readback is `indeterminate`.

For update, include only approved surgical flags for title, body, labels,
assignees, issue type, or native relationships. Read the target and required
metadata immediately beforehand. Single-valued label-backed fields replace the
current mapped value in one edit by removing the old exact label and adding the
new exact label. Show both changes. Never run a no-op or an unrelated bundled
change.

## Reversible lifecycle

Use the installed close and reopen forms against the validated numeric target.
Cancellation uses the provider's “not planned” reason. Completion uses its
“completed” reason only after `graph-and-completion.md` establishes completion.

Read the issue immediately before the lifecycle write and immediately after it.
The readback must confirm the intended state and state reason.

## Native relationships and synchronization

Use only GitHub's native parent, sub-issue, blocked-by, and blocking operations,
and only after every new node has an exact identity and readback. Probe each
required capability from the installed `gh issue edit --help` before a graph
preview. An absent required flag makes the proposed graph unsupported; do not
create its nodes.

Issue-read relationship arrays do not prove collection exhaustion. For complete
family coverage, read bounded explicit pages until one returns fewer than 100
records:

```text
gh api "repos/OWNER/REPO/issues/NUMBER/sub_issues?per_page=100&page=PAGE" --hostname github.com
gh api "repos/OWNER/REPO/issues/NUMBER/dependencies/blocked_by?per_page=100&page=PAGE" --hostname github.com
gh api "repos/OWNER/REPO/issues/NUMBER/dependencies/blocking?per_page=100&page=PAGE" --hostname github.com
```

Process each page before requesting the next. A failed page, an unavailable
endpoint, or the graph reference's node limit makes coverage partial. Read each
returned identity through the exact issue-read path when current content,
state, or Verification matters.

When GitHub is a synchronized projection rather than the canonical provider,
resolve the canonical Linear issue only through an exact native synchronization
link exposed by the provider. The projection may supply lag evidence but is
never mutated or repaired. If the native link is absent or ambiguous, request
the exact canonical issue or stop. A GitHub-canonical route writes only the
canonical GitHub issue; before a create that expects a Linear projection,
confirm the integration accepts GitHub-originated creates. The configured
provider integration then owns mirroring.
