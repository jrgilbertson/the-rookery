#!/usr/bin/env bash
#
# run-helper-checks.sh — exercises every documented output state of the
# checking-pr-readiness surface-report helper, and the step 1 surface identity,
# against throwaway git fixtures.
#
# Each assertion checks the verdict line (line 1) and the exit code, because the
# helper's contract is exactly that pair. Fixtures are built under a mktemp
# directory and removed on exit; this repository is never written to.
#
# Usage: bash tests/checking-pr-readiness/fixtures/run-helper-checks.sh
# Exits 0 when every assertion passes, 1 otherwise.

set -uo pipefail

here=$(cd "$(dirname "$0")" && pwd)
scripts="$here/../../../skills/checking-pr-readiness/scripts"
surface="$scripts/surface-report.sh"

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

passed=0
failed=0

# Every verdict line the helper emits is recorded with its exit code, so the
# exit-map pin at the end can hold the whole run against the documented pairs.
record() { # record <output> <exit>
	first=$(printf '%s\n' "$1" | sed -n '1p')
	case "$first" in
	"verdict: "*) printf '%s|%s\n' "${first#verdict: }" "$2" >>"$work/observed" ;;
	esac
}

check() { # check <state> <expected-verdict> <expected-exit> <cwd> <cmd>...
	state="$1" want="$2" want_code="$3" dir="$4"
	shift 4
	out=$(cd "$dir" && "$@" 2>&1)
	code=$?
	record "$out" "$code"
	got=$(printf '%s\n' "$out" | sed -n '1p')
	if [ "$got" = "verdict: $want" ] && [ "$code" -eq "$want_code" ]; then
		printf 'PASS %s\n' "$state"
		passed=$((passed + 1))
	else
		printf 'FAIL %s — got [%s] exit %s, wanted [verdict: %s] exit %s\n' \
			"$state" "$got" "$code" "$want" "$want_code"
		failed=$((failed + 1))
	fi
}

ok() { printf 'PASS %s\n' "$1"; passed=$((passed + 1)); }
no() { printf 'FAIL %s — %s\n' "$1" "$2"; failed=$((failed + 1)); }

# The listing and flag checks below assert on the detail lines, not only
# on the verdict pair, so one invocation is captured and then read repeatedly.
run_out=""
run_code=0
run() { # run <cwd> <cmd>...
	dir="$1"
	shift
	run_out=$(cd "$dir" && "$@" 2>&1)
	run_code=$?
	record "$run_out" "$run_code"
}

exits() { # exits <state> <expected-exit>
	if [ "$run_code" -eq "$2" ]; then ok "$1"; else
		no "$1" "exit $run_code, wanted $2: $(printf '%s\n' "$run_out" | sed -n '1p')"
	fi
}

# Drain piped output: grep -q can close early and make printf fail under pipefail.
says() { # says <state> <exact line>
	if printf '%s\n' "$run_out" | grep -Fx -- "$2" >/dev/null; then ok "$1"; else
		no "$1" "no line [$2]"
	fi
}

mentions_text() { # mentions_text <state> <substring>
	if printf '%s\n' "$run_out" | grep -F -- "$2" >/dev/null; then ok "$1"; else
		no "$1" "output does not carry [$2]"
	fi
}

omits() { # omits <state> <substring that must not appear>
	if printf '%s\n' "$run_out" | grep -F -- "$2" >/dev/null; then
		no "$1" "output carries [$2] and should not"
	else ok "$1"; fi
}

lines_matching() { # lines_matching <state> <grep pattern> <expected count>
	got=$(printf '%s\n' "$run_out" | grep -c -- "$2")
	if [ "$got" -eq "$3" ]; then ok "$1"; else
		no "$1" "$got lines match [$2], wanted $3"
	fi
}

w() { # w <path> <content>
	mkdir -p "$(dirname "$1")"
	printf '%s\n' "$2" >"$1"
}

cm() { # cm <repo> <iso-date> <message>
	git -C "$1" add -A
	GIT_AUTHOR_DATE="$2" GIT_COMMITTER_DATE="$2" git -C "$1" commit -qm "$3"
}

repo() { # repo <name> [init-branch] — seeded repo, left on the default branch
	r="$work/$1"
	mkdir -p "$r"
	git -C "$r" init -q -b "${2:-main}"
	git -C "$r" config user.email tester@example.invalid
	git -C "$r" config user.name Tester
	w "$r/seed.txt" seed
	cm "$r" 2020-01-01T00:00:00Z seed
	printf '%s\n' "$r"
}

