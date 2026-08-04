Tax was rounded per line item and then summed, so multi-line invoices
could disagree with the tax authority's invoice-level calculation by a
cent or two. This sums unrounded line tax and rounds once at the invoice
level, with a backfill migration recomputing stored totals.
