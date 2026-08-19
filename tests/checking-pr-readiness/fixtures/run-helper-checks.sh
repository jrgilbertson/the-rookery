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
nl='
'

passed=0
failed=0

# Every verdict line a helper emits is recorded with its exit code, so the
# exit-map pin at the end can hold the whole run against the reference table.
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

# The listing, flag, and cap checks below assert on the detail lines, not only
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

says() { # says <state> <exact line>
	if printf '%s\n' "$run_out" | grep -qFx -- "$2"; then ok "$1"; else
		no "$1" "no line [$2]"
	fi
}

mentions_text() { # mentions_text <state> <substring>
	if printf '%s\n' "$run_out" | grep -qF -- "$2"; then ok "$1"; else
		no "$1" "output does not carry [$2]"
	fi
}

omits() { # omits <state> <substring that must not appear>
	if printf '%s\n' "$run_out" | grep -qF -- "$2"; then
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
check "surface: not run (control character in cap name)" "not run" 2 "$s1" "$surface" \
	--cap "reviewer${nl}forged=1"
long_cap_name=$(printf 'r%.0s' $(seq 1 65))
check "surface: not run (cap name too long)" "not run" 2 "$s1" "$surface" \
	--cap "${long_cap_name}=1"
check "surface: not run (cap beyond integer range)" "not run" 2 "$s1" "$surface" \
	--cap "reviewer=999999999999999999999999999999999999"

s2=$(repo surface-clean)
check "surface: no changes on surface" "no changes on surface" 0 "$s2" "$surface" --cap reviewer=10

s3=$(repo surface-unresolved feature)
w "$s3/staged.txt" staged
git -C "$s3" add -A
check "surface: cap unverified (committed unmeasured)" "cap unverified" 0 "$s3" "$surface" --cap reviewer=10

s7=$(repo surface-tag-main develop)
w "$s7/src.txt" work
cm "$s7" 2020-02-01T00:00:00Z work
git -C "$s7" tag main
check "surface: cap unverified (tag named main is not a branch)" "cap unverified" 0 \
	"$s7" "$surface" --cap reviewer=10

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
check "surface: not run (control character in --defer)" "not run" 2 "$s1" "$surface" \
	--defer "ci${nl}verdict: forged"
long_defer=$(printf 'g%.0s' $(seq 1 129))
check "surface: not run (--defer too long)" "not run" 2 "$s1" "$surface" --defer "$long_defer"

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
check "changelog: not run (control character in --defer)" "not run" 2 "$c6" "$changelog" \
	--defer "ci${nl}verdict: forged"
check "changelog: not run (--defer too long)" "not run" 2 "$c6" "$changelog" --defer "$long_defer"
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

c19=$(repo changelog-symlink-staged)
ln -s "$work/private-target.txt" "$c19/CHANGELOG.md"
git -C "$c19" add CHANGELOG.md
check "changelog: no changelog (staged symlink)" "no changelog" 2 "$c19" "$changelog"

c20=$(repo changelog-conflict)
w "$c20/CHANGELOG.md" "# Changelog"
cm "$c20" 2020-02-01T00:00:00Z changelog
branch "$c20"
w "$c20/CHANGELOG.md" "# Changelog
- ours"
cm "$c20" 2020-03-01T00:00:00Z ours
git -C "$c20" checkout -q main
w "$c20/CHANGELOG.md" "# Changelog
- theirs"
cm "$c20" 2020-03-02T00:00:00Z theirs
git -C "$c20" checkout -q work
git -C "$c20" merge -q main >/dev/null 2>&1 || true
check "changelog: not run (unresolved merge conflict)" "not run" 4 "$c20" "$changelog"

c21=$(repo changelog-plusplus-b)
w "$c21/CHANGELOG.md" "# Changelog"
cm "$c21" 2020-02-01T00:00:00Z changelog
branch "$c21"
w "$c21/CHANGELOG.md" "# Changelog
++ b/release note"
check "changelog: present (entry starting with ++ b/)" present 0 "$c21" "$changelog"

c22=$(repo changelog-tag-main develop)
w "$c22/CHANGELOG.md" "# Changelog"
w "$c22/src.txt" work
cm "$c22" 2020-02-01T00:00:00Z work
git -C "$c22" tag main
check "changelog: not run (tag named main is not a branch)" "not run" 4 "$c22" "$changelog"

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
check "evidence: not run (control character in --defer)" "not run" 2 "$e3" "$evidence" \
	--defer "ci${nl}verdict: forged"
check "evidence: not run (--defer too long)" "not run" 2 "$e3" "$evidence" --defer "$long_defer"
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

e17=$(repo evidence-symlink-inputs)
w "$e17/notes/impl.md" "implementation"
cm "$e17" 2020-02-01T00:00:00Z impl
w "$e17/logs/run.md" "ran the suite"
cm "$e17" 2020-03-01T00:00:00Z record
ln -s "$work/private-target.txt" "$e17/logs/linked.md"
ln -s "$work/private-target.txt" "$e17/notes/linked.md"
ln -s "$work" "$e17/linked-search-root"
check "evidence: not run (symlink record)" "not run" 4 "$e17" \
	"$evidence" logs/linked.md notes/impl.md
check "evidence: not run (symlink described path)" "not run" 4 "$e17" \
	"$evidence" logs/run.md notes/linked.md
check "evidence: not run (symlink search root)" "not run" 4 "$e17" \
	"$evidence" --check-name private-target.txt linked-search-root
check "evidence: not run (record outside repository)" "not run" 4 "$e17" \
	"$evidence" ../private-target.txt notes/impl.md
check "evidence: not run (search root outside repository)" "not run" 4 "$e17" \
	"$evidence" --check-name private-target.txt "$work"

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

run "$s8" "$surface" --cap reviewer=1000
exits "surface: 500 untracked paths report (not SIGPIPE)" 0
says "surface: verdict survives the capped listing" "verdict: under caps"
says "surface: untracked count is exact" "untracked: 500"
says "surface: total is exact" "total distinct changed files: 500"
lines_matching "surface: 25 paths listed under the cap" "^  ${pad}-" 25
says "surface: the remainder is named" "  … and 475 more (--full lists every path)"

run "$s8" "$surface" --cap reviewer=1000 --full
exits "surface: --full over 500 paths" 0
lines_matching "surface: --full lists every path" "^  ${pad}-" 500
omits "surface: --full drops the remainder line" "… and "

# --- --merge-base validation --------------------------------------------------
# A supplied merge base decides the committed category on its own, so an
# unchecked one is a silent pass: HEAD passed here empties the committed diff
# and branch work reads as an empty surface (surface-report) or as `missing`
# (changelog-union). Both helpers must refuse instead.

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

for helper_name in surface changelog; do
	case "$helper_name" in
	surface) helper="$surface" ;;
	changelog) helper="$changelog" ;;
	esac

	plain=$(cd "$mb" && "$helper" 2>&1)
	flagged=$(cd "$mb" && "$helper" --merge-base "$true_mb" 2>&1)
	if [ "$plain" = "$flagged" ]; then
		ok "$helper_name: --merge-base at the true merge base matches the unflagged run"
	else
		no "$helper_name: --merge-base at the true merge base matches the unflagged run" \
			"outputs differ: $(printf '%s\n' "$flagged" | sed -n '1p')"
	fi

	run "$mb" "$helper" --merge-base HEAD
	exits "$helper_name: --merge-base HEAD refused" 4
	says "$helper_name: --merge-base HEAD reports not run" "verdict: not run"
	mentions_text "$helper_name: --merge-base HEAD names the mismatch" \
		"does not match merge-base(HEAD,"

	run "$mb" "$helper" --merge-base "$side_sha"
	exits "$helper_name: --merge-base off the branch refused" 4
	says "$helper_name: --merge-base off the branch reports not run" "verdict: not run"
