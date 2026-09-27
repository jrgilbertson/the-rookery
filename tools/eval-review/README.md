# Eval review

Local inspection and feedback for frozen skill-evaluation rounds. One server
reads either a single manifest or one repository index of manifests, and writes
only the feedback file for the skill being reviewed. It does not launch a
model, grade output, price a call, or run a job.

The page itself is `viewer.html` in this directory, served unchanged when that
file is present. Keep its CSS and script inline. Model output is data: render
it as text, and trust `bindings` for pass, cost, and activation claims.

## Launch

One manifest:

```sh
python3 tools/eval-review/review.py \
  --manifest path/to/manifest.json \
  --feedback path/to/feedback.json \
  --port 8765
```

One repository:

```sh
python3 tools/eval-review/review.py \
  --index path/to/repo-index.json \
  --port 8765
```

`--index` cannot be combined with `--manifest` or `--feedback`. The process
binds `127.0.0.1` and prints `http://127.0.0.1:PORT`. `--port` defaults to 0
and asks the OS for a free port. Put real manifests, feedback files, and the
index outside the repository. `fixtures/manifest.json` is public synthetic data
for the server tests, not an execution record.

### Repository index

The index is the whole configuration. The server does not scan a checkout.

```json
{
  "repository": "the-rookery",
  "skills": [
    {
      "id": "checking-simplicity",
      "manifest": "checking-simplicity.json",
      "feedback": "checking-simplicity-feedback.json"
    }
  ]
}
```

`repository` and each skill `id` match `^[A-Za-z0-9][A-Za-z0-9._-]{0,80}$`.
`manifest` and `feedback` are absolute paths, or paths relative to the index
file's directory. Each entry names one skill. The id must equal that manifest's
`skill.name`. Catalog order is the file order, and the first entry is the
default skill.

Startup fails if the index is missing, malformed, or empty; if an id is
invalid or duplicated; if a manifest cannot be read as a schema-1 round whose
skill name equals the id; if two feedback paths are the same file; or if a
feedback path is the index, any configured manifest, or any listed evidence
path. Those checks follow symlinks, hard links, and another spelling of the
same path. A listed path counts even when its file or evidence root is missing
or the root is not a directory. A listed evidence file that is missing,
unreadable, or not a regular file stays a manifest error and does not, by
itself, stop startup.

Every load compares the manifest skill name with the configured skill id. When
they differ, the review has no cases, bindings, or evidence, and feedback is
not saved. Restoring a manifest whose skill name matches the id serves that
skill again.

A single-manifest launch uses the same review routes with one skill. Its
catalog `repository` is null. The skill id is that manifest's skill name when
the name is a valid id. When the only manifest has no valid skill name, the
catalog id is empty and the review is selected by omitting `skill`.

Every request must send one Host header, `127.0.0.1:PORT` or `localhost:PORT`.
A feedback write must also send one Origin header, `http://127.0.0.1:PORT` or
`http://localhost:PORT`. A repeated Host, Origin, or Content-Length header, or
a Transfer-Encoding header, is rejected with `{"error":"Rejected."}` and no
manifest, feedback, or evidence body. Host and framing checks run before a
skill selector is read. A feedback write checks Origin and the body before
that selector or any skill file is opened. Request bodies larger than 65536
bytes are refused and nothing is written.

A feedback save must not resolve to the index, to any configured manifest, to
another skill's feedback file, or to a listed evidence path. That includes
another path spelling, a symlink, or a hard link, including one introduced
after startup. The same check runs before a review read loads feedback, and
the read, the check, and the write share one lock across every skill. When
the feedback path is such an alias, the review still shows the selected cases
and returns no feedback items. `feedback.error` is `Feedback path overlaps a
review input.` The files are left unchanged. A save is rejected the same way.

Startup also rejects feedback paths whose realpaths match after Unicode NFC
and case folding, including paths that do not exist yet. Names that differ
only by case, or by composed and decomposed accents, are ambiguous. This is a
portable configuration restriction for filesystems that ignore case or
normalization. It does not mean those spellings are one inode. Symlinks and
hard links are still decided by file identity.

## Routes

| Method | Path | Response |
| --- | --- | --- |
| GET | `/` | `viewer.html` as `text/html` when that regular file is inside this directory. Otherwise `404` `{"error":"viewer.html is not present"}`. |
| GET | `/api/skills` | `{repository, skills: [{id, name}], default_skill}`. Names are manifest skill names. The catalog contains no filesystem paths. |
| GET | `/api/review` | Display manifest, feedback, errors, and bindings for the selected skill. |
| POST | `/api/feedback` | JSON feedback write for the selected skill. `Content-Type: application/json`. |
| GET | `/evidence/<id>` | One file listed by the selected skill, as `text/plain; charset=utf-8` with `X-Content-Type-Options: nosniff`. |

