export async function saveAttempt(exportId: string, attempt: number) {
  await stateStore.put(`export:${exportId}`, { attempt });
}
