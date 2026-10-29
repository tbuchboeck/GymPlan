import { useState } from 'react';
import { TriangleAlert } from 'lucide-react';
import type { Exercise } from '../types';
import { formatAmount } from '../utils/format';
import type { PlanTheme } from '../utils/plan-theme';
import { Button } from './ui/Button';

interface ExerciseCardProps {
  exercise: Exercise;
  currentSet: number;
  exerciseNumber: number;
  totalExercises: number;
  theme: PlanTheme;
  onAbort?: () => void;
}

/** Inhalt einer Übung: Animation groß oben, darunter Name, Satz-Fortschritt und Anleitung. */
export function ExerciseCard({ exercise, currentSet, exerciseNumber, totalExercises, theme, onAbort }: ExerciseCardProps) {
  const [imageFailed, setImageFailed] = useState(false);
  const showImage = !!exercise.imageUrl && !imageFailed;
  const Icon = theme.icon;

  return (
    <article className="animate-slide-up">
      {/* Animation – Platz reserviert, damit beim Laden nichts springt */}
      <div className="relative aspect-[4/3] w-full overflow-hidden rounded-3xl bg-gradient-to-b from-slate-800 to-slate-900 shadow-xl shadow-black/40 ring-1 ring-white/5">
        {showImage ? (
          <img
            src={exercise.imageUrl}
            alt={exercise.name}
            onError={() => setImageFailed(true)}
            className="h-full w-full object-contain"
          />
        ) : (
          <div className="grid h-full w-full place-items-center">
            <span className={`grid h-20 w-20 place-items-center rounded-3xl bg-gradient-to-br ${theme.gradient} text-white`}>
              <Icon className="h-10 w-10" />
            </span>
          </div>
        )}
      </div>

      {/* Name & Menge */}
      <div className="mt-5 px-1">
        <p className={`text-sm font-semibold ${theme.text}`}>
          Übung {exerciseNumber} von {totalExercises}
        </p>
        <h2 className="mt-0.5 text-[1.75rem] font-bold leading-tight tracking-tight text-white">{exercise.name}</h2>
      </div>

      {/* Nerven-/Dehnübung: sofort abbrechen können */}
      {exercise.caution && onAbort && (
        <Button variant="danger" size="lg" block onClick={onAbort} className="mt-4 text-base!">
          <TriangleAlert className="h-5 w-5" />
          Kribbelt / zieht – abbrechen
        </Button>
      )}
      {/* Satz-Fortschritt */}
      <section className="mt-4 rounded-3xl bg-slate-900 p-4 ring-1 ring-white/5" aria-label="Satz-Fortschritt">
        <div className="flex items-end justify-between gap-3">
          <div>
            <div className="text-xs font-medium uppercase tracking-wider text-slate-500">Satz</div>
            <div className="text-2xl font-bold tabular-nums text-white">
              {currentSet} <span className="text-lg font-medium text-slate-500">von {exercise.sets}</span>
            </div>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-white">{formatAmount(exercise)}</div>
            <div className="text-sm text-slate-400">{exercise.weight > 0 ? `${exercise.weight} kg` : 'Körpergewicht'}</div>
          </div>
        </div>
        <div className="mt-3 flex gap-1.5">
          {Array.from({ length: exercise.sets }, (_, i) => i + 1).map((setNumber) => {
            const isCompleted = setNumber < currentSet;
            const isCurrent = setNumber === currentSet;
            return (
              <div
                key={setNumber}
                className={`h-2.5 flex-1 rounded-full transition-colors duration-300 ${
                  isCompleted ? 'bg-emerald-500' : isCurrent ? `bg-gradient-to-r ${theme.gradient}` : 'bg-slate-800'
                }`}
                aria-label={`Satz ${setNumber}${isCompleted ? ': erledigt' : isCurrent ? ': jetzt' : ''}`}
              />
            );
          })}
        </div>
      </section>

      {/* Anleitung */}
      {exercise.instructions && (
        <section className="mt-3 rounded-3xl bg-slate-900 p-4 ring-1 ring-white/5">
          <h3 className="mb-1.5 text-xs font-semibold uppercase tracking-wider text-slate-500">So geht’s</h3>
          <p className="text-base leading-relaxed text-slate-200">{exercise.instructions}</p>
        </section>
      )}

    </article>
  );
}
