---
title: "Run blind cross-model grading through each CLI's native JSON schema flag"
date: 2026-09-23
last_updated: 2026-09-23
category: best-practices
module: "creating-portable-skills skill verification"
problem_type: best_practice
component: testing_framework
severity: high
applies_when:
  - "Grading a skill's matched A/B runs with a grader model that differs from the model that wrote the outputs"
  - "Running a coding-agent CLI headless as a grader or as a test target"
  - "Using Grok CLI at high effort on long prompts"
  - "Testing a skill that tells the agent to launch a fresh-context reviewer"
symptoms:
  - "Grok CLI returned an empty answer with stopReason \"cancelled\" after spending nearly all output tokens on reasoning"
  - "A schema-constrained grade came back as invalid JSON with trailing characters"
  - "A test run launched nested agent sessions from the shell and hung until the wall-clock cap"
  - "A machine restart wiped every raw run output kept under /tmp"
tags: [cross-model-grading, blind-grading, structured-output, json-schema, grok-cli, claude-code, codex-cli, isolation, timeouts, skill-evals]
related_components:
  - development_workflow
  - tooling
---

# Run blind cross-model grading through each CLI's native JSON schema flag

## Context

The `creating-portable-skills` baseline protocol asks for an independent
grader in step 3 ("Grade binary") of
`skills/creating-portable-skills/assets/baseline-test-template.md`. One grader scores both variants of a case on a target. When a
second model is available, the grader is a different model from the one that
wrote the outputs. It sees final answers only, with variant names removed.
`tests/README.md` ("Matched comparison") points the repo's suites at that
template.

The issue #134 refresh ran that protocol across two harnesses: Claude Code
2.1.281 with Opus 5.5 at medium effort, and Grok CLI 1.0.41 with Grok 4.7 at
high effort. The two models cross-graded each other. Grok graded the Opus
outputs, and Opus graded the Grok outputs. `tests/creating-portable-skills/log.md`
records the setup in its lead-model round header and the later Sol recovery.

Earlier rounds on the same issue graded with Claude subagents only, and the
log found grader noise, not the skill, behind most flipped verdicts. Outputs
that quoted their run folder's name also leaked the variant to the grader
until packets were scrubbed (session history).

Getting a trustworthy grade out of a headless CLI took more than a prompt.
The CLI flags, field names, and failure modes below were observed on the
versions named above and can change with a CLI release.
Grok often returned no grade at all. Output parsed from prose was fragile. A
test run hung. A restart destroyed the raw outputs. The practice below is what
held up across those failures.

## Guidance

**Constrain every grade with one JSON schema, passed through each CLI's own
flag.** Build one grading packet per case per target: the request the agent
received, the case checklist, and every output under a neutral letter, in
shuffled order. Keep the letter-to-run key in a separate file the grader never
sees. Then give the same packet and the same schema file to whichever CLI
grades:

```bash
# Claude Code grades: the grade lands in the "structured_output" field
claude -p --model claude-opus-5-5 --effort medium --output-format json \
  --json-schema "$(cat grade-schema.json)" \
  --setting-sources project --disable-slash-commands --strict-mcp-config \
  --no-session-persistence --tools "" < packet.txt > grade.json

# Grok CLI grades: the grade lands in the "structuredOutput" field
grok --prompt-file packet.txt -m grok-4.7 --effort high \
  --json-schema "$(cat grade-schema.json)" \
  --no-leader --no-plan --no-subagents --disable-web-search \
  --disallowed-tools "run_terminal_command,read_file,list_dir,grep,write,web_fetch,web_search,spawn_subagent" \
  < /dev/null > grade.json

# Codex CLI grades: the -o file holds the grade object itself
codex exec --output-schema grade-schema.json -o grade.json - < packet.txt
```

The recovery round also exercised Codex CLI 0.155.1 with gpt-6-sol at high
effort. Codex required a strict schema: every object declares
`additionalProperties: false` and lists all its properties as required.
An array of grades with an explicit `letter` field works across the three
CLIs; an object with arbitrary letter keys does not satisfy that contract.
Each grade carries one entry per checklist item and quoted evidence:

