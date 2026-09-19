#!/bin/sh
# Mechanical pre-check for references/review-checklist.md.
#
# Usage: signal-scan.sh <skill-directory>...
#
# Scans SKILL.md and references/*.md in each package and prints, per signal,
# a header "## <signal> (<count>) -> <checklist item>" followed by the hits as
# file:line:text. Hits are review candidates, not failures, so a completed scan
# exits 0. A directory without a SKILL.md is the only error exit.

[ "$#" -gt 0 ] || { echo "usage: $0 <skill-directory>..." >&2; exit 2; }

list=$(mktemp) || exit 2
trap 'rm -f "$list"' EXIT

for dir in "$@"; do
	dir=${dir%/}
	[ -f "$dir/SKILL.md" ] || { echo "no SKILL.md in $dir" >&2; exit 2; }
	printf '%s\n' "$dir/SKILL.md" >>"$list"
	[ -d "$dir/references" ] && find "$dir/references" -type f -name '*.md' | LC_ALL=C sort >>"$list"
done

report() { # report <signal> <checklist item> <hits>
	if [ -n "$3" ]; then count=$(printf '%s\n' "$3" | grep -c .); else count=0; fi
	printf '## %s (%s) -> %s\n' "$1" "$count" "$2"
	[ "$count" -eq 0 ] || printf '%s\n' "$3"
}

scan() { # scan <signal> <checklist item> <grep flags> <pattern>
	hits=$(while IFS= read -r file; do
		grep -nH"$3"E -e "$4" "$file"
	done <"$list")
	report "$1" "$2" "$hits"
}

scan 'pressure language' 'Steering is positive' w \
	'MUST|NEVER|ALWAYS|CRITICAL|IMPORTANT|!!'
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
scan 'pinned model name' 'Sediment' i \
	'(claude|gpt|gemini|grok|llama|opus|sonnet|haiku)[- ][0-9]'

runs=$(while IFS= read -r file; do
	awk -v f="$file" '{
		if ($0 ~ /^(- |[0-9]+\. )?(Do not|Never|Avoid) /) { n++; if (n == 3) print f ":" NR ":" $0 }
		else n = 0
	}' "$file"
done <"$list")
report 'prohibition run' 'Steering is positive' "$runs"

scan 'numbered workflow heading' 'Specificity matches fragility' '' \
	'^#+ [0-9]+\.'

exit 0
