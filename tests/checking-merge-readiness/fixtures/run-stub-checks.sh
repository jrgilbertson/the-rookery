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
REPO_ROOT="$(cd "$HERE/../../.." && pwd)"
GH="$HERE/bin/gh"
PRS="$HERE/prs"
PASS=0
FAIL=0
AUTHFAIL=
ISSUEFAIL=
STUB_ENV=

pass() { PASS=$((PASS + 1)); printf 'PASS  %s\n' "$1"; }
fail() { FAIL=$((FAIL + 1)); printf 'FAIL  %s\n     %s\n' "$1" "$2"; }

exit_is() {
  local label=$1 want=$2 spec=$3; shift 3
  local out got
  out=$(env CMR_FIXTURE="$PRS/$spec" ${AUTHFAIL:+CMR_GH_AUTH_FAIL=1} ${ISSUEFAIL:+CMR_ISSUE_VIEW_FAIL=1} ${STUB_ENV:+"$STUB_ENV"} "$GH" "$@" 2>&1); got=$?
  if [ "$got" = "$want" ]; then pass "$label"
  else fail "$label" "expected exit $want, got $got: $(printf '%s' "$out" | head -1)"; fi
}

msg_is() {
  local label=$1 want=$2 needle=$3 spec=$4; shift 4
  local out got
  out=$(env CMR_FIXTURE="$PRS/$spec" ${AUTHFAIL:+CMR_GH_AUTH_FAIL=1} ${ISSUEFAIL:+CMR_ISSUE_VIEW_FAIL=1} ${STUB_ENV:+"$STUB_ENV"} "$GH" "$@" 2>&1); got=$?
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
  if ! raw=$(env CMR_FIXTURE="$PRS/$spec" ${AUTHFAIL:+CMR_GH_AUTH_FAIL=1} ${ISSUEFAIL:+CMR_ISSUE_VIEW_FAIL=1} ${STUB_ENV:+"$STUB_ENV"} "$GH" "$@" 2>&1); then
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
  if ! raw=$(env CMR_FIXTURE="$PRS/$spec" ${AUTHFAIL:+CMR_GH_AUTH_FAIL=1} ${ISSUEFAIL:+CMR_ISSUE_VIEW_FAIL=1} ${STUB_ENV:+"$STUB_ENV"} "$GH" "$@" 2>&1); then
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
# History queries bind repository + pullRequest number like fetch-pr-history.sh.
# shellcheck disable=SC2016
THREADS='query($owner:String!,$name:String!,$n:Int!){repository(owner:$owner,name:$name){pullRequest(number:$n){reviewThreads(first:100){pageInfo{hasNextPage endCursor} nodes{id isResolved path line comments(first:100){nodes{id body author{login} pullRequestReview{id submittedAt}}}}}}}}'
# shellcheck disable=SC2016
REVIEWS='query($owner:String!,$name:String!,$n:Int!){repository(owner:$owner,name:$name){pullRequest(number:$n){reviews(first:100){pageInfo{hasNextPage endCursor} nodes{id author{login} submittedAt state body commit{oid}}}}}}'
# shellcheck disable=SC2016
COMMENTS='query($owner:String!,$name:String!,$n:Int!){repository(owner:$owner,name:$name){pullRequest(number:$n){comments(first:100){pageInfo{hasNextPage endCursor} nodes{id body author{login}}}}}}'
# shellcheck disable=SC2016
EDITS='query($owner:String!,$name:String!,$n:Int!){repository(owner:$owner,name:$name){pullRequest(number:$n){userContentEdits(first:100){pageInfo{hasNextPage endCursor} nodes{editedAt editor{login} diff}}}}}'
# shellcheck disable=SC2016
ISSUE_COMMENTS='query($owner:String!,$name:String!,$issueNumber:Int!){repository(owner:$owner,name:$name){issue(number:$issueNumber){number title body state url comments(first:100){pageInfo{hasNextPage endCursor} nodes{id body author{login} createdAt url}}}}}'

specimen_pr_bind() {
  python3 -c 'import json,sys
d=json.load(open(sys.argv[1]))
repo=d["repo"].removeprefix("github.com/")
owner, name = repo.split("/", 1)
print(owner)
print(name)
print(d["number"])
' "$PRS/$1/forge.json"
}

bind_spec() {
  {
    IFS= read -r BIND_OWNER
    IFS= read -r BIND_NAME
    IFS= read -r BIND_N
  } < <(specimen_pr_bind "$1")
}

echo "== A. serve real fixture content =="
bind_spec specimen-a
json_is "specimen-a: four resolved threads" \
  specimen-a "str(len(d['reviewThreads']['nodes']))+' '+str(all(t['isResolved'] for t in d['reviewThreads']['nodes']))" \
  "4 True" api graphql -f "query=$THREADS" \
  -F "owner=$BIND_OWNER" -F "name=$BIND_NAME" -F "n=$BIND_N"
bind_spec specimen-e
json_is "specimen-e: one unresolved thread" \
  specimen-e "sum(1 for t in d['reviewThreads']['nodes'] if not t['isResolved'])" \
  "1" api graphql -f "query=$THREADS" \
  -F "owner=$BIND_OWNER" -F "name=$BIND_NAME" -F "n=$BIND_N"
bind_spec specimen-j
json_is "specimen-j: page one reports more" \
  specimen-j "str(len(d['reviewThreads']['nodes']))+' '+str(d['reviewThreads']['pageInfo']['hasNextPage'])" \
  "2 True" api graphql -f "query=$THREADS" \
  -F "owner=$BIND_OWNER" -F "name=$BIND_NAME" -F "n=$BIND_N"
# shellcheck disable=SC2016
json_is "specimen-j: page two is the third thread" \
  specimen-j "str(len(d['reviewThreads']['nodes']))+' '+str(d['reviewThreads']['pageInfo']['hasNextPage'])" \
  "1 False" api graphql \
  -f 'query=query($owner:String!,$name:String!,$n:Int!){repository(owner:$owner,name:$name){pullRequest(number:$n){reviewThreads(first:100, after:"reviewThreads:2"){pageInfo{hasNextPage endCursor} nodes{id isResolved path line comments(first:100){nodes{id body author{login} pullRequestReview{id submittedAt}}}}}}}}' \
  -F "owner=$BIND_OWNER" -F "name=$BIND_NAME" -F "n=$BIND_N"
# Variable-bound `after` is what skill runs use.
# shellcheck disable=SC2016
json_is "specimen-j: variable after advances reviews" \
  specimen-j "any('invalidat' in (n.get('body') or '').lower() for n in d['reviews']['nodes'])" \
  "True" api graphql \
  -f 'query=query($owner:String!,$name:String!,$n:Int!,$cursor:String){repository(owner:$owner,name:$name){pullRequest(number:$n){reviews(first:100, after:$cursor){pageInfo{hasNextPage endCursor} nodes{id author{login} submittedAt state body commit{oid}}}}}}' \
  -F "owner=$BIND_OWNER" -F "name=$BIND_NAME" -F "n=$BIND_N" \
  -f 'cursor=reviews:2'
# shellcheck disable=SC2016
json_is "specimen-j: counters request behind comments cursor" \
  specimen-j "any('hit' in (n.get('body') or '') for n in d['comments']['nodes'])" \
  "True" api graphql \
  -f 'query=query($owner:String!,$name:String!,$n:Int!){repository(owner:$owner,name:$name){pullRequest(number:$n){comments(first:100, after:"comments:2"){pageInfo{hasNextPage endCursor} nodes{id body author{login}}}}}}' \
  -F "owner=$BIND_OWNER" -F "name=$BIND_NAME" -F "n=$BIND_N"
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
bind_spec specimen-a
# shellcheck disable=SC2016
exit_is "reviews without commit" 2 specimen-a api graphql \
  -f 'query=query($owner:String!,$name:String!,$n:Int!){repository(owner:$owner,name:$name){pullRequest(number:$n){reviews(first:1){nodes{id author{login} submittedAt state body}}}}}' \
  -F "owner=$BIND_OWNER" -F "name=$BIND_NAME" -F "n=$BIND_N"
# shellcheck disable=SC2016
exit_is "reviews without id" 2 specimen-a api graphql \
  -f 'query=query($owner:String!,$name:String!,$n:Int!){repository(owner:$owner,name:$name){pullRequest(number:$n){reviews(first:1){nodes{author{login} submittedAt state body commit{oid}}}}}}' \
  -F "owner=$BIND_OWNER" -F "name=$BIND_NAME" -F "n=$BIND_N"
# shellcheck disable=SC2016
exit_is "reviews without author" 2 specimen-a api graphql \
  -f 'query=query($owner:String!,$name:String!,$n:Int!){repository(owner:$owner,name:$name){pullRequest(number:$n){reviews(first:1){nodes{id submittedAt state body commit{oid}}}}}}' \
  -F "owner=$BIND_OWNER" -F "name=$BIND_NAME" -F "n=$BIND_N"
# shellcheck disable=SC2016
exit_is "threads without isResolved" 2 specimen-a api graphql \
  -f 'query=query($owner:String!,$name:String!,$n:Int!){repository(owner:$owner,name:$name){pullRequest(number:$n){reviewThreads(first:1){pageInfo{hasNextPage} nodes{id path line comments(first:100){nodes{id body author{login} pullRequestReview{id submittedAt}}}}}}}}' \
  -F "owner=$BIND_OWNER" -F "name=$BIND_NAME" -F "n=$BIND_N"
# shellcheck disable=SC2016
exit_is "threads without pullRequestReview join" 2 specimen-a api graphql \
  -f 'query=query($owner:String!,$name:String!,$n:Int!){repository(owner:$owner,name:$name){pullRequest(number:$n){reviewThreads(first:1){nodes{id isResolved path comments(first:100){nodes{id body author{login}}}}}}}}' \
  -F "owner=$BIND_OWNER" -F "name=$BIND_NAME" -F "n=$BIND_N"
# shellcheck disable=SC2016
exit_is "edits without diff snapshot" 2 specimen-a api graphql \
  -f 'query=query($owner:String!,$name:String!,$n:Int!){repository(owner:$owner,name:$name){pullRequest(number:$n){userContentEdits(first:1){nodes{editedAt editor{login}}}}}}' \
  -F "owner=$BIND_OWNER" -F "name=$BIND_NAME" -F "n=$BIND_N"
# shellcheck disable=SC2016
exit_is "edits without editor" 2 specimen-a api graphql \
  -f 'query=query($owner:String!,$name:String!,$n:Int!){repository(owner:$owner,name:$name){pullRequest(number:$n){userContentEdits(first:1){nodes{editedAt diff}}}}}' \
  -F "owner=$BIND_OWNER" -F "name=$BIND_NAME" -F "n=$BIND_N"
exit_is "skill-shaped threads query accepted" 0 specimen-a api graphql -f "query=$THREADS" \
  -F "owner=$BIND_OWNER" -F "name=$BIND_NAME" -F "n=$BIND_N"
STUB_ENV=GH_HOST=evil.example
msg_is "history GraphQL refuses other GH_HOST" 1 "does not match" specimen-a \
  api graphql -f "query=$REVIEWS" -F "owner=$BIND_OWNER" -F "name=$BIND_NAME" -F "n=$BIND_N"
STUB_ENV=GH_HOST=github.com
msg_is "history GraphQL refuses --hostname= form" 1 "does not match" specimen-a \
  api graphql --hostname=evil.example -f "query=$REVIEWS" \
  -F "owner=$BIND_OWNER" -F "name=$BIND_NAME" -F "n=$BIND_N"
STUB_ENV=
# shellcheck disable=SC2016
msg_is "history GraphQL refuses other repository" 1 "no repository evil/wrong" specimen-a \
  api graphql \
  -f 'query=query($owner:String!,$name:String!,$n:Int!){repository(owner:$owner,name:$name){pullRequest(number:$n){reviews(first:1){nodes{id author{login} submittedAt state body commit{oid}}}}}}' \
  -F owner=evil -F name=wrong -F n=999
msg_is "history GraphQL refuses other pull request number" 1 "no pull request 999" specimen-a \
  api graphql -f "query=$REVIEWS" -F "owner=$BIND_OWNER" -F "name=$BIND_NAME" -F n=999
# Missing-arg messages wrap the field name in backticks.
# shellcheck disable=SC2016
msg_is "history GraphQL refuses pullRequest without number" 2 '`number` is required' specimen-a \
  api graphql \
  -f 'query=query($owner:String!,$name:String!){repository(owner:$owner,name:$name){pullRequest{reviews(first:1){nodes{id author{login} submittedAt state body commit{oid}}}}}}' \
  -F "owner=$BIND_OWNER" -F "name=$BIND_NAME"
# shellcheck disable=SC2016
msg_is "history GraphQL refuses pullRequest without repository arguments" 2 '`owner` is required' specimen-a \
  api graphql \
  -f 'query=query{repository{pullRequest(number:412){reviews(first:1){nodes{id author{login} submittedAt state body commit{oid}}}}}}'
exit_is "skill-shaped edits query accepted" 0 specimen-a api graphql -f "query=$EDITS" \
  -F "owner=$BIND_OWNER" -F "name=$BIND_NAME" -F "n=$BIND_N"
# shellcheck disable=SC2016
exit_is "issue comments without createdAt refused" 2 specimen-a api graphql \
  -f 'query=query($owner:String!,$name:String!,$issueNumber:Int!){repository(owner:$owner,name:$name){issue(number:$issueNumber){number title body state url comments(first:100){pageInfo{hasNextPage endCursor} nodes{id body author{login}}}}}}' \
  -F owner=mapleworks -F name=orderline -F issueNumber=73

echo "== C. every specimen serves the battery-shaped queries =="
for d in "$PRS"/specimen-*; do
  s=$(basename "$d")
  bind_spec "$s"
  exit_is "specimen $s: threads" 0 "$s" api graphql -f "query=$THREADS" \
    -F "owner=$BIND_OWNER" -F "name=$BIND_NAME" -F "n=$BIND_N"
  exit_is "specimen $s: reviews" 0 "$s" api graphql -f "query=$REVIEWS" \
    -F "owner=$BIND_OWNER" -F "name=$BIND_NAME" -F "n=$BIND_N"
  exit_is "specimen $s: comments" 0 "$s" api graphql -f "query=$COMMENTS" \
    -F "owner=$BIND_OWNER" -F "name=$BIND_NAME" -F "n=$BIND_N"
  exit_is "specimen $s: edits" 0 "$s" api graphql -f "query=$EDITS" \
    -F "owner=$BIND_OWNER" -F "name=$BIND_NAME" -F "n=$BIND_N"
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
if python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); a=list(d.get("argv") or []); oid=a[a.index("--match-head-commit")+1] if "--match-head-commit" in a else ""; raise SystemExit(0 if d.get("kind")=="merge" and "--squash" in a and oid=="a91e4f0" and "412" in a and "--repo" in a and a[a.index("--repo")+1]=="mapleworks/orderline" else 1)' "$MERGELOG"
then pass "gated pr merge: argv recorded"
else fail "gated pr merge: argv recorded" "$(cat "$MERGELOG")"
fi
out=$(env CMR_ALLOW_MERGE=1 CMR_MERGE_STATE="$MERGEST" CMR_FIXTURE="$PRS/specimen-a" "$GH" pr view 412 --repo mapleworks/orderline --json state,mergedAt 2>&1); got=$?
if [ "$got" = 0 ] && printf '%s' "$out" | python3 -c 'import json,sys; d=json.load(sys.stdin); raise SystemExit(0 if d.get("state")=="MERGED" and d.get("mergedAt") else 1)'
then pass "gated pr merge: readback MERGED"
else fail "gated pr merge: readback MERGED" "$out"; fi
VLOG=$(mktemp)
out=$(env CMR_ALLOW_MERGE=1 CMR_MERGE_LOG="$VLOG" CMR_MERGE_STATE="$MERGEST" CMR_FIXTURE="$PRS/specimen-a" "$GH" pr view 412 --repo mapleworks/orderline --json state,mergedAt 2>&1); got=$?
if [ "$got" = 0 ] && python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); a=list(d.get("argv") or []); raise SystemExit(0 if d.get("kind")=="view" and "412" in a and "--repo" in a and a[a.index("--repo")+1]=="mapleworks/orderline" else 1)' "$VLOG"
then pass "merged overlay logs certified pr view"
else fail "merged overlay logs certified pr view" "$out $(cat "$VLOG")"
fi
rm -f "$VLOG"
out=$(env CMR_ALLOW_MERGE=1 CMR_MERGE_LOG="$MERGELOG" CMR_MERGE_STATE="$MERGEST" CMR_FIXTURE="$PRS/specimen-a" "$GH" pr merge 412 --repo mapleworks/orderline --squash --match-head-commit a91e4f0 2>&1); got=$?
if [ "$got" = 1 ] && printf '%s' "$out" | grep -q "already merged"
then pass "gated pr merge: already-merged refuse"
else fail "gated pr merge: already-merged refuse" "$out"; fi
if python3 -c 'import json,sys; n=sum(1 for l in open(sys.argv[1]) if l.strip() and json.loads(l).get("kind")=="merge"); raise SystemExit(0 if n==2 else 1)' "$MERGELOG"
then pass "gated pr merge: second attempt logged"
else fail "gated pr merge: second attempt logged" "$(cat "$MERGELOG")"
fi
FLOG=$(mktemp)
out=$(env CMR_ALLOW_MERGE=1 CMR_MERGE_RESULT=failed CMR_MERGE_LOG="$FLOG" CMR_FIXTURE="$PRS/specimen-a" "$GH" pr merge 412 --repo mapleworks/orderline --squash --match-head-commit a91e4f0 2>&1); got=$?
out2=$(env CMR_ALLOW_MERGE=1 CMR_MERGE_LOG="$FLOG" CMR_FIXTURE="$PRS/specimen-a" "$GH" pr view 412 --repo mapleworks/orderline --json state,mergedAt 2>&1); got2=$?
if [ "$got" != 0 ] && [ "$got2" = 0 ] && python3 -c 'import json,sys; rows=[json.loads(l) for l in open(sys.argv[1]) if l.strip()]; raise SystemExit(0 if any(r.get("kind")=="merge" for r in rows) and any(r.get("kind")=="view" and "412" in (r.get("argv") or []) for r in rows) else 1)' "$FLOG"
then pass "failed merge still logs certified pr view"
else fail "failed merge still logs certified pr view" "$out $out2 $(cat "$FLOG")"
fi
rm -f "$FLOG"
PLOG=$(mktemp)
out=$(env GH_PROMPT_DISABLED=1 CMR_ALLOW_MERGE=1 CMR_MERGE_LOG="$PLOG" CMR_FIXTURE="$PRS/specimen-a" "$GH" pr merge 412 --repo mapleworks/orderline --squash --match-head-commit a91e4f0 2>&1); got=$?
if [ "$got" = 0 ] && python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); raise SystemExit(0 if d.get("promptDisabled")=="1" else 1)' "$PLOG"
then pass "gated pr merge: promptDisabled recorded"
else fail "gated pr merge: promptDisabled recorded" "$out $(cat "$PLOG")"
fi
rm -f "$PLOG"
out=$(env CMR_ALLOW_MERGE=1 CMR_FIXTURE="$PRS/specimen-a" "$GH" pr merge 999 412 --repo mapleworks/orderline --squash --match-head-commit a91e4f0 2>&1); got=$?
if [ "$got" = 2 ] && printf '%s' "$out" | grep -q "at most 1"
then pass "gated pr merge refuses second selector"
else fail "gated pr merge refuses second selector" "$out"; fi
# shellcheck disable=SC2016
ELIG='query($owner:String!,$name:String!){repository(owner:$owner,name:$name){mergeCommitAllowed squashMergeAllowed rebaseMergeAllowed viewerDefaultMergeMethod}}'
# shellcheck disable=SC2016
PROT='query($owner:String!,$name:String!){repository(owner:$owner,name:$name){branchProtectionRules(first:1){nodes{pattern requiresConversationResolution}}}}'
msg_is "eligibility GraphQL refuses other repository" 1 "no repository evil/wrong" specimen-a \
  api graphql -f "query=$ELIG" -F owner=evil -F name=wrong
