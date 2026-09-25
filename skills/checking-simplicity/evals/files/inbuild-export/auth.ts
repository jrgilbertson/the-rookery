export function authorize(canExport: boolean): void {
  if (!canExport) throw new Error("forbidden");
}
