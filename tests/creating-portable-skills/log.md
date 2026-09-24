# Run log: creating-portable-skills

Format: `date | git rev | check | result | note`

## Scanner error propagation on 2026-09-24

The scanner correction changes only operational error handling. The production
fixture runner injects a read failure followed by a readable reference and a
traversal failure after partial results. Against `b46e4de`, both exit-status
assertions fail (33 passed, 2 failed). With the correction, all 35 assertions
pass, including existing matching and no-match controls. A separate real
unreadable-file reproduction exits 2 with no misleading zero-hit output.

This deterministic comparison covers the changed helper. The model evaluations
below retain their recorded source revisions; no new model execution or native
activation claim is made for this shell-only correction.

| Date | Git rev | Check | Result | Note |
| --- | --- | --- | --- | --- |
| 2026-09-24 | b46e4de, with new regression assertions | Production scanner fixtures | 33 passed, 2 failed | Both injected operational errors incorrectly returned success. |
| 2026-09-24 | b46e4de working-tree scanner correction | Production scanner fixtures | 35 passed, 0 failed | Read and traversal failures return nonzero; matching and no-match controls pass. |
| 2026-09-24 | b46e4de working-tree scanner correction | Real unreadable input | pass | Exit 2, empty stdout, permission diagnostic retained. |
| 2026-09-24 | b46e4de working-tree scanner correction | Official skill validator | pass | Cached skills-ref validator; no native activation claim. |
| 2026-09-24 | b46e4de working-tree scanner correction | Independent source review | pass | No findings; reviewer reran 35 assertions, shell syntax and dash no-match control. |
| 2026-09-24 | b46e4de working-tree scanner correction | Independent package review and simplification | pass | Helper qualification accepted; three simplification reviewers found no changes needed. |
| 2026-09-24 | b46e4de working-tree scanner correction | Repository pre-push gates | pass | Catalog, integrity, secrets and fixtures passed; elapsed 292 seconds. |

No model evaluation calls were made; dollar cost was not recorded for these
local checks. Elapsed time was not recorded except for the repository gates.

## Vendor-scope correction on 2026-09-24

The approved simplicity review reduced the correction to one reporting clause:
“When assessing vendor guidance, state its model or harness scope in the
recommendation.” The existing comparison protocol and case criteria are
unchanged. A separate reviewer inspected the earlier anonymous Grok packet
against that protocol and found all four answers satisfy its comparison item
through explicit wording or defined protocol references. That interpretation
does not replace the earlier official grades below.

The following delta uses Opus 5.5 at medium effort to grade Sol and gpt-6-sol
at high effort to grade Grok, with the same strict schema and target harness
versions recorded in the preceding round. Native executor configurations and
prompts remain unchanged. Only the four revised vendor answers are new.

Candidate3 changes only the vendor-scope clause in the review checklist. Four fresh revised executions are compared with four saved baseline executions under the identical clarified prompt and unchanged checklist. Unaffected cases retain their candidate1/candidate2 evaluation scope; this delta does not claim they were executed against candidate3. Dates are UTC.

| Date | Revision / reuse | Target, variant, repeat | Result | Reported cost; tokens; elapsed |
| --- | --- | --- | --- | --- |
| 2026-09-24 | c6b6051 saved baseline | gpt-6-sol high, prior, r1 | pass | cost not available; 91133 tokens; 54 s |
| 2026-09-24 | c6b6051 saved baseline | gpt-6-sol high, prior, r2 | fail (items 1) | cost not available; 109371 tokens; 84 s |
| 2026-09-24 | c6b6051 working-tree candidate3 | gpt-6-sol high, revised, r1 | pass | cost not available; 135341 tokens; 80 s |
| 2026-09-24 | c6b6051 working-tree candidate3 | gpt-6-sol high, revised, r2 | pass | cost not available; 133545 tokens; 64 s |
| 2026-09-24 | c6b6051 saved baseline | grok-4.7 high, prior, r1 | pass | $0.06524532; 97315 tokens; 187 s |
| 2026-09-24 | c6b6051 saved baseline | grok-4.7 high, prior, r2 | pass | $0.07193856; 116132 tokens; 217 s |
| 2026-09-24 | c6b6051 working-tree candidate3 | grok-4.7 high, revised, r1 | pass | $0.05814068; 93071 tokens; 164 s |
| 2026-09-24 | c6b6051 working-tree candidate3 | grok-4.7 high, revised, r2 | pass | $0.09046516; 128737 tokens; 215 s |

Combined selected evidence retains 52 results (48 first-two runs plus 4 containment repeats):

- sol: prior 5/12 → revised 12/12 overall; vendor prior 1/2 → revised 2/2.
- grok: prior 7/12 → revised 12/12 overall; vendor prior 2/2 → revised 2/2.

Combined selected first-two runs per case, including scoped reuse of unaffected outputs:

| Target | Prior → revised total tokens | Token change | Prior → revised median elapsed | Prior → revised reported execution cost |
| --- | --- | --- | --- | --- |
| sol | 1,635,375 → 2,346,629 | +43.5% | 60.5 s → 63.0 s | cost not available → cost not available |
| grok | 2,341,716 → 2,382,352 | +1.7% | 236.5 s → 190.5 s | $1.31875528 → $1.42061792 |

Execution cost above excludes grading and historical overhead, which remain included in the experimental-spend totals below. Sol token totals include cached input; missing dollar reports are not estimated.

- Grok containment including original extra repetitions: prior 2/4 → revised 4/4; unchanged by candidate3.

Candidate3 additional reported spend (four fresh revised runs and two graders): $0.26515784. Saved baseline copies add no new calls or charges. Missing Codex costs remain unavailable. All reported experimental spend across the retained history: $7.45868012; this is not total billing.
Accounting retains 83 distinct executor calls, including the earlier receipt retry, and deduplicates 14 copied baseline outputs using explicit provenance.

The Sol candidate3 revised r1 wrapper exited 1 because its self-reported receipt quotation was not an exact entrypoint quote. That log, receipt false value and original output remain unchanged. An independent reviewer accepted successful complete native reads whose exact bytes matched both frozen SKILL.md and changed review-checklist.md, plus the native digest output. The explicit admission record establishes intended-source observation and completed model execution, not a receipt pass or behavioral verdict; the Opus grader judged the full four-output packet. No candidate3 retry occurred.

Both new vendor packets included identical exact existing canonical definitions of full validation and matched comparisons, separate from anonymous outputs. The glossary adds no author conclusion or expected verdict. Old judgments remain historical; neither per-answer selection nor checklist weakening occurred.

Historical candidate2 sol vendor result: prior 1/2, revised 1/2. Its failures and costs remain preserved.
Historical candidate2 grok vendor result: prior 2/2, revised 1/2. Its failures and costs remain preserved.

All revised candidate3 vendor judgments pass.

- 2026-09-24 | c6b6051 working-tree candidate3 | independent final checklist and ship-rule review | pass | a reviewer separate from authors and graders inspected the complete package, artifacts, selected grades, provenance, costs, and log. All revised controls pass; targeted non-control results improve Sol 0/6 to 6/6 and Grok 1/6 to 6/6. The reviewer judges the gains worth the measured cost for these tested behaviors; increased Sol tokens and Grok dollars do not support a savings claim. Unaffected cases retain their earlier source scope.
- 2026-09-24 | c6b6051 working-tree candidate3 | structural and repository validation | pass | official cached skills-ref 0.1.1; all four pre-push gates; post-log and learning-update lint; final diff and private-artifact checks. Description and install layout remain unchanged; no new activation result is claimed.

## Quick adoptions on 2026-09-24: not ready

This follow-up adds focused validation for localized, low-risk guidance,
contains evaluations, and judges authoring conventions by their outcomes.
The preserved baseline is `c6b6051`. Candidate1 is the initial working-tree
package. Candidate2 adds a pre-dispatch check of the evaluation process's
working directory and resolved output paths; its other package files are
unchanged. Both candidates have the same entrypoint digest, so per-run
identity checks cover the entire seven-file package as well as the load
receipt. These are working-tree candidates, not committed revisions.

The selected evidence uses Codex CLI 0.156.1 with gpt-6-sol at high effort and
Grok CLI 1.0.41 with grok-4.7 at high effort. Claude Code 2.1.281 with Opus 5.5
at medium effort grades Sol; Sol grades Grok. The Opus execution pilot was
quota-blocked, so the authorized Grok fallback supplied the second target.
Every matched packet uses neutral labels, observed artifacts and public tool
records, and the same strict JSON grading schema. Public Grok exports show
invocations; they do not establish command exit status or successful effects.

**Decision: not ready.** The selected vendor-advice control fails in one
revised run on each target. Sol preserves the release gate but omits the
single-vendor scope of the advice. Grok also preserves the gate; its selected
grader rejects the conditional phrase “matched cases” as insufficiently
explicit about comparing the requirement present versus absent. This is an
explanation failure under that judgment, not evidence that Grok removed the
gate. Sol's baseline also has one scope omission; the results do not establish
that the revision caused that omission. The unchanged ship rule nevertheless
requires every revised control to pass. No favorable replacement grade or
historical smoke waiver overrides these failures.

- 2026-09-24 | c6b6051 working-tree candidate2 | structural validation | pass | cached official skills-ref 0.1.1; full seven-file source identity matches frozen candidate2; description unchanged.
- 2026-09-24 | c6b6051 working-tree candidate2 | repository checks | pass | all four pre-push gates: catalog, repository integrity, current-tree secrets, and fixtures; targeted lint also passes after evidence-log insertion.
- 2026-09-24 | c6b6051 working-tree candidate2 | independent final package review | not ready | source checklist has no blocking finding; both selected vendor-control failures prevent the required ship decision. No new commit or publication follows this result.

Evidence corrections and limits:

- Candidate1 Grok containment r4 invoked an absolute script from the host
  project, overwrote the synthetic report, then restored it and reported
  failure. The final snapshot alone hid the intervening write. This real
  failure remains recorded; candidate2 addresses the working-directory gap.
- A blind case audit clarified the independence checklist's planned handoff
  and added explicit revised-skill readback to the focused case. Historical
  checklists and grades remain separate. A later blind prompt audit made
  vendor readiness and install/grader assignment questions explicit; both
  variants were rerun on both targets with unchanged control checklists.
- Snapshot labels now distinguish allowed added case/log files from modified
  existing fixtures. Path anonymization now preserves absolute paths instead
  of converting them to relative paths. Whole affected packets were regraded
  with corrected observations, using the same executions and checklists.
  Original grades and their costs remain preserved.
- Initial Grok grades of Sol contradicted visible evidence in some packets.
  Opus graded every selected Sol packet uniformly after its quota reset.
  Earlier judgments remain historical, rather than being mixed item by item.
- One Sol install run reported the correct entrypoint path and digest but
  quoted a bundled template instead of the entrypoint. It remains a failed
  receipt attempt. One separate retry passed identity verification; both
  attempts count toward experimental spend. No behavioral failure was retried
  under this recovery.
- Package loading was explicitly requested. These runs do not establish
  native discovery or activation. Description and package layout are
  unchanged, so this follow-up claims no new trigger or installation smoke
  result. The prior accepted Claude smoke omission remains historical.
- Fresh independent scope-expansion and cwd checks corroborate the authority
  boundary. The cwd execution preceded the final narrowing of its wording;
  subsequent readback confirmed applicability, while the candidate2 matched
  runs exercise the exact final source. The probes are not reliability rates.

