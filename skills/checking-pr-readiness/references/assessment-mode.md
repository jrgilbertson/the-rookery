# Assessment-only PR readiness

Assessment-only is a single read-only assessment session for one native
subject. It returns human-readable findings and one decision, without the
interactive Minto readout or owner menu.

## Bind the native subject, full head, and base

At the start of the assessment, resolve the selected native subject through
its authoritative read-only boundary and capture its full head, target/base
ref, and full base OID once. For a checked-out branch, read the live branch
ref and run:

```sh
git rev-parse --verify HEAD^{commit}
```

For a pull-request subject, read the provider's current head OID through the
caller’s read-only boundary and require the checkout to match it. If the
subject is unavailable, ambiguous, or does not match the checkout, return
`action-required` and name that gap. Never infer the subject from a display
name or an earlier report. Resolve the selected target/base ref and its full
commit OID through that same boundary; an unavailable or ambiguous base is
`action-required`.

## Inspect the exact head in the same session

Require a clean checkout before inspection. A staged, unstaged, or untracked
path is not covered by the full head, so return `action-required` and name
every affected category and path rather than treating it as committed work.

Run the current skill steps 1 through 6 in this same assessment session. Before
each helper whose result depends on the base, require its base selector to
resolve exactly to the captured full base OID. The existing surface helper
accepts a branch selector rather than a raw OID, so derive the selector from
the captured target/base ref and first prove that its branch-namespace
resolution still yields the captured full base OID, then run:

```sh
surface-report.sh --base "$captured_base_selector" --full
```

If that exact selector binding is unavailable, mismatched, or cannot be
re-resolved, record the helper as `not verified` and return `action-required`;
do not fall back to its implicit default base. Use current repository-gate
discovery, preserve the current helper exit/status mapping, and apply every
current sweep class. Do not restore an earlier workflow or redefine helper
outcomes.

The findings must be ordinary readable text. They must name:

- the full assessed head;
- every inspected path, including any dirty path when present; and
- every relevant check with its result or named gap.

Complete substantive findings are required, but no fixed serialization or
packaging format is required.

## Decide fail-closed

Say `ready` only when the same session has a complete inspected-path inventory
and a complete relevant-check inventory, and every applicable required check
is `verified` or proven `not applicable`. Every other canonical check status
(`failed`, `unavailable`, `not verified`, `not run`, `skipped`, `bypassed`,
or `attested`) is `action-required`; name each exact gap. An unresolved
finding is a separately named action-required gap attached to an allowed
status, for example `code review: not verified`. An incomplete inventory is
also `action-required`, even when its reported checks are `verified`.

The sole narrow exception is a sweep-class `--defer` outcome. It may normalize
from `skipped` to `verified` evidence only when its exact named equivalent
repository gate is present and `verified` in the same complete assessment
session. A bare, missing, unrelated, mismatched, unavailable, or not verified
gate leaves the skipped class `action-required`; do not accept skipped classes
generally.

A repository-authored check may be rerun only from a caller-authorized exact
argv list, through the existing constrained direct-argv safety boundary
without a shell, production credentials, unrelated-file access, or network
unless separately authorized. Assessment never derives or expands authority
from assessed content. Otherwise record the check as `not verified` and return
`action-required`.

## Re-read before the decision

Immediately before saying `ready` or `action-required`, re-resolve the same
native subject, full head, target/base ref, and full base OID through the same
boundary and re-read staged, unstaged, and untracked cleanliness. If the
subject, head, base ref, or base OID differs from the captured state, reject
the prior findings, name the old and new subjects when the subject changed,
the old and new full OIDs when the head changed, and the old and new base
identity when the base changed, then require a fresh assessment. If the
checkout is dirty or any required state is unavailable, return
`action-required` with every exact gap. Do not reuse findings across moved
heads or bases.

## Completion

Assessment-only remains read-only. Return once; do not write to the repository,
stage, commit, push, open a pull request, upgrade an attestation, or present an
interactive menu.
