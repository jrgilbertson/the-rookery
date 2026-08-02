#!/usr/bin/env bash
# Assert the fixture `gh` stub's contract, state by state.
#
# The stub's purpose is to be no more permissive than real `gh`, so that a
# malformed fetch cannot pass the behavioural battery and then fail against
# GitHub. That guarantee is only worth what a test can falsify: the battery
# itself cannot see over-serving or under-pagination unless a run happens to
# exercise them, so the stub carries its own assertions here.
#
# Every assertion pins an exact exit code, and where the exit code alone would
# not distinguish right from wrong, an exact value oracle as well.
#
#   bash tests/checking-merge-readiness/fixtures/run-stub-checks.sh

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GH="$HERE/bin/gh"
PRS="$HERE/prs"
PASS=0
FAIL=0
AUTHFAIL=

pass() { PASS=$((PASS + 1)); printf 'PASS  %s\n' "$1"; }
fail() { FAIL=$((FAIL + 1)); printf 'FAIL  %s\n     %s\n' "$1" "$2"; }

# exit_is <label> <expected-exit> <specimen> <args...>
exit_is() {
  local label=$1 want=$2 spec=$3; shift 3
  local out got
  out=$(env CMR_FIXTURE="$PRS/$spec" ${AUTHFAIL:+CMR_GH_AUTH_FAIL=1} "$GH" "$@" 2>&1); got=$?
  if [ "$got" = "$want" ]; then pass "$label"
  else fail "$label" "expected exit $want, got $got: $(printf '%s' "$out" | head -1)"; fi
}

