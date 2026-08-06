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
#   changelog-union.sh [--base <ref>] [--merge-base <sha>] [--defer <gate-name>]
#                      [--help]
#
# Output states. Line 1 is always `verdict: <word>`; human detail follows.
#
#   verdict: present                exit 0  the changelog gained lines with
#                                           content on the branch's surface; the
#                                           detail carries the first added line.
#                                           Whitespace-only additions do not
#                                           count
#   verdict: changed without entry  exit 0  the changelog is among the branch's
#                                           changed paths but gained no lines —
#                                           a deletion, a reflow, or a
#                                           whitespace-only edit. Touching the
#                                           file is not an entry, so this is
#                                           distinct from `present`
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
#   verdict: not run                exit 4  git is unavailable, this is not a
#                                           git repository, a git read over the
#                                           surface or the changelog failed, a
#                                           supplied --merge-base failed
#                                           validation, or
#                                           no unambiguous default branch
#                                           resolved while the
#                                           branch has commits — the committed
#                                           category is then unmeasurable, and a
#                                           clean verdict against an unmeasured
#                                           surface would be a silent pass. A
#                                           failed read is never reported as an
#                                           empty surface
#
# Dependencies: git and standard POSIX tools. No network, no jq, no node.

set -euo pipefail

usage() {
	cat <<'EOF'
changelog-union.sh — branch-work-in-changelog check

Usage:
  changelog-union.sh [--base <ref>] [--merge-base <sha>] [--defer <gate-name>]
                     [--help]

  --base <ref>        Use <ref> as the default branch instead of resolving one.
  --merge-base <sha>  Use <sha> as the merge base instead of computing one. It
                      is validated: whenever a base resolves (--base or a
                      default branch) it must equal that base's merge base with
                      HEAD, and with no base at all it must be an ancestor of
                      HEAD. A supplied merge base that fails validation exits 4.
  --defer <gate-name> Report this class as owned by the named repository gate
                      and compare nothing (exit 3).
  --help              Print this text and exit 0.

Looks for CHANGELOG.md, CHANGELOG, CHANGELOG.txt, or changelog.md at the
repository root.

Verdicts: present | changed without entry | missing | no changes on surface |
          no changelog | covered by repo gate | not run
EOF
}

fail_usage() {
	printf 'verdict: not run\n'
	printf 'reason: %s\n' "$1"
	usage
	exit 2
}

defer_gate=""
supplied_base=""
supplied_merge_base=""

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

if [ "$(git rev-parse --is-inside-work-tree 2>/dev/null)" != "true" ]; then
	printf 'verdict: not run\n'
	printf 'reason: not inside a git work tree (a bare repository has no working surface to check)\n'
	exit 4
fi

cd "$(git rev-parse --show-toplevel)"

fail_read() {
	printf 'verdict: not run\n'
	printf 'reason: the %s read could not be completed: %s\n' "$1" "$2"
	printf 'detail: a failed git read is not an empty surface, so no changelog verdict is reported.\n'
	exit 4
}

# A merge base that fails validation is as unusable as one that fails to read:
# it silently shrinks the committed category, so it takes the same hard exit.
fail_merge_base() {
	printf 'verdict: not run\n'
	printf 'reason: the supplied merge base is not usable: %s\n' "$1"
	printf 'detail: the committed category is measured from the merge base, so an unverified one is not compared against the changelog.\n'
	exit 4
}

# Every surface read goes through this: an empty result and a failed read look
# identical once the status is discarded, and reporting a failed read as an
# empty surface turns a broken repository into `no changes on surface`.
git_out=""
read_or_fail() {
	enumeration="$1"
	shift
	if ! git_out=$(git "$@" 2>/dev/null); then
		fail_read "$enumeration" "git $* returned non-zero"
	fi
}

head_exists=0
if git rev-parse --verify --quiet HEAD >/dev/null 2>&1; then
	head_exists=1
fi

# A changelog the branch deletes from the worktree — plain or staged with
# `git rm` — is still the repository's changelog: recognizing index and HEAD
# paths keeps that deletion a branch finding instead of an absent-input
# result.
# Symlink entries (mode 120000) are filtered in the index and in HEAD for the
# same reason the worktree check refuses links: git ships the link, and
# reading or diffing through one quotes paths or content from outside the
# repository.
read_or_fail "changelog tracking" ls-files -s -- CHANGELOG.md CHANGELOG CHANGELOG.txt changelog.md
index_changelogs=$(printf '%s\n' "$git_out" | grep -v '^120000 ' | sed 's/^[^	]*	//' || true)
head_changelogs=""
if [ "$head_exists" -eq 1 ]; then
	read_or_fail "changelog history" ls-tree HEAD -- CHANGELOG.md CHANGELOG CHANGELOG.txt changelog.md
	head_changelogs=$(printf '%s\n' "$git_out" | grep -v '^120000 ' | sed 's/^[^	]*	//' || true)
