import { useState } from 'react';
import type { Exercise } from '../types';

interface ExerciseCardProps {
  exercise: Exercise;
  currentSet: number;
  onSetComplete: () => void;
  exerciseNumber: number;
}

export function ExerciseCard({
  exercise,
  currentSet,
  onSetComplete,
  exerciseNumber,
}: ExerciseCardProps) {
  const [imageLoaded, setImageLoaded] = useState(false);

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
          {exercise.sets} × {exercise.reps} Wdh
          {exercise.weight > 0 && ` × ${exercise.weight} kg`}
        </div>
      </div>

      {/* Exercise Image */}
      {exercise.imageUrl && (
        <div className={`bg-slate-800 p-3 ${imageLoaded ? '' : 'hidden'}`}>
          <img
            src={exercise.imageUrl}
            alt={exercise.name}
            onLoad={() => setImageLoaded(true)}
            onError={() => setImageLoaded(false)}
            className="w-full max-h-48 object-contain rounded-lg mx-auto"
          />
        </div>
      )}

      {/* Instructions */}
      {exercise.instructions && (
        <div className="mx-4 mt-3 bg-slate-800 border-l-2 border-indigo-400 px-4 py-2 rounded-r-lg">
          <p className="text-sm text-slate-300">{exercise.instructions}</p>
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
            {exercise.reps} × {exercise.weight > 0 ? `${exercise.weight} kg` : 'Körpergewicht'}
          </div>
        </div>

        {/* Action button */}
        <button
          onClick={onSetComplete}
          className="w-full bg-indigo-500 hover:bg-indigo-400 text-white py-3 rounded-xl font-semibold transition-colors"
        >
          Fertig ✓
        </button>
      </div>
    </div>
  );
}
