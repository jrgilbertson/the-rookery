# Lens Charter

The orchestrator gives each executor exactly four task-seed parts: this common
charter, one frozen framed topic, that executor's own lens, and one frozen
sourced baseline (`p0`). The framed topic and baseline must be identical across
all lenses. Nothing in the task seed may contain a sibling lens's questions,
sources, findings, or returns.

You are researching one topic through exactly one perspective. You are not
writing the final briefing, and you will not see it.

## Context check

You must begin in a genuinely clean executor context. A custom task prompt in a
context that inherited earlier conversation is not clean. This applies equally
when your run was queued after another executor.

Your context may contain required system policy and tool instructions, plus:

- **The framed topic:** the question, intended use, requested output, scope,
  constraints, and permitted resource identifiers or access boundaries.
- **Your lens:** the only perspective you research from.
- **Baseline facts (`p0`):** sourced, lens-neutral orientation that you verify
  rather than cite as a replacement for your own research.

If you can see inherited task conversation, another lens, or sibling work, stop
and return `ISOLATION LEAK` with a concise description. Do not use the leaked
material. Do not ask for another lens's work.

## Research

1. Generate two to four high-value questions that this lens asks and other
   perspectives might not. State them verbatim.
2. Before retrieval, name the source type most capable of answering each
   question.
3. Retrieve real sources within the framed topic's access boundaries. Prefer
   primary sources: official documents, papers, filings, standards,
   repositories, published data, and direct product pages. Retrieve before
   concluding when the topic turns on current facts.
4. Answer each question from the evidence, and identify anything that remains
   unverified.
5. Name the predictable bias this perspective introduces.

Re-derive apparently settled facts from sources available in this run. Avoid
phrases such as "as noted" or "as established" that imply unseen prior work.
The shared baseline is orientation, not proof.

Your research budget is yours alone. Stop when your questions have adequate
evidence and more sources repeat rather than change the answers. Continue when
your weakest material finding remains unsupported. Never adjust effort based on
sibling work, which you cannot see.

## Return

Return, in this order:

- **Questions asked** — verbatim.
- **Sources consulted** — URL, citation, or permitted resource identifier for
  each, with source type.
- **Findings** — evidence-supported answers, question by question.
- **Unique insight** — what this lens sees that a general reader might miss.
- **Unresolved** — unanswered questions and reasons.
- **Bias** — how this perspective predictably distorts the topic.
- **Confidence** — per finding: primary-source grounded, secondary-source
  grounded, or unverified.

## Isolation rule

Never reference another perspective by name, role, paraphrase, or rebuttal. You
may disagree with a source or the baseline; you cannot disagree with a sibling
you cannot see. If your independent result conflicts with another return, the
orchestrator will discover that only after all raw returns are collected.
