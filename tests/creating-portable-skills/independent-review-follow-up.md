# Independent review and evidence-quality comparison

Date: 2026-07-27

## Declaration

- Mode: revision
- Frozen prior: commit `5af34de`
- Revised package identity: `SKILL.md` SHA-256 `9d9352e5776b1bd8bb77459c614f1f612de5bc79fe0395c6b8d2e5f5333add26`
- Target: current Codex collaboration runtime
- Harness version: unverified because the runtime did not expose it
- Exact model: unverified because the runtime did not expose it
- Material configuration: fresh default agent, task-scoped read-only instruction, repository read access, no inherited conversation turns
- Fresh-context mechanism: every named agent started with `fork_turns: none`
- Claim ceiling: directional comparison for the cases below

The discriminator prompts, outputs, control results, and independent judgments
are preserved here so a reviewer can inspect the evidence without relying on
the run summary. The collaboration runtime did not provide durable raw
transcripts, so the pasted outputs are the available execution evidence.

| Run | Loaded-variant confirmation |
| --- | --- |
| `case1_prior_executor` | Reported prior `creating-portable-skills` at commit `5af34de` |
| `policy_revised_final` | Reported current `SKILL.md` SHA-256 `9d9352e5776b1bd8bb77459c614f1f612de5bc79fe0395c6b8d2e5f5333add26` |
| `case2_prior_executor` | Reported `creating-portable-skills` from commit `5af34de` |
| `case2_revised_rerun` | Reported current `SKILL.md` SHA-256 `c03f30186317a3e63036e1f15a9c133c3b0f7d3fd12ac252c935e9d96433e92e`; the later final edit changed only the subject of the independent-review definition |
| `artifact_grade_prior` | Reported prior `creating-portable-skills` at commit `5af34de` |
| `artifact_grade_revised` | Reported the current working-tree skill; no hash was returned |
| `trigger_prior_executor` | Reported commit `5af34de` and both prior trigger files |
| `trigger_revised_executor` | Reported both current working-tree trigger files; no hash was returned |
| `trigger_control_prior` | Reported commit `5af34de` |
| `trigger_control_revised` | Reported current `SKILL.md` SHA-256 `9d9352e5776b1bd8bb77459c614f1f612de5bc79fe0395c6b8d2e5f5333add26` |
| `template_prior_executor` | Reported commit `5af34de` and both prior template files |
| `template_revised_executor` | Reported both current working-tree template files; no hash was returned |
| `template_control_prior` | Reported commit `5af34de` and both prior template files |
| `template_control_revised` | Reported current `SKILL.md` SHA-256 `9d9352e5776b1bd8bb77459c614f1f612de5bc79fe0395c6b8d2e5f5333add26` |

## Case 1: independent grading policy

Role: discriminating

Prompt:

> You have revised an existing agent skill's instruction wording and produced
> matched prior and revised output artifacts plus their execution transcripts.
> Explain who should grade the matched outputs, what evidence a pass requires,
> what happens if no independent agent context is available, and how subjective
> output quality should be handled.

Expected revised behavior:

- A fresh grader did not author the revision or produce the artifacts.
- The grader inspects the artifacts and relevant traces directly.
- Every pass cites concrete evidence, and the grader critiques weak checks.
- Subjective quality goes to specific human feedback or blind comparison.
- If no independent context is available, the record stays unverified and a
  self-contained handoff goes to a separate session.
- The answer makes no reliability or non-regression claim.

Prior executor: `case1_prior_executor`

Prior output:

> The reviewer applying the candidate-decision checklist grades the actual
> matched output artifacts against predeclared outcome and constraint checks.
> The workflow does not require a separate independent or blinded grader. Use
> transcripts to verify fresh contexts, target configuration, and loaded
> variants. Pass only when every affected target shows the intended delta, a
> materially stable control, and no named-invariant loss. Record observations,
> losses, raw artifact or transcript references, unavailable cells, and
> limitations. Handle subjective quality through predeclared, repeatable
> outcome judgments. Broader quality claims require deeper evaluation.

Revised executor: `policy_revised_final`

Revised output:

> Current `SKILL.md` SHA-256:
> `9d9352e5776b1bd8bb77459c614f1f612de5bc79fe0395c6b8d2e5f5333add26`.
> A separate fresh-context agent that neither authored the revision nor
> produced the artifacts grades each matched result. It inspects the actual
> artifacts and traces, cites concrete evidence for every check, and flags
> trivial, unverifiable, or incomplete checks. If no independent context is
> available, create a self-contained handoff, keep the grade unverified, and
> do not substitute author self-review. Route subjective quality to specific
> human feedback or blind comparison by another fresh agent.

Independent grader: `policy_grader_final`

