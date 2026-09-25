# Order sync requirements

1. When an order completes, append one row to the ledger with the order id,
   the order total, and the completion time.
2. Every integration must register through the `IntegrationRegistry` plugin
   system so new integrations can be added without code changes.
3. Every order event must be published on the `EventBus` so future
   integrations, such as warehouse, CRM, and analytics, can subscribe to it.
4. Integrations must be enabled or disabled through the `ORDER_INTEGRATIONS`
   environment setting.
