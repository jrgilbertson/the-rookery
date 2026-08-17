---
title: "Ship bundled skill helpers with an executable falsifiability contract"
date: 2026-07-31
last_updated: 2026-08-11
category: workflow-issues
module: "skills/checking-pr-readiness, skills/checking-merge-readiness, skills/repo-gardener"
problem_type: workflow_issue
component: testing_framework
severity: high
applies_when:
  - "Bundling executable helper scripts inside a portable skill"
  - "A helper's output is what an agent reads to decide a gate passes or fails"
  - "Reviewing a script whose documented states include absent input, deferral, and environment failure"
  - "A guard is written as a conjunction of conditions that can occur separately"
  - "Deciding whether a named artifact exists by searching a repository"
symptoms:
  - "A helper returns a green verdict at exit 0 in a state its own header documents as a finding"
  - "Prose review of a helper reports no issues, and a first execution against fixtures fails immediately"
  - "A guard's conditions are individually reachable but the guard only fires when both hold"
  - "A failed external read and an empty result are indistinguishable in the helper's output"
root_cause: missing_validation
resolution_type: tooling_addition
related_components:
  - development_workflow
  - tooling
tags: [agent-skills, helper-scripts, falsifiability-contract, silent-pass, fixture-testing, exit-codes, fail-closed, execution-based-review, jq-null-object, unvalidated-ref, sigpipe, recurrence]
---

# Ship bundled skill helpers with an executable falsifiability contract

## Context

The `checking-pr-readiness` skill bundles three helper scripts that an agent
runs to decide whether a branch is ready for review:
`skills/checking-pr-readiness/scripts/surface-report.sh`,
`changelog-union.sh`, and `evidence-freshness.sh`. This work shipped in #23.

All three were designed for falsifiability from the first draft. Each header
enumerates the helper's output states with a distinct exit code per state:
absent input exits 2, verdicts exit 0, an explicit deferral to a repository-owned
gate exits 3, and an environment failure exits 4. Line 1 of every output is
`verdict: <word>`, so a caller reads a fixed pair — verdict line and exit code —
rather than parsing prose. `evidence-freshness.sh:31-77`,
`changelog-union.sh:16-55`, and `surface-report.sh:17-58` each carry that
enumeration in the header.

That design was not enough. All three helpers still shipped with holes where a
state the header documents as a finding came back green at exit 0:

1. **Deleted-record bypass.** The no-records guard required both an empty
   timestamp and an absent file. A record that had been committed and then
   deleted from the working tree satisfied only the second condition, so the
   guard fell through. The record was then dated `now` (the pre-fix
   `last_edit_of` returned the current time for anything dirty, and a deleted
   tracked file is dirty), which is later than every described path, so
   evidence describing a record that no longer existed read `fresh`.
2. **Changelog present-without-entry.** Membership in the branch's changed-path
   set was the whole test. Once the changelog appeared among the changed paths
   the helper printed `verdict: present` unconditionally, even for a deletion,
   a reflow, or a whitespace-only edit that added no line. The pre-fix code
   computed a first-added line purely for display and printed `present`
   regardless of whether one was found.
3. **Failed git reads read as empty.** Every enumeration was wrapped in
   `2>/dev/null || true`. A corrupted index makes `git diff` fail; the failure
   became an empty category, the empty categories summed to a small total, and
   a broken repository reported `under caps` at exit 0.
4. **Self-matching content grep.** `--check-name` decided whether a plan-named
   artifact still existed by grepping file *contents* for the name. The
   document that made the name stale — the plan proposing an artifact that was
   never built — contains the name, so it matched itself. The check could not
   fail, which made `consistent` unfalsifiable.

Independent execution-based review found all four: a validator that ran the
scripts against adversarial fixtures, plus a cross-model reviewer. Prose
reviewers reading the same three files reported no issues. The fix — two
review-fix commits on the unmerged branch above, whose SHAs will change if the
branch is squash-merged — closed each hole and
committed a rerunnable fixture runner,
`tests/checking-pr-readiness/fixtures/run-helper-checks.sh`, which
asserts the exact verdict line and exit code for every documented output state
across all three helpers, all currently green.

### Recurrence (2026-08-06): a new helper, written with this learning in view

The pattern recurred on `checking-merge-readiness`'s new fetch helper,
`skills/checking-merge-readiness/scripts/fetch-pr-history.sh` — a script
authored with this document's discipline from the first draft (enumerated
header contract, distinct exit codes, "exit 4 is incomplete history, never a
silent partial"). It passed prose review, shellcheck, and a live-PR
byte-stability check, and an independent multi-reviewer pass (a cross-model
adversarial reviewer on a different model family, plus a validator that
reproduced each claim against fixtures before counting it) found three
reproducible holes the same day:

