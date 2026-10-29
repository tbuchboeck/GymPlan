import type { Feeling, WorkoutSession } from '../types';

// Pläne, die im Bericht für die Physio auftauchen (Kennung im Plan-Namen)
export const PHYSIO_PLANS = [
  { tag: '@rücken', label: 'Rücken-Aufbau (@rücken)' },
  { tag: '@nacken', label: 'Nacken, Schulter & BWS (@nacken)' },
  { tag: '@morgen', label: 'Morgen-Reset (@morgen)' },
] as const;

// Pläne mit Befindens-Abfrage nach dem Training
export function hasFeelingCheck(planName: string): boolean {
  return planName.includes('(@rücken)') || planName.includes('(@nacken)');
}

export const FEELING_LABELS: Record<Feeling, string> = {
  better: 'besser',
  same: 'gleich',
  worse: 'schlechter',
};

const WEEKS = 4;
const DAY_MS = 24 * 60 * 60 * 1000;

function startOfWeek(d: Date): Date {
  // Montag 00:00 Ortszeit
  const res = new Date(d.getFullYear(), d.getMonth(), d.getDate());
  const offset = (res.getDay() + 6) % 7;
  res.setDate(res.getDate() - offset);
  return res;
}

function addDays(d: Date, days: number): Date {
  const res = new Date(d);
  res.setDate(res.getDate() + days);
  return res;
}

function isoWeek(d: Date): number {
  const t = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
  const day = t.getUTCDay() || 7;
  t.setUTCDate(t.getUTCDate() + 4 - day);
  const yearStart = Date.UTC(t.getUTCFullYear(), 0, 1);
  return Math.ceil(((t.getTime() - yearStart) / DAY_MS + 1) / 7);
}

function fmtDate(d: Date): string {
  return d.toLocaleDateString('de-AT', { day: '2-digit', month: '2-digit', year: 'numeric' });
}

function fmtShort(d: Date): string {
  return d.toLocaleDateString('de-AT', { day: '2-digit', month: '2-digit' });
}

function planOf(session: WorkoutSession) {
  return PHYSIO_PLANS.find((p) => session.planName.includes(p.tag));
}

export function physioReportTitle(now: Date = new Date()): string {
  return `Trainingsbericht für die Physio (${fmtDate(now)})`;
}

/**
 * Textbericht über die letzten 4 Kalenderwochen (inkl. laufender Woche)
 * für die Pläne @rücken, @nacken und @morgen.
 */
export function buildPhysioReport(sessions: WorkoutSession[], now: Date = new Date()): string {
  const currentWeek = startOfWeek(now);
  const weeks = Array.from({ length: WEEKS }, (_, i) => {
    const start = addDays(currentWeek, -7 * (WEEKS - 1 - i));
    return { start, end: addDays(start, 7) };
  });
  const from = weeks[0].start;
  const to = weeks[WEEKS - 1].end;

  const relevant = sessions
    .filter((s) => {
      const d = new Date(s.date);
      return !isNaN(d.getTime()) && d >= from && d < to && planOf(s);
    })
    .toSorted((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

  const lines: string[] = [];
  lines.push(physioReportTitle(now));
  lines.push(`Zeitraum: ${fmtDate(from)} – ${fmtDate(addDays(to, -1))}`);
  lines.push('');

  for (const plan of PHYSIO_PLANS) {
    const planSessions = relevant.filter((s) => s.planName.includes(plan.tag));
    lines.push(`== ${plan.label} ==`);

    lines.push(`Einheiten gesamt: ${planSessions.length}`);
    for (const w of weeks) {
      const count = planSessions.filter((s) => {
        const d = new Date(s.date);
        return d >= w.start && d < w.end;
      }).length;
      lines.push(`  KW ${isoWeek(w.start)} (${fmtShort(w.start)}–${fmtShort(addDays(w.end, -1))}): ${count}`);
    }

    if (hasFeelingCheck(plan.label)) {
      const rated = planSessions.filter((s) => s.feeling || typeof s.tingling === 'boolean');
      lines.push('Befinden nach dem Training:');
      if (rated.length === 0) {
        lines.push('  keine Angaben');
      } else {
        for (const s of rated) {
          const feeling = s.feeling ? FEELING_LABELS[s.feeling] : 'keine Angabe';
          const tingling = typeof s.tingling === 'boolean' ? (s.tingling ? 'ja' : 'nein') : 'keine Angabe';
          lines.push(`  ${fmtDate(new Date(s.date))}: ${feeling}, Kribbeln/Ziehen im Arm: ${tingling}`);
        }
      }
    }

    const aborted = planSessions.filter((s) => s.abortedExercises && s.abortedExercises.length > 0);
    lines.push('Abgebrochene Übungen (Kribbeln):');
    if (aborted.length === 0) {
      lines.push('  keine');
    } else {
      for (const s of aborted) {
        lines.push(`  ${fmtDate(new Date(s.date))}: ${(s.abortedExercises ?? []).join(', ')}`);
      }
    }
    lines.push('');
  }

  return lines.join('\n').trimEnd() + '\n';
}
