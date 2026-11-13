#!/usr/bin/env bash
# Pins the sentences that carry coordinating-work's merge guards and its
# batch rules. Each pin names one protected boundary. Each forbidden pattern
# names text the skill must not carry. Together they catch a deleted or
# inverted rule and a reintroduced one; they do not show that an agent obeys
# the text.
set -euo pipefail

repo_root=$(git rev-parse --show-toplevel)
skill_dir="$repo_root/skills/coordinating-work"

# name|file relative to the skill|sentence that carries the boundary
pins=(
  "workers never merge|SKILL.md|Workers never merge."
  "the merge approval comes only from the approved proposal|SKILL.md|Without that approved proposal the Coordinator merges nothing."
  "deploy, spend, force-push and destructive actions wait for the operator|SKILL.md|deploying, spending, force-pushing, and destructive actions still wait for the operator"
  "pull requests with a held change stay open unless pre-authorised|references/operate.md|A pull request with a held change stays open no matter how clean it is, unless the operator pre-authorised it."
  "nothing merges unless every checklist line is true|references/operate.md|A line that is false, that you cannot read, or that is unclear means no merge."
  "nothing produced during the run widens the merge approval|SKILL.md|Nothing produced during the run widens it or stands in for a checklist line"
  "a merge queue or an enforced up-to-date rule decides currency|references/operate.md|Where the repository merges through a queue or enforces up-to-date branches itself, that decides currency; otherwise the branch is current with its base."
  "a behind-base note is no condition when the repository decides currency|references/operate.md|Where line 4 leaves currency to the repository, a note that the branch is behind its base is not such a condition."
  "verification still runs on an up-to-date branch|SKILL.md|Bring the branch up to date with the latest default branch before each run of the repository's verification gate"
  "a follow-on starts fresh once the earlier session has ended|SKILL.md|Confirm the earlier session has ended, and release it through the guide when it has not, then start the follow-on fresh with the whole brief."
  "a settled assignment gets no message|SKILL.md|Never message a settled assignment."
  "a paid option needs the proposal's spending approval|references/operate.md|choose no paid option unless the approved proposal lets you"
  "continuing after a usage limit is the check, not a Revive|references/operate.md|That is part of the check, not a Revive"
  "the proposal records whether the Coordinator may spend|references/setup.md|Whether the Coordinator may choose a paid option, such as at a usage-limit prompt. The default is no."
  "a reply never narrows the repository's gates|SKILL.md|A reply never tells a worker to skip or shorten a gate the repository requires."
  "setup may approve a class of incidental work|references/setup.md|Name a class of work the Coordinator may dispatch without an amended proposal"
  "work outside the batch and its approved class takes an amended proposal|references/operate.md|Adding issues takes an amended proposal the operator approves, except incidental work inside a class the approved proposal names"
  "an issue closes on its completion check, not on the merge|references/operate.md|The issue closes on that result, not on the merge"
  "an issue stays open when the completion check cannot run|references/operate.md|A gap the check finds, or a missing \`managing-issues\`, leaves the issue open"
  "briefs leave out the tracker's closing keywords|SKILL.md|without the tracker's closing keywords"
  "a timed-out write is checked before a retry|references/operate.md|before each retry, check whether an earlier attempt landed. A timed-out write is not proof it failed."
  "a merge-ready question leaves evidence in the pull request|SKILL.md|Evidence belongs in the pull request body, not in the message."
  "setup asks whether to hold or pre-authorise held changes|references/setup.md|Ask the operator directly whether to hold those for review or pre-authorise merging them under a stated bar. With no answer, they are held."
  "a pre-authorised held change merges only under its recorded bar|references/operate.md|except one the record shows the operator pre-authorised for this issue, under a bar this pull request meets"
  "the Coordinator's own rules are a held change|references/operate.md|the project's agent instructions, and its merge and review policy"
  "an update reports the defaults decided alone|references/operate.md|also go through every decision you made by default since the last such report"
)

# name|extended regex the skill text must not match|sample text that matches it
forbidden=(
  "the brief asks the watch to keep the branch current|asked to keep the branch current|asked to keep the branch current"
  "a tracker's issue identifier format|\\b[A-Z][A-Z0-9]+-[0-9]+\\b|#[0-9]+\\b|Closes #12"
)

flatten() { tr -s '[:space:]' ' ' < "$1"; }

# check_rules DIR: prints each broken rule, returns the count broken.
check_rules() {
  local dir=$1 broken=0 pin name rest file sentence entry pattern
  for pin in "${pins[@]}"; do
    name=${pin%%|*}
    rest=${pin#*|}
    file=${rest%%|*}
    sentence=${rest#*|}
    if ! flatten "$dir/$file" | grep -qF -- "$sentence"; then
      echo "boundary missing: $name ($file)"
      broken=$((broken + 1))
    fi
  done
  for entry in "${forbidden[@]}"; do
    name=${entry%%|*}
    rest=${entry#*|}
    pattern=${rest%|*}
    if cat "$dir/SKILL.md" "$dir"/references/*.md | tr -s '[:space:]' ' ' | grep -qE -- "$pattern"; then
      echo "forbidden text present: $name"
      broken=$((broken + 1))
    fi
  done
  return "$broken"
}

if ! check_rules "$skill_dir"; then
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
  if output=$(check_rules "$copy"); then
    echo "pin did not fail when its sentence was removed: $name" >&2
    exit 1
  fi
  if [[ "$output" != "boundary missing: $name ($file)" ]]; then
    echo "unexpected result for broken boundary '$name': $output" >&2
    exit 1
  fi
done

# Prove each forbidden pattern fails when its sample is added, on a scratch copy.
for entry in "${forbidden[@]}"; do
  name=${entry%%|*}
  sample=${entry##*|}
  index=$((index + 1))
  copy="$scratch/$index"
  cp -R "$skill_dir" "$copy"
  printf '\n%s\n' "$sample" >> "$copy/SKILL.md"
  if output=$(check_rules "$copy"); then
    echo "forbidden pattern did not fail when its sample was added: $name" >&2
    exit 1
  fi
  if [[ "$output" != "forbidden text present: $name" ]]; then
    echo "unexpected result for forbidden pattern '$name': $output" >&2
    exit 1
  fi
done

echo "coordinating-work boundary checks: ${#pins[@]} boundaries pinned, ${#forbidden[@]} patterns forbidden"
