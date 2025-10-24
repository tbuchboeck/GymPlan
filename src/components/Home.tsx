import type { WorkoutPlan, WorkoutSession } from '../types';
import { Play, BarChart3, Calendar, Bell, Dumbbell } from 'lucide-react';

interface HomeProps {
  workoutPlan: WorkoutPlan;
  sessions: WorkoutSession[];
  onStartWorkout: () => void;
  onViewHistory: () => void;
  onManageReminders: () => void;
}

export function Home({
  workoutPlan,
  sessions,
  onStartWorkout,
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
    <div className="min-h-screen bg-gradient-to-br from-indigo-100 via-purple-50 to-pink-100">
      {/* Header */}
      <div className="bg-white shadow-md">
        <div className="max-w-4xl mx-auto px-4 py-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-xl">
              <Dumbbell className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-800">GymPlan</h1>
              <p className="text-gray-600">Dein persönlicher Trainingsplan</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Workout Plan Info */}
        <div className="bg-gradient-to-br from-indigo-600 to-purple-600 rounded-2xl shadow-2xl p-8 text-white mb-6">
          <h2 className="text-2xl font-bold mb-2">{workoutPlan.name}</h2>
          <div className="space-y-1 text-indigo-100">
            <p>🎯 Ziel: {workoutPlan.goal}</p>
            <p>👨‍🏫 Trainer: {workoutPlan.trainer}</p>
            <p>📅 Erstellt am: {workoutPlan.createdAt}</p>
            <p>🔄 Einheiten pro Woche: {workoutPlan.sessionsPerWeek}</p>
            <p>💪 Übungen: {workoutPlan.exercises.length}</p>
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
          <div className="bg-white rounded-xl shadow-md p-6">
            <div className="flex items-center gap-3 mb-2">
              <Calendar className="w-5 h-5 text-indigo-600" />
              <span className="text-sm text-gray-600">Diese Woche</span>
            </div>
            <div className="text-3xl font-bold text-gray-800">
              {thisWeek} / {workoutPlan.sessionsPerWeek}
            </div>
            <div className="text-sm text-gray-500 mt-1">Trainings</div>
          </div>

          <div className="bg-white rounded-xl shadow-md p-6">
            <div className="flex items-center gap-3 mb-2">
              <BarChart3 className="w-5 h-5 text-purple-600" />
              <span className="text-sm text-gray-600">Gesamt</span>
            </div>
            <div className="text-3xl font-bold text-gray-800">{sessions.length}</div>
            <div className="text-sm text-gray-500 mt-1">Trainings</div>
          </div>
        </div>

        {/* Last Workout */}
        {lastWorkout && (
          <div className="bg-white rounded-xl shadow-md p-6 mb-6">
            <h3 className="font-semibold text-gray-800 mb-3">Letztes Training</h3>
            <div className="flex items-center justify-between">
              <div>
                <div className="text-gray-600">
                  {new Date(lastWorkout.date).toLocaleDateString('de-DE', {
                    weekday: 'long',
                    day: '2-digit',
                    month: '2-digit',
                    year: 'numeric'
                  })}
                </div>
                <div className="text-sm text-gray-500 mt-1">
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
            className="w-full bg-white hover:bg-gray-50 text-gray-800 py-4 px-6 rounded-xl font-semibold flex items-center justify-center gap-3 shadow-md transition-colors"
          >
            <BarChart3 className="w-5 h-5" />
            Trainings-Statistiken
          </button>

          <button
            onClick={onManageReminders}
            className="w-full bg-white hover:bg-gray-50 text-gray-800 py-4 px-6 rounded-xl font-semibold flex items-center justify-center gap-3 shadow-md transition-colors"
          >
            <Bell className="w-5 h-5" />
            Erinnerungen verwalten
          </button>
        </div>

        {/* Exercises Preview */}
        <div className="bg-white rounded-xl shadow-md p-6 mt-6">
          <h3 className="font-semibold text-gray-800 mb-4">Übungen in diesem Plan</h3>
          <div className="space-y-2">
            {workoutPlan.exercises.map((exercise, index) => (
              <div
                key={exercise.id}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-indigo-100 text-indigo-600 rounded-full flex items-center justify-center font-semibold">
                    {index + 1}
                  </div>
                  <span className="text-gray-800">{exercise.name}</span>
                </div>
                <div className="text-sm text-gray-600">
                  {exercise.sets} × {exercise.reps}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
