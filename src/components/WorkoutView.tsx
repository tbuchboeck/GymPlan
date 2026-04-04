import { useState } from 'react';
import type { Exercise, WorkoutSession } from '../types';
import { ExerciseCard } from './ExerciseCard';
import { RestTimer } from './RestTimer';
import { ArrowLeft, ArrowRight, Home } from 'lucide-react';

interface WorkoutViewProps {
  exercises: Exercise[];
  planName: string;
  onComplete: (session: WorkoutSession) => void;
  onExit: () => void;
  initialExerciseIndex?: number;
}

export function WorkoutView({ exercises, planName, onComplete, onExit, initialExerciseIndex = 0 }: WorkoutViewProps) {
  const [currentExerciseIndex, setCurrentExerciseIndex] = useState(initialExerciseIndex);
  const [currentSet, setCurrentSet] = useState(1);
  const [isResting, setIsResting] = useState(false);
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
          planName,
          completedExercises: exercises.length,
          totalExercises: exercises.length,
          duration
        };
        onComplete(session);
      } else {
        // Rest before next exercise
        setIsResting(true);
      }
    } else {
      // Rest before next set
      setIsResting(true);
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
    setIsResting(false);
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
    setIsResting(false);
  };

  const handleNext = () => {
    if (currentSet < currentExercise.sets) {
      setCurrentSet((prev) => prev + 1);
    } else if (currentExerciseIndex < exercises.length - 1) {
      setCurrentExerciseIndex((prev) => prev + 1);
      setCurrentSet(1);
      setCompletedExercises((prev) => prev + 1);
    }
    setIsResting(false);
  };

  const progress = ((completedExercises + (currentSet - 1) / currentExercise.sets) / exercises.length) * 100;

  return (
    <div className="h-dvh flex flex-col bg-slate-900">
      {/* Header */}
      <div className="bg-slate-900/95 backdrop-blur-sm border-b border-slate-800 z-10">
        <div className="max-w-4xl mx-auto px-4 py-3">
          <div className="flex items-center justify-between mb-2">
            <button
              onClick={onExit}
              className="text-slate-400 hover:text-white transition-colors p-1"
              aria-label="Beenden"
            >
              <Home className="w-5 h-5" />
            </button>
            <span className="text-sm font-medium text-slate-300">
              {currentExerciseIndex + 1} / {exercises.length}
            </span>
          </div>

          {/* Progress Bar */}
          <div className="w-full bg-slate-800 rounded-full h-1.5">
            <div
              className="bg-indigo-500 h-1.5 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      </div>

      {/* Content area */}
      <div className="flex-1 overflow-y-auto relative">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <ExerciseCard
            exercise={currentExercise}
            currentSet={currentSet}
            onSetComplete={handleSetComplete}
            exerciseNumber={currentExerciseIndex + 1}
          />
        </div>

        {/* Rest Timer Overlay */}
        {isResting && (
          <div className="absolute inset-0 bg-slate-900/80 backdrop-blur-sm flex items-center justify-center z-20 animate-fade-in">
            <RestTimer
              seconds={currentExercise.rest}
              onComplete={handleRestComplete}
              onSkip={handleSkipRest}
            />
          </div>
        )}
      </div>

      {/* Bottom nav */}
      <div className="bg-slate-900/95 backdrop-blur-sm border-t border-slate-800 z-10">
        <div className="max-w-4xl mx-auto px-4 py-3 flex gap-3">
          <button
            onClick={handlePrevious}
            disabled={currentExerciseIndex === 0 && currentSet === 1}
            className="flex-1 flex items-center justify-center gap-2 bg-slate-800 hover:bg-slate-700 disabled:opacity-30 disabled:cursor-not-allowed text-white py-3 rounded-xl font-semibold transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            Zurück
          </button>

          <button
            onClick={handleNext}
            disabled={isLastExercise && isLastSet}
            className="flex-1 flex items-center justify-center gap-2 bg-slate-800 hover:bg-slate-700 disabled:opacity-30 disabled:cursor-not-allowed text-white py-3 rounded-xl font-semibold transition-colors"
          >
            Weiter
            <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
}
