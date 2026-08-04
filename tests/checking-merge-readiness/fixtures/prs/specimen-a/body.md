Finance asked for a way to pull the filtered invoices list into a
spreadsheet. This adds an **Export CSV** button to the invoices list page
that downloads the currently filtered rows as a CSV file.

- New endpoint `GET /invoices/export` honoring the same filter query
  parameters as the list endpoint.
- Streaming CSV writer so large result sets do not buffer in memory.
- The button appears only for users carrying the `invoices:read`
  permission the list page already requires.

Out of scope: scheduled exports and XLSX output — tracked separately.
