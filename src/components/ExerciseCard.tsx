import { useState } from 'react';
import type { Exercise } from '../types';
import { CheckCircle, Circle } from 'lucide-react';

interface ExerciseCardProps {
  exercise: Exercise;
  currentSet: number;
  onSetComplete: () => void;
  exerciseNumber: number;
  totalExercises: number;
}

export function ExerciseCard({
  exercise,
  currentSet,
  onSetComplete,
  exerciseNumber,
  totalExercises
}: ExerciseCardProps) {
  const isSetCompleted = (setNumber: number) => setNumber < currentSet;
  const isCurrentSet = (setNumber: number) => setNumber === currentSet;
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageError, setImageError] = useState(false);

  const handleImageLoad = () => {
    setImageLoaded(true);
    setImageError(false);
  };

  const handleImageError = () => {
    setImageError(true);
    setImageLoaded(false);
  };

  return (
    <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl shadow-2xl overflow-hidden border border-slate-700">
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-6">
        <div className="text-sm font-medium mb-2 text-indigo-100">
          Übung {exerciseNumber} von {totalExercises}
        </div>
        <h2 className="text-3xl font-bold mb-2">{exercise.name}</h2>
        <div className="flex items-center gap-4 text-sm text-indigo-100">
          <span>{exercise.sets} Sätze</span>
          <span>•</span>
          <span>{exercise.reps} Wiederholungen</span>
          {exercise.weight > 0 && (
            <>
              <span>•</span>
              <span>{exercise.weight} kg</span>
            </>
          )}
        </div>
      </div>

      {/* Exercise Image */}
      {exercise.imageUrl && !imageError && (
        <div className="bg-gradient-to-br from-slate-700 to-slate-800 p-6">
          <img
            src={exercise.imageUrl}
            alt={exercise.name}
            onLoad={handleImageLoad}
            onError={handleImageError}
            className={`w-full max-w-md mx-auto rounded-lg shadow-2xl border-2 border-slate-600 transition-opacity duration-300 ${
              imageLoaded ? 'opacity-100' : 'opacity-0'
            }`}
          />
          {!imageLoaded && (
            <div className="w-full max-w-md mx-auto h-64 flex items-center justify-center">
              <div className="animate-pulse text-slate-500">Bild wird geladen...</div>
            </div>
          )}
        </div>
      )}

      {/* Instructions */}
      {exercise.instructions && (
        <div className="p-6 bg-gradient-to-r from-blue-600 to-cyan-600 border-l-4 border-cyan-400">
          <h3 className="font-semibold text-white mb-2">Anweisungen:</h3>
          <p className="text-blue-50">{exercise.instructions}</p>
        </div>
      )}

      {/* Sets Progress */}
      <div className="p-6">
        <h3 className="font-semibold text-white mb-4">Sätze</h3>
        <div className="space-y-3">
          {Array.from({ length: exercise.sets }, (_, i) => i + 1).map((setNumber) => (
            <div
              key={setNumber}
              className={`flex items-center justify-between p-4 rounded-xl border-2 transition-all ${
                isSetCompleted(setNumber)
                  ? 'bg-gradient-to-r from-emerald-600 to-green-600 border-emerald-400 shadow-lg'
                  : isCurrentSet(setNumber)
                  ? 'bg-gradient-to-r from-blue-600 to-cyan-600 border-cyan-400 ring-2 ring-cyan-300 shadow-lg'
                  : 'bg-gradient-to-r from-slate-700 to-slate-600 border-slate-500'
              }`}
            >
              <div className="flex items-center gap-3">
                {isSetCompleted(setNumber) ? (
                  <CheckCircle className="w-6 h-6 text-emerald-200" />
                ) : (
                  <Circle className="w-6 h-6 text-slate-400" />
                )}
                <div>
                  <div className="font-semibold text-white">Satz {setNumber}</div>
                  <div className="text-sm text-slate-200">
                    {exercise.reps} × {exercise.weight > 0 ? `${exercise.weight} kg` : 'Körpergewicht'}
                  </div>
                </div>
              </div>

              {isCurrentSet(setNumber) && (
                <button
                  onClick={onSetComplete}
                  className="bg-gradient-to-r from-yellow-500 to-orange-500 hover:from-yellow-600 hover:to-orange-600 text-white px-6 py-2 rounded-lg font-bold transition-all transform hover:scale-105 shadow-lg"
                >
                  Fertig
                </button>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
