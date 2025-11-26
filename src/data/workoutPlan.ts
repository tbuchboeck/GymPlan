import type { WorkoutPlan } from '../types';

// Gym Trainingsplan
export const gymWorkoutPlan: WorkoutPlan = {
  name: "Ganzkörper-Trainingsplan (@gym)",
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
      imageUrl: "/exercise-images/ellipsentrainer.svg"
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
      name: "Rotary Torso",
      sets: 6,
      reps: 15,
      weight: 15,
      rest: 50,
      instructions: "Oberkörper-Rotation. 6 Sätze abwechselnd: Satz 1 Links, Satz 2 Rechts, Satz 3 Links, Satz 4 Rechts, Satz 5 Links, Satz 6 Rechts. Schulterpolster nutzen, kontrollierte Drehbewegung",
      imageUrl: "/exercise-images/rotary-torso.svg"
    },
    {
      id: 9,
      name: "Abdominal Crunch Maschine",
      sets: 3,
      reps: 15,
      weight: 20,
      rest: 50,
      instructions: "Rolle A hinter Schultern, Rolle B vorne. Kontrollierte Bewegung nach vorne, Bauchmuskeln anspannen",
      imageUrl: "/exercise-images/abdominal-crunch-machine.svg"
    },
    {
      id: 10,
      name: "Laufband",
      sets: 1,
      reps: 20, // 20 minutes
      weight: 0,
      rest: 50,
      instructions: "20 Minuten auf Laufband",
      imageUrl: "/exercise-images/laufband.svg"
    }
  ]
};

// Home Trainingsplan
export const homeWorkoutPlan: WorkoutPlan = {
  name: "Home-Trainingsplan (@home)",
  duration: "Unbegrenzt",
  sessionsPerWeek: 2,
  goal: "Allgemeine Fitness",
  trainer: "Martin Schiendorfer",
  createdAt: "24.10.2025",
  exercises: [
    {
      id: 1,
      name: "Sit-Ups",
      sets: 3,
      reps: 10,
      weight: 0,
      rest: 60,
      instructions: "Kontrollierte Ausführung, Nacken entspannt",
      imageUrl: "/exercise-images/situps.svg"
    },
    {
      id: 2,
      name: "Butterfly",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Hanteltraining 2kg - Arme seitlich anheben und vor der Brust zusammenführen",
      imageUrl: "/exercise-images/butterfly.svg"
    },
    {
      id: 3,
      name: "Trizeps",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Hanteltraining 2kg - Hantel über Kopf, Ellbogen fixiert, Unterarm nach oben strecken",
      imageUrl: "/exercise-images/theraband-trizeps.svg"
    },
    {
      id: 4,
      name: "Bizeps",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Hanteltraining 2kg - Bizeps Curls, Ellbogen am Körper fixiert",
      imageUrl: "/exercise-images/theraband-bizeps.svg"
    },
    {
      id: 5,
      name: "Front Raises",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Hanteltraining 2kg - Arme gestreckt nach vorne anheben bis Schulterhöhe",
      imageUrl: "/exercise-images/seitheben.svg"
    },
    {
      id: 6,
      name: "Hammer Curls",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Hanteltraining 2kg - Hanteln mit neutralem Griff (Daumen nach oben) beugen",
      imageUrl: "/exercise-images/theraband-bizeps.svg"
    },
    {
      id: 7,
      name: "Hula Hoop",
      sets: 1,
      reps: 10, // 10 minutes
      weight: 0,
      rest: 60,
      instructions: "10 Minuten Hula Hoop",
      imageUrl: "/exercise-images/hula-hoop.svg"
    },
    {
      id: 8,
      name: "Gehen",
      sets: 1,
      reps: 15, // 15 minutes
      weight: 0,
      rest: 60,
      instructions: "15 Minuten Gehen (z.B. draußen oder auf der Stelle)",
      imageUrl: "/exercise-images/walking.svg"
    },
    {
      id: 9,
      name: "Tanzen",
      sets: 1,
      reps: 15, // 15 minutes
      weight: 0,
      rest: 0,
      instructions: "15 Minuten Tanzen - Viel Spaß!",
      imageUrl: "/exercise-images/dancing.svg"
    }
  ]
};

// Default export für Kompatibilität
export const workoutPlan = gymWorkoutPlan;
