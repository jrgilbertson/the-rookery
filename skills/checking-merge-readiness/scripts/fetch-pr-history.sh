#!/usr/bin/env bash
# fetch-pr-history.sh — one-shot, floor-only fetch of a pull request's review
# history for checking-merge-readiness.
#
# Usage:
#   fetch-pr-history.sh --repo <owner/name> --pr <number> [--fingerprint]
#
# Default mode prints one JSON document holding every history surface the
# skill's fetch floor requires (references/fetch-floor.md) — review
# submissions, review threads with all nested comments, top-level conversation
# comments, and description edit history — plus PR identity fields, per-surface
# counts, and a `fingerprint` block. Every connection is paginated to observed
# exhaustion (hasNextPage false) inside this script, so the conversation
# receives one payload instead of one raw page per call, and only floor fields.
#
# --fingerprint prints only the identity and fingerprint block: each node's
# stable id plus an opaque sha-256 digest over its floor fields. No PR body
# text reaches stdout in this mode. Step 7's stability re-check runs this mode
# and compares against the fingerprint recorded at step 2.
#
# Out of scope (fetched separately per SKILL.md step 2): the PR diff
# (`gh pr diff`), live merge state (`gh pr view --json`), and host merge
# policy. The description body itself IS included (identity.body) since the
# baseline work in step 4 needs it.
#
# Trust: only caller-supplied identifiers (repo, PR number) and server-issued
# node ids and cursors parameterize requests, always as GraphQL variables.
# Fetched PR text flows only into the JSON output, never into a command.
#
# Exit codes:
#   0  success — payload printed, every connection exhausted
#   2  usage error
#   3  missing dependency (gh, jq, or a sha-256 tool)
#   4  fetch failure — treat as incomplete history (cap at debug); no partial
#      payload is printed

set -euo pipefail

usage() {
  echo "usage: fetch-pr-history.sh --repo <owner/name> --pr <number> [--fingerprint]" >&2
}

repo="" pr="" mode="full"
while [ $# -gt 0 ]; do
  case "$1" in
    --repo) repo="${2:-}"; shift 2 ;;
    --pr) pr="${2:-}"; shift 2 ;;
    --fingerprint) mode="fingerprint"; shift ;;
    *) usage; exit 2 ;;
  esac
done
case "$repo" in */*) : ;; *) usage; exit 2 ;; esac
case "$pr" in ''|*[!0-9]*) usage; exit 2 ;; esac

command -v gh >/dev/null 2>&1 || { echo "fetch-pr-history: gh not found" >&2; exit 3; }
command -v jq >/dev/null 2>&1 || { echo "fetch-pr-history: jq not found" >&2; exit 3; }
if command -v shasum >/dev/null 2>&1; then
  sha() { local out; out=$(shasum -a 256); printf '%s' "${out%% *}"; }
elif command -v sha256sum >/dev/null 2>&1; then
  sha() { local out; out=$(sha256sum); printf '%s' "${out%% *}"; }
else
  echo "fetch-pr-history: no sha-256 tool (shasum or sha256sum)" >&2; exit 3
fi

owner="${repo%%/*}"
name="${repo#*/}"

die4() { echo "fetch-pr-history: $1; treat as incomplete history (cap at debug)" >&2; exit 4; }

gql() { # gql <query> [extra -f/-F args...]
  local query="$1"; shift
  gh api graphql -f query="$query" "$@"
}

