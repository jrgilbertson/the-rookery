#!/usr/bin/env bash
# Contract checks for scripts/fetch-pr-history.sh, driven by the scripted
# pagination stub in fixtures/history-bin/gh.
#
# Scope: the ways a fetch can look complete without being complete —
#   a surface split across pages, a thread whose comments resume mid-run,
#   a surface that dies after the first page, an identity the floor rejects,
#   a resume cursor the forge never issued, and a fingerprint that either
#   drifts between identical runs or carries PR text out of the payload.
# Not in scope: GraphQL well-formedness (live GitHub is the only oracle).
#
# Scenarios are built into a mktemp directory and removed on exit; this
# repository is never written to and no network call is made.
#
#   bash tests/checking-merge-readiness/fixtures/run-fetch-checks.sh

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# CMR_FETCH_HELPER points the run at a mutated copy of the helper, which is how
# each guard below was falsification-probed; unset, the shipped script runs.
FETCH="${CMR_FETCH_HELPER:-$HERE/../../../skills/checking-merge-readiness/scripts/fetch-pr-history.sh}"
STUB="$HERE/history-bin"
PASS=0
FAIL=0

pass() { PASS=$((PASS + 1)); printf 'PASS  %s\n' "$1"; }
fail() { FAIL=$((FAIL + 1)); printf 'FAIL  %s\n     %s\n' "$1" "$2"; }

WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

# The sentinel rides in every fetched body. Its absence from --fingerprint
# stdout is only meaningful because the full payload proves it is really there.
SENTINEL='SENTINEL-fixture-body-Zq7'

python3 - "$WORK" "$SENTINEL" <<'PYE'
import json, os, sys

work, S = sys.argv[1], sys.argv[2]

def page(after, nodes, nxt=None, more=None):
    return {"after": after, "nodes": nodes,
            "hasNextPage": nxt is not None if more is None else more,
            "endCursor": nxt}

def identity(body=None, base_ref={"target": {"oid": "base-oid"}}, author={"login": "pr-author"}):
    return {"state": "OPEN", "isDraft": False, "headRefOid": "head-oid",
            "baseRefName": "main", "updatedAt": "2026-01-09T00:00:00Z",
            "body": body if body is not None else f"description {S}",
            "author": author, "baseRef": base_ref}

def review(n, body=None):
    return {"id": f"REV{n}", "author": {"login": f"reviewer-{n}"},
            "submittedAt": f"2026-01-0{n}T00:00:00Z", "state": "COMMENTED",
            "body": body if body is not None else f"submission {n} {S}",
            "commit": {"oid": f"commit-oid-{n}"}}

def tcomment(tid, n):
    return {"id": f"{tid}-C{n}", "author": {"login": "reviewer-1"},
            "createdAt": f"2026-01-0{n}T01:00:00Z",
            "body": f"thread note {n} {S}", "line": n, "originalLine": n,
            "pullRequestReview": {"id": "REV1"}}

def thread(n, comments, nxt=None, more=None):
    tid = f"THR{n}"
    return {"id": tid, "path": f"src/file{n}.txt", "isResolved": n % 2 == 0,
            "comments": {"pageInfo": {"hasNextPage": more if more is not None
                                      else nxt is not None,
                                      "endCursor": nxt},
                         "nodes": comments}}

def comment(n):
    return {"id": f"CMT{n}", "author": {"login": f"watcher-{n}"},
            "createdAt": f"2026-01-0{n}T02:00:00Z",
            "body": f"conversation note {n} {S}"}

def edit(n):
    return {"editedAt": f"2026-01-0{n}T03:00:00Z",
            "editor": {"login": "pr-author"},
            "diff": f"post-edit body snapshot {n} {S}"}

def write(name, scenario):
    with open(os.path.join(work, name + ".json"), "w") as fh:
        json.dump(scenario, fh, indent=2)

def paged(reviews=None):
    """Every top-level surface split across two pages behind a cursor."""
    revs = reviews or [[review(1), review(2)], [review(3)]]
    return {
        "identity": identity(),
        "surfaces": {
            "reviews": [page(None, revs[0], "rev:2"), page("rev:2", revs[1])],
            "reviewThreads": [
                page(None, [thread(1, [tcomment("THR1", 1), tcomment("THR1", 2)]),
                            thread(2, [tcomment("THR2", 1)])], "thr:2"),
                page("thr:2", [thread(3, [tcomment("THR3", 1)])]),
            ],
            "comments": [page(None, [comment(1), comment(2)], "com:2"),
                         page("com:2", [comment(3)])],
            "userContentEdits": [page(None, [edit(1)], "edt:1"),
                                 page("edt:1", [edit(2)])],
        },
    }

