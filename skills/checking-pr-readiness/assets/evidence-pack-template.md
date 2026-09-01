# Evidence Pack Template

Use this shape as a flexible writing aid, not a fixed form. Fill it at approval
and hand it to the finishing path inside the readout. Its top heading is
`## Evidence pack` so the section nests under a pull request description's own
headings without restructuring them.

```markdown
## Evidence pack

**Recommendation:** approve and proceed / request changes / stop and file
follow-up — <one-sentence cause>.

**Next work:** remaining owner work after this decision. On approve, that
is opening the pull request and babysitting it. Write `none` when nothing
else remains. Do not list unrun code review or simplify as leftover work.

**Coverage close:** gather completed. Every applicable check is verified, not
applicable, or recorded without a receipt. Incomplete gather cannot recommend approve.

**Intent:** <durable source and one-sentence outcome>. When the branch has no
linked issue or ticket, brief, or durable repository plan: comparison
unavailable — <what the branch was meant to do>.

**Learning signal:** captured at <path> / capture planned: <follow-up> / none
because <reason> / override recorded: <the stated reason>.
```

Do not add a line per sweep class. A missing class line is not a missing check
when the coverage close is present. Summarize intent from its durable source.
Omit ignored-plan paths and contents, local-only paths, credentials, and
unnecessary personal data.
