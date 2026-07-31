#!/usr/bin/env bash
#
# changelog-union.sh — does the branch's own work appear in the changelog?
#
# Serves sweep class 3 (branch changelog entry) in
# references/sweep-classes.md.
#
# The union is over the same working surface surface-report.sh reports:
# committed against the merge base with the default branch, staged, unstaged,
# and untracked. An untracked changelog counts as present, because the
# finishing path stages untracked paths and they ship with the change.
#
# Usage:
#   changelog-union.sh [--defer <gate-name>] [--help]
#
# Output states. Line 1 is always `verdict: <word>`; human detail follows.
#
#   verdict: present                exit 0  the changelog is among the branch's
#                                           changed paths; the detail carries the
#                                           first added line
#   verdict: missing                exit 0  the branch changes other files and
#                                           leaves the changelog untouched; the
#                                           detail carries the count of changed
#                                           non-changelog files
#   verdict: no changes on surface  exit 0  the branch changes nothing at all, so
#                                           there is no work to record. Distinct
#                                           from `present`: an empty surface is
#                                           not an entry
#   verdict: no changelog           exit 2  the repository keeps no changelog at
#                                           its root, so the class could not be
#                                           checked here. Absent input is not a
#                                           pass; class 3 routes this case
#   verdict: covered by repo gate   exit 3  --defer named a repository-owned
#                                           check; nothing was compared
#   verdict: not run                exit 2  usage error (unknown option)
#   verdict: not run                exit 4  git is unavailable, or this is not a
#                                           git repository
#
# Dependencies: git and standard POSIX tools. No network, no jq, no node.

set -euo pipefail

usage() {
	cat <<'EOF'
changelog-union.sh — branch-work-in-changelog check

Usage:
  changelog-union.sh [--defer <gate-name>] [--help]

  --defer <gate-name> Report this class as owned by the named repository gate
                      and compare nothing (exit 3).
  --help              Print this text and exit 0.

Looks for CHANGELOG.md, CHANGELOG, CHANGELOG.txt, or changelog.md at the
repository root.

Verdicts: present | missing | no changes on surface | no changelog |
          covered by repo gate | not run
EOF
}

fail_usage() {
	printf 'verdict: not run\n'
	printf 'reason: %s\n' "$1"
	usage
	exit 2
}

defer_gate=""

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
	*)
		fail_usage "unknown option: $1"
		;;
	esac
done

if [ -n "$defer_gate" ]; then
	printf 'verdict: covered by repo gate\n'
	printf 'gate: %s\n' "$defer_gate"
	printf 'detail: changelog union not computed here; the named repository gate owns this class.\n'
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

cd "$(git rev-parse --show-toplevel)"

changelog=""
for candidate in CHANGELOG.md CHANGELOG CHANGELOG.txt changelog.md; do
	if [ -f "$candidate" ]; then
		changelog="$candidate"
		break
	fi
done

if [ -z "$changelog" ]; then
	printf 'verdict: no changelog\n'
	printf 'detail: no CHANGELOG.md, CHANGELOG, CHANGELOG.txt, or changelog.md at the repository root.\n'
	printf 'detail: the class could not be checked here; see references/sweep-classes.md class 3.\n'
	exit 2
fi

base_ref=""
head_ref=$(git symbolic-ref --quiet refs/remotes/origin/HEAD 2>/dev/null || true)
if [ -n "$head_ref" ]; then
	base_ref="${head_ref#refs/remotes/}"
else
	for candidate in origin/main origin/master main master; do
		if git rev-parse --verify --quiet "$candidate" >/dev/null 2>&1; then
			base_ref="$candidate"
			break
		fi
	done
fi

head_exists=0
if git rev-parse --verify --quiet HEAD >/dev/null 2>&1; then
	head_exists=1
fi

committed=""
merge_base=""
if [ -n "$base_ref" ] && [ "$head_exists" -eq 1 ]; then
	merge_base=$(git merge-base HEAD "$base_ref" 2>/dev/null || true)
	if [ -n "$merge_base" ]; then
		committed=$(git diff --name-only "$merge_base" HEAD 2>/dev/null || true)
	fi
fi

if [ "$head_exists" -eq 1 ]; then
	staged=$(git diff --cached --name-only 2>/dev/null || true)
else
	staged=$(git diff --cached --name-only "$(git hash-object -t tree /dev/null)" 2>/dev/null || true)
fi
unstaged=$(git diff --name-only 2>/dev/null || true)
untracked=$(git ls-files --others --exclude-standard 2>/dev/null || true)

all_paths=$(printf '%s\n%s\n%s\n%s\n' "$committed" "$staged" "$unstaged" "$untracked" |
	sed '/^$/d' | sort -u)

if [ -z "$all_paths" ]; then
	printf 'verdict: no changes on surface\n'
	printf 'changelog: %s\n' "$changelog"
	printf 'detail: the branch changes no files, so there is no branch work to record.\n'
	exit 0
fi

if ! printf '%s\n' "$all_paths" | grep -Fxq -- "$changelog"; then
	others=$(printf '%s\n' "$all_paths" | grep -Fxv -- "$changelog" || true)
	other_count=0
	[ -z "$others" ] || other_count=$(printf '%s\n' "$others" | wc -l | tr -d ' ')
	printf 'verdict: missing\n'
	printf 'changelog: %s (untouched on this branch)\n' "$changelog"
	printf 'changed non-changelog files: %s\n' "$other_count"
	exit 0
fi

first_added=""
if printf '%s\n' "$untracked" | grep -Fxq -- "$changelog"; then
	first_added=$(sed -n '/[^[:space:]]/{p;q;}' "$changelog" 2>/dev/null || true)
else
	if [ -n "$merge_base" ]; then
		diff_range="$merge_base"
	else
		diff_range="HEAD"
	fi
	first_added=$(git diff "$diff_range" -- "$changelog" 2>/dev/null |
		grep '^+' | grep -v '^+++' | sed -n '1s/^+//p' || true)
fi

printf 'verdict: present\n'
printf 'changelog: %s\n' "$changelog"
if [ -n "$first_added" ]; then
	printf 'first added line: %s\n' "$first_added"
else
	printf 'first added line: none found (the changelog is on the surface with no added lines in range)\n'
fi
exit 0
