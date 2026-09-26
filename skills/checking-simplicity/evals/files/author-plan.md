# Plan: CSV download for the invoices page

## Goal

Account owners can download the invoices they already see on the invoices
page as one CSV file. The owner asked for this one format only. Invoice lists
stay under 5,000 rows per account, and the page already loads them in one
query through `listInvoices(accountId)`.

## Constraints

- Only account owners may download, using the existing `requireOwner` check.
- The CSV holds the same columns the page shows: number, date, amount, status.

## Steps

1. Add an `ExportFormat` plugin interface and a format registry so CSV, XLSX,
   and PDF writers can be registered later.
2. Implement a `CsvFormat` plugin and register it at startup.
3. Add an `export_jobs` table and a background worker that builds the file
   and stores it in object storage.
4. Add a `GET /exports/:id` status endpoint that the page polls until the job
   finishes, then shows a download link.
5. Add `EXPORT_FORMATS_ENABLED` and `EXPORT_WORKER_CONCURRENCY` environment
   settings.
6. Add a `GET /invoices/export` endpoint that checks `requireOwner`, creates
   the job, and returns its id.
7. Tests for each plugin, the worker, the status endpoint, and the settings.