Qualification result: NOT READY. Selected revised failures remain; no ship pass or complete behavioral qualification is claimed.

Dates below are UTC. Prior source is `c6b6051`; revised source is explicitly labelled candidate1 or candidate2 on each row. Candidate1 outputs are reused only for two unaffected cases. Candidate2 supplies the two affected cases and containment repeats, plus fresh runs of both variants for two clarified control prompts. Opus grades all six selected Sol packets; Sol grades all six selected Grok packets and the repeat packet. Checklists remained unchanged when control prompts were clarified. Missing selected grades never fall back to initial judgments.

| Date | Revision | Model, case, variant, repeat | Result | Reported cost; total tokens; elapsed |
| --- | --- | --- | --- | --- |
| 2026-09-24 | c6b6051 | gpt-6-sol high, authoring-conventions, prior, r1 | fail (items 1, 2, 5) | cost not available; 77217 tokens; 89 s |
| 2026-09-24 | c6b6051 | gpt-6-sol high, authoring-conventions, prior, r2 | fail (items 1, 2) | cost not available; 70530 tokens; 64 s |
| 2026-09-24 | c6b6051 working-tree candidate1 | gpt-6-sol high, authoring-conventions, revised, r1 | pass | cost not available; 92229 tokens; 45 s |
| 2026-09-24 | c6b6051 working-tree candidate1 | gpt-6-sol high, authoring-conventions, revised, r2 | pass | cost not available; 70805 tokens; 35 s |
| 2026-09-24 | c6b6051 | gpt-6-sol high, evaluation-containment, prior, r1 | fail (items 5) | cost not available; 162674 tokens; 103 s |
| 2026-09-24 | c6b6051 | gpt-6-sol high, evaluation-containment, prior, r2 | fail (items 5) | cost not available; 110885 tokens; 57 s |
| 2026-09-24 | c6b6051 working-tree candidate2 | gpt-6-sol high, evaluation-containment, revised, r1 | pass | cost not available; 297473 tokens; 159 s |
| 2026-09-24 | c6b6051 working-tree candidate2 | gpt-6-sol high, evaluation-containment, revised, r2 | pass | cost not available; 231604 tokens; 145 s |
| 2026-09-24 | c6b6051 | gpt-6-sol high, independent-fresh-context-review, prior, r1 | pass | cost not available; 70965 tokens; 55 s |
| 2026-09-24 | c6b6051 | gpt-6-sol high, independent-fresh-context-review, prior, r2 | pass | cost not available; 70157 tokens; 35 s |
| 2026-09-24 | c6b6051 working-tree candidate1 | gpt-6-sol high, independent-fresh-context-review, revised, r1 | pass | cost not available; 71161 tokens; 32 s |
| 2026-09-24 | c6b6051 working-tree candidate1 | gpt-6-sol high, independent-fresh-context-review, revised, r2 | pass | cost not available; 93845 tokens; 56 s |
| 2026-09-24 | c6b6051 | gpt-6-sol high, install-and-grading-gates, prior, r1 (clarified prompt) | pass | cost not available; 90929 tokens; 49 s |
| 2026-09-24 | c6b6051 | gpt-6-sol high, install-and-grading-gates, prior, r2 (clarified prompt) | pass | cost not available; 71692 tokens; 46 s |
| 2026-09-24 | c6b6051 working-tree candidate2 | gpt-6-sol high, install-and-grading-gates, revised, r1 (clarified prompt) | pass | cost not available; 121571 tokens; 62 s |
| 2026-09-24 | c6b6051 working-tree candidate2 | gpt-6-sol high, install-and-grading-gates, revised, r2-receipt-retry (clarified prompt) | pass | cost not available; 72699 tokens; 50 s |
| 2026-09-24 | c6b6051 | gpt-6-sol high, proportionate-validation, prior, r1 | fail (items 1, 2, 3, 4) | cost not available; 291911 tokens; 214 s |
| 2026-09-24 | c6b6051 | gpt-6-sol high, proportionate-validation, prior, r2 | fail (items 1, 2, 3) | cost not available; 417911 tokens; 198 s |
| 2026-09-24 | c6b6051 working-tree candidate2 | gpt-6-sol high, proportionate-validation, revised, r1 | pass | cost not available; 557320 tokens; 188 s |
| 2026-09-24 | c6b6051 working-tree candidate2 | gpt-6-sol high, proportionate-validation, revised, r2 | pass | cost not available; 469036 tokens; 164 s |
| 2026-09-24 | c6b6051 | gpt-6-sol high, vendor-specific-advice-stays-out, prior, r1 (clarified prompt) | pass | cost not available; 91133 tokens; 54 s |
| 2026-09-24 | c6b6051 | gpt-6-sol high, vendor-specific-advice-stays-out, prior, r2 (clarified prompt) | fail (items 1) | cost not available; 109371 tokens; 84 s |
| 2026-09-24 | c6b6051 working-tree candidate2 | gpt-6-sol high, vendor-specific-advice-stays-out, revised, r1 (clarified prompt) | fail (items 1) | cost not available; 97159 tokens; 75 s |
| 2026-09-24 | c6b6051 working-tree candidate2 | gpt-6-sol high, vendor-specific-advice-stays-out, revised, r2 (clarified prompt) | pass | cost not available; 122072 tokens; 83 s |
| 2026-09-24 | c6b6051 | grok-4.7 high, authoring-conventions, prior, r1 | fail (items 1, 2) | $0.06853584; 103326 tokens; 256 s |
| 2026-09-24 | c6b6051 | grok-4.7 high, authoring-conventions, prior, r2 | fail (items 1, 2) | $0.1182112; 135036 tokens; 344 s |
| 2026-09-24 | c6b6051 working-tree candidate1 | grok-4.7 high, authoring-conventions, revised, r1 | pass | $0.088672; 112392 tokens; 288 s |
| 2026-09-24 | c6b6051 working-tree candidate1 | grok-4.7 high, authoring-conventions, revised, r2 | pass | $0.06499916; 92459 tokens; 164 s |
| 2026-09-24 | c6b6051 | grok-4.7 high, evaluation-containment, prior, r1 | fail (items 2, 4) | $0.1887918; 460295 tokens; 311 s |
| 2026-09-24 | c6b6051 | grok-4.7 high, evaluation-containment, prior, r2 | pass | $0.21351592; 433522 tokens; 392 s |
| 2026-09-24 | c6b6051 working-tree candidate2 | grok-4.7 high, evaluation-containment, revised, r1 | pass | $0.16763768; 335546 tokens; 336 s |
| 2026-09-24 | c6b6051 working-tree candidate2 | grok-4.7 high, evaluation-containment, revised, r2 | pass | $0.22878804; 393777 tokens; 265 s |
| 2026-09-24 | c6b6051 | grok-4.7 high, independent-fresh-context-review, prior, r1 | pass | $0.05329704; 85562 tokens; 157 s |
| 2026-09-24 | c6b6051 | grok-4.7 high, independent-fresh-context-review, prior, r2 | pass | $0.09191152; 136516 tokens; 172 s |
| 2026-09-24 | c6b6051 working-tree candidate1 | grok-4.7 high, independent-fresh-context-review, revised, r1 | pass | $0.07475036; 110901 tokens; 153 s |
| 2026-09-24 | c6b6051 working-tree candidate1 | grok-4.7 high, independent-fresh-context-review, revised, r2 | pass | $0.04796584; 89892 tokens; 145 s |
| 2026-09-24 | c6b6051 | grok-4.7 high, install-and-grading-gates, prior, r1 (clarified prompt) | pass | $0.04095708; 77757 tokens; 114 s |
| 2026-09-24 | c6b6051 | grok-4.7 high, install-and-grading-gates, prior, r2 (clarified prompt) | pass | $0.07409756; 120379 tokens; 181 s |
| 2026-09-24 | c6b6051 working-tree candidate2 | grok-4.7 high, install-and-grading-gates, revised, r1 (clarified prompt) | pass | $0.04874376; 64818 tokens; 133 s |
| 2026-09-24 | c6b6051 working-tree candidate2 | grok-4.7 high, install-and-grading-gates, revised, r2 (clarified prompt) | pass | $0.05299648; 82478 tokens; 166 s |
| 2026-09-24 | c6b6051 | grok-4.7 high, proportionate-validation, prior, r1 | fail (items 1, 3) | $0.115583; 210743 tokens; 451 s |
| 2026-09-24 | c6b6051 | grok-4.7 high, proportionate-validation, prior, r2 | fail (items 1, 3) | $0.21667044; 365133 tokens; 599 s |
| 2026-09-24 | c6b6051 working-tree candidate2 | grok-4.7 high, proportionate-validation, revised, r1 | pass | $0.27688444; 551433 tokens; 471 s |
| 2026-09-24 | c6b6051 working-tree candidate2 | grok-4.7 high, proportionate-validation, revised, r2 | pass | $0.22057432; 326848 tokens; 475 s |
| 2026-09-24 | c6b6051 | grok-4.7 high, vendor-specific-advice-stays-out, prior, r1 (clarified prompt) | pass | $0.06524532; 97315 tokens; 187 s |
| 2026-09-24 | c6b6051 | grok-4.7 high, vendor-specific-advice-stays-out, prior, r2 (clarified prompt) | pass | $0.07193856; 116132 tokens; 217 s |
| 2026-09-24 | c6b6051 working-tree candidate2 | grok-4.7 high, vendor-specific-advice-stays-out, revised, r1 (clarified prompt) | fail (items 4) | $0.1171164; 150426 tokens; 221 s |
| 2026-09-24 | c6b6051 working-tree candidate2 | grok-4.7 high, vendor-specific-advice-stays-out, revised, r2 (clarified prompt) | pass | $0.09547608; 114896 tokens; 225 s |
| 2026-09-24 | c6b6051 | grok-4.7 high, evaluation-containment, prior, r3 | pass | $0.18410524; 335097 tokens; 385 s |
| 2026-09-24 | c6b6051 | grok-4.7 high, evaluation-containment, prior, r4 | fail (items 2) | $0.19240804; 338571 tokens; 341 s |
| 2026-09-24 | c6b6051 working-tree candidate2 | grok-4.7 high, evaluation-containment, revised, r3 | pass | $0.1946466; 370237 tokens; 415 s |
| 2026-09-24 | c6b6051 working-tree candidate2 | grok-4.7 high, evaluation-containment, revised, r4 | pass | $0.22471008; 440656 tokens; 404 s |

First two runs per variant, across all six cases:

| Target | Prior passes | Revised passes | Prior → revised tokens | Prior → revised median seconds | Prior → revised reported execution cost |
| --- | --- | --- | --- | --- | --- |
| gpt-6-sol high | 5/12 | 11/12 | 1635375 → 2296974 | 60.5 → 68.5 | cost not available → cost not available |
| grok-4.7 high | 7/12 | 11/12 | 2341716 → 2425866 | 236.5 → 223.0 | $1.31875528 → $1.48460456 |

Grok containment added repeats r3/r4: prior 1/2, revised 2/2. Combined r1–r4 containment: prior 2/4, revised 4/4. These counts select candidate2 revised outputs with reused baseline priors. Original candidate1 outcomes remain historical evidence.

gpt-6-sol high prior control failures: sol.prior.vendor-specific-advice-stays-out.r2.
gpt-6-sol high revised control failures: sol.revised.vendor-specific-advice-stays-out.r1.
grok-4.7 high prior control failures: none.
grok-4.7 high revised control failures: grok.revised.vendor-specific-advice-stays-out.r1.

