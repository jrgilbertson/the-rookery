#!/usr/bin/env bash
#
# evidence-freshness.sh — records that predate the final edit they describe,
# and plan-named artifacts that no longer match what shipped.
#
# Serves sweep class 4 (evidence or test records predating the final edit) and
# supports class 2 (stale cross-references) in references/sweep-classes.md.
#
# Order comes from commit ancestry, never committer timestamps or filesystem
# mtimes: a checkout stamps every file with the same recent mtime, and a skewed
# or rewritten committer clock can date a later commit earlier, so a described
# path is fresh only when its last commit is contained in the history of the
# record's last commit. A described path that is dirty in the working tree
# (staged, unstaged, or untracked) is stale outright: the edit happened after
# any committed record.
#
# Relative paths are resolved from the repository root, matching the other
# bundled helpers.
#
# The record itself is held to a stricter rule: its time always comes from its
# last commit. A dirty record has no established write time, so it cannot prove
# anything is fresh — treating it as written now would let a record and the path
# it describes both be dirty and rate as fresh against each other.
#
# Usage:
#   evidence-freshness.sh <record-file> <described-path>...
#   evidence-freshness.sh --check-name <name> <search-root>
#   evidence-freshness.sh --defer <gate-name>
#   evidence-freshness.sh --help
#
# Output states. Line 1 is always `verdict: <word>`; human detail follows.
#
#   verdict: fresh                  exit 0  every described path's last commit
#                                           is contained in the history of the
#                                           record's last commit
#   verdict: stale record found     exit 0  a described path changed after the
#                                           record — its last commit descends
#                                           from the record's, it is dirty in
#                                           the working tree, or its history is
#                                           incomparable with the record's; the
#                                           detail names the path and commits.
#                                           Also emitted when a described path
#                                           is missing from the working tree, or
#                                           has no git history to compare
#                                           against — a record describing
#                                           something that no longer exists is
#                                           stale, not fresh — and when the
#                                           record itself has git history but
#                                           is gone from the working tree
#   verdict: record unverifiable (dirty)  exit 0  the record is dirty in the working
#             (dirty)                       tree, so its own write time cannot be
#                                           established. A record that cannot be
#                                           dated proves nothing fresh
#   verdict: consistent             exit 0  --check-name matched a file on the
#                                           working surface under the search root
#                                           whose basename or path suffix is the
#                                           name; the detail also lists any docs
#                                           mentioning it
#   verdict: stale reference found  exit 0  --check-name matched no such file: a
#                                           plan-named artifact that does not
#                                           match what shipped. A name that is
#                                           only mentioned in prose, with no file
#                                           behind it, lands here
#   verdict: no records             exit 2  the record file is absent — neither
#                                           committed nor present in the working
#                                           tree — or the --check-name search
#                                           root does not exist. Absent input is
#                                           not a pass
#   verdict: covered by repo gate   exit 3  --defer named a repository-owned
#                                           check; nothing was compared
#   verdict: not run                exit 2  usage error, including no arguments
#   verdict: not run                exit 4  git is unavailable, this is not a
#                                           git repository, or a git read the
#                                           comparison needs failed. A failed
#                                           read is never reported as a clean
#                                           status or an empty listing
#
# Dependencies: git and standard POSIX tools. No network, no jq, no node.

set -euo pipefail

usage() {
	cat <<'EOF'
evidence-freshness.sh — stale-record and stale-name check

Usage:
  evidence-freshness.sh <record-file> <described-path>...
  evidence-freshness.sh --check-name <name> <search-root>
  evidence-freshness.sh --defer <gate-name>
  evidence-freshness.sh --help

  <record-file>       A log, run record, or recorded result.
  <described-path>    A path that record describes. Repeatable.
  --check-name        Look under <search-root> for a file whose basename or
                      path suffix is the literal <name>, and report whether a
                      plan-named artifact still matches what shipped. Takes no
                      further arguments.
  --defer <gate-name> Report this class as owned by the named repository gate
                      and compare nothing (exit 3).
  --help              Print this text and exit 0.

Verdicts: fresh | stale record found | record unverifiable (dirty) |
          consistent | stale reference found | no records |
          covered by repo gate | not run
EOF
}

fail_usage() {
	printf 'verdict: not run\n'
	printf 'reason: %s\n' "$1"
	usage
	exit 2
}

