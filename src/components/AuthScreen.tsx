import { useMemo, useState } from 'react';
import { Dumbbell, Fingerprint, Key } from 'lucide-react';
import { authService } from '../lib/auth-service';

interface AuthScreenProps {
  onUnlock: () => void;
}

interface AuthError extends Error {
  kind?: 'network' | 'http';
  status?: number;
}

function normalizeRecoveryCode(raw: string): string {
  return raw.toUpperCase().replace(/[^A-Z0-9]/g, '');
}

function formatRecoveryCode(normalized: string): string {
  return normalized.match(/.{1,5}/g)?.join('-') ?? normalized;
}

/**
 * AuthScreen — replaces PinLogin. Gates the app behind a WebAuthn passkey
 * served by auth.apps.buchboeck.at. Two paths:
 *   - "Mit Fingerabdruck entsperren" — uses an existing passkey
 *   - "Recovery-Code verwenden" — bootstraps a new passkey on this device
 *
 * No PIN UI — GymPlan joins the per-app passkey rollout (Plan D).
 */
export function AuthScreen({ onUnlock }: AuthScreenProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showRecovery, setShowRecovery] = useState(false);
  const [recoveryInput, setRecoveryInput] = useState('');

  const normalized = useMemo(() => normalizeRecoveryCode(recoveryInput), [recoveryInput]);
  const formatted = useMemo(() => formatRecoveryCode(normalized), [normalized]);

  const handleLogin = async () => {
    setError('');
    setLoading(true);
    try {
      await authService.loginWithPasskey();
      onUnlock();
    } catch (err) {
      const e = err as AuthError;
      console.error('[auth] login error', e);
      if (e.name === 'NotAllowedError') {
        setError('Abgebrochen oder kein Passkey verfügbar.');
      } else if (e.kind === 'network') {
        setError(`Netzwerk-/CORS-Fehler: ${e.message}`);
      } else if (e.status === 404) {
        setError('Noch kein Passkey für dieses Gerät. Recovery-Code verwenden.');
      } else {
        setError(`Login fehlgeschlagen: ${e.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleRecoverySubmit = async () => {
    if (normalized.length !== 25) {
      setError(`Code muss 25 Zeichen haben (aktuell ${normalized.length}).`);
      return;
    }
    setError('');
    setLoading(true);
    try {
      await authService.consumeRecoveryCode(formatted);
      onUnlock();
    } catch (err) {
      const e = err as AuthError;
      console.error('[auth] recovery error', e);
      if (e.kind === 'network') {
        setError(`Netzwerk-/CORS-Fehler: ${e.message}`);
      } else if (e.status === 404 || e.status === 410) {
        setError('Recovery-Code ungültig oder bereits verwendet.');
      } else if (e.name === 'NotAllowedError') {
        setError('Passkey-Erstellung abgebrochen.');
      } else {
        setError(`Recovery fehlgeschlagen: ${e.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 grid place-items-center p-6 bg-gradient-to-br from-pink-300 via-rose-300 to-amber-200">
      <div className="w-full max-w-sm rounded-2xl bg-white/96 dark:bg-slate-800 shadow-2xl p-8 text-center text-slate-900 dark:text-slate-100">
        <div className="mx-auto mb-4 grid h-16 w-16 place-items-center rounded-full bg-gradient-to-br from-pink-500 to-rose-400 text-white">
          <Dumbbell size={32} strokeWidth={2.2} />
        </div>
        <h2 className="mb-1 text-xl font-semibold">GymPlan</h2>
        <p className="mb-5 text-sm text-slate-500 dark:text-slate-400">Entsperren</p>

        {error && (
          <div className="mb-3 rounded-lg bg-rose-100 dark:bg-rose-900/40 px-3 py-2 text-sm text-rose-700 dark:text-rose-200">
            {error}
          </div>
        )}

        <button
          type="button"
          onClick={handleLogin}
          disabled={loading}
          className="mb-2 flex w-full items-center justify-center gap-2 rounded-xl bg-pink-500 px-4 py-3 text-base font-semibold text-white transition hover:bg-pink-600 active:scale-[0.98] disabled:opacity-60 disabled:cursor-progress"
        >
          <Fingerprint size={18} />
          <span>Mit Fingerabdruck entsperren</span>
        </button>

        {!showRecovery ? (
          <button
            type="button"
            onClick={() => {
              setError('');
              setShowRecovery(true);
            }}
            disabled={loading}
            className="mt-2 flex w-full items-center justify-center gap-1.5 rounded-lg px-3 py-2 text-sm text-slate-500 dark:text-slate-400 transition hover:text-slate-900 dark:hover:text-slate-100 disabled:opacity-60 disabled:cursor-progress"
          >
            <Key size={14} />
            <span>Recovery-Code verwenden</span>
          </button>
        ) : (
          <div className="mt-4 text-left">
            <label htmlFor="recovery-code" className="mb-1 block text-xs font-medium text-slate-600 dark:text-slate-300">
              Recovery-Code (5 Gruppen à 5 Zeichen)
            </label>
            <input
              id="recovery-code"
              type="text"
              inputMode="text"
              autoComplete="off"
              autoCorrect="off"
              autoCapitalize="characters"
              spellCheck={false}
              value={formatted}
              onChange={(e) => setRecoveryInput(e.target.value)}
              placeholder="ABCDE-FGHIJ-KLMNO-PQRST-UVWXY"
              disabled={loading}
              className="w-full rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 px-3 py-2 font-mono text-sm tracking-wider text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:border-pink-500 focus:outline-none focus:ring-2 focus:ring-pink-500/30 disabled:opacity-60"
            />
            <div className="mt-1 text-xs text-slate-500 dark:text-slate-400">
              {normalized.length} / 25 Zeichen
            </div>
            <div className="mt-3 flex gap-2">
              <button
                type="button"
                onClick={() => {
                  setShowRecovery(false);
                  setRecoveryInput('');
                  setError('');
                }}
                disabled={loading}
                className="flex-1 rounded-lg border border-slate-300 dark:border-slate-600 px-3 py-2 text-sm text-slate-700 dark:text-slate-200 transition hover:bg-slate-100 dark:hover:bg-slate-700 disabled:opacity-60"
              >
                Abbrechen
              </button>
              <button
                type="button"
                onClick={handleRecoverySubmit}
                disabled={loading || normalized.length !== 25}
                className="flex-1 rounded-lg bg-pink-500 px-3 py-2 text-sm font-semibold text-white transition hover:bg-pink-600 disabled:opacity-60 disabled:cursor-not-allowed"
              >
                Einlösen
              </button>
            </div>
          </div>
        )}

        {loading && (
          <div
            className="mx-auto mt-4 h-5 w-5 animate-spin rounded-full border-2 border-pink-500 border-t-transparent"
            aria-hidden="true"
          />
        )}
      </div>
    </div>
  );
}