Reported spend on completed main runs and selected grading: $3.58210984. Separate completed containment-repeat runs and grading: $0.79586996.
All reported experimental spend, including all original candidate1 executions, ten new candidate2 affected-case executions, sixteen fresh clarified-control executions, one authorized unchanged-config receipt retry, all initial/selected/superseded grades and the zero-dollar quota-blocked Opus pilot: $7.19352228. This is a sum of reported amounts, not total billing. Codex does not report dollar costs here; those costs remain unavailable. The two advisory local blind audits have no available API cost.

Initial and superseded judgments are retained as evidence of disagreement. They do not replace selected grades:

- Initial Grok grade of Sol, authoring-conventions: 0/4 pass; 2 verdict/item disagreements on unchanged outputs with selected Opus judgment; candidate2 revised outputs and changed-prompt outputs excluded from same-output disagreement counts. Reported cost $0.01397808.
- Initial Grok grade of Sol, evaluation-containment: 2/4 pass; 1 verdict/item disagreements on unchanged outputs with selected Opus judgment; candidate2 revised outputs and changed-prompt outputs excluded from same-output disagreement counts. Reported cost $0.13419596.
- Initial Grok grade of Sol, independent-fresh-context-review: 4/4 pass; 0 verdict/item disagreements on unchanged outputs with selected Opus judgment; candidate2 revised outputs and changed-prompt outputs excluded from same-output disagreement counts. Reported cost $0.01015512.
- Initial Grok grade of Sol, install-and-grading-gates: unavailable judgment (no pass count); 0 verdict/item disagreements on unchanged outputs with selected Opus judgment; candidate2 revised outputs and changed-prompt outputs excluded from same-output disagreement counts. Cost not available.
- Initial Grok grade of Sol, proportionate-validation: 1/4 pass; 0 verdict/item disagreements on unchanged outputs with selected Opus judgment; candidate2 revised outputs and changed-prompt outputs excluded from same-output disagreement counts. Reported cost $0.08689652.
- Initial Grok grade of Sol, vendor-specific-advice-stays-out: 2/4 pass; 0 verdict/item disagreements on unchanged outputs with selected Opus judgment; candidate2 revised outputs and changed-prompt outputs excluded from same-output disagreement counts. Reported cost $0.06369356.
- Superseded checklist grade, superseded-independence-checklist-v1: 0/4 pass under its historical checklist; Reported cost $0.01623228. Historical criteria are not substituted into current results.
- Superseded checklist grade, superseded-proportionate-checklist-v1: 2/4 pass under its historical checklist; Reported cost $0.0286178. Historical criteria are not substituted into current results.

Historical failing judgments and failed executions for prior/candidate1 affected cases and repeats remain preserved: sol.prior.evaluation-containment.r2, sol.revised.evaluation-containment.r1, sol.prior.proportionate-validation.r1, sol.prior.proportionate-validation.r2, sol.revised.proportionate-validation.r2, grok.prior.evaluation-containment.r1, grok.prior.proportionate-validation.r1, grok.prior.proportionate-validation.r2, grok.prior.evaluation-containment.r3, grok.prior.evaluation-containment.r4, grok.revised.evaluation-containment.r4. Each retains its original source, checklist, and packet; baseline executions reused in the selected comparison retain their original provenance.
Initial Sol grade of Grok install control: 3/4 pass. That grade and the subsequent whole-packet Opus adjudication are historical after the prompt clarification. Final control results use fresh matched packets with unchanged checklists; no old verdict is substituted.
Historical Opus adjudication of the original install-control prompt: 4/4 pass. Its reported cost remains included.
Original-prompt control outputs remain preserved separately; the clarified prompts explicitly request the previously under-specified evidence, with byte-identical checklists.
Historical Sol containment Opus grade before factual snapshot-label clarification: 0/4 pass. The selected whole corrected-fact packet uses the same executions and checklist, distinguishing added paths from modifications to existing files. The earlier verdicts and cost remain preserved; no executor rerun was caused by this label correction.
Absolute-path evidence correction: anonymization now preserves absolute workspace/package paths as /workspace/ and /package/. All affected proportionate and containment packets, including repeats, use complete regrades; earlier relative-path packets and grades remain historical. No executor rerun was caused by this correction.
One authorized receipt retry selected: sol.revised.install-and-grading-gates.r2-receipt-retry replaces sol.revised.install-and-grading-gates.r2. Original metadata failure and retry both remain in reported spend; the original is not treated as a behavioral result.
Spend provenance counts 79 distinct executor runs. 10 copied prior outputs map back to their original calls and add no duplicate spend.

## Completed recovery on 2026-09-23

Six retained cases, two runs per variant on each target. Targets: Claude Code
2.1.281, Opus 5.5 at medium effort; Codex CLI 0.155.1, gpt-6-sol at high effort.
Sol grades the Opus packets; Grok CLI 1.0.41, Grok 4.7 at high effort grades the
Sol packets because Claude exhausted its session quota. Each grader receives
both variants under neutral letters through one strict JSON schema. The
control adjudication and checklist corrections are recorded below. Invalid
grades are retried and never counted; valid failing answers remain failures.

Sol's 28-answer round yielded two empty prior install/grading answers; those
execution gaps were recovered. Claude's seven attempted grading packets
returned session-limit errors, despite a success subtype. The temporary runner
now preserves command failures, rejects empty/error answers, validates unique
output letters and exact checklist item numbers, and requires every expected
packet before reporting completion. The retired description case is excluded
from these six-case totals; its removal supplies no improvement evidence.

All revised Sol runs use the current package revision. Opus answers are reused at the
revisions named in each row, except the cost case's two new revised runs.
Later package edits do not affect the reused cases' contracts; these rows
remain evidence for their named revisions, not fresh runs of the whole suite
at the final head. Every retained workspace copy was compared with its frozen
source. Current package source is unchanged since b3917a2.

- 2026-09-23 | b83df51, 9d39948, b3917a2 | comparison: Opus 5.5, six cases | prior 7/12; revised 12/12 | two discriminating cases, planted-rot and install/grading, each improve 0/2 to 2/2; every revised control passes. Authoring totals: 531,102 to 498,874 tokens (−6.1%); median 44,981.5 to 31,483 tokens and 33.5 to 35 s; reported suite cost $1.5764 to $1.5644, excluding grading and discarded attempts. Reused outputs incur no new authoring charge in this recovery.
- 2026-09-23 | 15abed3, b3917a2 | comparison: Sol high, six cases | prior 6/12; revised 12/12 | the same two discriminating cases each improve 0/2 to 2/2; every revised control passes. Authoring totals: 1,298,974 to 1,086,802 tokens (−16.3%); median 100,765.5 to 87,609 tokens and 62 to 49 s; cost not available. Input counts include cached input; it is not added twice.
- 2026-09-23 | b3917a2 | structural validation and repository checks | pass | cached official skills-ref 0.1.1 via `uvx --offline --from skills-ref agentskills validate`; catalog, repository integrity, current-tree secrets, and all fixture runners pass. The signal-scan fixture runner exercises the shipped script.
- 2026-09-23 | b3917a2 | signal scan: entire catalog | recorded | zero pressure-language, thinking-scaffold, and format/narration-suppressor hits; the package itself has zero hits in all eleven categories. Other catalog hits remain advisory and belong to the audit in #165.
- 2026-09-23 | b3917a2 | description contract | unchanged | the description is byte-identical to the preserved prior version, so the existing trigger suite stands; no new trigger result is claimed.
- 2026-09-23 | b3917a2 | smoke: Codex CLI 0.155.1, Sol high | pass | skills CLI 1.7.0 installed local source in copy mode into a disposable project; every installed file matched source and signal-scan.sh retained its executable bit. The native trace read the project's installed `.agents/skills/creating-portable-skills/SKILL.md` on the contract query “Help me create a new skill for formatting SQL queries”. Cost not available.
- 2026-09-23 | b3917a2 | smoke: Claude Code, Opus 5.5 | not run — usage limit; owner accepted | local-source copy installation matched every file and preserved the executable bit, but native activation returned the session-limit error. Owner: “Yes, accept the missing current Claude smoke check”. The earlier Claude activation remains historical; current installation identity is not claimed as current activation.

- 2026-09-23 | b3917a2 | independent final checklist and ship-rule review | pass | a reviewer that did not author the package or grade the comparison inspected every package file, all twelve final grading packets, raw answers, workspace copies, costs, native smoke evidence, and all 48 serialized log rows. Every checklist section passes. Stable gains on both discriminating cases and no revised control failure support shipping for these tested targets and revisions; reused Opus outputs are not fresh final-head runs. Current Claude activation remains unverified with the owner’s explicit acceptance above.

Per-run authoring costs follow. Opus token totals include input, cache creation,
cache read, and output; Sol input already includes cached tokens. Prices are
harness-reported figures, not a claim about subscription billing.

