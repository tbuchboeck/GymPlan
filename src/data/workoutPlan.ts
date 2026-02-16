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
      name: "Brustpresse sitzend",
      sets: 3,
      reps: 15,
      weight: 15,
      rest: 50,
      instructions: "Sitzend nach vorne drücken, Schultern bleiben hinten, kontrollierte Bewegung",
      imageUrl: "/exercise-images/brustpresse-sitzend.svg"
    },
    {
      id: 7,
      name: "Vertikales Rudern",
      sets: 3,
      reps: 15,
      weight: 15,
      rest: 50,
      instructions: "Brust an Polster, Griffe auf Schulterhöhe greifen, Ellbogen nach hinten ziehen, Schulterblätter zusammen",
      imageUrl: "/exercise-images/vertical-row.svg"
    },
    {
      id: 8,
      name: "Tiefes Rudern",
      sets: 3,
      reps: 15,
      weight: 15,
      rest: 50,
      instructions: "Adjustable Pulley unten, Griff mit beiden Händen greifen, Rudern zur Hüfte, Rücken gerade, Schulterblätter zusammenziehen",
      imageUrl: "/exercise-images/low-row.svg"
    },
    {
      id: 9,
      name: "Butterfly Maschine",
      sets: 3,
      reps: 15,
      weight: 5,
      rest: 50,
      instructions: "Reverse Ausführung, Ellbogen auf Schulterhöhe, Halbkreisbewegung, Nacken entspannen",
      imageUrl: "/exercise-images/butterfly.svg"
    },
    {
      id: 10,
      name: "Ruderzug Maschine",
      sets: 3,
      reps: 15,
      weight: 19,
      rest: 50,
      instructions: "Rudern beim Kabelturm, Ellbogen zur Hüfte, Nussknacker hinten",
      imageUrl: "/exercise-images/ruderzug.svg"
    },
    {
      id: 11,
      name: "Rumpfrotation",
      sets: 6,
      reps: 15,
      weight: 15,
      rest: 50,
      instructions: "Oberkörper-Rotation. 6 Sätze abwechselnd: Satz 1 Links, Satz 2 Rechts, Satz 3 Links, Satz 4 Rechts, Satz 5 Links, Satz 6 Rechts. Schulterpolster nutzen, kontrollierte Drehbewegung",
      imageUrl: "/exercise-images/rotary-torso.svg"
    },
    {
      id: 12,
      name: "Bauchpresse",
      sets: 3,
      reps: 15,
      weight: 20,
      rest: 50,
      instructions: "Rolle A hinter Schultern, Rolle B vorne. Kontrollierte Bewegung nach vorne, Bauchmuskeln anspannen",
      imageUrl: "/exercise-images/abdominal-crunch-machine.svg"
    },
    {
      id: 13,
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

// Hanteltraining
export const homeWorkoutPlan: WorkoutPlan = {
  name: "Hanteltraining (@hantel)",
  duration: "Unbegrenzt",
  sessionsPerWeek: 2,
  goal: "Allgemeine Fitness",
  trainer: "Martin Schiendorfer",
  createdAt: "24.10.2025",
  exercises: [
    {
      id: 1,
      name: "Butterfly",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Hanteltraining 2kg - Arme seitlich anheben und vor der Brust zusammenführen",
      imageUrl: "/exercise-images/hantel-butterfly.svg"
    },
    {
      id: 2,
      name: "Trizeps 1",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Hanteltraining 2kg - Hantel über Kopf, Ellbogen fixiert, Unterarm nach oben strecken",
      imageUrl: "/exercise-images/hantel-trizeps.svg"
    },
    {
      id: 3,
      name: "Bizeps",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Hanteltraining 2kg - Bizeps Curls, Ellbogen am Körper fixiert",
      imageUrl: "/exercise-images/hantel-bizeps.svg"
    },
    {
      id: 4,
      name: "Front Raises",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Hanteltraining 2kg - Arme gestreckt nach vorne anheben bis Schulterhöhe",
      imageUrl: "/exercise-images/front-raises.svg"
    },
    {
      id: 5,
      name: "Hammer Curls",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Hanteltraining 2kg - Hanteln mit neutralem Griff (Daumen nach oben) beugen",
      imageUrl: "/exercise-images/hammer-curls.svg"
    },
    {
      id: 6,
      name: "Trizeps 2",
      sets: 3,
      reps: 15,
      weight: 0,
      rest: 60,
      instructions: "Liegestütz-Position, Arme eng am Körper, Trizeps-Liegestütze",
      imageUrl: "/exercise-images/trizeps-boden.svg"
    },
    {
      id: 7,
      name: "Bizeps plus über Kopf",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Hanteltraining 2kg - Bizeps Curl mit anschließendem Überkopfdrücken"
    },
    {
      id: 8,
      name: "Kreuzheben",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Hanteltraining 2kg - Rücken gerade, Hanteln vor dem Körper nach unten und wieder hoch"
    },
    {
      id: 9,
      name: "Butterfly reverse",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Hanteltraining 2kg - Vorgebeugt, Arme seitlich nach außen anheben"
    },
    {
      id: 10,
      name: "Seitheben Frontheben",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Hanteltraining 2kg - Abwechselnd seitlich und frontal anheben"
    },
    {
      id: 11,
      name: "Butterfly Boden",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Hanteltraining 2kg - Auf dem Rücken liegend, Arme seitlich zusammenführen"
    },
    {
      id: 12,
      name: "Sit-ups plus Hanteln",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Hanteltraining 2kg - Sit-ups mit Hantel vor der Brust"
    }
  ]
};

// Cardio Trainingsplan
export const homeWorkoutPlan2: WorkoutPlan = {
  name: "Cardio (@cardio)",
  duration: "Unbegrenzt",
  sessionsPerWeek: 2,
  goal: "Cardio & Beweglichkeit",
  trainer: "Martin Schiendorfer",
  createdAt: "06.12.2025",
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
      name: "Beine Hoch",
      sets: 3,
      reps: 30,
      weight: 0,
      rest: 60,
      instructions: "Auf dem Rücken liegen, Beine abwechselnd anheben und senken (Schere)",
      imageUrl: "/exercise-images/beine-hoch.svg"
    },
    {
      id: 3,
      name: "Bauch Beine Po",
      sets: 3,
      reps: 15,
      weight: 0,
      rest: 60,
      instructions: "Vierfüßlerstand, Bein nach hinten oben strecken (Donkey Kicks)",
      imageUrl: "/exercise-images/bauch-beine-po.svg"
    },
    {
      id: 4,
      name: "Kniebeugen",
      sets: 3,
      reps: 10,
      weight: 0,
      rest: 60,
      instructions: "Arme nach vorne gestreckt, Knie nicht über die Zehenspitzen",
      imageUrl: "/exercise-images/kniebeugen.svg"
    },
    {
      id: 5,
      name: "Knie Schritt",
      sets: 3,
      reps: 10,
      weight: 0,
      rest: 60,
      instructions: "Ausfallschritte, abwechselnd links und rechts",
      imageUrl: "/exercise-images/knie-schritt.svg"
    },
    {
      id: 6,
      name: "Sessel Step-Up",
      sets: 3,
      reps: 10,
      weight: 0,
      rest: 60,
      instructions: "Po-Übung: Auf einen Sessel aufsteigen. 10 Wiederholungen pro Seite, abwechselnd links und rechts. Arme zur Balance nach vorne strecken.",
      imageUrl: "/exercise-images/sessel-step-up.svg"
    },
    {
      id: 7,
      name: "Hula Hoop",
      sets: 1,
      reps: 10, // 10 minutes
      weight: 0,
      rest: 60,
      instructions: "10 Minuten Hula Hoop - Hüften kreisen, Reifen in Bewegung halten",
      imageUrl: "/exercise-images/hula-hoop.svg"
    },
    {
      id: 8,
      name: "Laufband Gehen",
      sets: 1,
      reps: 20, // 20 minutes
      weight: 0,
      rest: 60,
      instructions: "20 Minuten zügiges Gehen auf dem Laufband",
      imageUrl: "/exercise-images/walking.svg"
    },
    {
      id: 9,
      name: "Tanzen",
      sets: 1,
      reps: 20, // 20 minutes
      weight: 0,
      rest: 60,
      instructions: "20 Minuten frei tanzen - Musik genießen und bewegen!",
      imageUrl: "/exercise-images/dancing.svg"
    }
  ]
};