if [ "$#" -eq 0 ]; then
	fail_usage "no arguments given"
fi

defer_gate=""
check_name=""
search_root=""
mode="freshness"
positional_count=0
record=""
described=""

while [ "$#" -gt 0 ]; do
	case "$1" in
	--help | -h)
		usage
		exit 0
		;;
	--defer)
		[ "$#" -ge 2 ] || fail_usage "--defer requires a gate name"
		[ -n "$2" ] || fail_usage "--defer requires a non-empty gate name"
		defer_gate="$2"
		shift 2
		;;
	--check-name)
		[ "$#" -ge 3 ] || fail_usage "--check-name requires <name> <search-root>"
		[ "$mode" != "name" ] || fail_usage "--check-name given more than once; run one check per invocation"
		mode="name"
		check_name="$2"
		search_root="$3"
		shift 3
		;;
	-*)
		fail_usage "unknown option: $1"
		;;
	*)
		positional_count=$((positional_count + 1))
		if [ "$positional_count" -eq 1 ]; then
			record="$1"
		else
			described="${described}${1}
"
		fi
		shift
		;;
	esac
done

if [ -n "$defer_gate" ]; then
	printf 'verdict: covered by repo gate\n'
	printf 'gate: %s\n' "$defer_gate"
	printf 'detail: record freshness not compared here; the named repository gate owns this class.\n'
	exit 3
fi

if [ "$mode" = "name" ]; then
	# An empty name matches every path, so it would confirm anything.
	[ -n "$check_name" ] || fail_usage "--check-name requires a non-empty <name>"
	[ -n "$search_root" ] || fail_usage "--check-name requires a non-empty <search-root>"
	[ "$positional_count" -eq 0 ] || fail_usage "--check-name takes no arguments beyond <name> <search-root>"
fi

if ! command -v git >/dev/null 2>&1; then
	printf 'verdict: not run\n'
	printf 'reason: git is not available on PATH\n'
	exit 4
fi

if ! git rev-parse --git-dir >/dev/null 2>&1; then
	printf 'verdict: not run\n'
	printf 'reason: not inside a git repository\n'
	exit 4
fi

if [ "$(git rev-parse --is-inside-work-tree 2>/dev/null)" != "true" ]; then
	printf 'verdict: not run\n'
	printf 'reason: not inside a git work tree (a bare repository has no working surface to check)\n'
	exit 4
fi

cd "$(git rev-parse --show-toplevel)"

fail_read() {
	printf 'verdict: not run\n'
	printf 'reason: the %s read could not be completed: %s\n' "$1" "$2"
	printf 'detail: a failed git read is not a clean status or an empty listing, so no freshness verdict is reported.\n'
	exit 4
}

# Every git read the comparison depends on goes through this: an empty result
# and a failed read look identical once the status is discarded, and a failed
# status read reported as "clean" would let a dirty record rate as fresh.
git_out=""
read_or_fail() {
	enumeration="$1"
	shift
	if ! git_out=$(git "$@" 2>/dev/null); then
		fail_read "$enumeration" "git $* returned non-zero"
	fi
}

iso_of() {
	date -u -r "$1" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null ||
		date -u -d "@$1" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null ||
		printf 'epoch:%s\n' "$1"
}

