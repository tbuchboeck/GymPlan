import type { WorkoutSession } from '../types';
import { Trophy, Clock, Dumbbell, Calendar } from 'lucide-react';

interface WorkoutSummaryProps {
  session: WorkoutSession;
  onClose: () => void;
}

export function WorkoutSummary({ session, onClose }: WorkoutSummaryProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-green-100 via-teal-50 to-blue-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-3xl shadow-2xl max-w-md w-full p-8">
        <div className="text-center mb-8">
          <div className="inline-block p-4 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full mb-4">
            <Trophy className="w-16 h-16 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            Geschafft!
          </h1>
          <p className="text-gray-600">
            Fantastisches Training! Du bist großartig!
          </p>
        </div>

        <div className="space-y-4 mb-8">
          <div className="flex items-center gap-4 p-4 bg-blue-50 rounded-xl">
            <div className="p-3 bg-blue-100 rounded-lg">
              <Dumbbell className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <div className="text-sm text-gray-600">Übungen abgeschlossen</div>
              <div className="text-2xl font-bold text-gray-800">
                {session.completedExercises} / {session.totalExercises}
              </div>
            </div>
          </div>

          <div className="flex items-center gap-4 p-4 bg-purple-50 rounded-xl">
            <div className="p-3 bg-purple-100 rounded-lg">
              <Clock className="w-6 h-6 text-purple-600" />
            </div>
            <div>
              <div className="text-sm text-gray-600">Dauer</div>
              <div className="text-2xl font-bold text-gray-800">
                {session.duration} Minuten
              </div>
            </div>
          </div>

          <div className="flex items-center gap-4 p-4 bg-green-50 rounded-xl">
            <div className="p-3 bg-green-100 rounded-lg">
              <Calendar className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <div className="text-sm text-gray-600">Datum</div>
              <div className="text-lg font-bold text-gray-800">
                {new Date(session.date).toLocaleDateString('de-DE', {
                  day: '2-digit',
                  month: '2-digit',
                  year: 'numeric'
                })}
              </div>
            </div>
          </div>
        </div>

        <button
          onClick={onClose}
          className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white py-4 px-6 rounded-xl font-bold text-lg shadow-lg transition-all"
        >
          Fertig
        </button>
      </div>
    </div>
  );
}
