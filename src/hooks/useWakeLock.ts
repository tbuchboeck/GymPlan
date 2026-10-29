import { useEffect } from 'react';

/** Hält den Bildschirm wach, solange die Komponente gemountet ist. Scheitert still. */
export function useWakeLock(active = true): void {
  useEffect(() => {
    if (!active || typeof navigator === 'undefined' || !('wakeLock' in navigator)) return;

    let sentinel: WakeLockSentinel | null = null;
    let released = false;

    const request = async () => {
      if (released || document.visibilityState !== 'visible') return;
      try {
        const lock = await navigator.wakeLock.request('screen');
        if (released) {
          void lock.release().catch(() => {});
          return;
        }
        sentinel = lock;
      } catch {
        // z. B. Akku-Sparmodus oder nicht erlaubt
      }
    };

    // Das System gibt die Sperre beim Verstecken frei → beim Zurückkommen neu anfordern
    const onVisibility = () => {
      if (document.visibilityState === 'visible' && (!sentinel || sentinel.released)) void request();
    };

    void request();
    document.addEventListener('visibilitychange', onVisibility);
    return () => {
      released = true;
      document.removeEventListener('visibilitychange', onVisibility);
      if (sentinel && !sentinel.released) void sentinel.release().catch(() => {});
      sentinel = null;
    };
  }, [active]);
}