if [ "$mode" = "name" ]; then
	if [ ! -e "$search_root" ]; then
		read_or_fail "index listing" ls-files -- "$search_root"
		if [ -z "$git_out" ]; then
			printf 'verdict: no records\n'
			printf 'search root missing: %s\n' "$search_root"
			printf 'detail: nothing could be searched, so the name was neither confirmed nor refuted.\n'
			exit 2
		fi
		# Absent on disk but present in the index: a sparse-checkout cone can
		# omit the root while its tracked artifacts live on.
	fi
	# Existence is decided by paths, not by prose. A content grep matches the
	# plan that proposed the name as readily as the artifact that shipped — and
	# matches the file naming itself — so the name is matched against the paths
	# on the working surface, and the content hits are reported as detail only.
	# core.quotepath=false keeps non-ASCII pathnames raw instead of C-quoted,
	# so the existence test and suffix match see the real path.
	read_or_fail "search-root listing" -c core.quotepath=false ls-files --cached --others --exclude-standard -- "$search_root"
	surface="$git_out"
	matches=""
	while IFS= read -r candidate; do
		[ -n "$candidate" ] || continue
		# A pathname git had to C-quote even with quotepath off carries an
		# embedded control character (a newline breaks line-by-line parsing
		# outright), so the listing cannot be trusted — fail closed.
		case "$candidate" in
		\"*) fail_read "search-root listing" "a pathname required C-quoting, so the listing cannot be parsed line by line" ;;
		esac
		# An index entry deleted from the working tree ships as a deletion, so
		# it does not count as a shipped artifact; only a regular file does —
		# or a tracked path a sparse-checkout cone omits (absent from the
		# worktree yet clean in status). Paths outside this enumerated
		# surface — ignored files, directories — never count, which is why
		# there is no filesystem fallback here.
		if [ ! -f "$candidate" ]; then
			read_or_fail "index listing" ls-files -- "$candidate"
			[ -n "$git_out" ] || continue
			read_or_fail "working-tree status" status --porcelain -- "$candidate"
			[ -z "$git_out" ] || continue
		fi
		case "$candidate" in
		"$check_name" | */"$check_name")
			matches="${matches}${candidate}
"
			;;
		esac
	done <<EOF
$surface
EOF

	mentions=$(grep -rlF --exclude-dir=.git -e "$check_name" -- "$search_root" 2>/dev/null || true)

	if [ -z "$matches" ]; then
		printf 'verdict: stale reference found\n'
		printf 'name: %s\n' "$check_name"
		printf 'search root: %s\n' "$search_root"
		printf 'detail: no file under the search root carries this name.\n'
		if [ -n "$mentions" ]; then
			printf 'detail: the name is mentioned but nothing shipped under it; mentioned in:\n'
			printf '%s\n' "$mentions" | sed 's/^/  /'
		fi
		exit 0
	fi
	printf 'verdict: consistent\n'
	printf 'name: %s\n' "$check_name"
	printf 'search root: %s\n' "$search_root"
	printf 'files with this name:\n'
	printf '%s' "$matches" | sed 's/^/  /'
	if [ -n "$mentions" ]; then
		printf 'mentioned in:\n'
		printf '%s\n' "$mentions" | sed 's/^/  /'
	fi
	exit 0
fi

if [ "$positional_count" -lt 2 ]; then
	fail_usage "expected <record-file> and at least one <described-path>"
fi

# Called from the current shell, never through a command substitution, so a
# failed status read exits with the fail_read verdict instead of having it
# captured as text.
is_dirty() {
	read_or_fail "working-tree status" status --porcelain -- "$1"
	[ -n "$git_out" ]
}

# An index entry marked assume-unchanged (lowercase tag) or skip-worktree (S)
# suppresses status output, so a clean status there is no evidence of a clean
# file. Current-shell only, like is_dirty.
status_suppressed() {
	read_or_fail "index flags" ls-files -v -- "$1"
	# Explicit characters, not [a-z]: locale collation can pull uppercase
	# letters into a lowercase range and misread every ordinary H entry.
	case "$git_out" in
	[hsmrck]* | S*) return 0 ;;
	esac
	return 1
}

# An unborn repository has no commits to date anything by; that is legitimate
# empty history, distinct from a read that failed.
head_exists=0
if git rev-parse --verify --quiet HEAD >/dev/null 2>&1; then
	head_exists=1
fi

# Last commit that touched a path; empty when the path has no committed
# history. Also current-shell only, for the same reason as is_dirty.
last_commit=""
read_last_commit() {
	last_commit=""
	if [ "$head_exists" -eq 1 ]; then
		read_or_fail "commit history" rev-list -1 HEAD -- "$1"
		last_commit="$git_out"
	fi
}

# Ancestry, not committer timestamps, decides order: a skewed or rewritten
# committer clock can date a later commit earlier, and wall-clock ordering is
# refused for dirty paths above for the same reason.
# Return 0 = ancestor, 1 = not an ancestor; any other status is a failed read.
is_ancestor() {
	git merge-base --is-ancestor "$1" "$2" 2>/dev/null
	ancestor_rc=$?
	[ "$ancestor_rc" -le 1 ] ||
		fail_read "commit ancestry" "git merge-base --is-ancestor returned status $ancestor_rc"
	return "$ancestor_rc"
}

