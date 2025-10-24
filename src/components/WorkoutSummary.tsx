import type { WorkoutSession } from '../types';
import { Trophy, Clock, Dumbbell, Calendar } from 'lucide-react';

interface WorkoutSummaryProps {
  session: WorkoutSession;
  onClose: () => void;
}

export function WorkoutSummary({ session, onClose }: WorkoutSummaryProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-indigo-900 flex items-center justify-center p-4">
      <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-3xl shadow-2xl max-w-md w-full p-8 border-2 border-yellow-500 animate-pulse-slow">
        <div className="text-center mb-8">
          <div className="inline-block p-6 bg-gradient-to-br from-yellow-400 via-orange-500 to-red-500 rounded-full mb-6 animate-bounce-slow shadow-2xl">
            <Trophy className="w-20 h-20 text-white" />
          </div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-yellow-400 to-orange-500 bg-clip-text text-transparent mb-3">
            Geschafft!
          </h1>
          <p className="text-xl text-slate-200">
            Fantastisches Training! Du bist großartig!
          </p>
        </div>

        <div className="space-y-4 mb-8">
          <div className="flex items-center gap-4 p-5 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-xl shadow-lg transform hover:scale-105 transition-all">
            <div className="p-3 bg-white/20 backdrop-blur-sm rounded-lg">
              <Dumbbell className="w-7 h-7 text-white" />
            </div>
            <div>
              <div className="text-sm text-blue-100">Übungen abgeschlossen</div>
              <div className="text-3xl font-bold text-white">
                {session.completedExercises} / {session.totalExercises}
              </div>
            </div>
          </div>

          <div className="flex items-center gap-4 p-5 bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl shadow-lg transform hover:scale-105 transition-all">
            <div className="p-3 bg-white/20 backdrop-blur-sm rounded-lg">
              <Clock className="w-7 h-7 text-white" />
            </div>
            <div>
              <div className="text-sm text-purple-100">Dauer</div>
              <div className="text-3xl font-bold text-white">
                {session.duration} Minuten
              </div>
            </div>
          </div>

          <div className="flex items-center gap-4 p-5 bg-gradient-to-r from-emerald-600 to-teal-600 rounded-xl shadow-lg transform hover:scale-105 transition-all">
            <div className="p-3 bg-white/20 backdrop-blur-sm rounded-lg">
              <Calendar className="w-7 h-7 text-white" />
            </div>
            <div>
              <div className="text-sm text-emerald-100">Datum</div>
              <div className="text-xl font-bold text-white">
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
          className="w-full bg-gradient-to-r from-yellow-500 via-orange-500 to-red-500 hover:from-yellow-600 hover:via-orange-600 hover:to-red-600 text-white py-5 px-6 rounded-xl font-bold text-xl shadow-2xl transition-all transform hover:scale-105"
        >
          Fertig
        </button>
      </div>
    </div>
  );
}
