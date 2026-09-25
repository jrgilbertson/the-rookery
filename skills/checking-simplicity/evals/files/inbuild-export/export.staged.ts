import { authorize } from "./auth";
import { recordExportCompleted } from "./audit";
import { retryProvider } from "./retry-provider";

export async function runExport(input: ExportInput): Promise<void> {
  authorize(input.canExport);
  try {
    await retryProvider().run(() => input.writer.write(input.rows));
  } catch {
    throw new Error("export write failed");
  }
  recordExportCompleted(input.exportId);
}