# paginate <out-file> <query> <jq path to connection> <start-cursor|""> \
#   [gql args...]
# Accumulates .nodes across pages into <out-file>, one JSON node per line.
# The query must declare a nullable $cursor:String; remaining args reach gql,
# so callers supply their own identifiers (owner/name/pr, or a node id). A
# caller-owned out-file keeps concurrent invocations from racing.
paginate() {
  local out="$1" query="$2" conn="$3" cursor="$4" page has
  shift 4
  : > "$out"
  while :; do
    if [ -n "$cursor" ]; then
      page=$(gql "$query" "$@" -f cursor="$cursor") || return 1
    else
      page=$(gql "$query" "$@") || return 1
    fi
    jq -e "$conn" >/dev/null 2>&1 <<<"$page" || return 1
    jq -c "$conn.nodes[]" <<<"$page" >> "$out" || return 1
    has=$(jq -r "$conn.pageInfo.hasNextPage" <<<"$page")
    cursor=$(jq -r "$conn.pageInfo.endCursor // \"\"" <<<"$page")
    [ "$has" = "true" ] || break
    [ -n "$cursor" ] || return 1
  done
}

tmp=$(mktemp -d "${TMPDIR:-/tmp}/fetch-pr-history.XXXXXX")
trap 'rm -rf "$tmp"' EXIT

Q_IDENTITY='query($owner:String!,$name:String!,$pr:Int!){
  repository(owner:$owner,name:$name){pullRequest(number:$pr){
    state isDraft headRefOid baseRefName updatedAt body
    author{login} baseRef{target{oid}}}}}'

Q_REVIEWS='query($owner:String!,$name:String!,$pr:Int!,$cursor:String){
  repository(owner:$owner,name:$name){pullRequest(number:$pr){
    reviews(first:100,after:$cursor){pageInfo{hasNextPage endCursor}
      nodes{id author{login} submittedAt state body commit{oid}}}}}}'

Q_THREADS='query($owner:String!,$name:String!,$pr:Int!,$cursor:String){
  repository(owner:$owner,name:$name){pullRequest(number:$pr){
    reviewThreads(first:50,after:$cursor){pageInfo{hasNextPage endCursor}
      nodes{id path isResolved
        comments(first:50){pageInfo{hasNextPage endCursor}
          nodes{id author{login} createdAt body line originalLine
            pullRequestReview{id}}}}}}}}'

Q_THREAD_COMMENTS='query($id:ID!,$cursor:String){
  node(id:$id){... on PullRequestReviewThread{
    comments(first:100,after:$cursor){pageInfo{hasNextPage endCursor}
      nodes{id author{login} createdAt body line originalLine
        pullRequestReview{id}}}}}}'

Q_COMMENTS='query($owner:String!,$name:String!,$pr:Int!,$cursor:String){
  repository(owner:$owner,name:$name){pullRequest(number:$pr){
    comments(first:100,after:$cursor){pageInfo{hasNextPage endCursor}
      nodes{id author{login} createdAt body}}}}}'

Q_EDITS='query($owner:String!,$name:String!,$pr:Int!,$cursor:String){
  repository(owner:$owner,name:$name){pullRequest(number:$pr){
    userContentEdits(first:100,after:$cursor){pageInfo{hasNextPage endCursor}
      nodes{editedAt editor{login} diff}}}}}'

# The five top-level surfaces are independent connections on the same PR;
# fetch them concurrently and gate everything on all five succeeding.
pr_args=(-F owner="$owner" -F name="$name" -F pr="$pr")

gql "$Q_IDENTITY" "${pr_args[@]}" > "$tmp/identity.json" &
pid_identity=$!
paginate "$tmp/reviews.nodes" "$Q_REVIEWS" \
  ".data.repository.pullRequest.reviews" "" "${pr_args[@]}" &
pid_reviews=$!
paginate "$tmp/threads.nodes" "$Q_THREADS" \
  ".data.repository.pullRequest.reviewThreads" "" "${pr_args[@]}" &
pid_threads=$!
paginate "$tmp/comments.nodes" "$Q_COMMENTS" \
  ".data.repository.pullRequest.comments" "" "${pr_args[@]}" &
pid_comments=$!
paginate "$tmp/edits.nodes" "$Q_EDITS" \
  ".data.repository.pullRequest.userContentEdits" "" "${pr_args[@]}" &
