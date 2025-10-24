export interface Exercise {
  id: number;
  name: string;
  sets: number;
  reps: number;
  weight: number;
  rest: number; // in seconds
  instructions?: string;
  imageUrl?: string;
}

export interface WorkoutPlan {
  name: string;
  duration: string;
  sessionsPerWeek: number;
  goal: string;
  trainer: string;
  createdAt: string;
  exercises: Exercise[];
}

export interface WorkoutSession {
  id: string;
  date: string;
  planName: string;
  completedExercises: number;
  totalExercises: number;
  duration: number; // in minutes
  notes?: string;
}

export interface ExerciseProgress {
  exerciseId: number;
  completedSets: number;
  notes?: string;
}
