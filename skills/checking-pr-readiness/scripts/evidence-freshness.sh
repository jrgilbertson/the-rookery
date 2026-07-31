#!/usr/bin/env bash
#
# evidence-freshness.sh — records that predate the final edit they describe,
# and plan-named artifacts that no longer match what shipped.
#
# Serves sweep class 4 (evidence or test records predating the final edit) and
# supports class 2 (stale cross-references) in references/sweep-classes.md.
#
# Times come from git commit history, never from filesystem mtimes: a worktree
# checkout or a copy stamps every file with the same recent mtime, which would
# make every record look fresh. A described path that is dirty in the working
# tree (staged, unstaged, or untracked) counts as edited now, because the edit
# has happened even though no commit records it yet.
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
#   verdict: fresh                  exit 0  the record's commit time is at or
#                                           after the last edit of every
#                                           described path
#   verdict: stale record found     exit 0  a described path was edited after the
#                                           record; the detail names that path
#                                           and both ISO timestamps. Also emitted
#                                           when a described path is missing from
#                                           the working tree, or has no git
#                                           history to compare against — a record
#                                           describing something that no longer
#                                           exists is stale, not fresh — and when
#                                           the record itself has git history but
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
#   verdict: not run                exit 4  git is unavailable, or this is not a
#                                           git repository
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
		defer_gate="$2"
		shift 2
		;;
	--check-name)
		[ "$#" -ge 3 ] || fail_usage "--check-name requires <name> <search-root>"
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

iso_of() {
	date -u -r "$1" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null ||
		date -u -d "@$1" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null ||
		printf 'epoch:%s\n' "$1"
}

if [ "$mode" = "name" ]; then
	if [ ! -e "$search_root" ]; then
		printf 'verdict: no records\n'
		printf 'search root missing: %s\n' "$search_root"
		printf 'detail: nothing could be searched, so the name was neither confirmed nor refuted.\n'
		exit 2
	fi
	# Existence is decided by paths, not by prose. A content grep matches the
	# plan that proposed the name as readily as the artifact that shipped — and
	# matches the file naming itself — so the name is matched against the paths
	# on the working surface, and the content hits are reported as detail only.
	surface=$(git ls-files --cached --others --exclude-standard -- "$search_root" 2>/dev/null || true)
	matches=""
	while IFS= read -r candidate; do
		[ -n "$candidate" ] || continue
		case "$candidate" in
		"$check_name" | */"$check_name")
			matches="${matches}${candidate}
"
			;;
		esac
	done <<EOF
$surface
EOF
	for candidate in "$search_root/$check_name" "$check_name"; do
		if [ -e "$candidate" ]; then
			printf '%s\n' "$matches" | grep -Fx -- "$candidate" >/dev/null ||
				matches="${matches}${candidate}
"
		fi
	done

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

now=$(date +%s)

is_dirty() {
	[ -n "$(git status --porcelain -- "$1" 2>/dev/null || true)" ]
}

# Last edit time of a described path: now when it is dirty in the working tree,
# otherwise the commit time of its last commit. Empty when neither applies.
last_edit_of() {
	if is_dirty "$1"; then
		printf '%s\n' "$now"
		return 0
	fi
	git log -1 --format=%ct -- "$1" 2>/dev/null || true
}

# The record is dated by its last commit only. `now` is never substituted here:
# a record with no established write time must not certify anything as fresh.
record_time=$(git log -1 --format=%ct -- "$record" 2>/dev/null || true)

if [ ! -e "$record" ]; then
	if [ -n "$record_time" ]; then
		printf 'verdict: stale record found\n'
		printf 'record missing: %s\n' "$record"
		printf 'detail: record existed in history but is gone from the working tree.\n'
		exit 0
	fi
	printf 'verdict: no records\n'
	printf 'record missing: %s\n' "$record"
	printf 'detail: the record is neither committed nor present in the working tree, so freshness could not be checked.\n'
	exit 2
fi

if is_dirty "$record" || [ -z "$record_time" ]; then
	printf 'verdict: record unverifiable (dirty)\n'
	printf 'record: %s\n' "$record"
	printf 'detail: the record is uncommitted in the working tree, so its own write time cannot be established.\n'
	printf 'detail: commit the record, then re-run; an undatable record cannot prove a described path fresh.\n'
	exit 0
fi

stale_lines=""
fresh_lines=""
while IFS= read -r path; do
	[ -n "$path" ] || continue
	if [ ! -e "$path" ]; then
		stale_lines="${stale_lines}described path missing: ${path}
"
		continue
	fi
	path_time=$(last_edit_of "$path")
	if [ -z "$path_time" ]; then
		stale_lines="${stale_lines}described path has no git history: ${path} (freshness cannot be proven)
"
		continue
	fi
	if [ "$path_time" -gt "$record_time" ]; then
		stale_lines="${stale_lines}stale: ${path} edited $(iso_of "$path_time"), after the record at $(iso_of "$record_time")
"
	else
		fresh_lines="${fresh_lines}described: ${path} last edited $(iso_of "$path_time"), at or before the record
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
printf 'record: %s last committed %s\n' "$record" "$(iso_of "$record_time")"
[ -z "$stale_lines" ] || printf '%s' "$stale_lines"
[ -z "$fresh_lines" ] || printf '%s' "$fresh_lines"
exit 0