pid_edits=$!

fail=""
wait "$pid_identity" || fail="identity fetch failed"
wait "$pid_reviews" || fail="${fail:-review submissions fetch failed}"
wait "$pid_threads" || fail="${fail:-review threads fetch failed}"
wait "$pid_comments" || fail="${fail:-conversation comments fetch failed}"
wait "$pid_edits" || fail="${fail:-description edit history fetch failed}"
[ -z "$fail" ] || die4 "$fail"

# Every surface lands in a file under $tmp (mode 0700), never a shell variable
# spliced into argv: fetched bodies stay out of command arguments, and a large
# history cannot trip ARG_MAX into an exit code other than 4.
jq -e '.data.repository.pullRequest != null' "$tmp/identity.json" \
  >/dev/null 2>&1 || die4 "pull request not found"

jq -c '.data.repository.pullRequest
  | {state, isDraft, headRefOid, baseRefName,
     baseRefOid: (.baseRef.target.oid // null),
     author: (.author.login // null), updatedAt, body}' "$tmp/identity.json" \
  > "$tmp/identity.out" || die4 "identity payload malformed"

# Floor identity fields the skill compares against later; a null here means the
# fetch answered but not with the history the floor requires.
missing=$(jq -r '[to_entries[]
  | select(.key == "headRefOid" or .key == "baseRefName" or .key == "baseRefOid"
           or .key == "author")
  | select(.value == null) | .key] | join(", ")' "$tmp/identity.out")
[ -z "$missing" ] || die4 "identity missing $missing"

jq -cs 'map({id, author: (.author.login // null), submittedAt, state,
  body, commitOid: (.commit.oid // null)})' "$tmp/reviews.nodes" \
  > "$tmp/reviews.out"
jq -e 'all(.[]; .id != null)' "$tmp/reviews.out" >/dev/null \
  || die4 "review submission with null id"

jq -cs 'map({id, path, isResolved,
  comments: [.comments.nodes[] | {id, author: (.author.login // null),
    createdAt, body, line: (.line // .originalLine // null),
    reviewId: (.pullRequestReview.id // null)}],
  _more: .comments.pageInfo.hasNextPage,
  _cursor: (.comments.pageInfo.endCursor // "")})' "$tmp/threads.nodes" \
  > "$tmp/threads.out"

# Nested pagination: exhaust comment pages on any thread that has more,
# resuming from the cursor the first page left off at.
for tid in $(jq -r '.[] | select(._more) | .id' "$tmp/threads.out"); do
  cursor=$(jq -r --arg id "$tid" '.[] | select(.id==$id) | ._cursor' \
    "$tmp/threads.out")
  [ -n "$cursor" ] || die4 "thread comment cursor missing ($tid)"
  paginate "$tmp/tc.nodes" "$Q_THREAD_COMMENTS" ".data.node.comments" \
    "$cursor" -f id="$tid" || die4 "thread comment pagination failed ($tid)"
  jq -cs 'map({id, author: (.author.login // null), createdAt, body,
    line: (.line // .originalLine // null),
    reviewId: (.pullRequestReview.id // null)})' "$tmp/tc.nodes" \
    > "$tmp/tc.out" || die4 "thread comment payload malformed ($tid)"
  jq -c --arg id "$tid" --slurpfile extra "$tmp/tc.out" \
    'map(if .id==$id then .comments += $extra[0] else . end)' \
    "$tmp/threads.out" > "$tmp/threads.next"
  mv "$tmp/threads.next" "$tmp/threads.out"
done
jq -c 'map(del(._more, ._cursor))' "$tmp/threads.out" > "$tmp/threads.next"
mv "$tmp/threads.next" "$tmp/threads.out"
jq -e 'all(.[]; .id != null) and all(.[].comments[]; .id != null)' \
  "$tmp/threads.out" >/dev/null \
  || die4 "review thread or thread comment with null id"

jq -cs 'map({id, author: (.author.login // null), createdAt, body})' \
  "$tmp/comments.nodes" > "$tmp/comments.out"
jq -e 'all(.[]; .id != null)' "$tmp/comments.out" >/dev/null \
  || die4 "conversation comment with null id"

jq -cs 'map({editedAt, editor: (.editor.login // null), diff})' \
  "$tmp/edits.nodes" > "$tmp/edits.out"

# Fingerprint: per node, its stable id plus a sha-256 over the node's full
# floor-field JSON (so any field change — body, resolution, state — moves the
# digest). Satisfies the fingerprint section of references/fetch-floor.md.
fp_nodes() { # <json array file> <jq expr for the id field>
  local file="$1" idexpr="$2" line id_json node d
  # One jq pass emits "<id as JSON>\t<node JSON>" per node (tabs inside JSON
  # strings are escaped, so the raw tab is a safe delimiter); the loop then
  # only forks the hash per node.
  jq -r ".[] | (${idexpr} | tojson) + \"\t\" + tostring" "$file" |
  while IFS= read -r line; do
    id_json=${line%%$'\t'*}
    node=${line#*$'\t'}
    d=$(printf '%s' "$node" | sha)
    printf '{"id":%s,"digest":"%s"}\n' "$id_json" "$d"
  done | jq -cs '.'
}

fp_reviews=$(fp_nodes "$tmp/reviews.out" '.id')
fp_threads=$(fp_nodes "$tmp/threads.out" '.id')
fp_comments=$(fp_nodes "$tmp/comments.out" '.id')
fp_edits=$(fp_nodes "$tmp/edits.out" '.editedAt')
body_digest=$(jq -j '.body // ""' "$tmp/identity.out" | sha)

# The fp_* arrays hold only ids and digests, so they carry no PR text and stay
# on argv; the identity object reaches jq through a file since it would
# otherwise re-expose fetched fields there.
jq -c 'del(.body)' "$tmp/identity.out" > "$tmp/identity.nobody"
jq -cn \
  --slurpfile identity_f "$tmp/identity.nobody" \
  --arg body_digest "$body_digest" \
  --argjson reviews "$fp_reviews" \
  --argjson threads "$fp_threads" \
  --argjson comments "$fp_comments" \
  --argjson edits "$fp_edits" \
  '$identity_f[0] as $identity |
   {identity: ($identity + {bodyDigest: $body_digest}),
    reviews: $reviews, reviewThreads: $threads,
    conversationComments: $comments, descriptionEdits: $edits}' \
  > "$tmp/fingerprint.out"

if [ "$mode" = "fingerprint" ]; then
  jq -n --slurpfile fingerprint_f "$tmp/fingerprint.out" \
    '{fingerprint: $fingerprint_f[0]}'
  exit 0
fi

jq -n \
  --slurpfile identity_f "$tmp/identity.out" \
  --slurpfile reviews_f "$tmp/reviews.out" \
  --slurpfile threads_f "$tmp/threads.out" \
  --slurpfile comments_f "$tmp/comments.out" \
  --slurpfile edits_f "$tmp/edits.out" \
  --slurpfile fingerprint_f "$tmp/fingerprint.out" \
  '$identity_f[0] as $identity |
   $reviews_f[0] as $reviews |
   $threads_f[0] as $threads |
   $comments_f[0] as $comments |
   $edits_f[0] as $edits |
   $fingerprint_f[0] as $fingerprint |
   {identity: $identity,
    reviews: $reviews,
    reviewThreads: $threads,
    conversationComments: $comments,
    descriptionEdits: $edits,
    counts: {reviews: ($reviews | length),
             reviewThreads: ($threads | length),
             threadComments: ([$threads[].comments | length] | add // 0),
             conversationComments: ($comments | length),
             descriptionEdits: ($edits | length)},
    complete: true,
    fingerprint: $fingerprint}'