# Anything committed before this belongs to the merge base, not to the branch.
branch() { git -C "$1" checkout -qb work; }

nogit="$work/nogit"
mkdir -p "$nogit"

bare="$work/bare"
git init -q --bare "$bare"

# --- surface-report.sh -------------------------------------------------------

s1=$(repo surface-listed)
branch "$s1"
w "$s1/src.txt" changed
cm "$s1" 2020-02-01T00:00:00Z change
w "$s1/extra.txt" new
check "surface: surface listed" "surface listed" 0 "$s1" "$surface"
check "surface: not run (unknown option)" "not run" 2 "$s1" "$surface" --bogus
check "surface: not run (retired --cap)" "not run" 2 "$s1" "$surface" --cap reviewer=10

s2=$(repo surface-clean)
check "surface: no changes on surface" "no changes on surface" 0 "$s2" "$surface"

s3=$(repo surface-unresolved feature)
w "$s3/staged.txt" staged
git -C "$s3" add -A
check "surface: surface incomplete (committed unmeasured)" "surface incomplete" 0 "$s3" "$surface"

s7=$(repo surface-tag-main develop)
w "$s7/src.txt" work
cm "$s7" 2020-02-01T00:00:00Z work
git -C "$s7" tag main
check "surface: surface incomplete (tag named main is not a branch)" "surface incomplete" 0 \
	"$s7" "$surface"

s6=$(repo surface-ambiguous)
w "$s6/src.txt" work
cm "$s6" 2020-02-01T00:00:00Z work
git -C "$s6" branch master
git -C "$s6" checkout -qb work
w "$s6/src.txt" changed
cm "$s6" 2020-03-01T00:00:00Z change
check "surface: surface incomplete (ambiguous default branch)" "surface incomplete" 0 \
	"$s6" "$surface"

s5=$(repo surface-unresolved-clean feature)
w "$s5/src.txt" work
cm "$s5" 2020-02-01T00:00:00Z work
check "surface: surface incomplete (unresolved base, clean worktree)" "surface incomplete" 0 \
	"$s5" "$surface"

s4=$(repo surface-broken)
printf 'not an index' >"$s4/.git/index"
check "surface: not run (failed git read)" "not run" 4 "$s4" "$surface"
check "surface: not run (not a git repository)" "not run" 4 "$nogit" "$surface"
check "surface: not run (bare repository)" "not run" 4 "$bare" "$surface"

# A pull request that targets a non-default branch is measured against that
# target, not against the default branch the helper would resolve on its own.
nt=$(repo surface-nondefault-target)
git -C "$nt" checkout -qb assessment-target
w "$nt/target.txt" target
cm "$nt" 2020-02-01T00:00:00Z target
git -C "$nt" checkout -qb work
w "$nt/src.txt" work
cm "$nt" 2020-03-01T00:00:00Z work
run "$nt" "$surface" --base assessment-target
exits "surface: --base names a non-default target" 0
says "surface: the non-default target is the measured base" \
	"default branch: refs/heads/assessment-target (from --base)"
says "surface: only the branch's own commit is counted" "committed: 1"
run "$nt" "$surface"
says "surface: the implicit default base counts the target's commit too" "committed: 2"

# --- Listing caps on a large surface -----------------------------------------
# A capped listing has to stay a report, not a truncation that kills the run:
# with a payload past the pipe buffer, closing the listing early raises SIGPIPE
# on the writer, and pipefail turns that into exit 141 with no verdict at all.
# 500 long pathnames put roughly 96 KiB through the listing, well past the
# 64 KiB buffer, so the exit code here is the real assertion.

pad=$(printf 'x%.0s' $(seq 1 180))
s8=$(repo surface-listing-cap)
branch "$s8"
i=1
while [ "$i" -le 500 ]; do
	printf 'file %s\n' "$i" >"$s8/${pad}-$i.txt"
	i=$((i + 1))
done

run "$s8" "$surface"
exits "surface: 500 untracked paths report (not SIGPIPE)" 0
says "surface: verdict survives the capped listing" "verdict: surface listed"
says "surface: untracked count is exact" "untracked: 500"
says "surface: total is exact" "total distinct changed files: 500"
lines_matching "surface: 25 paths listed under the cap" "^  ${pad}-" 25
says "surface: the remainder is named" "  … and 475 more (--full lists every path)"

