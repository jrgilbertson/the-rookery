export class RetryEngine {
  constructor(private events: RetryEventBus, private policy: RetryPolicy) {}

  async run(operation: () => Promise<void>): Promise<void> {
    this.events.emit("retry.started");
    for (let attempt = 1; attempt <= this.policy.attempts; attempt += 1) {
      try {
        await operation();
        this.events.emit("retry.completed");
        return;
      } catch (error) {
        if (attempt === this.policy.attempts) throw error;
        this.events.emit("retry.scheduled");
      }
    }
  }
}

class RetryEventBus {
  emit(event: string): void {
    retryEvents.publish(event);
  }
}
