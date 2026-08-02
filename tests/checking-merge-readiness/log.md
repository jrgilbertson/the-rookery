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

- 2026-08-02 | greenfield | stub self-check | pass | thin fixture server (no GraphQL projection); read-only perimeter; selectors; under-fetch; pagination including variable-bound `after`; auth-fail mode; every specimen serves the battery-shaped queries. Falsification-probed: write-verb message pinned (not exit code alone); unbound `$cursor` fails rather than paging from zero

## Behavioral battery

Harness: `../fixtures/bin/gh` + opaque `specimen-*` directories. Blind graders
for skilled/bare pairs. Scenario 11 uses real `gh` against real GitHub.

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
Re-grading a discriminating case blind on the final 331-line text remains open
soft work, not a hard block.

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

## Design notes carried forward

- Test seam lives in PATH/`CMR_FIXTURE`, never in shipped SKILL.md
- Do not simulate GitHub GraphQL in the stub
- `userContentEdits.diff` is a post-edit body snapshot, not a patch; pre-edit text is not fetchable once edited
- Never cite line numbers into this append-only log
- Assertions that pass for the wrong reason are the recurring defect — pin message, not only exit code; falsification-probe every guard
- Fetch contract is outcomes + completeness + a minimal floor, not a GraphQL field encyclopedia; incomplete payload removes merge the same way degraded history does
- Stub under-fetch tokens stay aligned once to that floor, then frozen — presence checks only, no selection-set projection

- 2026-08-02 | greenfield | step 2 reframe (adversarial-amended) | landed | SKILL.md surfaces/jobs + floor table + observed exhaustion + incomplete-payload cap; stub SERVED_CONNECTIONS expanded once (ids, pullRequestReview, editor, diff); self-check still green
