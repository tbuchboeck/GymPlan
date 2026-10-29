import { useEffect, useState } from 'react';
import { RefreshCw } from 'lucide-react';
import { BUILD_INFO, fetchLatestBuildInfo, formatBuildTime, type BuildInfo } from '../lib/build-info';

/**
 * Zeigt Version, Commit und Deploy-Zeitpunkt der laufenden App. Prüft beim
 * Anzeigen, ob online schon eine neuere Version liegt (PWA-Cache), und bietet
 * dann ein Neu-Laden an.
 */
const UPDATE_TRY_KEY = 'gym.updateTry';
const AUTO_UPDATE_KEY = 'gym.autoUpdate';

/** Neue Service-Worker-Version holen und warten, bis sie die Seite übernimmt –
 *  sonst lädt der Browser beim Neuladen wieder die alte Version aus dem Cache. */
async function updateServiceWorker(): Promise<void> {
  const sw = navigator.serviceWorker;
  const reg = await sw?.getRegistration();
  if (!sw || !reg) return;
  const takeover = new Promise<void>((resolve) => {
    sw.addEventListener('controllerchange', () => resolve(), { once: true });
    setTimeout(resolve, 8000);
  });
  await reg.update();
  if (reg.installing || reg.waiting) {
    reg.waiting?.postMessage({ type: 'SKIP_WAITING' });
    await takeover;
  }
}

export function VersionBadge() {
  const [latest, setLatest] = useState<BuildInfo | null>(null);

  useEffect(() => {
    fetchLatestBuildInfo().then((info) => {
      setLatest(info);
      // Neue Version online: einmal pro Version automatisch holen und neu laden,
      // damit niemand auf den Knopf tippen muss. Klappt das nicht, bleibt der Knopf.
      if (!info || info.sha === BUILD_INFO.sha) return;
      try {
        if (sessionStorage.getItem(AUTO_UPDATE_KEY) === info.sha) return;
        sessionStorage.setItem(AUTO_UPDATE_KEY, info.sha);
      } catch {
        return;
      }
      updateServiceWorker()
        .catch(() => {})
        .finally(() => window.location.reload());
    });
  }, []);

  const outdated = latest !== null && latest.sha !== BUILD_INFO.sha;

  const [updating, setUpdating] = useState(false);

  const reload = async () => {
    if (updating || !latest) return;
    setUpdating(true);
    // Hat der normale Weg für genau diese Version schon einmal nicht gereicht,
    // räumen wir Service Worker und Cache komplett ab.
    let hard = false;
    try {
      hard = sessionStorage.getItem(UPDATE_TRY_KEY) === latest.sha;
      sessionStorage.setItem(UPDATE_TRY_KEY, latest.sha);
    } catch {
      // ohne sessionStorage einfach der normale Weg
    }
    try {
      if (hard) {
        const regs = (await navigator.serviceWorker?.getRegistrations()) ?? [];
        await Promise.all(regs.map((r) => r.unregister()));
        const keys = (await caches?.keys()) ?? [];
        await Promise.all(keys.map((k) => caches.delete(k)));
      } else {
        await updateServiceWorker();
      }
    } catch {
      // egal – neu laden hilft trotzdem oft
    }
    window.location.reload();
  };

  return (
    <div className="mt-6 text-xs text-slate-400 dark:text-slate-500">
      <div>
        Version {BUILD_INFO.version} · {BUILD_INFO.sha}
      </div>
      <div>Veröffentlicht am {formatBuildTime(BUILD_INFO.builtAt)}</div>
      {outdated && (
        <button
          type="button"
          onClick={reload}
          disabled={updating}
          className="mt-3 inline-flex items-center gap-1.5 rounded-lg bg-amber-100 px-3 py-1.5 text-xs font-semibold text-amber-800 transition hover:bg-amber-200"
        >
          <RefreshCw size={14} className={updating ? 'animate-spin' : undefined} />
          {updating ? 'Neue Version wird geladen …' : `Neue Version vom ${formatBuildTime(latest.builtAt)} – neu laden`}
        </button>
      )}
    </div>
  );
}