```json
{
  "type": "object", "additionalProperties": false, "required": ["grades"],
  "properties": {"grades": {"type": "array", "items": {
    "type": "object", "additionalProperties": false,
    "required": ["letter", "items", "pass"],
    "properties": {
      "letter": {"type": "string"}, "pass": {"type": "boolean"},
      "items": {"type": "array", "items": {
        "type": "object", "additionalProperties": false,
        "required": ["n", "verdict", "evidence"],
        "properties": {
          "n": {"type": "integer"},
          "verdict": {"type": "string", "enum": ["pass", "fail"]},
          "evidence": {"type": "string"}
        }
      }}
    }
  }}}
}
```

Drop any regex that pulls JSON out of prose. Read the structured field.
The earlier object-keyed schema remains historical evidence; use the array
contract above for new cross-CLI runs.

**Validate every grade before counting it.** A schema flag does not guarantee a
valid grade. Check three things against the packet, and treat any failure as
no grade:

1. Output letters are unique and their set equals the letters in the packet key.
2. Each output has exactly one item for every checklist number, with no duplicate
   or missing numbers. An item-count check alone can accept the same item twice.
3. Each output's `pass` flag equals "every item passed".

If the structured field is missing, the CLI reported an error, or a check
fails, rerun that grade. Never record a missing or malformed grade as a pass or
a fail. The log notes these reruns: "One Grok grade returned invalid JSON and
was rerun" (the correction-rerun header in
`tests/creating-portable-skills/log.md`), and "Grok returned no grade on some
calls (empty answer, stopped as cancelled); those calls were rerun and never
counted as verdicts" (the lead-model round header).

**Preserve execution failure separately from artifact validation.** In the
recovery round, the model command failed or produced nothing, but a successful
JSON wrapper replaced its exit status with zero. Claude also returned
`is_error: true` and a session-limit message inside a result marked
`subtype: "success"`. Neither a shell exit nor that subtype proves a usable
answer. Save the model command's exit status before wrapping its output,
reject error or empty answers, and require a validated grade for every expected
packet before declaring a batch complete. Retry missing execution or grading;
do not silently omit it from the denominator. A valid answer that fails the
checklist remains a behavioral failure.

**Keep missing costs missing.** Codex's bare grade object has no price field.
Record `cost not available`; a default of zero falsely claims a free run.
Use reported token counts and wall time to compare those runs.

**Prefer `--prompt-file` plus `--json-schema` for Grok.** In this session's
runs, plain `grok -p` grading of long packets at high effort returned empty
text with `stopReason: "cancelled"` on 4 of 5 calls, with nearly all output
tokens spent on reasoning. Switching to `--prompt-file` with `--json-schema`
returned well-formed grades in `structuredOutput`. It still failed sometimes,
with `structuredOutputError: model output was not valid JSON: trailing
characters` or another cancellation. The validation step above catches both.

**Isolate each run from the operator's own agent setup.** For Grok, start from
an empty environment and a throwaway home that holds only a link to the auth
file:

```bash
mkdir -p ghome/.grok && ln -s ~/.grok/auth.json ghome/.grok/auth.json
env -i PATH=/usr/bin:/bin:/opt/homebrew/bin HOME="$PWD/ghome" \
  GROK_HOME="$PWD/ghome/.grok" TERM=dumb grok inspect
```

In this session, `grok inspect` under that setup showed zero skills, MCP
servers, instructions, and hooks. Two flags behaved against expectation.
`--tools` alone did not remove built-in tools, so name the unwanted ones in
`--disallowed-tools`. `--sandbox read-only` refused to start because
`/var/run/docker.sock` is a symlink on this machine, so the runs went without
it and ran in throwaway projects instead.

For Claude Code, these flags kept user settings, slash commands, MCP servers,
and session history out of a test run:

```bash
claude -p "$PROMPT" --output-format json \
  --setting-sources project --disable-slash-commands --strict-mcp-config \
  --no-session-persistence --tools "Read,Glob,Grep,Bash" \
  --allowedTools "Read,Glob,Grep,Bash" < /dev/null
```

**Put a hard wall-clock limit on every run, and count a timeout as a failure
with no answer.** macOS has no `timeout` binary by default. A Perl alarm works
anywhere Perl does:

```bash
perl -e 'alarm shift; exec @ARGV' 1500 grok -p "$PROMPT" ... --no-subagents
```

**Keep raw runner outputs outside `/tmp`.** A restart cleared `/tmp` during
this work and took every raw output with it. Write run outputs, packets, and
grades to a durable work folder outside the repository.

