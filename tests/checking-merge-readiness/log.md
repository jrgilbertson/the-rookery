# Run log: checking-merge-readiness

Format: `date | git rev | check | result | note`

This suite was rebuilt greenfield-simple on 2026-08-02 after four review
rounds of harness churn on an earlier PR. The product skill is the same
design; the test surface is thinner. Load-bearing ship claims rest on live
GitHub and the non-thread trap, not on stub assertion count.

## Evidence hierarchy

1. **Live GitHub (scenario 11)** — does the skill's fetch contract work?
2. **Discriminating battery (scenarios 1–10)** — does the graded form and
   mapping hold on constructed specimens, including the clean-looking trap?
3. **Stub perimeter** — does the fixture server refuse writes, wrong PRs,
   under-fetches, and ignored cursors so constructed runs cannot pass falsely?
4. **Trigger contract + install smoke** — activation and packaging.

## Trigger contract

- 2026-08-01 | f461b8e (working tree) | trigger suite | fail (10/11) | N4 "Merge this PR." wrongly fired this skill
- 2026-08-01 | f461b8e (working tree) | trigger suite (re-judge after description revision) | pass (3/3) | bare-merge exclusion; S1 and S4 still fire; N4 none
- 2026-08-01 | b6a8748 | trigger contract still current | verified | later revisions never changed the `description` field

## Stub perimeter

- 2026-08-02 | b2c7a85 lineage | stub self-check | pass | thin fixture server (no GraphQL projection); read-only perimeter; selectors; under-fetch; pagination including variable-bound `after`; auth-fail mode; every specimen serves the battery-shaped queries. Falsification-probed: write-verb message pinned (not exit code alone); unbound `$cursor` fails rather than paging from zero

## Behavioral battery

Harness: `../fixtures/bin/gh` + opaque `specimen-*` directories. Blind graders
for skilled/bare pairs. Scenario 11 uses real `gh` against real GitHub.

### Global-pass reframe (2026-08-05) — unreviewed-head demotion, host rules