Add `?skill=<id>` to choose a catalog skill on `/api/review`, `/api/feedback`,
and `/evidence/<id>`. An omitted `skill` selects `default_skill`. An unknown
id is `404`. An empty, repeated, or malformed `skill` value is `400`
`{"error":"Rejected."}`. There is no path parameter. Other query keys are
ignored and are never opened as files.

`/api/review` omits `evidence_root` and `files`. Evidence links are
`/evidence/<id>`, with the same `skill` query when a catalog skill is selected.
Unlisted ids, `..`, and symlinks that resolve outside the evidence root are
`404` and return no file bytes. Duplicate case, round, grade, and evidence ids
in another skill's manifest are not served or written for the selected skill.

## Manifest

`schema` is `1`. `round.id` is the frozen round. A case with `runs: []` and
`grades: []` is a pre-run case. `null` means the measure was not captured.

```json
{
  "schema": 1,
  "title": "Checking-simplicity synthetic review",
  "skill": {"name": "checking-simplicity", "revision": "synthetic-public"},
  "round": {"id": "2026-09-26-synthetic", "frozen": true, "note": null},
  "evidence_root": "evidence",
  "files": [{"id": "protect-with-trace", "path": "protect-with-trace.json"}],
  "cases": [],
  "triggers": []
}
```

`evidence_root` is relative to the manifest file, or absolute. Each `files`
path is relative to that root and cannot be absolute or contain `..`.

Cases use `id`, `title`, `prompt`, `inputs` (`label`, `text`), `expected`,
`assertions` (`id`, `text`, `check` of `deterministic` or `judgment`),
`provenance`, `runs`, and `grades`. A run uses `id`, `target`, `arm`
(`with_skill` or `without_skill`), `model`, `settings`, `skill_availability`
(`verified`, `unverified`, or `missing`), `output`, `summary`, `duration_ms`,
`tokens` (`input`, `output`, `total`), `cost`, and `evidence` (`id`, `label`).
`skill_availability: "verified"` means the arm's intended availability was
checked. Whether the skill was supposed to be present is the `arm` value.

`cost` is `null` or `{"usd": number, "basis": "api_equivalent_estimate" | "subscription_charge"}`.
A null cost is unknown. It is not zero. Show an API-equivalent estimate and a
subscription charge as different figures.

A grade uses `id`, `grader`, `target`, `run_ids`, `verdict` (`pass`, `fail`,
`mixed`, or `null`), `assertions` (`assertion_id`, `result` of `pass`, `fail`,
or `unknown`, `evidence`), `summary`, and `evidence`.

A trigger uses `id`, `query`, `expected` (`trigger` or `no_trigger`), `note`,
and `observations`. An observation uses `id`, `target`, `description_revision`,
`role` (`training`, `validation`, or `fresh`), `used_for_selection`, `observed`
(`loaded`, `not_loaded`, or `unverified`), `basis` (`native` or
`listing_proxy`), `summary`, and `evidence`.

Ids match `^[A-Za-z0-9][A-Za-z0-9._-]{0,80}$`.

Malformed JSON, a schema other than `1`, or a missing round id returns a
manifest of `null` and an `errors` entry. A bad grade, run, or cost is named in
`errors`, nulled in the display manifest, and does not remove sibling cases.
The file on disk is not rewritten.

## Bindings

`/api/review` includes `bindings`. Use these instead of inferring a pass, a
zero cost, or an activation.

A `subject` binding has `record_type` `subject`, `subject_id`, `fingerprint`,
and `usable`. It identifies the case or trigger definition, including a
trigger's `note`. A case note or query note is saved against that fingerprint.
`usable` is false when the definition cannot be identified.

A `grade` binding has `subject_id`, `record_id`, `run_ids`, `fingerprint`,
`usable`, `evidence_state` (`present` or `missing`), `confirmed`, and
`verdict_claim`. `verdict_claim` keeps the grade's `pass`, `fail`, `mixed`, or `null` label.
`usable` stays true for an incomplete or inconsistent grade, so a person can
still disagree. `evidence_state` is `present` only when every grade assertion
has evidence text and every grade evidence file is readable and no larger than
2,000,000 bytes. An id that is merely listed, or a file that is oversized or
unreadable, is `missing`. The evidence route returns the same files and no
others.

