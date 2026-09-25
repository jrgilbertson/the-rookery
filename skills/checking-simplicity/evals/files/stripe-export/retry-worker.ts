type Task<T> = () => Promise<T>;

interface RetryWorkerOptions {
  maxRetries: number;
  baseDelayMs: number;
}

interface RetryState {
  attempts: number;
  lastError?: string;
  nextRunAt?: number;
}

const RETRYABLE = new Set(["StripeConnectionError", "StripeRateLimitError", "StripeAPIError"]);

export class RetryWorker {
  private queue: Array<() => Promise<void>> = [];
  private running = false;
  private states = new Map<number, RetryState>();
  private nextId = 1;

  constructor(private options: RetryWorkerOptions) {}

  submit<T>(task: Task<T>): Promise<T> {
    const id = this.nextId++;
    this.states.set(id, { attempts: 0 });
    return new Promise<T>((resolve, reject) => {
      this.queue.push(() => this.attempt(id, task, resolve, reject));
      void this.drain();
    });
  }

  private async drain(): Promise<void> {
    if (this.running) return;
    this.running = true;
    while (this.queue.length > 0) {
      const next = this.queue.shift()!;
      await next();
    }
    this.running = false;
  }

  private async attempt<T>(
    id: number,
    task: Task<T>,
    resolve: (value: T) => void,
    reject: (error: unknown) => void,
  ): Promise<void> {
    const state = this.states.get(id)!;
    state.attempts += 1;
    try {
      resolve(await task());
      this.states.delete(id);
    } catch (error) {
      const type = (error as { type?: string }).type ?? "";
      state.lastError = type;
      if (!RETRYABLE.has(type) || state.attempts > this.options.maxRetries) {
        this.states.delete(id);
        reject(error);
        return;
      }
      const delay = this.options.baseDelayMs * 2 ** (state.attempts - 1) * (0.5 + Math.random());
      state.nextRunAt = Date.now() + delay;
      await new Promise((wait) => setTimeout(wait, delay));
      this.queue.push(() => this.attempt(id, task, resolve, reject));
    }
  }
}
