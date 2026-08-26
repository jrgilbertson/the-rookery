#!/usr/bin/env bash
# Minimal contract checks for the fixture `gh` stub.
#
# Scope: the few ways a constructed run can pass falsely —
#   write succeeds, wrong PR served, under-fetch, page never followed,
#   auth failure reads as success, variable cursor ignored.
# Not in scope: GraphQL well-formedness (scenario 11 / live GitHub).
#
#   bash tests/checking-merge-readiness/fixtures/run-stub-checks.sh

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GH="$HERE/bin/gh"
PRS="$HERE/prs"
PASS=0
FAIL=0
AUTHFAIL=
ISSUEFAIL=

pass() { PASS=$((PASS + 1)); printf 'PASS  %s\n' "$1"; }
fail() { FAIL=$((FAIL + 1)); printf 'FAIL  %s\n     %s\n' "$1" "$2"; }

exit_is() {
  local label=$1 want=$2 spec=$3; shift 3
  local out got
  out=$(env CMR_FIXTURE="$PRS/$spec" ${AUTHFAIL:+CMR_GH_AUTH_FAIL=1} ${ISSUEFAIL:+CMR_ISSUE_VIEW_FAIL=1} "$GH" "$@" 2>&1); got=$?
  if [ "$got" = "$want" ]; then pass "$label"
  else fail "$label" "expected exit $want, got $got: $(printf '%s' "$out" | head -1)"; fi
}

msg_is() {
  local label=$1 want=$2 needle=$3 spec=$4; shift 4
  local out got
  out=$(env CMR_FIXTURE="$PRS/$spec" ${AUTHFAIL:+CMR_GH_AUTH_FAIL=1} ${ISSUEFAIL:+CMR_ISSUE_VIEW_FAIL=1} "$GH" "$@" 2>&1); got=$?
  if [ "$got" != "$want" ]; then
    fail "$label" "expected exit $want, got $got: $(printf '%s' "$out" | head -1)"; return
  fi
  case "$out" in
    *"$needle"*) pass "$label" ;;
    *) fail "$label" "exit $want but for the wrong reason: $(printf '%s' "$out" | head -1)" ;;
  esac
}

