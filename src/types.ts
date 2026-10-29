export interface Exercise {
  id: number;
  name: string;
  sets: number;
  reps: number;
  unit?: 'reps' | 'seconds' | 'minutes'; // was `reps` zählt, Standard: Wiederholungen
  perSide?: boolean;
  weight: number;
  rest: number; // in seconds
  instructions?: string;
  imageUrl?: string;
  // Nerven-/Dehnübung: im Training gibt es einen Knopf „Kribbelt – abbrechen“,
  // der die Übung überspringt und das in der Session vermerkt.
  caution?: boolean;
}

export interface WorkoutPlan {
  name: string;
  duration: string;
  sessionsPerWeek: number;
  goal: string;
  trainer: string;
  createdAt: string;
  // Wichtiger Hinweis zum ganzen Plan (z. B. wann ärztlich abklären),
  // wird auf der Plan-Übersicht vor den Übungen angezeigt.
  notice?: string;
  exercises: Exercise[];
}

export type Feeling = 'better' | 'same' | 'worse';

export interface WorkoutSession {
  id: string;
  date: string;
  planName: string;
  completedExercises: number; // wirklich abgeschlossene Übungen
  totalExercises: number;
  duration: number; // in minutes
  notes?: string;
  // Nur bei Plänen mit Befindens-Abfrage (Thomas: @rücken, @nacken)
  feeling?: Feeling;
  tingling?: boolean; // Kribbeln/Ziehen im Arm während oder nach dem Training
  abortedExercises?: string[]; // Namen der per „Kribbelt – abbrechen“ übersprungenen Übungen
}

export interface ExerciseProgress {
  exerciseId: number;
  completedSets: number;
  notes?: string;
}
