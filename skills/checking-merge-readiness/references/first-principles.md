# First Principles

> "Simplicity is a choice." Hickey's *Simple Made Easy* (2011) names the
> failure this file guards against: complecting, the braiding together of
> things that could have stayed separate.

The digest's principle-tension drivers cite this file. Each principle below
carries its exact citation and one operational definition: a test the digest
applies to the accumulated review fixes at grading time rather than a summary
of the book. The rubric in risk-rubric.md maps these principles onto driver classes
and grades; this file owns what each principle means and where it comes from.

## 1. Deep-module erosion

Ousterhout, *A Philosophy of Software Design*, 2nd ed. (2021), Ch. 4.

Modules should be deep: a small interface hiding substantial functionality.
Operational test: a fix that widens an interface faster than it grows hidden
functionality damages the design regardless of fixing the flagged issue. When
a review round adds a parameter, an exported helper, a mode flag, or a new
public entry point to close a finding, ask whether the module's interface grew
while what it hides stayed the same.

## 2. Tactical-fix accumulation

Ousterhout, Ch. 2 §2.4 ("complexity is incremental") and Ch. 3 (tactical
versus strategic programming).

Complexity arrives in small doses, each individually defensible. Operational
test: grade the sequence of fixes, not any single diff. Each round's change
may read as reasonable on its own. The question is whether the rounds
together bent the design, special case on special case, each one the fastest
answer to that round's finding rather than the right change to the design.

## 3. Knowledge duplication (DRY)

Hunt & Thomas, *The Pragmatic Programmer*, 20th Anniversary ed. (2019),
Tip 11.

Every piece of knowledge should have one authoritative representation. DRY
and "single source of truth" are one principle under two names, and the
principle is about knowledge, not text. Operational test: flag only when the
same fact or rule now lives in two places, so an edit to one will not reach
the other. Similar-looking blocks that encode independent rules are NOT
violations. That misreading is precisely what produces premature abstraction
under review pressure, and this digest must not repeat it.

## 4. Speculative generality (YAGNI)

Fowler, "Yagni" (martinfowler.com bliki) and *Refactoring*, 2nd ed. (2018),
the "Speculative Generality" smell.

Operational test: an abstraction, configuration knob, or state machine
introduced for a hypothetical case the review raised but the PR does not
need. Review feedback is a common source of hypotheticals ("what if this is
called concurrently", "what about a second provider"), and code grown to
answer them is speculative until something exercises it. Fowler's scope
clarification applies: Yagni is about presumptive features, not about effort
that makes software easier to modify. Refactoring toward changeability is not
a violation; building for an imagined caller is.

## 5. Essential versus accidental complexity

Brooks, "No Silver Bullet" (1986).

Essential complexity lives in the problem; accidental complexity is
self-inflicted by the solution. Operational test: classify each review-driven
change as addressing the problem's real difficulty or adding self-inflicted
machinery. A fix that handles a genuinely hard case earns its weight; a fix
whose weight comes from the shape of earlier fixes is accidental, however
correct. Accidental weight grades through the **complexity accretion** driver
in risk-rubric.md; this section supplies the test, not a fifth driver class.

## Supporting evidence: churn and the cross-round driver

Nagappan & Ball, ICSE 2005 — relative code churn predicts defect density.
High churn during fix cycles correlates with new defects, which is why the
rubric's cross-round fix interaction driver treats repeatedly reworked
regions as risk carriers rather than as settled code.

## A note on the framing

No prior literature names AI-review-induced defensive-complexity creep, the
pattern where each automated review round extracts a little more guarding,
abstraction, or state machinery than the change needs. This skill's framing
establishes the concept rather than citing it; the principles above are the
established canon it composes from.
