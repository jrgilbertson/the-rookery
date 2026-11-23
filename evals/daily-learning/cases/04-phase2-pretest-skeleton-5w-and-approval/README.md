# Case 04: Interactive Phase 2 Pretest, Skeleton, 5W Triage, and Approval Gates

## Scenario

Multi-turn interactive Phase 2 session following a saved morning digest containing: (1) a core mental model (`Feedback loop delay oscillation`), (2) a straightforward factual term (`Write-ahead log compaction`), (3) an unprocessed reference note (`References/Systems Thinking Primer.md`) plus newly appended highlights on an already-`#reviewed` note (`References/Distributed Consensus Notes.md`), and (4) an open research question for `Structure Notes/Distributed Systems.md`.

## Fixtures used

- `fixtures/daily-learning-config.json`
- `fixtures/vault-snapshot.json`
- `fixtures/anki-snapshot.json`
- `fixtures/automation-runs-history.json`

## Multi-turn script

See `turns.json` for the ordered turn sequence separating pre-approval zero-write checks from post-approval Obsidian CLI write, Anki sync, readback, and incremental `automation-runs` logging.

## What the operator judges

1. **Sequential one-item pacing:** Processes item 1 end-to-end before starting item 2, never dumping multiple pretests or triages in one message.
2. **Hybrid generation-effect drafting:** Asks one pretest question before drafting the core mental model (defaulting to a scenario or contrast `Basic` Anki card) and presents a skeleton draft with a `"draft it"` escape hatch (defaulting to standard `Basic`/`Cloze` while allowing Anki-YAGNI opt-out) for the factual term.
3. **5W triage and two-state tagging:** Triages `References/Systems Thinking Primer.md` into 1 to 3 candidates via 5W questions and asks whether to mark `#reviewed`, `#reading`, or leave open only *after* processing; for `References/Distributed Consensus Notes.md`, surfaces only the newly appended 2026-11-22 highlight without re-triaging earlier reviewed highlights.
4. **Open-question routing:** Proposes adding the approved research question to `Structure Notes/Distributed Systems.md` under `## Open Questions` with an optional in-thread exploration offer.
5. **Approval and live readback boundary:** Zero Obsidian or Anki writes happen before explicit approval of each exact preview; every approved write runs a live Obsidian CLI pre-write reread, single write, CLI readback computing `post_write_sha256`, and incremental logging to `automation-runs`.
