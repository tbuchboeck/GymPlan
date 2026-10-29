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

// Anzeigenamen der Pläne. Der volle Name (mit altem „@“-Kürzel) bleibt intern
// der Schlüssel, unter dem Trainings gespeichert und synchronisiert sind.
const PLAN_TITLES: Record<string, string> = {
  'Ganzkörper-Trainingsplan (@gym)': 'Gym-Training',
  'Hanteltraining (@hantel)': 'Hanteltraining',
  'Cardio (@cardio)': 'Cardio',
  'Rücken-Aufbau (@rücken)': 'Rücken-Aufbau',
  'Nacken, Schulter & BWS (@nacken)': 'Nacken & Schulter',
  'Morgen-Reset (@morgen)': 'Morgen-Routine',
};

export function planTitle(name: string): string {
  return PLAN_TITLES[name] ?? name.replace(/\s*\(@[^)]*\)\s*$/, '');
}