run "$s8" "$surface" --full
exits "surface: --full over 500 paths" 0
lines_matching "surface: --full lists every path" "^  ${pad}-" 500
omits "surface: --full drops the remainder line" "… and "

# --- --merge-base validation --------------------------------------------------
# A supplied merge base decides the committed category on its own, so an
# unchecked one is a silent pass: HEAD passed here empties the committed diff
# and branch work reads as an empty surface. The helper must refuse instead.

mb=$(repo merge-base-checks)
w "$mb/CHANGELOG.md" "# Changelog"
cm "$mb" 2020-02-01T00:00:00Z changelog
git -C "$mb" checkout -qb side
w "$mb/side.txt" side
cm "$mb" 2020-02-15T00:00:00Z side
side_sha=$(git -C "$mb" rev-parse HEAD)
git -C "$mb" checkout -q main
branch "$mb"
w "$mb/src.txt" work
w "$mb/CHANGELOG.md" "# Changelog

- added the widget"
cm "$mb" 2020-03-01T00:00:00Z work
true_mb=$(git -C "$mb" merge-base HEAD main)

plain=$(cd "$mb" && "$surface" 2>&1)
flagged=$(cd "$mb" && "$surface" --merge-base "$true_mb" 2>&1)
if [ "$plain" = "$flagged" ]; then
	ok "surface: --merge-base at the true merge base matches the unflagged run"
else
	no "surface: --merge-base at the true merge base matches the unflagged run" \
		"outputs differ: $(printf '%s\n' "$flagged" | sed -n '1p')"
fi

run "$mb" "$surface" --merge-base HEAD
exits "surface: --merge-base HEAD refused" 4
says "surface: --merge-base HEAD reports not run" "verdict: not run"
mentions_text "surface: --merge-base HEAD names the mismatch" \
	"does not match merge-base(HEAD,"

run "$mb" "$surface" --merge-base "$side_sha"
exits "surface: --merge-base off the branch refused" 4
says "surface: --merge-base off the branch reports not run" "verdict: not run"

# With no base to check against, the weaker ancestor test is the only one left,
# and a non-ancestor must still fail closed.
nb=$(repo merge-base-nobase feature)
w "$nb/CHANGELOG.md" "# Changelog"
cm "$nb" 2020-02-01T00:00:00Z changelog
git -C "$nb" checkout -qb elsewhere
w "$nb/other.txt" other
cm "$nb" 2020-02-15T00:00:00Z other
other_sha=$(git -C "$nb" rev-parse HEAD)
git -C "$nb" checkout -q feature
w "$nb/src.txt" work
cm "$nb" 2020-03-01T00:00:00Z work

run "$nb" "$surface" --merge-base "$other_sha"
exits "surface: non-ancestor --merge-base refused with no base to check against" 4
mentions_text "surface: non-ancestor --merge-base names the ancestry test" \
	"is not an ancestor of HEAD"

# --- --base namespace resolution ----------------------------------------------
# git resolves a bare short name tags-first, so a tag named main shadows the
# branch: the helpers would diff the branch against its own tip and report an
# empty committed category. A supplied --base resolves in the branch namespaces
# only, and a value that resolves in neither is refused rather than falling back
# to a bare rev-parse a tag could hijack.

bt=$(repo base-tag-spoof)
w "$bt/CHANGELOG.md" "# Changelog"
cm "$bt" 2020-02-01T00:00:00Z changelog
branch "$bt"
w "$bt/src.txt" work
cm "$bt" 2020-03-01T00:00:00Z work
git -C "$bt" tag main HEAD
git -C "$bt" tag v1.0 HEAD

run "$bt" "$surface" --base main
exits "surface: --base main measures against the branch, not the tag" 0
says "surface: --base main names the branch namespace" \
	"default branch: refs/heads/main (from --base)"
says "surface: --base main counts the branch commit" "committed: 1"

run "$bt" "$surface" --base v1.0
exits "surface: --base naming only a tag refused" 4
says "surface: --base naming only a tag reports not run" "verdict: not run"
mentions_text "surface: --base naming only a tag names the ref" \
	"the supplied --base v1.0 resolves to no branch"

run "$bt" "$surface" --base no-such-ref
exits "surface: --base resolving to no branch refused" 4
says "surface: --base resolving to no branch reports not run" "verdict: not run"

