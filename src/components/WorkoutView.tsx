import { useEffect, useRef, useState } from 'react';
import type { Exercise, WorkoutSession } from '../types';
import type { Person } from '../lib/auth-service';
import { ExerciseCard } from './ExerciseCard';
import { RestTimer } from './RestTimer';
import { holdSeconds } from '../utils/format';
import { useWakeLock } from '../hooks/useWakeLock';
import {
  clearWorkoutProgress,
  loadWorkoutProgress,
  saveWorkoutProgress,
  unlockAudio,
} from '../lib/workout-progress';
import { ArrowLeft, ArrowRight, Home } from 'lucide-react';

interface WorkoutViewProps {
  exercises: Exercise[];
  planName: string;
  person: Person;
  onComplete: (session: WorkoutSession) => void;
  onExit: () => void;
  // Gesetzt = gezielt bei dieser Übung einsteigen; nicht gesetzt = gespeicherten Stand fortsetzen
  initialExerciseIndex?: number;
}

type Phase =
  | { kind: 'idle' }
  | { kind: 'hold'; side: 1 | 2 }
  | { kind: 'switch' }
  | { kind: 'rest' };

const SIDE_SWITCH_SECONDS = 5;
const HISTORY_MARKER = 'gymplanWorkout';

const setKey = (exerciseIndex: number, set: number) => `${exerciseIndex}:${set}`;

function clampIndex(i: number, length: number) {
  return Math.min(Math.max(0, Math.floor(i) || 0), Math.max(0, length - 1));
}

/** Auf Minuten gerundet; ab 30 s mindestens 1 Minute. */
function durationMinutes(startedAt: number) {
  const ms = Date.now() - startedAt;
  if (ms <= 30_000) return 0;
  return Math.max(1, Math.round(ms / 60_000));
}

