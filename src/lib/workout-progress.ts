import type { Person } from './auth-service';

// Laufendes Training, damit man nach Neuladen/App-Wechsel weitermachen kann.
export interface WorkoutProgress {
  person: Person;
  planName: string;
  exerciseIndex: number;
  currentSet: number;
  totalExercises: number;
  startedAt: number; // ms seit Epoch
  updatedAt: number;
  completedSets: string[]; // "<Übungsindex>:<Satz>"
  abortedExercises: string[];
}

/** Stand gilt so lange als fortsetzbar. */
export const RESUME_MAX_AGE_MS = 12 * 60 * 60 * 1000;

const progressKey = (person: Person) => `workoutInProgress.${person}`;

export function loadWorkoutProgress(person: Person): WorkoutProgress | null {
  try {
    const raw = localStorage.getItem(progressKey(person));
    if (!raw) return null;
    const p = JSON.parse(raw) as WorkoutProgress;
    if (typeof p !== 'object' || p === null || p.person !== person) return null;
    if (typeof p.exerciseIndex !== 'number' || !Array.isArray(p.completedSets)) return null;
    if (Date.now() - (p.updatedAt ?? 0) > RESUME_MAX_AGE_MS) return null;
    return { ...p, abortedExercises: Array.isArray(p.abortedExercises) ? p.abortedExercises : [] };
  } catch {
    return null;
  }
}

export function saveWorkoutProgress(progress: WorkoutProgress): void {
  try {
    localStorage.setItem(progressKey(progress.person), JSON.stringify(progress));
  } catch {
    // Speicher voll/gesperrt – Fortsetzen geht dann eben nicht.
  }
}

export function clearWorkoutProgress(person: Person): void {
  try {
    localStorage.removeItem(progressKey(person));
  } catch {
    // ignorieren
  }
}

/** Für die Startseite: gibt es ein angefangenes Training dieses Plans (jünger als 12 h)? */
export function getResumableWorkout(
  person: Person,
  planName: string,
): { exerciseIndex: number; totalExercises: number; startedAt: number } | null {
  const p = loadWorkoutProgress(person);
  if (!p || p.planName !== planName) return null;
  // Nur geöffnet, nichts gemacht → nichts zum Fortsetzen
  if (p.exerciseIndex === 0 && p.currentSet === 1 && p.completedSets.length === 0 && p.abortedExercises.length === 0) {
    return null;
  }
  return { exerciseIndex: p.exerciseIndex, totalExercises: p.totalExercises, startedAt: p.startedAt };
}

// --- Signale (Ton/Vibration) am Ende eines Countdowns ---

let audioCtx: AudioContext | null = null;

/** Muss aus einer Nutzergeste (Tippen) heraus aufgerufen werden, sonst bleibt der Ton stumm. */
export function unlockAudio(): void {
  try {
    if (!audioCtx) {
      const Ctor = window.AudioContext ?? (window as unknown as { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
      if (!Ctor) return;
      audioCtx = new Ctor();
    }
    if (audioCtx.state === 'suspended') void audioCtx.resume().catch(() => {});
  } catch {
    // kein Ton möglich
  }
}

/** Kurzer Piepton + Vibration. Scheitert still. */
export function signalTimerEnd(): void {
  try {
    navigator.vibrate?.([200, 100, 200]);
  } catch {
    // ignorieren
  }
  try {
    const ctx = audioCtx;
    if (!ctx) return;
    if (ctx.state === 'suspended') void ctx.resume().catch(() => {});
    const beep = (start: number) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.value = 880;
      gain.gain.setValueAtTime(0.0001, start);
      gain.gain.exponentialRampToValueAtTime(0.3, start + 0.02);
      gain.gain.exponentialRampToValueAtTime(0.0001, start + 0.18);
      osc.connect(gain).connect(ctx.destination);
      osc.start(start);
      osc.stop(start + 0.2);
    };
    beep(ctx.currentTime);
    beep(ctx.currentTime + 0.3);
  } catch {
    // ignorieren
  }
}