write("paged", paged())

# Same history with one review body rewritten: the fingerprint must move for
# that node and for nothing else.
write("paged-edited",
      paged(reviews=[[review(1), review(2, body=f"rewritten submission {S}")],
                     [review(3)]]))

# A thread whose first comment page reports more, resuming from its cursor.
nested = {
    "identity": identity(),
    "surfaces": {
        "reviewThreads": [page(None, [thread(1, [tcomment("THR1", 1),
                                                 tcomment("THR1", 2)],
                                             nxt="tc:2")])],
    },
    "threadComments": {"THR1": [page("tc:2", [tcomment("THR1", 3)])]},
}
write("nested", nested)

# The same thread, but the forge reports more with no cursor to resume from.
nocursor = {
    "identity": identity(),
    "surfaces": {
        "reviewThreads": [page(None, [thread(1, [tcomment("THR1", 1)],
                                            nxt=None, more=True)])],
    },
}
write("nocursor", nocursor)

mid = paged()
mid["fail"] = {"surface": "comments", "after": "com:2", "mode": "nonzero"}
write("midfail", mid)

garbled = paged()
garbled["fail"] = {"surface": "reviewThreads", "after": None, "mode": "garbage"}
write("garbled", garbled)

write("notfound", {"identity": None})

write("nullfloor", {"identity": identity(base_ref=None)})

write("nullauthor", {"identity": identity(author=None)})

# A body far past ARG_MAX: fetched text that reached a command argument would
# fail here as something other than a clean run.
write("bigbody", {"identity": identity(),
                  "surfaces": {"reviews": [page(None, [review(1, body="B" * 1200000)])]}})
PYE
[ $? -eq 0 ] || { printf 'FAIL  scenario build\n'; exit 1; }

RUN_CODE=0
run() { # run <scenario> [fetch args...]
  local scen=$1
  shift
  env CMR_HISTORY_SCENARIO="$WORK/$scen.json" PATH="$STUB:$PATH" \
    "$FETCH" --repo mapleworks/orderline --pr 412 "$@" \
    >"$WORK/out" 2>"$WORK/err"
  RUN_CODE=$?
}

code_is() { # code_is <label> <want>
  if [ "$RUN_CODE" = "$2" ]; then pass "$1"
  else fail "$1" "expected exit $2, got $RUN_CODE: $(head -1 "$WORK/err")"; fi
}

err_has() { # err_has <label> <needle>
  if grep -qF -- "$2" "$WORK/err"; then pass "$1"
  else fail "$1" "message does not name [$2]: $(head -1 "$WORK/err")"; fi
}

stdout_empty() { # stdout_empty <label>
  if [ ! -s "$WORK/out" ]; then pass "$1"
  else fail "$1" "$(wc -c <"$WORK/out" | tr -d ' ') bytes printed; a partial payload must never reach stdout"; fi
}

jq_is() { # jq_is <label> <filter> <want>
  local got
  got=$(jq -r "$2" "$WORK/out" 2>&1)
  if [ "$got" = "$3" ]; then pass "$1"
  else fail "$1" "expected [$3], got [$got]"; fi
}

echo "== A. outer pagination: the union of pages, counted once =="
# Pins the completion bound in references/fetch-floor.md: a surface split
# across pages must arrive whole, and arrive once.
run paged
code_is "paged: exit 0" 0
jq_is "paged: complete" '.complete' true
jq_is "paged: review ids are the union of both pages" \
  '[.reviews[].id] | join(",")' "REV1,REV2,REV3"
jq_is "paged: thread ids are the union of both pages" \
  '[.reviewThreads[].id] | join(",")' "THR1,THR2,THR3"
jq_is "paged: conversation comment ids are the union of both pages" \
  '[.conversationComments[].id] | join(",")' "CMT1,CMT2,CMT3"
jq_is "paged: counts match the union" \
  '[.counts.reviews, .counts.reviewThreads, .counts.threadComments,
    .counts.conversationComments, .counts.descriptionEdits] | join(" ")' \
  "3 3 4 3 2"
jq_is "paged: no duplicate node ids on any surface" \
  '[[.reviews[].id], [.reviewThreads[].id], [.conversationComments[].id],
    [.reviewThreads[].comments[].id]]
   | map(length - (unique | length)) | add' 0

