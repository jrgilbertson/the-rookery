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
# Variable-bound after (what real skill runs use) — the footgun that forced the greenfield cursor fix.
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
out=$(env GH_HOST=evil.example CMR_FIXTURE="$PRS/specimen-a" "$GH" api graphql -f "query=$REVIEWS" -F "owner=$BIND_OWNER" -F "name=$BIND_NAME" -F "n=$BIND_N" 2>&1); got=$?
if [ "$got" = 1 ] && printf '%s' "$out" | grep -q "does not match"
then pass "history GraphQL refuses other GH_HOST"
else fail "history GraphQL refuses other GH_HOST" "$out"; fi
out=$(env GH_HOST=github.com CMR_FIXTURE="$PRS/specimen-a" "$GH" api graphql --hostname=evil.example -f "query=$REVIEWS" -F "owner=$BIND_OWNER" -F "name=$BIND_NAME" -F "n=$BIND_N" 2>&1); got=$?
if [ "$got" = 1 ] && printf '%s' "$out" | grep -q "does not match"
then pass "history GraphQL refuses --hostname= form"
else fail "history GraphQL refuses --hostname= form" "$out"; fi
# shellcheck disable=SC2016
out=$(env CMR_FIXTURE="$PRS/specimen-a" "$GH" api graphql -f 'query=query($owner:String!,$name:String!,$n:Int!){repository(owner:$owner,name:$name){pullRequest(number:$n){reviews(first:1){nodes{id author{login} submittedAt state body commit{oid}}}}}}' -F owner=evil -F name=wrong -F n=999 2>&1); got=$?
if [ "$got" = 1 ] && printf '%s' "$out" | grep -q "no repository evil/wrong"
then pass "history GraphQL refuses other repository"
else fail "history GraphQL refuses other repository" "$out"; fi
# shellcheck disable=SC2016
out=$(env CMR_FIXTURE="$PRS/specimen-a" "$GH" api graphql -f "query=$REVIEWS" -F "owner=$BIND_OWNER" -F "name=$BIND_NAME" -F n=999 2>&1); got=$?
if [ "$got" = 1 ] && printf '%s' "$out" | grep -q "no pull request 999"
then pass "history GraphQL refuses other pull request number"
else fail "history GraphQL refuses other pull request number" "$out"; fi
# shellcheck disable=SC2016
out=$(env CMR_FIXTURE="$PRS/specimen-a" "$GH" api graphql -f 'query=query($owner:String!,$name:String!){repository(owner:$owner,name:$name){pullRequest{reviews(first:1){nodes{id author{login} submittedAt state body commit{oid}}}}}}' -F "owner=$BIND_OWNER" -F "name=$BIND_NAME" 2>&1); got=$?
# The stub's missing-arg message wraps the field name in backticks.
# shellcheck disable=SC2016
if [ "$got" = 2 ] && printf '%s' "$out" | grep -q '`number` is required'
then pass "history GraphQL refuses pullRequest without number"
else fail "history GraphQL refuses pullRequest without number" "$out"; fi
out=$(env CMR_FIXTURE="$PRS/specimen-a" "$GH" api graphql -f 'query=query{repository{pullRequest(number:412){reviews(first:1){nodes{id author{login} submittedAt state body commit{oid}}}}}}' 2>&1); got=$?
# The stub's missing-arg message wraps the field name in backticks.
# shellcheck disable=SC2016
if [ "$got" = 2 ] && printf '%s' "$out" | grep -q '`owner` is required'
then pass "history GraphQL refuses pullRequest without repository arguments"
else fail "history GraphQL refuses pullRequest without repository arguments" "$out"; fi
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
out=$(env CMR_FIXTURE="$PRS/specimen-a" "$GH" api graphql -f "query=$ELIG" -F owner=evil -F name=wrong 2>&1); got=$?
if [ "$got" = 1 ] && printf '%s' "$out" | grep -q "no repository evil/wrong"
then pass "eligibility GraphQL refuses other repository"
else fail "eligibility GraphQL refuses other repository" "$out"; fi
out=$(env CMR_FIXTURE="$PRS/specimen-a" "$GH" api graphql -f "query=$ELIG" -F owner=mapleworks -F name=orderline 2>&1); got=$?
if [ "$got" = 0 ]
then pass "eligibility GraphQL matching repository"
else fail "eligibility GraphQL matching repository" "$out"; fi
out=$(env CMR_FIXTURE="$PRS/specimen-a" "$GH" api graphql -f "query=$PROT" -F owner=evil -F name=wrong 2>&1); got=$?
if [ "$got" = 1 ] && printf '%s' "$out" | grep -q "no repository evil/wrong"
then pass "branchProtectionRules GraphQL refuses other repository"
else fail "branchProtectionRules GraphQL refuses other repository" "$out"; fi
out=$(env CMR_FIXTURE="$PRS/specimen-a" "$GH" api graphql -f "query=$PROT" -F owner=mapleworks -F name=orderline 2>&1); got=$?
if [ "$got" = 0 ]
then pass "branchProtectionRules GraphQL matching repository"
else fail "branchProtectionRules GraphQL matching repository" "$out"; fi
out=$(env CMR_FIXTURE="$PRS/specimen-a" "$GH" api graphql -f 'query=query{repository{mergeCommitAllowed squashMergeAllowed rebaseMergeAllowed viewerDefaultMergeMethod}}' 2>&1); got=$?
if [ "$got" = 2 ] && printf '%s' "$out" | grep -q "owner"
then pass "eligibility GraphQL requires repository arguments"
else fail "eligibility GraphQL requires repository arguments" "$out"; fi
out=$(env CMR_FIXTURE="$PRS/specimen-a" "$GH" api graphql -f 'query=query{repository{branchProtectionRules(first:1){nodes{pattern requiresConversationResolution}}}}' 2>&1); got=$?
if [ "$got" = 2 ] && printf '%s' "$out" | grep -q "owner"
then pass "branchProtectionRules GraphQL requires repository arguments"
else fail "branchProtectionRules GraphQL requires repository arguments" "$out"; fi
out=$(env GH_HOST=evil.example CMR_FIXTURE="$PRS/specimen-a" "$GH" api graphql -f "query=$ELIG" -F owner=mapleworks -F name=orderline 2>&1); got=$?
if [ "$got" = 1 ] && printf '%s' "$out" | grep -q "does not match"
then pass "eligibility GraphQL refuses other GH_HOST"
else fail "eligibility GraphQL refuses other GH_HOST" "$out"; fi
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
out=$(env CMR_FIXTURE="$PRS/specimen-a" "$GH" api graphql -f "query=$QUEUE" -F owner=mapleworks -F name=orderline -F n=999 2>&1); got=$?
if [ "$got" = 1 ] && printf '%s' "$out" | grep -q "no pull request 999"
then pass "isMergeQueueEnabled refuses other PR number"
else fail "isMergeQueueEnabled refuses other PR number" "$out"; fi
# shellcheck disable=SC2016
out=$(env CMR_FIXTURE="$PRS/specimen-a" "$GH" api graphql -f 'query=query($owner:String!,$name:String!){repository(owner:$owner,name:$name){isMergeQueueEnabled}}' -F owner=mapleworks -F name=orderline 2>&1); got=$?
if [ "$got" = 2 ] && printf '%s' "$out" | grep -q "number"
then pass "isMergeQueueEnabled requires pullRequest number"
else fail "isMergeQueueEnabled requires pullRequest number" "$out"; fi
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
out=$(env CMR_ALLOW_MERGE=1 CMR_FIXTURE="$PRS/specimen-a" "$GH" pr merge 412 --repo mapleworks/orderline --squash --match-head-commit a91e4f0 --subject "x" 2>&1); got=$?
if [ "$got" = 3 ] && printf '%s' "$out" | grep -q "refuses extra token"
then pass "gated pr merge refuses --subject"
else fail "gated pr merge refuses --subject" "$out"; fi
out=$(env CMR_ALLOW_MERGE=1 CMR_FIXTURE="$PRS/specimen-a" "$GH" pr merge 412 --repo mapleworks/orderline --squash --match-head-commit a91e4f0 --body "x" 2>&1); got=$?
if [ "$got" = 3 ] && printf '%s' "$out" | grep -q "refuses extra token"
then pass "gated pr merge refuses --body"
else fail "gated pr merge refuses --body" "$out"; fi
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
out=$(env CMR_FIXTURE="$PRS/specimen-a" "$GH" api --hostname evil.example repos/mapleworks/orderline/rules/branches/main 2>&1); got=$?
if [ "$got" = 1 ] && printf '%s' "$out" | grep -q "does not match"
then pass "rules refuse other host"
else fail "rules refuse other host" "$out"; fi
out=$(env CMR_FIXTURE="$PRS/specimen-a" "$GH" api repos/mapleworks/orderline 2>&1); got=$?
if [ "$got" = 0 ] && printf '%s' "$out" | python3 -c 'import json,sys; d=json.load(sys.stdin); raise SystemExit(0 if d.get("allow_squash_merge") is True and d.get("allow_merge_commit") is True and d.get("allow_rebase_merge") is False else 1)'
then pass "REST repo allow_* methods"
else fail "REST repo allow_* methods" "$out"; fi
msg_is "REST repo refuses other repository" 1 "no repository evil/wrong" specimen-a \
  api repos/evil/wrong
out=$(env CMR_FIXTURE="$PRS/specimen-a" "$GH" api -X GET repos/mapleworks/orderline 2>&1); got=$?
if [ "$got" = 0 ]
then pass "REST repo allows explicit GET"
else fail "REST repo allows explicit GET" "$out"; fi
out=$(env CMR_FIXTURE="$PRS/specimen-a" "$GH" api -X DELETE repos/mapleworks/orderline 2>&1); got=$?
if [ "$got" = 3 ] && printf '%s' "$out" | grep -q "DELETE is a write"
then pass "REST repo refuses DELETE"
else fail "REST repo refuses DELETE" "$out"; fi
out=$(env CMR_FIXTURE="$PRS/specimen-a" "$GH" api --method PATCH repos/mapleworks/orderline/rules/branches/main 2>&1); got=$?
if [ "$got" = 3 ] && printf '%s' "$out" | grep -q "PATCH is a write"
then pass "REST rules refuse PATCH"
else fail "REST rules refuse PATCH" "$out"; fi

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

printf '\n%d assertions: %d passed, %d failed\n' "$((PASS + FAIL))" "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ] || exit 1
