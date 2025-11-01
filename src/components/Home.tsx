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
    ? sessions.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())[0]
    : null;

  const thisWeek = sessions.filter(s => {
    const sessionDate = new Date(s.date);
    const weekAgo = new Date();
    weekAgo.setDate(weekAgo.getDate() - 7);
    return sessionDate >= weekAgo;
  }).length;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-indigo-900">
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 shadow-2xl">
        <div className="max-w-4xl mx-auto px-4 py-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-white/20 backdrop-blur-sm rounded-xl">
              <Dumbbell className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-white">GymPlan</h1>
              <p className="text-indigo-100">Dein persönlicher Trainingsplan</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Workout Plan Info */}
        <div className="bg-gradient-to-br from-indigo-600 to-purple-600 rounded-2xl shadow-2xl p-8 text-white mb-6">
          <h2 className="text-2xl font-bold mb-4">{workoutPlan.name}</h2>
          <div className="space-y-2 text-indigo-100 mb-2">
            <p className="text-lg">🔄 Einheiten pro Woche: {workoutPlan.sessionsPerWeek}</p>
            <p className="text-lg">💪 Übungen: {workoutPlan.exercises.length}</p>
          </div>

          <button
            onClick={onStartWorkout}
            className="w-full mt-6 bg-white hover:bg-gray-50 text-indigo-600 py-4 px-6 rounded-xl font-bold text-lg flex items-center justify-center gap-3 transition-colors shadow-lg"
          >
            <Play className="w-6 h-6 fill-current" />
            Training starten
          </button>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="bg-gradient-to-br from-blue-500 to-cyan-600 rounded-xl shadow-2xl p-6">
            <div className="flex items-center gap-3 mb-2">
              <Calendar className="w-5 h-5 text-white" />
              <span className="text-sm text-blue-100">Diese Woche</span>
            </div>
            <div className="text-3xl font-bold text-white">
              {thisWeek} / {workoutPlan.sessionsPerWeek}
            </div>
            <div className="text-sm text-blue-100 mt-1">Trainings</div>
          </div>

          <div className="bg-gradient-to-br from-purple-500 to-pink-600 rounded-xl shadow-2xl p-6">
            <div className="flex items-center gap-3 mb-2">
              <BarChart3 className="w-5 h-5 text-white" />
              <span className="text-sm text-purple-100">Gesamt</span>
            </div>
            <div className="text-3xl font-bold text-white">{sessions.length}</div>
            <div className="text-sm text-purple-100 mt-1">Trainings</div>
          </div>
        </div>

        {/* Last Workout */}
        {lastWorkout && (
          <div className="bg-gradient-to-br from-emerald-500 to-teal-600 rounded-xl shadow-2xl p-6 mb-6">
            <h3 className="font-semibold text-white mb-3">Letztes Training</h3>
            <div className="flex items-center justify-between">
              <div>
                <div className="text-emerald-50">
                  {new Date(lastWorkout.date).toLocaleDateString('de-DE', {
                    weekday: 'long',
                    day: '2-digit',
                    month: '2-digit',
                    year: 'numeric'
                  })}
                </div>
                <div className="text-sm text-emerald-100 mt-1">
                  {lastWorkout.completedExercises} Übungen • {lastWorkout.duration} Minuten
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="space-y-4">
          <button
            onClick={onViewHistory}
            className="w-full bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600 text-white py-4 px-6 rounded-xl font-semibold flex items-center justify-center gap-3 shadow-2xl transition-all transform hover:scale-105"
          >
            <BarChart3 className="w-5 h-5" />
            Trainings-Statistiken
          </button>

          <button
            onClick={onManageReminders}
            className="w-full bg-gradient-to-r from-amber-500 to-yellow-500 hover:from-amber-600 hover:to-yellow-600 text-white py-4 px-6 rounded-xl font-semibold flex items-center justify-center gap-3 shadow-2xl transition-all transform hover:scale-105"
          >
            <Bell className="w-5 h-5" />
            Erinnerungen verwalten
          </button>
        </div>

        {/* Exercises Preview */}
        <div className="bg-gradient-to-br from-slate-700 to-slate-800 rounded-xl shadow-2xl p-6 mt-6 border border-slate-600">
          <h3 className="font-semibold text-white mb-4">Übungen in diesem Plan</h3>
          <p className="text-sm text-slate-300 mb-4">Klicke auf eine Übung, um direkt damit zu starten</p>
          <div className="space-y-2">
            {workoutPlan.exercises.map((exercise, index) => (
              <button
                key={exercise.id}
                onClick={() => onStartExercise(index)}
                className="w-full flex items-center justify-between p-3 bg-gradient-to-r from-slate-600 to-slate-700 rounded-lg hover:from-indigo-600 hover:to-purple-600 transition-all cursor-pointer"
              >
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-purple-600 text-white rounded-full flex items-center justify-center font-semibold shadow-lg">
                    {index + 1}
                  </div>
                  <span className="text-white">{exercise.name}</span>
                </div>
                <div className="text-sm text-slate-300">
                  {exercise.sets} × {exercise.reps}
                </div>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