echo "== B. nested thread-comment resume =="
# Pins finding #7 (cursor guard) and the nested-connection clause of the
# fetch floor: continuation comments append once, with no page-one repeat.
run nested
code_is "nested: exit 0" 0
jq_is "nested: continuation appended once, in order" \
  '[.reviewThreads[0].comments[].id] | join(",")' "THR1-C1,THR1-C2,THR1-C3"
jq_is "nested: thread comment count counts each comment once" \
  '.counts.threadComments' 3

echo "== C. a surface that dies mid-run is never a payload =="
# Pins finding #3 (fail-closed guards): exit 4 and nothing on stdout, so a
# caller can never read a partial history as complete.
run midfail
code_is "mid-run failure: exit 4" 4
stdout_empty "mid-run failure: no payload printed"
err_has "mid-run failure: names the surface" "conversation comments fetch failed"
run garbled
code_is "malformed page: exit 4" 4
stdout_empty "malformed page: no payload printed"

echo "== D. identity the floor rejects =="
# Pins finding #3: a fetch that answers without the floor's identity fields is
# incomplete history, not a thin success.
run notfound
code_is "pull request null: exit 4" 4
err_has "pull request null: names the condition" "pull request not found"
stdout_empty "pull request null: no payload printed"
run nullfloor
code_is "null base ref: exit 4" 4
err_has "null base ref: names the missing field" "baseRefOid"
stdout_empty "null base ref: no payload printed"
run nullauthor
code_is "null author: exit 4" 4
err_has "null author: names the missing field" "author"
stdout_empty "null author: no payload printed"

echo "== E. resume cursor the forge never issued =="
# Pins finding #7: hasNextPage with no endCursor must stop the run, not drop
# the remaining comments silently.
run nocursor
code_is "missing resume cursor: exit 4" 4
err_has "missing resume cursor: names the guard" "thread comment cursor missing"
stdout_empty "missing resume cursor: no payload printed"

echo "== F. fingerprint stability and body containment =="
# Pins the step 7 fingerprint contract: identical history digests identically,
# a changed body moves exactly its own node, and no PR text leaves in
# --fingerprint mode.
run paged --fingerprint
code_is "fingerprint: exit 0" 0
cp "$WORK/out" "$WORK/fp-1.json"
run paged --fingerprint
cp "$WORK/out" "$WORK/fp-2.json"
if cmp -s "$WORK/fp-1.json" "$WORK/fp-2.json"; then
  pass "fingerprint: two runs over identical history are byte-identical"
else
  fail "fingerprint: two runs over identical history are byte-identical" \
    "$(diff "$WORK/fp-1.json" "$WORK/fp-2.json" | head -3)"
fi
if grep -qF -- "$SENTINEL" "$WORK/fp-1.json"; then
  fail "fingerprint: no body text on stdout" "the fetched body sentinel reached --fingerprint stdout"
else
  pass "fingerprint: no body text on stdout"
fi
run paged
if grep -qF -- "$SENTINEL" "$WORK/out"; then
  pass "fingerprint: the sentinel is really in the fetched bodies (control)"
else
  fail "fingerprint: the sentinel is really in the fetched bodies (control)" \
    "the full payload carries no sentinel, so the containment check above proves nothing"
fi
run paged-edited --fingerprint
cp "$WORK/out" "$WORK/fp-3.json"
moved=$(jq -s -r '
  def flat: .fingerprint
    | {identity: .identity.bodyDigest}
      + ([.reviews[], .reviewThreads[], .conversationComments[],
          .descriptionEdits[]]
         | map({key: (.id | tostring), value: .digest}) | from_entries);
  (.[0] | flat) as $a | (.[1] | flat) as $b
  | [$a | to_entries[] | select($b[.key] != .value) | .key] | join(",")
' "$WORK/fp-1.json" "$WORK/fp-3.json" 2>&1)
if [ "$moved" = "REV2" ]; then pass "fingerprint: a changed body moves exactly that node's digest"
else fail "fingerprint: a changed body moves exactly that node's digest" \
  "digests moved for [$moved], expected [REV2]"; fi

echo "== G. fetched text stays out of argv =="
# Pins finding #8: a body past ARG_MAX spliced into a command argument would
# fail as something other than a clean run.
run bigbody
code_is "1.2MB body: exit 0" 0
jq_is "1.2MB body: the review still arrives" '.counts.reviews' 1

printf '\n%d assertions: %d passed, %d failed\n' "$((PASS + FAIL))" "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ] || exit 1
