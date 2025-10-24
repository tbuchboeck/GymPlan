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

  return (
    <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-6">
        <div className="text-sm font-medium mb-2">
          Übung {exerciseNumber} von {totalExercises}
        </div>
        <h2 className="text-2xl font-bold mb-2">{exercise.name}</h2>
        <div className="flex items-center gap-4 text-sm">
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
      {exercise.imageUrl && (
        <div className="bg-gray-50 p-4">
          <img
            src={exercise.imageUrl}
            alt={exercise.name}
            className="w-full max-w-md mx-auto rounded-lg"
          />
        </div>
      )}

      {/* Instructions */}
      {exercise.instructions && (
        <div className="p-6 bg-blue-50 border-l-4 border-blue-500">
          <h3 className="font-semibold text-blue-900 mb-2">Anweisungen:</h3>
          <p className="text-blue-800">{exercise.instructions}</p>
        </div>
      )}

      {/* Sets Progress */}
      <div className="p-6">
        <h3 className="font-semibold text-gray-800 mb-4">Sätze</h3>
        <div className="space-y-3">
          {Array.from({ length: exercise.sets }, (_, i) => i + 1).map((setNumber) => (
            <div
              key={setNumber}
              className={`flex items-center justify-between p-4 rounded-xl border-2 transition-all ${
                isSetCompleted(setNumber)
                  ? 'bg-green-50 border-green-500'
                  : isCurrentSet(setNumber)
                  ? 'bg-blue-50 border-blue-500 ring-2 ring-blue-200'
                  : 'bg-gray-50 border-gray-200'
              }`}
            >
              <div className="flex items-center gap-3">
                {isSetCompleted(setNumber) ? (
                  <CheckCircle className="w-6 h-6 text-green-600" />
                ) : (
                  <Circle className="w-6 h-6 text-gray-400" />
                )}
                <div>
                  <div className="font-semibold text-gray-800">Satz {setNumber}</div>
                  <div className="text-sm text-gray-600">
                    {exercise.reps} × {exercise.weight > 0 ? `${exercise.weight} kg` : 'Körpergewicht'}
                  </div>
                </div>
              </div>

              {isCurrentSet(setNumber) && (
                <button
                  onClick={onSetComplete}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-semibold transition-colors"
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
