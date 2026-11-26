# The review page's data

Read this at the start of step 3: its fields are what step 3 gathers, and
its last section builds the page in step 4. The page is
`assets/review-page.html`. It draws everything from one JSON object that you
write, so this file describes that object and how to fill each part. The
template orders the pull requests, computes products and leverage, draws
every panel, and builds the verdict lines. You supply facts and short text.

Write plain text everywhere. The page shows every value as text, so markup,
Markdown, and HTML entities appear literally. Keep each text field to the
length given; the page is read in one sitting across many pull requests.

## The round

```json
{
  "scope": "8 open pull requests across acme · built from the raw diffs · nothing has been written to GitHub",
  "generated": "Built 2026-11-24 22:40 PST",
  "notices": ["The open list for acme stopped at 1,000 results."],
  "across": [{"label": "Read together", "text": "ledger-app #418 and #421 both change how an upgrade is billed. Merge #421 first.", "refs": ["acme/ledger-app#418", "acme/ledger-app#421"]}],
  "prs": [],
  "inProgress": [],
  "merged": {"window": "", "without": [], "changedAfter": []}
}
```

- `scope`: one line naming the count, the owners, and that nothing has been
  written yet.
- `generated`: when the page was built, in the operator's time zone.
- `notices`: anything that makes the round incomplete, such as a cut-off
  discovery list or a repository that could not be read. Empty when none.
- `across`: notes that span pull requests, each one sentence: two that change
  the same files or behavior with a merge order, or a theme that repeats.
  Label each `Read together`, `Merge order`, or `Repeats`. List in `refs` each
  pull request the note names, as `owner/repo#number`; the page repeats the note
  in those blocks so the operator sees it while deciding.
- `prs`: one entry per held, unclassified, and dependency-bot pull request.
  In-progress ones go in `inProgress`.

## One pull request

```json
{
  "repo": "acme/ledger-app", "number": 421, "url": "https://github.com/acme/ledger-app/pull/421",
  "title": "Fix proration on mid-cycle plan changes",
  "head": "<the reviewed head, all 40 characters>",
  "owner": "owned by repo-captain",
  "status": "checks pass · no conflict",
  "size": {"additions": 19, "deletions": 4, "files": 3},
  "scores": {"impact": 2, "confidence": 2, "verify": 2, "undo": 3},
  "driver": "Changes rounding in billing without saying so. A charge that is wrong stays made after a revert.",
  "sensitiveKind": "money",
  "audience": "customer",
  "ifWrong": "", "proof": "", "asked": "",
  "code": [],
  "read": {"judgment": "", "check": "", "notExamined": ""},
  "feedback": "",
  "rest": ""
}
```

- `owner`: the ownership from step 2 as a short phrase: `owned by <role>`,
  `No owner`, `External fork`, `External contributor`, `Ambiguous owner`,
  `Review only`, or the bot's name.
- `status`: checks and conflict state, plus the base branch when it is not
  the default branch, and a never-carried-out verdict on a held pull request.
- `scores`: integers from 1 to 3, from step 3. Let the page compute the order
  and products. A missing score holds the pull request and sorts it to the top
  of the held group; its V × U shows `?` unless both factors are present.
- `driver`: one or two sentences saying what drives the score, written for
  the overview.
- `sensitiveKind`: each sensitive kind from the first hold test in
  [review-contract.md](review-contract.md) that the pull request touches,
  such as `CI workflow`, `access and authorization`, or `dependency
  lockfile`, as a string or a list of strings. Omit it when none applies.
  The page holds any pull request that sets this field, whatever its scores,
  and displays the kind in both the overview and the block.
- `audience`: who sees the difference: `customer`, `caller`, `operator`, or
  another single noun. The panel reads "What is different for a <audience>".

### What is different

Add one or more of `situations`, `screens`, and `text` to the pull request.
Use `situations` for a change in logic, `screens` for a change on a screen,
both when a pull request changes both, and `text` for a change in wording or
a change with no user-visible effect. Leave out a part that does not apply
rather than writing it empty.

**Situations.** Format the behavioral cases found in step 3 as rows, adding one
unchanged row when it shows the boundary of the change.

```json
"situations": {
  "source": "diff",
  "rows": [
    {"situation": "Switch $10 to $10, mid-cycle", "before": "$0.00", "after": "$0.01", "described": "no"},
    {"situation": "Upgrade on the first day", "before": "full difference", "after": "full difference", "described": "unchanged"}
  ]
}
```

`described` is `yes` when the title, body, or linked issue mentions the case,
`no` when nothing does, and `unchanged` for a boundary row. The page marks
every `no` row in orange, and shows any other value as "Unclear", marked the
same way. Write concrete values, such as amounts, exit codes, or messages,
and keep each cell under about 40 characters.

**Screens.** Before and after, each either a real screenshot or a schematic.

```json
"screens": {
  "before": {"image": "https://user-images.githubusercontent.com/..."},
  "after": {"items": [
    {"kind": "heading", "text": "Choose a plan"},
    {"kind": "row", "items": [
      {"kind": "text", "text": "Pro"},
      {"kind": "badge", "text": "Recommended", "changed": true},
      {"kind": "button", "text": "Choose", "variant": "new", "changed": true}
    ], "split": 2}
  ]},
  "sourceNote": "The pull request links one screenshot that could not be opened.",
  "path": [{"step": "Opens Billing"}, {"step": "Sees the plan cards", "changed": true}, {"step": "Clicks Choose"}],
  "components": [
    {"name": "Button", "status": "dropped"},
    {"name": "UpgradeButton", "status": "added"},
    {"name": "Colors outside the tokens", "status": "added", "note": "New colors", "swatches": ["#7c3aed"]}
  ]
}
```

