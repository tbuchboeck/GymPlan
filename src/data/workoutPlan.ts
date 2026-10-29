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
      unit: 'minutes',
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
      name: "Trizepszug",
      sets: 3,
      reps: 15,
      weight: 15,
      rest: 50,
      instructions: "Brust an Polster, Griffe auf Schulterhöhe greifen, Ellbogen nach hinten ziehen, Schulterblätter zusammen",
      imageUrl: "/exercise-images/vertical-row.svg"
    },
    {
      id: 6,
      name: "Ruderzug Maschine",
      sets: 3,
      reps: 15,
      weight: 19,
      rest: 50,
      instructions: "Rudern beim Kabelturm, Ellbogen zur Hüfte, Nussknacker hinten",
      imageUrl: "/exercise-images/ruderzug.svg"
    },
    {
      id: 7,
      name: "Schulterpresse",
      sets: 3,
      reps: 15,
      weight: 15,
      rest: 50,
      instructions: "Griffe auf Schulterhöhe, Ellbogen nicht über 90° hinaus, Nacken entspannen, kontrolliert nach oben drücken, nicht komplett durchstrecken",
      imageUrl: "/exercise-images/schulterpresse.svg"
    },
    {
      id: 8,
      name: "Brustpresse sitzend",
      sets: 3,
      reps: 15,
      weight: 15,
      rest: 50,
      instructions: "Sitzend nach vorne drücken, Schultern bleiben hinten, kontrollierte Bewegung",
      imageUrl: "/exercise-images/brustpresse-sitzend.svg"
    },
    {
      id: 9,
      name: "Low Row Maschine",
      sets: 3,
      reps: 15,
      weight: 15,
      rest: 50,
      instructions: "Adjustable Pulley unten, Griff mit beiden Händen greifen, Rudern zur Hüfte, Rücken gerade, Schulterblätter zusammenziehen",
      imageUrl: "/exercise-images/low-row.svg"
    },
    {
      id: 10,
      name: "Rotary Torso",
      sets: 6,
      reps: 15,
      weight: 15,
      rest: 50,
      instructions: "Oberkörper-Rotation. 6 Sätze abwechselnd: Satz 1 Links, Satz 2 Rechts, Satz 3 Links, Satz 4 Rechts, Satz 5 Links, Satz 6 Rechts. Schulterpolster nutzen, kontrollierte Drehbewegung",
      imageUrl: "/exercise-images/rotary-torso.svg"
    },
    {
      id: 11,
      name: "Bauchpresse",
      sets: 3,
      reps: 15,
      weight: 20,
      rest: 50,
      instructions: "Rolle A hinter Schultern, Rolle B vorne. Kontrollierte Bewegung nach vorne, Bauchmuskeln anspannen",
      imageUrl: "/exercise-images/abdominal-crunch-machine.svg"
    },
    {
      id: 12,
      name: "Laufband",
      sets: 1,
      reps: 20, // 20 minutes
      unit: 'minutes',
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
      instructions: "Hanteltraining 2kg - Bizeps Curl mit anschließendem Überkopfdrücken",
      imageUrl: "/exercise-images/bizeps-ueber-kopf.svg"
    },
    {
      id: 8,
      name: "Kreuzheben",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Hanteltraining 2kg - Rücken gerade, Hanteln vor dem Körper nach unten und wieder hoch",
      imageUrl: "/exercise-images/kreuzheben.svg"
    },
    {
      id: 9,
      name: "Butterfly reverse",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Hanteltraining 2kg - Vorgebeugt, Arme seitlich nach außen anheben",
      imageUrl: "/exercise-images/butterfly-reverse.svg"
    },
    {
      id: 10,
      name: "Seitheben Frontheben",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Hanteltraining 2kg - Abwechselnd seitlich und frontal anheben",
      imageUrl: "/exercise-images/seitheben-frontheben.svg"
    },
    {
      id: 11,
      name: "Butterfly Boden",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Hanteltraining 2kg - Auf dem Rücken liegend, Arme seitlich zusammenführen",
      imageUrl: "/exercise-images/butterfly-boden.svg"
    },
    {
      id: 12,
      name: "Sit-ups plus Hanteln",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Hanteltraining 2kg - Sit-ups mit Hantel vor der Brust",
      imageUrl: "/exercise-images/situps-hantel.svg"
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
      name: "Reverse Crunch",
      sets: 3,
      reps: 10,
      weight: 0,
      rest: 60,
      instructions: "Rückenlage, Knie angewinkelt. Knie kontrolliert Richtung Brust ziehen und langsam absenken, ohne den Boden zu berühren. Trainiert den unteren Bauch.",
      imageUrl: "/exercise-images/reverse-crunch.svg"
    },
    {
      id: 8,
      name: "Bauchlage-Beinheben",
      sets: 3,
      reps: 15,
      weight: 0,
      rest: 60,
      instructions: "Bauchlage auf der Matte, Oberkörper leicht angehoben, auf die Unterarme gestützt. Beide Beine gestreckt vom Boden anheben. Trainiert den unteren Rücken und die untere Bauchmuskulatur.",
      imageUrl: "/exercise-images/prone-leg-lifts.svg"
    },
    {
      id: 9,
      name: "Scissor Kicks (Schere)",
      sets: 3,
      reps: 15,
      weight: 0,
      rest: 60,
      instructions: "Bauchlage, Oberkörper aufgestützt. Die gestreckten Beine abwechselnd auf und ab bewegen (Scherenbewegung). Zielt auf den unteren Bauch und die Hüftbeuger.",
      imageUrl: "/exercise-images/scissor-kicks.svg"
    },
    {
      id: 10,
      name: "Bauchlage-Crunch",
      sets: 3,
      reps: 10,
      weight: 0,
      rest: 60,
      instructions: "Bauchlage, Oberkörper aufgestützt. Die Knie abwechselnd angewinkelt Richtung Brust ziehen. Trainiert den gesamten Core.",
      imageUrl: "/exercise-images/prone-crunch.svg"
    },
    {
      id: 11,
      name: "Bicycle Kicks (Bauchlage)",
      sets: 3,
      reps: 15,
      weight: 0,
      rest: 60,
      instructions: "Bauchlage, Oberkörper aufgestützt. Abwechselndes Anziehen und Strecken der Beine in einer Tretbewegung (ähnlich Fahrradfahren). Trainiert den unteren Bauch und die schrägen Bauchmuskeln.",
      imageUrl: "/exercise-images/bicycle-kicks-prone.svg"
    },
    {
      id: 12,
      name: "Reverse Crunch (gestreckt)",
      sets: 3,
      reps: 10,
      weight: 0,
      rest: 60,
      instructions: "Bauchlage, seitlich gestützt. Die Beine angewinkelt anziehen und dann gestreckt wieder absenken. Trainiert die gesamte Rumpfmuskulatur.",
      imageUrl: "/exercise-images/reverse-crunch-extended.svg"
    },
    {
      id: 13,
      name: "Hula Hoop",
      sets: 1,
      reps: 10, // 10 minutes
      unit: 'minutes',
      weight: 0,
      rest: 60,
      instructions: "10 Minuten Hula Hoop - Hüften kreisen, Reifen in Bewegung halten",
      imageUrl: "/exercise-images/hula-hoop.svg"
    },
    {
      id: 14,
      name: "Laufband Gehen",
      sets: 1,
      reps: 20, // 20 minutes
      unit: 'minutes',
      weight: 0,
      rest: 60,
      instructions: "20 Minuten zügiges Gehen auf dem Laufband",
      imageUrl: "/exercise-images/walking.svg"
    },
    {
      id: 15,
      name: "Tanzen",
      sets: 1,
      reps: 20, // 20 minutes
      unit: 'minutes',
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
      unit: 'minutes',
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
      perSide: true,
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
      perSide: true,
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
      unit: 'seconds',
      perSide: true,
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
      unit: 'minutes',
      weight: 0,
      rest: 0,
      instructions: "1–2 Minuten entspannt gehen. Kein aggressives Dehnen direkt nach der Einheit nötig. Wenn du dich morgen gleich gut oder besser fühlst, kannst du beim nächsten Mal leicht steigern.",
      imageUrl: "/exercise-images/walking.svg"
    }
  ]
};