done

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
run "$nb" "$changelog" --merge-base "$other_sha"
exits "changelog: non-ancestor --merge-base refused with no base to check against" 4
mentions_text "changelog: non-ancestor --merge-base names the ancestry test" \
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

run "$bt" "$changelog" --base main
exits "changelog: --base main measures against the branch, not the tag" 0
says "changelog: --base main sees the branch work" "verdict: missing"
says "changelog: --base main counts the branch commit" "changed non-changelog files: 1"

for helper_name in surface changelog; do
	case "$helper_name" in
	surface) helper="$surface" ;;
	changelog) helper="$changelog" ;;
	esac

	run "$bt" "$helper" --base v1.0
	exits "$helper_name: --base naming only a tag refused" 4
	says "$helper_name: --base naming only a tag reports not run" "verdict: not run"
	mentions_text "$helper_name: --base naming only a tag names the ref" \
		"the supplied --base v1.0 resolves to no branch"

	run "$bt" "$helper" --base no-such-ref
	exits "$helper_name: --base resolving to no branch refused" 4
	says "$helper_name: --base resolving to no branch reports not run" "verdict: not run"
done

# --- Mentions cap and the untracked search -------------------------------------
# Same SIGPIPE exposure as the surface listing, on the other capped listing:
# 900 mentioning files put roughly 170 KiB through it.

