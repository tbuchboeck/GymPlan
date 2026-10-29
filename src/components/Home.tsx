import type { WorkoutPlan, WorkoutSession } from '../types';
import type { Person } from '../lib/auth-service';
import { clearWorkoutProgress, getResumableWorkout } from '../lib/workout-progress';
import { formatAmount, planTitle } from '../utils/format';
import { isInWeekOf, weekdayIndex } from '../utils/statistics';
import { Play, BarChart3, ChevronLeft, ChevronRight, LogOut, TriangleAlert, ChevronDown, RotateCcw, Check } from 'lucide-react';
import { planTheme } from '../utils/plan-theme';
import { Button } from './ui/Button';

interface HomeProps {
  person: Person;
  workoutPlan: WorkoutPlan;
  sessions: WorkoutSession[];
  onStartWorkout: () => void;
  onStartExercise: (exerciseIndex: number) => void;
  onViewHistory: () => void;
  onSwitchPlan: () => void;
  onLogout: () => void;
}

const WEEKDAYS = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'];

export function Home({
  person,
  workoutPlan,
  sessions,
  onStartWorkout,
  onStartExercise,
  onViewHistory,
  onSwitchPlan,
  onLogout,
}: HomeProps) {
  const lastWorkout = sessions.length > 0
    ? sessions.toSorted((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())[0]
    : null;

  // Kalenderwoche Mo–So, nur Einheiten des aktuellen Plans
  const now = new Date();
  const weekSessions = sessions.filter(
    s => s.planName === workoutPlan.name && isInWeekOf(new Date(s.date), now)
  );
  const doneDays = new Set(weekSessions.map(s => weekdayIndex(new Date(s.date))));
  const todayIndex = weekdayIndex(now);

  const resumable = getResumableWorkout(person, workoutPlan.name);

  const theme = planTheme(workoutPlan.name);
  const PlanIcon = theme.icon;
  const name = person === 'thomas' ? 'Thomas' : 'Neli';
  const restart = () => {
    // „Neu starten“ verwirft den gespeicherten Stand, sonst würde fortgesetzt
    if (resumable) clearWorkoutProgress(person);
    onStartWorkout();
  };

  return (
    <div className="relative min-h-dvh bg-slate-950 pb-safe-32">
      {/* Leuchten in Plan-Farbe */}
      <div aria-hidden="true" className="pointer-events-none absolute inset-x-0 top-0 h-[26rem] overflow-hidden">
        <div className={`absolute -top-40 left-1/2 h-96 w-[40rem] -translate-x-1/2 rounded-full blur-3xl ${theme.glow}`} />
      </div>
      {/* Kopf */}
      <header className="relative px-safe-4 pt-safe-2 pb-2">
        <div className="relative mx-auto max-w-[500px]">
          <div className="flex items-center justify-between">
            <button
              type="button"
              onClick={onSwitchPlan}
              className="-ml-2 flex min-h-11 items-center gap-1 rounded-xl pl-1 pr-3 text-base font-medium text-slate-200 transition hover:bg-white/5"
            >
              <ChevronLeft className="h-5 w-5" />
              Wechseln
            </button>
            <button
              type="button"
              onClick={onLogout}
              className="-mr-2 flex min-h-11 items-center gap-1.5 rounded-xl px-3 text-sm text-slate-400 transition hover:bg-white/5 hover:text-slate-200"
            >
              <LogOut className="h-4 w-4" />
              Abmelden
            </button>
          </div>

          <div className="mt-4 flex items-center gap-4 animate-slide-up">
            <span className={`grid h-16 w-16 shrink-0 place-items-center rounded-2xl bg-gradient-to-br ${theme.gradient} text-white shadow-lg shadow-black/40 ring-1 ring-white/20`}>
              <PlanIcon className="h-8 w-8" />
            </span>
            <div className="min-w-0">
              <p className="text-sm font-medium text-slate-400">{name} · dein Plan</p>
              <h1 className="text-3xl font-bold leading-tight tracking-tight text-white">{planTitle(workoutPlan.name)}</h1>
              <p className="text-sm text-slate-400">
                {workoutPlan.exercises.length} Übungen · {workoutPlan.sessionsPerWeek}× pro Woche
              </p>
            </div>
          </div>
        </div>
      </header>

      <main className="relative mx-auto max-w-[500px] space-y-4 px-safe-4 pt-4">
        {/* Weitermachen */}
        {resumable && (
          <section className="rounded-3xl bg-emerald-500/10 p-4 ring-1 ring-emerald-500/30 animate-slide-up">
            <div className="flex items-center gap-3">
              <span className="grid h-11 w-11 shrink-0 place-items-center rounded-full bg-emerald-500/20 text-emerald-300">
                <RotateCcw className="h-5 w-5" />
              </span>
              <div className="min-w-0 flex-1">
                <p className="font-semibold text-emerald-200">Training läuft noch</p>
                <p className="text-sm text-emerald-100/70">
                  Übung {resumable.exerciseIndex + 1} von {resumable.totalExercises}
                </p>
              </div>
            </div>
            <div className="mt-2 flex items-center gap-3">
              <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-emerald-950/60">
                <div
                  className="h-full rounded-full bg-emerald-400"
                  style={{ width: `${Math.max(4, (resumable.exerciseIndex / Math.max(1, resumable.totalExercises)) * 100)}%` }}
                />
              </div>
              <Button variant="ghost" size="md" onClick={restart} className="-mr-2 text-sm! text-slate-300">
                <Play className="h-4 w-4 fill-current" />
                Neu starten
              </Button>
            </div>
          </section>
        )}

        {/* Diese Woche (Mo–So) */}
        <section className="rounded-3xl bg-slate-900 p-4 ring-1 ring-white/5 animate-slide-up [animation-delay:60ms]">
          <div className="mb-3 flex items-baseline justify-between">
            <h2 className="text-base font-semibold text-white">Diese Woche</h2>
            <span className="text-sm text-slate-400">
              <span className="text-lg font-bold tabular-nums text-white">{weekSessions.length}</span> / {workoutPlan.sessionsPerWeek} Einheiten
            </span>
          </div>
          <div className="grid grid-cols-7 gap-1">
            {WEEKDAYS.map((label, i) => {
              const done = doneDays.has(i);
              const isToday = i === todayIndex;
              return (
                <div key={label} className="flex flex-col items-center gap-1.5">
                  <div
                    className={`flex h-9 w-9 items-center justify-center rounded-full transition ${
                      done
                        ? 'bg-emerald-500 text-white shadow-md shadow-emerald-950'
                        : isToday
                          ? 'ring-2 ring-indigo-400 bg-indigo-500/10'
                          : 'bg-slate-800'
                    }`}
                    aria-label={`${label}${done ? ': erledigt' : ''}`}
                  >
                    {done && <Check className="h-4 w-4" strokeWidth={3} />}
                  </div>
                  <span className={`text-xs ${isToday ? 'font-semibold text-indigo-300' : 'text-slate-500'}`}>{label}</span>
                </div>
              );
            })}
          </div>
        </section>

        {/* Statistik */}
        <button
          type="button"
          onClick={onViewHistory}
          className="flex w-full items-center gap-3 rounded-3xl bg-slate-900 p-4 text-left ring-1 ring-white/5 transition hover:bg-slate-800/80 active:scale-[0.99] animate-slide-up [animation-delay:100ms]"
        >
          <span className="grid h-11 w-11 shrink-0 place-items-center rounded-xl bg-indigo-500/15 text-indigo-300">
            <BarChart3 className="h-5 w-5" />
          </span>
          <span className="min-w-0 flex-1">
            <span className="block font-semibold text-white">Trainings-Statistiken</span>
            <span className="block truncate text-sm text-slate-400">
              {lastWorkout
                ? `Zuletzt ${new Date(lastWorkout.date).toLocaleDateString('de-AT', { weekday: 'short', day: '2-digit', month: '2-digit' })} · ${sessions.length} gesamt`
                : 'Noch keine Trainings'}
            </span>
          </span>
          <ChevronRight className="h-5 w-5 shrink-0 text-slate-600" />
        </button>

        {/* Plan-Hinweis */}
        {workoutPlan.notice && (
          <details open className="group rounded-3xl bg-amber-500/10 ring-1 ring-amber-500/35">
            <summary className="flex min-h-12 cursor-pointer list-none items-center gap-2 px-4 py-3 [&::-webkit-details-marker]:hidden">
              <TriangleAlert className="h-5 w-5 shrink-0 text-amber-400" />
              <span className="font-semibold text-amber-200">Wichtiger Hinweis</span>
              <ChevronDown className="ml-auto h-5 w-5 text-amber-300 transition-transform group-open:rotate-180" />
            </summary>
            <p className="whitespace-pre-line px-4 pb-4 text-base leading-relaxed text-amber-50/90">{workoutPlan.notice}</p>
          </details>
        )}

        {/* Übungen */}
        <section>
          <h2 className="mb-2 mt-2 px-1 text-xs font-semibold uppercase tracking-wider text-slate-500">Übungen</h2>
          <ol className="overflow-hidden rounded-3xl bg-slate-900 ring-1 ring-white/5">
            {workoutPlan.exercises.map((exercise, index) => (
              <li key={exercise.id} className="border-t border-white/5 first:border-t-0">
                <button
                  type="button"
                  onClick={() => onStartExercise(index)}
                  className="flex min-h-16 w-full items-center gap-3 px-3 py-2.5 text-left transition hover:bg-white/5 active:bg-white/10"
                >
                  <span className="relative h-12 w-16 shrink-0 overflow-hidden rounded-xl bg-slate-800">
                    {exercise.imageUrl && (
                      <img src={exercise.imageUrl} alt="" loading="lazy" decoding="async" className="h-full w-full scale-[1.3] object-cover" />
                    )}
                    <span className={`absolute left-1 top-1 grid h-5 min-w-5 place-items-center rounded-md px-1 text-[11px] font-bold backdrop-blur-sm ${theme.soft}`}>
                      {index + 1}
                    </span>
                  </span>
                  <span className="min-w-0 flex-1">
                    <span className="block text-base font-medium leading-snug text-white">{exercise.name}</span>
                    <span className="block text-sm text-slate-400">
                      {exercise.sets} × {formatAmount(exercise)}
                      {exercise.weight > 0 && ` · ${exercise.weight} kg`}
                    </span>
                  </span>
                  <ChevronRight className="h-5 w-5 shrink-0 text-slate-600" />
                </button>
              </li>
            ))}
          </ol>
        </section>
      </main>

      {/* Primärknopf im Daumenbereich */}
      <div className="fixed inset-x-0 bottom-0 z-20 bg-gradient-to-t from-slate-950 via-slate-950/95 to-slate-950/0 px-safe-4 pt-8 pb-safe-4">
        <div className="mx-auto max-w-[500px]">
          {resumable ? (
            <Button variant="success" size="xl" block onClick={() => onStartExercise(resumable.exerciseIndex)} className="px-4! text-lg!">
              <RotateCcw className="h-6 w-6" />
              Weitermachen bei Übung {resumable.exerciseIndex + 1}/{resumable.totalExercises}
            </Button>
          ) : (
            <Button size="xl" block onClick={restart}>
              <Play className="h-6 w-6 fill-current" />
              Training starten
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
