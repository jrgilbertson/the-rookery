export const retryPolicy = {
  attempts: Number(process.env.RETRY_ATTEMPTS ?? 2),
  backoff: process.env.RETRY_BACKOFF ?? "linear",
};
