import type { WorkoutSession } from '../types';
import { Trophy, Clock, Dumbbell, Calendar } from 'lucide-react';

interface WorkoutSummaryProps {
  session: WorkoutSession;
  onClose: () => void;
}

export function WorkoutSummary({ session, onClose }: WorkoutSummaryProps) {
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
        </div>

        <button
          onClick={onClose}
          className="w-full mt-6 bg-indigo-500 hover:bg-indigo-400 text-white py-3 rounded-xl font-semibold transition-colors"
        >
          Fertig
        </button>
      </div>
    </div>
  );
}