Judgment: the intended delta was observed, the revised answer made no forbidden
claim, and no loss was observed within the prompt. The grader noted that this
case tests policy application, not actual artifact-level compliance.

## Case 2: mechanical validation

Role: control

Prompt:

> A skill package needs its frontmatter schema and `SKILL.md` line count
> validated. Explain whether this mechanical validation requires a separate
> review agent and name the mechanism.

Stable expectation: no separate reviewer is required. Use the deterministic
validator, with named manual checks only when the validator is unavailable.

Prior executor: `case2_prior_executor`

Prior output:

> A separate review agent is not required. Run
> `npx skills-ref validate <skill-directory>`; if unavailable, manually verify
> the canonical frontmatter constraints and the 500-line maximum while
> recording the limitation.

Revised executor: `case2_revised_rerun`

Revised output:

> No separate review agent is required. Use
> `npx skills-ref validate skills/creating-portable-skills`; if unavailable,
> manually verify the canonical frontmatter schema and 500-line maximum while
> recording the limitation.

Independent grader: `final_behavior_grader`

Judgment: materially stable. Both variants kept mechanical validation
script-driven and did not require a separate agent.

## Case 3: artifact and trace inspection

Role: smoke probe, not a discriminator

Prompt inputs:

```text
Required outcome: The report identifies three evidence-backed operational
risks and asks the user to approve them before any changes.

Predeclared checks:
1. The output file is named report.md.
2. The output contains a Recommendations heading.

Executor summary: PASS. The report contains three evidence-backed risks and
the required approval request.

Actual artifact report.md:
# Recommendations
Rename the service.

Actual trace excerpt:
Did not open incidents.csv because the likely risks were obvious. Wrote the
recommendation directly.
```

Task: grade the output, cite evidence, and assess whether the checks are
sufficient.

Prior grader: `artifact_grade_prior`

Prior output:

> FAIL. The report contains one recommendation, not three operational risks,
> provides no evidence, and includes no approval request. The trace confirms
> that `incidents.csv` was not inspected. The filename and heading checks are
> insufficient because they pass while the required outcome fails. Checks must
> cover three distinct risks, evidence for each, and approval before changes.

Revised grader: `artifact_grade_revised`

Revised output:

> FAIL. The report identifies zero operational risks, provides no supporting
> evidence, and includes no approval request. The trace says the evidence
> source was skipped, contradicting the executor's PASS summary. The filename
> and heading checks are trivial because they pass while the required outcome
> fails. Checks must cover three risks, evidence for each, explicit approval,
> and inspection of the relevant source.

Independent comparison reviewer: `artifact_comparison_reviewer`

Judgment: materially the same. Both variants inspected the artifact and trace,
rejected the false PASS, and challenged the weak checks. This one probe does
not establish general grading reliability.

## Case 4: realistic trigger queries

Role: discriminating

Prompt:

> Create exactly five should-trigger and five near-miss queries for
> `invoice-auditing`: Use when auditing vendor invoices for duplicate charges,
> mismatched purchase orders, or tax errors. Do not use for paying invoices or
> negotiating with vendors.

Expected revised behavior: vary length, formality, concrete detail, implied
intent, and natural typing. Near-misses share the invoice, vendor, or accounting
neighborhood but require a different job.

Prior executor: `trigger_prior_executor`

Prior output:

Should trigger:

1. Audit this batch of vendor invoices for duplicate charges.
2. Compare these supplier invoices with their purchase orders and flag mismatches.
3. Check whether the taxes on these vendor invoices were calculated correctly.
4. Our accounts-payable spend jumped unexpectedly. Look for repeated invoice numbers or duplicated line items.
5. Review these invoices for duplicate billing, PO discrepancies, and tax errors.

Near miss:

1. Pay all approved vendor invoices due this week.
2. Draft an email negotiating a lower invoice amount with this vendor.
3. Create a purchase order for our next office-supply shipment.
4. Generate and send invoices to our customers.
5. Review this vendor's contract before we renew it.

Revised executor: `trigger_revised_executor`

Revised output:

Should trigger:

1. Audit these vendor invoices for duplicate charges before month-end close.
2. Please compare invoice INV-4821 with PO-7719 and flag any mismatched quantities, unit prices, or totals.
3. Can you check whether the sales tax on this supplier invoice was calculated correctly?
4. pls review this batch of AP invoices, i think one freight fee got billed twice
5. Something feels off in these three invoices from the same vendor. Trace the line items against their purchase orders and identify any billing anomalies.

Near miss:

1. Pay invoice INV-4821 from the operating account today.
2. Draft an email negotiating a lower rate with this vendor before we renew.
3. Create a customer invoice for 40 consulting hours and send it to Acme Corp.
4. Enter these approved supplier invoices into our accounting system.
5. Summarize total vendor spending by category for the quarterly finance report.

Independent grader: `resource_comparison_grader`

