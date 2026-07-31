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
# Usage:
#   evidence-freshness.sh <record-file> <described-path>...
#   evidence-freshness.sh --check-name <name> <search-root>
#   evidence-freshness.sh --defer <gate-name>
#   evidence-freshness.sh --help
#
# Output states. Line 1 is always `verdict: <word>`; human detail follows.
#
#   verdict: fresh                  exit 0  the record's time is at or after the
#                                           last edit of every described path
#   verdict: stale record found     exit 0  a described path was edited after the
#                                           record; the detail names that path
#                                           and both ISO timestamps. Also emitted
#                                           when a described path is missing from
#                                           the working tree, or has no git
#                                           history to compare against — a record
#                                           describing something that no longer
#                                           exists is stale, not fresh
#   verdict: consistent             exit 0  --check-name found the literal name
#                                           under the search root
#   verdict: stale reference found  exit 0  --check-name found zero hits: a
#                                           plan-named artifact that does not
#                                           match what shipped
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
  --check-name        Search <search-root> for the literal <name> and report
                      whether a plan-named artifact still matches what shipped.
  --defer <gate-name> Report this class as owned by the named repository gate
                      and compare nothing (exit 3).
  --help              Print this text and exit 0.

Verdicts: fresh | stale record found | consistent | stale reference found |
          no records | covered by repo gate | not run
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
	hits=$(grep -rlF --exclude-dir=.git -e "$check_name" -- "$search_root" 2>/dev/null || true)
	if [ -z "$hits" ]; then
		printf 'verdict: stale reference found\n'
		printf 'name: %s\n' "$check_name"
		printf 'search root: %s\n' "$search_root"
		printf 'detail: zero files under the search root contain this literal name.\n'
		exit 0
	fi
	printf 'verdict: consistent\n'
	printf 'name: %s\n' "$check_name"
	printf 'search root: %s\n' "$search_root"
	printf 'found in:\n'
	printf '%s\n' "$hits" | sed 's/^/  /'
	exit 0
fi

if [ "$positional_count" -lt 2 ]; then
	fail_usage "expected <record-file> and at least one <described-path>"
fi

now=$(date +%s)

# Last edit time of a path: now when it is dirty in the working tree, otherwise
# the commit time of its last commit. Empty when neither applies.
last_edit_of() {
	if [ -n "$(git status --porcelain -- "$1" 2>/dev/null || true)" ]; then
		printf '%s\n' "$now"
		return 0
	fi
	git log -1 --format=%ct -- "$1" 2>/dev/null || true
}

record_time=$(last_edit_of "$record")
if [ -z "$record_time" ] && [ ! -e "$record" ]; then
	printf 'verdict: no records\n'
	printf 'record missing: %s\n' "$record"
	printf 'detail: the record is neither committed nor present in the working tree, so freshness could not be checked.\n'
	exit 2
fi
if [ -z "$record_time" ]; then
	record_time="$now"
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
printf 'record: %s last written %s\n' "$record" "$(iso_of "$record_time")"
[ -z "$stale_lines" ] || printf '%s' "$stale_lines"
[ -z "$fresh_lines" ] || printf '%s' "$fresh_lines"
exit 0
