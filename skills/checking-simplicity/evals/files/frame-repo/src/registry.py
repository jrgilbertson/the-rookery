import os


class IntegrationRegistry:
    def __init__(self):
        self.factories = {}

    def register(self, name, factory):
        self.factories[name] = factory

    def enabled(self, settings):
        names = os.environ.get("ORDER_INTEGRATIONS", "ledger").split(",")
        return [self.factories[name](settings) for name in names if name in self.factories]
