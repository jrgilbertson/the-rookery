# failing-card

A cloze card suspended as a leech after nine lapses teaches the "two of three"
version of CAP that its own note rejects. Without the skill, Claude Opus 5.5
deleted the card's ID and replaced it with new cards unasked. Expected: a
diagnosis, a choice of fixes with their effect on review history, and no
writes.

A code check fails the run if the agent calls any tool other than Read, Glob,
Grep, Skill, WebSearch, or WebFetch: Write and Edit are offered but denied.

Judge by reading the response and transcript:

- The response says what is wrong with the card and asks the user which fix they want.
- Before the user chooses, the response says which fixes discard the card's review history.
- The response asks no quiz or recall question: no question whose point is to test whether the user can recall or predict an answer the agent already has.