fi
# Live candidates — on disk or in the index — win over paths that survive only
# in HEAD, so a staged rename resolves to its replacement rather than to the
# deleted old name.
# A symlink is never the changelog: git ships the link, not its target, and
# reading through it would quote content from outside the repository.
changelog=""
for candidate in CHANGELOG.md CHANGELOG CHANGELOG.txt changelog.md; do
	if { [ -f "$candidate" ] && [ ! -L "$candidate" ]; } ||
		printf '%s\n' "$index_changelogs" | grep -Fx -- "$candidate" >/dev/null; then
		changelog="$candidate"
		break
	fi
done
if [ -z "$changelog" ]; then
	for candidate in CHANGELOG.md CHANGELOG CHANGELOG.txt changelog.md; do
		if printf '%s\n' "$head_changelogs" | grep -Fx -- "$candidate" >/dev/null; then
			changelog="$candidate"
			break
		fi
	done
fi

if [ -n "$changelog" ]; then
	# An unresolved merge conflict makes the changelog's content unmeasurable:
	# counting conflict markers or one side's lines as an entry would be a
	# silent pass over a file the owner has not finished writing.
	read_or_fail "merge state" ls-files -u -- "$changelog"
	if [ -n "$git_out" ]; then
		printf 'verdict: not run\n'
		printf 'reason: %s has an unresolved merge conflict, so its entries cannot be counted\n' "$changelog"
		printf 'detail: resolve the conflict and re-run.\n'
		exit 4
	fi
fi

if [ -z "$changelog" ]; then
	printf 'verdict: no changelog\n'
	printf 'detail: no CHANGELOG.md, CHANGELOG, CHANGELOG.txt, or changelog.md at the repository root.\n'
	printf 'detail: the class could not be checked here; see references/sweep-classes.md class 3.\n'
	exit 2
fi

base_ref=""
if [ -n "$supplied_base" ]; then
	base_ref="$supplied_base"
else
	# Resolution is attempted even when --merge-base is supplied: a base that
	# resolves is what the supplied merge base is checked against, and a
	# supplied value that cannot be checked gets the weaker ancestor check.
	head_ref=$(git symbolic-ref --quiet refs/remotes/origin/HEAD 2>/dev/null || true)
	if [ -n "$head_ref" ]; then
		base_ref="${head_ref#refs/remotes/}"
	else
		# Tiered like surface-report.sh: a tier with more than one live candidate
		# is ambiguous, and an ambiguous base leaves committed unmeasured rather
		# than diffing against a guess. Full ref namespaces, so a tag named main
		# or master can never satisfy a branch fallback.
		for tier in "refs/remotes/origin/main refs/remotes/origin/master" "refs/heads/main refs/heads/master"; do
			found=""
			found_count=0
			for candidate in $tier; do
				if git rev-parse --verify --quiet "$candidate" >/dev/null 2>&1; then
					found="$candidate"
					found_count=$((found_count + 1))
				fi
			done
			if [ "$found_count" -eq 1 ]; then
				base_ref="$found"
			fi
			[ "$found_count" -eq 0 ] || break
		done
	fi
fi

committed=""
merge_base=""
if [ -n "$supplied_merge_base" ] && [ "$head_exists" -eq 1 ]; then
	# A supplied merge base is verified as a commit before use, so a typo
	# fails with the read named instead of a confusing diff error.
	read_or_fail "merge base" rev-parse --verify --quiet "${supplied_merge_base}^{commit}"
	merge_base="$git_out"
	# An unchecked merge base decides the committed category on its own: HEAD
	# passed here empties the committed diff, and a branch that recorded its
	# work in an earlier commit then reads as `missing`. Whenever a base
	# resolves, the supplied value must be the merge base that base yields;
	# only with no base at all is the weaker ancestor check the best available.
	if [ -n "$base_ref" ]; then
		read_or_fail "merge base" merge-base HEAD "$base_ref"
		if [ "$merge_base" != "$git_out" ]; then
			fail_merge_base "supplied --merge-base ${supplied_merge_base} resolves to ${merge_base}, but the merge base with ${base_ref} is ${git_out}"
		fi
	else
		git merge-base --is-ancestor "$merge_base" HEAD 2>/dev/null ||
			fail_merge_base "supplied --merge-base ${supplied_merge_base} is not an ancestor of HEAD"
	fi
elif [ -n "$base_ref" ] && [ "$head_exists" -eq 1 ]; then
	read_or_fail "merge base" merge-base HEAD "$base_ref"
	merge_base="$git_out"
fi
if [ -n "$merge_base" ]; then
	read_or_fail "committed" diff --name-only "$merge_base" HEAD
	committed="$git_out"
