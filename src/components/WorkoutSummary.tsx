import { useState } from 'react';
import type { Feeling, WorkoutSession } from '../types';
import type { Person } from '../lib/auth-service';
import type { LucideIcon } from 'lucide-react';
import { Trophy, Clock, Dumbbell, Calendar, AlertTriangle, Check, Smile, Meh, Frown } from 'lucide-react';
import { planTitle } from '../utils/format';
import { Button } from './ui/Button';
import { hasFeelingCheck } from '../utils/physio-report';

interface WorkoutSummaryProps {
  session: WorkoutSession;
  onClose: () => void;
  person?: Person;
  // Aktualisiert die bereits gespeicherte Session (Befinden, Kribbeln)
  onUpdateSession?: (session: WorkoutSession) => void;
}

const FEELING_OPTIONS: { value: Feeling; label: string; icon: LucideIcon; active: string }[] = [
  { value: 'better', label: 'Besser', icon: Smile, active: 'bg-emerald-500 text-white ring-emerald-300 shadow-lg shadow-emerald-950' },
  { value: 'same', label: 'Gleich', icon: Meh, active: 'bg-slate-500 text-white ring-slate-300' },
  { value: 'worse', label: 'Schlechter', icon: Frown, active: 'bg-rose-500 text-white ring-rose-300 shadow-lg shadow-rose-950' },
];