// Nacken, Schulter & BWS – Mobilisation, Haltung, Nerve Glides
export const neckWorkoutPlan: WorkoutPlan = {
  name: "Nacken, Schulter & BWS (@nacken)",
  duration: "Unbegrenzt",
  sessionsPerWeek: 4,
  goal: "BWS-Mobilität, Schulterhaltung & Nackenentlastung",
  trainer: "Physiotherapie-basiert",
  createdAt: "29.10.2026",
  exercises: [
    {
      id: 1,
      name: "Bauch- und Rippenatmung",
      sets: 1,
      reps: 5, // 3–5 Minuten
      unit: 'minutes',
      weight: 0,
      rest: 30,
      instructions: "Startposition: Rückenlage mit aufgestellten Beinen oder aufrecht sitzen. Eine Hand auf dem Bauch, eine seitlich an den Rippen. Einatmen 4 s: Durch die Nase erst in den Bauch, dann seitlich in die Rippen atmen. Die Hände werden nach außen geschoben, die Schultern bleiben unten. Ausatmen 6 s: Langsam durch den Mund ausatmen, Rippen sinken zurück, Nacken und Schultern lösen. Täglich 3–5 Min., kombinierbar mit Rolle und Open Book: in die gedehnte Seite atmen. Wichtig: Hebt sich beim Einatmen die Schulter, arbeiten die Treppenmuskeln am Hals mit. Dann flacher und tiefer in Bauch und Rippen atmen. Entspannt die Treppenmuskeln am Hals, zwischen denen die Armnerven verlaufen. Bei akutem Ziehen im Arm: erst 5 tiefe Atemzüge, dann Chin Tucks.",
      imageUrl: "/exercise-images/bauch-rippenatmung.svg"
    },
    {
      id: 2,
      name: "Extension über die Rolle (Faszienrolle)",
      sets: 1,
      reps: 2, // 1–2 Minuten, 3–4 Segmente
      unit: 'minutes',
      weight: 0,
      rest: 30,
      instructions: "Startposition: Rolle quer unter die mittlere BWS, Knie gebeugt, Füße und Gesäß am Boden. Hände am Hinterkopf, Ellbogen nach vorn, Kinn leicht zur Brust. Absinken: Oberkörper langsam über die Rolle nach hinten sinken lassen, ausatmen. Kein Hohlkreuz in der LWS. Endposition: 2–3 Atemzüge halten, zurück, Rolle eine Handbreit nach oben schieben. Segmentweise nach oben wandern, die LWS bleibt am Boden. Wichtig: Nur BWS, nie Lenden- oder Halswirbelsäule über die Rolle legen – nie unter den Nacken.",
      imageUrl: "/exercise-images/bws-rolle.svg"
    },
    {
      id: 3,
      name: "Open Book",
      sets: 1,
      reps: 10, // 8–10 pro Seite
      perSide: true,
      weight: 0,
      rest: 30,
      instructions: "Startposition: Seitenlage, Kopf auf einem Kissen, Knie 90° gebeugt und aufeinander, Arme gestreckt nach vorn, Handflächen zusammen. Aufdrehen: Oberen Arm im Bogen zur anderen Seite öffnen, Blick folgt der Hand. Knie bleiben zusammen. Endposition: Brust zeigt zur Decke, 2 Atemzüge halten, langsam zurück. Die Drehung kommt aus der BWS, nicht aus der Hüfte. 8–10 pro Seite. Wichtig: Knie dürfen nicht auseinanderrutschen, sonst dreht die LWS mit.",
      imageUrl: "/exercise-images/open-book.svg"
    },
    {
      id: 4,
      name: "Katze-Kuh (BWS-Fokus)",
      sets: 1,
      reps: 10,
      weight: 0,
      rest: 30,
      instructions: "Startposition: Vierfüßlerstand, Hände unter den Schultern, Knie unter der Hüfte. Runden: Zwischen den Schulterblättern nach oben schieben, Kopf locker hängen lassen. Strecken: Brustbein nach vorn-unten sinken lassen, Blick schräg nach vorn. Bewegung bewusst in den mittleren Rücken legen, langsam und mit der Atmung gekoppelt. Lendenbereich so ruhig wie möglich halten. Tipp: Wenn die BWS nicht mitgeht, Hände auf einen Stuhl – dann ist es leichter isoliert.",
      imageUrl: "/exercise-images/katze-kuh.svg"
    },
    {
      id: 5,
      name: "Thread the Needle",
      sets: 1,
      reps: 8, // pro Seite
      perSide: true,
      weight: 0,
      rest: 30,
      instructions: "Startposition: Vierfüßlerstand, Hände unter den Schultern, Knie unter der Hüfte, Gewicht gleichmäßig verteilt. Durchfädeln: Rechten Arm unter dem Körper nach links schieben, Schulter und Schläfe sinken Richtung Boden. Aufdrehen: Arm zurückholen und im Bogen zur Decke öffnen, Blick folgt der Hand, Brust öffnet sich. Hüfte bleibt über den Knien, nur der Oberkörper dreht. 8 pro Seite. Wichtig: Im Durchfädeln nicht auf den Nacken legen. Die Schulter trägt, nicht der Kopf.",
      imageUrl: "/exercise-images/thread-the-needle.svg"
    },
    {
      id: 6,
      name: "Brustdehnung im Türrahmen",
      sets: 2,
      reps: 30, // Sekunden halten, pro Seite
      unit: 'seconds',
      perSide: true,
      weight: 0,
      rest: 30,
      instructions: "Startposition: Unterarm senkrecht am Türrahmen, Ellbogen 90° auf Schulterhöhe, ein Fuß vorn. Schulterblatt zurück und nach unten. Vorlehnen: Mit dem Körper langsam nach vorn lehnen (nicht mit der Schulter), bis die Brust zieht. Schulter bleibt unten. Halten: 30 Sekunden ruhig atmen, beide Seiten. Ellbogen etwas höher = mehr unterer Brustmuskel. Wichtig: Ziehen in der Brust ist ok – Kribbeln oder Einschießen in Hand oder Arm heißt: Nerv gereizt, Spannung sofort reduzieren.",
      imageUrl: "/exercise-images/tuerrahmen-dehnung.svg"
    },
    {
      id: 7,
      name: "Y-T-W in Bauchlage",
      sets: 2,
      reps: 10, // 8–10 pro Buchstabe
      weight: 0,
      rest: 45,
      instructions: "Bauchlage, Stirn auf einem kleinen Handtuch, Beine lang. Y: Arme schräg nach vorn in Y-Form, Daumen nach oben. Schulterblätter zurück und runter, Arme 2–3 cm heben, 2 s halten. T: Arme seitlich ausstrecken, Daumen nach oben. Gleiche Bewegung: erst Schulterblätter, dann Arme heben. W: Ellbogen an die Rippen ziehen, Hände neben den Schultern. Ellbogen und Hände anheben, Schulterblätter zusammen. Langsam ablegen. Ohne Gewicht starten. Variante (mehr Bewegungsweg): auf der Hyperextension-Bank mit frei hängenden Armen. Wichtig: Kopf bleibt in Verlängerung der Wirbelsäule. Nicht nach vorn schauen, sonst arbeitet der Nacken mit.",
      imageUrl: "/exercise-images/ytw.svg"
    },
    {
      id: 8,
      name: "Wall Angels",
      sets: 2,
      reps: 10,
      weight: 0,
      rest: 45,
      instructions: "Startposition: Rücken, Hinterkopf und Gesäß an der Wand, Füße eine Fußlänge vor der Wand. Arme in U-Form an der Wand. Rippen unten halten, kein Hohlkreuz. Hochgleiten: Arme an der Wand langsam nach oben schieben, so weit Handrücken und Ellbogen Kontakt halten. Runterziehen: Ellbogen Richtung Rippen ziehen, Schulterblätter nach unten – das ist der eigentliche Arbeitsteil. Tipp: Bei steifer BWS ist der Bewegungsweg anfangs klein. Das ist normal und wird mit der Mobilisation besser.",
      imageUrl: "/exercise-images/wall-angels.svg"
    },
    {
      id: 9,
      name: "Face Pulls (Sling)",
      sets: 3,
      reps: 12, // 10–12
      weight: 0,
      rest: 45,
      instructions: "Sling auf Kopfhöhe befestigen, Griffe mit gestreckten Armen fassen. Erst Schulterblätter zurück und nach unten Richtung Gesäßtasche, dann Griffe Richtung Gesicht ziehen, Ellbogen hoch und nach außen. Kurz halten, kontrolliert zurück. Wichtig: Schulterblätter zusätzlich nach unten ziehen, nicht nur zusammen – so arbeitet der mittlere und untere Trapez und der obere wird entlastet.",
      imageUrl: "/exercise-images/face-pulls.svg"
    },
    {
      id: 10,
      name: "Reverse Flys (Sling)",
      sets: 3,
      reps: 12, // 10–12
      weight: 0,
      rest: 45,
      instructions: "Griffe mit leicht gebeugten Armen vor der Brust fassen. Erst Schulterblätter zurück und nach unten Richtung Gesäßtasche, dann Arme im Bogen seitlich öffnen. Kurz halten, kontrolliert zurück. Wichtig: Schulterblätter zusätzlich nach unten ziehen, nicht nur zusammen. Schultern bleiben weg von den Ohren.",
      imageUrl: "/exercise-images/reverse-flys.svg"
    },
    {
      id: 11,
      name: "Chin Tucks",
      sets: 1,
      reps: 10, // je 5 Sekunden halten
      weight: 0,
      rest: 30,
      instructions: "Startposition: Aufrecht sitzen oder stehen, Schultern locker, Blick geradeaus. Zurückschieben: Kinn waagrecht nach hinten schieben (Doppelkinn), nicht nach unten nicken. Blick bleibt auf Augenhöhe. Halten: 5 Sekunden halten, Nacken wird hinten lang. Locker lösen. Mehrmals täglich, auch am Schreibtisch: einmal pro Stunde ein paar Chin Tucks und Schulterkreise nach hinten bringen oft mehr als eine lange Einheit am Abend. Wichtig: Sanfter Zug im oberen Nacken ist gut. Kein Druck in den Kiefer.",
      imageUrl: "/exercise-images/chin-tuck.svg"
    },
    {
      id: 12,
      name: "Seitliche Nackendehnung",
      sets: 2,
      reps: 30, // Sekunden halten, pro Seite
      unit: 'seconds',
      perSide: true,
      weight: 0,
      rest: 30,
      instructions: "Startposition: Auf einem Stuhl sitzen, rechte Hand unter das Gesäß klemmen – das fixiert die Schulter. Neigen: Kopf zur linken Seite neigen, Ohr Richtung Schulter, Schulter bleibt unten. Halten: Nase leicht Richtung linke Achsel drehen (für den Levator), 30 s halten, ruhig atmen. Kein Ziehen am Kopf mit der Hand. Dann Seite wechseln. Wichtig: Zieht es bis in den Arm, Neigung verringern – die Dehnung bleibt im Nacken.",
      imageUrl: "/exercise-images/nackendehnung.svg"
    },
    {
      id: 13,
      name: "Nerve Glide (Ulnaris, rechts)",
      sets: 1,
      reps: 10, // 5–10 sanft, nur rechts
      weight: 0,
      rest: 30,
      instructions: "Nur rechts, wo Ring- und kleiner Finger betroffen sind. Erst die tiefe Atmung, dann der Glide. Startposition: Rechter Arm seitlich ausgestreckt auf Schulterhöhe, Handfläche nach vorn, Kopf neutral. Gleiten: Ellbogen beugen, Hand Richtung Ohr führen, Finger zeigen nach hinten (Maske ums Auge). Gleichzeitig Kopf nach rechts neigen. Zurück: Arm wieder strecken und Kopf nach links neigen. Rhythmisch hin und her, langsam, nie halten. Wichtig: Der Ulnaris reagiert empfindlich. Kein Einschießen, kein zunehmendes Kribbeln. Am nächsten Tag darf es nicht schlimmer sein. Ärztlich abklären, wenn Taubheit, Kribbeln oder Kraftverlust in Hand oder Arm dazukommen oder die Schmerzen häufiger werden. Hält es an, klärt eine NLG-Messung, ob der Nerv am Ellbogen oder an der HWS gereizt ist.",
      imageUrl: "/exercise-images/ulnaris-glide.svg"
    },
    {
      id: 14,
      name: "Nerve Glide (Medianus)",
      sets: 1,
      reps: 10, // 5–10 sanft
      weight: 0,
      rest: 30,
      instructions: "Startposition: Arm seitlich auf Schulterhöhe, Ellbogen gebeugt, Handfläche zum Ohr. Kopf neutral. Gleiten: Ellbogen strecken und Handgelenk nach hinten kippen, gleichzeitig Kopf zur selben Seite neigen. Zurück: Ellbogen beugen und Kopf zur Gegenseite neigen. Rhythmisch hin und her, nie halten. Die Bewegung ist ein Gleiten, keine Dehnung – nur leichter Zug, nie Schmerz. Ulnaris- und Radialis-Varianten von der Physio zeigen lassen. Wichtig: Kein Einschießen, kein zunehmendes Kribbeln. Wenn doch: sofort aufhören, nicht mehr in dieser Woche.",
      imageUrl: "/exercise-images/medianus-glide.svg"
    }
  ]
};

