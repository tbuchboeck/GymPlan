import { useState } from 'react';
import type { Exercise, WorkoutSession } from '../types';
import { ExerciseCard } from './ExerciseCard';
import { RestTimer } from './RestTimer';
import { ArrowLeft, ArrowRight, Home } from 'lucide-react';

interface WorkoutViewProps {
  exercises: Exercise[];
  onComplete: (session: WorkoutSession) => void;
  onExit: () => void;
  initialExerciseIndex?: number;
}

type ViewState = 'exercise' | 'rest';

export function WorkoutView({ exercises, onComplete, onExit, initialExerciseIndex = 0 }: WorkoutViewProps) {
  const [currentExerciseIndex, setCurrentExerciseIndex] = useState(initialExerciseIndex);
  const [currentSet, setCurrentSet] = useState(1);
  const [viewState, setViewState] = useState<ViewState>('exercise');
  const [completedExercises, setCompletedExercises] = useState(0);
  const [startTime] = useState(Date.now());

  const currentExercise = exercises[currentExerciseIndex];
  const isLastExercise = currentExerciseIndex === exercises.length - 1;
  const isLastSet = currentSet === currentExercise.sets;

  const handleSetComplete = () => {
    if (isLastSet) {
      setCompletedExercises((prev) => prev + 1);

      if (isLastExercise) {
        // Workout complete!
        const duration = Math.round((Date.now() - startTime) / 60000);
        const session: WorkoutSession = {
          id: Date.now().toString(),
          date: new Date().toISOString(),
          planName: 'Ganzkörper-Trainingsplan',
          completedExercises: exercises.length,
          totalExercises: exercises.length,
          duration
        };
        onComplete(session);
      } else {
        // Move to rest before next exercise
        setViewState('rest');
      }
    } else {
      // Move to rest before next set
      setViewState('rest');
    }
  };

  const handleRestComplete = () => {
    if (isLastSet) {
      // Move to next exercise
      setCurrentExerciseIndex((prev) => prev + 1);
      setCurrentSet(1);
    } else {
      // Move to next set
      setCurrentSet((prev) => prev + 1);
    }
    setViewState('exercise');
  };

  const handleSkipRest = () => {
    handleRestComplete();
  };

  const handlePrevious = () => {
    if (currentSet > 1) {
      setCurrentSet((prev) => prev - 1);
    } else if (currentExerciseIndex > 0) {
      setCurrentExerciseIndex((prev) => prev - 1);
      setCurrentSet(exercises[currentExerciseIndex - 1].sets);
      setCompletedExercises((prev) => Math.max(0, prev - 1));
    }
    setViewState('exercise');
  };

  const handleNext = () => {
    if (currentSet < currentExercise.sets) {
      setCurrentSet((prev) => prev + 1);
    } else if (currentExerciseIndex < exercises.length - 1) {
      setCurrentExerciseIndex((prev) => prev + 1);
      setCurrentSet(1);
      setCompletedExercises((prev) => prev + 1);
    }
    setViewState('exercise');
  };

  const progress = ((completedExercises + (currentSet - 1) / currentExercise.sets) / exercises.length) * 100;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-indigo-900">
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 shadow-2xl sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between mb-3">
            <button
              onClick={onExit}
              className="flex items-center gap-2 text-white hover:text-indigo-100 transition-colors"
            >
              <Home className="w-5 h-5" />
              <span>Beenden</span>
            </button>
            <div className="text-sm text-indigo-100">
              {completedExercises} / {exercises.length} Übungen
            </div>
          </div>

          {/* Progress Bar */}
          <div className="w-full bg-white/20 rounded-full h-3">
            <div
              className="bg-gradient-to-r from-yellow-400 to-orange-500 h-3 rounded-full transition-all duration-300 shadow-lg"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-4 py-8">
        {viewState === 'exercise' ? (
          <ExerciseCard
            exercise={currentExercise}
            currentSet={currentSet}
            onSetComplete={handleSetComplete}
            exerciseNumber={currentExerciseIndex + 1}
            totalExercises={exercises.length}
          />
        ) : (
          <RestTimer
            seconds={currentExercise.rest}
            onComplete={handleRestComplete}
            onSkip={handleSkipRest}
          />
        )}

        {/* Navigation */}
        <div className="flex gap-4 mt-6">
          <button
            onClick={handlePrevious}
            disabled={currentExerciseIndex === 0 && currentSet === 1}
            className="flex-1 flex items-center justify-center gap-2 bg-gradient-to-r from-slate-600 to-slate-700 hover:from-slate-500 hover:to-slate-600 disabled:from-slate-800 disabled:to-slate-900 disabled:text-slate-600 text-white py-4 px-6 rounded-xl font-semibold shadow-2xl transition-all transform hover:scale-105 disabled:transform-none disabled:cursor-not-allowed"
          >
            <ArrowLeft className="w-5 h-5" />
            Zurück
          </button>

          <button
            onClick={handleNext}
            disabled={isLastExercise && isLastSet}
            className="flex-1 flex items-center justify-center gap-2 bg-gradient-to-r from-slate-600 to-slate-700 hover:from-slate-500 hover:to-slate-600 disabled:from-slate-800 disabled:to-slate-900 disabled:text-slate-600 text-white py-4 px-6 rounded-xl font-semibold shadow-2xl transition-all transform hover:scale-105 disabled:transform-none disabled:cursor-not-allowed"
          >
            Weiter
            <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
}
