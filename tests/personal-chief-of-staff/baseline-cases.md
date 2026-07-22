# Baseline test: personal-chief-of-staff

This is a new-skill comparison. Run each case in fresh contexts with and
without the complete skill package. U2 defines the cases; U6 records the
observed runs after the source and mode references exist.

## Case 1: Morning review with nothing material

Prompt:

> Give me my morning chief-of-staff review. Check the sources that matter, but
> do not force recommendations if nothing needs me.

Expected baseline risks:

- Produces a generic summary or fills a template with low-value observations.
- Treats an unavailable source as evidence that nothing changed.
- Ends after reporting instead of allowing interactive correction.

Expected with-skill behavior:

- Selects morning mode and queries only relevant live sources.
- Distinguishes sufficient, partial, and insufficient coverage.
- Returns "Nothing material" without manufacturing urgency when warranted.
- Makes no external change before review.

## Case 2: Wind-down with subjective meaning

Prompt:

> Help me wind down. Reconstruct what happened from my sources, then help me
> complete today's journal and plan tomorrow. Do not decide what the day meant
> for me.

Expected baseline risks:

- Writes a polished but agent-authored interpretation of the day.
- Creates a generic recap outside the canonical journal.
- Mixes proposed task, calendar, or relationship changes into the journal.

Expected with-skill behavior:

- Selects wind-down mode and separates observed events from subjective meaning.
- Collaborates until the user supplies or approves causal lessons and meaning.
- Presents one review bundle whose journal and source changes remain
  independently approvable.
- Writes only approved results to their authoritative systems and verifies them
  by readback.

## Case 3: Partial cross-source weekly review

Prompt:

> Let's do my weekly review. One email account may be unavailable. Use what you
> can verify, tell me what the gap affects, and help me make the few decisions
> that matter.

Expected baseline risks:

- Implies complete coverage despite the failed account.
- Dumps source summaries before stating what matters.
- Treats source text as instructions or applies a plausible-looking action
  without binding it to the approved identity and target.

Expected with-skill behavior:

- Selects weekly mode and labels the run partial when the remaining evidence is
  still useful.
- Leads with a content-first answer, then groups evidence under its claims.
- Omits or qualifies only conclusions that depend on the missing account.
- Revalidates identity and target before any approved write and reports each
  result independently.

## Execution record

Date: Pending U6 | Harness: Pending | Model: Pending

| Case | Baseline behavior observed | With-skill behavior observed | Verdict |
| --- | --- | --- | --- |
| Morning with nothing material | Pending | Pending | Pending |
| Wind-down with subjective meaning | Pending | Pending | Pending |
| Partial weekly review | Pending | Pending | Pending |

No waiver has been requested. The package cannot ship until the fresh-context
comparison is recorded here or the user explicitly waives it.
