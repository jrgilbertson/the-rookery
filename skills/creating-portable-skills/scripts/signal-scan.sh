#!/bin/sh
# Mechanical pre-check for references/review-checklist.md.
#
# Usage: signal-scan.sh <skill-directory>...
#
# Scans SKILL.md and references/*.md in each package and prints, per signal,
# a header "## <signal> (<count>) -> <checklist item>" followed by the hits as
# file:line:text. Hits are review candidates, not failures, so a completed scan
# exits 0. Invalid inputs and scan errors exit nonzero. The scan
# writes nothing, so it runs in a read-only sandbox.

set -e

[ "$#" -gt 0 ] || { echo "usage: $0 <skill-directory>..." >&2; exit 2; }

directories=""
for dir in "$@"; do
	case "$dir" in
		*'
'*) echo 'signal-scan: newline in pathname is not supported' >&2; exit 2 ;;
		/*) ;;
		*) dir=./$dir ;;
	esac
	# Keep pwd's final newline until the sentinel is removed, so command
	# substitution cannot silently trim newlines belonging to the root itself.
	dir=$(CDPATH='' cd -P "$dir" && pwd -P && printf '.')
	dir=${dir%.}
	dir=${dir%?}
	case "$dir" in
		*'
'*) echo 'signal-scan: newline in pathname is not supported' >&2; exit 2 ;;
	esac
	[ ! -L "$dir/SKILL.md" ] && [ ! -L "$dir/references" ] || {
		echo "signal-scan: symbolic-link package entry is not allowed: $dir" >&2
		exit 2
	}
	[ -f "$dir/SKILL.md" ] || { echo "no SKILL.md in $dir" >&2; exit 2; }
	directories="$directories$dir
"
done

# Only validated, newline-free package roots use line records. Discovered files
# stay in argument arrays. Batched -exec makes a child error fail find itself.
each_file() {
	flags=$1 pattern=$2
	printf '%s' "$directories" | while IFS= read -r dir; do
		set -- "$dir/SKILL.md"
		if [ -d "$dir/references" ]; then
			set -- "$@" "$dir/references"
		fi
		find "$@" -type f -name '*.md' -exec sh -c '
			flags=$1 pattern=$2
			shift 2
			for file do
				case "$file" in
					*"
"*) echo "signal-scan: newline in pathname is not supported" >&2; exit 2 ;;
				esac
				if grep -nH"$flags"E -e "$pattern" -- "$file"; then
					:
				else
					status=$?
					[ "$status" -eq 1 ] || exit "$status"
				fi
			done
		' signal-scan "$flags" "$pattern" {} + || exit
	done
}

report() { # report <signal> <checklist item> <hits>
	if [ -n "$3" ]; then count=$(printf '%s\n' "$3" | grep -c .); else count=0; fi
	printf '## %s (%s) -> %s\n' "$1" "$count" "$2"
	[ "$count" -eq 0 ] || printf '%s\n' "$3"
}

scan() { # scan <signal> <checklist item> <grep flags> <pattern>
	hits=$(each_file "$3" "$4")
	report "$1" "$2" "$hits"
}

scan 'pressure language' 'Steering is positive' '' \
	'(^|[^[:alnum:]_])(MUST|NEVER|ALWAYS|CRITICAL|IMPORTANT)([^[:alnum:]_]|$)|!!'
scan 'hedged requirement' 'Qualifiers are operationalized' iw \
	'try to|if possible|ideally'
scan 'model trait claim' 'Steering is positive' i \
	"you (tend to|often|sometimes)|don't be too"
scan 'thinking scaffold' 'No-ops' i \
	'think step by step|take a deep breath|<scratchpad>|<thinking>'
scan 'output clamp or cadence' 'Specificity matches fragility' i \
	'every [0-9]+ (tool calls|messages|turns)|at most [0-9]+ (words|sentences|bullets)'
scan 'format or narration suppressor' 'Steering is positive' i \
	"never use (bullets|headers|bold)|don't narrate|no interim|hold (all )?(findings|results)"
scan 'reinforcement padding' 'Duplication' '' \
	'Remember,|Again,|As stated above'
scan 'grader vocabulary' 'No-ops' i \
	'you will be graded|hidden tests?'
scan 'migration-relative phrasing' 'Sediment' i \
	'no longer|now works|also counts|previously|used to be'
scan 'history identifier' 'Sediment' '' \
	'#[0-9]{2,}|PR [0-9]+|20[0-9]{2}-[0-9]{2}-[0-9]{2}'
# A maintained list: add a family name when a new one appears in reviewed skills.
scan 'pinned model name' 'Sediment' i \
	'(claude|gpt|gemini|grok|llama|opus|sonnet|haiku)[- ][0-9]'

exit 0