exit_is "eligibility GraphQL matching repository" 0 specimen-a \
  api graphql -f "query=$ELIG" -F owner=mapleworks -F name=orderline
msg_is "branchProtectionRules GraphQL refuses other repository" 1 "no repository evil/wrong" specimen-a \
  api graphql -f "query=$PROT" -F owner=evil -F name=wrong
exit_is "branchProtectionRules GraphQL matching repository" 0 specimen-a \
  api graphql -f "query=$PROT" -F owner=mapleworks -F name=orderline
msg_is "eligibility GraphQL requires repository arguments" 2 "owner" specimen-a \
  api graphql -f 'query=query{repository{mergeCommitAllowed squashMergeAllowed rebaseMergeAllowed viewerDefaultMergeMethod}}'
msg_is "branchProtectionRules GraphQL requires repository arguments" 2 "owner" specimen-a \
  api graphql -f 'query=query{repository{branchProtectionRules(first:1){nodes{pattern requiresConversationResolution}}}}'
STUB_ENV=GH_HOST=evil.example
msg_is "eligibility GraphQL refuses other GH_HOST" 1 "does not match" specimen-a \
  api graphql -f "query=$ELIG" -F owner=mapleworks -F name=orderline
STUB_ENV=
GHE=$(mktemp -d)
cp -R "$PRS/specimen-a/." "$GHE/"
python3 -c 'import json,sys; p=sys.argv[1]+"/forge.json"; d=json.load(open(p)); d["host"]="ghe.example"; json.dump(d, open(p,"w"))' "$GHE"
out=$(env CMR_FIXTURE="$GHE" "$GH" api graphql -f "query=$ELIG" -F owner=mapleworks -F name=orderline 2>&1); got=$?
if [ "$got" = 1 ] && printf '%s' "$out" | grep -q "does not match"
then pass "eligibility GraphQL enterprise host without --hostname"
else fail "eligibility GraphQL enterprise host without --hostname" "$out"; fi
out=$(env CMR_FIXTURE="$GHE" "$GH" api graphql --hostname ghe.example -f "query=$ELIG" -F owner=mapleworks -F name=orderline 2>&1); got=$?
if [ "$got" = 0 ]
then pass "eligibility GraphQL enterprise host with --hostname"
else fail "eligibility GraphQL enterprise host with --hostname" "$out"; fi
rm -rf "$GHE"
# shellcheck disable=SC2016
QUEUE='query($owner:String!,$name:String!,$n:Int!){repository(owner:$owner,name:$name){pullRequest(number:$n){isMergeQueueEnabled}}}'
msg_is "isMergeQueueEnabled refuses other PR number" 1 "no pull request 999" specimen-a \
  api graphql -f "query=$QUEUE" -F owner=mapleworks -F name=orderline -F n=999