export function WorkoutView({ exercises, planName, person, onComplete, onExit, initialExerciseIndex }: WorkoutViewProps) {
  // Gespeicherten Stand desselben Plans übernehmen (loadWorkoutProgress prüft die 12 h)
  const [initial] = useState(() => {
    const saved = loadWorkoutProgress(person);
    const usable = saved && saved.planName === planName && saved.totalExercises === exercises.length ? saved : null;
    const resumeHere = usable && initialExerciseIndex === undefined;
    const exerciseIndex = clampIndex(resumeHere ? usable.exerciseIndex : (initialExerciseIndex ?? 0), exercises.length);
    const maxSet = exercises[exerciseIndex]?.sets ?? 1;
    return {
      exerciseIndex,
      currentSet: resumeHere ? Math.min(Math.max(1, usable.currentSet || 1), maxSet) : 1,
      startedAt: usable?.startedAt ?? Date.now(),
      completedSets: usable?.completedSets ?? [],
      abortedExercises: usable?.abortedExercises ?? [],
    };
  });

  const [currentExerciseIndex, setCurrentExerciseIndex] = useState(initial.exerciseIndex);
  const [currentSet, setCurrentSet] = useState(initial.currentSet);
  const [startedAt] = useState(initial.startedAt);
  const [completedSets, setCompletedSets] = useState<string[]>(initial.completedSets);
  const [abortedExercises, setAbortedExercises] = useState<string[]>(initial.abortedExercises);
  const [phase, setPhase] = useState<Phase>({ kind: 'idle' });
  const [confirmExit, setConfirmExit] = useState(false);
  const [toast, setToast] = useState<string | null>(null);
  const finishedRef = useRef(false);

  useWakeLock();

  const currentExercise = exercises[currentExerciseIndex];
  const isLastExercise = currentExerciseIndex === exercises.length - 1;
  const isLastSet = currentSet === currentExercise.sets;
  const overlayOpen = phase.kind !== 'idle';

  // Stand bei jeder Änderung sichern
  useEffect(() => {
    if (finishedRef.current) return;
    saveWorkoutProgress({
      person,
      planName,
      exerciseIndex: currentExerciseIndex,
      currentSet,
      totalExercises: exercises.length,
      startedAt,
      updatedAt: Date.now(),
      completedSets,
      abortedExercises,
    });
  }, [person, planName, currentExerciseIndex, currentSet, exercises.length, startedAt, completedSets, abortedExercises]);

  // Android-Zurück-Geste: eigenen Verlaufseintrag anlegen und Zurück abfangen
  useEffect(() => {
    history.pushState({ [HISTORY_MARKER]: true }, '');
    const onPop = (e: PopStateEvent) => {
      // Landung auf einem eigenen Eintrag (z. B. StrictMode-Doppelmount) → nichts tun
      if (e.state && e.state[HISTORY_MARKER]) return;
      history.pushState({ [HISTORY_MARKER]: true }, '');
      setConfirmExit(true);
    };
    window.addEventListener('popstate', onPop);
    return () => {
      window.removeEventListener('popstate', onPop);
      if (history.state && history.state[HISTORY_MARKER]) history.back();
    };
  }, []);

  useEffect(() => {
    if (!toast) return;
    const t = setTimeout(() => setToast(null), 4000);
    return () => clearTimeout(t);
  }, [toast]);

  const countCompleted = (sets: string[], aborted: string[]) => {
    const done = new Set(sets);
    return exercises.filter(
      (ex, i) =>
        !aborted.includes(ex.name) &&
        Array.from({ length: ex.sets }, (_, s) => s + 1).every((s) => done.has(setKey(i, s))),
    ).length;
  };

  const finish = (sets: string[], aborted: string[]) => {
    finishedRef.current = true;
    clearWorkoutProgress(person);
    const completed = countCompleted(sets, aborted);
    if (completed === 0) {
      // Nichts wirklich gemacht → keine Session speichern
      onExit();
      return;
    }
    const session: WorkoutSession = {
      id: Date.now().toString(),
      date: new Date().toISOString(),
      planName,
      completedExercises: completed,
      totalExercises: exercises.length,
      duration: durationMinutes(startedAt),
      ...(aborted.length > 0 ? { abortedExercises: aborted } : {}),
    };
    onComplete(session);
  };

  const goToExercise = (index: number, set = 1) => {
    setCurrentExerciseIndex(index);
    setCurrentSet(set);
    setPhase({ kind: 'idle' });
  };

  const handleSetComplete = () => {
    unlockAudio();
    const key = setKey(currentExerciseIndex, currentSet);
    const nextSets = completedSets.includes(key) ? completedSets : [...completedSets, key];
    setCompletedSets(nextSets);

    if (isLastSet && isLastExercise) {
      finish(nextSets, abortedExercises);
    } else {
      setPhase({ kind: 'rest' });
    }
  };

  const handleStartTimer = () => {
    unlockAudio();
    setPhase({ kind: 'hold', side: 1 });
  };

  const handleHoldComplete = () => {
    if (currentExercise.perSide && phase.kind === 'hold' && phase.side === 1) {
      setPhase({ kind: 'switch' });
    } else {
      handleSetComplete();
    }
  };

  const handleRestComplete = () => {
    if (isLastSet) {
      goToExercise(currentExerciseIndex + 1);
    } else {
      setCurrentSet((prev) => prev + 1);
      setPhase({ kind: 'idle' });
    }
  };

  const handleAbortExercise = () => {
    const name = currentExercise.name;
    const nextAborted = abortedExercises.includes(name) ? abortedExercises : [...abortedExercises, name];
    setAbortedExercises(nextAborted);
    setToast('Übung abgebrochen – heute nicht wiederholen');
    if (isLastExercise) {
      finish(completedSets, nextAborted);
    } else {
      goToExercise(currentExerciseIndex + 1);
    }
  };

  const handlePrevious = () => {
    if (overlayOpen) return;
    if (currentSet > 1) {
      setCurrentSet((prev) => prev - 1);
    } else if (currentExerciseIndex > 0) {
      goToExercise(currentExerciseIndex - 1, exercises[currentExerciseIndex - 1].sets);
    }
  };

  const handleNext = () => {
    if (overlayOpen) return;
    if (currentSet < currentExercise.sets) {
      setCurrentSet((prev) => prev + 1);
    } else if (currentExerciseIndex < exercises.length - 1) {
      goToExercise(currentExerciseIndex + 1);
    }
  };

  const handleDiscard = () => {
    finishedRef.current = true;
    clearWorkoutProgress(person);
    onExit();
  };

  // Fortschritt aus Position ableiten
  const progress = ((currentExerciseIndex + (currentSet - 1) / currentExercise.sets) / exercises.length) * 100;
  const completedCount = countCompleted(completedSets, abortedExercises);
  const holdTotal = holdSeconds(currentExercise) ?? 0;
  const nextExercise = isLastSet ? exercises[currentExerciseIndex + 1] : undefined;

  return (
    <div className="h-dvh flex flex-col bg-slate-900">
      {/* Header */}
      <div className="bg-slate-900/95 backdrop-blur-sm border-b border-slate-800 z-10">
        <div className="max-w-4xl mx-auto px-4 py-2">
          <div className="flex items-center justify-between mb-1">
            <button
              type="button"
              onClick={() => setConfirmExit(true)}
              className="-ml-2 min-w-11 min-h-11 flex items-center justify-center rounded-xl text-slate-400 hover:text-white transition-colors"
              aria-label="Training beenden"
            >
              <Home className="w-6 h-6" />
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
            key={currentExercise.id}
            exercise={currentExercise}
            currentSet={currentSet}
            onSetComplete={handleSetComplete}
            onStartTimer={handleStartTimer}
            onAbort={handleAbortExercise}
            exerciseNumber={currentExerciseIndex + 1}
          />
        </div>

        {/* Halte-Countdown; bei „pro Seite“ zweimal */}
        {phase.kind === 'hold' && (
          <div className="absolute inset-0 bg-slate-900/80 backdrop-blur-sm flex items-center justify-center z-20 animate-fade-in px-4">
            <RestTimer
              key={`hold-${currentExerciseIndex}-${currentSet}-${phase.side}`}
              seconds={holdTotal}
              label={currentExercise.name}
              hint={currentExercise.perSide ? `Seite ${phase.side} von 2` : undefined}
              skipLabel="Abbrechen"
              onComplete={handleHoldComplete}
              onSkip={() => setPhase({ kind: 'idle' })}
            />
          </div>
        )}

        {phase.kind === 'switch' && (
          <div className="absolute inset-0 bg-slate-900/80 backdrop-blur-sm flex items-center justify-center z-20 animate-fade-in px-4">
            <RestTimer
              key={`switch-${currentExerciseIndex}-${currentSet}`}
              seconds={SIDE_SWITCH_SECONDS}
              label="Seite wechseln"
              hint="Gleich geht es mit Seite 2 weiter"
              skipLabel="Abbrechen"
              onComplete={() => setPhase({ kind: 'hold', side: 2 })}
              onSkip={() => setPhase({ kind: 'idle' })}
            />
          </div>
        )}

        {/* Pause */}
        {phase.kind === 'rest' && (
          <div className="absolute inset-0 bg-slate-900/80 backdrop-blur-sm flex items-center justify-center z-20 animate-fade-in px-4">
            <RestTimer
              key={`rest-${currentExerciseIndex}-${currentSet}`}
              seconds={currentExercise.rest}
              hint={nextExercise ? `Als Nächstes: ${nextExercise.name}` : undefined}
              onComplete={handleRestComplete}
              onSkip={handleRestComplete}
            />
          </div>
        )}

        {toast && (
          <div className="fixed left-1/2 -translate-x-1/2 bottom-24 z-30 max-w-sm w-[calc(100%-2rem)] bg-slate-800 border border-red-500/40 text-red-200 text-sm text-center rounded-xl px-4 py-3 shadow-xl animate-fade-in" role="status">
            {toast}
          </div>
        )}
      </div>

      {/* Bottom nav – während Timer/Pause gesperrt */}
      <div className="bg-slate-900/95 backdrop-blur-sm border-t border-slate-800 z-10">
        <div className="max-w-4xl mx-auto px-4 py-3 flex gap-3">
          <button
            type="button"
            onClick={handlePrevious}
            disabled={overlayOpen || (currentExerciseIndex === 0 && currentSet === 1)}
            className="flex-1 min-h-12 flex items-center justify-center gap-2 bg-slate-800 hover:bg-slate-700 disabled:opacity-30 disabled:cursor-not-allowed text-white py-3 rounded-xl font-semibold transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            Zurück
          </button>

          <button
            type="button"
            onClick={handleNext}
            disabled={overlayOpen || (isLastExercise && isLastSet)}
            className="flex-1 min-h-12 flex items-center justify-center gap-2 bg-slate-800 hover:bg-slate-700 disabled:opacity-30 disabled:cursor-not-allowed text-white py-3 rounded-xl font-semibold transition-colors"
          >
            Weiter
            <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Rückfrage beim Beenden */}
      {confirmExit && (
        <div
          className="fixed inset-0 z-40 bg-slate-950/80 backdrop-blur-sm flex items-end sm:items-center justify-center p-4 animate-fade-in"
          role="dialog"
          aria-modal="true"
          aria-labelledby="exit-title"
          onClick={() => setConfirmExit(false)}
        >
          <div
            className="w-full max-w-sm bg-slate-800 border border-slate-700 rounded-2xl p-5 shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <h2 id="exit-title" className="text-lg font-bold text-white mb-1">Training beenden?</h2>
            <p className="text-sm text-slate-400 mb-4">
              Dein Fortschritt bleibt gespeichert – du kannst später weitermachen.
            </p>
            <div className="flex flex-col gap-2">
              <button
                type="button"
                onClick={onExit}
                className="w-full min-h-12 bg-indigo-500 hover:bg-indigo-400 text-white rounded-xl font-semibold transition-colors"
              >
                Beenden, später weitermachen
              </button>
              {completedCount > 0 && (
                <button
                  type="button"
                  onClick={() => finish(completedSets, abortedExercises)}
                  className="w-full min-h-12 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl font-semibold transition-colors"
                >
                  Jetzt abschließen ({completedCount} {completedCount === 1 ? 'Übung' : 'Übungen'})
                </button>
              )}
              <button
                type="button"
                onClick={handleDiscard}
                className="w-full min-h-12 border border-red-500/50 bg-red-500/10 hover:bg-red-500/20 text-red-300 rounded-xl font-medium transition-colors"
              >
                Verwerfen
              </button>
              <button
                type="button"
                onClick={() => setConfirmExit(false)}
                className="w-full min-h-11 text-slate-400 hover:text-white rounded-xl font-medium transition-colors"
              >
                Weiter trainieren
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
