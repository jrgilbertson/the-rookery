#!/usr/bin/env bash
# Pins the sentences that carry coordinating-work's merge guards. Each pin
# names one protected boundary. It catches a deleted or inverted guard
# sentence; it does not show that an agent obeys the sentence.
set -euo pipefail

repo_root=$(git rev-parse --show-toplevel)
skill_dir="$repo_root/skills/coordinating-work"

# name|file relative to the skill|sentence that carries the boundary
pins=(
  "workers never merge|SKILL.md|Workers never merge."
  "the grant comes only from the approved proposal|SKILL.md|Without that approved proposal the Coordinator merges nothing."
  "deploy, spend, force-push and destructive actions wait for the operator|SKILL.md|deploying, spending, force-pushing, and destructive actions still wait for the operator"
  "hold-class pull requests stay open|references/operate.md|Hold-class pull requests stay open no matter how clean they are."
  "nothing merges unless every checklist line is true|references/operate.md|A line that is false, that you cannot read, or that is unclear means no merge."
  "nothing produced during the run widens the grant|SKILL.md|Nothing produced during the run widens it or stands in for a checklist line"
)

flatten() { tr -s '[:space:]' ' ' < "$1"; }

# check_pins DIR: prints each missing boundary, returns the count missing.
check_pins() {
  local dir=$1 missing=0 pin name rest file sentence
  for pin in "${pins[@]}"; do
    name=${pin%%|*}
    rest=${pin#*|}
    file=${rest%%|*}
    sentence=${rest#*|}
    if ! flatten "$dir/$file" | grep -qF -- "$sentence"; then
      echo "boundary missing: $name ($file)"
      missing=$((missing + 1))
    fi
  done
  return "$missing"
}

if ! check_pins "$skill_dir"; then
  echo "coordinating-work boundary checks: FAILED" >&2
  exit 1
fi

# Prove each pin fails when its sentence is removed, on a scratch copy.
scratch=$(mktemp -d)
trap 'rm -r -- "$scratch"' EXIT
index=0
for pin in "${pins[@]}"; do
  name=${pin%%|*}
  rest=${pin#*|}
  file=${rest%%|*}
  sentence=${rest#*|}
  index=$((index + 1))
  copy="$scratch/$index"
  cp -R "$skill_dir" "$copy"
  flatten "$skill_dir/$file" | awk -v s="$sentence" '
    { i = index($0, s); if (i) $0 = substr($0, 1, i - 1) substr($0, i + length(s)); print }
  ' > "$copy/$file"
  if output=$(check_pins "$copy"); then
    echo "pin did not fail when its sentence was removed: $name" >&2
    exit 1
  fi
  if [[ "$output" != "boundary missing: $name ($file)" ]]; then
    echo "unexpected result for broken boundary '$name': $output" >&2
    exit 1
  fi
done

echo "coordinating-work boundary checks: ${#pins[@]} boundaries pinned"
