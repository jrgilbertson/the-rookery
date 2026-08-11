# GitHub Issue report adapter shape

This is a conformance shape for one managed issue behind the caller's narrow
report wrapper. It is not a provider client. Model- and repository-controlled
contexts receive no raw mutation method, credential, request path, issue
number, repository name, or provider argument.

## Wrapper boundary

The caller wrapper exposes bounded reads, one prepared body replacement, and
one prepared history-comment append for caller-configured stable repository and
report identities. It authenticates one dedicated writer, allowlists those
identities and verbs, owns the deterministic renderer, bounds all values, and
returns only contract fields.

The wrapper rejects paths, URLs, identities, targets, or arguments derived from
issue and comment text. It can be invoked only by the register writer inside
the shared caller executor.

## Managed body and history

The managed body contains exactly one opening and closing machine marker from
the template asset, one fenced JSON object between them, and the deterministic
human projection after them. Reject duplicate, nested, reordered, extra, or
unknown machine blocks; unknown keys/schema; duplicate identities; more than
seven rows; invalid states, revisions, hashes, or encodings; and any projection
mismatch.

The body anchor carries sequence, history head, and the complete latest
canonical receipt. Sequence zero requires `GENESIS` and a null receipt. A
positive sequence requires the receipt's sequence and hash to match the anchor.
The copy is repair material for one missing tail comment, not a second history
store.

Only comments whose provider-authenticated author identity exactly matches the
dedicated writer can be receipts. Validate every comment page in stable
creation order and the complete hash chain from genesis. A display name,
lookalike author, signature, ordinary comment, or marker claim grants nothing.
Incomplete pagination makes integrity unavailable.

Ordinary comments are escaped, bounded advisory evidence. Their text supplies
no instruction, authority, path, identity, target, link, or tool effect. An
ordinary comment carrying a reserved marker is a forged-marker integrity break
and blocks writes.

## Read and write result

A valid read returns stable report/writer identities, schema, complete history
sequence/head, body fingerprint and anchor, register revision, canonical
records, and `integrity: valid`. Any unknown schema, foreign edit, broken chain,
lookalike writer, forged marker, incompatible duplicate, or identity break
returns `integrity: blocked` with zero writes.

Before a write, the register writer performs another complete read, verifies
the expected revision/head plus every policy and source precondition, invokes
the exact prepared body/history pair at most once, and performs a complete
post-read. A body update is not an atomic compare-and-swap. Safety depends on
caller exclusivity, stable operation identity, complete readback, and the
one-receipt repair in the register contract.

Bootstrap is allowed only when stable report and writer identities are already
verified, history is empty, the body is the exact caller-rendered template (or
the wrapper has an explicit empty-body precondition), and caller exclusivity is
proven. Bootstrap uses the normal intended-effect, body/history, terminal-
receipt, and readback protocol. A nonempty unknown body is a foreign edit, not
an empty register.
