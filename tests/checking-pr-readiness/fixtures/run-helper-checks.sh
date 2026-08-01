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

bare="$work/bare"
git init -q --bare "$bare"

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
check "surface: not run (cap beyond integer range)" "not run" 2 "$s1" "$surface" \
	--cap "reviewer=999999999999999999999999999999999999"

s2=$(repo surface-clean)
check "surface: no changes on surface" "no changes on surface" 0 "$s2" "$surface" --cap reviewer=10

s3=$(repo surface-unresolved feature)
w "$s3/staged.txt" staged
git -C "$s3" add -A
check "surface: cap unverified (committed unmeasured)" "cap unverified" 0 "$s3" "$surface" --cap reviewer=10

s6=$(repo surface-ambiguous)
w "$s6/src.txt" work
cm "$s6" 2020-02-01T00:00:00Z work
git -C "$s6" branch master
git -C "$s6" checkout -qb work
w "$s6/src.txt" changed
cm "$s6" 2020-03-01T00:00:00Z change
check "surface: cap unverified (ambiguous default branch)" "cap unverified" 0 \
	"$s6" "$surface" --cap reviewer=10

s5=$(repo surface-unresolved-clean feature)
w "$s5/src.txt" work
cm "$s5" 2020-02-01T00:00:00Z work
check "surface: cap unverified (unresolved base, clean worktree)" "cap unverified" 0 \
	"$s5" "$surface" --cap reviewer=10

s4=$(repo surface-broken)
printf 'not an index' >"$s4/.git/index"
check "surface: not run (failed git read)" "not run" 4 "$s4" "$surface" --cap reviewer=10
check "surface: not run (not a git repository)" "not run" 4 "$nogit" "$surface"
check "surface: not run (bare repository)" "not run" 4 "$bare" "$surface"
check "surface: not run (empty --defer)" "not run" 2 "$s1" "$surface" --defer ""

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
check "changelog: not run (empty --defer)" "not run" 2 "$c6" "$changelog" --defer ""
check "changelog: not run (not a git repository)" "not run" 4 "$nogit" "$changelog"
check "changelog: not run (bare repository)" "not run" 4 "$bare" "$changelog"

c7=$(repo changelog-broken)
w "$c7/CHANGELOG.md" "# Changelog"
cm "$c7" 2020-02-01T00:00:00Z changelog
branch "$c7"
printf 'not an index' >"$c7/.git/index"
check "changelog: not run (failed git read)" "not run" 4 "$c7" "$changelog"

c8=$(repo changelog-unresolved feature)
w "$c8/CHANGELOG.md" "# Changelog"
w "$c8/src.txt" work
cm "$c8" 2020-02-01T00:00:00Z work
check "changelog: not run (default branch unresolved)" "not run" 4 "$c8" "$changelog"

c12=$(repo changelog-renamed)
w "$c12/CHANGELOG.md" "# Changelog
- one"
cm "$c12" 2020-02-01T00:00:00Z changelog
branch "$c12"
git -C "$c12" rm -q CHANGELOG.md
w "$c12/CHANGELOG" "# Changelog
- one
- renamed and extended"
git -C "$c12" add CHANGELOG
check "changelog: present (staged rename with new entry)" present 0 "$c12" "$changelog"

c13=$(repo changelog-plusplus)
w "$c13/CHANGELOG.md" "# Changelog"
cm "$c13" 2020-02-01T00:00:00Z changelog
branch "$c13"
w "$c13/CHANGELOG.md" "# Changelog
++ Added increment operator"
check "changelog: present (entry starting with two pluses)" present 0 "$c13" "$changelog"

c11=$(repo changelog-rm)
w "$c11/CHANGELOG.md" "# Changelog
- one"
cm "$c11" 2020-02-01T00:00:00Z changelog
branch "$c11"
git -C "$c11" rm -q CHANGELOG.md
check "changelog: changed without entry (staged changelog deletion)" "changed without entry" 0 \
	"$c11" "$changelog"