5. **Dead not-found guard (jq object construction over null).** jq's
   `{state, isDraft, ...}` construction applied to a `null` input yields an
   object of null fields, not the string `null`, so the guard comparing the
   constructed object against `"null"` never fired and a `pullRequest: null`
   response produced `complete: true` at exit 0. The fix tests the raw
   response before construction (`fetch-pr-history.sh:167-168`).
6. **Unvalidated `--merge-base` pass-through.** The sibling helpers' new
   pass-through flag trusted any value that resolved to a commit. Passing
   `HEAD` emptied the committed diff range and turned a diff-laden branch
   into a green `verdict: no changes on surface` at exit 0. The fix
   cross-checks the supplied value against the merge base the resolved
   default branch yields, or ancestry when no base resolves
   (`surface-report.sh:313-320`).
7. **SIGPIPE crash in the capped-listing pipeline.** `printf | head -25 |
   sed` under `set -euo pipefail` dies at exit 141 once the payload outlives
   `head` closing the pipe — exactly and only on the oversized surfaces the
   cap exists for, which is why a small live run never triggered it. The fix
   caps with `sed -n '1,25p'`, which drains its stdin
   (`surface-report.sh:206-212`).

All three fixes shipped in the same change as the fixtures that pin them:
`tests/checking-merge-readiness/fixtures/run-fetch-checks.sh` (31 assertions,
including not-found, null floor identity, mid-run failure, missing resume
cursor, and a 1.2MB body) and an extended
`tests/checking-pr-readiness/fixtures/run-helper-checks.sh` (154 assertions,
including 500-path and 900-file payloads sized to actually reproduce the
SIGPIPE race).

### Recurrence (2026-08-11): self-consistent evidence without authenticated execution

The same failure shape appeared at a larger boundary in `repo-gardener` and
assessment mode. A reconciliation result could be internally well formed while
its manifest omitted installed lanes, its receipt collections omitted complete
envelopes, or its authority claims were merely booleans written by the caller.
Provider authentication bound a receipt identifier only loosely enough to
permit replay against different canonical receipt content, and the stored last
operation fingerprint was checked for shape rather than recomputed from the
authenticated operation. Assessment mode could likewise accept a correctly
digested result claiming success for a command that was never run. Finally, a
configuration search could find `repository_portfolio_limit` in the wrong YAML
section and accept any positive value instead of the Release A contract value.

The correction makes each boundary verify the authority it claims. The
production CLI now consumes an exact installed-lane manifest, validates every
receipt envelope and its run/register identity, requires an independent
versioned write-authority record for write-capable scenarios, binds each
provider receipt identifier one-to-one to canonical receipt content, and
recomputes the operation fingerprint from authenticated operation material.
Assessment evidence must come from an authenticated owning runner outside the
assessed commit or from an allowlisted command that the evaluator reruns and
verifies. Policy parsing addresses only
`boundaries.repository_portfolio_limit` and requires the public Release A value
exactly. Structurally complete mutations now forge each previously accepted
shape, including a self-consistent assessment result for a command that does
not exist, so the tests prove the rejection boundary rather than merely testing
malformed input.

## Guidance

When a bundled helper's output is what an agent reads to decide a gate:

1. **Write the output states into the header as a contract before writing the
   logic.** Name each state, its verdict word, and its exit code, and make line
   1 of every output that verdict word. A caller that must parse prose cannot
   distinguish a pass from a failure to check.

2. **Commit a fixture runner that asserts every documented state.** Assert
   exactly the contract — the verdict line and the exit code as a pair — not
   substrings of the detail lines. Build throwaway repositories under a
   `mktemp` directory so the runner never writes to the repository under test,
   and make it rerunnable by anyone with no setup beyond `bash`.

3. **Give every state a fixture, especially the states that are not findings.**
   The absent-input, deferral, usage-error, and environment-failure states are
   where silent passes hide, because nobody writes a happy-path test for them.

4. **Include adversarial fixtures, not just representative ones.** A corrupted
   index, a record committed and then deleted, a file touched without adding
   content, and an empty flag value are all states a real branch reaches. Each
   of the four holes above is exactly one such state.

5. **Fail closed on every external read.** Route each read through a wrapper
   that distinguishes a failed read from an empty result and exits with the
   environment-failure code. `2>/dev/null || true` converts a broken
   environment into a clean bill of health.

6. **Check a guard's conditions for independent reachability.** A guard written
   as `A AND B` leaves the `A-and-not-B` and `not-A-and-B` states unhandled. If
   either can occur alone, each needs its own branch and its own verdict.

7. **Decide existence by structure, never by a content search that the claim
   itself can satisfy.** Match names against paths on the working surface.
   Content hits belong in the detail lines as context, not in the decision.