// Morgen-Reset – 10-teilige Routine zum Wachwerden, 100 % Nasenatmung
export const morningWorkoutPlan: WorkoutPlan = {
  name: "Morgen-Reset (@morgen)",
  duration: "Unbegrenzt",
  sessionsPerWeek: 7,
  goal: "Wach werden, Wirbelsäule & Schultern lockern",
  trainer: "Eigene Routine",
  createdAt: "29.10.2026",
  exercises: [
    {
      id: 1,
      name: "Lymphatisches Hüpfen",
      sets: 1,
      reps: 1, // 1 Minute
      unit: 'minutes',
      weight: 0,
      rest: 10,
      instructions: "Locker auf den Fußballen hüpfen, Knie weich, Arme hängen entspannt. Beim Hochspringen einatmen, beim Landen ausatmen – durch die Nase. Schultern bleiben unten und locker. Die ganze Routine 100 % durch die Nase atmen."
    },
    {
      id: 2,
      name: "Bodywaves",
      sets: 1,
      reps: 1, // 1 Minute
      unit: 'minutes',
      weight: 0,
      rest: 10,
      instructions: "Sanfte Wellenbewegung von Becken über Bauch und Brust bis zum Kopf für eine geschmeidige Wirbelsäule. Die Welle vor allem durch den mittleren Rücken (BWS) laufen lassen, der Nacken folgt nur locker, kein Kopfnicken. Die ganze Routine 100 % durch die Nase atmen."
    },
    {
      id: 3,
      name: "Armswings",
      sets: 1,
      reps: 1, // 1 Minute
      unit: 'minutes',
      weight: 0,
      rest: 10,
      instructions: "Arme locker vor dem Körper kreuzen und weit nach hinten öffnen. Öffnet den Brustkorb und befreit die Schultern. Schwung aus dem Oberkörper, nicht reißen. Wichtig: Zieht oder kribbelt es im rechten Arm, Bewegung kleiner machen. Die ganze Routine 100 % durch die Nase atmen."
    },
    {
      id: 4,
      name: "Trunk Twists",
      sets: 1,
      reps: 1, // 1 Minute
      unit: 'minutes',
      weight: 0,
      rest: 10,
      instructions: "Hüftbreit stehen, Oberkörper locker nach links und rechts drehen, die Arme schwingen mit. Rumpfrotation zur Aktivierung des Rückens. Die Drehung kommt aus der BWS, Knie weich, Becken bleibt ruhig. Die ganze Routine 100 % durch die Nase atmen."
    },
    {
      id: 5,
      name: "Hip Twist Hops",
      sets: 1,
      reps: 1, // 1 Minute
      unit: 'minutes',
      weight: 0,
      rest: 10,
      instructions: "Kleine Hopser, bei denen sich Hüfte und Beine zur einen Seite drehen und der Oberkörper zur anderen. Dynamisch, aber leichtfüßig landen. Die ganze Routine 100 % durch die Nase atmen."
    },
    {
      id: 6,
      name: "Dead Arms",
      sets: 1,
      reps: 1, // 1 Minute
      unit: 'minutes',
      weight: 0,
      rest: 10,
      instructions: "Arme komplett locker hängen lassen und aus Schultern und Oberkörper ausschütteln. Schüttelt festgefahrene Spannung aus den Armen. Schultern dabei bewusst weg von den Ohren sinken lassen. Die ganze Routine 100 % durch die Nase atmen."
    },
    {
      id: 7,
      name: "Golferswings",
      sets: 1,
      reps: 1, // 1 Minute
      unit: 'minutes',
      weight: 0,
      rest: 10,
      instructions: "Wie beim Golfschwung diagonal von unten-seitlich nach oben über die andere Schulter schwingen, Gewicht verlagert sich mit. Befreit die Diagonalketten des Körpers. Beide Seiten gleich oft. Die ganze Routine 100 % durch die Nase atmen."
    },
    {
      id: 8,
      name: "Standard March",
      sets: 1,
      reps: 1, // 1 Minute
      unit: 'minutes',
      weight: 0,
      rest: 10,
      instructions: "Am Stand marschieren, Knie heben und mit der gegengleichen Hand antippen. Kreuzbewegungen zur Gehirn-Synchronisation. Aufrecht bleiben, Kinn leicht zurück. Die ganze Routine 100 % durch die Nase atmen."
    },
    {
      id: 9,
      name: "Ballet Squat",
      sets: 1,
      reps: 1, // 1 Minute
      unit: 'minutes',
      weight: 0,
      rest: 10,
      instructions: "Breiter Stand, Füße und Knie nach außen gedreht, langsam tief in die Hocke und wieder hoch. Kräftigt Beine und Beckenboden in tiefer Öffnung. Knie zeigen in Richtung der Zehen, Rücken lang. Die ganze Routine 100 % durch die Nase atmen."
    },
    {
      id: 10,
      name: "Horse Stance / Horse Dance",
      sets: 1,
      reps: 1, // 1 Minute
      unit: 'minutes',
      weight: 0,
      rest: 10,
      instructions: "Tief und breit stehen wie im Reitersitz, Hüfte bewusst nach vorne und hinten rollen, locker in Bewegung bleiben. Oberkörper aufrecht, Schultern entspannt. Die ganze Routine 100 % durch die Nase atmen."
    }
  ]
};

// Default export für Kompatibilität
export const workoutPlan = gymWorkoutPlan;