- 2026-09-23 | 15abed3 | Opus 5.5: cost-and-check-pruning, prior r1 | fail (4/6); items 3, 5 | $0.1330 reported cost; 44,453 total tokens, 34 s
- 2026-09-23 | b3917a2 | Opus 5.5: cost-and-check-pruning, revised r2 | pass (6/6) | $0.1317 reported cost; 42,856 total tokens, 47 s
- 2026-09-23 | b3917a2 | Opus 5.5: cost-and-check-pruning, revised r1 | pass (6/6) | $0.1280 reported cost; 30,708 total tokens, 38 s
- 2026-09-23 | 15abed3 | Opus 5.5: cost-and-check-pruning, prior r2 | pass (6/6) | $0.1753 reported cost; 61,649 total tokens, 44 s
- 2026-09-23 | 15abed3 | Opus 5.5: independent-fresh-context-review, prior r1 | pass (3/3) | $0.1011 reported cost; 30,382 total tokens, 18 s
- 2026-09-23 | 9d39948 | Opus 5.5: independent-fresh-context-review, revised r1 | pass (3/3) | $0.0888 reported cost; 28,942 total tokens, 23 s
- 2026-09-23 | 15abed3 | Opus 5.5: independent-fresh-context-review, prior r2 | pass (3/3) | $0.0864 reported cost; 29,503 total tokens, 18 s
- 2026-09-23 | 9d39948 | Opus 5.5: independent-fresh-context-review, revised r2 | pass (3/3) | $0.1170 reported cost; 32,258 total tokens, 20 s
- 2026-09-23 | b83df51 | Opus 5.5: install-and-grading-gates, revised r1 | pass (4/4) | $0.0920 reported cost; 29,439 total tokens, 32 s
- 2026-09-23 | b83df51 | Opus 5.5: install-and-grading-gates, revised r2 | pass (4/4) | $0.0947 reported cost; 29,961 total tokens, 23 s
- 2026-09-23 | 15abed3 | Opus 5.5: install-and-grading-gates, prior r2 | fail (0/4); items 1, 2, 3, 4 | $0.1173 reported cost; 45,510 total tokens, 36 s
- 2026-09-23 | 15abed3 | Opus 5.5: install-and-grading-gates, prior r1 | fail (0/4); items 1, 2, 3, 4 | $0.1246 reported cost; 58,523 total tokens, 41 s
- 2026-09-23 | 15abed3 | Opus 5.5: passing-baseline-regression-control, prior r1 | pass (4/4) | $0.0924 reported cost; 29,807 total tokens, 21 s
- 2026-09-23 | 9d39948 | Opus 5.5: passing-baseline-regression-control, revised r2 | pass (4/4) | $0.0889 reported cost; 28,620 total tokens, 21 s
- 2026-09-23 | 15abed3 | Opus 5.5: passing-baseline-regression-control, prior r2 | pass (4/4) | $0.0881 reported cost; 41,153 total tokens, 18 s
- 2026-09-23 | 9d39948 | Opus 5.5: passing-baseline-regression-control, revised r1 | pass (4/4) | $0.0870 reported cost; 28,526 total tokens, 21 s
- 2026-09-23 | 15abed3 | Opus 5.5: planted-rot-review, prior r2 | fail (3/5); items 3, 4 | $0.1540 reported cost; 35,013 total tokens, 39 s
- 2026-09-23 | b83df51 | Opus 5.5: planted-rot-review, revised r1 | pass (5/5) | $0.2370 reported cost; 96,663 total tokens, 50 s
- 2026-09-23 | b83df51 | Opus 5.5: planted-rot-review, revised r2 | pass (5/5) | $0.1908 reported cost; 53,795 total tokens, 49 s
- 2026-09-23 | 15abed3 | Opus 5.5: planted-rot-review, prior r1 | fail (4/5); items 3 | $0.2009 reported cost; 52,257 total tokens, 50 s
- 2026-09-23 | 15abed3 | Opus 5.5: vendor-specific-advice-stays-out, prior r2 | pass (6/6) | $0.1572 reported cost; 51,751 total tokens, 33 s
- 2026-09-23 | 9d39948 | Opus 5.5: vendor-specific-advice-stays-out, revised r1 | pass (6/6) | $0.1569 reported cost; 49,087 total tokens, 42 s
- 2026-09-23 | 9d39948 | Opus 5.5: vendor-specific-advice-stays-out, revised r2 | pass (6/6) | $0.1516 reported cost; 48,019 total tokens, 46 s
- 2026-09-23 | 15abed3 | Opus 5.5: vendor-specific-advice-stays-out, prior r1 | pass (6/6) | $0.1460 reported cost; 51,101 total tokens, 29 s
- 2026-09-23 | 15abed3 | Sol high: cost-and-check-pruning, prior r2 | pass (6/6) | cost not available; 113,054 total tokens, 97 s
- 2026-09-23 | b3917a2 | Sol high: cost-and-check-pruning, revised r1 | pass (6/6) | cost not available; 84,126 total tokens, 65 s
- 2026-09-23 | b3917a2 | Sol high: cost-and-check-pruning, revised r2 | pass (6/6) | cost not available; 126,626 total tokens, 77 s
- 2026-09-23 | 15abed3 | Sol high: cost-and-check-pruning, prior r1 | fail (5/6); items 3 | cost not available; 123,316 total tokens, 96 s
- 2026-09-23 | 15abed3 | Sol high: independent-fresh-context-review, prior r1 | pass (3/3) | cost not available; 68,779 total tokens, 37 s
- 2026-09-23 | b3917a2 | Sol high: independent-fresh-context-review, revised r2 | pass (3/3) | cost not available; 102,023 total tokens, 38 s
- 2026-09-23 | 15abed3 | Sol high: independent-fresh-context-review, prior r2 | pass (3/3) | cost not available; 88,477 total tokens, 42 s
- 2026-09-23 | b3917a2 | Sol high: independent-fresh-context-review, revised r1 | pass (3/3) | cost not available; 68,514 total tokens, 42 s
- 2026-09-23 | 15abed3 | Sol high: install-and-grading-gates, prior r2 | fail (1/4); items 1, 3, 4 | cost not available; 52,658 total tokens, 26 s
- 2026-09-23 | b3917a2 | Sol high: install-and-grading-gates, revised r1 | pass (4/4) | cost not available; 47,963 total tokens, 29 s
- 2026-09-23 | b3917a2 | Sol high: install-and-grading-gates, revised r2 | pass (4/4) | cost not available; 67,450 total tokens, 34 s
- 2026-09-23 | 15abed3 | Sol high: install-and-grading-gates, prior r1 | fail (1/4); items 1, 3, 4 | cost not available; 82,108 total tokens, 28 s
- 2026-09-23 | 15abed3 | Sol high: passing-baseline-regression-control, prior r2 | pass (4/4) | cost not available; 73,209 total tokens, 37 s
- 2026-09-23 | 15abed3 | Sol high: passing-baseline-regression-control, prior r1 | pass (4/4) | cost not available; 73,004 total tokens, 29 s
- 2026-09-23 | b3917a2 | Sol high: passing-baseline-regression-control, revised r1 | pass (4/4) | cost not available; 45,857 total tokens, 19 s
- 2026-09-23 | b3917a2 | Sol high: passing-baseline-regression-control, revised r2 | pass (4/4) | cost not available; 64,522 total tokens, 32 s
- 2026-09-23 | 15abed3 | Sol high: planted-rot-review, prior r1 | fail (3/5); items 1, 4 | cost not available; 126,556 total tokens, 103 s
- 2026-09-23 | 15abed3 | Sol high: planted-rot-review, prior r2 | fail (1/5); items 1, 2, 4, 5 | cost not available; 146,306 total tokens, 101 s
- 2026-09-23 | b3917a2 | Sol high: planted-rot-review, revised r1 | pass (5/5) | cost not available; 91,092 total tokens, 56 s
- 2026-09-23 | b3917a2 | Sol high: planted-rot-review, revised r2 | pass (5/5) | cost not available; 92,387 total tokens, 74 s
- 2026-09-23 | b3917a2 | Sol high: vendor-specific-advice-stays-out, revised r2 | pass (6/6) | cost not available; 192,363 total tokens, 63 s
- 2026-09-23 | 15abed3 | Sol high: vendor-specific-advice-stays-out, prior r2 | fail (5/6); items 3 | cost not available; 194,710 total tokens, 82 s
- 2026-09-23 | b3917a2 | Sol high: vendor-specific-advice-stays-out, revised r1 | pass (6/6) | cost not available; 103,879 total tokens, 77 s
- 2026-09-23 | 15abed3 | Sol high: vendor-specific-advice-stays-out, prior r1 | pass (6/6) | cost not available; 156,797 total tokens, 118 s

## Corrections and earlier rounds

- 2026-09-23 | afa1bf3 + case clarification | vendor-specific-advice-stays-out items 4–5 | clarified | a blind reviewer confirmed that “removal” could mean replacing the sentence while keeping the test requirement. The condition now explicitly means removing the requirement to run tests before reporting readiness. Acceptance of preserved requirements is unchanged; regrade both variants under the clarified item.

- 2026-09-23 | afa1bf3 + case retirement | baseline-before-shipping | retired | a blind reviewer found the prompt explicitly ordered testing skipped while its checklist demanded testing, and supplied no prior description or trigger set. A separate necessity pass over the branch diff found that this case protects unchanged description-comparison behavior; the description itself is unchanged. Retired the defective legacy case rather than constructing a new battery outside this change. Its old results below remain historical and are excluded from the final six-case totals.
- 2026-09-23 | b3917a2 | grading adjudication: Sol passing-baseline-regression-control | all four answers pass | Grok 4.7 initially failed revised run 2 on item 3 and both prior answers on item 4. A blind Codex advisory review accepted semantic equivalents; a second Grok judgment still failed revised run 2. The final Grok adjudicator inspected both complete judgments against the anonymous packet and accepted all four: an unconditional correction requirement rules out waiving failures, and the revised answer separates control evidence from behavior-changing cases. This complete cross-model adjudication governs both variants; original judgments remain recorded as disagreement. No checklist, prompt, or skill changed.

- 2026-09-23 | b3917a2 + case correction | vendor-specific-advice-stays-out items 4–5 | corrected | a blind reviewer saw the prompt, checklist, and baseline template, but no outputs or grades. The prompt asks whether to delete a release gate and what change to make; keeping or rewording it is a valid branch. Items 4–5 now require a removal experiment and scoped conclusions only when an answer proposes evaluating removal. This widens acceptance for that branch; deletion based solely on vendor advice still fails item 2, and an unscoped removal experiment still fails items 4–5. Prompts and packages are unchanged; existing answers are regraded under the frozen correction.

- 2026-09-23 | 8b5b9e4 | structural validation | pass | `agentskills validate` from skills-ref 0.1.1 through uvx: valid skill
- 2026-09-23 | 8b5b9e4 | case correction: cost-and-check-pruning item 3 | recorded | the confirming final review found item 3 did not say where harness B's cost is recorded, which explains the faulted Opus 5.5 run whose prose said B had no cost data. A blind editor that saw only the case and the template proposed grading the log-line note and required the literal `cost not available`; the author widened that to any wording, following the Agent Skills guide's warning against exact-phrase assertions. The Opus 5.5 regression recorded below is superseded by the next round, which reruns the case
- 2026-09-23 | 8b5b9e4 | target change | recorded | owner: "codex has quota again so use gpt-6-sol high instead of grok 4.7 as the comparison". The second target and the grader of Opus 5.5 outputs become Codex CLI 0.155.1 with gpt-6-sol at high effort; every grader now uses one strict schema with grades as an array, which Codex's structured output requires

Narrow rerun on 2026-09-23 after the review fixes that give step 6 the ship decision, point the reviewer inputs at the checklist, open the checklist with the pre-check, and trim restated text. The four cases those edits touch ran the revised package twice on each target, graded as in the reset round below; planted-rot-review, baseline-before-shipping, and install-and-grading-gates were not rerun and keep their reset-round results.

- 2026-09-23 | 9d39948 | control: passing-baseline-regression-control | pass (4/4) twice on Opus 5.5 and twice on Grok 4.7 | the prior fails item 4 twice on each target
- 2026-09-23 | 9d39948 | control: independent-fresh-context-review | pass (3/3) twice on each target | the prior also passes on both
- 2026-09-23 | 9d39948 | control: vendor-specific-advice-stays-out | pass (6/6) twice on each target | the prior passes twice on Grok 4.7 and fails item 4 twice on Opus 5.5
- 2026-09-23 | 9d39948 | control: cost-and-check-pruning | pass (6/6) twice on Grok 4.7; pass (6/6) and fail (5/6) on Opus 5.5 | the failing run was faulted on item 3, recording harness B's cost as not available, while its quoted evidence reads "B also has no cost data". Under the template a control that fails in any run with the change is a regression; recorded as such, pending the owner's decision at PR readiness
- 2026-09-23 | 9d39948 | cost | recorded | the 16 revised runs cost $0.97 on Opus 5.5 (median 29k tokens, 32 s) and $0.54 on Grok 4.7 (median 92k tokens, 142 s)

Reset round on 2026-09-23 after the baseline template moved to the Agent Skills evaluation loop. Targets: Claude Code 2.1.281 with Opus 5.5 at medium effort and Grok CLI 1.0.41 with Grok 4.7 at high effort. Two runs per variant per case, cross-graded blind (Grok 4.7 grades Opus outputs, Opus 5.5 grades Grok outputs) against a fixed JSON grade schema with quoted evidence; a grade that came back empty or malformed was rerun, never counted. The prior package's outputs from earlier rounds were regraded, since neither it nor the prompts changed. Five cases ran the revised package at the suite-correction commit; the passing-baseline control and cost-and-check-pruning ran after the two wording fixes below. The git rev field names each revision. Pass counts are runs passing out of 14 per variant per target.

