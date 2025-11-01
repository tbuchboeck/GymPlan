import type { WorkoutSession } from '../types';
import { Calendar, TrendingUp, Dumbbell, Clock, ArrowLeft } from 'lucide-react';

interface WorkoutHistoryProps {
  sessions: WorkoutSession[];
  onClose: () => void;
}

export function WorkoutHistory({ sessions, onClose }: WorkoutHistoryProps) {
  const totalWorkouts = sessions.length;
  const totalMinutes = sessions.reduce((sum, s) => sum + s.duration, 0);

  const thisWeek = sessions.filter(s => {
    const sessionDate = new Date(s.date);
    const weekAgo = new Date();
    weekAgo.setDate(weekAgo.getDate() - 7);
    return sessionDate >= weekAgo;
  }).length;

  const thisMonth = sessions.filter(s => {
    const sessionDate = new Date(s.date);
    const monthAgo = new Date();
    monthAgo.setMonth(monthAgo.getMonth() - 1);
    return sessionDate >= monthAgo;
  }).length;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-indigo-900">
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 shadow-2xl">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <button
            onClick={onClose}
            className="flex items-center gap-2 text-white hover:text-indigo-100 mb-4 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Zurück</span>
          </button>
          <h1 className="text-3xl font-bold text-white">Trainings-Statistiken</h1>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
          <div className="bg-gradient-to-br from-blue-600 to-cyan-600 rounded-2xl shadow-2xl p-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-white/20 backdrop-blur-sm rounded-xl">
                <Dumbbell className="w-8 h-8 text-white" />
              </div>
              <div>
                <div className="text-sm text-blue-100">Gesamt Trainings</div>
                <div className="text-3xl font-bold text-white">{totalWorkouts}</div>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-purple-600 to-pink-600 rounded-2xl shadow-2xl p-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-white/20 backdrop-blur-sm rounded-xl">
                <Clock className="w-8 h-8 text-white" />
              </div>
              <div>
                <div className="text-sm text-purple-100">Gesamt Zeit</div>
                <div className="text-3xl font-bold text-white">{totalMinutes} min</div>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-emerald-600 to-teal-600 rounded-2xl shadow-2xl p-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-white/20 backdrop-blur-sm rounded-xl">
                <Calendar className="w-8 h-8 text-white" />
              </div>
              <div>
                <div className="text-sm text-emerald-100">Diese Woche</div>
                <div className="text-3xl font-bold text-white">{thisWeek} Trainings</div>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-orange-600 to-red-600 rounded-2xl shadow-2xl p-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-white/20 backdrop-blur-sm rounded-xl">
                <TrendingUp className="w-8 h-8 text-white" />
              </div>
              <div>
                <div className="text-sm text-orange-100">Dieser Monat</div>
                <div className="text-3xl font-bold text-white">{thisMonth} Trainings</div>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Sessions */}
        <div className="bg-gradient-to-br from-slate-700 to-slate-800 rounded-2xl shadow-2xl p-6 border border-slate-600">
          <h2 className="text-xl font-bold text-white mb-4">Letzte Trainings</h2>
          {sessions.length === 0 ? (
            <div className="text-center py-8 text-slate-400">
              Noch keine Trainings absolviert.
              <br />
              Starte dein erstes Training!
            </div>
          ) : (
            <div className="space-y-3">
              {sessions
                .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
                .map((session) => (
                  <div
                    key={session.id}
                    className="flex items-center justify-between p-4 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl border border-indigo-400 shadow-lg hover:from-indigo-500 hover:to-purple-500 transition-all"
                  >
                    <div>
                      <div className="font-semibold text-white">
                        {session.planName}
                      </div>
                      <div className="text-sm text-indigo-100">
                        {new Date(session.date).toLocaleDateString('de-DE', {
                          weekday: 'long',
                          day: '2-digit',
                          month: '2-digit',
                          year: 'numeric'
                        })}
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="font-semibold text-white">
                        {session.completedExercises} Übungen
                      </div>
                      <div className="text-sm text-indigo-200">
                        {session.duration} Minuten
                      </div>
                    </div>
                  </div>
                ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
