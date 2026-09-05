# Run comment pairs

`check_run_records.py` exercises the production CLI against a complete opening
and closing comment pair, including a Markdown morning report. It checks exact
closing content, run identity and order, the static issue body, pagination and
counts, foreign and missing authors, malformed records, and absent closure.
Ordinary comments remain advisory. No body projection, event hash, or repair
transaction is required.