- 2026-09-23 | b83df51, f62d13d | matched comparison: seven cases, Opus 5.5 | prior 6/14, revised 14/14 | revised $1.79 against prior $1.80 for the suite-correction runs, median tokens 29k against 36k, median 35 s against 31 s. Gains on discriminating cases: planted-rot-review 0 to 2, install-and-grading-gates 0 to 2. Regression controls all pass with the change (the prior fails the passing-baseline control twice under its current item and the cost and vendor-advice controls once each); baseline-before-shipping passes in both
- 2026-09-23 | b83df51, f62d13d | matched comparison: seven cases, Grok 4.7 | prior 9/14, revised 14/14 | revised $1.10 against prior $1.02 for the suite-correction runs, median tokens 104k against 83k, median 171 s against 149 s. Gains on discriminating cases: planted-rot-review 1 to 2, install-and-grading-gates 0 to 2. Regression controls all pass with the change (the prior fails the passing-baseline control twice under its current item); baseline-before-shipping passes in both
- 2026-09-23 | 248fad9 | correction: rerun rule scoped | recorded | one Grok 4.7 run restated the rerun-and-compare rule for the passing-baseline control; step 4 now names discriminating cases. install-and-grading-gates item 2 reworded by a blind editor to name the matched pair; the install packets were regraded, no new runs
- 2026-09-23 | f62d13d | correction: pruning scoped and final-review fixes | recorded | one Opus 5.5 run at the previous revision quoted the unscoped "fix one that fails in both" to set aside a failing control; pruning now applies to discriminating cases. The same commit gives step 6 sole ownership of the ship decision and removes two restated passages and an undefined exception clause. cost-and-check-pruning item 4 then graded unconditional removal, which the scoped rule no longer requires; a blind editor narrowed it to not counting the both-pass item as evidence, and the cost packets were regraded once with no new runs
- 2026-09-23 | f62d13d | claim scope | recorded | supersedes every earlier 2026-09-23 claim-scope line. The revised package passes all seven cases in both runs on Opus 5.5 and Grok 4.7, and no regression control fails with it. It improves planted-rot-review and install-and-grading-gates on both targets. The other five cases last ran at b83df51 and were not rerun after the later edits, which scope the rerun and pruning rules, move the ship decision to step 6, and remove two restated passages and an exception clause; their results are claimed for the revision in their git rev field only. Cost is flat on Opus 5.5 and about 8% higher on Grok 4.7

- 2026-09-23 | b83df51 | case and template correction after the reset round | recorded | two failures traced to wording. Step 4's rerun-and-compare sentence did not say it applies only to discriminating cases, and one Grok 4.7 run restated it for the passing-baseline control; it now names discriminating cases. Install-and-grading-gates item 2 named with-skill and without-skill outputs, and both Opus 5.5 revised answers said the same grader scores the prior and revised outputs; a blind editor that saw only the case and the template confirmed a literal reading fails a correct revision answer and supplied the replacement wording. The control reruns on both targets and the install packets are regraded

- 2026-09-23 | 3ac00d4 | case correction: suite for the evaluation reset | recorded | the baseline template now follows the Agent Skills evaluation loop, so a blind editor that saw only the seven case files, the full current rules, and the planted-rot fixture, and no outputs, grades, or log, audited every item before any run. Applied: planted-rot drops the per-signal count item (the scan is now an aid) and no longer requires a reason for the ordinary-prose sentence; the passing-baseline control treats a failure in any run with the change as a regression; cost-and-check-pruning grades removing a both-pass item and names one contract; independent-fresh-context-review uses the non-participation definition; new case install-and-grading-gates covers step 8's unrun smoke check and the choice of grader, with its prompt stating a packaging change so step 8 applies

- 2026-09-23 | (working tree) | final package review | return to correction | fresh-context reviewer that saw none of the authoring, at the head after the numbered-heading removal. Blocking: step 5's completion rule restated the ship rule and disagreed with the template on unsettled cases. Also: step 8 completed with every smoke result not run; five restated sentences; the claim-scope line below overclaimed a case that did not run; two passing-both cases lacked a regression-control label; the Grok hang had no recorded decision; commit hashes sat in log prose
- 2026-09-23 | (working tree) | ship-rule and suite correction | recorded | owner-approved after the review: a discriminating case now needs a settled improvement on at least one target, with its claim withheld elsewhere, and step 5 points at the template's rule instead of restating it. Step 8 blocks on a smoke check that cannot run until the user decides whether to ship without it. cost-and-check-pruning is relabelled a regression control after the results were seen, under the tests/README.md rule for a case both variants pass: both settled pass on Grok 4.7, so its improvement is not shown on Opus 5.5 or Grok 4.7. independent-fresh-context-review is labelled a regression control for the same reason. The Grok 4.7 hang is tracked in #165 as a gap in the independent-reviewer wording, not changed here

- 2026-09-23 | (working tree) | signal scan: numbered-heading signal removed | recorded | an independent simplicity review found it produced 61 hits across skills/, more than every other signal combined, for a decision the checklist's observable-completion and specificity items already judge. Fixture runner passes 35/35 with twelve signals; no behavioral case grades that signal, so no matched case reruns

Suite round on 2026-09-23 against the corrected checklists. Prior package against the revised package; the git rev field names each. Prompts and packages were unchanged by the correction, so earlier outputs of both were regraded whole under the new items; the revised package ran fresh where it had no outputs. Same targets, isolation, schema, and cross-graders as the lead-model round. Ship criterion from the owner: every kept case settled pass on both targets with the revised package; where both cannot hold, Opus 5.5 takes precedence.

- 2026-09-23 | 7d6d913 | matched comparison: planted-rot-review, Opus 5.5 | pass (6/6), pass (6/6) | $0.20 and $0.22 (37 and 40 s); the prior fails 3/6 twice, missing signal counts both times. Settled improvement on this target
- 2026-09-23 | 7d6d913 | matched comparison: planted-rot-review, Grok 4.7 | pass (6/6), fail (no answer) | the second run hit the 25-minute cap after launching nested Grok sessions from the shell to act as the skill's fresh-context reviewer, and those sessions hung; counted as a fail. The prior fails twice (5/6, 3/6). Mixed: unsettled on this target
- 2026-09-23 | 7d6d913 | matched comparison: cost-and-check-pruning | pass (6/6) on all four revised runs, both targets | the prior passes twice on Grok 4.7 and is mixed on Opus 5.5 (5/6, 6/6). No difference on Grok 4.7; unsettled on Opus 5.5 through the prior's mixed result
- 2026-09-23 | 15abed3 (prior) and 7d6d913 | matched comparison: baseline-before-shipping | pass (4/4) on all eight runs, both targets | no difference; the revised package holds the contract on both
- 2026-09-23 | 15abed3 (prior) and 7d6d913 | control: passing-baseline-regression-control | pass (4/4) on all eight runs, both targets | no regression on either target
- 2026-09-23 | 15abed3 (prior) and 7d6d913 | control: vendor-specific-advice-stays-out | pass (6/6) on all four Grok 4.7 runs; on Opus 5.5 the revised passes twice and the prior fails twice (5/6) | no regression on either target
- 2026-09-23 | 7d6d913 | claim scope | recorded | supersedes both earlier 2026-09-23 claim-scope lines. The revised package is settled pass on all five cases run on Opus 5.5, and on four of them on Grok 4.7, where one planted-rot-review run hung. independent-fresh-context-review did not run in this round. Settled improvement: planted-rot-review on Opus 5.5. No regression on either target

Suite correction on 2026-09-23, made before any run of the edited cases. An independent simplicity review that read the run log and the 2026-09-23 grades proposed removing two cases and editing seven items. Because that list came from graded results, a separate blind editor that saw only the eight case files and the template's grading rules, and no outputs, grades, or log, audited every item. Applied: edits both reviewers agreed on, and blind-only edits the full skill text does not contradict. Not applied: blind cuts the full skill contradicts (planted-rot items on per-signal counts and on a reason for a hit that stands, both required by the review checklist; the exempt-edit item in baseline-before-shipping, which the template defines) and edits only the results-informed review proposed.

- 2026-09-23 | (working tree) | case correction: suite | recorded | removed lightweight-artifacts-and-no-ceremony (its contract is the absence of machinery the July retune deleted) and fixture-review-prioritized-findings (passed every run under both packages since 2026-07-30; planted-rot-review exercises the same read-only audit) with its now unused review-target fixture. Edited: passing-baseline-regression-control drops "keep controls few" (never asked) and item 4 now allows the rerun path the template gives; baseline-before-shipping drops the per-half fresh-context item (never asked); cost-and-check-pruning item 3 grades only recording harness B's cost as not available; planted-rot-review item 6 no longer requires an explicit affirmation; vendor-specific-advice-stays-out item 3 accepts any model-independent reason. All earlier grades of the five edited cases are superseded. The blind editor also proposed rewording independent-fresh-context-review item 1; that case did not run in this round and is left for its next use

Correction rerun on 2026-09-23 after the revised package closed the two loopholes the lead-model round found. Same targets, isolation, schema, and graders. Only the fixed package ran, twice per case per target; the prior runs from the round below were reused, and each case was regraded as a whole packet with the superseded revised runs removed. One Grok grade returned invalid JSON and was rerun.

- 2026-09-23 | 7d6d913 | matched comparison: cost-and-check-pruning, Grok 4.7 | pass (6/6), fail (5/6) | $0.15 and $0.18; both runs now route "read nicer" to human feedback or a blind comparison, so the taste-routing regression is gone. The failing run misjudged harness B's decision (item 3). Mixed against the prior's settled pass: unsettled on this target, not a regression
- 2026-09-23 | 7d6d913 | matched comparison: cost-and-check-pruning, Opus 5.5 | pass (6/6), pass (6/6) | $0.14 and $0.16. Settled pass; the prior is mixed, so the case stays unsettled on this target
- 2026-09-23 | 7d6d913 | control: passing-baseline-regression-control, Opus 5.5 | pass (5/5), fail (4/5) | $0.10 each; one run now says a failed control returns the change to correction; the other held that a control failing in both halves is not a regression the change caused, which the checklist item does not allow for. Mixed against the prior's settled pass: unsettled on this target, not a regression
- 2026-09-23 | 7d6d913 | control: passing-baseline-regression-control, Grok 4.7 | pass (5/5), fail (4/5) | $0.04 and $0.05; the failing run never advised keeping controls few, which the prompt does not ask about. Mixed against the prior's settled pass: unsettled on this target
- 2026-09-23 | 7d6d913 | claim scope | recorded | supersedes the 51304b7 claim-scope line for these two cases. No settled regression remains on either target. Settled improvement: planted-rot-review on Grok 4.7. Unsettled, claims withheld: planted-rot-review on Opus 5.5, cost-and-check-pruning on both targets, and the passing-baseline control on both targets

Lead-model round on 2026-09-23. Targets: Claude Code 2.1.281 with Opus 5.5 at medium effort, and Grok CLI 1.0.41 with Grok 4.7 at high effort, each the harness default. Forced-load runs in neutrally named throwaway projects, two runs per variant per case, all cases frozen before the first run. Cross-graded and blind to variant: Grok 4.7 graded the Opus outputs and Opus 5.5 graded the Grok outputs, one grader per case per target, final answers only, every verdict constrained to a fixed JSON grade schema with quoted evidence. Grok returned no grade on some calls (empty answer, stopped as cancelled); those calls were rerun and never counted as verdicts. Costs are per run as each harness reported them.

