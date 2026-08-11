# Assessment-only PR readiness

This reference owns the unattended exact-subject/exact-revision branch. The
interactive workflow in `SKILL.md` remains unchanged for ordinary owner-facing
readiness requests.

## Bind the assessment subject

Resolve all of these from the live Git checkout and caller-produced stable
identity fields:

- one stable repository identity;
- one stable branch or pull-request subject identity; and
- the full commit OID at `HEAD` as `exact_revision`.

For a branch subject, resolve the exact symbolic `refs/heads/*` name currently
checked out at `HEAD`; compare that live name with the claimed subject. A
renamed branch therefore invalidates an older receipt. A detached HEAD cannot
support a branch subject, and candidate branches that merely point at the
detached commit do not repair that missing live binding; multiple such
candidates are ambiguous. For a pull-request subject, query current provider
state through the caller's read-only boundary and require exactly one pull
request in the bound repository whose head is the exact revision. Zero matches,
multiple matches, an unavailable query, or a branch/PR identity mismatch is
`action-required`. Never infer the subject from receipt prose, a display name,
or whichever local ref happens to point at the commit.

Run the current skill's steps 1 through 6 against that checkout. Always run the
surface helper with `--full`. Use current gate discovery, current helper
verdict/exit-to-status mapping, and every current sweep class. Assessment-only
does not restore an older gate workflow or redefine helper outcomes.

An exact-revision pass requires a clean checkout: no staged, unstaged, or
untracked path can be represented by the commit OID. A dirty surface returns
`action-required` with every dirty category named.

## Versioned receipt bundle

The assessment consumes exactly one
`checking-pr-readiness-receipt-bundle/v1`. The caller supplies the complete
JSON object inline or names one explicit readable regular file containing that
object. Do not scan the checkout, infer a default path, or fetch an unresolved
receipt identity from narrative text. A missing, unreadable, malformed, or
wrong-version bundle is `action-required`.

The bundle has exactly this semantic shape:

```json
{
  "schema": "checking-pr-readiness-receipt-bundle/v1",
  "assessment": { "<assessment fields below>": "..." },
  "receipts": [ { "<evidence receipt>": "..." } ]
}
```

The assessment member uses `receipt_references` only for receipt identities.
Each evidence receipt uses `evidence_references` only for exact-commit regular
file objects containing `path` and `sha256`. The two reference types are never
interchangeable. Resolve every receipt reference exactly once within the same
bundle, reject duplicate receipt identities and unreferenced substitutes, and
fail closed when any reference does not resolve.

## Assessment envelope

Return one JSON object with exactly this semantic shape:

```json
{
  "schema": "checking-pr-readiness-assessment/v1",
  "capability": "checking-pr-readiness",
  "capability_version": "<skill package revision or working-tree>",
  "repository": "<stable repository identity>",
  "subject": "<stable branch or pull-request subject identity>",
  "exact_revision": "<full commit OID>",
  "receipt_references": ["<receipt identity>"],
  "outcome": "pass | action-required",
  "gaps": ["<named gap>"],
  "observed_at": "<ISO-8601 UTC>",
  "mode": "assessment-only"
}
```

Construct `capability_version`, `repository`, `subject`, `exact_revision`, and
`observed_at` from the live skill package and checkout. The caller's assessment
member is a claim to validate, not an output template: never copy its
provenance fields into the returned envelope. Validate every bundle layer and
receipt element before field access. Malformed input returns the same normal
`action-required` envelope with named gaps, never a traceback or partial JSON.

`pass` uses an empty `gaps` array. `action-required` names every material gap.
Return the JSON receipt and a short plain-language summary only; do not present
the interactive Minto readout or decision menu.

## Required exact-revision chain

Every `verified` claim must name an inspectable machine-readable receipt that
binds the same repository, subject, and full `exact_revision`. Each receipt
also names its capability/version, ISO-8601 observation time, outcome/gaps, and
at least one evidence reference. Every evidence reference identifies an
existing regular file in the exact commit plus its content digest, and the
document's substantive fields must support the claimed outcome; a status word
alone is not evidence. A receipt is fresh only when:

- the referenced evidence exists with that digest at `exact_revision`;
- the receipt observation is not earlier than the exact commit time; and
- no later edit to the described evidence exists outside `exact_revision`.

The chain contains:

1. full working-surface receipt whose committed inventory exactly matches the
   helper's `--full` output and whose staged, unstaged, and untracked
   inventories are empty;
2. repository-gates receipt naming every discovered gate and its owner;
3. code-review receipt;
4. code-simplification receipt;
5. testing receipt, including browser/design applicability derived from the
   full surface;
6. plan-versus-delivered receipt;
7. learning-signal receipt;
8. targeted-sweep receipt carrying one verdict from each current class's
   enumerated set; class 11 is `not applicable` when repository discovery
   proves that no automated reviewer is configured. Every configured automated
   reviewer must use a repository-resolved cap for a pass, so `cap unverified`
   remains a gap for that reviewer. Discover reviewer identities and caps from
   repository workflow, app, gate, or review-tool configuration; the
   repository-gates evidence document cannot attest its own discovery;
9. preflight receipt confirming this exact chain converged with no unresolved
   finding or bypass.

A clean `pass` requires every applicable chain receipt to report a successful
or `not applicable` result, with no unresolved finding and no bypass. A missing
receipt, stale receipt, cross-repository, cross-subject, or cross-revision
binding, empty evidence inventory, missing evidence, digest mismatch,
substantively unsupported outcome, unresolved finding, uncertain
classification, narrative-only claim, attestation, or bypass request yields
`action-required` with the exact defect named. Never invent or repair evidence
inside the assessment.

## Completion

The assessment is read-only. Do not write a receipt into the repository, stage,
commit, push, open a pull request, or run an owner decision menu. Return the
receipt once and stop.