json_is() {
  local label=$1 spec=$2 expr=$3 want=$4; shift 4
  local raw got
  if ! raw=$(env CMR_FIXTURE="$PRS/$spec" ${AUTHFAIL:+CMR_GH_AUTH_FAIL=1} ${ISSUEFAIL:+CMR_ISSUE_VIEW_FAIL=1} "$GH" "$@" 2>&1); then
    fail "$label" "command failed: $(printf '%s' "$raw" | head -1)"; return
  fi
  got=$(printf '%s' "$raw" | python3 -c "
import json,sys
d=json.load(sys.stdin)['data']['repository']['pullRequest']
print($expr)
" 2>&1)
  if [ "$got" = "$want" ]; then pass "$label"
  else fail "$label" "expected [$want], got [$got]"; fi
}

top_json_is() {
  local label=$1 spec=$2 expr=$3 want=$4; shift 4
  local raw got
  if ! raw=$(env CMR_FIXTURE="$PRS/$spec" ${AUTHFAIL:+CMR_GH_AUTH_FAIL=1} ${ISSUEFAIL:+CMR_ISSUE_VIEW_FAIL=1} "$GH" "$@" 2>&1); then
    fail "$label" "command failed: $(printf '%s' "$raw" | head -1)"; return
  fi
  got=$(printf '%s' "$raw" | python3 -c "
import json,sys
d=json.load(sys.stdin)
print($expr)
" 2>&1)
  if [ "$got" = "$want" ]; then pass "$label"
  else fail "$label" "expected [$want], got [$got]"; fi
}

# Floor-aligned shapes (SKILL.md step 2); extra fields still allowed.
THREADS='query{repository{pullRequest{reviewThreads(first:100){pageInfo{hasNextPage endCursor} nodes{id isResolved path line comments(first:100){nodes{id body author{login} pullRequestReview{id submittedAt}}}}}}}}'
REVIEWS='query{repository{pullRequest{reviews(first:100){pageInfo{hasNextPage endCursor} nodes{id author{login} submittedAt state body commit{oid}}}}}}'
COMMENTS='query{repository{pullRequest{comments(first:100){pageInfo{hasNextPage endCursor} nodes{id body author{login}}}}}}'
EDITS='query{repository{pullRequest{userContentEdits(first:100){pageInfo{hasNextPage endCursor} nodes{editedAt editor{login} diff}}}}}'
# shellcheck disable=SC2016
ISSUE_COMMENTS='query($owner:String!,$name:String!,$issueNumber:Int!){repository(owner:$owner,name:$name){issue(number:$issueNumber){number title body state url comments(first:100){pageInfo{hasNextPage endCursor} nodes{id body author{login} createdAt url}}}}}'

echo "== A. serve real fixture content =="
json_is "specimen-a: four resolved threads" \
  specimen-a "str(len(d['reviewThreads']['nodes']))+' '+str(all(t['isResolved'] for t in d['reviewThreads']['nodes']))" \
  "4 True" api graphql -f "query=$THREADS"
json_is "specimen-e: one unresolved thread" \
  specimen-e "sum(1 for t in d['reviewThreads']['nodes'] if not t['isResolved'])" \
  "1" api graphql -f "query=$THREADS"
json_is "specimen-j: page one reports more" \
  specimen-j "str(len(d['reviewThreads']['nodes']))+' '+str(d['reviewThreads']['pageInfo']['hasNextPage'])" \
  "2 True" api graphql -f "query=$THREADS"
json_is "specimen-j: page two is the third thread" \
  specimen-j "str(len(d['reviewThreads']['nodes']))+' '+str(d['reviewThreads']['pageInfo']['hasNextPage'])" \
  "1 False" api graphql \
  -f 'query=query{repository{pullRequest{reviewThreads(first:100, after:"reviewThreads:2"){pageInfo{hasNextPage endCursor} nodes{id isResolved path line comments(first:100){nodes{id body author{login} pullRequestReview{id submittedAt}}}}}}}}'
# Variable-bound after (what real skill runs use) — the footgun that forced the greenfield cursor fix.
# shellcheck disable=SC2016
json_is "specimen-j: variable after advances reviews" \
  specimen-j "any('invalidat' in (n.get('body') or '').lower() for n in d['reviews']['nodes'])" \
  "True" api graphql \
  -f 'query=query($cursor:String){repository{pullRequest{reviews(first:100, after:$cursor){pageInfo{hasNextPage endCursor} nodes{id author{login} submittedAt state body commit{oid}}}}}}' \
  -f 'cursor=reviews:2'
json_is "specimen-j: counters request behind comments cursor" \
  specimen-j "any('hit' in (n.get('body') or '') for n in d['comments']['nodes'])" \
  "True" api graphql \
  -f 'query=query{repository{pullRequest{comments(first:100, after:"comments:2"){pageInfo{hasNextPage endCursor} nodes{id body author{login}}}}}}'
top_json_is "specimen-a: pull request exposes its closing issue" \
  specimen-a "d['closingIssuesReferences'][0]['number']" "73" \
  pr view 412 --repo mapleworks/orderline --json closingIssuesReferences
top_json_is "specimen-a: source issue metadata is served" \
  specimen-a "str(d['number'])+' '+d['title']" \
  "73 Export filtered invoices as CSV" \
  issue view 73 --repo mapleworks/orderline --json number,title,body,state,url
top_json_is "specimen-a: source issue comments use GraphQL" \
  specimen-a "str(d['data']['repository']['issue']['number'])+' '+str(len(d['data']['repository']['issue']['comments']['nodes']))" \
  "73 1" api graphql -f "query=$ISSUE_COMMENTS" \
  -F owner=mapleworks -F name=orderline -F issueNumber=73
exit_is "specimen-a: issue GraphQL rejects another repository" 1 specimen-a \
  api graphql -f "query=$ISSUE_COMMENTS" \
  -F owner=mapleworks -F name=another-repo -F issueNumber=73
exit_is "specimen-a: issue view cannot substitute for comment pagination" \
  2 specimen-a issue view 73 --repo mapleworks/orderline \
  --json number,title,body,state,url,comments
top_json_is "specimen-m: pull request exposes both closing issues" \
  specimen-m "str(len(d['closingIssuesReferences']))" "2" \
  pr view 501 --repo mapleworks/orderline --json closingIssuesReferences
top_json_is "specimen-m: second closing issue is served" \
  specimen-m "str(d['number'])+' '+d['title']" \
  "81 Migrate scheduled invoice exports" \
  issue view 81 --repo mapleworks/orderline --json number,title,body,state,url

echo "== B. under-fetch refuses (floor-aligned) =="
exit_is "reviews without commit" 2 specimen-a api graphql \
  -f 'query=query{repository{pullRequest{reviews(first:1){nodes{id author{login} submittedAt state body}}}}}'
exit_is "reviews without id" 2 specimen-a api graphql \
  -f 'query=query{repository{pullRequest{reviews(first:1){nodes{author{login} submittedAt state body commit{oid}}}}}}'
exit_is "reviews without author" 2 specimen-a api graphql \
  -f 'query=query{repository{pullRequest{reviews(first:1){nodes{id submittedAt state body commit{oid}}}}}}'
exit_is "threads without isResolved" 2 specimen-a api graphql \
  -f 'query=query{repository{pullRequest{reviewThreads(first:1){pageInfo{hasNextPage} nodes{id path line comments(first:100){nodes{id body author{login} pullRequestReview{id submittedAt}}}}}}}}'
exit_is "threads without pullRequestReview join" 2 specimen-a api graphql \
  -f 'query=query{repository{pullRequest{reviewThreads(first:1){nodes{id isResolved path comments(first:100){nodes{id body author{login}}}}}}}}'
exit_is "edits without diff snapshot" 2 specimen-a api graphql \
  -f 'query=query{repository{pullRequest{userContentEdits(first:1){nodes{editedAt editor{login}}}}}}'
exit_is "edits without editor" 2 specimen-a api graphql \
  -f 'query=query{repository{pullRequest{userContentEdits(first:1){nodes{editedAt diff}}}}}'
exit_is "skill-shaped threads query accepted" 0 specimen-a api graphql -f "query=$THREADS"
exit_is "skill-shaped edits query accepted" 0 specimen-a api graphql -f "query=$EDITS"
# shellcheck disable=SC2016
exit_is "issue comments without createdAt refused" 2 specimen-a api graphql \
  -f 'query=query($owner:String!,$name:String!,$issueNumber:Int!){repository(owner:$owner,name:$name){issue(number:$issueNumber){number title body state url comments(first:100){pageInfo{hasNextPage endCursor} nodes{id body author{login}}}}}}' \
  -F owner=mapleworks -F name=orderline -F issueNumber=73

echo "== C. every specimen serves the battery-shaped queries =="
for d in "$PRS"/specimen-*; do
  s=$(basename "$d")
  exit_is "specimen $s: threads" 0 "$s" api graphql -f "query=$THREADS"
  exit_is "specimen $s: reviews" 0 "$s" api graphql -f "query=$REVIEWS"
  exit_is "specimen $s: comments" 0 "$s" api graphql -f "query=$COMMENTS"
  exit_is "specimen $s: edits" 0 "$s" api graphql -f "query=$EDITS"
  exit_is "specimen $s: description" 0 "$s" pr view --json number,body,state
  exit_is "specimen $s: diff" 0 "$s" pr diff
done

echo "== D. joins name real review submissions by id =="
for d in "$PRS"/specimen-*; do
  s=$(basename "$d")
  got=$(python3 - "$d/forge.json" <<'PYE'
import json,sys
d=json.load(open(sys.argv[1]))
real={r.get("id") for r in d.get("reviews",[]) if r.get("id")}
ghosts=[c["pullRequestReview"].get("id")
        for t in d.get("reviewThreads",[]) for c in t.get("comments",[])
        if isinstance(c.get("pullRequestReview"),dict)
        and c["pullRequestReview"].get("id") not in real]
missing=sum(1 for t in d.get("reviewThreads",[]) for c in t.get("comments",[])
            if isinstance(c.get("pullRequestReview"),dict)
            and not c["pullRequestReview"].get("id"))
print(f"{len(ghosts)} {missing}")
PYE
)
  if [ "$got" = "0 0" ]; then pass "specimen $s: no ghost review join id"
  else fail "specimen $s: no ghost review join id" "ghosts/missing: $got"; fi
done
out=$(env CMR_FIXTURE="$PRS/specimen-a" "$GH" pr view --json baseRefOid 2>&1); got=$?
if [ "$got" = 0 ] && printf '%s' "$out" | python3 -c 'import json,sys; d=json.load(sys.stdin); raise SystemExit(0 if d.get("baseRefOid") else 1)' 2>/dev/null
then pass "identity: baseRefOid non-empty on pr view"
else fail "identity: baseRefOid non-empty on pr view" "$out"; fi

echo "== E. read-only perimeter =="
exit_is "pr view without --json" 2 specimen-a pr view
exit_is "pr view unknown field" 2 specimen-a pr view --json bogusField
exit_is "pr view served fields" 0 specimen-a pr view --json number,title,closingIssuesReferences
msg_is "pr merge writes" 3 "writes; this stub is read-only" specimen-a pr merge
MERGELOG=$(mktemp)
MERGEST=$(mktemp)
out=$(env CMR_ALLOW_MERGE=1 CMR_MERGE_LOG="$MERGELOG" CMR_MERGE_STATE="$MERGEST" CMR_FIXTURE="$PRS/specimen-a" "$GH" pr merge 412 --repo mapleworks/orderline --squash --match-head-commit a91e4f0 2>&1); got=$?
if [ "$got" = 0 ]; then pass "gated pr merge: success"
else fail "gated pr merge: success" "$out"; fi
if python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); raise SystemExit(0 if d.get("method")=="--squash" and d.get("matchHeadCommit")=="a91e4f0" else 1)' "$MERGELOG"
then pass "gated pr merge: argv recorded"
else fail "gated pr merge: argv recorded" "$(cat "$MERGELOG")"
fi
out=$(env CMR_ALLOW_MERGE=1 CMR_MERGE_STATE="$MERGEST" CMR_FIXTURE="$PRS/specimen-a" "$GH" pr view --json state,mergedAt 2>&1); got=$?
if [ "$got" = 0 ] && printf '%s' "$out" | python3 -c 'import json,sys; d=json.load(sys.stdin); raise SystemExit(0 if d.get("state")=="MERGED" and d.get("mergedAt") else 1)'
then pass "gated pr merge: readback MERGED"
else fail "gated pr merge: readback MERGED" "$out"; fi
out=$(env CMR_ALLOW_MERGE=1 CMR_FIXTURE="$PRS/specimen-a" "$GH" pr merge 412 --repo mapleworks/orderline --squash --admin --match-head-commit a91e4f0 2>&1); got=$?
if [ "$got" = 3 ] && printf '%s' "$out" | grep -q "refuses --admin"
then pass "gated pr merge refuses --admin"
else fail "gated pr merge refuses --admin" "$out"; fi
rm -f "$MERGELOG" "$MERGEST"
msg_is "pr edit writes" 3 "writes; this stub is read-only" specimen-a pr edit
msg_is "pr checkout outside set" 3 "outside the skill" specimen-a pr checkout
msg_is "issue edit writes" 3 "writes; this stub is read-only" specimen-a issue edit 73
msg_is "auth login writes" 3 "the rest of" specimen-a auth login
exit_is "auth status reads" 0 specimen-a auth status
exit_is "issue list outside set" 3 specimen-a issue list

echo "== F. selector agrees with specimen =="
exit_is "correct number + owner" 0 specimen-a pr view 412 --repo mapleworks --json number
exit_is "no selector serves specimen" 0 specimen-a pr view --json number
exit_is "wrong number" 1 specimen-a pr view 999999 --json number
exit_is "wrong repo" 1 specimen-a pr view 412 --repo entirely/wrong --json number
exit_is "matching URL" 0 specimen-a pr view https://github.com/mapleworks/orderline/pull/412 --json number
exit_is "diff refuses another PR" 1 specimen-a pr diff 999999
exit_is "linked issue number + repo" 0 specimen-a issue view 73 --repo mapleworks/orderline --json number
exit_is "linked issue number + canonical repo flag" 0 specimen-a issue view 73 -R github.com/mapleworks/orderline --json number
exit_is "linked issue URL" 0 specimen-a issue view https://github.com/mapleworks/orderline/issues/73 --json number
exit_is "external-host issue URL" 1 specimen-a issue view https://evil.example/mapleworks/orderline/issues/73 --json number
ISSUEFAIL=1
msg_is "linked issue unavailable" 4 "temporarily unavailable" specimen-a issue view 73 --repo mapleworks/orderline --json number
ISSUEFAIL=
exit_is "wrong issue number" 1 specimen-a issue view 999999 --repo mapleworks/orderline --json number
exit_is "wrong issue repo" 1 specimen-a issue view 73 --repo entirely/wrong --json number
exit_is "wrong issue repo with canonical flag" 1 specimen-a issue view 73 -R github.com/entirely/wrong --json number
exit_is "rules for the specimen's base" 0 specimen-a \
  api repos/mapleworks/orderline/rules/branches/main
msg_is "rules for another base" 1 "Not Found (HTTP 404)" specimen-a \
  api repos/mapleworks/orderline/rules/branches/release-2024

echo "== G. unauthenticated forge =="
AUTHFAIL=1
exit_is "auth-fail pr view" 4 specimen-a pr view --json number
exit_is "auth-fail issue view" 4 specimen-a issue view 73 --repo mapleworks/orderline --json number
exit_is "auth-fail graphql" 4 specimen-a api graphql -f "query=$REVIEWS"
exit_is "auth-fail status" 1 specimen-a auth status
AUTHFAIL=
exit_is "authenticated still serves" 0 specimen-a pr view --json number
out=$(CMR_FIXTURE='' "$GH" pr view --json number 2>&1); got=$?
if [ "$got" = 4 ]; then pass "no specimen configured"
else fail "no specimen configured" "expected exit 4, got $got"; fi

echo "== H. unbound variable and mutation refuse =="
# shellcheck disable=SC2016
exit_is "unbound after variable" 2 specimen-j api graphql \
  -f 'query=query($cursor:String){repository{pullRequest{reviews(first:1, after:$cursor){nodes{id author{login} submittedAt state body commit{oid}}}}}}'
# Combined query: top-level conversation comments must still be served when
# reviewThreads is also present (two comments( connections). pageInfo on
# pullRequest.comments proves the top-level connection was filled, not only
# nested thread comments.
json_is "combined query serves top-level comments with threads" \
  specimen-j "str(d.get('comments',{}).get('pageInfo',{}).get('hasNextPage'))+' '+str(len(d.get('comments',{}).get('nodes',[])))" \
  "True 2" api graphql \
  -f 'query=query{repository{pullRequest{reviewThreads(first:2){pageInfo{hasNextPage endCursor} nodes{id isResolved path line comments(first:2){nodes{id body author{login} pullRequestReview{id submittedAt}}}}} comments(first:2){pageInfo{hasNextPage endCursor} nodes{id body author{login}}}}}}'
msg_is "mutation refused" 3 "mutation" specimen-a api graphql \
  -f 'query=mutation{closePullRequest(input:{pullRequestId:"x"}){pullRequest{id}}}'

printf '\n%d assertions: %d passed, %d failed\n' "$((PASS + FAIL))" "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ] || exit 1