8. **Have a reviewer execute the helper, not only read it.** Reading verifies
   that the code says what it means to say. Only execution against a fixture in
   the adversarial state verifies that the state produces the documented output.

9. **Ship the adversarial fixtures in the same change as the helper, and check
   the named trap shapes explicitly.** The recurrence above happened on a
   helper written with items 1-8 in view, so treat these as a checklist, not
   background: a guard for an empty response must test the raw value before
   any jq object construction (`{a, b}` over null builds an object of nulls,
   which is truthy); a caller-supplied ref that decides what gets measured
   (`--base`, `--merge-base`, `--since`) must be validated against what the
   tool would have resolved itself, because a resolvable-but-wrong ref is the
   attack surface; and a capped listing under `pipefail` must use `sed -n`
   rather than `head`, with a fixture payload big enough to actually trigger
   the SIGPIPE race. "Merge now, harden the tests next" leaves the gate
   silently unfalsifiable for exactly the window that matters.

10. **Do not let an evidence artifact authenticate itself.** A valid schema,
    digest, and claimed exit code prove only internal consistency. Require an
    authenticated owning runner outside the assessed change, or rerun an
    allowlisted command and verify its exit code, standard output, and standard
    error at the assessment boundary.

11. **Bind provider identifiers to canonical content and operation material.**
    A receipt identifier must map one-to-one to the exact canonical receipt
    hash, must not replay across history entries, and any recorded operation
    fingerprint must be recomputed from the authenticated operation fields.

12. **Parse configuration by exact structural path and pin release constants.**
    Searching for a key anywhere in a document lets an unrelated section
    satisfy the gate. Require the named top-level section and its key exactly
    once, never let the same key in another section substitute for it, and
    compare against the exact public contract value rather than a looser
    predicate such as positivity.

## Why This Matters

A helper that cannot fail is worse than no helper. It converts an unchecked
class into a recorded pass, and the evidence pack then carries a green line
that no human will re-derive. The failure is silent by construction: the exit
code is 0, the verdict word is one of the documented ones, and nothing in the
output signals that the check did not happen.

Careful design does not prevent this. All three helpers were designed around
distinct outputs per state, with the reasoning written into the headers, and
all three shipped with holes anyway. The 2026-08-06 recurrence sharpens the
point: a fourth helper written by an author who had this very document in
context shipped three more holes of the same class, so designing for
falsifiability is necessary and still not sufficient — the gap closes only
when the adversarial fixtures exist and someone independent runs them. The gap is not between careless and
careful authoring; it is between reading code and running it. A prose reviewer
reads `if [ -z "$record_time" ] && [ ! -e "$record" ]` and confirms it handles
the missing-record case, which it does. Only executing it against a record that
was committed and then deleted reveals the state the conjunction drops.

The cost asymmetry favors the runner heavily. The runner is a single bash file
that builds its own fixtures and takes seconds to run. The alternative is a
gate that reports green on a branch it never actually checked, discovered — if
ever — long after the branch merged.

## When to Apply

Apply this whenever a skill bundles an executable whose output an agent treats
as evidence. It applies most strongly when the helper has states beyond
pass and fail — absent input, deferral to another gate, environment failure —
because those are the states that most often collapse into a pass.

It applies with less force to a helper whose only job is to print information a
human reads directly, where a wrong answer is visible at the point of use.

Do not treat prose review as a substitute here, and do not treat the author's
own execution as independent. The author runs the cases they designed for. The
value came from a reviewer running the scripts against states the author had
not imagined.

## Examples

**Deleted-record bypass.** The pre-fix guard required both conditions, and a
committed-then-deleted record satisfied only one. The fix dates the record from
its last commit alone and splits the absent-record case in two
(`skills/checking-pr-readiness/scripts/evidence-freshness.sh:353-378`; the
commit lookup routes through the same fail-closed wrapper as every other git
read, so a failed read exits 4 instead of reading as empty history):

```sh
# The record is dated by its last commit only. A record with no established
# committed write point must not certify anything as fresh.
read_last_commit "$record"
record_commit="$last_commit"

if [ ! -e "$record" ]; then
	if [ -n "$record_commit" ]; then
		printf 'verdict: stale record found\n'
		...
		exit 0
	fi
	printf 'verdict: no records\n'
	...
	exit 2
fi
```

A dirty record now gets its own verdict rather than certifying anything fresh
(`evidence-freshness.sh:380-394`), and a dirty described path is reported
stale outright (`evidence-freshness.sh:415-418`). Committed paths are ordered
by commit ancestry, never committer timestamps, which a skewed or rewritten
clock can defeat.

