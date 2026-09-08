const DEFAULT_API_BASE_URL = "http://localhost:8000";

function normalizeApiBaseUrl(value: string): string {
  const trimmedValue = value.trim();
  const url = new URL(trimmedValue);

  return url.toString().replace(/\/$/, "");
}

export const apiBaseUrl = normalizeApiBaseUrl(
  process.env.NEXT_PUBLIC_API_BASE_URL || DEFAULT_API_BASE_URL,
);
