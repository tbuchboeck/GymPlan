import { useMemo, useState } from 'react';
import { Dumbbell, Fingerprint, Key } from 'lucide-react';
import { authService, type Person } from '../lib/auth-service';
import { VersionBadge } from './VersionBadge';

interface AuthScreenProps {
  onUnlock: (person: Person) => void;
}

interface AuthError extends Error {
  kind?: 'network' | 'http';
  status?: number;
}

// Remembers who logged in last on this device so the shared GymPlan install
// (Neli + Thomas) opens on the right person. Defaults to Neli — it's her app.
const PERSON_KEY = 'gym.auth.person';
const PEOPLE: Person[] = ['neli', 'thomas'];
const PERSON_LABEL: Record<Person, string> = { neli: 'Neli', thomas: 'Thomas' };

function loadPerson(): Person {
  try {
    const saved = localStorage.getItem(PERSON_KEY);
    if (saved === 'neli' || saved === 'thomas') return saved;
  } catch {
    // localStorage unavailable (private mode) — fall through to default.
  }
  return 'neli';
}

function savePerson(person: Person): void {
  try {
    localStorage.setItem(PERSON_KEY, person);
  } catch {
    // Best-effort; the in-memory state still drives this session.
  }
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
 *
 * Multi-user: a Neli/Thomas tab selects whose passkey to use. The choice is
 * threaded to the auth service as the `label` and persisted per device.
 */
export function AuthScreen({ onUnlock }: AuthScreenProps) {
  const [person, setPerson] = useState<Person>(loadPerson);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showRecovery, setShowRecovery] = useState(false);
  const [recoveryInput, setRecoveryInput] = useState('');

  const normalized = useMemo(() => normalizeRecoveryCode(recoveryInput), [recoveryInput]);
  const formatted = useMemo(() => formatRecoveryCode(normalized), [normalized]);

  const selectPerson = (next: Person) => {
    if (loading || next === person) return;
    setPerson(next);
    savePerson(next);
    setError('');
  };

  const handleLogin = async () => {
    setError('');
    setLoading(true);
    try {
      await authService.loginWithPasskey(person);
      onUnlock(person);
    } catch (err) {
      const e = err as AuthError;
      console.error('[auth] login error', e);
      if (e.name === 'NotAllowedError') {
        setError('Abgebrochen oder kein Passkey verfügbar.');
      } else if (e.kind === 'network') {
        setError(`Netzwerk-/CORS-Fehler: ${e.message}`);
      } else if (e.status === 404) {
        setError(`Noch kein Passkey für ${PERSON_LABEL[person]} auf diesem Gerät. Recovery-Code verwenden.`);
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
      await authService.consumeRecoveryCode(formatted, person);
      onUnlock(person);
    } catch (err) {
      const e = err as AuthError;
      console.error('[auth] recovery error', e);
      if (e.kind === 'network') {
        setError(`Netzwerk-/CORS-Fehler: ${e.message}`);
      } else if (e.status === 404 || e.status === 410 || e.status === 401) {
        setError('Recovery-Code ungültig, bereits verwendet oder falsche Person.');
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
    <div className="fixed inset-0 z-50 grid place-items-center overflow-y-auto p-4 bg-slate-900">
      <div className="w-full max-w-sm rounded-2xl border border-slate-700/50 bg-slate-800 shadow-2xl p-8 text-center text-slate-100">
        <div className="mx-auto mb-4 grid h-16 w-16 place-items-center rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 text-white">
          <Dumbbell size={32} strokeWidth={2.2} />
        </div>
        <h2 className="mb-1 text-xl font-semibold">GymPlan</h2>
        <p className="mb-4 text-sm text-slate-400">Entsperren</p>

        <div
          role="tablist"
          aria-label="Person auswählen"
          className="mb-5 grid grid-cols-2 gap-1 rounded-xl bg-slate-900/60 border border-slate-700/50 p-1"
        >
          {PEOPLE.map((p) => {
            const active = p === person;
            return (
              <button
                key={p}
                type="button"
                role="tab"
                aria-selected={active}
                onClick={() => selectPerson(p)}
                disabled={loading}
                className={
                  'min-h-11 rounded-lg px-3 py-2 text-sm font-semibold transition disabled:cursor-progress ' +
                  (active
                    ? 'bg-indigo-500 text-white shadow'
                    : 'text-slate-400 hover:text-slate-100')
                }
              >
                {PERSON_LABEL[p]}
              </button>
            );
          })}
        </div>

        {error && (
          <div className="mb-3 rounded-lg border border-rose-500/30 bg-rose-500/10 px-3 py-2 text-sm text-rose-200">
            {error}
          </div>
        )}

        <button
          type="button"
          onClick={handleLogin}
          disabled={loading}
          className="mb-2 flex w-full items-center justify-center gap-2 rounded-xl bg-indigo-500 px-4 py-3 text-base font-semibold text-white transition hover:bg-indigo-400 active:scale-[0.98] disabled:opacity-60 disabled:cursor-progress"
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
            className="mt-2 flex min-h-11 w-full items-center justify-center gap-1.5 rounded-lg px-3 py-2 text-sm text-slate-400 transition hover:text-slate-100 disabled:opacity-60 disabled:cursor-progress"
          >
            <Key size={14} />
            <span>Recovery-Code verwenden</span>
          </button>
        ) : (
          <div className="mt-4 text-left">
            <label htmlFor="recovery-code" className="mb-1 block text-xs font-medium text-slate-300">
              Recovery-Code für {PERSON_LABEL[person]} (5 Gruppen à 5 Zeichen)
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
              className="w-full rounded-lg border border-slate-600 bg-slate-900 px-3 py-2 font-mono text-sm tracking-wider text-slate-100 placeholder-slate-500 focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/30 disabled:opacity-60"
            />
            <div className="mt-1 text-xs text-slate-400">
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
                className="min-h-11 flex-1 rounded-lg border border-slate-600 px-3 py-2 text-sm text-slate-200 transition hover:bg-slate-700 disabled:opacity-60"
              >
                Abbrechen
              </button>
              <button
                type="button"
                onClick={handleRecoverySubmit}
                disabled={loading || normalized.length !== 25}
                className="min-h-11 flex-1 rounded-lg bg-indigo-500 px-3 py-2 text-sm font-semibold text-white transition hover:bg-indigo-400 disabled:opacity-60 disabled:cursor-not-allowed"
              >
                Einlösen
              </button>
            </div>
          </div>
        )}

        {loading && (
          <div
            className="mx-auto mt-4 h-5 w-5 animate-spin rounded-full border-2 border-indigo-400 border-t-transparent"
            aria-hidden="true"
          />
        )}

        <VersionBadge />
      </div>
    </div>
  );
}
