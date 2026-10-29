import { useMemo, useState, type CSSProperties } from 'react';
import { Check, Dumbbell, Fingerprint, Key } from 'lucide-react';
import { Button } from './ui/Button';
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
const PERSON_AVATAR: Record<Person, string> = {
  neli: 'from-fuchsia-500 to-pink-500',
  thomas: 'from-sky-500 to-indigo-500',
};

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
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-950 text-slate-100">
      {/* Hintergrund-Leuchten */}
      <div aria-hidden="true" className="pointer-events-none absolute inset-x-0 top-0 h-[70vh] overflow-hidden">
        <div className="absolute left-1/2 top-[-10%] h-[28rem] w-[28rem] -translate-x-1/2 rounded-full bg-indigo-600/25 blur-3xl animate-glow" />
        <div className="absolute right-[-20%] top-[25%] h-64 w-64 rounded-full bg-violet-600/15 blur-3xl" />
      </div>

      <div className="relative mx-auto flex min-h-full w-full max-w-sm flex-col px-safe-5 pt-safe-10 pb-safe-6">
        <section className="flex flex-1 flex-col items-center justify-center py-6 text-center animate-slide-up">
          <HeroMark />
          <h1 className="mt-7 text-5xl font-extrabold tracking-tight text-white">
            Gym<span className="bg-gradient-to-r from-indigo-300 to-violet-300 bg-clip-text text-transparent">Plan</span>
          </h1>
          <p className="mt-3 text-lg text-slate-300">Schön, dass du da bist.</p>
        </section>

        <section className="animate-slide-up [animation-delay:80ms]">
          <h2 className="mb-3 text-center text-sm font-medium text-slate-400">Wer trainiert heute?</h2>
          <div role="tablist" aria-label="Person auswählen" className="mb-5 grid grid-cols-2 gap-3">
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
                    'relative flex min-h-16 flex-col items-center justify-center gap-2 rounded-2xl px-2 py-3 text-center transition duration-200 active:scale-[0.98] disabled:cursor-progress ' +
                    (active
                      ? 'bg-slate-800 ring-2 ring-indigo-400 shadow-lg shadow-indigo-950/50'
                      : 'bg-slate-900 ring-1 ring-white/5 hover:bg-slate-800/70')
                  }
                >
                  <span
                    aria-hidden="true"
                    className={`relative grid h-11 w-11 shrink-0 place-items-center rounded-full text-lg font-bold transition ${active ? `bg-gradient-to-br text-white ${PERSON_AVATAR[p]}` : 'bg-slate-800 text-slate-400'}`}
                  >
                    {PERSON_LABEL[p][0]}
                    {active && (
                      // Häkchen als Abzeichen am Avatar – kollidiert so nie mit dem Namen
                      <span className="absolute -bottom-0.5 -right-0.5 grid h-5 w-5 place-items-center rounded-full bg-indigo-500 text-white ring-2 ring-slate-800">
                        <Check size={12} strokeWidth={3.5} />
                      </span>
                    )}
                  </span>
                  <span className={`max-w-full break-words text-lg font-semibold leading-tight ${active ? 'text-white' : 'text-slate-400'}`}>{PERSON_LABEL[p]}</span>
                </button>
              );
            })}
          </div>

          {error && (
            <div role="alert" className="mb-4 rounded-2xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-200 animate-fade-in">
              {error}
            </div>
          )}

          {!showRecovery ? (
            <>
              <Button size="xl" block onClick={handleLogin} disabled={loading} className="px-4! text-lg! disabled:cursor-progress">
                {loading ? (
                  <span className="h-6 w-6 animate-spin rounded-full border-2 border-white/80 border-t-transparent" aria-hidden="true" />
                ) : (
                  <Fingerprint size={24} />
                )}
                <span>Mit Fingerabdruck entsperren</span>
              </Button>
              <button
                type="button"
                onClick={() => {
                  setError('');
                  setShowRecovery(true);
                }}
                disabled={loading}
                className="mt-3 flex min-h-12 w-full items-center justify-center gap-2 rounded-xl px-3 text-base text-slate-400 transition hover:text-white disabled:opacity-60 disabled:cursor-progress"
              >
                <Key size={16} />
                <span>Recovery-Code verwenden</span>
              </button>
            </>
          ) : (
            <div className="rounded-3xl bg-slate-900 p-4 ring-1 ring-white/5 animate-scale-in">
              <label htmlFor="recovery-code" className="mb-2 block text-sm font-medium text-slate-300">
                Recovery-Code für {PERSON_LABEL[person]}
                <span className="block text-xs font-normal text-slate-500">5 Gruppen à 5 Zeichen</span>
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
                className="min-h-12 w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 font-mono text-base tracking-normal text-slate-100 placeholder-slate-600 focus:border-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/30 disabled:opacity-60"
              />
              <div className="mt-2 flex items-center gap-2 text-xs text-slate-400">
                <div className="h-1 flex-1 overflow-hidden rounded-full bg-slate-800">
                  <div
                    className={`h-full rounded-full transition-all duration-300 ${normalized.length === 25 ? 'bg-emerald-400' : 'bg-indigo-400'}`}
                    style={{ width: `${Math.min(100, (normalized.length / 25) * 100)}%` }}
                  />
                </div>
                <span className="tabular-nums">{normalized.length} / 25 Zeichen</span>
              </div>
              <div className="mt-4 flex gap-2">
                <Button
                  variant="secondary"
                  size="md"
                  className="flex-1"
                  onClick={() => {
                    setShowRecovery(false);
                    setRecoveryInput('');
                    setError('');
                  }}
                  disabled={loading}
                >
                  Abbrechen
                </Button>
                <Button size="md" className="flex-1" onClick={handleRecoverySubmit} disabled={loading || normalized.length !== 25}>
                  {loading && (
                    <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/80 border-t-transparent" aria-hidden="true" />
                  )}
                  Einlösen
                </Button>
              </div>
            </div>
          )}

          <div className="text-center">
            <VersionBadge />
          </div>
        </section>
      </div>
    </div>
  );
}

