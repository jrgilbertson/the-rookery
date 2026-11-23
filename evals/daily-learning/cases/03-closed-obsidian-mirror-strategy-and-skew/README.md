# Case 03: Closed-Obsidian Mirror-Mapped Strategy, Skew Detection, and Anki Pulse

## Scenario

Obsidian desktop is closed overnight while the vault-owned `personal-chief-of-staff` source map (`System/chief-of-staff-sources.json`) and its `strategy` and `learning` notes live inside `synthetic-vault` with free-text `interface: "host document reader"`. The last 14 daily runs skewed heavily toward engineering (`12/14` runs) while `Strategy/Personal Strategy.md` prioritizes founder proof essays and structured writing. Local AnkiConnect on the isolated loopback endpoint (`http://127.0.0.1:18765`) reports 64 due cards, 31 overdue cards, one newly manually suspended Cloze sibling (`2000000001001`), one newly `leech`-auto-suspended card (`2000000001002`), and one pre-existing orphaned suspended card (`2000000009999`) already in prior `suspended_card_ids`.

## Fixtures used

- `fixtures/daily-learning-config.json`
- `fixtures/personal-chief-of-staff-sources.json`
- `fixtures/vault-snapshot.json`
- `fixtures/sessions-snapshot.json`
- `fixtures/anki-snapshot.json`
- `fixtures/automation-runs-history.json`

## What the operator judges

1. **Overnight mirror-mapped source resolution:** Resolves `System/chief-of-staff-sources.json` and same-vault `strategy`/`learning` notes by `identity == vault.name` from the bare Git mirror via `git show` even though Obsidian is closed and `interface` is not literally `"obsidian-cli"`.
2. **Engineering skew and dynamic focus:** Flags the sustained engineering skew across the 14-run lookback against stated strategic priorities without expecting a hardcoded active structure-notes list.
3. **Evidence discipline:** Separates observed evidence from missing mental models and labels model-only disagreements (such as a remote-worker claim) as `hypothesis to test` rather than `verified error`.
4. **Bounded Anki pulse and delta detection:** Warns gently about the elevated backlog (`64` due / `31` overdue) and suggests deferring new cards without shaming missed days; computes newly suspended cards via set difference against prior `suspended_card_ids` (surfacing `2000000001001` as manual and `2000000001002` as `leech`, while skipping pre-existing `2000000009999` on an active day).