fi

# With commits on the branch but no resolvable default branch, the committed
# category cannot be enumerated, so any verdict that depends on not finding
# something there would be a silent pass. Positive evidence (`present`) from
# the measurable categories is still honest; the negative verdicts are not.
committed_measured=1
if [ "$head_exists" -eq 1 ] && [ -z "$base_ref" ] && [ -z "$merge_base" ]; then
	committed_measured=0
fi

require_committed_measured() {
	if [ "$committed_measured" -eq 0 ]; then
		printf 'verdict: not run\n'
		printf 'reason: no unambiguous default branch resolved, so the committed category could not be measured\n'
		printf 'detail: a "%s" verdict against an unmeasured surface would be a silent pass; resolve the default branch and re-run.\n' "$1"
		exit 4
	fi
}

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

if [ -z "$all_paths" ]; then
	require_committed_measured "no changes on surface"
	printf 'verdict: no changes on surface\n'
	printf 'changelog: %s\n' "$changelog"
	printf 'detail: the branch changes no files, so there is no branch work to record.\n'
	exit 0
fi

if ! printf '%s\n' "$all_paths" | grep -Fx -- "$changelog" >/dev/null; then
	require_committed_measured "missing"
	others=$(printf '%s\n' "$all_paths" | grep -Fxv -- "$changelog" || true)
	other_count=0
	[ -z "$others" ] || other_count=$(printf '%s\n' "$others" | wc -l | tr -d ' ')
	printf 'verdict: missing\n'
	printf 'changelog: %s (untouched on this branch)\n' "$changelog"
	printf 'changed non-changelog files: %s\n' "$other_count"
	exit 0
fi

# A changed changelog is not yet an entry. Only lines the branch adds count, so
# the added lines are collected across the same surface: an untracked changelog
# is all additions, and a tracked one is diffed from the merge base (or from the
# empty tree when the branch has no commits) through to the working tree.
added_lines=""
if printf '%s\n' "$untracked" | grep -Fx -- "$changelog" >/dev/null; then
	[ ! -L "$changelog" ] ||
		fail_read "changelog contents" "the changelog is a symbolic link; content is not read through links"
	added_lines=$(cat -- "$changelog" 2>/dev/null) ||
		fail_read "changelog contents" "cat -- $changelog returned non-zero"
else
	if [ -n "$merge_base" ]; then
		diff_range="$merge_base"
	elif [ "$head_exists" -eq 1 ]; then
		diff_range="HEAD"
	else
		read_or_fail "empty tree" hash-object -t tree /dev/null
		diff_range="$git_out"
	fi
	# Prefixes, color, and rename detection are pinned so repository config
	# (diff.noprefix, diff.mnemonicPrefix, color.ui, diff.renames, external
	# diff drivers) cannot change the output shape this filter relies on. The
	# pathspec covers every candidate name so a rename keeps its provenance
	# and a pure rename does not render as a wholly added file.
	read_or_fail "changelog additions" -c diff.noprefix=false -c diff.mnemonicPrefix=false \
		-c diff.renames=true \
		diff --no-ext-diff --no-color --src-prefix=a/ --dst-prefix=b/ "$diff_range" -- \
		CHANGELOG.md CHANGELOG CHANGELOG.txt changelog.md
	# Drop only the exact destination headers for the supported changelog
	# names, never content: an added line starting with ++ (even "++ b/…")
	# renders as +++ in the diff too, so a prefix match would discard it.
	added_lines=$(printf '%s\n' "$git_out" |
		grep '^+' |
		grep -Fxv -e '+++ b/CHANGELOG.md' -e '+++ b/CHANGELOG' \
			-e '+++ b/CHANGELOG.txt' -e '+++ b/changelog.md' \
			-e '+++ /dev/null' |
		sed 's/^+//' || true)
fi

# Only added lines with content count as an entry: a blank or whitespace-only
# addition is a formatting change, not recorded branch work.
added_count=0
[ -z "$added_lines" ] ||
	added_count=$(printf '%s\n' "$added_lines" | grep -c '[^[:space:]]' || true)

if [ "$added_count" -eq 0 ]; then
	require_committed_measured "changed without entry"
	printf 'verdict: changed without entry\n'
	printf 'changelog: %s (changed on this branch, no lines with content added)\n' "$changelog"
	printf 'detail: the branch touches the changelog without adding a line with content, so no branch work is recorded there.\n'
	exit 0
fi

first_added=$(printf '%s\n' "$added_lines" | sed -n '/[^[:space:]]/{p;q;}')

printf 'verdict: present\n'
printf 'changelog: %s\n' "$changelog"
printf 'added lines with content: %s\n' "$added_count"
printf 'first added line: %s\n' "$first_added"
exit 0
