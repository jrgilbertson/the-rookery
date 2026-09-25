from event_bus import EventBus
from ledger_integration import LedgerIntegration
from registry import IntegrationRegistry


def build_bus(settings):
    registry = IntegrationRegistry()
    registry.register("ledger", LedgerIntegration)
    bus = EventBus()
    for integration in registry.enabled(settings):
        integration.attach(bus)
    return bus


def on_order_completed(order, bus):
    bus.publish("order.completed", order)
