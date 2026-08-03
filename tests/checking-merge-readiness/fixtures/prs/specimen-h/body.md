Support asked for a once-a-day summary instead of the per-message
notifications, which are the top complaint in the last two quarters of
feedback.

This adds a nightly job that sends one digest email per account, listing the
messages that arrived in the previous day and went unread. One email per
account per day, sent from the existing transactional mailer.

- New `digest` job, scheduled nightly, reusing the existing `Mailer` and the
  unread-message query the inbox page already runs.
- A `daily_digest` opt-in on the account settings row, defaulting off, so
  this rolls out to accounts that ask for it before it becomes the default.

Out of scope: weekly and monthly digests, per-folder digests, and any change
to the existing per-message notifications, which stay on until the digest
proves itself.
