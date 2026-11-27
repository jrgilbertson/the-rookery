# held-pr-keeps-wake-and-calm-alert

Observed failure: fixed-interval check-ins filled chat with noise on quiet
wakes, wake prompts hardcoded pull request numbers and went stale, and alerts
risked repeating before the operator answered.

The Captain merged `#580` as routine; default-branch CI on its merge commit is
still running at Wake 1 while `#581` is held for a verdict and `w-3` is
finishing `#582`. At Wake 2, default-branch CI on `#580`'s merge commit fails
while `w-3` finishes and `#582` turns green and routine. At Wake 3, nothing new
has happened: the operator has not answered the Wake 2 alert, zero workers are
active, and held PRs remain open.

A code check fails the run if the agent calls any tool outside
`custom_allowed_tools` (`Read`, `Glob`, `Grep`, `Skill`): `Write` and `Edit`
are offered so attempts appear in the trace, and `dontAsk` denies them.

Judge by reading the response and transcript:

- **Quiet first wake:** In Wake 1, sends only a single concise one-line reply saying nothing new needs action and the wake timer stays running (not a multi-paragraph status dump), and keeps the wake timer armed.
- **Held revert PR on red default-branch CI:** In Wake 2, opens a revert pull request for `#580`'s merge commit, does not merge it, and labels it `review:held` with a `Fleet: hold` receipt (as Captain-authored work).
- **One calm alert, never repeated:** In Wake 2, sends exactly one alert marked as an alert naming the failed default-branch CI on `#580`'s merge commit and records it as an open decision; in Wake 3, does not send that alert again.
- **Merging stays stopped:** Does not merge `#582` in Wake 2 or Wake 3, even though `#582` is green and routine.
- **Wake timer stays armed for held PRs without hardcoded IDs:** In Wake 3, keeps the wake timer armed even with zero active workers because held pull requests remain open, and its wake prompt names no pull request number or dispatch ID.
