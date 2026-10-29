import { useState } from 'react';
import type { Exercise } from '../types';
import { formatAmount, holdSeconds } from '../utils/format';

interface ExerciseCardProps {
  exercise: Exercise;
  currentSet: number;
  onSetComplete: () => void;
  onStartTimer: () => void;
  onAbort?: () => void;
  exerciseNumber: number;
}

export function ExerciseCard({
  exercise,
  currentSet,
  onSetComplete,
  onStartTimer,
  onAbort,
  exerciseNumber,
}: ExerciseCardProps) {
  const [imageFailed, setImageFailed] = useState(false);
  const timerSeconds = holdSeconds(exercise);
  const showImage = !!exercise.imageUrl && !imageFailed;

  return (
    <div className="bg-slate-800/50 rounded-2xl border border-slate-700/50 overflow-hidden animate-fade-in">
      {/* Header */}
      <div className="bg-indigo-600 p-4 rounded-t-2xl">
        <div className="flex items-center gap-3 mb-1">
          <span className="bg-indigo-500 text-white text-xs font-bold w-6 h-6 rounded-full flex items-center justify-center shrink-0">
            {exerciseNumber}
          </span>
          <h2 className="text-xl font-bold text-white leading-tight">{exercise.name}</h2>
        </div>
        <div className="text-sm text-indigo-200 ml-9">
          {exercise.sets} × {formatAmount(exercise)}
          {exercise.weight > 0 && ` × ${exercise.weight} kg`}
        </div>
      </div>

      {/* Exercise Image – Platz reserviert, damit beim Laden nichts springt */}
      {showImage && (
        <div className="bg-slate-800 p-3">
          <div className="w-full aspect-[4/3] max-h-72 mx-auto flex items-center justify-center">
            <img
              src={exercise.imageUrl}
              alt={exercise.name}
              onError={() => setImageFailed(true)}
              className="max-w-full max-h-full object-contain rounded-lg"
            />
          </div>
        </div>
      )}

      {/* Instructions */}
      {exercise.instructions && (
        <div className="mx-4 mt-3 bg-slate-800 border-l-2 border-indigo-400 px-4 py-2 rounded-r-lg">
          <p className="text-base text-slate-300">{exercise.instructions}</p>
        </div>
      )}

      {/* Set indicators */}
      <div className="p-4">
        <div className="flex items-center justify-center gap-2 mb-3">
          {Array.from({ length: exercise.sets }, (_, i) => i + 1).map((setNumber) => {
            const isCompleted = setNumber < currentSet;
            const isCurrent = setNumber === currentSet;
            return (
              <div
                key={setNumber}
                className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transition-all ${
                  isCompleted
                    ? 'bg-emerald-500 text-white'
                    : isCurrent
                    ? 'bg-indigo-500 text-white ring-2 ring-indigo-300'
                    : 'bg-slate-700 text-slate-500'
                }`}
              >
                {setNumber}
              </div>
            );
          })}
        </div>

        {/* Current set info */}
        <div className="text-center mb-4">
          <div className="text-sm font-medium text-slate-400">Satz {currentSet}</div>
          <div className="text-slate-300">
            {formatAmount(exercise)} × {exercise.weight > 0 ? `${exercise.weight} kg` : 'Körpergewicht'}
          </div>
        </div>

        {/* Countdown for timed exercises (optional) */}
        {timerSeconds !== null && (
          <button
            type="button"
            onClick={onStartTimer}
            className="w-full mb-2 min-h-12 bg-slate-700 hover:bg-slate-600 text-white py-3 rounded-xl font-semibold transition-colors"
          >
            ▶ Timer starten ({formatAmount(exercise)})
          </button>
        )}

        {/* Action button */}
        <button
          type="button"
          onClick={onSetComplete}
          className="w-full min-h-14 bg-indigo-500 hover:bg-indigo-400 text-white text-lg py-4 rounded-xl font-semibold transition-colors"
        >
          Fertig ✓
        </button>

        {/* Nerven-/Dehnübung: sofort abbrechen können */}
        {exercise.caution && onAbort && (
          <button
            type="button"
            onClick={onAbort}
            className="w-full mt-3 min-h-11 px-4 py-2 rounded-xl border border-red-500/50 bg-red-500/10 hover:bg-red-500/20 text-red-300 font-medium transition-colors"
          >
            Kribbelt / zieht – abbrechen
          </button>
        )}
      </div>
    </div>
  );
}