**Changelog present-without-entry.** Path membership is now only the first
test. The helper counts the added lines that carry content — a whitespace-only
addition is a formatting change, not an entry — and a zero count gets a
distinct verdict rather than falling into `present`
(`skills/checking-pr-readiness/scripts/changelog-union.sh:320-332`):

```sh
# Only added lines with content count as an entry: a blank or whitespace-only
# addition is a formatting change, not recorded branch work.
added_count=0
[ -z "$added_lines" ] ||
	added_count=$(printf '%s\n' "$added_lines" | grep -c '[^[:space:]]' || true)

if [ "$added_count" -eq 0 ]; then
	printf 'verdict: changed without entry\n'
	...
	exit 0
fi
```

**Failed reads as empty categories.** Every one of the five git enumerations
now goes through one wrapper that exits 4 on a non-zero status
(`skills/checking-pr-readiness/scripts/surface-report.sh:218-228`):

```sh
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
```

An unmeasurable committed count downgrades the result to `cap unverified`
rather than letting an under-cap total stand
(`surface-report.sh:307-310`).

**Self-matching content grep.** Existence is now decided against paths on the
working surface, with content hits demoted to detail
(`skills/checking-pr-readiness/scripts/evidence-freshness.sh:234-238`):

```sh
# Existence is decided by paths, not by prose. A content grep matches the
# plan that proposed the name as readily as the artifact that shipped — and
# matches the file naming itself — so the name is matched against the paths
# on the working surface, and the content hits are reported as detail only.
surface=$(git ls-files --cached --others --exclude-standard -- "$search_root" 2>/dev/null || true)
```

**The runner.** Each assertion compares the first output line and the exit code
against the documented pair, and nothing else
(`tests/checking-pr-readiness/fixtures/run-helper-checks.sh:27-41`):

```sh
check() { # check <state> <expected-verdict> <expected-exit> <cwd> <cmd>...
	state="$1" want="$2" want_code="$3" dir="$4"
	shift 4
	out=$(cd "$dir" && "$@" 2>&1)
	code=$?
	got=$(printf '%s\n' "$out" | sed -n '1p')
	if [ "$got" = "verdict: $want" ] && [ "$code" -eq "$want_code" ]; then
```

The adversarial fixtures are built inline. A corrupted index is one line
(`run-helper-checks.sh:93-95`):

```sh
s4=$(repo surface-broken)
printf 'not an index' >"$s4/.git/index"
check "surface: not run (failed git read)" "not run" 4 "$s4" "$surface" --cap reviewer=10
```

The deleted-record case (`run-helper-checks.sh:166-168`), the changelog edit
that removes a line without adding one (`run-helper-checks.sh:111-120`), and
the empty `--cap` name and empty `--check-name` values
(`run-helper-checks.sh:82` and `:184`) each get the same treatment. Running
`bash tests/checking-pr-readiness/fixtures/run-helper-checks.sh` reports every
assertion passing (`0 failed`).

## Related

- `docs/solutions/integration-issues/skills-cli-ref-not-checked-out.md` is the
  canonical statement of the meta-lesson this learning generalizes: a
  verification that cannot distinguish success from silent fallback is a
  false-positive generator. That doc's example is a one-off probe against a
  third-party CLI; this learning applies the same principle to first-party
  bundled scripts, where the durable fix is a committed fixture runner rather
  than a better ad hoc probe.
- `docs/solutions/workflow-issues/verify-disposition-claims-before-landing-a-prune.md`
  shows the same failure shape in prose claims: assertions that pass because
  nothing forces them to be checked against the actual artifact.
- `docs/solutions/best-practices/independent-fresh-context-review-for-agent-skills.md`
  covers the review-independence half of the same lesson. This learning adds
  that for an executable artifact, independence must include execution, not
  only fresh context.
- `docs/solutions/best-practices/cross-harness-dogfood-testing.md` makes the
  parallel point for skill bodies: a run is evidence only when the artifact
  under test is the one that actually executed.
- `skills/checking-pr-readiness/SKILL.md:183-194` maps helper exit codes and
  verdict lines onto the gate's status words — verdicts say what a class found,
  status words say whether the check happened.
- `tests/checking-pr-readiness/log.md:11` records the first green 34/34 run
  after the original fixes; the harness has since grown to 154 assertions.
- `skills/checking-merge-readiness/references/fetch-floor.md` names
  `fetch-pr-history.sh` the preferred transport for the merge-readiness review's history
  surfaces, which is exactly why a silent-pass hole in it would degrade every
  digest that relies on it.
- `tests/checking-merge-readiness/fixtures/run-fetch-checks.sh` states the
  generalizable question in its own header: the ways a fetch can look complete
  without being complete are the right thing to ask of any new bundled helper
  before trusting its exit code.
