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
# as a pass. Counts are always exact; each category's path listing is capped
# at 25 paths unless --full is given, so a huge surface reports without
# flooding the caller.
#
# Usage:
#   surface-report.sh [--cap <name>=<n>]... [--base <ref>] [--merge-base <sha>]
#                     [--full] [--defer <gate-name>] [--help]
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
#                                              check could not be made; or the
#                                              committed category could not be
#                                              measured, so no supplied cap can
#                                              be called met. The surface is
#                                              still reported
#   verdict: no changes on surface     exit 0  all four categories are empty and
#                                              the committed category was
#                                              measured; when it could not be,
#                                              an empty measured surface reports
#                                              `cap unverified` instead.
#                                              Distinct from `under caps`: an
#                                              absent surface is not a pass
#                                              against a cap
#   verdict: covered by repo gate      exit 3  --defer named a repository-owned
#                                              check; nothing was measured
#   verdict: not run                   exit 2  usage error (unknown option, or a
#                                              malformed --cap value)
#   verdict: not run                   exit 4  git is unavailable, this is not a
#                                              git repository, one of the five
#                                              git enumerations (merge base,
#                                              committed, staged, unstaged,
#                                              untracked) failed to read, or a
#                                              supplied --merge-base failed
#                                              validation. A failed read is never
#                                              reported as an empty category; the
#                                              reason line names the enumeration
#
# One further state rides in the detail lines rather than the verdict: when no
# default branch resolves, `default branch: unresolved` is printed, the
# committed category reports `not computed`, and the other three categories are
# still reported, so the verdict describes a HEAD-only surface. Because the
# committed count is then unknown, supplied caps report `cap unverified` unless
# the measured part alone already exceeds one.
#
# Dependencies: git and standard POSIX tools. No network, no jq, no node.

set -euo pipefail

usage() {
	cat <<'EOF'
surface-report.sh — working-surface and size report

Usage:
  surface-report.sh [--cap <name>=<n>]... [--base <ref>] [--merge-base <sha>]
                    [--full] [--defer <gate-name>] [--help]

  --cap <name>=<n>    Compare the total distinct changed-file count against
                      reviewer cap <n> for reviewer <name>. Repeatable.
                      With no --cap the size check reports `cap unverified`.
  --base <ref>        Use <ref> as the default branch instead of resolving one.
  --merge-base <sha>  Use <sha> as the merge base instead of computing one. It
                      is validated: whenever a base resolves (--base or a
                      default branch) it must equal that base's merge base with
                      HEAD, and with no base at all it must be an ancestor of
                      HEAD and the merge-base line says it went unverified.
                      A supplied merge base that fails validation exits 4.
  --full              Print every path in each category instead of the first
                      25. Counts are exact either way.
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
supplied_base=""
supplied_merge_base=""
full_listing=0

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
		# Beyond 15 digits the shell's integer comparison breaks, and a broken
		# comparison must not fall through to a clean verdict.
		[ "${#cap_value}" -le 15 ] || fail_usage "--cap count is too large to compare: $2"
		case "${2%%=*}" in
		'') fail_usage "--cap requires a reviewer name before '=', got: $2" ;;
		esac
		caps="${caps}${2}
"
		shift 2
		;;
	--base)
		[ "$#" -ge 2 ] || fail_usage "--base requires a ref"
		[ -n "$2" ] || fail_usage "--base requires a non-empty ref"
		supplied_base="$2"
		shift 2
		;;
	--merge-base)
		[ "$#" -ge 2 ] || fail_usage "--merge-base requires a commit"
		[ -n "$2" ] || fail_usage "--merge-base requires a non-empty commit"
		supplied_merge_base="$2"
		shift 2
		;;
	--full)
		full_listing=1
		shift
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

if [ "$(git rev-parse --is-inside-work-tree 2>/dev/null)" != "true" ]; then
	printf 'verdict: not run\n'
	printf 'reason: not inside a git work tree (a bare repository has no working surface to report)\n'
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