## Why This Matters

A grade that is missing or malformed looks like a verdict if the harness does
not check it. An empty Grok answer parsed as "no items passed" would have
recorded a false fail. A malformed grade with a wrong item count would have
scored a case against the wrong checklist. The step 3 rule in the baseline
template holds only if every counted verdict came from a complete, well-formed
grade.

One schema across CLIs holds the output contract fixed. The packet,
checklist, and output format stay the same whichever model grades, which reduces extraction differences; grader disagreement can still change
verdicts and must not be mistaken for target behavior. Each CLI names the structured field differently (`structured_output`,
`structuredOutput`, or the `-o` file), and only the reader has to know that.

Isolation matters because the operator's machine carries skills, hooks, and
instructions the test user will not have. A run that loads the operator's
global setup can pass for reasons the skill under test does not supply.

The hard timeout matters because a skill can tell the agent to do something
the harness cannot support. One Grok run had subagents disabled while the skill
told it to use a fresh-context reviewer. It launched nested Grok sessions from
the shell, and those hung until the 25-minute cap
(the suite-round planted-rot-review line for Grok 4.7 in
`tests/creating-portable-skills/log.md`). Counting that run as a fail with
no answer kept the case honest: the log recorded the failure instead of
letting the run quietly drop out of the record.

## When to Apply

- Any matched comparison under the baseline template where a second model
  grades, including issue #165's follow-up rounds and any skill suite in
  `tests/`.
- Any headless use of Grok CLI at high effort with a long prompt, whether it
  grades or is the target.
- Any test run where the skill under test may try to start another agent,
  a reviewer, or a long-lived process.
- Any multi-hour run round whose raw outputs must survive until grading and
  logging finish.

## Examples

**A grade that must be rerun.** Grok returns
`{"stopReason":"cancelled","text":""}` with no `structuredOutput`. The reader
finds no structured grade and exits with the stop reason. The operator reruns
that grade. The case's log line cites the rerun, not a fail.

**A grade that fails validation.** A packet holds outputs A through D, and the
checklist has six items. The grader returns letters A through C, or gives
output B five items, or marks B `"pass": true` while item 4 is `fail`. Each
case is invalid. Rerun the grade rather than editing the verdict by hand.

**A minimal validator.** This reads either CLI's field or a bare `-o` file and
applies all three checks:

```python
import json, re, sys
def grade_obj(path):
    d = json.load(open(path))
    assert not d.get("is_error"), "grader reported an error"
    for k in ("structured_output", "structuredOutput"):
        if isinstance(d.get(k), dict):
            return d[k]["grades"]
    if "grades" in d:
        return d["grades"]
    sys.exit(f"no grade; stopReason={d.get('stopReason') or d.get('subtype')}")

grades = grade_obj("grade.json")
assert len({v["letter"] for v in grades}) == len(grades), "duplicate letters"
g = {v["letter"]: v for v in grades}
key = json.load(open("packet.key.json"))
n = len(re.findall(r"^- \[ \]", open("case.md").read(), re.M))
assert set(g) == set(key), "letters differ from packet"
for L, v in g.items():
    assert sorted(i["n"] for i in v["items"]) == list(range(1, n + 1)), f"{L}: item numbers"
    assert all(i["verdict"] in ("pass", "fail") for i in v["items"]), f"{L}: verdict"
    assert v["pass"] == all(i["verdict"] == "pass" for i in v["items"]), f"{L}: pass flag"
```

**Cross-grading assignment.** With two targets, fix the grader per target for
the whole round: Grok 4.7 grades every Opus case packet, and Opus 5.5 grades
every Grok case packet. Each packet holds both variants of one case on one
target, so one grader scores both halves of the comparison, as step 3
requires. Scrub variant names and project paths from the outputs before they
enter the packet.

## Related

- `docs/solutions/best-practices/independent-fresh-context-review-for-skills.md`:
  who may grade and what counts as evidence. This doc covers running and
  validating the grader.
- `docs/solutions/best-practices/cross-harness-dogfood-testing.md`: proving
  which skill copy loaded in a target run.
- `docs/solutions/workflow-issues/loosening-a-checklist-during-grading-removes-the-check.md`:
  fix a bad item in its own commit, never mid-grading.
