#!/usr/bin/env bash
#
# run-helper-checks.sh — exercises every documented output state of the three
# checking-pr-readiness helpers against throwaway git fixtures.
#
# Each assertion checks the verdict line (line 1) and the exit code, because the
# helpers' contract is exactly that pair. Fixtures are built under a mktemp
# directory and removed on exit; this repository is never written to.
#
# Usage: bash tests/checking-pr-readiness/fixtures/run-helper-checks.sh
# Exits 0 when every assertion passes, 1 otherwise.

set -uo pipefail

here=$(cd "$(dirname "$0")" && pwd)
scripts="$here/../../../skills/checking-pr-readiness/scripts"
surface="$scripts/surface-report.sh"
changelog="$scripts/changelog-union.sh"
evidence="$scripts/evidence-freshness.sh"

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

passed=0
failed=0

check() { # check <state> <expected-verdict> <expected-exit> <cwd> <cmd>...
	state="$1" want="$2" want_code="$3" dir="$4"
	shift 4
	out=$(cd "$dir" && "$@" 2>&1)
	code=$?
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

# --- surface-report.sh -------------------------------------------------------

s1=$(repo surface-caps)
branch "$s1"
w "$s1/src.txt" changed
cm "$s1" 2020-02-01T00:00:00Z change
w "$s1/extra.txt" new
check "surface: under caps" "under caps" 0 "$s1" "$surface" --cap reviewer=10
check "surface: exceeds cap" "exceeds cap for reviewer" 0 "$s1" "$surface" --cap reviewer=1
check "surface: cap unverified (no cap given)" "cap unverified" 0 "$s1" "$surface"
check "surface: covered by repo gate" "covered by repo gate" 3 "$s1" "$surface" --defer ci-size
check "surface: not run (unknown option)" "not run" 2 "$s1" "$surface" --bogus
check "surface: not run (empty --cap name)" "not run" 2 "$s1" "$surface" --cap "=0"
check "surface: not run (non-integer cap)" "not run" 2 "$s1" "$surface" --cap "reviewer=x"

s2=$(repo surface-clean)
check "surface: no changes on surface" "no changes on surface" 0 "$s2" "$surface" --cap reviewer=10

s3=$(repo surface-unresolved feature)
w "$s3/staged.txt" staged
git -C "$s3" add -A
check "surface: cap unverified (committed unmeasured)" "cap unverified" 0 "$s3" "$surface" --cap reviewer=10

s4=$(repo surface-broken)
printf 'not an index' >"$s4/.git/index"
check "surface: not run (failed git read)" "not run" 4 "$s4" "$surface" --cap reviewer=10
check "surface: not run (not a git repository)" "not run" 4 "$nogit" "$surface"

# --- changelog-union.sh ------------------------------------------------------

c1=$(repo changelog-present)
w "$c1/CHANGELOG.md" "# Changelog"
cm "$c1" 2020-02-01T00:00:00Z changelog
branch "$c1"
w "$c1/CHANGELOG.md" "# Changelog

- added the widget"
w "$c1/src.txt" work
cm "$c1" 2020-03-01T00:00:00Z entry
check "changelog: present" present 0 "$c1" "$changelog"

c2=$(repo changelog-touched)
w "$c2/CHANGELOG.md" "# Changelog
- one
- two"
cm "$c2" 2020-02-01T00:00:00Z changelog
branch "$c2"
w "$c2/CHANGELOG.md" "# Changelog
- two"
cm "$c2" 2020-03-01T00:00:00Z "drop a line"
check "changelog: changed without entry" "changed without entry" 0 "$c2" "$changelog"

c3=$(repo changelog-missing)
w "$c3/CHANGELOG.md" "# Changelog"
cm "$c3" 2020-02-01T00:00:00Z changelog
branch "$c3"
w "$c3/src.txt" work
cm "$c3" 2020-03-01T00:00:00Z work
check "changelog: missing" missing 0 "$c3" "$changelog"

c4=$(repo changelog-clean)
w "$c4/CHANGELOG.md" "# Changelog"
cm "$c4" 2020-02-01T00:00:00Z changelog
branch "$c4"
check "changelog: no changes on surface" "no changes on surface" 0 "$c4" "$changelog"

c5=$(repo changelog-absent)
w "$c5/src.txt" work
check "changelog: no changelog" "no changelog" 2 "$c5" "$changelog"

c6=$(repo changelog-untracked)
w "$c6/CHANGELOG.md" "- untracked entry"
check "changelog: present (untracked changelog)" present 0 "$c6" "$changelog"
check "changelog: covered by repo gate" "covered by repo gate" 3 "$c6" "$changelog" --defer ci-changelog
check "changelog: not run (unknown option)" "not run" 2 "$c6" "$changelog" --bogus
check "changelog: not run (not a git repository)" "not run" 4 "$nogit" "$changelog"

# --- evidence-freshness.sh ---------------------------------------------------

e1=$(repo evidence-fresh)
w "$e1/notes/impl.md" "implementation"
cm "$e1" 2020-02-01T00:00:00Z impl
w "$e1/logs/run.md" "ran the suite"
cm "$e1" 2020-03-01T00:00:00Z record
check "evidence: fresh" fresh 0 "$e1" "$evidence" logs/run.md notes/impl.md
w "$e1/logs/run.md" "ran the suite again"
check "evidence: record unverifiable (dirty)" "record unverifiable (dirty)" 0 "$e1" \
	"$evidence" logs/run.md notes/impl.md

e2=$(repo evidence-stale)
w "$e2/logs/run.md" "ran the suite"
cm "$e2" 2020-02-01T00:00:00Z record
w "$e2/notes/impl.md" "implementation"
cm "$e2" 2020-03-01T00:00:00Z impl
check "evidence: stale record found (path newer)" "stale record found" 0 "$e2" \
	"$evidence" logs/run.md notes/impl.md
rm "$e2/logs/run.md"
check "evidence: stale record found (record deleted)" "stale record found" 0 "$e2" \
	"$evidence" logs/run.md notes/impl.md
check "evidence: no records (record never existed)" "no records" 2 "$e2" \
	"$evidence" logs/absent.md notes/impl.md

e3=$(repo evidence-names)
w "$e3/notes/impl.md" "implementation"
w "$e3/docs/plan.md" "the plan proposes widget-report.md"
cm "$e3" 2020-02-01T00:00:00Z names
check "evidence: consistent (file carries the name)" consistent 0 "$e3" \
	"$evidence" --check-name impl.md notes
check "evidence: stale reference found (named but never built)" "stale reference found" 0 "$e3" \
	"$evidence" --check-name widget-report.md docs
check "evidence: no records (search root missing)" "no records" 2 "$e3" \
	"$evidence" --check-name impl.md absent-dir
check "evidence: covered by repo gate" "covered by repo gate" 3 "$e3" "$evidence" --defer ci-evidence
check "evidence: not run (no arguments)" "not run" 2 "$e3" "$evidence"
check "evidence: not run (empty --check-name)" "not run" 2 "$e3" "$evidence" --check-name "" notes
check "evidence: not run (trailing args in name mode)" "not run" 2 "$e3" \
	"$evidence" --check-name impl.md notes extra
check "evidence: not run (one positional only)" "not run" 2 "$e3" "$evidence" logs/run.md
check "evidence: not run (not a git repository)" "not run" 4 "$nogit" "$evidence" rec.md path.md

# --- Verdict drift guard -----------------------------------------------------
# Every verdict a helper can emit must appear in the sweep reference, so the
# reference cannot silently drift from the scripts. One direction only:
# reference-side additions are caught by review, not here. Parameterized
# verdicts are checked by their fixed prefix.
ref="$scripts/../references/sweep-classes.md"
if [ -f "$ref" ]; then
	emitted=$({ grep -h "printf 'verdict: " "$surface" "$evidence" "$changelog" |
		sed "s/.*printf 'verdict: //;s/\\\\n.*//"
		grep -h '^[[:space:]]*verdict="' "$surface" | sed 's/.*verdict="//;s/".*//'
	} | grep -v '^%s$' | sed 's/ for \$.*/ for/' | sort -u)
	while IFS= read -r v; do
		[ -n "$v" ] || continue
		if grep -qF -- "$v" "$ref"; then
			printf 'PASS reference lists emitted verdict: %s\n' "$v"
			passed=$((passed + 1))
		else
			printf 'FAIL reference missing emitted verdict: %s\n' "$v"
			failed=$((failed + 1))
		fi
	done <<EOF
$emitted
EOF
else
	printf 'FAIL sweep reference not found at %s\n' "$ref"
	failed=$((failed + 1))
fi

printf '%s assertions: %s passed, %s failed\n' "$((passed + failed))" "$passed" "$failed"
[ "$failed" -eq 0 ]
