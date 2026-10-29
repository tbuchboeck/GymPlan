import { useEffect, useRef, useState } from 'react';
import type { Exercise, WorkoutSession } from '../types';
import type { Person } from '../lib/auth-service';
import { ExerciseCard } from './ExerciseCard';
import { RestTimer } from './RestTimer';
import { formatAmount, holdSeconds, planTitle } from '../utils/format';
import { planTheme } from '../utils/plan-theme';
import { Button } from './ui/Button';
import { useWakeLock } from '../hooks/useWakeLock';
import {
  clearWorkoutProgress,
  loadWorkoutProgress,
  saveWorkoutProgress,
  unlockAudio,
} from '../lib/workout-progress';
import { ArrowLeft, ArrowRight, Check, Play, X } from 'lucide-react';

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

  const theme = planTheme(planName);
  const timerSeconds = holdSeconds(currentExercise);
  const overlayClass =
    'absolute inset-0 z-20 flex flex-col items-center bg-slate-950/90 backdrop-blur-md animate-fade-in';

  return (
    <div className="flex h-dvh flex-col bg-slate-950">
      {/* Kopf: Beenden, Plan, Fortschritt */}
      <header className="z-10 border-b border-white/5 bg-slate-950/95 px-safe-4 pt-safe-1 pb-3 backdrop-blur">
        <div className="mx-auto max-w-xl">
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => setConfirmExit(true)}
              className="-ml-2 flex min-h-11 min-w-11 items-center justify-center rounded-xl text-slate-300 transition hover:bg-white/5 hover:text-white"
              aria-label="Training beenden"
            >
              <X className="h-6 w-6" />
            </button>
            <span className="min-w-0 flex-1 truncate text-center text-sm font-medium text-slate-400">
              {planTitle(planName)}
            </span>
            <span className="min-w-11 rounded-full bg-slate-800 px-2.5 py-1 text-center text-sm font-semibold tabular-nums text-slate-200">
              {currentExerciseIndex + 1} / {exercises.length}
            </span>
          </div>

          <div className="mt-2 h-2 w-full overflow-hidden rounded-full bg-slate-800">
            <div
              className={`h-full rounded-full bg-gradient-to-r ${theme.gradient} transition-all duration-500 ease-out`}
              style={{ width: `${Math.max(progress, 2)}%` }}
            />
          </div>
        </div>
      </header>

      {/* Inhalt + Daumenleiste; Timer-Overlays decken beides ab */}
      <div className="relative flex min-h-0 flex-1 flex-col">
        <div className="flex-1 overflow-y-auto">
          <div className="mx-auto max-w-xl px-safe-4 pt-4 pb-6">
            <ExerciseCard
              key={currentExercise.id}
              exercise={currentExercise}
              currentSet={currentSet}
              exerciseNumber={currentExerciseIndex + 1}
              totalExercises={exercises.length}
              theme={theme}
              onAbort={handleAbortExercise}
            />
          </div>
        </div>

        {/* Daumenleiste – während Timer/Pause verdeckt */}
        <div className="z-10 border-t border-white/5 bg-slate-950/95 px-safe-4 pt-3 pb-safe-3 backdrop-blur">
          <div className="mx-auto max-w-xl space-y-2">
            {timerSeconds !== null && (
              <button
                type="button"
                onClick={handleStartTimer}
                disabled={overlayOpen}
                className={`flex min-h-16 w-full items-center justify-center gap-2 rounded-2xl bg-gradient-to-br ${theme.gradient} px-4 text-lg font-semibold text-white shadow-lg shadow-black/40 transition active:scale-[0.98] disabled:opacity-40`}
              >
                <Play className="h-6 w-6 fill-current" />
                Timer starten ({formatAmount(currentExercise)})
              </button>
            )}
            <div className="flex gap-2">
              <Button
                variant="secondary"
                size={timerSeconds !== null ? 'lg' : 'xl'}
                onClick={handlePrevious}
                disabled={overlayOpen || (currentExerciseIndex === 0 && currentSet === 1)}
                aria-label="Zurück"
                className="w-16 shrink-0 px-0!"
              >
                <ArrowLeft className="h-6 w-6" />
              </Button>
              <Button
                variant={timerSeconds !== null ? 'secondary' : 'primary'}
                size={timerSeconds !== null ? 'lg' : 'xl'}
                onClick={handleSetComplete}
                disabled={overlayOpen}
                className="flex-1"
              >
                <Check className="h-6 w-6" strokeWidth={3} />
                Fertig
              </Button>
              <Button
                variant="secondary"
                size={timerSeconds !== null ? 'lg' : 'xl'}
                onClick={handleNext}
                disabled={overlayOpen || (isLastExercise && isLastSet)}
                aria-label="Weiter"
                className="w-16 shrink-0 px-0!"
              >
                <ArrowRight className="h-6 w-6" />
              </Button>
            </div>
          </div>
        </div>

        {/* Halte-Countdown; bei „pro Seite“ zweimal */}
        {phase.kind === 'hold' && (
          <div className={overlayClass}>
            <RestTimer
              key={`hold-${currentExerciseIndex}-${currentSet}-${phase.side}`}
              seconds={holdTotal}
              label={currentExercise.name}
              hint={currentExercise.perSide ? `Seite ${phase.side} von 2` : `Satz ${currentSet} von ${currentExercise.sets}`}
              skipLabel="Abbrechen"
              accentFrom={theme.from}
              accentTo={theme.to}
              previewImage={currentExercise.imageUrl}
              onComplete={handleHoldComplete}
              onSkip={() => setPhase({ kind: 'idle' })}
            />
          </div>
        )}

        {phase.kind === 'switch' && (
          <div className={overlayClass}>
            <RestTimer
              key={`switch-${currentExerciseIndex}-${currentSet}`}
              seconds={SIDE_SWITCH_SECONDS}
              label="Seite wechseln"
              hint="Gleich geht es mit Seite 2 weiter"
              skipLabel="Abbrechen"
              accentFrom="#fde047"
              accentTo="#f59e0b"
              onComplete={() => setPhase({ kind: 'hold', side: 2 })}
              onSkip={() => setPhase({ kind: 'idle' })}
            />
          </div>
        )}

        {/* Pause */}
        {phase.kind === 'rest' && (
          <div className={overlayClass}>
            <RestTimer
              key={`rest-${currentExerciseIndex}-${currentSet}`}
              seconds={currentExercise.rest}
              hint={nextExercise ? `Als Nächstes: ${nextExercise.name}` : `Gleich: Satz ${currentSet + 1} von ${currentExercise.sets}`}
              accentFrom={theme.from}
              accentTo={theme.to}
              previewImage={nextExercise?.imageUrl}
              onComplete={handleRestComplete}
              onSkip={handleRestComplete}
            />
          </div>
        )}

        {toast && (
          <div
            className="absolute left-1/2 top-3 z-30 w-[calc(100%-2rem)] max-w-sm -translate-x-1/2 rounded-2xl bg-slate-800 px-4 py-3 text-center text-sm text-red-200 shadow-xl ring-1 ring-red-500/40 animate-slide-up"
            role="status"
          >
            {toast}
          </div>
        )}
      </div>

      {/* Rückfrage beim Beenden */}
      {confirmExit && (
        <div
          className="fixed inset-0 z-40 flex items-end justify-center bg-slate-950/80 px-safe-3 pb-safe-3 backdrop-blur-sm animate-fade-in sm:items-center"
          role="dialog"
          aria-modal="true"
          aria-labelledby="exit-title"
          onClick={() => setConfirmExit(false)}
        >
          <div
            className="w-full max-w-md rounded-3xl bg-slate-900 p-5 shadow-2xl ring-1 ring-white/10 animate-sheet-up"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="mx-auto mb-4 h-1.5 w-10 rounded-full bg-slate-700" aria-hidden="true" />
            <h2 id="exit-title" className="text-xl font-bold text-white">Training beenden?</h2>
            <p className="mb-5 mt-1 text-base text-slate-400">
              Dein Fortschritt bleibt gespeichert – du kannst später weitermachen.
            </p>
            <div className="flex flex-col gap-2">
              <Button block onClick={onExit}>
                Beenden, später weitermachen
              </Button>
              {completedCount > 0 && (
                <Button variant="success" block onClick={() => finish(completedSets, abortedExercises)}>
                  Jetzt abschließen ({completedCount} {completedCount === 1 ? 'Übung' : 'Übungen'})
                </Button>
              )}
              <Button variant="danger" size="md" block onClick={handleDiscard} className="min-h-12">
                Verwerfen
              </Button>
              <Button variant="ghost" size="md" block onClick={() => setConfirmExit(false)} className="min-h-12">
                Weiter trainieren
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
