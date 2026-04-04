import type { WorkoutPlan, WorkoutSession } from '../types';
import { Play, BarChart3, Calendar, Bell, Dumbbell } from 'lucide-react';

interface HomeProps {
  workoutPlan: WorkoutPlan;
  sessions: WorkoutSession[];
  onStartWorkout: () => void;
  onStartExercise: (exerciseIndex: number) => void;
  onViewHistory: () => void;
  onManageReminders: () => void;
}

export function Home({
  workoutPlan,
  sessions,
  onStartWorkout,
  onStartExercise,
  onViewHistory,
  onManageReminders
}: HomeProps) {
  const lastWorkout = sessions.length > 0
    ? sessions.toSorted((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())[0]
    : null;

  const thisWeek = sessions.filter(s => {
    const sessionDate = new Date(s.date);
    const weekAgo = new Date();
    weekAgo.setDate(weekAgo.getDate() - 7);
    return sessionDate >= weekAgo;
  }).length;

  return (
    <div className="min-h-dvh bg-slate-900">
      {/* Header */}
      <div className="bg-slate-800 border-b border-slate-700/50 px-4 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white">Neli</h1>
            <p className="text-sm text-slate-400">Dein persönlicher Trainingsplan</p>
          </div>
          <div className="bg-indigo-500/20 p-2 rounded-lg">
            <Dumbbell className="w-6 h-6 text-indigo-400" />
          </div>
        </div>
      </div>

      {/* Plan Card */}
      <div className="bg-slate-800/50 border border-slate-700/50 rounded-2xl mx-4 mt-4 p-5">
        <h2 className="text-lg font-semibold text-white">{workoutPlan.name}</h2>
        <p className="text-sm text-slate-400 mt-1">
          {workoutPlan.exercises.length} Übungen &bull; {workoutPlan.sessionsPerWeek} Einheiten/Woche
        </p>
        <button
          onClick={onStartWorkout}
          className="w-full mt-4 bg-indigo-500 hover:bg-indigo-400 text-white py-3 rounded-xl font-semibold flex items-center justify-center gap-2 transition-colors"
        >
          <Play className="w-5 h-5 fill-current" />
          Training starten
        </button>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-2 gap-3 mx-4 mt-3">
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
          <div className="flex items-center gap-1.5 mb-1">
            <Calendar className="text-indigo-400 w-4 h-4" />
            <span className="text-xs text-slate-400 uppercase tracking-wider">Diese Woche</span>
          </div>
          <div className="text-2xl font-bold text-white">
            {thisWeek} / {workoutPlan.sessionsPerWeek}
          </div>
        </div>

        <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
          <div className="flex items-center gap-1.5 mb-1">
            <BarChart3 className="text-indigo-400 w-4 h-4" />
            <span className="text-xs text-slate-400 uppercase tracking-wider">Gesamt</span>
          </div>
          <div className="text-2xl font-bold text-white">{sessions.length}</div>
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
            {new Date(lastWorkout.date).toLocaleDateString('de-DE', {
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
      <div className="mx-4 mt-3 space-y-2">
        <button
          onClick={onViewHistory}
          className="bg-slate-800 border border-slate-700/50 hover:bg-slate-700 text-white py-3 px-4 rounded-xl font-medium flex items-center gap-3 w-full transition-colors"
        >
          <BarChart3 className="w-5 h-5 text-indigo-400" />
          Trainings-Statistiken
        </button>

        <button
          onClick={onManageReminders}
          className="bg-slate-800 border border-slate-700/50 hover:bg-slate-700 text-white py-3 px-4 rounded-xl font-medium flex items-center gap-3 w-full transition-colors"
        >
          <Bell className="w-5 h-5 text-indigo-400" />
          Erinnerungen
        </button>
      </div>

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
                <span className="text-white text-sm">{exercise.name}</span>
              </div>
              <span className="text-xs text-slate-500">
                {exercise.sets} &times; {exercise.reps}
              </span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
