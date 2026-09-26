import { authorize } from "./auth";
import { recordExportCompleted } from "./audit";

export async function runExport(input: ExportInput): Promise<void> {
  authorize(input.canExport);
  try {
    await input.writer.write(input.rows);
  } catch {
    throw new Error("export write failed");
  }
  recordExportCompleted(input.exportId);
}
