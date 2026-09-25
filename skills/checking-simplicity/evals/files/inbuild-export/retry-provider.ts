import { retryPolicy } from "./retry-config";
import { RetryEngine } from "./retry-engine";

export interface RetryProvider {
  run(operation: () => Promise<void>): Promise<void>;
}

const providers = new Map<string, () => RetryProvider>();
providers.set("default", () => new RetryEngine(retryEvents, retryPolicy));

export function retryProvider(): RetryProvider {
  return providers.get(process.env.RETRY_PROVIDER ?? "default")!();
}
