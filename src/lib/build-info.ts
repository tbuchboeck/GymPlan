export interface BuildInfo {
  version: string;
  sha: string;
  builtAt: string; // ISO
}

export const BUILD_INFO: BuildInfo = __BUILD_INFO__;

/** z. B. "29.10.2026, 04:05" in österreichischer Zeit. */
export function formatBuildTime(iso: string): string {
  return new Date(iso).toLocaleString('de-AT', {
    timeZone: 'Europe/Vienna',
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

/** Holt die Build-Info der aktuell online liegenden Version (am Cache vorbei).
 *  null, wenn offline oder im Dev-Server (dort gibt es keine version.json). */
export async function fetchLatestBuildInfo(): Promise<BuildInfo | null> {
  try {
    const res = await fetch(`/version.json?t=${Date.now()}`, { cache: 'no-store' });
    if (!res.ok) return null;
    const data = (await res.json()) as BuildInfo;
    return typeof data.sha === 'string' ? data : null;
  } catch {
    return null;
  }
}
