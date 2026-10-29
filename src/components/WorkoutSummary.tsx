import { useState } from 'react';
import type { Feeling, WorkoutSession } from '../types';
import type { Person } from '../lib/auth-service';
import { Trophy, Clock, Dumbbell, Calendar, AlertTriangle, Check } from 'lucide-react';
import { hasFeelingCheck } from '../utils/physio-report';

interface WorkoutSummaryProps {
  session: WorkoutSession;
  onClose: () => void;
  person?: Person;
  // Aktualisiert die bereits gespeicherte Session (Befinden, Kribbeln)
  onUpdateSession?: (session: WorkoutSession) => void;
}

const FEELING_OPTIONS: { value: Feeling; label: string; active: string }[] = [
  { value: 'better', label: 'Besser', active: 'bg-emerald-500 border-emerald-400 text-white' },
  { value: 'same', label: 'Gleich', active: 'bg-slate-500 border-slate-400 text-white' },
  { value: 'worse', label: 'Schlechter', active: 'bg-rose-500 border-rose-400 text-white' },
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

  return (
    <div className="min-h-dvh bg-slate-900 flex items-center justify-center p-4">
      <div className="bg-slate-800/50 border border-slate-700/50 rounded-2xl max-w-sm w-full p-8 animate-fade-in">
        <div className="text-center">
          <div className="bg-amber-500/20 p-4 rounded-2xl inline-flex">
            <Trophy className="w-12 h-12 text-amber-400" />
          </div>
          <h1 className="text-3xl font-bold text-white mt-4">Geschafft!</h1>
          <p className="text-slate-400 mt-1">Fantastisches Training!</p>
        </div>

        <div className="space-y-3 mt-6">
          <div className="flex items-center gap-3 p-3 bg-slate-800 rounded-xl">
            <Dumbbell className="w-5 h-5 text-indigo-400" />
            <span className="text-sm text-slate-400">Übungen</span>
            <span className="text-lg font-semibold text-white ml-auto">
              {session.completedExercises} / {session.totalExercises}
            </span>
          </div>

          <div className="flex items-center gap-3 p-3 bg-slate-800 rounded-xl">
            <Clock className="w-5 h-5 text-indigo-400" />
            <span className="text-sm text-slate-400">Dauer</span>
            <span className="text-lg font-semibold text-white ml-auto">
              {session.duration} Min
            </span>
          </div>

          <div className="flex items-center gap-3 p-3 bg-slate-800 rounded-xl">
            <Calendar className="w-5 h-5 text-indigo-400" />
            <span className="text-sm text-slate-400">Datum</span>
            <span className="text-lg font-semibold text-white ml-auto">
              {new Date(session.date).toLocaleDateString('de-DE', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric'
              })}
            </span>
          </div>

          {aborted.length > 0 && (
            <div className="p-3 bg-amber-500/10 border border-amber-500/30 rounded-xl">
              <div className="flex items-center gap-2 text-amber-300 text-sm font-semibold">
                <AlertTriangle className="w-4 h-4" />
                Wegen Kribbeln abgebrochen
              </div>
              <ul className="mt-2 space-y-1 text-sm text-slate-200">
                {aborted.map((name, i) => (
                  <li key={`${name}-${i}`}>• {name}</li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {askFeeling && (
          <div className="mt-6">
            <h2 className="text-base font-semibold text-white">Wie geht es dir jetzt?</h2>
            <p className="text-xs text-slate-500 mb-3">Freiwillig – einfach überspringen, wenn du nichts angeben willst.</p>
            <div className="grid grid-cols-3 gap-2">
              {FEELING_OPTIONS.map((opt) => {
                const selected = feeling === opt.value;
                return (
                  <button
                    key={opt.value}
                    onClick={() => update({ feeling: opt.value })}
                    aria-pressed={selected}
                    className={`py-4 rounded-xl border text-sm font-semibold transition-colors ${
                      selected ? opt.active : 'bg-slate-800 border-slate-700 text-slate-300 hover:bg-slate-700'
                    }`}
                  >
                    {opt.label}
                  </button>
                );
              })}
            </div>

            <div className="mt-4 p-3 bg-slate-800 rounded-xl">
              <div className="text-sm text-slate-300 mb-2">Kribbeln/Ziehen im Arm?</div>
              <div className="grid grid-cols-2 gap-2">
                {([true, false] as const).map((value) => {
                  const selected = tingling === value;
                  return (
                    <button
                      key={String(value)}
                      onClick={() => update({ tingling: value })}
                      aria-pressed={selected}
                      className={`py-3 rounded-lg border text-sm font-semibold transition-colors ${
                        selected
                          ? value
                            ? 'bg-amber-500 border-amber-400 text-white'
                            : 'bg-indigo-500 border-indigo-400 text-white'
                          : 'bg-slate-900/50 border-slate-700 text-slate-300 hover:bg-slate-700'
                      }`}
                    >
                      {value ? 'Ja' : 'Nein'}
                    </button>
                  );
                })}
              </div>
            </div>

            {(feeling || typeof tingling === 'boolean') && (
              <p className="flex items-center gap-1 text-xs text-emerald-300 mt-2" role="status">
                <Check className="w-3 h-3" /> Gespeichert
              </p>
            )}
          </div>
        )}

        <button
          onClick={onClose}
          className="w-full mt-6 bg-indigo-500 hover:bg-indigo-400 text-white py-3 rounded-xl font-semibold transition-colors"
        >
          {askFeeling && !feeling && typeof tingling !== 'boolean' ? 'Überspringen & fertig' : 'Fertig'}
        </button>
      </div>
    </div>
  );
}
