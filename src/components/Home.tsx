import type { WorkoutPlan, WorkoutSession } from '../types';
import type { Person } from '../lib/auth-service';
import { clearWorkoutProgress, getResumableWorkout } from '../lib/workout-progress';
import { formatAmount } from '../utils/format';
import { isInWeekOf, weekdayIndex } from '../utils/statistics';
import { Play, BarChart3, Calendar, ArrowLeftRight, LogOut, TriangleAlert, ChevronDown, RotateCcw, Check } from 'lucide-react';

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

  return (
    <div className="min-h-dvh bg-slate-900">
      {/* Header */}
      <div className="bg-slate-800 border-b border-slate-700/50 px-4 py-3">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white">{person === 'thomas' ? 'Thomas' : 'Neli'}</h1>
            <p className="text-sm text-slate-400">Dein persönlicher Trainingsplan</p>
          </div>
          <button
            onClick={onLogout}
            className="min-h-11 flex items-center gap-1.5 px-3 rounded-lg text-xs text-slate-400 hover:text-slate-200 hover:bg-slate-700/50 transition-colors"
          >
            <LogOut className="w-4 h-4" />
            Abmelden
          </button>
        </div>
      </div>

      {/* Plan Card */}
      <div className="bg-slate-800/50 border border-slate-700/50 rounded-2xl mx-4 mt-4 p-5">
        <div className="flex items-center justify-between gap-2">
          <h2 className="text-lg font-semibold text-white">{workoutPlan.name}</h2>
          <button
            onClick={onSwitchPlan}
            className="min-h-11 -mr-2 px-3 flex items-center gap-1.5 rounded-lg text-sm text-indigo-400 hover:text-indigo-300 hover:bg-slate-700/40 transition-colors shrink-0"
          >
            <ArrowLeftRight className="w-4 h-4" />
            Wechseln
          </button>
        </div>
        <p className="text-sm text-slate-400 mt-1">
          {workoutPlan.exercises.length} Übungen &bull; {workoutPlan.sessionsPerWeek} Einheiten/Woche
        </p>

        {resumable && (
          <button
            onClick={() => onStartExercise(resumable.exerciseIndex)}
            className="w-full mt-4 bg-emerald-500/15 hover:bg-emerald-500/25 border border-emerald-500/40 text-emerald-300 py-3 px-4 rounded-xl font-semibold flex items-center justify-center gap-2 transition-colors"
          >
            <RotateCcw className="w-5 h-5" />
            Weitermachen bei Übung {resumable.exerciseIndex + 1}/{resumable.totalExercises}
          </button>
        )}

        <button
          onClick={() => {
            // „Neu starten“ verwirft den gespeicherten Stand, sonst würde fortgesetzt
            if (resumable) clearWorkoutProgress(person);
            onStartWorkout();
          }}
          className={`w-full py-3 rounded-xl font-semibold flex items-center justify-center gap-2 transition-colors ${
            resumable
              ? 'mt-3 bg-slate-700 hover:bg-slate-600 text-white'
              : 'mt-4 bg-indigo-500 hover:bg-indigo-400 text-white'
          }`}
        >
          <Play className="w-5 h-5 fill-current" />
          {resumable ? 'Neu starten' : 'Training starten'}
        </button>
      </div>

      {/* Diese Woche (Mo–So) */}
      <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl mx-4 mt-3 p-4">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-1.5">
            <Calendar className="text-indigo-400 w-4 h-4" />
            <span className="text-xs text-slate-400 uppercase tracking-wider">Diese Woche</span>
          </div>
          <span className="text-lg font-bold text-white">
            {weekSessions.length} / {workoutPlan.sessionsPerWeek}
          </span>
        </div>
        <div className="grid grid-cols-7 gap-1">
          {WEEKDAYS.map((label, i) => {
            const done = doneDays.has(i);
            const isToday = i === todayIndex;
            return (
              <div key={label} className="flex flex-col items-center gap-1">
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center ${
                    done
                      ? 'bg-emerald-500 text-white'
                      : isToday
                        ? 'border-2 border-indigo-400'
                        : 'border border-slate-600'
                  }`}
                  aria-label={`${label}${done ? ': erledigt' : ''}`}
                >
                  {done && <Check className="w-4 h-4" strokeWidth={3} />}
                </div>
                <span className={`text-xs ${isToday ? 'text-indigo-300 font-semibold' : 'text-slate-500'}`}>
                  {label}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Last Workout */}
      {lastWorkout && (
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl mx-4 mt-3 p-4">
          <div className="flex items-center gap-2 mb-1">
            <div className="w-2 h-2 rounded-full bg-emerald-500" />
            <span className="text-xs text-slate-400 uppercase tracking-wider">Letztes Training</span>
          </div>
          <p className="text-sm text-slate-300">
            {new Date(lastWorkout.date).toLocaleDateString('de-AT', {
              weekday: 'long',
              day: '2-digit',
              month: '2-digit',
              year: 'numeric'
            })}
            {' '}&bull;{' '}
            {lastWorkout.duration} Minuten
          </p>
        </div>
      )}

      {/* Action Buttons */}
      <div className="mx-4 mt-3">
        <button
          onClick={onViewHistory}
          className="bg-slate-800 border border-slate-700/50 hover:bg-slate-700 text-white py-3 px-4 rounded-xl font-medium flex items-center gap-3 w-full transition-colors"
        >
          <BarChart3 className="w-5 h-5 text-indigo-400" />
          Trainings-Statistiken
          <span className="ml-auto text-sm text-slate-400">{sessions.length} gesamt</span>
        </button>
      </div>

      {/* Plan-Hinweis */}
      {workoutPlan.notice && (
        <details open className="group mx-4 mt-4 rounded-xl border border-amber-500/40 bg-amber-500/10">
          <summary className="min-h-11 flex items-center gap-2 px-4 py-3 cursor-pointer list-none [&::-webkit-details-marker]:hidden">
            <TriangleAlert className="w-5 h-5 text-amber-400 shrink-0" />
            <span className="font-semibold text-amber-200">Wichtiger Hinweis</span>
            <ChevronDown className="w-4 h-4 text-amber-300 ml-auto transition-transform group-open:rotate-180" />
          </summary>
          <p className="px-4 pb-4 text-sm text-amber-100/90 whitespace-pre-line">{workoutPlan.notice}</p>
        </details>
      )}

      {/* Exercise List */}
      <div className="mx-4 mt-4 mb-6">
        <h3 className="text-sm font-medium text-slate-400 uppercase tracking-wider mb-2">Übungen</h3>
        <div className="space-y-1.5">
          {workoutPlan.exercises.map((exercise, index) => (
            <button
              key={exercise.id}
              onClick={() => onStartExercise(index)}
              className="bg-slate-800/30 hover:bg-slate-800 border border-slate-700/30 rounded-lg p-3 flex items-center justify-between w-full transition-colors"
            >
              <div className="flex items-center gap-3">
                <div className="w-7 h-7 bg-indigo-500/20 text-indigo-400 rounded-lg text-sm font-medium flex items-center justify-center">
                  {index + 1}
                </div>
                <span className="text-white text-sm text-left">{exercise.name}</span>
              </div>
              <span className="text-xs text-slate-500 shrink-0 ml-2">
                {exercise.sets} &times; {formatAmount(exercise)}
              </span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
