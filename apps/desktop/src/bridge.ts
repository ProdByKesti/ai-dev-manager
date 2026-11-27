import { invoke } from "@tauri-apps/api/core";

const expectedResponse = "Desktop foundation bridge is available.";

export async function readFoundationStatus(): Promise<string> {
  const response = await invoke<unknown>("get_foundation_status");
  if (response !== expectedResponse) {
    throw new Error("Invalid desktop bridge response.");
  }
  return response;
}
