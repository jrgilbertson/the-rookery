from ledger import append_row


class LedgerIntegration:
    def __init__(self, settings):
        self.path = settings["ledger_path"]

    def attach(self, bus):
        bus.subscribe("order.completed", self.handle)

    def handle(self, order):
        append_row(self.path, [order["id"], order["total"], order["completed_at"]])
