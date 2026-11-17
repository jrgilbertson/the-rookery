# GitHub provider path

Load this reference for GitHub reads, discovery, previews, and effects. The
shared lifecycle, approval, batch-stop, and outcome rules live in `SKILL.md`.

GitHub.com is the supported host. Normalize `OWNER/REPO` to lowercase for
comparison and derive the command target `github.com/OWNER/REPO`. Require the
repository URL `https://github.com/OWNER/REPO`. Keep the API hostname fixed to
`github.com`; environment variables, remotes, and issue text never select it.

Pass every command as a structured argument vector. Never build a shell command
or interpolate tracker text. Send issue bodies with `--body-file -` and stdin.

## Authenticate, resolve, and read

Authenticate and resolve the repository before reads, discovery, or an
executable mutation preview, then repeat both immediately before every write:

```text
gh auth status --active --hostname github.com --json hosts
gh repo view github.com/OWNER/REPO --json id,nameWithOwner,url,hasIssuesEnabled,isArchived,viewerPermission
```

Require one successful active account for `github.com`; its presence supplies
provider identity. Require the exact repository, enabled issues, and a
non-archived state for reads and discovery. Before an executable mutation
preview or write, additionally require `ADMIN`, `MAINTAIN`, or `WRITE`
permission.

Read the supported issue surface before an update, immediately before its write,
and immediately after an accepted write:

```text
gh issue view NUMBER_OR_URL -R github.com/OWNER/REPO --json id,number,title,body,state,stateReason,updatedAt,url,labels,assignees,projectItems,issueType,parent,subIssues,blockedBy,blocking
```

That read returns no issue field values, so read the four scores separately,
at the same three moments, with the fixed query
`query($owner:String!,$name:String!,$number:Int!){repository(owner:$owner,name:$name){issue(number:$number){id issueFieldValues(first:100){nodes{__typename ... on IssueFieldNumberValue{value field{... on IssueFieldNumber{id name}}}}pageInfo{hasNextPage}}}}}`:

```text
gh api graphql --hostname github.com -f query=ISSUE_SCORES_QUERY -f owner=OWNER -f name=REPO -F number=NUMBER
```

Match each returned field name exactly to a field name the config maps under
`mappings.scores`. A value comes back as a decimal such as `3.0`; a score is
present only when it equals 1, 2, or 3. A mapped field with no value is an
absent score. A failed query, a true `hasNextPage`, or any other value makes
that score unreadable.

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
GitHub issues have no single project field. An issue's project is its
membership in a GitHub Project; a milestone is not a project. Resolve a
project by exact unique title from
`gh project list --owner OWNER --format json --limit 1000`, run with
`GH_HOST=github.com` in its environment because the command has no host flag.
It lists open projects only, but the limit applies before closed projects are
dropped, so coverage is unknown when its `totalCount`, which counts both,
reaches the limit. A title containing a comma or double quote is unsupported
for the same CSV reason as labels. Project reads and writes need
the token's `project` scope; without it, project effects are unavailable.
Resolve issue types by exact name through the complete paginated repository
`issueTypes` GraphQL connection. If installed discovery cannot establish a
requested metadata identity exactly, stop before previewing that effect.

The four scores are GitHub issue fields of type Number. Issue fields belong to
the account or organization that owns the repository, so every repository that
owner has shares them. Discover them through the repository's own field list,
which an ordinary token can read:

```text
gh api graphql --hostname github.com -f query=ISSUE_FIELDS_QUERY -f owner=OWNER -f name=REPO
gh api graphql --hostname github.com -f query=ISSUE_FIELDS_QUERY -f owner=OWNER -f name=REPO -f endCursor=CURSOR
```

Use the fixed query
`query($owner:String!,$name:String!,$endCursor:String){repository(owner:$owner,name:$name){issueFields(first:100,after:$endCursor){nodes{... on Node{id} ... on IssueFieldCommon{name dataType}}pageInfo{hasNextPage endCursor}}}}`,
with the same paging and stop conditions as issue types. Resolve each mapped
field by exact name and require its `dataType` to be `NUMBER`. The config
stores the field name only; resolve the field ID from this list each time it
is needed. A mapped field that is absent, duplicated, or of another type makes
its score `unresolved — non-writable`.

