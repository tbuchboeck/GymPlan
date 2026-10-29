import type { WorkoutSession } from '../types';

export interface ExtendedStatistics {
  // Grundlegende Stats
  totalWorkouts: number;
  totalMinutes: number;
  thisWeek: number;
  thisMonth: number;

  // Neue erweiterte Stats
  averageDuration: number;
  longestWorkout: WorkoutSession | null;
  shortestWorkout: WorkoutSession | null;
  currentStreak: number;
  longestStreak: number;
  favoritePlan: {
    name: string;
    count: number;
  } | null;
  workoutsByWeekday: {
    day: string;
    count: number;
  }[];

  // Chart-Daten
  workoutsOverTime: {
    date: string;
    count: number;
    totalMinutes: number;
  }[];
}

export function calculateExtendedStatistics(sessions: WorkoutSession[]): ExtendedStatistics {
  // Grundlegende Stats
  const totalWorkouts = sessions.length;
  const totalMinutes = sessions.reduce((sum, s) => sum + s.duration, 0);

  // Kalenderwoche (Mo–So) und Kalendermonat, jeweils lokal
  const now = new Date();
  const thisWeek = sessions.filter(s => isInWeekOf(new Date(s.date), now)).length;
  const thisMonth = sessions.filter(s => {
    const d = new Date(s.date);
    return d.getFullYear() === now.getFullYear() && d.getMonth() === now.getMonth();
  }).length;

  // Durchschnittliche Dauer
  const averageDuration = totalWorkouts > 0 ? Math.round(totalMinutes / totalWorkouts) : 0;

  // Längste und kürzeste Trainingseinheit
  let longestWorkout: WorkoutSession | null = null;
  let shortestWorkout: WorkoutSession | null = null;

  if (sessions.length > 0) {
    longestWorkout = sessions.reduce((max, s) => s.duration > max.duration ? s : max);
    shortestWorkout = sessions.reduce((min, s) => s.duration < min.duration ? s : min);
  }

  // Streak-Berechnung
  const { currentStreak, longestStreak } = calculateStreaks(sessions);

  // Lieblings-Trainingsplan
  const favoritePlan = calculateFavoritePlan(sessions);

  // Wochentag-Analyse
  const workoutsByWeekday = calculateWorkoutsByWeekday(sessions);

  // Chart-Daten für Zeitverlauf
  const workoutsOverTime = calculateWorkoutsOverTime(sessions);

  return {
    totalWorkouts,
    totalMinutes,
    thisWeek,
    thisMonth,
    averageDuration,
    longestWorkout,
    shortestWorkout,
    currentStreak,
    longestStreak,
    favoritePlan,
    workoutsByWeekday,
    workoutsOverTime,
  };
}

function calculateStreaks(sessions: WorkoutSession[]): { currentStreak: number; longestStreak: number } {
  // Einzigartige Trainingstage als fortlaufende Tagesnummern (lokal)
  const days = Array.from(new Set(sessions.map(s => dayNumber(localDayKey(new Date(s.date))))))
    .sort((a, b) => b - a); // neueste zuerst

  if (days.length === 0) {
    return { currentStreak: 0, longestStreak: 0 };
  }

  // Aktuelle Serie: muss heute oder gestern beginnen
  const today = dayNumber(localDayKey(new Date()));
  let currentStreak = 0;
  if (days[0] === today || days[0] === today - 1) {
    currentStreak = 1;
    for (let i = 1; i < days.length && days[i] === days[i - 1] - 1; i++) {
      currentStreak++;
    }
  }

  // Längste Serie
  let longestStreak = 1;
  let tempStreak = 1;
  for (let i = 1; i < days.length; i++) {
    tempStreak = days[i] === days[i - 1] - 1 ? tempStreak + 1 : 1;
    longestStreak = Math.max(longestStreak, tempStreak);
  }

  return { currentStreak, longestStreak };
}

