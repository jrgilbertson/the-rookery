# Nightly paid-invoice export

- Once a night, export the previous day's paid invoices from Stripe to one
  CSV file in the existing reports bucket, using the installed `stripe` Node
  SDK and `writeReport` from the existing storage module.
- Columns: invoice id, customer id, amount paid, currency, paid at.
- Retry transient Stripe API failures (network errors, rate limiting, and
  server errors) at most twice per request, with backoff between attempts.
- When a request still fails, the run fails and on-call reruns it by hand.
  Restart survival is not required.
- The export runs as one scheduled process. No other code calls the retry
  worker.