# json_is <label> <specimen> <python-expr-over-d> <expected> <args...>
# The expression reads the parsed response as `d` and prints one value.
json_is() {
  local label=$1 spec=$2 expr=$3 want=$4; shift 4
  local raw got
  raw=$(env CMR_FIXTURE="$PRS/$spec" ${AUTHFAIL:+CMR_GH_AUTH_FAIL=1} "$GH" "$@" 2>&1)
  if [ $? -ne 0 ]; then
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

# A query shaped the way the skill's fetch contract says to ask.
THREADS='query{repository{pullRequest{reviewThreads(first:100){pageInfo{hasNextPage endCursor} nodes{isResolved path comments(first:100){nodes{body author{login} pullRequestReview{submittedAt}}}}}}}}'
REVIEWS='query{repository{pullRequest{reviews(first:100){pageInfo{hasNextPage endCursor} nodes{submittedAt state body commit{oid}}}}}}'
COMMENTS='query{repository{pullRequest{comments(first:100){pageInfo{hasNextPage endCursor} nodes{body author{login}}}}}}'
EDITS='query{repository{pullRequest{userContentEdits(first:100){pageInfo{hasNextPage endCursor} nodes{editedAt}}}}}'

echo "== A. no over-serve =="
json_is "overserve: reviews node carries only the four selected fields" \
  specimen-a "sorted(d['reviews']['nodes'][0].keys())" \
  "['body', 'commit', 'state', 'submittedAt']" api graphql -f "query=$REVIEWS"
json_is "overserve: reviews node omits author the query never asked for" \
  specimen-a "'author' in d['reviews']['nodes'][0]" "False" api graphql -f "query=$REVIEWS"
json_is "overserve: connection carries only nodes and pageInfo" \
  specimen-a "sorted(d['reviews'].keys())" "['nodes', 'pageInfo']" api graphql -f "query=$REVIEWS"
json_is "overserve: thread node omits unselected line" \
  specimen-a "'line' in d['reviewThreads']['nodes'][0]" "False" api graphql -f "query=$THREADS"
json_is "overserve: author projects to exactly the selected subfield" \
  specimen-a "sorted(d['reviewThreads']['nodes'][0]['comments']['nodes'][0]['author'].keys())" \
  "['login']" api graphql -f "query=$THREADS"
json_is "overserve: the fixture's own author key cannot leak through" \
  specimen-a "sorted(set(d['reviews']['nodes'][0]) - {'submittedAt','state','body','commit'})" \
  "[]" api graphql -f "query=$REVIEWS"

echo "== B. required selection paths =="
exit_is "required: reviews without commit" 2 specimen-a api graphql \
  -f 'query=query{repository{pullRequest{reviews(first:1){nodes{submittedAt state body}}}}}'
exit_is "required: reviews without submittedAt" 2 specimen-a api graphql \
  -f 'query=query{repository{pullRequest{reviews(first:1){nodes{state body commit{oid}}}}}}'
exit_is "required: reviews without body" 2 specimen-a api graphql \
  -f 'query=query{repository{pullRequest{reviews(first:1){nodes{submittedAt state commit{oid}}}}}}'
exit_is "required: threads without isResolved" 2 specimen-a api graphql \
  -f 'query=query{repository{pullRequest{reviewThreads(first:1){nodes{path comments{nodes{body author{login} pullRequestReview{submittedAt}}}}}}}}'
exit_is "required: threads without nested comment body" 2 specimen-a api graphql \
  -f 'query=query{repository{pullRequest{reviewThreads(first:1){nodes{isResolved path comments{nodes{author{login} pullRequestReview{submittedAt}}}}}}}}'
exit_is "required: thread-level body does not satisfy the comment-body path" 2 specimen-a api graphql \
  -f 'query=query{repository{pullRequest{reviewThreads(first:1){nodes{isResolved path body comments{nodes{author{login} pullRequestReview{submittedAt}}}}}}}}'
exit_is "required: threads without the review join" 2 specimen-a api graphql \
  -f 'query=query{repository{pullRequest{reviewThreads(first:1){nodes{isResolved path comments{nodes{body author{login}}}}}}}}'
exit_is "required: userContentEdits without editedAt" 2 specimen-a api graphql \
  -f 'query=query{repository{pullRequest{userContentEdits(first:1){nodes{diff}}}}}'
exit_is "required: comments without author" 2 specimen-j api graphql \
  -f 'query=query{repository{pullRequest{comments(first:1){nodes{body}}}}}'
exit_is "required: number alone serves no connection" 2 specimen-a api graphql \
  -f 'query=query{repository{pullRequest{number}}}'
exit_is "required: the skill-shaped threads query is accepted" 0 specimen-a api graphql -f "query=$THREADS"

echo "== C. projection shape =="
json_is "shape: fixture commit string projects to commit.oid" \
  specimen-a "d['reviews']['nodes'][0]['commit']['oid']" "f3a9c21" api graphql -f "query=$REVIEWS"
json_is "shape: fixture author string projects to author.login" \
  specimen-a "d['reviewThreads']['nodes'][0]['comments']['nodes'][0]['author']['login']" \
  "quill-bot" api graphql -f "query=$THREADS"
json_is "shape: the thread-to-review join carries a real submittedAt" \
  specimen-a "d['reviewThreads']['nodes'][0]['comments']['nodes'][0]['pullRequestReview']['submittedAt']" \
  "2026-07-18T14:05:00Z" api graphql -f "query=$THREADS"
exit_is "shape: composite selected without a selection set" 2 specimen-a api graphql \
  -f 'query=query{repository{pullRequest{reviews(first:1){nodes{submittedAt state body commit}}}}}'
exit_is "shape: empty selection set on a composite" 2 specimen-a api graphql \
  -f 'query=query{repository{pullRequest{reviews(first:1){nodes{}}}}}'
exit_is "shape: a response key selected twice" 2 specimen-a api graphql \
  -f 'query=query{repository{pullRequest{reviews(first:1){nodes{submittedAt state body commit{oid}} nodes{state}}}}}'

echo "== D. pagination =="
json_is "page: specimen-j caps reviews at its page size" \
  specimen-j "len(d['reviews']['nodes'])" "2" api graphql -f "query=$REVIEWS"
json_is "page: a capped connection reports a next page" \
  specimen-j "d['reviews']['pageInfo']['hasNextPage']" "True" api graphql -f "query=$REVIEWS"
json_is "page: the issued cursor names its connection and offset" \
  specimen-j "d['reviews']['pageInfo']['endCursor']" "reviews:2" api graphql -f "query=$REVIEWS"
json_is "page: following the cursor returns the remaining review itself" \
  specimen-j "d['reviews']['nodes'][0]['state']+' '+d['reviews']['nodes'][0]['submittedAt']" \
  "APPROVED 2026-07-25T10:02:00Z" api graphql \
  -f 'query=query{repository{pullRequest{reviews(first:100, after:"reviews:2"){pageInfo{hasNextPage endCursor} nodes{submittedAt state body commit{oid}}}}}}'
json_is "page: the last page reports no next page" \
  specimen-j "d['reviews']['pageInfo']['hasNextPage']" "False" api graphql \
  -f 'query=query{repository{pullRequest{reviews(first:100, after:"reviews:2"){pageInfo{hasNextPage endCursor} nodes{submittedAt state body commit{oid}}}}}}'
json_is "page: page two holds exactly the nodes page one did not" \
  specimen-j "[n['submittedAt'] for n in d['reviews']['nodes']]" \
  "['2026-07-25T10:02:00Z']" api graphql \
  -f 'query=query{repository{pullRequest{reviews(first:100, after:"reviews:2"){nodes{submittedAt state body commit{oid}}}}}}'
json_is "page: first:0 returns no nodes rather than inventing one" \
  specimen-j "len(d['reviews']['nodes'])" "0" api graphql \
  -f 'query=query{repository{pullRequest{reviews(first:0){pageInfo{hasNextPage endCursor} nodes{submittedAt state body commit{oid}}}}}}'
exit_is "page: negative first" 2 specimen-j api graphql \
  -f 'query=query{repository{pullRequest{reviews(first:-1){nodes{submittedAt state body commit{oid}}}}}}'
exit_is "page: a cursor issued for another connection" 2 specimen-j api graphql \
  -f 'query=query{repository{pullRequest{reviews(first:100, after:"reviewThreads:1"){nodes{submittedAt state body commit{oid}}}}}}'
exit_is "page: a cursor past the end" 2 specimen-j api graphql \
  -f 'query=query{repository{pullRequest{reviews(first:100, after:"reviews:99"){nodes{submittedAt state body commit{oid}}}}}}'
exit_is "page: a cursor this stub never issued" 2 specimen-j api graphql \
  -f 'query=query{repository{pullRequest{reviews(first:100, after:"reviews:abc"){nodes{submittedAt state body commit{oid}}}}}}'
exit_is "page: an argument the stub would otherwise ignore" 2 specimen-a api graphql \
  -f 'query=query{repository{pullRequest{reviews(first:1, states:[APPROVED]){nodes{submittedAt state body commit{oid}}}}}}'

exit_is "page: first:true is not an integer" 2 specimen-a api graphql \
  -f 'query=query{repository{pullRequest{reviews(first:true){nodes{submittedAt state body commit{oid}}}}}}'
exit_is "page: first:1.5 is not an integer" 2 specimen-a api graphql \
  -f 'query=query{repository{pullRequest{reviews(first:1.5){nodes{submittedAt state body commit{oid}}}}}}'
json_is "page: a nested connection inherits the specimen's page cap" \
  specimen-j "len(d['reviewThreads']['nodes'][1]['comments']['nodes'])" "2" api graphql -f "query=$THREADS"
json_is "page: the capped nested connection reports its next page" \
  specimen-j "d['reviewThreads']['nodes'][1]['comments']['pageInfo']['hasNextPage']" "True" api graphql \
  -f 'query=query{repository{pullRequest{reviewThreads(first:100){nodes{isResolved path comments(first:100){pageInfo{hasNextPage endCursor} nodes{body author{login} pullRequestReview{submittedAt}}}}}}}}'

echo "== D2. nested cursors name an absolute parent =="
json_is "page: a nested cursor carries the parent's absolute index" \
  specimen-a "d['reviewThreads']['nodes'][0]['comments']['pageInfo']['endCursor']" \
  "reviewThreads[0].comments:1" api graphql \
  -f 'query=query{repository{pullRequest{reviewThreads(first:1){nodes{isResolved path comments(first:1){pageInfo{hasNextPage endCursor} nodes{body author{login} pullRequestReview{submittedAt}}}}}}}}'
json_is "page: the second thread's nested cursor is scoped to index 1, not 0" \
  specimen-a "d['reviewThreads']['nodes'][0]['comments']['pageInfo']['endCursor']" \
  "reviewThreads[1].comments:1" api graphql \
  -f 'query=query{repository{pullRequest{reviewThreads(first:1, after:"reviewThreads:1"){nodes{isResolved path comments(first:1){pageInfo{hasNextPage endCursor} nodes{body author{login} pullRequestReview{submittedAt}}}}}}}}'
exit_is "page: thread 0's nested cursor is refused against thread 1" 2 specimen-a api graphql \
  -f 'query=query{repository{pullRequest{reviewThreads(first:1, after:"reviewThreads:1"){nodes{isResolved path comments(first:1, after:"reviewThreads[0].comments:1"){nodes{body author{login} pullRequestReview{submittedAt}}}}}}}}'

echo "== E. variables =="
json_is "var: after bound through -f matches the literal cursor" \
  specimen-j "len(d['reviews']['nodes'])" "1" api graphql \
  -f 'query=query($c:String){repository{pullRequest{reviews(first:100, after:$c){nodes{submittedAt state body commit{oid}}}}}}' \
  -f 'c=reviews:2'
json_is "var: first bound through -f is honoured" \
  specimen-a "len(d['reviews']['nodes'])" "1" api graphql \
  -f 'query=query($n:Int){repository{pullRequest{reviews(first:$n){nodes{submittedAt state body commit{oid}}}}}}' \
  -f 'n=1'
exit_is "var: an unbound after fails rather than paging from the start" 2 specimen-j api graphql \
  -f 'query=query($c:String){repository{pullRequest{reviews(first:100, after:$c){nodes{submittedAt state body commit{oid}}}}}}'
exit_is "var: an unbound first fails rather than serving everything" 2 specimen-a api graphql \
  -f 'query=query($n:Int){repository{pullRequest{reviews(first:$n){nodes{submittedAt state body commit{oid}}}}}}'

echo "== F. the two comments connections =="
json_is "comments: the top-level connection is served on its own" \
  specimen-j "d['comments']['nodes'][0]['author']['login']" "tobin-sre" api graphql -f "query=$COMMENTS"
json_is "comments: a specimen without them serves an empty connection" \
  specimen-a "len(d['comments']['nodes'])" "0" api graphql -f "query=$COMMENTS"
json_is "comments: top-level and nested are distinct in one query" \
  specimen-j "d['comments']['nodes'][0]['author']['login'] != d['reviewThreads']['nodes'][0]['comments']['nodes'][0]['author']['login']" \
  "True" api graphql \
  -f 'query=query{repository{pullRequest{comments(first:100){nodes{body author{login}}} reviewThreads(first:100){nodes{isResolved path comments(first:100){nodes{body author{login} pullRequestReview{submittedAt}}}}}}}}'

echo "== G. every specimen still serves the battery-shaped query =="
for d in "$PRS"/specimen-*; do
  s=$(basename "$d")
  exit_is "specimen $s: threads" 0 "$s" api graphql -f "query=$THREADS"
  exit_is "specimen $s: reviews" 0 "$s" api graphql -f "query=$REVIEWS"
  exit_is "specimen $s: comments" 0 "$s" api graphql -f "query=$COMMENTS"
  exit_is "specimen $s: edits" 0 "$s" api graphql -f "query=$EDITS"
  exit_is "specimen $s: description" 0 "$s" pr view --json number,body,state
  exit_is "specimen $s: diff" 0 "$s" pr diff
done

echo "== G2. the specimen sweep pins content, not just exit 0 =="
json_is "specimen-a: four threads, every one resolved" \
  specimen-a "str(len(d['reviewThreads']['nodes']))+' '+str(all(t['isResolved'] for t in d['reviewThreads']['nodes']))" \
  "4 True" api graphql -f "query=$THREADS"
json_is "specimen-a: the first thread opens with the reviewer who filed it" \
  specimen-a "d['reviewThreads']['nodes'][0]['comments']['nodes'][0]['author']['login']" \
  "quill-bot" api graphql -f "query=$THREADS"
json_is "specimen-e: exactly one thread is left unresolved" \
  specimen-e "sum(1 for t in d['reviewThreads']['nodes'] if not t['isResolved'])" \
  "1" api graphql -f "query=$THREADS"
json_is "specimen-g: exactly one thread is left unresolved" \
  specimen-g "sum(1 for t in d['reviewThreads']['nodes'] if not t['isResolved'])" \
  "1" api graphql -f "query=$THREADS"
# specimen-j caps at two, so a single page cannot see its third thread: this
# pins both pages, or the claim "every thread is resolved" would be blind to it.
json_is "specimen-j: page one holds two resolved threads and reports more" \
  specimen-j "str(len(d['reviewThreads']['nodes']))+' '+str(sum(1 for t in d['reviewThreads']['nodes'] if not t['isResolved']))+' '+str(d['reviewThreads']['pageInfo']['hasNextPage'])" \
  "2 0 True" api graphql -f "query=$THREADS"
json_is "specimen-j: page two holds its third thread, also resolved" \
  specimen-j "str(len(d['reviewThreads']['nodes']))+' '+str(sum(1 for t in d['reviewThreads']['nodes'] if not t['isResolved']))+' '+str(d['reviewThreads']['pageInfo']['hasNextPage'])" \
  "1 0 False" api graphql \
  -f 'query=query{repository{pullRequest{reviewThreads(first:100, after:"reviewThreads:2"){pageInfo{hasNextPage endCursor} nodes{isResolved path comments(first:100){nodes{body author{login} pullRequestReview{submittedAt}}}}}}}}'
json_is "specimen-h: five threads across its four rounds" \
  specimen-h "len(d['reviewThreads']['nodes'])" "5" api graphql -f "query=$THREADS"

echo "== G3. every join names a real review submission =="
for d in "$PRS"/specimen-*; do
  s=$(basename "$d")
  # A join that points at a timestamp absent from reviews[] invents a review
  # round, which is the data-side version of the over-serve problem.
  got=$(python3 - "$d/forge.json" <<'PYE'
import json,sys
d=json.load(open(sys.argv[1]))
real={r.get("submittedAt") for r in d.get("reviews",[])}
ghosts=[c["pullRequestReview"]["submittedAt"]
        for t in d.get("reviewThreads",[]) for c in t.get("comments",[])
        if isinstance(c.get("pullRequestReview"),dict)
        and c["pullRequestReview"].get("submittedAt") not in real]
print(len(ghosts))
PYE
)
  if [ "$got" = "0" ]; then pass "specimen $s: no join invents a review round"
  else fail "specimen $s: no join invents a review round" "$got join(s) name a submittedAt absent from reviews[]"; fi
done

echo "== H. the read-only perimeter =="
exit_is "perimeter: pr view without --json" 2 specimen-a pr view
exit_is "perimeter: pr view --json with an unserved field" 2 specimen-a pr view --json bogusField
exit_is "perimeter: pr view --json with served fields" 0 specimen-a pr view --json number,title
exit_is "perimeter: pr merge writes" 3 specimen-a pr merge
exit_is "perimeter: pr edit writes" 3 specimen-a pr edit
exit_is "perimeter: pr checkout is outside the read set" 3 specimen-a pr checkout
exit_is "perimeter: auth login writes" 3 specimen-a auth login
exit_is "perimeter: auth status reads" 0 specimen-a auth status
exit_is "perimeter: issue list is outside the read set" 3 specimen-a issue list

echo "== I. the unauthenticated forge =="
AUTHFAIL=1
exit_is "auth-fail: pr view" 4 specimen-a pr view --json number
exit_is "auth-fail: api graphql" 4 specimen-a api graphql -f "query=$REVIEWS"
exit_is "auth-fail: auth status reports not logged in" 1 specimen-a auth status
AUTHFAIL=
exit_is "auth-fail: the authenticated forge still serves" 0 specimen-a pr view --json number
out=$(CMR_FIXTURE= "$GH" pr view --json number 2>&1); got=$?
if [ "$got" = 4 ]; then pass "auth-fail: no specimen configured"
else fail "auth-fail: no specimen configured" "expected exit 4, got $got"; fi

echo "== J. the parser fails loudly =="
exit_is "parse: a fragment spread" 3 specimen-a api graphql \
  -f 'query=query{repository{pullRequest{reviews(first:1){...F}}}}'
exit_is "parse: a mutation" 3 specimen-a api graphql \
  -f 'query=mutation{resolveReviewThread(input:{threadId:"x"}){thread{isResolved}}}'
exit_is "parse: an unbalanced brace" 2 specimen-a api graphql \
  -f 'query=query{repository{pullRequest{reviews(first:1){nodes{state}}}'
exit_is "parse: no repository selection" 2 specimen-a api graphql \
  -f 'query=query{viewer{login}}'
exit_is "parse: a pull request field outside the read set" 3 specimen-a api graphql \
  -f 'query=query{repository{pullRequest{timelineItems(first:1){nodes{__typename}}}}}'
exit_is "parse: no query supplied" 2 specimen-a api graphql -f 'owner=x'
exit_is "parse: a directive" 2 specimen-a api graphql \
  -f 'query=query{repository{pullRequest{reviews(first:1) @include(if:true){nodes{submittedAt state body commit{oid}}}}}}'

echo "== K. aliases =="
json_is "alias: the response uses the alias, not the field name" \
  specimen-a "sorted(d.keys())" "['threads']" api graphql \
  -f 'query=query{repository{pullRequest{threads:reviewThreads(first:100){nodes{isResolved path comments(first:100){nodes{body author{login} pullRequestReview{submittedAt}}}}}}}}'
json_is "alias: an aliased required field is still fetched, under its alias" \
  specimen-a "d['reviews']['nodes'][0]['c']['oid']" "f3a9c21" api graphql \
  -f 'query=query{repository{pullRequest{reviews(first:1){nodes{submittedAt state body c:commit{oid}}}}}}'

printf '\n%d assertions: %d passed, %d failed\n' "$((PASS + FAIL))" "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ] || exit 1