c16=$(repo changelog-rename-only)
w "$c16/CHANGELOG.md" "# Changelog
- one"
cm "$c16" 2020-02-01T00:00:00Z changelog
branch "$c16"
git -C "$c16" mv CHANGELOG.md CHANGELOG
check "changelog: changed without entry (pure rename)" "changed without entry" 0 \
	"$c16" "$changelog"

c17=$(repo changelog-symlink)
printf '%s\n' "private content outside the repository" >"$work/private-target.txt"
ln -s "$work/private-target.txt" "$c17/CHANGELOG.md"
check "changelog: no changelog (untracked symlink)" "no changelog" 2 "$c17" "$changelog"

c18=$(repo changelog-color)
w "$c18/CHANGELOG.md" "# Changelog"
cm "$c18" 2020-02-01T00:00:00Z changelog
branch "$c18"
git -C "$c18" config color.ui always
w "$c18/CHANGELOG.md" "# Changelog
- colored entry"
check "changelog: present (color.ui=always)" present 0 "$c18" "$changelog"

c14=$(repo changelog-noprefix)
w "$c14/CHANGELOG.md" "# Changelog
- one
- two"
cm "$c14" 2020-02-01T00:00:00Z changelog
branch "$c14"
git -C "$c14" config diff.noprefix true
w "$c14/CHANGELOG.md" "# Changelog
- one"
check "changelog: changed without entry (deletion under diff.noprefix)" "changed without entry" 0 \
	"$c14" "$changelog"

c15=$(repo changelog-ambiguous)
w "$c15/CHANGELOG.md" "# Changelog"
w "$c15/src.txt" work
cm "$c15" 2020-02-01T00:00:00Z work
git -C "$c15" branch master
git -C "$c15" checkout -qb work
w "$c15/src.txt" changed
cm "$c15" 2020-03-01T00:00:00Z change
check "changelog: not run (ambiguous default branch)" "not run" 4 "$c15" "$changelog"

c10=$(repo changelog-deleted)
w "$c10/CHANGELOG.md" "# Changelog
- one"
cm "$c10" 2020-02-01T00:00:00Z changelog
branch "$c10"
rm "$c10/CHANGELOG.md"
check "changelog: changed without entry (tracked changelog deleted)" "changed without entry" 0 \
	"$c10" "$changelog"

c9=$(repo changelog-whitespace)
w "$c9/CHANGELOG.md" "# Changelog"
cm "$c9" 2020-02-01T00:00:00Z changelog
branch "$c9"
printf '# Changelog\n   \n' >"$c9/CHANGELOG.md"
check "changelog: changed without entry (whitespace-only addition)" "changed without entry" 0 \
	"$c9" "$changelog"

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
check "evidence: consistent (invoked from a subdirectory)" consistent 0 "$e3/docs" \
	"$evidence" --check-name impl.md notes
w "$e3/widget-report.md" "at the repository root, outside the search root"
check "evidence: stale reference found (match outside search root)" "stale reference found" 0 \
	"$e3" "$evidence" --check-name widget-report.md docs
rm "$e3/notes/impl.md"
check "evidence: stale reference found (deleted from worktree)" "stale reference found" 0 "$e3" \
	"$evidence" --check-name impl.md notes
check "evidence: covered by repo gate" "covered by repo gate" 3 "$e3" "$evidence" --defer ci-evidence
check "evidence: not run (no arguments)" "not run" 2 "$e3" "$evidence"
check "evidence: not run (empty --check-name)" "not run" 2 "$e3" "$evidence" --check-name "" notes
check "evidence: not run (trailing args in name mode)" "not run" 2 "$e3" \
	"$evidence" --check-name impl.md notes extra
check "evidence: not run (repeated --check-name)" "not run" 2 "$e3" \
	"$evidence" --check-name missing.md docs --check-name impl.md notes