- 2026-09-23 | 15abed3 (prior) | matched comparison: planted-rot-review, Grok 4.7 | fail (5/6), fail (2/6) | $0.08 and $0.10; neither reported signal counts. Settled fail
- 2026-09-23 | 51304b7 | matched comparison: planted-rot-review, Grok 4.7 | pass (6/6), pass (6/6) | $0.08 and $0.14. Settled pass: improvement on this target
- 2026-09-23 | 15abed3 (prior) | matched comparison: planted-rot-review, Opus 5.5 | fail (3/6), fail (2/6) | $0.15 and $0.20. Settled fail
- 2026-09-23 | 51304b7 | matched comparison: planted-rot-review, Opus 5.5 | fail (4/6), pass (6/6) | $0.20 and $0.22; the failing run reported counts only for signals with hits. Mixed: unsettled on this target, no improvement claimed
- 2026-09-23 | 15abed3 (prior) | matched comparison: cost-and-check-pruning, Grok 4.7 | pass (6/6), pass (6/6) | $0.12 and $0.17. Settled pass
- 2026-09-23 | 51304b7 | matched comparison: cost-and-check-pruning, Grok 4.7 | fail (5/6), fail (4/6) | $0.14 and $0.16; both quoted the new blind-comparison section ("log the preference as a note") and logged the reviewer's unblinded "read nicer" as that note instead of routing it to human feedback or a blind comparison. Settled regression on this target
- 2026-09-23 | 15abed3 (prior) | matched comparison: cost-and-check-pruning, Opus 5.5 | fail (5/6), pass (6/6) | $0.13 and $0.18. Mixed: unsettled on this target
- 2026-09-23 | 51304b7 | matched comparison: cost-and-check-pruning, Opus 5.5 | pass (6/6), pass (6/6) | $0.15 and $0.17
- 2026-09-23 | 15abed3 (prior) and 51304b7 | matched comparison: baseline-before-shipping, Grok 4.7 | pass (5/5) on all four runs | $0.08 to $0.11. No difference
- 2026-09-23 | 15abed3 (prior) and 51304b7 | matched comparison: baseline-before-shipping, Opus 5.5 | fail on all four runs (4/5, 4/5 prior; 3/5, 4/5 revised) | $0.10 to $0.12; every run failed the item on specifying test content. No difference
- 2026-09-23 | 15abed3 (prior) and 51304b7 | control: passing-baseline-regression-control, Grok 4.7 | pass (5/5) on all four runs | $0.04 to $0.05. No regression on this target
- 2026-09-23 | 15abed3 (prior) | control: passing-baseline-regression-control, Opus 5.5 | pass (5/5), pass (5/5) | $0.09 each. Settled pass
- 2026-09-23 | 51304b7 | control: passing-baseline-regression-control, Opus 5.5 | fail (4/5), fail (4/5) | $0.10 and $0.11; both offered the settling rule's "accept a failing control as that case's result" and "ship with that target's claim withheld" as a path past a failed control. Settled regression on this target
- 2026-09-23 | 15abed3 (prior) and 51304b7 | control: vendor-specific-advice-stays-out, Grok 4.7 | pass (6/6) on all four runs | $0.05 to $0.07. No regression on this target
- 2026-09-23 | 15abed3 (prior) | control: vendor-specific-advice-stays-out, Opus 5.5 | fail (5/6), fail (5/6) | $0.15 and $0.16. Settled fail, so this case is not a passing control on this target
- 2026-09-23 | 51304b7 | control: vendor-specific-advice-stays-out, Opus 5.5 | pass (6/6), pass (6/6) | $0.17 each. Settled pass
- 2026-09-23 | 51304b7 | claim scope | recorded | on Grok 4.7: improvement on planted-rot-review, regression on cost-and-check-pruning, no difference elsewhere. On Opus 5.5: regression on the passing-baseline control, planted-rot-review and cost-and-check-pruning unsettled, no difference on baseline-before-shipping; the vendor-advice control went from settled fail to settled pass, which a control cannot claim as improvement. The change returns to correction for the two regressions. Total run cost $2.89 on Opus 5.5 and $1.77 on Grok 4.7

Codex settling round on 2026-09-21 against the co-located template text. Codex CLI 0.154.0, Sol at medium effort, forced-load runs, scrubbed packets, blind Opus subagent grader. Every run is read together with the earlier runs of the same variant on this target, as the template's rule requires.

- 2026-09-21 | dd43427 | control: passing-baseline-regression-control, Codex Sol | fail (4/5), fail (4/5) | 44 s and 64 s; 73k/52k/0.9k and 73k/52k/1.4k tokens; co-location recovered one of the two missing facts, since both runs now say a discriminating case is still required. Both still omit advice to keep controls few, which the prompt does not ask about and the prior package volunteers on every run (three of three, settled pass). Revised is settled fail on this target, so the regression stands, narrowed to that one item
- 2026-09-21 | 15abed3 (prior) | control: vendor-specific-advice-stays-out, Codex Sol | pass (6/6) | 182 s; 165k/134k/1.5k tokens; settled pass across two runs
- 2026-09-21 | dd43427 | control: vendor-specific-advice-stays-out, Codex Sol | pass (6/6) | 215 s; 240k/209k/3.0k tokens; read with the 77bd796 fail the revised variant is mixed, so the case is unsettled on this target and the claim that the revision holds this contract there is withheld
- 2026-09-21 | dd43427 | matched comparison: cost-and-check-pruning, Codex Sol | fail (5/6) | 111 s; 101k/73k/2.6k tokens; dismissed the taste comment without routing it to human feedback or a blind comparison. The revised variant passed this case on this target at 77bd796 and 225b388, so it is now mixed: unsettled, and the improvement claimed for this target in the 2026-09-20 claim-scope line is withdrawn
- 2026-09-21 | dd43427 | claim scope | recorded | supersedes the 2026-09-20 claim-scope line. Settled improvement: planted-rot-review on Claude Code with Opus 5 and Fable 5.1, cost-and-check-pruning on Fable 5.1, baseline-before-shipping on Opus 5. On Codex Sol nothing is claimed: planted-rot-review and baseline-before-shipping fail under both packages, cost-and-check-pruning and the vendor-advice control are unsettled, and passing-baseline-regression-control is a settled regression on one item. The vendor-advice control is also unsettled on Opus 5

Co-location round on 2026-09-20 after dd43427 gathered the regression-control rules under one heading in the baseline template, moved and not copied. The owner chose this fix over an inline restatement in step 5 because it names no harness. Blind Opus subagent grader, scrubbed packets.

- 2026-09-20 | dd43427 | control: passing-baseline-regression-control, Claude Code Opus 5 | pass (5/5) | 36k tokens, 43 s; no regression on this target
- 2026-09-20 | dd43427 | control: passing-baseline-regression-control, Claude Code Fable 5.1 | pass (5/5) | 31k tokens, 23 s
- 2026-09-20 | dd43427 | matched comparison: cost-and-check-pruning, Claude Code Opus 5 | pass (6/6) | 35k tokens, 56 s; moving the control rules did not disturb the decision step
- 2026-09-20 | dd43427 | matched comparison: planted-rot-review, Claude Code Opus 5 | pass (6/6) | 81k tokens, 55 s
- 2026-09-20 | dd43427 | control: passing-baseline-regression-control, Codex Sol | not run — harness usage limit | the settling pair that would show whether co-location closes the settled regression logged below. Until it runs, that regression stands on this target and the change is not cleared to ship there

Settling round on 2026-09-20 after 225b388 added the unsettled-state rule to the baseline template. A fresh Opus subagent that saw no results drafted the rule; the author returned its first draft because two-of-three agreement made the state unreachable. Both variants of the contested control were rerun at the 07f79c9 prompt and read together with the closing pair below, as the rule requires. Blind Opus subagent grader, scrubbed packets.

- 2026-09-20 | 15abed3 (prior) | control: passing-baseline-regression-control, Codex Sol | pass (5/5) | 30 s; 74k/47k/0.9k tokens; with the closing pair the prior variant is settled pass on this target, two of two
- 2026-09-20 | 225b388 | control: passing-baseline-regression-control, Codex Sol | fail (3/5) | 33 s; 73k/46k/1.1k tokens; with the closing pair the revised variant is settled fail on this target, two of two, on the same two items both times: it never says a discriminating case is still required and never advises keeping controls few. Settled pass without the change against settled fail with it is a regression on this target under the template's rule. The change returns to correction
- 2026-09-20 | 15abed3 (prior) | control: passing-baseline-regression-control, Claude Code Opus 5 | pass (5/5) | 49k tokens, 36 s
- 2026-09-20 | 225b388 | control: passing-baseline-regression-control, Claude Code Opus 5 | pass (5/5) | 35k tokens, 50 s; no regression on this target
- 2026-09-20 | 225b388 | matched comparison: cost-and-check-pruning, revised on the new template text | pass (6/6) on Opus 5, Fable 5.1, and Codex Sol | 113k tokens 67 s, 78k tokens 52 s, and 55 s 73k/53k/2.1k tokens; the template edit did not disturb the case that exercises its decision step
- 2026-09-20 | 77bd796 | control: vendor-specific-advice-stays-out, Claude Code Opus 5 | unsettled | revised variant mixed across three runs (pass, fail, pass), prior variant settled pass across three; under the rule further runs cannot unmix it, so none were bought. The claim that this revision holds the vendor-advice contract on this target is withheld
- 2026-09-20 | 77bd796 | control: vendor-specific-advice-stays-out, Codex Sol | fail (5/6), one run | prior passed its one run; a single pair, accepted as the result until both variants are rerun

Final review and record corrections on 2026-09-20.

- 2026-09-20 | b0f542f | final checklist review | return to correction, narrow scope | fresh-context Opus subagent that saw none of the authoring. It found the package sound: description unchanged, 102 lines, body estimate 2,566 tokens, script read-only, all links internal, no model named in the instructions, more restatement removed than added. It returns the change because two labeled controls show revised-side failures that the template's rule calls regressions and that have not been rerun, and because the template has no vocabulary for an intermittently failing control, so the variance readings logged below are the author's judgment and not the package's rule. It also found the validator command named in step 4 was not the one that ran, fixed at ae44ab5
- 2026-09-20 | ae44ab5 | skill text after 77bd796 | recorded | one factual correction to step 4's validator command and one comment in the scan script. No case exercises either, so no comparison above is affected; structural validation and the 37 script assertions pass on this text
- 2026-09-20 | a67b48c | case correction: vendor-advice relabel and lightweight-artifacts item | recorded | vendor-specific-advice-stays-out relabeled a regression control because both packages passed it; the lightweight-artifacts item demanded exactly two durable artifacts while the testing convention keeps three, and it failed on both packages and both harnesses. Made by the author after seeing those grades
- 2026-09-20 | c951057 | case correction: seven checklists | recorded | restates the first-round line below for completeness: the reviewer saw no outputs or grades
- 2026-09-20 | 19642b5 | fixture correction: rot fixture name | recorded | the `name` field now matches the directory; no item graded it. Planted-rot runs before this commit used the old name
- 2026-09-20 | adaec59 | case correction: three settled items | recorded | passing-baseline control item narrowed to the consequence of a later failure; vendor-advice evidence item split, with its target-scope half tightened; planted-rot history item accepts cutting or restating the column order. The ruling reviewer saw no outputs and no grades. The author did describe to it, without attribution, the contested behavior classes graders had reported, including one quoted branching fix, so it was blind to results but not to the kinds of answer in dispute
- 2026-09-20 | 07f79c9 | case correction: control prompt | recorded | added "and what happens if that control later fails?" because an item graded that and the prompt never asked. Proposed by an independent simplicity reviewer who saw the run counts but no outputs
- 2026-09-20 | 77bd796 | smoke: Claude Code | not run — packaging unchanged since the c2b4c81 pass | replaces the undefined label "not run on this text" in the second-round block; the scripts directory last changed at f2b5d2e, before that pass, until the comment-only edit at ae44ab5
- 2026-09-20 | ae44ab5 | post-merge published-branch probe | not run | owed after merge because this branch adds a scripts directory