e15=$(repo evidence-mentions-cap)
i=1
while [ "$i" -le 900 ]; do
	w "$e15/docs/${pad}-$i.md" "the plan proposes widget-report.md"
	i=$((i + 1))
done
run "$e15" "$evidence" --check-name widget-report.md docs
exits "evidence: 900 mentioning files report (not SIGPIPE)" 0
says "evidence: verdict survives the capped mentions listing" "verdict: stale reference found"
lines_matching "evidence: 10 mentions listed under the cap" "^  docs/${pad}-" 10
says "evidence: the remainder is named" "  … and 890 more"

# The mentions search reaches untracked files without walking ignored trees.
e16=$(repo evidence-mentions-untracked)
w "$e16/.gitignore" "vendor/"
cm "$e16" 2020-02-01T00:00:00Z ignore
w "$e16/docs/note.md" "the plan proposes widget-report.md"
w "$e16/vendor/generated.md" "a build artifact naming widget-report.md"
run "$e16" "$evidence" --check-name widget-report.md .
exits "evidence: untracked mention search" 0
says "evidence: untracked mention is found" "  docs/note.md"
omits "evidence: ignored tree is not searched" "vendor/generated.md"

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

# --- Helper exit → status word pin -------------------------------------------
# A class verdict and the gate's status word are two layers, and the mapping
# between them is the SSOT table in the sweep reference. Every (verdict, exit)
# pair this run observed is held against that table, so a helper that starts
# returning a different exit for a verdict — or a table row that disappears —
# fails here instead of quietly changing what the gate reports.
if [ -f "$ref" ]; then
	for row in "| 0 |" "| 2 with absent-input verdict" "| 2 with \`not run\`" "| 3 |" "| 4 |"; do
		if grep -qF -- "$row" "$ref"; then
			ok "exit map: the table still carries the row for ${row}"
		else
			no "exit map: the table still carries the row for ${row}" "row missing from the reference"
		fi
	done
	# The exit-2 row names the absent-input verdicts itself, so the pin reads
	# them from the table rather than restating them here.
	# The backticks are literal Markdown delimiters.
	# shellcheck disable=SC2016
	absent_verdicts=$(grep -F '2 with absent-input verdict' "$ref" |
		grep -o '`[^`]*`' | tr -d '`')
	observed=$(sort -u "$work/observed")
	while IFS='|' read -r verdict code; do
		[ -n "$verdict" ] || continue
		label="exit map: ${verdict} at exit ${code}"
		case "$code" in
		0)
			# The gate verdict is checked in both directions: it is exit 3's
			# verdict and only exit 3's, or `skipped` stops meaning deferred.
			if [ "$verdict" = "not run" ]; then
				no "$label" "exit 0 carries a class verdict, never 'not run'"
			elif [ "$verdict" = "covered by repo gate" ]; then
				no "$label" "the gate verdict belongs to exit 3, which the gate reads as 'skipped'"
			else ok "$label"; fi
			;;
		2)
			if [ "$verdict" = "not run" ] ||
				printf '%s\n' "$absent_verdicts" | grep -qFx -- "$verdict"; then
				ok "$label"
			else
				no "$label" "exit 2 is a usage error ('not run') or an absent-input verdict the table names"
			fi
			;;
		3)
			if [ "$verdict" = "covered by repo gate" ]; then ok "$label"; else
				no "$label" "exit 3 is the --defer gate verdict"
			fi
			;;
		4)
			if [ "$verdict" = "not run" ]; then ok "$label"; else
				no "$label" "exit 4 is a helper hard failure, which reports 'not run'"
			fi
			;;
		*)
			no "$label" "the table maps exits 0, 2, 3, and 4 only"
			;;
		esac
	done <<MAP
$observed
MAP
	# A pin over pairs that never occurred proves nothing, so every mapped exit
	# has to have been exercised above.
	for want in 0 2 3 4; do
		if printf '%s\n' "$observed" | grep -q "|${want}\$"; then
			ok "exit map: exit $want was exercised"
		else
			no "exit map: exit $want was exercised" "no helper run in this suite returned it"
		fi
	done
else
	no "exit map: sweep reference not found" "expected at $ref"
fi

printf '%s assertions: %s passed, %s failed\n' "$((passed + failed))" "$passed" "$failed"
[ "$failed" -eq 0 ]