# The record is dated by its last commit only. A record with no established
# committed write point must not certify anything as fresh.
read_last_commit "$record"
record_commit="$last_commit"

record_sparse=0
if [ ! -e "$record" ]; then
	read_or_fail "index listing" ls-files -- "$record"
	record_tracked="$git_out"
	read_or_fail "working-tree status" status --porcelain -- "$record"
	if [ -n "$record_tracked" ] && [ -z "$git_out" ]; then
		# Tracked, absent, and clean in status: a sparse-checkout omission,
		# not a deletion — the record lives on in history and dates normally.
		record_sparse=1
	elif [ -n "$record_commit" ]; then
		printf 'verdict: stale record found\n'
		printf 'record missing: %s\n' "$record"
		printf 'detail: record existed in history but is gone from the working tree.\n'
		exit 0
	else
		printf 'verdict: no records\n'
		printf 'record missing: %s\n' "$record"
		printf 'detail: the record is neither committed nor present in the working tree, so freshness could not be checked.\n'
		exit 2
	fi
fi

record_undatable=0
if [ -z "$record_commit" ]; then
	record_undatable=1
elif [ "$record_sparse" -eq 0 ]; then
	if is_dirty "$record" || status_suppressed "$record"; then
		record_undatable=1
	fi
fi
if [ "$record_undatable" -eq 1 ]; then
	printf 'verdict: record unverifiable (dirty)\n'
	printf 'record: %s\n' "$record"
	printf 'detail: the record is uncommitted in the working tree, or its status is suppressed (assume-unchanged or skip-worktree), so its own write point cannot be established.\n'
	printf 'detail: commit the record and clear any index flags, then re-run; an undatable record cannot prove a described path fresh.\n'
	exit 0
fi

read_or_fail "commit history" log -1 --format=%ct "$record_commit"
record_time="$git_out"

stale_lines=""
fresh_lines=""
while IFS= read -r path; do
	[ -n "$path" ] || continue
	if [ ! -e "$path" ]; then
		read_or_fail "index listing" ls-files -- "$path"
		tracked_entry="$git_out"
		read_or_fail "working-tree status" status --porcelain -- "$path"
		if [ -z "$tracked_entry" ] || [ -n "$git_out" ]; then
			stale_lines="${stale_lines}described path missing: ${path}
"
			continue
		fi
		# Tracked, absent, and clean in status: a sparse-checkout omission,
		# not a deletion — the path lives on in history, so it is compared
		# by ancestry like any committed path.
	elif is_dirty "$path"; then
		stale_lines="${stale_lines}stale: ${path} is dirty in the working tree, so it was edited after any committed record
"
		continue
	elif status_suppressed "$path"; then
		stale_lines="${stale_lines}stale: ${path} has its status suppressed (assume-unchanged or skip-worktree), so a hidden edit cannot be ruled out (freshness cannot be proven)
"
		continue
	fi
	read_last_commit "$path"
	path_commit="$last_commit"
	if [ -z "$path_commit" ]; then
		stale_lines="${stale_lines}described path has no git history: ${path} (freshness cannot be proven)
"
		continue
	fi
	if [ "$path_commit" = "$record_commit" ]; then
		fresh_lines="${fresh_lines}described: ${path} last changed in the record's own commit
"
	elif is_ancestor "$path_commit" "$record_commit"; then
		fresh_lines="${fresh_lines}described: ${path} last changed in $(printf '%.7s' "$path_commit"), within the record's history
"
	elif is_ancestor "$record_commit" "$path_commit"; then
		stale_lines="${stale_lines}stale: ${path} last changed in $(printf '%.7s' "$path_commit"), after the record's last commit $(printf '%.7s' "$record_commit")
"
	else
		stale_lines="${stale_lines}stale: ${path} last changed in $(printf '%.7s' "$path_commit"), on a history incomparable with the record's last commit (freshness cannot be proven)
"
	fi
done <<EOF
$described
EOF

if [ -n "$stale_lines" ]; then
	printf 'verdict: stale record found\n'
else
	printf 'verdict: fresh\n'
fi
printf 'record: %s last committed %s in %.7s\n' "$record" "$(iso_of "$record_time")" "$record_commit"
[ -z "$stale_lines" ] || printf '%s' "$stale_lines"
[ -z "$fresh_lines" ] || printf '%s' "$fresh_lines"
exit 0