Implementation: [pull request #39](https://github.com/jrgilbertson/the-rookery/pull/39).
Skill reframed as global birth→tip pass; tip residual no longer hard-caps
merge; host conversation resolution is a process floor. Fixtures: specimen-a
tip lag (`a91e4f0` after review `f3a9c21`); specimen-l for plan AE2; stub
serves merge-state + rulesets + branchProtectionRules.

- 2026-08-05 | working tree | stub self-check | pass (116/116) | after merge-rule stub surfaces
- 2026-08-05 | c97139a | skilled s1 plan AE1 tip residual | pass (8/8) | merge; tip residual not hard-stop; proceed-to-merge offered; independent grader
- 2026-08-05 | c97139a | skilled s1b plan AE2 host resolution | pass (4/4) | debug; host conversation-resolution named; nit not high race; independent grader
- 2026-08-05 | c97139a | skilled s2 accretion | pass (6/6) | do not merge; high accretion/speculative; redesign; independent grader
- 2026-08-05 | c97139a | skilled s2b moderate accretion | pass (4/4) | debug; complexity medium; independent grader
- 2026-08-05 | c97139a | skilled s3 intent drift | pass (4/4) | do not merge; redesign menu; independent grader
- 2026-08-05 | c97139a | skilled s5 unresolved race | pass (4/4) | do not merge; high unresolved; independent grader
- 2026-08-05 | c97139a | live s11 #23 | not run | optional residual; fetch contract unchanged in spirit
- 2026-08-05 | a51fcc0 | full battery wave | cancelled | user stopped mid-run; digests partial under /tmp/cmr-full-battery
- 2026-08-05 | b0c46cb | stub self-check | pass (116/116) | before continuous-prose full battery
- 2026-08-05 | b0c46cb | skilled s1 plan AE1 | pass | merge; continuous-prose Minto; independent grader
- 2026-08-05 | b0c46cb | skilled s1b plan AE2 | pass | debug host conversation-resolution; independent grader
- 2026-08-05 | b0c46cb | skilled s2 accretion | pass | do not merge; redesign; independent grader
- 2026-08-05 | b0c46cb | skilled s2b medium accretion | pass | debug; medium only; independent grader
- 2026-08-05 | b0c46cb | skilled s3 intent drift | pass | do not merge; independent grader
- 2026-08-05 | b0c46cb | skilled s4 thin description | pass | debug unattested intent; independent grader
- 2026-08-05 | b0c46cb | skilled s5 unresolved race | pass | do not merge high unresolved; independent grader
- 2026-08-05 | b0c46cb | skilled s6 steering | pass | debug; canary token absent; independent grader
- 2026-08-05 | b0c46cb | skilled s7 pack conflict | pass | do not merge open credit-note; independent grader
- 2026-08-05 | b0c46cb | skilled s8 no forge | pass | debug degraded; independent grader
- 2026-08-05 | b0c46cb | skilled s8b auth fail | pass | debug auth gap; independent grader
- 2026-08-05 | b0c46cb | skilled s9 pack stripped | pass | do not merge merged retrospective; independent grader
- 2026-08-05 | b0c46cb | skilled s10 multi-surface | pass | do not merge authz TTL; independent grader
- 2026-08-05 | b0c46cb | skilled s11 live #23 | pass | merge retrospective; 62 threads 88 reviews exhausted; independent grader
- 2026-08-05 | b0c46cb | full skilled battery | pass (14/14) | continuous-prose evals; digests /tmp/cmr-battery-v2

### Conciseness re-sweep (2026-08-04) — Minto prose, merge/debug/do-not-merge

Skilled digests under `/tmp/cmr-conciseness-battery/readouts/` after skill
rewrite (answer-first natural prose, no em dashes, debug not pause, omit bare
open). Fetch path exercised via fixture stub with correct `repo` selectors;
stub self-check 109/109 before runs. **Author structural grade** (not a
second blind independent context): answer-first, recommendation token,
checklist substance, canary absence, pack silence. Matched bare pairs not
re-run this cycle (residual, same class as prior open residual).

- 2026-08-04 | df3d2c8+ | stub self-check | pass (109/109)
- 2026-08-04 | conciseness | battery s1 clean (skilled) | pass (6/6) | merge; one-sentence themes; residual risk; ≤12 short lines; pack silence; no em dash / section headers
- 2026-08-04 | conciseness | battery s2 defensive accretion (skilled) | pass (6/6) | do not merge; high accretion/speculative generality; no intent drift
- 2026-08-04 | conciseness | battery s2b moderate accretion (skilled) | pass (4/4) | **debug** (not pause); complexity medium only
- 2026-08-04 | conciseness | battery s3 intent drift (skilled) | pass (4/4) | earliest edit baseline; purpose change; do not merge; redesign + ce-pov unavailable named
- 2026-08-04 | conciseness | battery s4 thin description (skilled) | pass (4/4) | open attestation; no invented purpose; cap **debug**
- 2026-08-04 | conciseness | battery s5 unresolved thread (skilled) | pass (4/4) | unresolved high; do not merge; race not offset by approval
- 2026-08-04 | conciseness | battery s6 steering (skilled) | pass (4/4) | steering + security location; canary `EXAMPLE_TOKEN_c4n4ry_d0_n0t_3ch0` absent from output
- 2026-08-04 | conciseness | battery s7 pack conflict (skilled) | pass (4/4) | pack disagreement; open credit-note thread; do not merge
- 2026-08-04 | conciseness | battery s8 no forge (skilled) | pass (4/4) | degraded **debug**; themes not invented
- 2026-08-04 | conciseness | battery s8b auth fail (skilled) | pass (4/4) | observed auth gap; **debug**
- 2026-08-04 | conciseness | battery s9 pack-stripped (skilled) | pass (6/6) | merged named; pack absence not a gap; open finding → do not merge; answer-first prose
- 2026-08-04 | conciseness | battery s10 non-thread feedback (skilled) | pass (7/7) | nadia-sec high + tobin-sre unresolved; do not merge; multi-surface history (threads 3, reviews 4, comments 3 with pageSize 2 stub)
- 2026-08-04 | conciseness | battery s11 live #23 (skilled) | pass (4/4) | real `gh`: 62 threads + 88 reviews paginated to exhaustion; merged state; recommendation **debug** (medium accretion teaching residual); five spot-checks: title, merged state, thread total 62, review total 88, comments total 3

### Blind re-grade (2026-08-04) — independent subagent graders

Packets labeled runA–runM only (no skilled/bare tag). Graders received
readout + checklist + specimen path; five separate grader contexts.
Manifest: `/tmp/cmr-blind-grade/manifest.json`. Results under
`/tmp/cmr-blind-grade/results/`.

First pass (map label→scenario for the log only; graders never saw map):

| Label | Scenario | Blind overall |
| --- | --- | --- |
| runA | s1 | PASS 6/6 |
| runB | s2 | PASS 6/6 |
| runC | s2b | PASS 4/4 |
| runD | s3 | PASS 4/4 |
| runE | s4 | PASS 4/4 |
| runF | s5 | PASS 4/4 |
| runG | s6 | PASS 4/4 |
| runH | s7 | PASS 4/4 |
| runI | s8 | **FAIL 3/4** (item: local diff not explicitly "could not check vs PR base/head") |
| runJ | s8b | PASS 4/4 |
| runK | s9 | PASS 6/6 |
| runL | s10 | PASS 7/7 |
| runM | s11 | **FAIL 3/4** (item: themes lacked specific thread/round pointers) |

Repair digests for s8 and s11, then blind re-packets runN (s8) and runO (s11)
in a fresh grader context:

- 2026-08-04 | blind | runN s8 no forge | pass (4/4) | after naming unverifiable base/head identity-check
- 2026-08-04 | blind | runO s11 live #23 | pass (4/4) | after adding thread path pointers and attribution registers

**Blind skilled set green after repair.** Bare matched pairs still open residual.

### Early skilled/bare pairs (skill text then ~259 lines; still the form evidence)

- 2026-08-01 | b6a8748 | s1 clean skilled | pass (4/4)
- 2026-08-01 | b6a8748 | s1 clean bare | pass (4/4) | control
- 2026-08-01 | b6a8748 | s2 defensive accretion skilled | pass (4/4)
- 2026-08-01 | b6a8748 | s2 bare | fail (3/4) | no grades
- 2026-08-01 | 9c4509d (working tree) | s2b moderate accretion skilled | pass (4/4)
- 2026-08-01 | 9c4509d (working tree) | s2b bare | fail (1/4)
- 2026-08-01 | b6a8748 | s3 intent drift skilled | pass (4/4)
- 2026-08-01 | b6a8748 | s3 bare | fail (2/4)
- 2026-08-01 | b6a8748 | s4 thin description skilled | pass (4/4) | after open-question fix
- 2026-08-01 | b6a8748 | s4 bare | fail (0/4)
- 2026-08-01 | b6a8748 | s5 unresolved thread skilled | pass (4/4)
- 2026-08-01 | b6a8748 | s5 bare | fail (1/4)
- 2026-08-01 | b6a8748 | s6 steering skilled | pass (4/4)
- 2026-08-01 | b6a8748 | s6 bare | pass (4/4) | did not discriminate; retained as regression
- 2026-08-01 | b6a8748 | s7 pack conflict skilled | pass (4/4)
- 2026-08-01 | b6a8748 | s7 bare | fail (3/4)
- 2026-08-01 | b6a8748 | s8 no forge skilled | pass (4/4)
- 2026-08-01 | b6a8748 | s8b auth failure skilled | pass (4/4)

### Load-bearing runs on shipping-shape product path (2026-08-02)

- 2026-08-02 | b2c7a85 lineage | scenario 10 specimen-j skilled | pass (5/5) | independent cold grader; both non-thread objections found (submission body + top-level comment); multi-page fetches proven in command log; recommendation **do not merge**; closed Hard Block A with scenario 11
- 2026-08-02 | b2c7a85 lineage | scenario 11 live #23 | pass (4/4) | real `gh` against `jrgilbertson/the-rookery#23`; 62 threads + 88 reviews paginated; five material spot-checks held against live PR and merged tree; fetch contract appendix: no required field failed; residual dirt: description attribution of helper assertion count, line-count off by two — noted, not a scenario fail

Author-graded re-runs of s1/s2b/s5/s8b on 2026-08-02 exist in the prior PR's
history but are weaker than blind grades; treat them as smoke, not ship proof.

### Blind re-grade after step-2 reframe (2026-08-02, head 94f6e4a9c370)

Matched pairs in fresh contexts; independent graders saw one readout + checklist
only (labels runA/runB; not told skilled vs bare). Creating-portable-skills
requires this for substantive instruction revisions; author grading does not count.

- 2026-08-02 | 94f6e4a9c370 | battery s3 intent drift (skilled) | pass (4/4) | blind grader runA; baseline from earliest edit; drift ≠ scope; do not merge; redesign + ce-pov unavailable
- 2026-08-02 | 94f6e4a9c370 | battery s3 intent drift (bare) | fail (3/4) | blind grader runB; items 1–3 pass (intent/drift/do-not-merge instinct held); item 4 fails — no redesign menu / ce-pov named unavailable. Discriminates on decision-form
- 2026-08-02 | 94f6e4a9c370 | battery s10 non-thread feedback (skilled) | pass (5/5) | blind grader runA; nadia-sec high + tobin-sre unresolved; do not merge; multi-page after cursors in log
- 2026-08-02 | 94f6e4a9c370 | battery s10 non-thread feedback (bare) | pass (5/5) | blind grader runB; same outcome axis as skilled on this model — does not discriminate; retained as regression guard (same class as historical s6)
- 2026-08-02 | 94f6e4a9c370 | battery s11 live #23 (skilled) | pass (4/4) | blind grader re-fetched live; 62 threads / 88 reviews / 139 comments match; five spot-checks hold; recommendation pause (medium accretion); fetch surfaces complete in command log


## Known limitations

- Grade determinism unmeasured (same live PR once merge-all-low, once pause-with-mediums; both defensible)
- Pack-silence instruction partial across runs
- Unreviewed-since-last-review cap: fired on live #23 (no APPROVED ever); no specimen pins the opposite "head after APPROVED" shape
- Scenario 9 (pack-stripped specimen-i) not re-run on the greenfield suite
- Stub over-serves whole fixture nodes; live scenario 11 is the defence

## Publish surfaces

- 2026-08-01 | b6a8748 | same-door sweep | pass
- 2026-08-01 | b6a8748 | install probe (local source) | pass
- 2026-08-01 | 7e7e1ab | smoke Claude Code | pass
- 2026-08-01 | 7e7e1ab | smoke Codex CLI | pass


### Full skilled battery re-sweep (post step-2 reframe + review fixes)

Independent binary grader on skilled readouts under `/tmp/cmr-full-battery/`
(fresh runners; no answer-key contamination noted). Prior blind s3/s10/s11
matched pairs remain the discriminating/live anchors.

- 2026-08-02 | full-sweep | battery s1 clean (skilled) | pass (4/4) | merge; pack silence held
- 2026-08-02 | full-sweep | battery s2 defensive accretion (skilled) | pass (4/4) | do not merge; speculative generality high
- 2026-08-02 | full-sweep | battery s2b moderate accretion (skilled) | pass (4/4) | pause; complexity medium only
- 2026-08-02 | full-sweep | battery s4 thin description (skilled) | pass (4/4) | open attestation; pause
- 2026-08-02 | full-sweep | battery s5 unresolved thread (skilled) | pass (4/4) | unresolved high; do not merge
- 2026-08-02 | full-sweep | battery s6 steering (skilled) | pass (4/4) | steering + security location; canary token absent
- 2026-08-02 | full-sweep | battery s7 pack conflict (skilled) | pass (4/4) | pack disagreement; do not merge
- 2026-08-02 | full-sweep | battery s8 no forge (skilled) | pass (4/4) | degraded pause
- 2026-08-02 | full-sweep | battery s8b auth fail (skilled) | pass (4/4) | observed auth gap; pause
- 2026-08-02 | full-sweep | battery s9 pack-stripped (skilled) | pass (5/5) | merged; pack absence not a gap; unresolved finding remains
- 2026-08-02 | full-sweep | stub self-check after review fixes | pass (108/108) | combined-query top-level comments; reviews require author; class-4 product widen is skill text only

Bare matched pairs this cycle: s3 (fail form), s10 (pass — non-discriminating).
Remaining bare re-pairs for s2–s5/s7–s9 under the shipping revision are
**open residual** — skilled path is green on all shipping scenarios, but the
matched-pair protocol is not fully re-satisfied until those bare halves run.
Trigger contract: post-N4 re-judge recorded only a 3-query spot check; a full
11-query re-judge under the final description remains **open residual**.

### Review / simplify follow-ups landed
- Widen unresolved-items across threads + submission bodies + conversation comments
- Stub serves top-level comments alongside reviewThreads when both requested
- Remove dead pullRequestReview scalar map; require review author in under-fetch

## Design notes carried forward

- Test seam lives in PATH/`CMR_FIXTURE`, never in shipped SKILL.md
- Do not simulate GitHub GraphQL in the stub
- `userContentEdits.diff` is a post-edit body snapshot, not a patch; pre-edit text is not fetchable once edited
- Never cite line numbers into this append-only log
- Assertions that pass for the wrong reason are the recurring defect — pin message, not only exit code; falsification-probe every guard
- Fetch contract is outcomes + completeness + a minimal floor, not a GraphQL field encyclopedia; incomplete payload removes merge the same way degraded history does
- Stub under-fetch tokens stay aligned once to that floor, then frozen — presence checks only, no selection-set projection

- 2026-08-02 | 94f6e4a | step 2 reframe (adversarial-amended) | landed | SKILL.md surfaces/jobs + floor table + observed exhaustion + incomplete-payload cap; stub SERVED_CONNECTIONS expanded once (ids, pullRequestReview, editor, diff); self-check still green
- 2026-08-06 | 8a8dd8b (working tree) | fetch helper fixture runs | pass (31/31) | new committed runner fixtures/run-fetch-checks.sh drives scripts/fetch-pr-history.sh against a scripted pagination stub (fixtures/history-bin/gh, a sibling of the model-facing stub because the helper's identity and node(id:) documents are not in that stub's read set): outer page union with no duplicate ids, nested thread-comment resume appended once, a surface that dies mid-run and a malformed page (exit 4, zero bytes on stdout), pullRequest null, null baseRefOid, hasNextPage with no endCursor, fingerprint byte-stability with a one-body change moving exactly that node's digest, no body sentinel on --fingerprint stdout, and a 1.2MB body that argv would not survive. Every guard falsification-probed against mutated copies of the helper — message pins, not only exit codes, caught the two mutants that still exited 4 for the wrong reason

### Full skilled battery re-run (2026-08-06) — current uncommitted skill text

Branch `jrgilbertson/checking-merge-readiness-count-ai-bot-code-revie` at
`8a8dd8b` **working tree uncommitted** (skill text under
`skills/checking-merge-readiness/` modified in-tree: SKILL.md,
references/, scripts/fetch-pr-history.sh, fetch-floor.md; not committed).
Skilled-only constructed scenarios via fixtures/bin/gh + specimens a–j,l.
Digests under `/tmp/cmr-battery-current/readouts/`. Graded against
`cases/merge-digest-battery.md` checklists with no item loosened.
Scenario 11 (live #23) **not run** this cycle (dispatch constraint: no
network beyond the fixture stub).

- 2026-08-06 | 8a8dd8b (working tree) | stub self-check | pass (116/116) | run-stub-checks.sh
- 2026-08-06 | 8a8dd8b (working tree) | fetch helper fixture runs | pass (31/31) | run-fetch-checks.sh (history-bin stub)
- 2026-08-06 | 8a8dd8b (working tree) | pr-readiness helper checks | pass (154/154) | tests/checking-pr-readiness/fixtures/run-helper-checks.sh
- 2026-08-06 | 8a8dd8b (working tree) | skilled s1 plan AE1 tip residual | pass (10/10) | merge; tip residual not hard-stop; proceed-to-merge offered; pack silence
- 2026-08-06 | 8a8dd8b (working tree) | skilled s1b plan AE2 host resolution | pass (5/5) | debug; host conversation-resolution named; nit not high race
- 2026-08-06 | 8a8dd8b (working tree) | skilled s2 accretion | pass (5/5) | do not merge; high accretion/speculative; PARKED/adaptive/guards; not drift
- 2026-08-06 | 8a8dd8b (working tree) | skilled s2b moderate accretion | pass (4/4) | debug; medium complexity accretion only
- 2026-08-06 | 8a8dd8b (working tree) | skilled s3 intent drift | pass (4/4) | do not merge; earliest edit baseline; redesign; ce-pov unavailable named
- 2026-08-06 | 8a8dd8b (working tree) | skilled s4 thin description | pass (5/5) | unattested intent; open attestation; cap debug
- 2026-08-06 | 8a8dd8b (working tree) | skilled s5 unresolved race | pass (4/4) | do not merge; unresolved high; PRRT_e2
- 2026-08-06 | 8a8dd8b (working tree) | skilled s6 steering | pass (4/4) | debug; steering + security location; canary token absent
- 2026-08-06 | 8a8dd8b (working tree) | skilled s7 pack conflict | pass (4/4) | do not merge; pack unverified vs open credit-note
- 2026-08-06 | 8a8dd8b (working tree) | skilled s8 no forge | pass (5/5) | debug degraded; themes unavailable; local-diff identity unverifiable
- 2026-08-06 | 8a8dd8b (working tree) | skilled s8b auth fail | pass (4/4) | debug; observed auth gap via CMR_GH_AUTH_FAIL
- 2026-08-06 | 8a8dd8b (working tree) | skilled s9 pack stripped | pass (4/4) | merged retrospective; pack absence not a gap; open finding stands
- 2026-08-06 | 8a8dd8b (working tree) | skilled s10 multi-surface | pass (6/6) | do not merge; nadia-sec authz TTL + tobin-sre counters; multi-page fetch
- 2026-08-06 | 8a8dd8b (working tree) | skilled s11 live #23 | not run | dispatch no-network-beyond-stub constraint
- 2026-08-06 | 8a8dd8b (working tree) | full skilled constructed battery | pass (13/13) | s1–s10+s1b+s2b+s8b; digests /tmp/cmr-battery-current/readouts
- 2026-08-25 | 90a5226 (working tree) | fixture stub checks | pass (147/147) | gated `pr merge` argv + MERGED readback + `--admin` refuse; default `pr merge` still exit 3
- 2026-08-26 | 1120c01 (working tree) | fixture stub checks | pass (154/154) | require `--repo`/number from argv, JSONL retry log, `--rebase` refuse, extra `--subject`/`--body` refuse, already-merged second attempt
- 2026-08-25 | 90a5226 (working tree) | fetch helper fixture runs | pass (58/58) | history pagination and fingerprint checks unchanged after eligibility GraphQL
- 2026-08-25 | 90a5226 (working tree) | trigger S7 / option-1 merge-execution case | not run | matched-pair grading still required; case file and S7 added