check "evidence: not run (one positional only)" "not run" 2 "$e3" "$evidence" logs/run.md
check "evidence: not run (empty --defer)" "not run" 2 "$e3" "$evidence" --defer ""
check "evidence: not run (not a git repository)" "not run" 4 "$nogit" "$evidence" rec.md path.md
check "evidence: not run (bare repository)" "not run" 4 "$bare" "$evidence" rec.md path.md

e4=$(repo evidence-broken)
w "$e4/notes/impl.md" "implementation"
cm "$e4" 2020-02-01T00:00:00Z impl
w "$e4/logs/run.md" "ran the suite"
cm "$e4" 2020-03-01T00:00:00Z record
printf 'not an index' >"$e4/.git/index"
check "evidence: not run (failed git read)" "not run" 4 "$e4" "$evidence" logs/run.md notes/impl.md

# The record is committed first with a deliberately future committer date; a
# later descendant commit dated earlier must still read as stale, because
# ancestry, not the committer clock, decides order.
e6=$(repo evidence-skewed)
w "$e6/logs/run.md" "ran the suite"
cm "$e6" 2030-01-01T00:00:00Z record
w "$e6/notes/impl.md" "implementation"
cm "$e6" 2021-01-01T00:00:00Z impl
check "evidence: stale record found (descendant dated earlier)" "stale record found" 0 "$e6" \
	"$evidence" logs/run.md notes/impl.md

e7=$(repo evidence-quotepath)
w "$e7/docs/café/widget.md" "artifact"
cm "$e7" 2020-02-01T00:00:00Z artifact
check "evidence: consistent (non-ASCII pathname)" consistent 0 "$e7" \
	"$evidence" --check-name widget.md docs

e9=$(repo evidence-newline)
nl='
'
mkdir -p "$e9/docs/has${nl}newline"
w "$e9/docs/has${nl}newline/widget.md" "artifact"
cm "$e9" 2020-02-01T00:00:00Z artifact
check "evidence: not run (pathname with embedded newline)" "not run" 4 "$e9" \
	"$evidence" --check-name widget.md docs

e10=$(repo evidence-sparse)
w "$e10/src/app.md" "dependency"
cm "$e10" 2020-02-01T00:00:00Z impl
w "$e10/logs/run.md" "ran the suite"
cm "$e10" 2020-03-01T00:00:00Z record
git -C "$e10" sparse-checkout set logs 2>/dev/null
check "evidence: fresh (sparse checkout omits described path)" fresh 0 "$e10" \
	"$evidence" logs/run.md src/app.md

e11=$(repo evidence-sparse-record)
w "$e11/src/app.md" "dependency"
cm "$e11" 2020-02-01T00:00:00Z impl
w "$e11/logs/run.md" "ran the suite"
cm "$e11" 2020-03-01T00:00:00Z record
git -C "$e11" sparse-checkout set src 2>/dev/null
check "evidence: fresh (sparse checkout omits the record)" fresh 0 "$e11" \
	"$evidence" logs/run.md src/app.md

e12=$(repo evidence-assume)
w "$e12/notes/impl.md" "implementation"
cm "$e12" 2020-02-01T00:00:00Z impl
w "$e12/logs/run.md" "ran the suite"
cm "$e12" 2020-03-01T00:00:00Z record
w "$e12/notes/impl.md" "edited but hidden"
git -C "$e12" update-index --assume-unchanged notes/impl.md
check "evidence: stale record found (assume-unchanged hides an edit)" "stale record found" 0 \
	"$e12" "$evidence" logs/run.md notes/impl.md