function calculateFavoritePlan(sessions: WorkoutSession[]): { name: string; count: number } | null {
  if (sessions.length === 0) {
    return null;
  }

  const planCounts = new Map<string, number>();

  sessions.forEach(session => {
    const count = planCounts.get(session.planName) || 0;
    planCounts.set(session.planName, count + 1);
  });

  let favoritePlan: { name: string; count: number } | null = null;
  let maxCount = 0;

  planCounts.forEach((count, name) => {
    if (count > maxCount) {
      maxCount = count;
      favoritePlan = { name, count };
    }
  });

  return favoritePlan;
}

function calculateWorkoutsByWeekday(sessions: WorkoutSession[]): { day: string; count: number }[] {
  const weekdayNames = ['Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag'];
  const weekdayCounts = new Map<number, number>();

  // Initialisiere alle Wochentage mit 0
  for (let i = 0; i < 7; i++) {
    weekdayCounts.set(i, 0);
  }

  sessions.forEach(session => {
    const date = new Date(session.date);
    const weekday = date.getDay();
    weekdayCounts.set(weekday, (weekdayCounts.get(weekday) || 0) + 1);
  });

  // Konvertiere zu Array und starte mit Montag (Index 1)
  const result: { day: string; count: number }[] = [];

  // Montag bis Sonntag
  for (let i = 1; i < 7; i++) {
    result.push({
      day: weekdayNames[i],
      count: weekdayCounts.get(i) || 0,
    });
  }
  // Sonntag am Ende
  result.push({
    day: weekdayNames[0],
    count: weekdayCounts.get(0) || 0,
  });

  return result;
}

function calculateWorkoutsOverTime(sessions: WorkoutSession[]): { date: string; count: number; totalMinutes: number }[] {
  // Gruppiere nach Woche; Schlüssel = lokaler Montag als YYYY-MM-DD
  const weeklyData = new Map<string, { count: number; totalMinutes: number }>();

  sessions.forEach(session => {
    const weekKey = localDayKey(startOfWeek(new Date(session.date)));
    const existing = weeklyData.get(weekKey) || { count: 0, totalMinutes: 0 };
    weeklyData.set(weekKey, {
      count: existing.count + 1,
      totalMinutes: existing.totalMinutes + session.duration,
    });
  });

  // Erst nach ISO-Schlüssel sortieren, dann Label formatieren; nur letzte 12 Wochen
  return Array.from(weeklyData.entries())
    .sort(([a], [b]) => a.localeCompare(b))
    .slice(-12)
    .map(([key, data]) => ({
      date: formatWeekLabel(key),
      count: data.count,
      totalMinutes: data.totalMinutes,
    }));
}

/** Lokaler Tagesschlüssel YYYY-MM-DD (nie toISOString – das wäre UTC). */
export function localDayKey(date: Date): string {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

/** Fortlaufende Tagesnummer zu einem Tagesschlüssel (sommerzeitsicher). */
function dayNumber(key: string): number {
  const [y, m, d] = key.split('-').map(Number);
  return Math.round(Date.UTC(y, m - 1, d) / 86_400_000);
}

/** Montag 00:00 Ortszeit der Woche, in der `date` liegt. */
export function startOfWeek(date: Date): Date {
  const d = new Date(date);
  d.setHours(0, 0, 0, 0);
  const day = d.getDay(); // 0 = Sonntag
  d.setDate(d.getDate() - (day === 0 ? 6 : day - 1));
  return d;
}

/** Index 0–6 (Mo–So) des Wochentags, lokal. */
export function weekdayIndex(date: Date): number {
  return (date.getDay() + 6) % 7;
}

/** Liegt `date` in derselben Kalenderwoche (Mo–So) wie `ref`? */
export function isInWeekOf(date: Date, ref: Date = new Date()): boolean {
  return localDayKey(startOfWeek(date)) === localDayKey(startOfWeek(ref));
}

/** Liegt `date` am selben lokalen Kalendertag wie `ref`? */
export function isSameLocalDay(date: Date, ref: Date = new Date()): boolean {
  return localDayKey(date) === localDayKey(ref);
}

/** „1 Tag“ bzw. „n Tage“ */
export function formatDayCount(n: number): string {
  return n === 1 ? '1 Tag' : `${n} Tage`;
}

function formatWeekLabel(key: string): string {
  const [, month, day] = key.split('-');
  return `${day}.${month}`;
}
