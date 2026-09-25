import Stripe from "stripe";
import { writeReport } from "../storage";
import { RetryWorker } from "./retry-worker";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);
const worker = new RetryWorker({ maxRetries: 2, baseDelayMs: 500 });

export async function exportPaidInvoices(dayStart: number, dayEnd: number): Promise<void> {
  const rows: string[] = ["invoice_id,customer_id,amount_paid,currency,paid_at"];
  let startingAfter: string | undefined;
  for (;;) {
    const page = await worker.submit(() =>
      stripe.invoices.list({
        status: "paid",
        created: { gte: dayStart, lt: dayEnd },
        limit: 100,
        starting_after: startingAfter,
      }),
    );
    for (const invoice of page.data) {
      rows.push(
        [
          invoice.id,
          invoice.customer,
          invoice.amount_paid,
          invoice.currency,
          invoice.status_transitions.paid_at,
        ].join(","),
      );
    }
    if (!page.has_more) break;
    startingAfter = page.data[page.data.length - 1].id;
  }
  await writeReport(`invoices/${dayStart}.csv`, rows.join("\n"));
}
