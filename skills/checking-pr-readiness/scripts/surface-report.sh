#!/usr/bin/env bash
#
# surface-report.sh — the working-surface and size report.
#
# Serves SKILL.md step 1 (report the full working surface) and sweep class 11
# (diff size against automated-reviewer file caps) in
# references/sweep-classes.md.
#
# Reports four categories with counts and paths: committed against the merge
# base with the default branch, staged, unstaged, and untracked. Empty
# categories are printed explicitly, because a category silently omitted reads
# as a pass.
#
# Usage:
#   surface-report.sh [--cap <name>=<n>]... [--defer <gate-name>] [--help]
#
# Output states. Line 1 is always `verdict: <word>`; human detail follows.
#
#   verdict: under caps                exit 0  every supplied cap is at or above
#                                              the total distinct changed files
#   verdict: exceeds cap for <name>    exit 0  at least one supplied cap is below
#                                              the total; the verdict names the
#                                              first such reviewer and every cap
#                                              is listed in the detail lines
#   verdict: cap unverified            exit 0  no --cap was supplied, so the size
#                                              check could not be made; the
#                                              surface is still reported
#   verdict: no changes on surface     exit 0  all four categories are empty.
#                                              Distinct from `under caps`: an
#                                              absent surface is not a pass
#                                              against a cap
#   verdict: covered by repo gate      exit 3  --defer named a repository-owned
#                                              check; nothing was measured
#   verdict: not run                   exit 2  usage error (unknown option, or a
#                                              malformed --cap value)
#   verdict: not run                   exit 4  git is unavailable, or this is not
#                                              a git repository
#
# One further state rides in the detail lines rather than the verdict: when no
# default branch resolves, `default branch: unresolved` is printed, the
# committed category reports `not computed`, and the other three categories are
# still reported, so the verdict describes a HEAD-only surface.
#
# Dependencies: git and standard POSIX tools. No network, no jq, no node.

set -euo pipefail

usage() {
	cat <<'EOF'
surface-report.sh — working-surface and size report

Usage:
  surface-report.sh [--cap <name>=<n>]... [--defer <gate-name>] [--help]

  --cap <name>=<n>    Compare the total distinct changed-file count against
                      reviewer cap <n> for reviewer <name>. Repeatable.
                      With no --cap the size check reports `cap unverified`.
  --defer <gate-name> Report this class as owned by the named repository gate
                      and measure nothing (exit 3).
  --help              Print this text and exit 0.

Verdicts: under caps | exceeds cap for <name> | cap unverified |
          no changes on surface | covered by repo gate | not run
EOF
}

fail_usage() {
	printf 'verdict: not run\n'
	printf 'reason: %s\n' "$1"
	usage
	exit 2
}

caps=""
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
	--cap)
		[ "$#" -ge 2 ] || fail_usage "--cap requires <name>=<n>"
		case "$2" in
		*=*) ;;
		*) fail_usage "--cap expects <name>=<n>, got: $2" ;;
		esac
		cap_value="${2#*=}"
		case "$cap_value" in
		'' | *[!0-9]*) fail_usage "--cap count must be a non-negative integer, got: $2" ;;
		esac
		caps="${caps}${2}
"
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
	printf 'detail: surface and size not measured here; the named repository gate owns this class.\n'
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

count_of() {
	if [ -z "$1" ]; then
		printf '0\n'
	else
		printf '%s\n' "$1" | wc -l | tr -d ' '
	fi
}

emit_category() {
	printf '%s: %s\n' "$1" "$(count_of "$2")"
	if [ -n "$2" ]; then
		printf '%s\n' "$2" | sed 's/^/  /'
	fi
}

resolve_base() {
	head_ref=$(git symbolic-ref --quiet refs/remotes/origin/HEAD 2>/dev/null || true)
	if [ -n "$head_ref" ]; then
		printf '%s\torigin/HEAD\n' "${head_ref#refs/remotes/}"
		return 0
	fi
	for candidate in origin/main origin/master main master; do
		if git rev-parse --verify --quiet "$candidate" >/dev/null 2>&1; then
			printf '%s\tfallback\n' "$candidate"
			return 0
		fi
	done
	return 1
}

base_info=$(resolve_base) || base_info=""
base_ref="${base_info%%	*}"
base_how="${base_info##*	}"

head_exists=0
if git rev-parse --verify --quiet HEAD >/dev/null 2>&1; then
	head_exists=1
fi

committed=""
merge_base=""
base_line="default branch: unresolved — no origin/HEAD, origin/main, origin/master, main, or master resolved; reporting HEAD-only surface"
if [ -n "$base_ref" ]; then
	base_line="default branch: ${base_ref} (from ${base_how})"
	if [ "$head_exists" -eq 1 ]; then
		merge_base=$(git merge-base HEAD "$base_ref" 2>/dev/null || true)
		if [ -n "$merge_base" ]; then
			committed=$(git diff --name-only "$merge_base" HEAD 2>/dev/null || true)
		fi
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
total=$(count_of "$all_paths")

cap_lines="caps: none supplied — see references/sweep-classes.md cap table"
if [ -z "$all_paths" ]; then
	verdict="no changes on surface"
	cap_lines="caps: not evaluated — the working surface is empty"
elif [ -z "$caps" ]; then
	verdict="cap unverified"
else
	verdict="under caps"
	cap_lines=""
	first_exceeded=""
	while IFS= read -r cap_entry; do
		[ -n "$cap_entry" ] || continue
		cap_name="${cap_entry%%=*}"
		cap_max="${cap_entry#*=}"
		if [ "$total" -gt "$cap_max" ]; then
			cap_lines="${cap_lines}cap ${cap_name}=${cap_max}: exceeded by ${total} changed files
"
			[ -n "$first_exceeded" ] || first_exceeded="$cap_name"
		else
			cap_lines="${cap_lines}cap ${cap_name}=${cap_max}: under (${total} changed files)
"
		fi
	done <<EOF
$caps
EOF
	[ -z "$first_exceeded" ] || verdict="exceeds cap for ${first_exceeded}"
	cap_lines="${cap_lines%
}"
fi

printf 'verdict: %s\n' "$verdict"
printf '%s\n' "$base_line"
if [ -n "$merge_base" ]; then
	printf 'merge base: %s\n' "$merge_base"
	emit_category "committed" "$committed"
else
	printf 'merge base: not computed\n'
	printf 'committed: not computed (no merge base against a default branch)\n'
fi
emit_category "staged" "$staged"
emit_category "unstaged" "$unstaged"
emit_category "untracked" "$untracked"
printf 'total distinct changed files: %s\n' "$total"
printf '%s\n' "$cap_lines"
exit 0