// Rücken-Aufbau Trainingsplan (nach Hexenschuss / LWS-Blockade)
export const backWorkoutPlan: WorkoutPlan = {
  name: "Rücken-Aufbau (@rücken)",
  duration: "Unbegrenzt",
  sessionsPerWeek: 4,
  goal: "Rumpfstabilität & Rückfallprävention",
  trainer: "Physiotherapie-basiert",
  createdAt: "16.02.2026",
  exercises: [
    {
      id: 1,
      name: "Aufwärmen – Locker Gehen",
      sets: 1,
      reps: 2, // 2 Minuten
      weight: 0,
      rest: 30,
      instructions: "2 Minuten locker gehen oder am Stand marschieren. Ziel: Durchblutung, Rücken entspannt in Bewegung bringen. Ruhig atmen.",
      imageUrl: "/exercise-images/marschieren.svg"
    },
    {
      id: 2,
      name: "Glute Bridge (Beckenheben)",
      sets: 3,
      reps: 15,
      weight: 0,
      rest: 45,
      instructions: "Rückenlage, Füße hüftbreit, Knie ca. 90°. Ausatmen, Gesäß anspannen, Becken anheben bis Knie–Hüfte–Schulter eine Linie bilden. Oben 3–5 Sek. halten, dann kontrolliert absenken. Druck über die Fersen, nicht ins Hohlkreuz kippen. Tempo: 2s hoch / 3–5s halten / 2s runter.",
      imageUrl: "/exercise-images/glute-bridge.svg"
    },
    {
      id: 3,
      name: "Dead Bug",
      sets: 3,
      reps: 10, // pro Seite
      weight: 0,
      rest: 45,
      instructions: "Rückenlage, Hüfte/Knie 90° (Tischposition), Arme Richtung Decke. Bauchspannung aufbauen, dann gegengleich: rechtes Bein strecken + linker Arm nach hinten. Rücken bleibt flach am Boden! Zurück zur Mitte, Seite wechseln. Tempo: 3s raus / 1s halten / 3s zurück. 10 Wdh. pro Seite.",
      imageUrl: "/exercise-images/dead-bug.svg"
    },
    {
      id: 4,
      name: "Bird Dog",
      sets: 3,
      reps: 8, // pro Seite
      weight: 0,
      rest: 45,
      instructions: "Vierfüßlerstand: Hände unter Schultern, Knie unter Hüften. Bauchspannung setzen, dann rechtes Bein nach hinten + linker Arm nach vorne strecken. 5 Sek. halten, kontrolliert zurück. Becken bleibt gerade – keine Rotation! Tempo: 2s raus / 5s halten / 2s zurück. 8 Wdh. pro Seite.",
      imageUrl: "/exercise-images/bird-dog.svg"
    },
    {
      id: 5,
      name: "Seitstütz (Knie-Variante)",
      sets: 3,
      reps: 25, // Sekunden halten
      weight: 0,
      rest: 45,
      instructions: "Seitlage, Ellenbogen unter Schulter, Knie angewinkelt. Becken anheben bis Schulter–Hüfte–Knie eine Linie bilden. 20–30 Sek. halten, dann kontrolliert absetzen. Schulter weg vom Ohr, Becken nicht kippen. Ruhig atmen. Beide Seiten!",
      imageUrl: "/exercise-images/side-plank-knee.svg"
    },
    {
      id: 6,
      name: "Cool-Down – Entspanntes Gehen",
      sets: 1,
      reps: 2, // 2 Minuten
      weight: 0,
      rest: 0,
      instructions: "1–2 Minuten entspannt gehen. Kein aggressives Dehnen direkt nach der Einheit nötig. Wenn du dich morgen gleich gut oder besser fühlst, kannst du beim nächsten Mal leicht steigern.",
      imageUrl: "/exercise-images/walking.svg"
    }
  ]
};

// Default export für Kompatibilität
export const workoutPlan = gymWorkoutPlan;
