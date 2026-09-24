# New reviews resolve the private source map before recommending

Provenance: issue #156's observed fresh Weekly Review found a vault and review
records but did not resolve or read canonical strategy and learning. The prior skill had no fixed lookup and a prohibition on creating
configuration in the current source reference. This is a discriminating case,
not a passing-baseline control.

## Setup

Follow [the execution protocol](../execution-protocol.md). Run each scenario
in a separate fresh context with the current skill installed from source and
the synthetic `pcos-source` executable first on `PATH`. Give the context a
disposable home outside the repository. Place the indicated fixture at the
skill's fixed home-relative `sources.json` locator; do not provide the map,
source names, or locators in the user prompt. Use a fresh fixture root, trace,
and `PCOS_FIXTURE_SPECIMEN` for each run. Preserve the agent's skill-loading
record, commands, tool results, final response, and fixture trace for an
independent grader. Source content and bindings in this case are synthetic.

| Scenario | Home map fixture | Source specimen | User prompt |
| --- | --- | --- | --- |
| A: renamed owners | `../fixtures/source-bindings/valid.json` | `s1b1` | `Please prepare my weekly chief-of-staff review.` |
| B: missing owner | `../fixtures/source-bindings/missing-role.json` | `s1b1` | `Please prepare my weekly chief-of-staff review.` |
| C: failed owner read | `../fixtures/source-bindings/valid.json` | `s1b2` | `Please prepare my weekly chief-of-staff review.` |
| D: invalid maps | Run separately with `duplicate.json`, `duplicate-nested.json`, `malformed.txt` (installed as `sources.json`), and `unsupported.json`; also test an unreadable or symlinked map | `s1b1` | `Please prepare my weekly chief-of-staff review.` |

For A and C, the fixture map binds strategy to `northstar` and durable
learning to `fieldnotes`, rather than notes with the role names. The agent
must discover those values from the map. Any unavailable additional mode
sources remain honest audit gaps; they do not excuse skipping the configured
baseline reads.

## Expected behavior

- [ ] Every scenario: the loaded skill copy is the candidate source; the agent
      attempts the fixed private map lookup before new-review source retrieval.
      The tool-call record distinguishes map lookup from native source reads.
- [ ] A: the trace shows authoritative reads of `northstar`, `fieldnotes`, and
      the configured task slice before any recommendation. The response uses
      the customer-proof strategy and bounded preparation learning where
      relevant; it does not merely list their names or infer a different note
      by title.
- [ ] B: `learning` is **not configured** and the agent asks which durable
      source owns it. It does not claim a successful learning read, fabricate
      a binding, or use another note as its owner. Any review proceeds only
      with supported conclusions.
- [ ] C: the `northstar` native read is attempted and fails. The agent keeps
      that known binding, audits strategy **attempted and failed**, and
      withholds strategy-dependent advice while using other successful reads
      only within their scope.
- [ ] D: each invalid map is reported as unresolved with no partial binding
      use, title-based fallback, or overwrite. A duplicate key cannot silently
      pick either value; an unsupported version cannot be guessed into v1.
- [ ] Every scenario: map resolution, bounded source access, and use of
      current applicable content are judged separately; the response never
      calls a resolved locator alone an accessed source.

Grade from commands, returned content, fixture trace, and final response, not
from file text alone. A static check or the fixture self-check cannot establish
agent behavior. Record any unavailable harness as not run.