# shellcheck disable=SC2016
msg_is "isMergeQueueEnabled requires pullRequest number" 2 "number" specimen-a \
  api graphql \
  -f 'query=query($owner:String!,$name:String!){repository(owner:$owner,name:$name){isMergeQueueEnabled}}' \
  -F owner=mapleworks -F name=orderline
out=$(env CMR_ALLOW_MERGE=1 CMR_FIXTURE="$PRS/specimen-a" "$GH" pr merge 412 --repo mapleworks/orderline --squash --admin --match-head-commit a91e4f0 2>&1); got=$?
if [ "$got" = 3 ] && printf '%s' "$out" | grep -q "refuses --admin"
then pass "gated pr merge refuses --admin"
else fail "gated pr merge refuses --admin" "$out"; fi
out=$(env CMR_ALLOW_MERGE=1 CMR_FIXTURE="$PRS/specimen-a" "$GH" pr merge 412 --squash --match-head-commit a91e4f0 2>&1); got=$?
if [ "$got" = 2 ] && printf '%s' "$out" | grep -q "requires a PR number"
then pass "gated pr merge without --repo"
else fail "gated pr merge without --repo" "$out"; fi
out=$(env CMR_ALLOW_MERGE=1 CMR_FIXTURE="$PRS/specimen-a" "$GH" pr merge 412 --repo mapleworks --squash --match-head-commit a91e4f0 2>&1); got=$?
if [ "$got" = 1 ] && printf '%s' "$out" | grep -q "mapleworks"
then pass "gated pr merge owner-only --repo"
else fail "gated pr merge owner-only --repo" "$out"; fi
out=$(env CMR_ALLOW_MERGE=1 CMR_FIXTURE="$PRS/specimen-a" "$GH" pr merge --repo mapleworks/orderline --squash --match-head-commit a91e4f0 2>&1); got=$?
if [ "$got" = 2 ] && printf '%s' "$out" | grep -q "requires a PR number"
then pass "gated pr merge without number"
else fail "gated pr merge without number" "$out"; fi
out=$(env CMR_ALLOW_MERGE=1 CMR_FIXTURE="$PRS/specimen-a" "$GH" pr merge 412 --repo mapleworks/orderline --rebase --match-head-commit a91e4f0 2>&1); got=$?
if [ "$got" = 1 ] && printf '%s' "$out" | grep -q "rebaseMergeAllowed"
then pass "gated pr merge refuses --rebase"
else fail "gated pr merge refuses --rebase" "$out"; fi
out=$(env CMR_ALLOW_MERGE=1 GH_HOST=evil.example CMR_FIXTURE="$PRS/specimen-a" "$GH" pr merge 412 --repo mapleworks/orderline --squash --match-head-commit a91e4f0 2>&1); got=$?
if [ "$got" = 1 ] && printf '%s' "$out" | grep -q "does not match"
then pass "gated pr merge refuses other GH_HOST"
else fail "gated pr merge refuses other GH_HOST" "$out"; fi
# shellcheck disable=SC2016
msg_is "graphql refuses positional query=" 2 "no query= field" specimen-a \
  api graphql 'query=query($owner:String!,$name:String!){repository(owner:$owner,name:$name){mergeCommitAllowed}}'