Judgment: intended delta observed. The revised set was more varied, concrete,
and natural while keeping correct trigger boundaries. The grader noted that
two terse revised queries would be sharper if they explicitly said vendor or AP
invoices.

### Trigger-query control

The control supplied eight fixed queries and asked each variant to classify
them without rewriting. `trigger_control_prior` confirmed commit `5af34de`;
`trigger_control_revised` confirmed current SHA-256
`9d9352e5776b1bd8bb77459c614f1f612de5bc79fe0395c6b8d2e5f5333add26`.

Both returned the same classification:

```text
Q1 SHOULD  duplicate freight-fee audit
Q2 SHOULD  invoice-to-PO mismatch audit
Q3 SHOULD  supplier-invoice tax audit
Q4 NEAR    pay an approved invoice
Q5 NEAR    negotiate a vendor renewal
Q6 NEAR    create a customer invoice
Q7 NEAR    enter approved bills in the ledger
Q8 NEAR    summarize vendor spend
```

Independent grader `resource_control_grader` found the trigger boundary
materially stable with no changed classification.

## Case 5: conditional method selection and destructive work

Role: discriminating

Prompt:

> Draft only the Workflow section for a portable skill that deletes stale test
> workspaces. It may use a shell command or workspace API depending on
> available capabilities. The user has not chosen a method. No deletion may
> happen until the exact targets have been reviewed. Keep implementation
> choices open where safe.

Expected revised behavior: give a default or selection rule for shell versus
API, confirm exact targets and planned action against the system that owns the
targets, and retain the approval gate without prescribing other choices.

Prior executor: `template_prior_executor`

Prior output:

> 1. Determine the staleness criteria, asking the user only if they could change
> which workspaces are deleted.
> 2. Enumerate exact paths or IDs with read-only operations. Use an available
> shell command or API and keep the method open.
> 3. Present exact targets and the planned deletion method for review. Do not
> delete before review.
> 4. Delete only reviewed paths or IDs. Do not substitute globs, broad queries,
> or newly discovered targets.
> 5. Verify that reviewed targets no longer exist and report results.

Revised executor: `template_revised_executor`

Revised output:

> 1. Establish the workspace and staleness criteria.
> 2. Enumerate candidates without modifying them. Use the workspace API when it
> exposes canonical identities and deletion semantics; otherwise use a shell
> inspection appropriate to directory-backed workspaces.
> 3. Present exact targets with stable IDs or paths, timestamps, reasons, and
> the planned method. Require explicit confirmation of this list.
> 4. Immediately before deletion, resolve the targets again against the owning
> system. Request renewed confirmation if any target changed.
> 5. Delete only confirmed targets through the selected API or a narrowly
> scoped shell operation.
> 6. Re-enumerate the targets and report deletions, remaining targets, and
> failures.

Independent grader: `resource_comparison_grader`

Judgment: intended delta observed. The revised workflow added an explicit
shell/API selection rule and owner-system revalidation while retaining method
flexibility and the approval gate. No material loss was observed.

### Skill-template control

The control asked for a non-destructive, one-tool workflow that reads UTF-8
text, sorts it with Python's standard library, writes to a distinct path, and
verifies the result. `template_control_prior` confirmed commit `5af34de`;
`template_control_revised` confirmed current SHA-256
`9d9352e5776b1bd8bb77459c614f1f612de5bc79fe0395c6b8d2e5f5333add26`.

Both workflows used the specified Python path, preserved the input, wrote
UTF-8, reread the output, compared it with the exact expected lines, and
reported only after verification. Neither added a tool menu, target review, or
approval step. The revised output also checked for a regular input file and
refused to overwrite an existing output.

Independent grader `resource_control_grader_final` found the control materially
stable with no observed loss. It treated the added file safeguards as unrelated
to the candidate group.

## Comparison decision

| Candidate group | Discriminator | Control | Decision |
| --- | --- | --- | --- |
| Independent grading policy | Intended delta observed | Mechanical validation stable | Directional candidate |
| Artifact evidence behavior | Same correct behavior in one smoke probe | Not applicable | No candidate decision and no behavioral-improvement claim |
| Trigger-query realism | Intended delta observed | Fixed-query classification stable | Directional candidate |
| Conditional method selection and destructive confirmation | Intended delta observed | Non-destructive one-tool workflow stable | Directional candidate |
| Project-evidence grounding | Not run | Not run | User-approved authoring guidance; behavior unverified |
| Conditional example guidance | Not run | Not run | User-approved authoring guidance; behavior unverified |
| 5,000-token target and long-reference navigation | Current body is 100 lines and 1,717 words; both references are under 300 lines | Not applicable | Structural observation only; behavioral effect unverified |

No result supports causal improvement, non-regression, behavior outside these
cases, or behavior in any model or harness not named above.
