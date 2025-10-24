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
      name: "Adduktionsmaschine",
      sets: 3,
      reps: 15,
      weight: 15,
      rest: 120,
      imageUrl: "https://www.burnfit.io/cdn/shop/files/Hip-Adduction-Machine_1024x1024.gif?v=1684225346"
    },
    {
      id: 2,
      name: "Abduktionsmaschine",
      sets: 3,
      reps: 15,
      weight: 15,
      rest: 120,
      imageUrl: "https://www.burnfit.io/cdn/shop/files/Hip-Abduction-Machine_1024x1024.gif?v=1684225347"
    },
    {
      id: 3,
      name: "Beinpresse horizontal",
      sets: 3,
      reps: 15,
      weight: 50,
      rest: 120,
      instructions: "In den Beinen mind. rechter Winkel, nicht komplett durchstrecken",
      imageUrl: "https://www.burnfit.io/cdn/shop/files/Horizontal-Leg-Press_1024x1024.gif?v=1684225349"
    },
    {
      id: 4,
      name: "Brustpresse",
      sets: 3,
      reps: 15,
      weight: 15,
      rest: 120,
      instructions: "Schultern bleiben hinten, Nacken entspannen, Griffe auf Mitte Brust, Ellbogen bleibt auf Griffniveau, Sitzpolster Stufe 5",
      imageUrl: "https://www.burnfit.io/cdn/shop/files/Chest-Press-Machine_1024x1024.gif?v=1684225345"
    },
    {
      id: 5,
      name: "Seitheben Kurzhantel",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 120,
      instructions: "Nacken entspannen, auf Schulterniveau anheben",
      imageUrl: "https://www.burnfit.io/cdn/shop/files/Dumbbell-Lateral-Raise_1024x1024.gif?v=1684225346"
    },
    {
      id: 6,
      name: "Ruderzug Maschine",
      sets: 3,
      reps: 15,
      weight: 19,
      rest: 120,
      instructions: "Rudern beim Kabelturm, Ellbogen zur Hüfte, Nussknacker hinten",
      imageUrl: "https://www.burnfit.io/cdn/shop/files/Cable-Seated-Row_1024x1024.gif?v=1684225345"
    },
    {
      id: 7,
      name: "Butterfly Maschine",
      sets: 3,
      reps: 15,
      weight: 5,
      rest: 120,
      instructions: "Reverse Ausführung, Ellbogen auf Schulterhöhe, Halbkreisbewegung, Nacken entspannen",
      imageUrl: "https://www.burnfit.io/cdn/shop/files/Pec-Deck-Fly_1024x1024.gif?v=1684225350"
    },
    {
      id: 8,
      name: "Crunch",
      sets: 2,
      reps: 15,
      weight: 0,
      rest: 60,
      instructions: "Unterer Rücken bleibt am Boden",
      imageUrl: "https://www.burnfit.io/cdn/shop/files/Crunch_1024x1024.gif?v=1684225346"
    },
    {
      id: 9,
      name: "Heel Touches",
      sets: 2,
      reps: 15,
      weight: 0,
      rest: 60,
      instructions: "Unterer Rücken bleibt am Boden",
      imageUrl: "https://homeworkouts.org/wp-content/uploads/anim-alternating-heel-touches.gif"
    },
    {
      id: 10,
      name: "Hollow Hold",
      sets: 2,
      reps: 15, // 15 seconds
      weight: 0,
      rest: 60,
      instructions: "Bauch bewusst anspannen (15 Sekunden halten)",
      imageUrl: "https://homeworkouts.org/wp-content/uploads/anim-hollow-hold.gif"
    }
  ]
};
