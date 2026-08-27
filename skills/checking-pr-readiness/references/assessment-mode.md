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
Every element in `receipts` uses the exact
`checking-pr-readiness-evidence/v1` schema. Each receipt's
`evidence_references` identifies one complete evidence source: either an
exact-commit regular file object containing `path` and `sha256`, or the
complete evidence and result documents carried with their digests in the
caller-selected same-session bundle. The two reference types are never
interchangeable. Resolve every receipt reference exactly once within that one
bundle, reject duplicate receipt identities and unreferenced substitutes, and
fail closed when any reference is missing, ambiguous, or cannot be inspected.

For an outside-tree source, the evidence reference carries the literal
`transport: "bundle-inline"`, the live `exact_revision`, one nonempty
same-session `bundle_id`, one evidence document and one result document, and a
SHA-256 digest for each document. The evidence and result documents each carry
an identical `transport_identity` inside those digest-covered bytes: exact
repository, subject, revision, bundle ID, and receipt ID. The assessment accepts
that alternate packaging only when both digests and both identities match the
live receipt and checkout, every inline reference agrees on its one shared
bundle ID, and the documents satisfy every applicable substantive check. The
assessment derives that shared identity from the inline references, not from an
undocumented top-level member. It does not discover a second bundle, combine
documents from concurrent Workers, or fill missing transport fields from a
repository path.

## Assessment envelope

Return one `checking-pr-readiness-assessment/v2` JSON object with exactly this
semantic shape:

```json
{
  "schema": "checking-pr-readiness-assessment/v2",
  "capability": "checking-pr-readiness",
  "capability_version": "<skill package revision or working-tree>",
  "repository": "<stable repository identity>",
  "subject": "<stable branch or pull-request subject identity>",
  "exact_revision": "<full commit OID>",
  "receipt_references": ["<receipt identity>"],
  "outcome": "pass | action-required | UNKNOWN",
  "gaps": [{ "key": "<producer-owned correlation key>", "message": "<human-readable material gap>" }],
  "observed_at": "<ISO-8601 UTC>",
  "mode": "assessment-only"
}
```

Construct `capability_version`, `repository`, `subject`, `exact_revision`, and
`observed_at` from the live skill package and checkout. The caller's assessment
member is a claim to validate, not an output template: never copy its
provenance fields into the returned envelope. Validate every bundle layer and
receipt element before field access. Malformed transport and substantive receipt
failures return the normal `action-required` envelope with named gaps, never a
traceback or partial JSON.

`pass` uses an empty `gaps` array. `action-required` names every material gap
as exactly one object with only a nonempty producer-owned `key` and a
human-readable nonempty `message`. At the assessment boundary, send every
outer caller-supplied v2 claim, including a missing, null, or other non-object
member, through one integrity decision before accessing its fields. An invalid
outer claim returns the normal valid `UNKNOWN` envelope, never a pass, omission,
or traceback. Keys are equality-only correlation evidence: fixed semantic names
remain local to their production sites, are never parsed or mapped to behavior,
and do not include a list position, path, reference, timestamp, exact head, or
message content. One atomic corrective obligation keeps its key across exact
heads, receipt order, and message-only rewrites; repeated details may be
combined only when they name that same fixed obligation. Independent receipt or
evidence kinds use distinct fixed keys, so combining details cannot suppress
another obligation. The inner
`checking-pr-readiness-evidence/v1` receipt `gaps` arrays remain unchanged.
Return the JSON receipt and a short plain-language summary only; do not present
the interactive Minto readout or decision menu.

## Required exact-revision chain

Every `verified` claim must name an inspectable machine-readable receipt that
binds the same repository, subject, and full `exact_revision`. Each receipt
also names its capability/version, ISO-8601 observation time, outcome/gaps, and
at least one evidence reference. An evidence reference may identify an
existing regular file in the exact commit plus its content digest, or complete
evidence and result documents transported with their digests in that explicit
same-session bundle. In either form, the document's substantive fields must
support the claimed outcome; a status word alone is not evidence. A receipt is
fresh only when:

- the referenced evidence exists with that digest at `exact_revision`, or the
selected bundle carries complete digest-matched evidence and result documents
  whose digest-covered identities bind that same repository, subject,
  `exact_revision`, bundle, and receipt;
- the receipt observation is not earlier than the exact commit time; and
- no later edit to the described evidence exists outside `exact_revision`.

Evidence must unambiguously bind a versioned producer,
repository/subject/base/full-surface scope, the command or check identity and
arguments, a verified outcome, and nonempty structured results. A result may be
an exact-commit regular JSON file or a digest-matched document in the selected
bundle. Its producer, scope, command, and outcome bindings must agree with the
evidence. Assessment validates those semantics directly; it does not require a
published per-kind JSON Schema document or one internal result-file path. The
per-kind substance remains mandatory: gates name owner, command, outcome, and
result; review and simplification name the reviewed paths and findings; tests
name executable commands, outcomes, exit results, and applicability; the
remaining kinds bind their inventory to a structured result. Missing or
ambiguous bindings, name-only checks, zero-count assertions without review
scope, and owner/status tuples without executable gate results are
`action-required`.

Command-backed gate, review, simplification, and test results must also carry
execution evidence from a caller-authenticated owning runner that is outside
the assessed commit, or the assessment boundary must rerun the exact command
from a caller-owned allowlist outside that commit and verify its exit and
bounded result. Run it without a shell, production credentials, unrelated-file
access, network, or external-write capability unless the caller separately
authorizes a capability required by that exact command.
Repository-authored evidence and result JSON cannot authenticate their own
execution. A command that is absent, outside the discovered gate contract, or
reported successful without one of those independent proofs is
`action-required`, even when every receipt field and digest is structurally
valid.

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
binding, cross-bundle or cross-receipt transport identity, empty or mixed bundle
evidence inventory, missing evidence, digest mismatch,
substantively unsupported outcome, unresolved finding, uncertain
classification, narrative-only claim, attestation, or bypass request yields
`action-required` with the exact defect named. Never invent or repair evidence
inside the assessment.

## Completion

The assessment is read-only. Do not write a receipt into the repository, stage,
commit, push, open a pull request, or run an owner decision menu. Return the
receipt once and stop.