# --- Surface identity (SKILL.md step 1) --------------------------------------
# The identity command is read from the shipped SKILL.md and run as written, so
# these cases exercise the production text, not a copy. Each case is an edit
# that must change the identity, plus the guarantees that it leaves the real
# index alone and matches what a publisher's `git add -A` would commit.
skill_md="$here/../../../skills/checking-pr-readiness/SKILL.md"
identity_cmd=$(awk '/^```sh$/{on=1; next} /^```$/{on=0} on' "$skill_md")
surface_id() { # surface_id <repo> — print the identity tree OID
	(
		cd "$1" || exit 1
		# The SKILL.md command reads $tmp, which the shell check cannot see.
		# shellcheck disable=SC2034
		tmp=$(mktemp -d "$work/id.XXXXXX")
		eval "$identity_cmd"
	)
}
changes() { # changes <label> <before> <after>
	if [ -n "$2" ] && [ "$2" != "$3" ]; then ok "$1"; else no "$1" "identity did not change"; fi
}

si=$(repo surface-identity)
w "$si/.gitignore" "ign/"
cm "$si" 2020-02-01T00:00:00Z ignore
w "$si/src.txt" dirty
a=$(surface_id "$si"); w "$si/src.txt" "dirty, then edited in place"; b=$(surface_id "$si")
changes "identity: an in-place edit of an already-dirty file" "$a" "$b"
w "$si/new.txt" untracked; c=$(surface_id "$si")
changes "identity: a new untracked file" "$b" "$c"
w "$si/ign/forced.txt" v1; git -C "$si" add -f ign/forced.txt; d=$(surface_id "$si")
w "$si/ign/forced.txt" "v2, a longer edit"; e=$(surface_id "$si")
changes "identity: an edit to a force-added ignored file" "$d" "$e"
w "$si/ign/plain.txt" ignored; f=$(surface_id "$si")
if [ "$e" = "$f" ]; then ok "identity: an ignored file that will not ship is left out"
else no "identity: an ignored file that will not ship is left out" "identity changed"; fi
status_before=$(git -C "$si" status --porcelain); index_before=$(git -C "$si" ls-files -s)
surface_id "$si" >/dev/null
if [ "$status_before" = "$(git -C "$si" status --porcelain)" ] &&
	[ "$index_before" = "$(git -C "$si" ls-files -s)" ]; then
	ok "identity: the real index and working tree are untouched"
else no "identity: the real index and working tree are untouched" "status or index moved"; fi
pub=$(mktemp -d "$work/pub.XXXXXX")
cp "$si/.git/index" "$pub/index"
published=$(cd "$si" && GIT_INDEX_FILE="$pub/index" git add -A && GIT_INDEX_FILE="$pub/index" git write-tree)
if [ "$(surface_id "$si")" = "$published" ]; then ok "identity: matches what git add -A would commit"
else no "identity: matches what git add -A would commit" "trees differ"; fi
sn="$work/surface-identity-unborn"; mkdir -p "$sn"; git -C "$sn" init -q; w "$sn/a.txt" a
if [ -n "$(surface_id "$sn")" ]; then ok "identity: builds on a branch with no commits"
else no "identity: builds on a branch with no commits" "no tree OID"; fi

# --- Exit pin -----------------------------------------------------------------
# The verdict and exit code are one contract: a surface verdict always exits 0,
# and `not run` always exits 2 (usage) or 4 (hard failure). Every pair this run
# observed is held to that, and each exit has to have been exercised.
observed=$(sort -u "$work/observed")
while IFS='|' read -r verdict code; do
	[ -n "$verdict" ] || continue
	label="exit pin: ${verdict} at exit ${code}"
	case "$verdict|$code" in
	"surface listed|0" | "no changes on surface|0" | "surface incomplete|0" | "not run|2" | "not run|4")
		ok "$label" ;;
	*) no "$label" "not a documented verdict and exit pair" ;;
	esac
done <<MAP
$observed
MAP
for want in 0 2 4; do
	if printf '%s\n' "$observed" | grep "|${want}\$" >/dev/null; then
		ok "exit pin: exit $want was exercised"
	else
		no "exit pin: exit $want was exercised" "no helper run in this suite returned it"
	fi
done

printf '%s assertions: %s passed, %s failed\n' "$((passed + failed))" "$passed" "$failed"
[ "$failed" -eq 0 ]
