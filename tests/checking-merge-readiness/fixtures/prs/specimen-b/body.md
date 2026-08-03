Incident review INC-2107: transient network errors drop webhook
deliveries and partners miss shipment events. The incident action item is
a single automatic retry — a delivery that fails with a transient network
error is retried once after 30 seconds. Metrics from the incident show one
retry recovers about 97% of transient drops.

Out of scope, per the incident review: configurable retry policies,
exponential backoff, dead-letter handling.
