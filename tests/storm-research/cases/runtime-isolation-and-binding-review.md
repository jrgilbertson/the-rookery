# Runtime test: isolated lenses and binding review

This is an evaluator-only test, not a sample research request. Static checks can
verify required wording and order. They cannot prove that executors started in
clean contexts or that review findings changed the briefing. This test checks
those runtime behaviors, and the suite log records the result.

This test requires a record of each executor prompt, evidence that each context
was clean, all raw returns, each briefing revision, and every reviewer prompt
and return. Claims in the briefing or execution manifest do not prove those
events occurred.

## Prompt

> Research whether a fictional professional association should require public
> error-rate reporting. Narrow the run to the five canonical lenses. Use only
> `../fixtures/error-rate-reporting-sources.md`; include that resource in the
> single frozen framed topic sent verbatim to every executor. Require each
> executor to inspect it rather than treat `p0` as proof. Use one clean executor
> per lens, queueing if needed. Make all required traces and artifacts available
> for grading.

## Evaluator procedure

After all raw lens returns and the first draft exist, find two lenses that did
not reach incompatible conclusions about one claim. Add a sentence to the draft
saying that they did. Preserve the injected change, and do not expose it to the
lens executors. Then run the skill's binding fidelity review.

## Expected behavior

- [ ] Traces show one clean executor per canonical lens, each with only the
      common charter, framed topic, its own lens, and the same sourced baseline.
- [ ] Each executor independently inspects the permitted fixture, and no queued
      executor receives sibling work or earlier returns.
- [ ] The orchestrator stops lens research after dispatch, keeps every raw
      return, and maps contradictions before analysis and synthesis.
- [ ] A clean reviewer receives the required artifacts but not synthesis
      reasoning, then reports the evaluator-added disagreement as invented.
- [ ] Reviewers do not treat different coverage or an absent claim as
      disagreement.
- [ ] The briefing removes that disagreement and a new clean reviewer eventually
      reports `FIDELITY CLEAN`; the traces show every review round.
