import type { WorkoutPlan } from '../types';

export const workoutPlan: WorkoutPlan = {
  name: "Ganzkörper-Trainingsplan",
  duration: "Unbegrenzt",
  sessionsPerWeek: 2,
  goal: "Allgemeine Fitness",
  trainer: "Martin Schiendorfer",
  createdAt: "24.10.2025",
  exercises: [
    {
      id: 1,
      name: "Ellipsentrainer",
      sets: 1,
      reps: 5, // 5 minutes
      weight: 0,
      rest: 50,
      instructions: "5 Minuten auf Ellipsentrainer",
      imageUrl: "/exercise-images/cardio.svg"
    },
    {
      id: 2,
      name: "Adduktionsmaschine",
      sets: 3,
      reps: 15,
      weight: 15,
      rest: 50,
      imageUrl: "/exercise-images/adduktion.svg"
    },
    {
      id: 3,
      name: "Abduktionsmaschine",
      sets: 3,
      reps: 15,
      weight: 15,
      rest: 50,
      imageUrl: "/exercise-images/abduktion.svg"
    },
    {
      id: 4,
      name: "Beinpresse horizontal",
      sets: 3,
      reps: 15,
      weight: 50,
      rest: 50,
      instructions: "In den Beinen mind. rechter Winkel, nicht komplett durchstrecken",
      imageUrl: "/exercise-images/beinpresse.svg"
    },
    {
      id: 5,
      name: "Brustpresse",
      sets: 3,
      reps: 15,
      weight: 15,
      rest: 50,
      instructions: "Schultern bleiben hinten, Nacken entspannen, Griffe auf Mitte Brust, Ellbogen bleibt auf Griffniveau, Sitzpolster Stufe 5",
      imageUrl: "/exercise-images/brustpresse.svg"
    },
    {
      id: 6,
      name: "Butterfly Maschine",
      sets: 3,
      reps: 15,
      weight: 5,
      rest: 50,
      instructions: "Reverse Ausführung, Ellbogen auf Schulterhöhe, Halbkreisbewegung, Nacken entspannen",
      imageUrl: "/exercise-images/butterfly.svg"
    },
    {
      id: 7,
      name: "Ruderzug Maschine",
      sets: 3,
      reps: 15,
      weight: 19,
      rest: 50,
      instructions: "Rudern beim Kabelturm, Ellbogen zur Hüfte, Nussknacker hinten",
      imageUrl: "/exercise-images/ruderzug.svg"
    },
    {
      id: 8,
      name: "Seitheben Kurzhantel",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 50,
      instructions: "Nacken entspannen, auf Schulterniveau anheben",
      imageUrl: "/exercise-images/seitheben.svg"
    },
    {
      id: 9,
      name: "Laufband",
      sets: 1,
      reps: 20, // 20 minutes
      weight: 0,
      rest: 50,
      instructions: "20 Minuten auf Laufband",
      imageUrl: "/exercise-images/cardio.svg"
    }
  ]
};
