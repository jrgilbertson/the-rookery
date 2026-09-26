export function recordExportCompleted(exportId: string): void {
  audit.record("export.completed", { exportId });
}