- `image`: a screenshot attached to the pull request for that side, when one
  shows the reviewed head's version. Use its `https:`
  address on `github.com` or `*.githubusercontent.com`, or a `data:image/...`
  address when you downloaded it. Any other address appears as text.
- `items`: a schematic redrawn from the diff when no screenshot exists. Kinds:
  `heading`, `text`, `badge`, `input`, `image` (a placeholder box), `button`
  with `variant` `primary`, `secondary`, or `new`, and `row`, which holds
  other items and puts the ones from `split` onward on the right. Mark what
  the pull request changed with `"changed": true`. Use `variant: "new"` for a
  button style the design system does not have. Draw only the part of the
  screen the change touches.
- `path`: the steps a user takes through the change, with `changed: true` on
  the step that changed. Leave it out when the change has no path.
- `components`: what the change keeps (`kept`), drops (`dropped`), adds
  (`added`), or changes (`changed`), named as the codebase names them.
  `swatches` takes hex colors only.

The page labels each side as a screenshot or redrawn, so there is no source
field for screens.

**Text.** Either the wording before and after, or `none` saying there is no
user-visible change and what changes instead. The page finds and marks the
words that differ.

```json
"text": {"before": "Thank you for you business.", "after": "Thank you for your business.", "source": "diff"}
"text": {"none": "No user-visible change. Vite's release notes for 6.3.2 list one dev-server fix.", "source": "diff"}
```

### Value sources

Record where `situations` and `text` values came from in `source`:

- `tests`: the pull request's own test or CI output that shows the value.
- `screenshot`: a screenshot attached to the pull request that shows it.
- `diff`: worked out by reading the diff. This is the usual source.

A part with no `source` is labeled as read from the diff. When values in one
table come from different sources, use the weakest one.

### The side panels

Each is one or two sentences. Leave one empty only when there is nothing to
say; the page then shows "Nothing to report."

- `ifWrong`: what a user or the business suffers if the change is wrong, and
  whether a revert undoes it. Name stored or published names here, since a
  revert does not remove them. The panel turns orange when undo cost is 3.
- `proof`: what shows the change works: tests that cover which situations,
  CI, screenshots, and what is not covered. Write `Missing visual evidence`
  when step 3 found it.
- `asked`: whether a linked issue asked for this change, and what in the diff
  it did not ask for. "No linked issue" when there is none.

### Code, read, feedback, and the rest

- `code`: the lines behind each `described: "no"` situation and each
  departure the read names, as a list of excerpts, each
  `{"title": "...", "file": "...", "lines": ["- old", "+ new"]}`. Every entry
  in `lines` is one diff line starting with `+`, `-`, or a space. Keep each
  excerpt to the smallest hunk that shows the cause, at most about 12 lines.
- `read.judgment`: two or three sentences summarizing your step 3 findings on
  coding standards, design system, agent-written code, existing patterns, and
  any steering text quoted from the pull request.
- `read.check`: one thing for the operator to look at personally.
- `read.notExamined`: what you did not read or could not check.
- `feedback`: one line for any open or declined review feedback from step 3,
  with the answer given. Leave it empty when none exists.
- `rest`: one line summarizing the rest of the diff, such as "3 new tests, all
  matching the description."

## Closing rows

```json
"inProgress": [{"repo": "acme/cli-kit", "number": 137, "url": "...", "title": "...", "note": "Owned by repo-captain, checks running."}],
"merged": {
  "window": "The last 7 days, since 2026-11-17 22:40 PST.",
  "without": [{"repo": "...", "number": 412, "url": "...", "title": "...", "reason": "Merged with no verdict and no label."}],
  "changedAfter": [{"repo": "...", "number": 129, "url": "...", "title": "...", "summary": "Two commits after your merge verdict moved the token cache."}]
}
```

- `note`: who is working on it and what it waits on.
- `window`: the window step 1 used, stated so the operator can see it.
- `reason` and `summary`: one sentence each, from step 1's merged list. A pull
  request appears in only one of the two lists.

## Build the page

The template holds the security policy and shows every value as text, so the
data must reach it unchanged. Write the round as JSON to `round.json` in the
round's private directory, then run these commands there, with `<skill-dir>`
replaced by the skill's directory:

```sh
nonce=$(openssl rand -hex 16 2>/dev/null || od -An -N16 -tx1 /dev/urandom | tr -d ' \n')
sed -e 's/&/\\u0026/g' -e 's/</\\u003c/g' -e 's/>/\\u003e/g' round.json > data.json
sed -e "s/{{NONCE}}/$nonce/g" -e '/^{{ROUND_DATA}}$/{' -e 'r data.json' -e 'd' -e '}' <skill-dir>/assets/review-page.html > review.html
chmod 600 review.html
```

The first command escapes every `<`, `>`, and `&`, so no title or body can
close the data block. The second puts the escaped file in place of the
`{{ROUND_DATA}}` line byte for byte. Use these commands for the data every
time: `sed s`, `awk -v`, and file-writing tools can strip or decode the
escapes.

Before handing the page over, check `review.html`: no `{{` is left outside
the data block, the policy's nonce matches the script's, and the data block
is exactly `data.json` and holds no literal `<`. Pull request text can hold
`{{`, such as a workflow's `${{ secrets.TOKEN }}`.