out=$(env CMR_ALLOW_MERGE=1 CMR_FIXTURE="$PRS/specimen-a" "$GH" pr merge 412 --repo mapleworks/orderline --squash --match-head-commit a91e4f0 --subject "x" 2>&1); got=$?
if [ "$got" = 3 ] && printf '%s' "$out" | grep -q "refuses extra token"
then pass "gated pr merge refuses extra token"
else fail "gated pr merge refuses extra token" "$out"; fi
out=$(env CMR_ALLOW_MERGE=1 CMR_FIXTURE="$PRS/specimen-a" "$GH" pr merge 412 --repo evil.example/mapleworks/orderline --squash --match-head-commit a91e4f0 2>&1); got=$?
if [ "$got" = 1 ] && printf '%s' "$out" | grep -q "does not match"
then pass "gated pr merge refuses other host"
else fail "gated pr merge refuses other host" "$out"; fi
out=$(env CMR_ALLOW_MERGE=1 CMR_MERGE_STATE="$MERGEST" CMR_FIXTURE="$PRS/specimen-a" "$GH" pr view --json state,mergedAt 2>&1); got=$?
if [ "$got" = 2 ] && printf '%s' "$out" | grep -q "certified"
then pass "merged overlay refuses selectorless pr view"
else fail "merged overlay refuses selectorless pr view" "$out"; fi
out=$(env CMR_ALLOW_MERGE=1 CMR_MERGE_STATE="$MERGEST" CMR_FIXTURE="$PRS/specimen-a" "$GH" pr view 412 --repo evil.example/mapleworks/orderline --json state,mergedAt 2>&1); got=$?
if [ "$got" = 1 ] && printf '%s' "$out" | grep -q "does not match"
then pass "merged overlay refuses other host"
else fail "merged overlay refuses other host" "$out"; fi
ALREADY=$(mktemp)
out=$(env CMR_ALLOW_MERGE=1 CMR_MERGE_RESULT=already_merged CMR_MERGE_STATE="$ALREADY" CMR_FIXTURE="$PRS/specimen-a" "$GH" pr merge 412 --repo mapleworks/orderline --squash --match-head-commit a91e4f0 2>&1); got=$?
if [ "$got" = 1 ] && printf '%s' "$out" | grep -q "already merged"
then pass "CMR_MERGE_RESULT=already_merged refuses"
else fail "CMR_MERGE_RESULT=already_merged refuses" "$out"; fi
out=$(env CMR_ALLOW_MERGE=1 CMR_MERGE_STATE="$ALREADY" CMR_FIXTURE="$PRS/specimen-a" "$GH" pr view 412 --repo mapleworks/orderline --json state,mergedAt 2>&1); got=$?
if [ "$got" = 0 ] && printf '%s' "$out" | python3 -c 'import json,sys; d=json.load(sys.stdin); raise SystemExit(0 if d.get("state")=="MERGED" and d.get("mergedAt") else 1)'
then pass "already_merged readback MERGED"
else fail "already_merged readback MERGED" "$out"; fi
HLOG=$(mktemp)
out=$(env CMR_ALLOW_MERGE=1 CMR_MERGE_LOG="$HLOG" CMR_FIXTURE="$PRS/specimen-h" "$GH" pr merge 205 --repo mapleworks/inbox-svc --squash --match-head-commit 4c1b8e2 2>&1); got=$?
if [ "$got" != 0 ] && python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); raise SystemExit(0 if d.get("argv") else 1)' "$HLOG"
then pass "gated pr merge logs before eligibility refuse"
else fail "gated pr merge logs before eligibility refuse" "$out $(cat "$HLOG" 2>/dev/null)"
fi
rm -f "$MERGELOG" "$MERGEST" "$ALREADY" "$HLOG" "$PLOG"
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
msg_is "URL from another host" 1 "does not match" specimen-a \
  pr view https://evil.example/mapleworks/orderline/pull/412 --json number
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
msg_is "rules refuse other repository" 1 "no repository evil/wrong" specimen-a \
  api repos/evil/wrong/rules/branches/main
