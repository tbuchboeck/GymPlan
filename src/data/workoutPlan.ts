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
      instructions: "5 Min. locker zum Aufwärmen. Aufrecht stehen, ganze Fußsohle bleibt auf den Pedalen, Griffe locker mitbewegen. Tempo so wählen, dass du dich noch unterhalten kannst.",
      imageUrl: "/exercise-images/ellipsentrainer.svg"
    },
    {
      id: 2,
      name: "Adduktionsmaschine",
      sets: 3,
      reps: 15,
      weight: 15,
      rest: 50,
      instructions: "Aufrecht sitzen, Rücken am Polster, Polster an der Innenseite der Knie. Beine langsam zusammendrücken, kurz halten, kontrolliert wieder öffnen. Gewichte nicht aufschlagen lassen.",
      imageUrl: "/exercise-images/adduktion.svg"
    },
    {
      id: 3,
      name: "Abduktionsmaschine",
      sets: 3,
      reps: 15,
      weight: 15,
      rest: 50,
      instructions: "Aufrecht sitzen, Rücken am Polster, Polster an der Außenseite der Knie. Beine langsam nach außen drücken, kurz halten, kontrolliert zurück. Oberkörper bleibt ruhig.",
      imageUrl: "/exercise-images/abduktion.svg"
    },
    {
      id: 4,
      name: "Beinpresse horizontal",
      sets: 3,
      reps: 15,
      weight: 50,
      rest: 50,
      instructions: "In den Beinen mind. rechter Winkel, nicht komplett durchstrecken.",
      imageUrl: "/exercise-images/beinpresse.svg"
    },
    {
      id: 5,
      name: "Rudern sitzend (Brust am Polster)",
      sets: 3,
      reps: 15,
      weight: 15,
      rest: 50,
      instructions: "Brust an Polster, Griffe auf Schulterhöhe greifen, Ellbogen nach hinten ziehen, Schulterblätter zusammen.",
      imageUrl: "/exercise-images/vertical-row.svg"
    },
    {
      id: 6,
      name: "Ruderzug am Kabel",
      sets: 3,
      reps: 15,
      weight: 19,
      rest: 50,
      instructions: "Rudern beim Kabelturm, Ellbogen zur Hüfte, Schulterblätter hinten zusammenziehen.",
      imageUrl: "/exercise-images/ruderzug.svg"
    },
    {
      id: 7,
      name: "Schulterpresse",
      sets: 3,
      reps: 15,
      weight: 15,
      rest: 50,
      instructions: "Griffe auf Schulterhöhe, Ellbogen nicht über 90° hinaus, Nacken entspannen, kontrolliert nach oben drücken, nicht komplett durchstrecken.",
      imageUrl: "/exercise-images/schulterpresse.svg"
    },
    {
      id: 8,
      name: "Brustpresse sitzend",
      sets: 3,
      reps: 15,
      weight: 15,
      rest: 50,
      instructions: "Sitzend nach vorne drücken, Schultern bleiben hinten, kontrollierte Bewegung.",
      imageUrl: "/exercise-images/brustpresse-sitzend.svg"
    },
    {
      id: 9,
      name: "Low Row Maschine",
      sets: 3,
      reps: 15,
      weight: 15,
      rest: 50,
      instructions: "Seilzug unten einstellen, Griff mit beiden Händen greifen, Rudern zur Hüfte, Rücken gerade, Schulterblätter zusammenziehen.",
      imageUrl: "/exercise-images/low-row.svg"
    },
    {
      id: 10,
      name: "Rotary Torso",
      sets: 6,
      reps: 15,
      weight: 15,
      rest: 50,
      instructions: "Oberkörper-Rotation. 6 Sätze abwechselnd: Satz 1 links, Satz 2 rechts, Satz 3 links, Satz 4 rechts, Satz 5 links, Satz 6 rechts. Schulterpolster nutzen, kontrollierte Drehbewegung.",
      imageUrl: "/exercise-images/rotary-torso.svg"
    },
    {
      id: 11,
      name: "Bauchpresse",
      sets: 3,
      reps: 15,
      weight: 20,
      rest: 50,
      instructions: "Rolle A hinter Schultern, Rolle B vorne. Kontrollierte Bewegung nach vorne, Bauchmuskeln anspannen.",
      imageUrl: "/exercise-images/abdominal-crunch-machine.svg"
    },
    {
      id: 12,
      name: "Laufband",
      sets: 1,
      reps: 20, // 20 minutes
      unit: 'minutes',
      weight: 0,
      rest: 0,
      instructions: "20 Min. zügig gehen. Aufrecht bleiben, Blick nach vorn, Arme locker mitschwingen. Tempo so wählen, dass du dich noch unterhalten kannst.",
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
      instructions: "Arme seitlich anheben und vor der Brust zusammenführen.",
      imageUrl: "/exercise-images/hantel-butterfly.svg"
    },
    {
      id: 2,
      name: "Trizeps 1",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Hantel über Kopf, Ellbogen fixiert, Unterarm nach oben strecken.",
      imageUrl: "/exercise-images/hantel-trizeps.svg"
    },
    {
      id: 3,
      name: "Bizeps",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Bizeps-Curls, Ellbogen am Körper fixiert.",
      imageUrl: "/exercise-images/hantel-bizeps.svg"
    },
    {
      id: 4,
      name: "Frontheben",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Arme gestreckt nach vorne anheben bis Schulterhöhe.",
      imageUrl: "/exercise-images/front-raises.svg"
    },
    {
      id: 5,
      name: "Hammer Curls",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Hanteln mit neutralem Griff (Daumen nach oben) beugen.",
      imageUrl: "/exercise-images/hammer-curls.svg"
    },
    {
      id: 6,
      name: "Trizeps 2",
      sets: 3,
      reps: 15,
      weight: 0,
      rest: 60,
      instructions: "Liegestütz-Position, Arme eng am Körper, Trizeps-Liegestütze.",
      imageUrl: "/exercise-images/trizeps-boden.svg"
    },
    {
      id: 7,
      name: "Bizeps plus über Kopf",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Bizeps-Curl mit anschließendem Überkopfdrücken.",
      imageUrl: "/exercise-images/bizeps-ueber-kopf.svg"
    },
    {
      id: 8,
      name: "Kreuzheben",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Füße hüftbreit, Knie leicht gebeugt. Hüfte nach hinten schieben und den Oberkörper mit geradem Rücken vorneigen, Hanteln nah an den Beinen nach unten führen. Über die Hüfte wieder aufrichten.",
      imageUrl: "/exercise-images/kreuzheben.svg"
    },
    {
      id: 9,
      name: "Butterfly reverse",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Knie leicht gebeugt, Oberkörper mit geradem Rücken nach vorn geneigt. Arme leicht gebeugt seitlich bis Schulterhöhe anheben, Schulterblätter zusammen, langsam senken. Nacken bleibt lang.",
      imageUrl: "/exercise-images/butterfly-reverse.svg"
    },
    {
      id: 10,
      name: "Seitheben Frontheben",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Abwechselnd seitlich und frontal anheben.",
      imageUrl: "/exercise-images/seitheben-frontheben.svg"
    },
    {
      id: 11,
      name: "Butterfly Boden",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 60,
      instructions: "Auf dem Rücken liegend, Arme seitlich zusammenführen.",
      imageUrl: "/exercise-images/butterfly-boden.svg"
    },
    {
      id: 12,
      name: "Sit-ups plus Hanteln",
      sets: 3,
      reps: 15,
      weight: 2,
      rest: 0,
      instructions: "Rückenlage, Beine aufgestellt, Hantel mit beiden Händen vor der Brust. Oberkörper langsam aufrollen und kontrolliert wieder ablegen. Nacken locker, ohne Schwung.",
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
      name: "Sit-ups",
      sets: 3,
      reps: 10,
      weight: 0,
      rest: 60,
      instructions: "Kontrollierte Ausführung, Nacken entspannt.",
      imageUrl: "/exercise-images/situps.svg"
    },
    {
      id: 2,
      name: "Beinschere (Rückenlage)",
      sets: 3,
      reps: 15, // pro Seite (30 gesamt)
      perSide: true,
      weight: 0,
      rest: 60,
      instructions: "Auf dem Rücken liegen, Beine abwechselnd anheben und senken (Schere).",
      imageUrl: "/exercise-images/beine-hoch.svg"
    },
    {
      id: 3,
      name: "Bauch Beine Po",
      sets: 3,
      reps: 15,
      perSide: true,
      weight: 0,
      rest: 60,
      instructions: "Vierfüßlerstand, Bein nach hinten oben strecken (Donkey Kicks).",
      imageUrl: "/exercise-images/bauch-beine-po.svg"
    },
    {
      id: 4,
      name: "Kniebeugen",
      sets: 3,
      reps: 10,
      weight: 0,
      rest: 60,
      instructions: "Arme nach vorne gestreckt, Knie zeigen Richtung Zehen, ganze Fußsohle bleibt am Boden.",
      imageUrl: "/exercise-images/kniebeugen.svg"
    },
    {
      id: 5,
      name: "Knie Schritt",
      sets: 3,
      reps: 10,
      perSide: true,
      weight: 0,
      rest: 60,
      instructions: "Ausfallschritte, abwechselnd links und rechts.",
      imageUrl: "/exercise-images/knie-schritt.svg"
    },
    {
      id: 6,
      name: "Sessel Step-Up",
      sets: 3,
      reps: 10,
      perSide: true,
      weight: 0,
      rest: 60,
      instructions: "Po-Übung: Auf einen Sessel aufsteigen. 10 Wdh. pro Seite, abwechselnd links und rechts. Arme zur Balance nach vorne strecken.",
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
      instructions: "Bauchlage auf der Matte, Oberkörper leicht angehoben, auf die Unterarme gestützt. Beide Beine gestreckt nur wenige cm vom Boden anheben, Becken bleibt auf der Matte. Trainiert Gesäß und unteren Rücken.",
      imageUrl: "/exercise-images/prone-leg-lifts.svg"
    },
    {
      id: 9,
      name: "Beinschere (Bauchlage)",
      sets: 3,
      reps: 15,
      weight: 0,
      rest: 60,
      instructions: "Bauchlage, Oberkörper aufgestützt. Die gestreckten Beine abwechselnd wenige cm auf und ab bewegen (Scherenbewegung), Becken bleibt auf der Matte. Trainiert Gesäß und unteren Rücken.",
      imageUrl: "/exercise-images/scissor-kicks.svg"
    },
    {
      id: 10,
      name: "Bauchlage-Crunch",
      sets: 3,
      reps: 10,
      weight: 0,
      rest: 60,
      instructions: "Bauchlage, Oberkörper auf die Unterarme gestützt. Ein Knie seitlich am Boden entlang Richtung Ellbogen ziehen, zurück, dann Seite wechseln. Trainiert die seitliche Rumpf- und Hüftmuskulatur.",
      imageUrl: "/exercise-images/prone-crunch.svg"
    },
    {
      id: 11,
      name: "Bicycle Kicks (Bauchlage)",
      sets: 3,
      reps: 15,
      weight: 0,
      rest: 60,
      instructions: "Bauchlage, Oberkörper aufgestützt. Abwechselndes Anziehen und Strecken der Beine in einer Tretbewegung (ähnlich Fahrradfahren), Becken bleibt auf der Matte. Trainiert Gesäß, Hüfte und Rumpfstabilität.",
      imageUrl: "/exercise-images/bicycle-kicks-prone.svg"
    },
    {
      id: 12,
      name: "Knie-Anzug im Unterarmstütz",
      sets: 3,
      reps: 10,
      weight: 0,
      rest: 60,
      instructions: "Unterarmstütz, Ellbogen unter den Schultern. Die Beine angewinkelt anziehen und dann gestreckt wieder absenken. Trainiert die gesamte Rumpfmuskulatur.",
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
      instructions: "10 Min. Hula-Hoop – Hüften kreisen, Reifen in Bewegung halten.",
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
      instructions: "20 Min. zügiges Gehen auf dem Laufband.",
      imageUrl: "/exercise-images/laufband.svg"
    },
    {
      id: 15,
      name: "Tanzen",
      sets: 1,
      reps: 20, // 20 minutes
      unit: 'minutes',
      weight: 0,
      rest: 0,
      instructions: "20 Min. frei tanzen – Musik genießen und bewegen!",
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
  trainer: "Eigene Zusammenstellung (Physio-Übungen)",
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
      instructions: "2 Min. locker gehen oder am Stand marschieren. Ziel: Durchblutung, Rücken entspannt in Bewegung bringen. Ruhig atmen.",
      imageUrl: "/exercise-images/marschieren.svg"
    },
    {
      id: 2,
      name: "Glute Bridge (Beckenheben)",
      sets: 3,
      reps: 15,
      weight: 0,
      rest: 45,
      instructions: "Rückenlage, Füße hüftbreit, Knie ca. 90°. Ausatmen, Gesäß anspannen, Becken anheben, bis Knie–Hüfte–Schulter eine Linie bilden. Oben 3–5 s halten, dann kontrolliert absenken. Druck über die Fersen, nicht ins Hohlkreuz kippen. Tempo: 2 s hoch / 3–5 s halten / 2 s runter.",
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
      instructions: "Rückenlage, Hüfte/Knie 90° (Tischposition), Arme Richtung Decke. Bauchspannung aufbauen, dann gegengleich: rechtes Bein strecken + linker Arm nach hinten. Rücken bleibt flach am Boden! Zurück zur Mitte, Seite wechseln. Tempo: 3 s raus / 1 s halten / 3 s zurück.",
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
      instructions: "Vierfüßlerstand: Hände unter Schultern, Knie unter Hüften. Bauchspannung setzen, dann rechtes Bein nach hinten + linker Arm nach vorne strecken. 5 s halten, kontrolliert zurück. Becken bleibt gerade – keine Rotation! Tempo: 2 s raus / 5 s halten / 2 s zurück.",
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
      instructions: "Seitlage, Ellbogen unter Schulter, Knie angewinkelt. Becken anheben, bis Schulter–Hüfte–Knie eine Linie bilden. 25 s pro Seite halten, dann kontrolliert absetzen. Schulter weg vom Ohr, Becken nicht kippen. Ruhig atmen.",
      imageUrl: "/exercise-images/side-plank-knee.svg"
    },
    {
      id: 6,
      name: "Abwärmen – Entspanntes Gehen",
      sets: 1,
      reps: 2, // 2 Minuten
      unit: 'minutes',
      weight: 0,
      rest: 0,
      instructions: "1–2 Min. entspannt gehen. Kein aggressives Dehnen direkt nach der Einheit nötig. Wenn du dich morgen gleich gut oder besser fühlst, kannst du beim nächsten Mal leicht steigern.",
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
  trainer: "Eigene Zusammenstellung (Physio-Übungen)",
  createdAt: "29.10.2026",
  notice: "Diese Übungen ersetzen keine ärztliche oder physiotherapeutische Abklärung. Sofort aufhören bei Einschießen, zunehmendem Kribbeln oder Taubheit. Ärztlich abklären lassen bei: zunehmender Taubheit oder Kraftverlust in Hand oder Arm, Ungeschicklichkeit der Hände, Gangunsicherheit, Schwindel oder Sehstörungen bei Kopfbewegungen, starken nächtlichen Schmerzen – oder wenn die Beschwerden häufiger werden oder weiter ausstrahlen.",
  exercises: [
    {
      id: 1,
      name: "Bauch- und Rippenatmung",
      sets: 1,
      reps: 5, // 3–5 Minuten
      unit: 'minutes',
      weight: 0,
      rest: 30,
      instructions: "Rückenlage mit aufgestellten Beinen oder aufrecht sitzen, eine Hand am Bauch, eine seitlich an den Rippen. 4 s durch die Nase in Bauch und Rippen einatmen, 6 s langsam durch den Mund aus. Auch an trainingsfreien Tagen gut. Wichtig: Schultern bleiben unten. Bei Ziehen im Arm: erst 5 tiefe Atemzüge, dann Chin Tucks.",
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
      instructions: "Rolle quer unter die mittlere BWS, Knie gebeugt, Gesäß am Boden, Hände am Hinterkopf. Ausatmend langsam über die Rolle nach hinten sinken, 2–3 Atemzüge halten, zurück. Rolle eine Handbreit höher schieben. Wichtig: Nur die BWS auf die Rolle, nie Lende oder Nacken. Kein Hohlkreuz.",
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
      instructions: "Seitenlage, Kopf auf einem Kissen, Knie 90° gebeugt und aufeinander, Arme gestreckt nach vorn. Oberen Arm im Bogen zur anderen Seite öffnen, Blick folgt der Hand. 2 Atemzüge halten, langsam zurück. Wichtig: Knie bleiben zusammen – die Drehung kommt aus der BWS, nicht aus Hüfte oder Lende.",
      imageUrl: "/exercise-images/open-book.svg"
    },
    {
      id: 4,
      name: "Katze-Kuh (BWS-Fokus)",
      sets: 1,
      reps: 10,
      weight: 0,
      rest: 30,
      instructions: "Vierfüßlerstand, Hände unter den Schultern, Knie unter der Hüfte. Zwischen den Schulterblättern rund machen, Kopf locker hängen lassen. Dann Brustbein nach vorn-unten sinken lassen. Langsam, mit der Atmung. Wichtig: Bewegung im mittleren Rücken, Lende ruhig. Leichter mit den Händen auf einem Stuhl.",
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
      instructions: "Vierfüßlerstand, Hände unter den Schultern, Knie unter der Hüfte. Einen Arm unter dem Körper zur Gegenseite schieben, Schulter sinkt Richtung Boden. Dann den Arm im Bogen zur Decke öffnen, Blick folgt der Hand. Wichtig: Hüfte bleibt über den Knien. Die Schulter trägt, nicht Kopf oder Nacken.",
      imageUrl: "/exercise-images/thread-the-needle.svg"
    },
    {
      id: 6,
      name: "Y-T-W in Bauchlage",
      sets: 2,
      reps: 10, // 8–10 pro Buchstabe
      weight: 0,
      rest: 45,
      instructions: "Je 8–10 pro Buchstabe. Bauchlage, Stirn auf einem Handtuch. Erst Schulterblätter zurück und runter, dann Arme 2–3 cm heben, 2 s halten: Y schräg nach vorn, T seitlich (Daumen oben), W mit Ellbogen an den Rippen. Ohne Gewicht. Variante: Rückenstrecker-Bank. Wichtig: Kopf in Verlängerung der Wirbelsäule, nicht nach vorn schauen.",
      imageUrl: "/exercise-images/ytw.svg"
    },
    {
      id: 7,
      name: "Brustdehnung im Türrahmen",
      sets: 2,
      reps: 30, // Sekunden halten, pro Seite
      unit: 'seconds',
      perSide: true,
      weight: 0,
      rest: 30,
      caution: true,
      instructions: "Unterarm senkrecht am Türrahmen, Ellbogen 90° auf Schulterhöhe, ein Fuß vorn, Schulterblatt zurück und unten. Mit dem ganzen Körper nach vorn lehnen, bis die Brust zieht, 30 s ruhig atmen. Wichtig: Ziehen in der Brust ist ok. Kribbeln oder Einschießen in Hand oder Arm: Spannung sofort reduzieren.",
      imageUrl: "/exercise-images/tuerrahmen-dehnung.svg"
    },
    {
      id: 8,
      name: "Wall Angels",
      sets: 2,
      reps: 10,
      weight: 0,
      rest: 45,
      caution: true,
      instructions: "Rücken, Hinterkopf und Gesäß an der Wand, Füße eine Fußlänge davor, Arme in U-Form, kein Hohlkreuz. Arme hochschieben, solange Handrücken und Ellbogen die Wand berühren, dann Ellbogen Richtung Rippen ziehen. Wichtig: Kleiner Weg ist anfangs normal. Kribbelt es in Ring- oder kleinem Finger: Arme tiefer.",
      imageUrl: "/exercise-images/wall-angels.svg"
    },
    {
      id: 9,
      name: "Face Pulls (Schlingentrainer)",
      sets: 3,
      reps: 12, // 10–12
      weight: 0,
      rest: 45,
      caution: true,
      instructions: "Schlingentrainer auf Kopfhöhe, Griffe mit gestreckten Armen. Erst Schulterblätter zurück und nach unten ziehen, dann Griffe Richtung Gesicht, Ellbogen hoch und außen. Kurz halten, langsam zurück. Wichtig: So arbeiten der mittlere und untere Trapezmuskel. Kribbelt es in Ring- oder kleinem Finger: Ellbogen tiefer.",
      imageUrl: "/exercise-images/face-pulls.svg"
    },
    {
      id: 10,
      name: "Reverse Flys (Schlingentrainer)",
      sets: 3,
      reps: 12, // 10–12
      weight: 0,
      rest: 45,
      instructions: "Griffe mit leicht gebeugten Armen vor der Brust fassen. Erst Schulterblätter zurück und nach unten Richtung Gesäßtasche, dann Arme im Bogen seitlich öffnen. Kurz halten, kontrolliert zurück. Wichtig: Schulterblätter auch nach unten ziehen, nicht nur zusammen. Schultern weg von den Ohren.",
      imageUrl: "/exercise-images/reverse-flys.svg"
    },
    {
      id: 11,
      name: "Chin Tucks",
      sets: 1,
      reps: 10, // je 5 Sekunden halten
      weight: 0,
      rest: 30,
      instructions: "Aufrecht sitzen oder stehen, Blick geradeaus. Kinn waagrecht nach hinten schieben (Doppelkinn), nicht nicken. 5 s halten, der Nacken wird hinten lang, dann lösen. Auch am Schreibtisch: stündlich ein paar Wdh. und Schulterkreise nach hinten. Wichtig: Sanfter Zug im oberen Nacken ist gut, kein Druck in den Kiefer.",
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
      caution: true,
      instructions: "Auf einem Stuhl sitzen, rechte Hand unter das Gesäß klemmen. Kopf nach links neigen, Schulter bleibt unten, Nase leicht Richtung linke Achsel drehen (Schulterblattheber). 30 s ruhig halten, Seite wechseln. Wichtig: Nicht mit der Hand am Kopf ziehen. Zieht es bis in den Arm, Neigung verringern.",
      imageUrl: "/exercise-images/nackendehnung.svg"
    },
    {
      id: 13,
      name: "Nerve Glide (Ulnaris, rechts)",
      sets: 1,
      reps: 10, // 5–10 sanft, nur rechts
      weight: 0,
      rest: 30,
      caution: true,
      instructions: "Nur rechts, nach der Atmung. Arm seitlich auf Schulterhöhe, Handfläche nach vorn. Ellbogen beugen, Hand zum Ohr (Finger zeigen nach hinten), Kopf nach rechts neigen. Zurück: Arm strecken, Kopf nach links. Langsam, nie halten. Wichtig: Kein Einschießen, kein zunehmendes Kribbeln. Wenn doch: sofort aufhören und erst wieder, wenn es 2 Tage ruhig ist – sonst Physio fragen.",
      imageUrl: "/exercise-images/ulnaris-glide.svg"
    },
    {
      id: 14,
      name: "Nerve Glide (Medianus)",
      sets: 1,
      reps: 10, // 5–10 sanft
      weight: 0,
      rest: 0,
      caution: true,
      instructions: "Arm seitlich auf Schulterhöhe, Ellbogen gebeugt, Handfläche zum Ohr. Ellbogen strecken, Handgelenk nach hinten kippen, Kopf zur selben Seite neigen. Zurück: beugen, Kopf zur Gegenseite. Nie halten, nur leichter Zug. Radialis-Variante von der Physio zeigen lassen. Wichtig: Kein Einschießen, kein zunehmendes Kribbeln. Wenn doch: sofort aufhören und erst wieder, wenn es 2 Tage ruhig ist – sonst Physio fragen.",
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
      name: "Lockeres Hüpfen",
      sets: 1,
      reps: 1, // 1 Minute
      unit: 'minutes',
      weight: 0,
      rest: 10,
      instructions: "Locker auf den Fußballen hüpfen, Knie weich, Arme hängen entspannt. Ruhig durch die Nase atmen, nicht im Hüpf-Takt. Schultern bleiben unten und locker. Die ganze Routine 100 % durch die Nase atmen.",
      imageUrl: "/exercise-images/morgen-huepfen.svg"
    },
    {
      id: 2,
      name: "Bodywaves",
      sets: 1,
      reps: 1, // 1 Minute
      unit: 'minutes',
      weight: 0,
      rest: 10,
      instructions: "Sanfte Wellenbewegung von Becken über Bauch und Brust bis zum Kopf. Die Welle vor allem durch den mittleren Rücken (BWS) laufen lassen, der Nacken folgt nur locker, kein Kopfnicken.",
      imageUrl: "/exercise-images/bodywaves.svg"
    },
    {
      id: 3,
      name: "Armswings",
      sets: 1,
      reps: 1, // 1 Minute
      unit: 'minutes',
      weight: 0,
      rest: 10,
      instructions: "Arme locker vor dem Körper kreuzen und weit nach hinten öffnen, die Brust geht dabei mit auf. Schwung aus dem Oberkörper, nicht reißen. Wichtig: Zieht oder kribbelt es im rechten Arm, Bewegung kleiner machen.",
      imageUrl: "/exercise-images/armswings.svg"
    },
    {
      id: 4,
      name: "Trunk Twists",
      sets: 1,
      reps: 1, // 1 Minute
      unit: 'minutes',
      weight: 0,
      rest: 10,
      instructions: "Hüftbreit stehen, Oberkörper locker nach links und rechts drehen, die Arme schwingen mit. Die Drehung kommt aus der BWS, Knie weich, Becken bleibt ruhig.",
      imageUrl: "/exercise-images/trunk-twists.svg"
    },
    {
      id: 5,
      name: "Hip Twist Hops",
      sets: 1,
      reps: 1, // 1 Minute
      unit: 'minutes',
      weight: 0,
      rest: 10,
      instructions: "Kleine Hopser, bei denen sich Hüfte und Beine zur einen Seite drehen und der Oberkörper zur anderen. Klein und weich springen; bei Ziehen im Rücken ohne Hüpfen drehen.",
      imageUrl: "/exercise-images/hip-twist-hops.svg"
    },
    {
      id: 6,
      name: "Dead Arms",
      sets: 1,
      reps: 1, // 1 Minute
      unit: 'minutes',
      weight: 0,
      rest: 10,
      instructions: "Arme komplett locker hängen lassen und aus Schultern und Oberkörper ausschütteln, Hände und Finger schwingen locker mit. Schultern dabei bewusst weg von den Ohren sinken lassen.",
      imageUrl: "/exercise-images/dead-arms.svg"
    },
    {
      id: 7,
      name: "Golfschwung",
      sets: 1,
      reps: 1, // 1 Minute
      unit: 'minutes',
      weight: 0,
      rest: 10,
      instructions: "Wie beim Golfschwung diagonal von unten-seitlich nach oben über die andere Schulter schwingen, Gewicht verlagert sich mit. Knie weich, Schwung aus Hüfte und Oberkörper. Beide Seiten gleich oft.",
      imageUrl: "/exercise-images/golferswings.svg"
    },
    {
      id: 8,
      name: "Standard March",
      sets: 1,
      reps: 1, // 1 Minute
      unit: 'minutes',
      weight: 0,
      rest: 10,
      instructions: "Am Stand marschieren, Knie heben und mit der gegengleichen Hand antippen. Ruhiges, gleichmäßiges Tempo. Aufrecht bleiben, Kinn leicht zurück.",
      imageUrl: "/exercise-images/standard-march.svg"
    },
    {
      id: 9,
      name: "Ballet Squat",
      sets: 1,
      reps: 1, // 1 Minute
      unit: 'minutes',
      weight: 0,
      rest: 10,
      instructions: "Breiter Stand, Füße und Knie nach außen gedreht, langsam in die Hocke und wieder hoch – nur so tief, wie es angenehm ist. Knie zeigen in Richtung der Zehen, Rücken lang.",
      imageUrl: "/exercise-images/ballet-squat.svg"
    },
    {
      id: 10,
      name: "Horse Stance / Horse Dance",
      sets: 1,
      reps: 1, // 1 Minute
      unit: 'minutes',
      weight: 0,
      rest: 0,
      instructions: "Tief und breit stehen wie im Reitersitz, Hüfte bewusst nach vorne und hinten rollen, locker in Bewegung bleiben. Oberkörper aufrecht, Schultern entspannt.",
      imageUrl: "/exercise-images/horse-stance.svg"
    }
  ]
};

// Default export für Kompatibilität
export const workoutPlan = gymWorkoutPlan;
