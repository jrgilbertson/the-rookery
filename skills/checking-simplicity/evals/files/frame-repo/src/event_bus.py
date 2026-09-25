class EventBus:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, topic, handler):
        self.subscribers.setdefault(topic, []).append(handler)

    def publish(self, topic, payload):
        for handler in self.subscribers.get(topic, []):
            handler(payload)