msg_is "rules refuse other host" 1 "does not match" specimen-a \
  api --hostname evil.example repos/mapleworks/orderline/rules/branches/main
msg_is "REST repo GET is outside the set" 3 "are served" specimen-a \
  api repos/mapleworks/orderline
msg_is "REST repo refuses DELETE" 3 "DELETE is a write" specimen-a \
  api -X DELETE repos/mapleworks/orderline
msg_is "REST rules refuse PATCH" 3 "PATCH is a write" specimen-a \
  api --method PATCH repos/mapleworks/orderline/rules/branches/main
msg_is "REST rules refuse implicit POST from -f" 3 "POST is a write" specimen-a \
  api repos/mapleworks/orderline/rules/branches/main -f accidental=value
msg_is "REST rules refuse attached -f POST" 3 "POST is a write" specimen-a \
  api repos/mapleworks/orderline/rules/branches/main -faccidental=value
msg_is "REST rules refuse attached --field= POST" 3 "POST is a write" specimen-a \
  api repos/mapleworks/orderline/rules/branches/main --field=accidental=value

echo "== G. unauthenticated forge =="
AUTHFAIL=1
exit_is "auth-fail pr view" 4 specimen-a pr view --json number
exit_is "auth-fail issue view" 4 specimen-a issue view 73 --repo mapleworks/orderline --json number
bind_spec specimen-a
exit_is "auth-fail graphql" 4 specimen-a api graphql -f "query=$REVIEWS" \
  -F "owner=$BIND_OWNER" -F "name=$BIND_NAME" -F "n=$BIND_N"