const RING_R = 78;
const RING_C = 2 * Math.PI * RING_R;

/** Hero: Fortschrittsring um das App-Zeichen – ruhig, ohne Verspieltheit. */
function HeroMark() {
  return (
    <div className="relative h-44 w-44 animate-float" aria-hidden="true">
      <svg viewBox="0 0 180 180" className="absolute inset-0 h-full w-full">
        <defs>
          <linearGradient id="hero-ring" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stopColor="#818cf8" />
            <stop offset="0.6" stopColor="#a78bfa" />
            <stop offset="1" stopColor="#e879f9" />
          </linearGradient>
        </defs>
        <circle cx="90" cy="90" r={RING_R} fill="none" stroke="#1e293b" strokeWidth="7" />
        <circle
          cx="90"
          cy="90"
          r={RING_R}
          fill="none"
          stroke="url(#hero-ring)"
          strokeWidth="7"
          strokeLinecap="round"
          strokeDasharray={RING_C}
          strokeDashoffset={RING_C * 0.28}
          transform="rotate(-90 90 90)"
          className="animate-ring-draw"
          style={{ '--ring-length': RING_C } as CSSProperties}
        />
        <circle cx="90" cy="90" r="62" fill="none" stroke="#1e293b" strokeWidth="1" strokeDasharray="2 6" />
        <circle cx="168" cy="90" r="4" fill="#4ade80" />
        <circle cx="26" cy="46" r="3" fill="#fbbf24" />
      </svg>
      <div className="absolute inset-0 grid place-items-center">
        <div className="grid h-24 w-24 place-items-center rounded-[1.75rem] bg-gradient-to-br from-indigo-500 to-violet-600 text-white shadow-2xl shadow-indigo-900/60 ring-1 ring-white/20">
          <Dumbbell size={46} strokeWidth={2.2} />
        </div>
      </div>
    </div>
  );
}