export function WorkoutSummary({ session, onClose, person, onUpdateSession }: WorkoutSummaryProps) {
  const [feeling, setFeeling] = useState<Feeling | undefined>(session.feeling);
  const [tingling, setTingling] = useState<boolean | undefined>(session.tingling);

  const askFeeling = person === 'thomas' && !!onUpdateSession && hasFeelingCheck(session.planName);
  const aborted = session.abortedExercises ?? [];

  const update = (next: { feeling?: Feeling; tingling?: boolean }) => {
    const nextFeeling = 'feeling' in next ? next.feeling : feeling;
    const nextTingling = 'tingling' in next ? next.tingling : tingling;
    setFeeling(nextFeeling);
    setTingling(nextTingling);
    onUpdateSession?.({
      ...session,
      ...(nextFeeling ? { feeling: nextFeeling } : {}),
      ...(typeof nextTingling === 'boolean' ? { tingling: nextTingling } : {}),
    });
  };

  const stats: { icon: LucideIcon; label: string; value: string }[] = [
    { icon: Dumbbell, label: 'Übungen', value: `${session.completedExercises} / ${session.totalExercises}` },
    { icon: Clock, label: 'Dauer', value: `${session.duration} Min` },
    {
      icon: Calendar,
      label: 'Datum',
      value: new Date(session.date).toLocaleDateString('de-AT', { day: '2-digit', month: '2-digit' }),
    },
  ];

  return (
    <div className="relative flex min-h-dvh flex-col overflow-hidden bg-slate-950 px-safe-4 pt-safe-10 pb-safe-6">
      <div aria-hidden="true" className="pointer-events-none absolute left-1/2 top-[-8rem] h-96 w-[34rem] -translate-x-1/2 rounded-full bg-amber-500/15 blur-3xl" />

      <div className="relative mx-auto flex w-full max-w-sm flex-1 flex-col">
        <div className="text-center animate-scale-in">
          <div className="relative mx-auto h-28 w-28">
            <svg aria-hidden="true" viewBox="0 0 120 120" className="absolute inset-[-1.5rem] h-[calc(100%+3rem)] w-[calc(100%+3rem)]">
              <circle cx="14" cy="30" r="3" fill="#fbbf24" />
              <circle cx="108" cy="22" r="2.5" fill="#4ade80" />
              <circle cx="112" cy="84" r="3" fill="#a78bfa" />
              <circle cx="8" cy="90" r="2" fill="#f472b6" />
              <path d="M100 48l4-4M18 60l-5-2" stroke="#fbbf24" strokeWidth="2.5" strokeLinecap="round" />
            </svg>
            <div className="grid h-full w-full place-items-center rounded-full bg-gradient-to-br from-amber-300 to-orange-500 text-white shadow-2xl shadow-amber-900/50 ring-8 ring-amber-500/15">
              <Trophy className="h-14 w-14" strokeWidth={2} />
            </div>
          </div>
          <h1 className="mt-6 text-4xl font-extrabold tracking-tight text-white">Geschafft!</h1>
          <p className="mt-1 text-lg text-slate-300">Fantastisches Training!</p>
          <p className="text-sm text-slate-500">{planTitle(session.planName)}</p>
        </div>

        <div className="mt-7 grid grid-cols-3 gap-2 animate-slide-up [animation-delay:80ms]">
          {stats.map(({ icon: Icon, label, value }) => (
            <div key={label} className="rounded-2xl bg-slate-900 p-3 text-center ring-1 ring-white/5">
              <Icon className="mx-auto h-5 w-5 text-indigo-300" />
              <div className="mt-1.5 text-xl font-bold tabular-nums text-white">{value}</div>
              <div className="text-xs text-slate-400">{label}</div>
            </div>
          ))}
        </div>

        {aborted.length > 0 && (
          <div className="mt-3 rounded-2xl bg-amber-500/10 p-4 ring-1 ring-amber-500/30">
            <div className="flex items-center gap-2 text-sm font-semibold text-amber-300">
              <AlertTriangle className="h-4 w-4" />
              Wegen Kribbeln abgebrochen
            </div>
            <ul className="mt-2 space-y-1 text-base text-slate-200">
              {aborted.map((name, i) => (
                <li key={`${name}-${i}`}>• {name}</li>
              ))}
            </ul>
          </div>
        )}

        {askFeeling && (
          <section className="mt-6 animate-slide-up [animation-delay:140ms]">
            <h2 className="text-lg font-semibold text-white">Wie geht es dir jetzt?</h2>
            <p className="mb-3 text-sm text-slate-500">Freiwillig – einfach überspringen, wenn du nichts angeben willst.</p>
            <div className="grid grid-cols-3 gap-2">
              {FEELING_OPTIONS.map((opt) => {
                const selected = feeling === opt.value;
                const Icon = opt.icon;
                return (
                  <button
                    key={opt.value}
                    type="button"
                    onClick={() => update({ feeling: opt.value })}
                    aria-pressed={selected}
                    className={`flex min-h-20 flex-col items-center justify-center gap-1 rounded-2xl text-sm font-semibold ring-1 transition duration-200 active:scale-95 ${
                      selected ? `${opt.active} ring-2` : 'bg-slate-900 text-slate-300 ring-white/5 hover:bg-slate-800'
                    }`}
                  >
                    <Icon className="h-7 w-7" />
                    {opt.label}
                  </button>
                );
              })}
            </div>

            <div className="mt-3 rounded-2xl bg-slate-900 p-4 ring-1 ring-white/5">
              <div className="mb-3 text-base text-slate-200">Kribbeln/Ziehen im Arm?</div>
              <div className="grid grid-cols-2 gap-2">
                {([true, false] as const).map((value) => {
                  const selected = tingling === value;
                  return (
                    <button
                      key={String(value)}
                      type="button"
                      onClick={() => update({ tingling: value })}
                      aria-pressed={selected}
                      className={`min-h-12 rounded-xl text-base font-semibold ring-1 transition duration-200 active:scale-95 ${
                        selected
                          ? value
                            ? 'bg-amber-500 text-white ring-amber-300'
                            : 'bg-indigo-500 text-white ring-indigo-300'
                          : 'bg-slate-950/60 text-slate-300 ring-white/10 hover:bg-slate-800'
                      }`}
                    >
                      {value ? 'Ja' : 'Nein'}
                    </button>
                  );
                })}
              </div>
            </div>

            <p
              className={`mt-2 flex items-center gap-1 text-sm text-emerald-300 transition-opacity ${feeling || typeof tingling === 'boolean' ? 'opacity-100' : 'opacity-0'}`}
              role="status"
            >
              {(feeling || typeof tingling === 'boolean') && (
                <>
                  <Check className="h-4 w-4" /> Gespeichert
                </>
              )}
            </p>
          </section>
        )}

        <div className="mt-auto pt-6">
          <Button size="xl" block onClick={onClose}>
            {askFeeling && !feeling && typeof tingling !== 'boolean' ? 'Überspringen & fertig' : 'Fertig'}
          </Button>
        </div>
      </div>
    </div>
  );
}