`consistency` is one of `consistent`, `inconsistent`, and `incomplete`.
`confirmed` is true only for `consistent`. The grade must list each case
assertion id exactly once. A missing, unknown, or duplicate assertion id is
`incomplete` and unconfirmed, even when the original verdict remains visible.
With that exact list, every result must be `pass` or `fail`. `pass` is
`consistent` only when every result is `pass`. `fail` is `consistent` when at
least one result is `fail`, including when other assertions pass. A `pass` or
`fail` claim that breaks that rule is `inconsistent` and unconfirmed. `mixed` with both `pass` and `fail`, exact coverage, and readable evidence
stays unconfirmed and `incomplete`. A `mixed` grade with any other result
shape is `inconsistent`. Any remaining gap, including unknown results or
evidence that is not readable within the bound, is `incomplete`.

A `run` binding has `cost_state` (`unknown`, `api_equivalent_estimate`,
`subscription_charge`, or `malformed`), `duration_state` and `tokens_state`
(`unknown`, `present`, or `malformed`), `skill_availability`, and `usable`.
Read a number from the manifest only when the matching state is `present` or a
cost basis. Unknown and malformed measures have `null` in the display manifest.

An `observation` binding has `proof` (`recorded_trigger`,
`recorded_non_trigger`, or `unverified`), `basis`, `observed`, `role`,
`used_for_selection`, `selection`, `description_revision`, and `target`.
`recorded_trigger` means `basis` is `native`, `observed` is `loaded`, and
every cited evidence file is readable within the 2,000,000-byte bound. It is
the manifest's recorded claim beside that file, not a verified activation.
`recorded_non_trigger` is the same check with `observed: "not_loaded"`. The
server does not parse the trace, so a file whose text contradicts the claim
stays recorded. A viewer may show whether that recorded value matches the
trigger's expectation. It must not present the result as verified proof.
Empty, unlisted, oversized, or unreadable evidence stays `proof:
"unverified"`. A listing proxy is also `proof: "unverified"`.
`selection` is `training`, `validation`, `validation_used_for_selection`,
`fresh`, or `fresh_marked_used_for_selection`. Validation used for selection is
not untouched final evidence. Keep trigger observations out of the behavior
comparison.

## Feedback

The feedback file is `{"items": [ ... ]}` and is created on the first
successful save. Each stored item is:

```json
{
  "round_id": "2026-09-26-synthetic",
  "subject_id": "protect-export-boundaries",
  "grade_id": "grade-protect-with",
  "judgment": "agree",
  "note": "",
  "revision": 1,
  "saved_at": "2026-09-26T00:00:00Z",
  "fingerprint": "sha256:…"
}
```

`judgment` is `agree`, `disagree`, or `null`. `grade_id: null` with
`judgment: null` is a subject note, including a note before any grade exists.
A saved `judgment: null` on a grade is explicit No feedback. An absent item is
no feedback at all. Notes are limited to 4000 characters.

The server fingerprints the selected skill id, the round, subject, grade or
observation, the case or trigger definition, the referenced run output and
measures, and the sha256 and canonical resolved target path of each evidence
file those records name. For one manifest, that skill id is the manifest's
skill name when the name is a valid id. For an index, it is the configured
skill id. The same case bytes under another skill id are a different
fingerprint, so a save copied from one skill is rejected on the other.
Identical bytes at another root or relative path are a different fingerprint,
including when the file is oversized or unreadable. The canonical target is
recorded as soon as the contained path is known. Those files still do not
count as recorded activation or a confirmed grade. Editing a readable file
changes the fingerprint too. A first save that still sends the previous
fingerprint is rejected, and feedback saved against the previous fingerprint
is `binding: "earlier"`. Reusing a grade id
after that content changes does not inherit agreement. Show earlier feedback
as read-only. Only `binding: "current"` is the judgment for the evidence on
screen. Adding runs does not retire a pre-run note; editing the prompt, query,
or a referenced evidence file does.

POST `/api/feedback`:

```json
{
  "round_id": "2026-09-26-synthetic",
  "subject_id": "protect-export-boundaries",
  "grade_id": "grade-protect-with",
  "judgment": "agree",
  "note": "",
  "fingerprint": "sha256:…",
  "base_revision": 0
}
```

`fingerprint` is required. It must be the fingerprint currently displayed for
that subject, grade, or observation, including a subject note. The server
compares it with the fingerprint it just derived. A mismatch is `409
{"error":"Not saved: ...","item": null}` even when `base_revision` is 0, and
the file is not created or changed. A matching fingerprint with `base_revision:
0` creates the item. A later save sends the item's current `revision`. The
response is `200 {"item": ...}` only after the file is atomically replaced. A
stale revision for the same fingerprint is `409` with the current item, and
the file is unchanged. A bad round, an agreement without a usable grade or
observation, or a write the server cannot make is `400` or `500` with `Not
saved` and no success item.
Agreement is rejected for a malformed grade. It is allowed for an unconfirmed
grade. A symlink feedback path is refused so the write cannot follow the link.

## Tests

```sh
python3 -m unittest discover -s tools/eval-review -p 'test_*.py'
```
