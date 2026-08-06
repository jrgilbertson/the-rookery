# Evidence Pack Template

Use this shape as a flexible writing aid, not a fixed form. Fill it at approval
and hand it to the finishing path inside the readout. Its top heading is
`## Evidence pack` so the section nests under a pull request description's own
headings without restructuring them.

```markdown
## Evidence pack

**Plan vs delivered:** delivered — <items>. Not delivered — <items>. When the
branch has no plan or brief: comparison unavailable; attested intent —
<the owner's statement of what the branch was meant to do>.

**Checks:** one line per check, each `<check name>: <status word> — <result>`.
Status words come from the gate's closed set (SKILL.md, Status words). A
verified check names its receipt on its own line.

**Not verified / attested:** the explicit list of checks carrying `not
verified` and the checks carrying `attested`, named individually. An empty list
is written as `none`, never omitted.

**Sweep findings:** one line for every class in `references/sweep-classes.md`,
in that file's order — never a summary line standing in for several. A class
that fired is written `<class>: <verdict> — <disposition>`, where the
disposition is fixed, accepted with reason, or deferred. A class that passed is
written `<class>: <verdict>`. A class whose helper did not run keeps its class
verdict alongside the execution status: `<class>: not run → judgment:
<verdict>` when the fallback judgment ran, and `<class>: unavailable —
<verdict>` when the helper reached an absent-input verdict such as `no
changelog` or `no records`. `<class>: skipped (covered by <gate>)` and
`<class>: not applicable` are the only bare-status forms, because deferral and
inapplicability reach no verdict — a status word never replaces a verdict that
was actually reached. A missing line reads as a class nobody checked.

**Owner decision:** approved / changes requested / stopped and filed follow-up.

**Learning signal:** captured at <path> / capture planned: <follow-up> / none
because <reason> / override recorded: <the owner's stated reason>.

**Design-critique scores:** <score>, <n> P0, <n> P1. When the diff touches
user-interface files and no critique receipt exists, the line carries the
check's status word instead — `not verified`, `skipped (<what was missing>)`,
or `not run` — never a blank. Omit this line only when the diff touches no
user-interface files.
```

Every line above stays in the pack except the design-critique line, which is
omitted on diffs that touch no user-interface files. A check with nothing to
report keeps its line and carries `not applicable`, because a dropped line
reads as a pass.
