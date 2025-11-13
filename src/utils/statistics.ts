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

  const now = new Date();
  const weekAgo = new Date(now);
  weekAgo.setDate(weekAgo.getDate() - 7);

  const monthAgo = new Date(now);
  monthAgo.setDate(monthAgo.getDate() - 30);

  const thisWeek = sessions.filter(s => new Date(s.date) >= weekAgo).length;
  const thisMonth = sessions.filter(s => new Date(s.date) >= monthAgo).length;

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
  if (sessions.length === 0) {
    return { currentStreak: 0, longestStreak: 0 };
  }

  // Sortiere Sessions nach Datum (neueste zuerst)
  const sortedSessions = [...sessions].sort((a, b) =>
    new Date(b.date).getTime() - new Date(a.date).getTime()
  );

  // Extrahiere einzigartige Tage (mehrere Workouts am selben Tag = 1 Tag)
  const uniqueDays = new Set<string>();
  sortedSessions.forEach(session => {
    const dateStr = new Date(session.date).toISOString().split('T')[0];
    uniqueDays.add(dateStr);
  });

  const sortedDays = Array.from(uniqueDays).sort().reverse(); // Neueste zuerst

  if (sortedDays.length === 0) {
    return { currentStreak: 0, longestStreak: 0 };
  }

  // Berechne Current Streak
  let currentStreak = 0;
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const yesterday = new Date(today);
  yesterday.setDate(yesterday.getDate() - 1);

  const todayStr = today.toISOString().split('T')[0];
  const yesterdayStr = yesterday.toISOString().split('T')[0];

  // Streak kann heute oder gestern starten
  if (sortedDays[0] !== todayStr && sortedDays[0] !== yesterdayStr) {
    currentStreak = 0;
  } else {
    currentStreak = 1;
    let expectedDate = new Date(sortedDays[0]);

    for (let i = 1; i < sortedDays.length; i++) {
      expectedDate.setDate(expectedDate.getDate() - 1);
      const expectedStr = expectedDate.toISOString().split('T')[0];

      if (sortedDays[i] === expectedStr) {
        currentStreak++;
      } else {
        break;
      }
    }
  }

  // Berechne Longest Streak
  let longestStreak = 0;
  let tempStreak = 1;

  for (let i = 1; i < sortedDays.length; i++) {
    const prevDate = new Date(sortedDays[i - 1]);
    const currDate = new Date(sortedDays[i]);

    const dayDiff = Math.floor((prevDate.getTime() - currDate.getTime()) / (1000 * 60 * 60 * 24));

    if (dayDiff === 1) {
      tempStreak++;
    } else {
      longestStreak = Math.max(longestStreak, tempStreak);
      tempStreak = 1;
    }
  }

  longestStreak = Math.max(longestStreak, tempStreak);

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
  if (sessions.length === 0) {
    return [];
  }

  // Gruppiere Sessions nach Woche (ISO-Woche)
  const weeklyData = new Map<string, { count: number; totalMinutes: number }>();

  sessions.forEach(session => {
    const date = new Date(session.date);

    // Berechne ISO-Wochennummer und Jahr
    const weekStart = getMonday(date);
    const weekKey = weekStart.toISOString().split('T')[0];

    const existing = weeklyData.get(weekKey) || { count: 0, totalMinutes: 0 };
    weeklyData.set(weekKey, {
      count: existing.count + 1,
      totalMinutes: existing.totalMinutes + session.duration,
    });
  });

  // Konvertiere zu Array und sortiere nach Datum
  const result = Array.from(weeklyData.entries())
    .map(([date, data]) => ({
      date: formatWeekLabel(date),
      count: data.count,
      totalMinutes: data.totalMinutes,
    }))
    .sort((a, b) => a.date.localeCompare(b.date));

  // Nimm nur die letzten 12 Wochen
  return result.slice(-12);
}

function getMonday(date: Date): Date {
  const d = new Date(date);
  const day = d.getDay();
  const diff = d.getDate() - day + (day === 0 ? -6 : 1); // Anpassung für Sonntag
  return new Date(d.setDate(diff));
}

function formatWeekLabel(dateStr: string): string {
  const date = new Date(dateStr);
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  return `${day}.${month}`;
}