# The count is always exact — the cap check depends on it — but the path
# listing is capped so a 500-file surface does not flood the caller; --full
# restores the complete dump.
emit_category() {
	category_count=$(count_of "$2")
	printf '%s: %s\n' "$1" "$category_count"
	[ -n "$2" ] || return 0
	if [ "$full_listing" -eq 1 ] || [ "$category_count" -le 25 ]; then
		printf '%s\n' "$2" | sed 's/^/  /'
	else
		# sed drains its stdin: `head` would close the pipe early and kill the
		# writing printf with SIGPIPE, which `set -o pipefail` turns into a
		# 141 exit for the whole script.
		printf '%s\n' "$2" | sed -n '1,25s/^/  /p'
		printf '  … and %s more (--full lists every path)\n' "$((category_count - 25))"
	fi
}

# Fallbacks are tiered (remote refs, then local) and a tier with more than one
# live candidate is ambiguous — origin/main and origin/master both existing
# means the true target is a guess, and a surface diffed against a guessed
# base silently omits the commits between the two.
resolve_base() {
	head_ref=$(git symbolic-ref --quiet refs/remotes/origin/HEAD 2>/dev/null || true)
	if [ -n "$head_ref" ]; then
		printf '%s\torigin/HEAD\n' "${head_ref#refs/remotes/}"
		return 0
	fi
	# Candidates are verified in their full ref namespaces so a tag named
	# main or master can never satisfy a branch fallback.
	for tier in "refs/remotes/origin/main refs/remotes/origin/master" "refs/heads/main refs/heads/master"; do
		found=""
		found_count=0
		for candidate in $tier; do
			if git rev-parse --verify --quiet "$candidate" >/dev/null 2>&1; then
				found="$candidate"
				found_count=$((found_count + 1))
			fi
		done
		[ "$found_count" -le 1 ] || return 2
		if [ "$found_count" -eq 1 ]; then
			printf '%s\tfallback\n' "$found"
			return 0
		fi
	done
	return 1
}

base_rc=0
if [ -n "$supplied_base" ]; then
	base_info="${supplied_base}	--base"
else
	# Resolution is attempted even when --merge-base is supplied: a base that
	# resolves is what the supplied merge base is checked against, and a
	# supplied value that cannot be checked is reported as such.
	base_info=$(resolve_base) || base_rc=$?
	[ "$base_rc" -eq 0 ] || base_info=""
fi
base_ref="${base_info%%	*}"
base_how="${base_info##*	}"

head_exists=0
if git rev-parse --verify --quiet HEAD >/dev/null 2>&1; then
	head_exists=1
fi

fail_read() {
	printf 'verdict: not run\n'
	printf 'reason: the %s enumeration could not be read: %s\n' "$1" "$2"
	printf 'detail: a failed git read is not an empty category, so no surface and no cap result is reported.\n'
	exit 4
}

# A merge base that fails validation is as unusable as one that fails to read:
# it silently shrinks the committed category, so it takes the same hard exit.
fail_merge_base() {
	printf 'verdict: not run\n'
	printf 'reason: the supplied merge base is not usable: %s\n' "$1"
	printf 'detail: the committed category is measured from the merge base, so an unverified one is not reported as a surface.\n'
	exit 4
}

# Every enumeration goes through this: an empty result and a failed read look
# identical once the status is discarded, and reporting a failed read as an
# empty category turns a broken repository into a green report.
git_out=""
read_or_fail() {
	enumeration="$1"
	shift
	if ! git_out=$(git "$@" 2>/dev/null); then
		fail_read "$enumeration" "git $* returned non-zero"
	fi
}

committed=""
merge_base=""
merge_base_caveat=""
committed_measured=0
base_line="default branch: unresolved — no origin/HEAD, origin/main, origin/master, main, or master resolved; reporting HEAD-only surface"
if [ "$base_rc" -eq 2 ]; then
	base_line="default branch: ambiguous — more than one candidate resolves in the same tier; set origin/HEAD or name the target; reporting HEAD-only surface"
fi
if [ -n "$base_ref" ]; then
	base_line="default branch: ${base_ref} (from ${base_how})"