e14=$(repo evidence-assume-record)
w "$e14/notes/impl.md" "implementation"
cm "$e14" 2020-02-01T00:00:00Z impl
w "$e14/logs/run.md" "ran the suite"
cm "$e14" 2020-03-01T00:00:00Z record
w "$e14/logs/run.md" "edited but hidden"
git -C "$e14" update-index --assume-unchanged logs/run.md
check "evidence: record unverifiable (assume-unchanged record)" "record unverifiable (dirty)" 0 \
	"$e14" "$evidence" logs/run.md notes/impl.md

e13=$(repo evidence-sparse-name)
w "$e13/docs/widget.md" "artifact"
w "$e13/src/code.md" "code"
cm "$e13" 2020-02-01T00:00:00Z artifact
git -C "$e13" sparse-checkout set src 2>/dev/null
check "evidence: consistent (sparse checkout omits search root)" consistent 0 "$e13" \
	"$evidence" --check-name widget.md docs

e8=$(repo evidence-ignored)
w "$e8/.gitignore" "docs/widget.md"
cm "$e8" 2020-02-01T00:00:00Z ignore
w "$e8/docs/widget.md" "generated, ignored"
check "evidence: stale reference found (ignored file only)" "stale reference found" 0 "$e8" \
	"$evidence" --check-name widget.md docs

# The record carries a deliberately future committer date: a dirty described
# path must read as stale outright, not be ordered against a skewed clock.
e5=$(repo evidence-dirty-path)
w "$e5/notes/impl.md" "implementation"
cm "$e5" 2020-02-01T00:00:00Z impl
w "$e5/logs/run.md" "ran the suite"
cm "$e5" 2030-01-01T00:00:00Z record
w "$e5/notes/impl.md" "implementation, edited but uncommitted"
check "evidence: stale record found (described path dirty)" "stale record found" 0 "$e5" \
	"$evidence" logs/run.md notes/impl.md

# --- Verdict drift guard -----------------------------------------------------
# Every verdict a helper can emit must appear in the sweep-reference class that
# helper serves — surface-report class 11, changelog-union class 3,
# evidence-freshness classes 2 and 4 — so a verdict surviving elsewhere in the
# reference cannot mask drift in its own class. One direction only:
# reference-side additions are caught by review, not here. Parameterized
# verdicts are checked by their fixed prefix.
ref="$scripts/../references/sweep-classes.md"
if [ -f "$ref" ]; then
	class_block() { # class_block <n> — print the reference's "## <n>." section
		awk -v n="$1" '/^## /{on = ($2 == n".")} on' "$ref"
	}
	check_script_verdicts() { # check_script_verdicts <label> <class-numbers> <file>...
		label="$1"
		classes="$2"
		shift 2
		block=""
		for n in $classes; do
			block="$block
$(class_block "$n")"
		done
		emitted=$({ grep -h "printf 'verdict: " "$@" |
			sed "s/.*printf 'verdict: //;s/\\\\n.*//"
			grep -h '^[[:space:]]*verdict="' "$@" | sed 's/.*verdict="//;s/".*//'
		} | grep -v '^%s$' | sed 's/ for \$.*/ for/' | sort -u)
		while IFS= read -r v; do
			[ -n "$v" ] || continue
			if printf '%s\n' "$block" | grep -qF -- "$v"; then
				printf 'PASS %s: class(es) %s list verdict: %s\n' "$label" "$classes" "$v"
				passed=$((passed + 1))
			else
				printf 'FAIL %s: class(es) %s missing verdict: %s\n' "$label" "$classes" "$v"
				failed=$((failed + 1))
			fi
		done <<DRIFT
$emitted
DRIFT
	}
	check_script_verdicts "surface-report" "11" "$surface"
	check_script_verdicts "changelog-union" "3" "$changelog"
	check_script_verdicts "evidence-freshness" "2 4" "$evidence"
else
	printf 'FAIL sweep reference not found at %s\n' "$ref"
	failed=$((failed + 1))
fi

printf '%s assertions: %s passed, %s failed\n' "$((passed + failed))" "$passed" "$failed"
[ "$failed" -eq 0 ]