Closing pair on 2026-09-20 after 07f79c9 added "and what happens if that control later fails?" to the control prompt. An independent simplicity review found the two skill edits proposed for the Codex results were patches fitted to one question's grading, that both rules already exist in the package, and that the run counts do not establish a regression. No skill text changed after 77bd796.

- 2026-09-20 | 15abed3 (prior) | control: passing-baseline-regression-control, Codex Sol | pass (5/5) | 26 s; 74k/68k/0.7k tokens; read the baseline template and stated that a later failure is a regression that returns the change to correction
- 2026-09-20 | 77bd796 | control: passing-baseline-regression-control, Codex Sol | fail (3/5) | 23 s; 73k/69k/0.7k tokens; read the same template and stated the same consequence, so the item that failed in every earlier revised Codex run now passes. It failed two other items by not restating that a discriminating case is still required, which the prompt already grants, and by not advising that controls stay few, which the prompt does not ask. One pair; recorded as answer brevity on unprompted items, not as an established regression
- 2026-09-20 | 77bd796 | control: vendor-specific-advice-stays-out | recorded | two of four revised runs against none of four prior runs failed one item the graders called the loosest in the case; within chance at these counts and logged as variance on a grader-sensitive item
- 2026-09-20 | 77bd796 | claim scope | recorded | the revised package improves planted-rot-review on Claude Code with Opus 5 and Fable 5.1, cost-and-check-pruning on Fable 5.1 and Codex Sol, and baseline-before-shipping on Opus 5. On Codex Sol planted-rot-review fails under both packages, which is a limit of that target, and baseline-before-shipping fails under both. Nothing is claimed for harnesses or models that did not run

Regrade on 2026-09-20 of existing outputs against three items an independent reviewer settled at adaec59. No new runs. Blind Opus subagent graders, scrubbed packets. For these three cases the lines here supersede the grades in the two blocks below; costs are unchanged and stay on those lines.

- 2026-09-20 | 77bd796 | regrade: planted-rot-review | Opus 5 pass (6/6) three times, prior fail (3/6); Fable 5.1 pass (6/6), prior fail (5/6); Codex Sol fail (4/6), prior fail (3/6) | the revised package passes every run on both Claude models; on Codex it reports the counts and the rot, then lists the ordinary-prose sentence and the row-count criterion as defects, so no pass on that target
- 2026-09-20 | 77bd796 | regrade: control vendor-specific-advice-stays-out | Opus 5 fail (5/6), pass, pass; Codex Sol fail (5/6) | the prior package passes all four of its runs (Opus 5 three times, Codex once). Both failing revised runs attach the with-and-without comparison to their own rewrite or to a harness variant and never say a removal needs one. Two of four revised runs against none of four prior runs is a regression candidate on this control
- 2026-09-20 | 77bd796 | regrade: control passing-baseline-regression-control | Opus 5 pass, pass, one run ungraded; Fable 5.1 pass; Codex Sol fail (4/5), fail (3/5) | the prior package on Codex passes once and fails once (4/5). The grader returned seven of eight outputs, so one Opus 5 run has no grade this round. Both revised Codex runs omit what happens if the retained control later fails; regression candidate on this target

Codex round on 2026-09-20 against the same text as the second Claude round: Codex CLI 0.154.0, Sol at medium effort, forced-load runs in neutrally named disposable projects, scrubbed packets, blind Opus subagent grader. Codex reports no duration, so notes carry wall-clock seconds and input/cached/output tokens. No run read the same-name user-level copy. These lines supersede the c2b4c81 Codex lines in the first-round block.

- 2026-09-20 | 15abed3 (prior) | matched comparison: planted-rot-review, Codex Sol | fail (4/6) | 218 s; 219k/191k/4.3k tokens; no signal counts, and listed the ordinary-prose sentence as the top defect
- 2026-09-20 | 77bd796 | matched comparison: planted-rot-review, Codex Sol | fail (5/6) | 201 s; 206k/178k/3.9k tokens; reported every signal count and said the ordinary-prose hit stands, then opened its fix list with resolving that same sentence, so the case shows more items passed and no pass on this target
- 2026-09-20 | 77bd796 | matched comparison: cost-and-check-pruning, Codex Sol | pass (6/6) | 65 s; 74k/47k/2.5k tokens; the prior package's first-round output regrades at 5/6 (105k/75k/2.1k tokens), failing the taste-routing item
- 2026-09-20 | 77bd796 | matched comparison: baseline-before-shipping, Codex Sol | fail (2/5) | 68 s; 168k/140k/2.3k tokens; the prior package also fails 2/5; both runs stopped on the missing example package and never specified test content, so the description-only fix shows no effect on this target
- 2026-09-20 | 77bd796 | control: passing-baseline-regression-control, Codex Sol | fail (4/5), fail (4/5) | 25 to 26 s; 73k/50k/0.7k tokens each; both kept the control, denied it improvement credit, and ran it matched, and neither said a regression on it fails the comparison. With the c2b4c81 run the revised package is 0 of 3 on this target against 1 of 2 for the prior package. The grader notes the failing item bundles two requirements
- 2026-09-20 | 77bd796 | control: vendor-specific-advice-stays-out, Codex Sol | pass (5/5) | 125 s; 203k/175k/2.6k tokens
- 2026-09-20 | 77bd796 | control: fixture-review-prioritized-findings, Codex Sol | pass (5/5) | 174 s; 201k/187k/2.6k tokens
- 2026-09-20 | 77bd796 | control: independent-fresh-context-review, Codex Sol | pass (3/3) | 46 s; 104k/95k/1.5k tokens
- 2026-09-20 | 77bd796 | control: lightweight-artifacts-and-no-ceremony, Codex Sol | pass (4/4) | 73 s; 107k/82k/3.1k tokens
- 2026-09-20 | 77bd796 | smoke: Codex CLI 0.154.0, Sol | pass | installed from local source into a disposable project with skills CLI 1.7.0 in copy mode; files identical to source and `scripts/signal-scan.sh` kept its executable bit; on the contract query "Help me create a new skill for formatting SQL queries" the trace shows Codex reading the copy under the disposable project's `.agents/skills/` and running its scan script, and never the same-name user-level copy that exists on this machine. The run was stopped at a five-minute cap while it was still drafting
- 2026-09-20 | 77bd796 | smoke: Claude Code | not run on this text | packaging is unchanged since the c2b4c81 pass logged below
- 2026-09-20 | 77bd796 | final checklist review | not run | pending the owner's decision on the Codex results

Second round on 2026-09-19, after 77bd796 sharpened the step 5, 7, and 8 pointers, defined the description-only matched pair, and added the grader blinding rule. Same method as the block below, with two changes: run folders carry neutral names, and every packet was scrubbed of variant names before a blind Opus subagent graded it. These lines supersede the c2b4c81 Claude Code lines below. The Codex lines below tested c2b4c81 and stand as history until Codex reruns on this text.

- 2026-09-19 | 77bd796 | structural validation | pass | `agentskills validate` from the official `skills-ref` package through uvx; description unchanged from 15abed3
- 2026-09-19 | 77bd796 | fixture runner: signal scan | pass (37/37) | unchanged script
- 2026-09-19 | 15abed3 (prior) | matched comparison: baseline-before-shipping, Claude Code Opus 5 | fail (4/5), fail (4/5) | two runs, 70k to 75k tokens, 43 to 45 s; both tested the revised description alone
- 2026-09-19 | 77bd796 | matched comparison: baseline-before-shipping, Claude Code Opus 5 | pass (5/5) three times | 91k to 100k tokens, 44 to 47 s; each named the prior description against the revised one; this existing case now discriminates for the description-only pair
- 2026-09-19 | 77bd796 | matched comparison: baseline-before-shipping, Claude Code Fable 5.1 | pass (5/5) | 62k tokens, 24 s; no prior-side Fable run, so this shows no improvement on its own
- 2026-09-19 | 15abed3 (prior) | matched comparison: planted-rot-review, Claude Code Opus 5 | fail (2/6) | 63k tokens, 85 s
- 2026-09-19 | 77bd796 | matched comparison: planted-rot-review, Claude Code Opus 5 | fail (5/6), pass (6/6), pass (6/6) | 81k to 82k tokens, 58 to 66 s; the failing run offered to keep or cut the column-order line, and a later grader passed a similar branching fix, so the item is grader-sensitive
- 2026-09-19 | 15abed3 (prior) | matched comparison: planted-rot-review, Claude Code Fable 5.1 | fail (5/6) | 72k tokens, 112 s; no signal counts
- 2026-09-19 | 77bd796 | matched comparison: planted-rot-review, Claude Code Fable 5.1 | pass (6/6) | 56k tokens, 50 s
- 2026-09-19 | 77bd796 | matched comparison: cost-and-check-pruning, Claude Code Opus 5 | pass (6/6) | 93k tokens, 63 s; the prior package also passes on this target, so it does not discriminate here
- 2026-09-19 | 77bd796 | matched comparison: cost-and-check-pruning, Claude Code Fable 5.1 | pass (6/6) | 75k tokens, 57 s; the prior package fails 5/6 on this target (47k tokens, 35 s)
- 2026-09-19 | 77bd796 | control: passing-baseline-regression-control | pass (5/5) three times on Opus 5, pass (5/5) on Fable 5.1 | 30k to 48k tokens, 16 to 46 s
- 2026-09-19 | 77bd796 | control: vendor-specific-advice-stays-out, Claude Code Opus 5 | fail (4/5), pass (5/5), pass (5/5) | 83k to 85k tokens; the prior package passed all three of its runs; the failing run never said what evidence a removal would need, and the grader called that two-part item the loosest in the case, so a regression is not established
- 2026-09-19 | 77bd796 | control: fixture-review-prioritized-findings, Claude Code Opus 5 | pass (5/5) | 82k tokens, 61 s
- 2026-09-19 | 77bd796 | control: independent-fresh-context-review, Claude Code Opus 5 | pass (3/3) | 67k tokens, 46 s
- 2026-09-19 | 77bd796 | control: lightweight-artifacts-and-no-ceremony, Claude Code Opus 5 | pass (4/4) | 59k tokens, 59 s
- 2026-09-19 | 77bd796 | all cases on Codex CLI | not run — harness usage limit | credits exhausted during the first round
- 2026-09-19 | 77bd796 | smoke: Claude Code, Codex CLI | not run | the c2b4c81 Claude Code smoke pass below predates this text; packaging is unchanged since, and the probe is rerun with Codex
- 2026-09-19 | 77bd796 | final checklist review | not run | after the Codex runs

Method for the 2026-09-19 lines: forced-load runs in disposable projects, one per variant, with the skill read from an explicit path and harness skill discovery disabled, so no same-name user-level copy could load. Claude Code 2.1.278 ran Opus 5 and Fable 5.1 at medium effort; Codex CLI 0.154.0 ran Sol at medium effort. Blind Opus subagent grader against the case checklists at c951057, variant and run folder hidden. Codex reports no duration, so its notes carry wall-clock seconds and input/cached/output tokens.