fi
if [ -n "$supplied_merge_base" ] && [ "$head_exists" -eq 1 ]; then
	# A supplied merge base is verified as a commit before use, so a typo
	# fails with the read named instead of a confusing diff error.
	read_or_fail "merge base" rev-parse --verify --quiet "${supplied_merge_base}^{commit}"
	merge_base="$git_out"
	# An unchecked merge base decides the committed category on its own: HEAD
	# passed here empties the diff and turns branch work into `no changes on
	# surface`. Whenever a base resolves, the supplied value must be the merge
	# base that base yields; only with no base at all is the weaker ancestor
	# check the best available, and the readout then says so.
	if [ -n "$base_ref" ]; then
		read_or_fail "merge base" merge-base HEAD "$base_ref"
		if [ "$merge_base" != "$git_out" ]; then
			fail_merge_base "supplied --merge-base ${supplied_merge_base} resolves to ${merge_base}, but the merge base with ${base_ref} is ${git_out}"
		fi
	else
		git merge-base --is-ancestor "$merge_base" HEAD 2>/dev/null ||
			fail_merge_base "supplied --merge-base ${supplied_merge_base} is not an ancestor of HEAD"
		merge_base_caveat=" (from --merge-base, unverified against a base)"
		if [ "$base_rc" -eq 2 ]; then
			base_line="default branch: ambiguous — more than one candidate resolves in the same tier; set origin/HEAD or name the target, so the supplied merge base can be checked against one"
		else
			base_line="default branch: not resolved here, so the supplied merge base could not be checked against one"
		fi
	fi
	read_or_fail "committed" diff --name-only "$merge_base" HEAD
	committed="$git_out"
	committed_measured=1
elif [ -n "$base_ref" ] && [ "$head_exists" -eq 1 ]; then
	read_or_fail "merge base" merge-base HEAD "$base_ref"
	merge_base="$git_out"
	if [ -n "$merge_base" ]; then
		read_or_fail "committed" diff --name-only "$merge_base" HEAD
		committed="$git_out"
		committed_measured=1
	fi
fi
if [ "$head_exists" -eq 0 ]; then
	committed_measured=1
fi

if [ "$head_exists" -eq 1 ]; then
	read_or_fail "staged" diff --cached --name-only
else
	empty_tree=$(git hash-object -t tree /dev/null 2>/dev/null || true)
	[ -n "$empty_tree" ] || fail_read "staged" "the empty tree object could not be resolved"
	read_or_fail "staged" diff --cached --name-only "$empty_tree"
fi
staged="$git_out"
read_or_fail "unstaged" diff --name-only
unstaged="$git_out"
read_or_fail "untracked" ls-files --others --exclude-standard
untracked="$git_out"

all_paths=$(printf '%s\n%s\n%s\n%s\n' "$committed" "$staged" "$unstaged" "$untracked" |
	sed '/^$/d' | sort -u)
total=$(count_of "$all_paths")

cap_lines="caps: none supplied — see references/sweep-classes.md class 11"
if [ -z "$all_paths" ]; then
	if [ "$committed_measured" -eq 0 ]; then
		# An empty measured surface proves nothing when the committed
		# category was never measured; a clean verdict here would hide
		# exactly the branch work this report exists to expose.
		verdict="cap unverified"
		cap_lines="caps: not confirmed — the committed category could not be measured, so an empty measured surface is not a no-changes result"
	else
		verdict="no changes on surface"
		cap_lines="caps: not evaluated — the working surface is empty"
	fi
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
	if [ -n "$first_exceeded" ]; then
		# An unmeasured committed count only makes the total a floor, so an
		# exceeded cap still holds.
		verdict="exceeds cap for ${first_exceeded}"
	elif [ "$committed_measured" -eq 0 ]; then
		verdict="cap unverified"
		cap_lines="${cap_lines}caps: not confirmed — the committed category could not be measured, so the total above is a floor
"
	fi
	cap_lines="${cap_lines%
}"
fi

printf 'verdict: %s\n' "$verdict"
printf '%s\n' "$base_line"
if [ -n "$merge_base" ]; then
	printf 'merge base: %s%s\n' "$merge_base" "$merge_base_caveat"
	emit_category "committed" "$committed"
elif [ "$head_exists" -eq 0 ]; then
	printf 'merge base: not computed (the branch has no commits)\n'
	emit_category "committed" ""
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