exit_is "auth-fail status" 1 specimen-a auth status
AUTHFAIL=
exit_is "authenticated still serves" 0 specimen-a pr view --json number
out=$(CMR_FIXTURE='' "$GH" pr view --json number 2>&1); got=$?
if [ "$got" = 4 ]; then pass "no specimen configured"
else fail "no specimen configured" "expected exit 4, got $got"; fi

echo "== H. unbound variable and mutation refuse =="
bind_spec specimen-j
# shellcheck disable=SC2016
exit_is "unbound after variable" 2 specimen-j api graphql \
  -f 'query=query($owner:String!,$name:String!,$n:Int!,$cursor:String){repository(owner:$owner,name:$name){pullRequest(number:$n){reviews(first:1, after:$cursor){nodes{id author{login} submittedAt state body commit{oid}}}}}}' \
  -F "owner=$BIND_OWNER" -F "name=$BIND_NAME" -F "n=$BIND_N"
# Combined query: top-level conversation comments must still be served when
# reviewThreads is also present (two comments( connections). pageInfo on
# pullRequest.comments proves the top-level connection was filled, not only
# nested thread comments.
# shellcheck disable=SC2016
json_is "combined query serves top-level comments with threads" \
  specimen-j "str(d.get('comments',{}).get('pageInfo',{}).get('hasNextPage'))+' '+str(len(d.get('comments',{}).get('nodes',[])))" \
  "True 2" api graphql \
  -f 'query=query($owner:String!,$name:String!,$n:Int!){repository(owner:$owner,name:$name){pullRequest(number:$n){reviewThreads(first:2){pageInfo{hasNextPage endCursor} nodes{id isResolved path line comments(first:2){nodes{id body author{login} pullRequestReview{id submittedAt}}}}} comments(first:2){pageInfo{hasNextPage endCursor} nodes{id body author{login}}}}}}' \
  -F "owner=$BIND_OWNER" -F "name=$BIND_NAME" -F "n=$BIND_N"