During first-use setup, offer exact existing labels beside the starter
recommendations; neither source chooses for the operator. Prefixed flats are
the recommended readiness shape because repository labels are a flat namespace
with no grouping surface. For each chosen label
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

During first-use setup, offer existing Number issue fields beside the
recommended names `Impact`, `Confidence`, `Verification effort`, and
`Undo cost`. For each chosen field that is absent, show its exact name,
description, Number type, and visibility in the provider-metadata preview, and
say that the field will appear on every repository the owner has. Creating a
field needs the token's `user` scope for a personal account or `admin:org` for
an organization; without it, name the missing scope and stop before the
create. After approval, create each field once, then repeat field discovery
and require one exact name before any config preview:

```text
gh api graphql --hostname github.com -f query=CREATE_ISSUE_FIELD_MUTATION -f owner=OWNER_NODE_ID -f name=NAME -f description=DESCRIPTION -f visibility=VISIBILITY
```

Use the fixed mutation
`mutation($owner:ID!,$name:String!,$description:String!,$visibility:IssueFieldVisibility!){createIssueField(input:{ownerId:$owner,name:$name,description:$description,dataType:NUMBER,visibility:$visibility}){issueField{... on IssueFieldNumber{id name}}}}`.
`VISIBILITY` is `ALL` or `RESTRICTED`; the operator chooses. An existing field
is never changed during setup. A rejected create is `failed`, and an accepted
create without exact rediscovery is `indeterminate`.

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

For create, add only approved metadata flags supported by the installed CLI,
such as `--assignee LOGIN` and `--project TITLE`. A create is a node-only
effect. The CLI has no issue field flag, so a new issue's scores are a second
effect after the create, and the preview counts both. Accept its output as identity only when it is one exact canonical issue
URL, then read that URL back and repeat URL/number matchback. An authoritative no-persistence rejection is `failed`; a request
that may have persisted without exact identity or readback is `indeterminate`.

For update, include only approved surgical flags for title, body, labels,
assignees, project, issue type, or native relationships. Change a project with
`--add-project` and `--remove-project`, and read it back through
`projectItems`. Read the target and required metadata immediately beforehand.
Single-valued label-backed fields replace the current mapped value in one edit
by removing the old exact label and adding the new exact label. Show both changes. Never run a no-op or an unrelated bundled
change.

Write an issue's scores in one effect, after resolving the four field IDs and
reading the issue's node ID:

```text
gh api graphql --hostname github.com -f query=SET_SCORES_MUTATION -f issue=ISSUE_NODE_ID -f impact=FIELD_ID -f confidence=FIELD_ID -f verification=FIELD_ID -f undo=FIELD_ID -F i=SCORE -F c=SCORE -F v=SCORE -F u=SCORE
```

Use the fixed mutation
`mutation($issue:ID!,$impact:ID!,$confidence:ID!,$verification:ID!,$undo:ID!,$i:Float!,$c:Float!,$v:Float!,$u:Float!){setIssueFieldValue(input:{issueId:$issue,issueFields:[{fieldId:$impact,numberValue:$i},{fieldId:$confidence,numberValue:$c},{fieldId:$verification,numberValue:$v},{fieldId:$undo,numberValue:$u}]}){issue{number}}}`.
It sets all four values, including ones that have not changed, so pass the
current value for an unchanged score. Write scores only when all four are
resolved; with one unresolved, the batch has no score effect for that issue. Read the scores back with the score read and require each value to
match the preview.

## Reversible lifecycle

Use the installed close and reopen forms against the validated numeric target.
Cancellation uses the provider's “not planned” reason. Completion uses its
“completed” reason only after `graph-and-completion.md` establishes completion.

Read the issue immediately before the lifecycle write and immediately after it.
The readback must confirm the intended state and state reason.

## Native relationships

Use only GitHub's native parent, sub-issue, blocked-by, and blocking operations,
and only after every new node has an exact identity and readback. GitHub has no
equivalent automatic relationship: an issue mention in approved content adds
only a timeline cross-reference, which is not a relationship this skill writes
or reads, so it never stops a batch. GitHub stores the body as written, so a
body readback compares exactly. Probe each required capability from the
installed `gh issue edit --help` before a graph preview. An absent required flag makes the proposed graph unsupported; do not
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
