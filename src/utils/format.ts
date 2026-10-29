import type { Exercise } from '../types';

/** Menge pro Satz, z. B. "15 Wdh", "30 s pro Seite" oder "5 Min". */
export function formatAmount(exercise: Exercise): string {
  const unit =
    exercise.unit === 'seconds' ? 's' : exercise.unit === 'minutes' ? 'Min' : 'Wdh';
  return `${exercise.reps} ${unit}${exercise.perSide ? ' pro Seite' : ''}`;
}

/** Dauer eines Satzes in Sekunden, oder null wenn die Übung nach Wiederholungen zählt. */
export function holdSeconds(exercise: Exercise): number | null {
  if (exercise.unit === 'seconds') return exercise.reps;
  if (exercise.unit === 'minutes') return exercise.reps * 60;
  return null;
}