msg_is "mutation refused" 3 "mutation" specimen-a api graphql \
  -f 'query=mutation{closePullRequest(input:{pullRequestId:"x"}){pullRequest{id}}}'

echo "== I. unattended agent mode stays structurally assessment-only =="
AGENT_REF="$REPO_ROOT/skills/checking-merge-readiness/references/agent-mode.md"
AGENT_SKILL="$REPO_ROOT/skills/checking-merge-readiness/SKILL.md"
AGENT_CASE="$REPO_ROOT/tests/checking-merge-readiness/cases/agent-mode-never-merges.md"
if [ -f "$AGENT_REF" ] && [ -f "$AGENT_SKILL" ]; then
  pass "agent mode: dedicated reference exists"
else
  fail "agent mode: dedicated reference exists" "missing agent-mode reference or skill"
fi
for needle in \
  'mode:agent' \
  'repository' \
  'pull request number' \
  'current full head OID' \
  'recommendation' \
  'caps' \
  'process-only findings' \
  'material findings' \
  'actionable in-slice findings' \
  'protected-path policy' \
  'policy revision' \
  'full host/owner/name' \
  'history fingerprint' \
  'live merge/check state' \
  'linked-issue digests' \
  'rebuild from the new snapshot' \
  'return UNKNOWN'
