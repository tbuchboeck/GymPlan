import { useEffect, useState } from 'react';
import { RefreshCw } from 'lucide-react';
import { BUILD_INFO, fetchLatestBuildInfo, formatBuildTime, type BuildInfo } from '../lib/build-info';

/**
 * Zeigt Version, Commit und Deploy-Zeitpunkt der laufenden App. Prüft beim
 * Anzeigen, ob online schon eine neuere Version liegt (PWA-Cache), und bietet
 * dann ein Neu-Laden an.
 */
export function VersionBadge() {
  const [latest, setLatest] = useState<BuildInfo | null>(null);

  useEffect(() => {
    fetchLatestBuildInfo().then(setLatest);
  }, []);

  const outdated = latest !== null && latest.sha !== BUILD_INFO.sha;

  const reload = async () => {
    // Service Worker aktualisieren, damit nicht wieder die alte Version kommt
    try {
      const reg = await navigator.serviceWorker?.getRegistration();
      await reg?.update();
    } catch {
      // ohne Service Worker einfach neu laden
    }
    window.location.reload();
  };

  return (
    <div className="mt-6 text-xs text-slate-400 dark:text-slate-500">
      <div>
        Version {BUILD_INFO.version} · {BUILD_INFO.sha}
      </div>
      <div>Deployt am {formatBuildTime(BUILD_INFO.builtAt)}</div>
      {outdated && (
        <button
          type="button"
          onClick={reload}
          className="mt-3 inline-flex items-center gap-1.5 rounded-lg bg-amber-100 px-3 py-1.5 text-xs font-semibold text-amber-800 transition hover:bg-amber-200"
        >
          <RefreshCw size={14} />
          Neue Version vom {formatBuildTime(latest.builtAt)} – neu laden
        </button>
      )}
    </div>
  );
}
