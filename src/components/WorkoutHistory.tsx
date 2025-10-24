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
    <div className="min-h-screen bg-gradient-to-br from-indigo-100 via-purple-50 to-pink-100">
      {/* Header */}
      <div className="bg-white shadow-md">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <button
            onClick={onClose}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-800 mb-4"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Zurück</span>
          </button>
          <h1 className="text-3xl font-bold text-gray-800">Trainings-Statistiken</h1>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-blue-100 rounded-xl">
                <Dumbbell className="w-8 h-8 text-blue-600" />
              </div>
              <div>
                <div className="text-sm text-gray-600">Gesamt Trainings</div>
                <div className="text-3xl font-bold text-gray-800">{totalWorkouts}</div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-lg p-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-purple-100 rounded-xl">
                <Clock className="w-8 h-8 text-purple-600" />
              </div>
              <div>
                <div className="text-sm text-gray-600">Gesamt Zeit</div>
                <div className="text-3xl font-bold text-gray-800">{totalMinutes} min</div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-lg p-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-green-100 rounded-xl">
                <Calendar className="w-8 h-8 text-green-600" />
              </div>
              <div>
                <div className="text-sm text-gray-600">Diese Woche</div>
                <div className="text-3xl font-bold text-gray-800">{thisWeek} Trainings</div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-lg p-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-orange-100 rounded-xl">
                <TrendingUp className="w-8 h-8 text-orange-600" />
              </div>
              <div>
                <div className="text-sm text-gray-600">Dieser Monat</div>
                <div className="text-3xl font-bold text-gray-800">{thisMonth} Trainings</div>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Sessions */}
        <div className="bg-white rounded-2xl shadow-lg p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Letzte Trainings</h2>
          {sessions.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
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
                    className="flex items-center justify-between p-4 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl border border-indigo-100"
                  >
                    <div>
                      <div className="font-semibold text-gray-800">
                        {session.planName}
                      </div>
                      <div className="text-sm text-gray-600">
                        {new Date(session.date).toLocaleDateString('de-DE', {
                          weekday: 'long',
                          day: '2-digit',
                          month: '2-digit',
                          year: 'numeric'
                        })}
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="font-semibold text-indigo-600">
                        {session.completedExercises} Übungen
                      </div>
                      <div className="text-sm text-gray-600">
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
