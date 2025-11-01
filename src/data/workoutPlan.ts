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
      name: "Ausdauertraining",
      sets: 1,
      reps: 15, // 15 minutes
      weight: 0,
      rest: 120,
      instructions: "15 Minuten auf Laufband, Crosstrainer oder ähnlichem Gerät",
      imageUrl: "/exercise-images/cardio.svg"
    },
    {
      id: 2,
      name: "Adduktionsmaschine",
      sets: 3,
      reps: 15,
      weight: 15,
      rest: 120,
      imageUrl: "/exercise-images/adduktion.svg"
    },
    {
      id: 3,
      name: "Abduktionsmaschine",
      sets: 3,
      reps: 15,
      weight: 15,
      rest: 120,
      imageUrl: "/exercise-images/abduktion.svg"
    },
    {
      id: 4,
      name: "Beinpresse horizontal",
      sets: 3,
      reps: 15,
      weight: 50,
      rest: 120,
      instructions: "In den Beinen mind. rechter Winkel, nicht komplett durchstrecken",
      imageUrl: "/exercise-images/beinpresse.svg"
    },
    {
      id: 5,
      name: "Brustpresse",
      sets: 3,
      reps: 15,
      weight: 15,
      rest: 120,
      instructions: "Schultern bleiben hinten, Nacken entspannen, Griffe auf Mitte Brust, Ellbogen bleibt auf Griffniveau, Sitzpolster Stufe 5",
      imageUrl: "/exercise-images/brustpresse.svg"
    },
    {
      id: 6,
      name: "Butterfly Maschine",
      sets: 3,
      reps: 15,
      weight: 5,
      rest: 120,
      instructions: "Reverse Ausführung, Ellbogen auf Schulterhöhe, Halbkreisbewegung, Nacken entspannen",
      imageUrl: "/exercise-images/butterfly.svg"
    },
    {
      id: 7,
      name: "Seitheben Kurzhantel",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 120,
      instructions: "Nacken entspannen, auf Schulterniveau anheben",
      imageUrl: "/exercise-images/seitheben.svg"
    },
    {
      id: 8,
      name: "Ruderzug Maschine",
      sets: 3,
      reps: 15,
      weight: 19,
      rest: 120,
      instructions: "Rudern beim Kabelturm, Ellbogen zur Hüfte, Nussknacker hinten",
      imageUrl: "/exercise-images/ruderzug.svg"
    },
    {
      id: 9,
      name: "Crunch",
      sets: 2,
      reps: 15,
      weight: 0,
      rest: 60,
      instructions: "Unterer Rücken bleibt am Boden",
      imageUrl: "/exercise-images/crunch.svg"
    },
    {
      id: 10,
      name: "Heel Touches",
      sets: 2,
      reps: 15,
      weight: 0,
      rest: 60,
      instructions: "Unterer Rücken bleibt am Boden",
      imageUrl: "/exercise-images/heel-touches.svg"
    },
    {
      id: 11,
      name: "Hollow Hold",
      sets: 2,
      reps: 15, // 15 seconds
      weight: 0,
      rest: 60,
      instructions: "Bauch bewusst anspannen (15 Sekunden halten)",
      imageUrl: "/exercise-images/hollow-hold.svg"
    }
  ]
};