do
  if [ -f "$AGENT_REF" ] && grep -Fq "$needle" "$AGENT_REF"; then
    pass "agent mode: names $needle"
  else
    fail "agent mode: names $needle" "agent-mode reference omitted required contract"
  fi
done
if [ -f "$AGENT_REF" ] && ! grep -Eqi 'merge-execution\.md|Proceed to merge|gh pr merge|decision menu' "$AGENT_REF"; then
  pass "agent mode: reference has no merge route"
else
  fail "agent mode: reference has no merge route" "agent-mode reference exposes an interactive or merge path"
fi
if [ -f "$AGENT_SKILL" ] && python3 - "$AGENT_SKILL" <<'PY'
import sys

text = open(sys.argv[1]).read()
start = text.find("## Unattended agent mode")
end = text.find("## Workflow", start)
section = text[start:end] if start >= 0 and end > start else ""
required = ["mode:agent", "agent-mode.md", "current full head OID"]
forbidden = ["merge-execution.md", "Proceed to merge", "gh pr merge", "decision menu"]
raise SystemExit(0 if section and all(item in section for item in required)
                 and not any(item in section for item in forbidden) else 1)
PY
then pass "agent mode: routes before interactive workflow"
else fail "agent mode: routes before interactive workflow" "agent-mode route is missing or reaches interactive merge handling"
fi
if [ -f "$AGENT_CASE" ] && grep -Fq 'review state changes without head movement' "$AGENT_CASE" \
  && grep -Fq 'protected-path policy and revision' "$AGENT_CASE"; then
  pass "agent mode: behavioral case covers protected policy and review-only movement"
else
  fail "agent mode: behavioral case covers protected policy and review-only movement" "agent-mode case omitted a new subject or final-stability behavior"
fi
agent_case_has_full_oid() {
  python3 - "$1" "$(git -C "$REPO_ROOT" rev-parse --show-object-format)" <<'PY'
import re
import sys

text = open(sys.argv[1]).read()
length = {"sha1": 40, "sha256": 64}.get(sys.argv[2])
matches = re.findall(r"current full head OID\s*\n> `([0-9a-fA-F]+)`", text)
raise SystemExit(0 if length and len(matches) == 1 and len(matches[0]) == length else 1)
PY
}
if [ -f "$AGENT_CASE" ] && agent_case_has_full_oid "$AGENT_CASE"; then
  pass "agent mode: behavioral case binds a full repository-format OID"
else
  fail "agent mode: behavioral case binds a full repository-format OID" "agent-mode case omitted a full repository-format OID"
fi
AGENT_CASE_COPY_DIR=$(mktemp -d)
AGENT_CASE_COPY="$AGENT_CASE_COPY_DIR/agent-mode-never-merges.md"
cp "$AGENT_CASE" "$AGENT_CASE_COPY"
python3 - "$AGENT_CASE_COPY" <<'PY'
import re
import sys

path = sys.argv[1]
text = open(path).read()
match = re.search(r"current full head OID\s*\n> `([0-9a-fA-F]+)`", text)
if not match:
    raise SystemExit(1)
text = text[:match.start(1)] + match.group(1)[:-1] + text[match.end(1):]
open(path, "w").write(text)
PY
if ! agent_case_has_full_oid "$AGENT_CASE_COPY"; then
  pass "agent mode: shortened OID mutation fails"
else
  fail "agent mode: shortened OID mutation fails" "shortened OID was accepted"
fi
rm -rf "$AGENT_CASE_COPY_DIR"

echo "== J. Worker delivery exactness =="
GARDENER_SKILL="$REPO_ROOT/skills/repo-gardener/SKILL.md"
RECONCILIATION="$REPO_ROOT/skills/repo-gardener/references/reconciliation.md"
for source in "$GARDENER_SKILL" "$RECONCILIATION"; do
  label=$(basename "$source")
  source_text=$(tr '\n' ' ' < "$source" 2>/dev/null | tr -s ' ')
  for needle in \
    'uncertain PR-create response' \
    'exact repository and Worker branch' \
    'exact host/repository, head repository, Worker branch, and authorized full head OID' \
    'exactly one OPEN pull request' \
    'exactly one matching PR' \
    'Zero, multiple, unavailable, stale, closed, or mismatched' \
    'UNKNOWN' \
    'saved pushed state' \
    'never retry, guess, adopt, or blindly duplicate' \
    'never receives tracker or delivery credentials' \
    'authorized shipping broker' \
    'exact repository, branch, and full head' \
    'immediately before' \
    'post-read'
  do
    if [ -f "$source" ] && [[ "$source_text" == *"$needle"* ]]; then
      pass "delivery contract: $label names $needle"
    else
      fail "delivery contract: $label names $needle" "missing exact F1/F2 boundary"
    fi
  done
done

printf '\n%d assertions: %d passed, %d failed\n' "$((PASS + FAIL))" "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ] || exit 1