- 2026-09-19 | c2b4c81 | structural validation | pass | `agentskills validate` from the official `skills-ref` package through uvx: valid skill, scripts directory included
- 2026-09-19 | c2b4c81 | fixture runner: signal scan | pass (37/37) | deterministic runner in the pre-push roster; includes the assertion that the scan writes no file
- 2026-09-19 | c2b4c81 | signal scan over skills/ | recorded | zero hits for pressure language, thinking scaffolds, format and narration suppressors, and every other vendor signal; 10 migration-relative hits are ordinary domain prose, 3 history identifiers are issue references and a review date, 7 pinned model names are the dated routing table
- 2026-09-19 | 15abed3 (prior) | matched comparison: planted-rot-review, Claude Code Opus 5 | fail (3/6) | 65k tokens, 86 s; no signal counts, listed the ordinary-prose sentence as a defect
- 2026-09-19 | c2b4c81 | matched comparison: planted-rot-review, Claude Code Opus 5 | pass (6/6) | 81k tokens, 76 s
- 2026-09-19 | 15abed3 (prior) | matched comparison: planted-rot-review, Claude Code Fable 5.1 | fail (4/6) | 89k tokens, 110 s
- 2026-09-19 | c2b4c81 | matched comparison: planted-rot-review, Claude Code Fable 5.1 | pass (6/6) | 56k tokens, 47 s
- 2026-09-19 | 15abed3 (prior) | matched comparison: planted-rot-review, Codex Sol | fail (3/6) | 202 s; 255k/221k/3.7k tokens
- 2026-09-19 | c2b4c81 | matched comparison: planted-rot-review, Codex Sol | fail (5/6) | 195 s; 330k/298k/5.7k tokens; reported counts, history, the named-model workaround, and the unverified version, but faulted the row-count completion check, so the case shows no pass on this target
- 2026-09-19 | 15abed3 (prior) | matched comparison: cost-and-check-pruning, Claude Code Opus 5 | pass (6/6) | 110k tokens, 63 s; same as revised, so this target does not discriminate
- 2026-09-19 | c2b4c81 | matched comparison: cost-and-check-pruning, Claude Code Opus 5 | pass (6/6) | 51k tokens, 52 s
- 2026-09-19 | 15abed3 (prior) | matched comparison: cost-and-check-pruning, Claude Code Fable 5.1 | fail (5/6) | 47k tokens, 35 s; routed the taste comment to a new checklist item
- 2026-09-19 | c2b4c81 | matched comparison: cost-and-check-pruning, Claude Code Fable 5.1 | pass (6/6) | 118k tokens, 53 s
- 2026-09-19 | 15abed3 (prior) | matched comparison: cost-and-check-pruning, Codex Sol | fail (4/6) | 69 s; 105k/75k/2.1k tokens
- 2026-09-19 | c2b4c81 | matched comparison: cost-and-check-pruning, Codex Sol | pass (6/6) | 136 s; 128k/99k/3.1k tokens
- 2026-09-19 | c2b4c81 | control: vendor-specific-advice-stays-out | pass (5/5) on Opus 5 and Sol | prior package also passes 5/5 on both, so the case is a labeled control; Opus 5 60k to 84k tokens, Sol 108 to 110 s
- 2026-09-19 | c2b4c81 | control: fixture-review-prioritized-findings | pass (5/5) on Opus 5, pass (5/5) twice on Sol | prior package passes 5/5 twice on Sol; Opus 5 82k tokens, 70 s
- 2026-09-19 | c2b4c81 | control: lightweight-artifacts-and-no-ceremony | pass (4/4) twice on Opus 5, pass (4/4) on Sol | prior package passes on both; Opus 5 57k to 61k tokens
- 2026-09-19 | c2b4c81 | control: independent-fresh-context-review | pass (3/3) on Opus 5 and Sol | Opus 5 60k tokens, 47 s; Sol 38 s
- 2026-09-19 | c2b4c81 | control: passing-baseline-regression-control, Claude Code Opus 5 | pass (5/5) | 51k tokens, 47 s
- 2026-09-19 | c2b4c81 | control: passing-baseline-regression-control, Codex Sol | fail (3/5) | 27 s; one run; the prior package passed once (5/5) and failed once (4/5) on the same target, so a regression is not established; variance reruns not run, Codex usage limit
- 2026-09-19 | c2b4c81 | control: baseline-before-shipping, Claude Code Opus 5 | fail (4/5), pass (5/5), fail (4/5) | three runs; the prior package failed both of its runs (4/5) on the same item, a prior-versus-revised activation comparison for a description-only change, so the weakness predates this revision
- 2026-09-19 | c2b4c81 | control: baseline-before-shipping, Codex Sol | fail (2/5) | 203 s; the prior package also fails 2/5
- 2026-09-19 | c2b4c81 | variance reruns on Codex Sol | not run — harness usage limit | six runs never started or were cut off; none is counted
- 2026-09-19 | c2b4c81 | smoke: Claude Code 2.1.278, Opus 5 | pass | installed from local source into a disposable project with skills CLI 1.7.0 in copy mode; installed files identical to source and `scripts/signal-scan.sh` kept its executable bit; on the contract query "Help me create a new skill for formatting SQL queries" the trace shows the Skill tool loading the copy under the disposable project's `.claude/skills/`, with project-only settings so no user-level copy was in scope. An earlier attempt used a query that is not in the trigger contract and did not activate; it is not counted
- 2026-09-19 | c2b4c81 | smoke: Codex CLI | not run — harness usage limit |
- 2026-09-19 | (working tree) | case correction: planted-rot completion-criteria item | recorded | narrowing of scope, not a loosening of acceptance: a reviewer who saw no outputs or grades ruled that adding a missing check or an undefined artifact contract passes, while calling an existing criterion inadequate still fails. "Reconcile expected invoice identities, not merely an equal row count" still fails it, so no logged grade changes
- 2026-09-19 | c2b4c81 | final checklist review | not run | pending the remaining Codex runs
- 2026-09-19 | 31790a6 | case correction: planted-rot fixture | recorded | the fixture skipped deleted-customer rows and also required the full row count; three of four first-round runs reported that real contradiction and two items failed them for it; fixture fixed, checklist untouched, first-round planted-rot runs discarded
- 2026-09-19 | c951057 | case correction: seven checklists | recorded | a reviewer who saw no outputs or grades rewrote items that graded phrasing, a fixed output order, or the skill's vocabulary, merged duplicates, and removed items any agent passes; all earlier grades against the old items are superseded by the lines above
- 2026-09-19 | c2b4c81 | grading correction: blinding | recorded | first-round packets leaked the variant through run-folder names quoted in outputs; planted-rot was regraded from scrubbed packets and those grades are the ones logged

- 2026-09-08 | b075928 (working tree) | structural validation | pass | official `skills-ref` was unavailable; manual Agent Skills field, length, name, and package checks passed with the repository validator, catalog, and relative-link checks
- 2026-09-08 | b075928 (working tree) | trigger sample after SKILL.md/eval routing | pass (3/3) | three isolated fresh-context judges saw only the name, candidate description, and one query; eval update and SKILL.md/grader edit activated; standalone grader/rubric near miss stayed inactive. Complete trigger suite not rerun in this session.

- 2026-08-26 | db15238 | matched comparison: passing-baseline-regression-control (prior) | fail (2/5) | isolated runner allowed the control and limited its claim, but omitted the separate-discrimination requirement, matched-control regression blocking, and bounded-use guidance; separate blind grader
- 2026-08-26 | db15238 (working tree) | matched comparison: passing-baseline-regression-control (candidate) | pass (5/5) | fresh runner applied the candidate protocol; a separate blind grader confirmed explicit control labeling, separate discrimination, matched regression blocking, bounded use, and honest claims
- 2026-08-26 | db15238 (working tree) | structural validation | pass | official `skills-ref` was unavailable; manual Agent Skills field, length, name, and package checks passed with the repository validator, catalog, and relative-link checks

- 2026-08-17 | b8fbafb + terminology diff | trigger suite: generic skill terminology | pass (10/10 should-trigger; 11/11 near misses) | Twenty-one isolated ephemeral Codex CLI 0.147.0 contexts each saw only the current name, description, and one query; every first judgment was categorical, including `no` for the added role-playing-game near miss.

Branch-time `git rev` values below are preserved by PR #19 even if the
branch is squash-merged; the archive pointer's mainline commit stays
directly reachable.

- 2026-07-30 | 176b818 (prior) | matched comparison: baseline-before-shipping | pass (5/5) | Prior-side run against the frozen pre-retune package for the U5 revision's matched pair. Control held — the substantive-change discipline exists in both variants; the prior-specific tier question, monolithic record artifacts, and waiver machinery surfaced as the process delta the retune removes.
- 2026-07-30 | 176b818 (prior) | matched comparison: independent-fresh-context-review | pass (4/4) | Prior-side control held; independence outcome identical across variants.
- 2026-07-30 | 176b818 (prior) | matched comparison: fixture-review-prioritized-findings | pass (5/5) | Prior-side control held; read-only audit shape identical. With the three revised-side runs above, the matched comparison shows no regression and locates the intended delta in the retired ceremony and emitted artifact shape.

- 2026-07-30 | 9b76104 | case: fixture-review-prioritized-findings | pass (5/5) | Fresh-context run against the retuned repo package (U5); read SKILL.md + review-checklist.md.
- 2026-07-30 | 9b76104 | case: independent-fresh-context-review | pass (4/4) | Fresh-context run against the retuned repo package (U5).
- 2026-07-30 | f2fe80d | case: baseline-before-shipping | pass (5/5) | Fresh-context rerun against the final checked-in case text (post-clarification) and the retuned repo package; graded including the unforced-activation carve-out item. Supersedes the pre-clarification run at 9b76104.
- 2026-07-30 | aa6f7e4 | case: lightweight-artifacts-and-no-ceremony (revised) | pass (3/3) | Fresh-context run against the retuned repo package; no tier question, thin artifacts only, not-run handling without waivers.
- 2026-07-30 | 176b818 (prior) | matched comparison: lightweight-artifacts-and-no-ceremony | fail (0/3) | Prior-side half against the frozen pre-retune package: it asked the tier question, kept two monolithic evidence records, and routed the unrunnable check through waiver/Claim Ceiling machinery — the discriminating delta the U5 revision intends. With the three controls above, the matched comparison shows the intended improvement with no regression.
- 2026-07-30 | aa6f7e4 | structural validation (skills-ref) | pass | Tier-1 check on the retuned package including all PR-review corrections; rerun on the final package state before merge.
- 2026-07-30 | 93f0a43 | smoke: Claude Code | pass | Rerun with provenance: installed from source into a disposable project (project settings only); the transcript shows the Skill tool activating creating-portable-skills on a should-trigger query and reading the installed copy's own base directory (`.claude/skills/creating-portable-skills` under the disposable project). Supersedes the activation-only run at 9b76104.
- 2026-07-30 | 9b76104 | smoke: Codex CLI 0.145.0 | pass | Installed from source into a disposable project; trace read the exact installed .agents path and activated on a should-trigger query.
- 2026-07-30 | cc66ee8 | archive pointer | — | Full prior evidence (listing
  runs, matched comparisons, native checks, package hashes) is in git
  history at this commit, before the restructure removed trigger-queries.md,
  baseline-cases.md, and results.md.
