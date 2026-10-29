import { useState } from 'react';
import type { WorkoutSession } from '../types';
import type { Person } from '../lib/auth-service';
import type { LucideIcon } from 'lucide-react';
import type { ReactNode } from 'react';
import { Calendar, TrendingUp, Dumbbell, Clock, ChevronLeft, Award, Flame, Target, BarChart3, Download, Upload, FileText, Share2, Timer } from 'lucide-react';
import { planTheme } from '../utils/plan-theme';
import { Button } from './ui/Button';
import { calculateExtendedStatistics, formatDayCount } from '../utils/statistics';
import { AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { exportToJSON, exportToCSV, importFromJSON, downloadTextFile, getDateString } from '../utils/export';
import { buildPhysioReport, physioReportTitle } from '../utils/physio-report';
import { planTitle } from '../utils/format';

interface WorkoutHistoryProps {
  sessions: WorkoutSession[];
  onClose: () => void;
  onImport?: (sessions: WorkoutSession[]) => void;
  person?: Person;
}

export function WorkoutHistory({ sessions, onClose, onImport, person }: WorkoutHistoryProps) {
  const stats = calculateExtendedStatistics(sessions);
  const [reportHint, setReportHint] = useState<{ text: string; ok: boolean } | null>(null);

  const handleImport = () => {
    if (onImport) {
      importFromJSON(onImport, { currentPerson: person, existingIds: sessions.map((s) => s.id) });
    }
  };

  const handleShareReport = async () => {
    const now = new Date();
    const title = physioReportTitle(now);
    const text = buildPhysioReport(sessions, now);
    setReportHint(null);

    if (typeof navigator.share === 'function') {
      try {
        await navigator.share({ title, text });
        return;
      } catch (err) {
        // Vom Benutzer abgebrochen: nichts weiter tun
        if (err instanceof DOMException && err.name === 'AbortError') return;
      }
    }

    try {
      await navigator.clipboard.writeText(text);
      setReportHint({ ok: true, text: 'Bericht in die Zwischenablage kopiert – du kannst ihn jetzt z. B. in eine Nachricht einfügen.' });
    } catch {
      setReportHint({ ok: false, text: 'Teilen nicht möglich. Lade den Bericht als Textdatei herunter.' });
    }
  };

  const handleDownloadReport = () => {
    downloadTextFile(buildPhysioReport(sessions), `physio-bericht-${getDateString()}.txt`);
  };

  const tiles: { icon: LucideIcon; label: string; value: string; sub?: string }[] = [
    { icon: Dumbbell, label: 'Trainings gesamt', value: String(stats.totalWorkouts) },
    { icon: Clock, label: 'Zeit gesamt', value: `${stats.totalMinutes} Min` },
    { icon: Calendar, label: 'Diese Woche', value: String(stats.thisWeek), sub: 'Trainings' },
    { icon: TrendingUp, label: 'Dieser Monat', value: String(stats.thisMonth), sub: 'Trainings' },
    { icon: BarChart3, label: 'Durchschnitt', value: `${stats.averageDuration} Min` },
    { icon: Flame, label: 'Aktuelle Serie', value: formatDayCount(stats.currentStreak) },
  ];

  const highlights: { icon: LucideIcon; label: string; value: string; sub: string; extra?: string }[] = [
    ...(stats.favoritePlan
      ? [{ icon: Target, label: 'Lieblings-Plan', value: planTitle(stats.favoritePlan.name), sub: `${stats.favoritePlan.count}× absolviert` }]
      : []),
    { icon: Award, label: 'Längste Serie', value: formatDayCount(stats.longestStreak), sub: 'am Stück trainiert' },
    ...(stats.longestWorkout
      ? [{
          icon: Timer,
          label: 'Längstes Training',
          value: `${stats.longestWorkout.duration} Min`,
          sub: planTitle(stats.longestWorkout.planName),
          extra: new Date(stats.longestWorkout.date).toLocaleDateString('de-AT'),
        }]
      : []),
    ...(stats.shortestWorkout
      ? [{
          icon: Clock,
          label: 'Kürzestes Training',
          value: `${stats.shortestWorkout.duration} Min`,
          sub: planTitle(stats.shortestWorkout.planName),
          extra: new Date(stats.shortestWorkout.date).toLocaleDateString('de-AT'),
        }]
      : []),
  ];

  const maxWeekday = Math.max(...stats.workoutsByWeekday.map(d => d.count), 1);
  const tooltipStyle = {
    backgroundColor: '#0f172a',
    border: '1px solid #334155',
    borderRadius: '12px',
    color: '#fff',
  };

  return (
    <div className="min-h-dvh bg-slate-950">
      {/* Kopf */}
      <header className="sticky top-0 z-10 border-b border-white/5 bg-slate-950/90 px-safe-4 pt-safe-2 pb-3 backdrop-blur">
        <div className="mx-auto max-w-3xl">
          <button
            type="button"
            onClick={onClose}
            className="-ml-2 flex min-h-11 items-center gap-1 rounded-xl pl-1 pr-3 text-base font-medium text-slate-200 transition hover:bg-white/5"
          >
            <ChevronLeft className="h-5 w-5" />
            Zurück
          </button>
          <h1 className="mt-1 text-3xl font-bold tracking-tight text-white">Trainings-Statistiken</h1>
        </div>
      </header>

      <main className="mx-auto max-w-3xl space-y-4 px-safe-4 pt-4 pb-safe-8">
        {/* Bericht für die Physio (nur Thomas) */}
        {person === 'thomas' && (
          <section className="rounded-3xl bg-gradient-to-br from-indigo-500/20 to-violet-600/10 p-4 ring-1 ring-indigo-400/25">
            <div className="mb-1 flex items-center gap-3">
              <span className="grid h-10 w-10 place-items-center rounded-xl bg-indigo-500/20 text-indigo-200">
                <FileText className="h-5 w-5" />
              </span>
              <h2 className="text-lg font-bold text-white">Bericht für die Physio</h2>
            </div>
            <p className="mb-4 text-base text-slate-300">
              Letzte 4 Wochen: Einheiten je Woche, Befinden und abgebrochene Übungen für Rücken-Aufbau, Nacken & Schulter und Morgen-Routine.
            </p>
            <div className="flex gap-2">
              <Button size="md" onClick={handleShareReport} className="min-h-12 flex-1">
                <Share2 className="h-5 w-5" />
                Bericht für die Physio
              </Button>
              <Button variant="secondary" size="md" onClick={handleDownloadReport} title="Als Textdatei herunterladen" className="min-h-12">
                <Download className="h-4 w-4" />
                .txt
              </Button>
            </div>
            {reportHint && (
              <p className={`mt-3 text-sm ${reportHint.ok ? 'text-emerald-300' : 'text-amber-300'}`} role="status">{reportHint.text}</p>
            )}
          </section>
        )}

        {/* Kennzahlen */}
        <section className="grid grid-cols-2 gap-3 lg:grid-cols-3">
          {tiles.map(({ icon: Icon, label, value, sub }) => (
            <div key={label} className="rounded-3xl bg-slate-900 p-4 ring-1 ring-white/5">
              <Icon className="h-5 w-5 text-indigo-300" />
              <div className="mt-3 text-2xl font-bold tabular-nums text-white">
                {value}
                {sub && <span className="ml-1 text-sm font-medium text-slate-400">{sub}</span>}
              </div>
              <div className="text-sm text-slate-400">{label}</div>
            </div>
          ))}
        </section>

        {/* Bestwerte */}
        <section className="grid grid-cols-1 gap-3 md:grid-cols-2">
          {highlights.map(({ icon: Icon, label, value, sub, extra }) => (
            <div key={label} className="flex items-center gap-4 rounded-3xl bg-slate-900 p-4 ring-1 ring-white/5">
              <span className="grid h-12 w-12 shrink-0 place-items-center rounded-2xl bg-amber-500/15 text-amber-300">
                <Icon className="h-6 w-6" />
              </span>
              <div className="min-w-0 flex-1">
                <div className="text-sm text-slate-400">{label}</div>
                <div className="truncate text-xl font-bold text-white">{value}</div>
                <div className="text-sm text-slate-400">
                  {sub}
                  {extra && <span className="text-slate-500"> · {extra}</span>}
                </div>
              </div>
            </div>
          ))}
        </section>

        {/* Diagramme */}
        {stats.workoutsOverTime.length > 0 && (
          <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
            <ChartCard icon={TrendingUp} title="Trainings pro Woche">
              <ResponsiveContainer width="100%" height={220}>
                <BarChart data={stats.workoutsOverTime} margin={{ top: 8, right: 4, left: -24, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#818cf8" stopOpacity={1} />
                      <stop offset="100%" stopColor="#7c3aed" stopOpacity={1} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                  <XAxis dataKey="date" stroke="#64748b" tickLine={false} axisLine={false} style={{ fontSize: '12px' }} />
                  <YAxis stroke="#64748b" tickLine={false} axisLine={false} allowDecimals={false} style={{ fontSize: '12px' }} />
                  <Tooltip
                    cursor={{ fill: 'rgba(148,163,184,0.08)' }}
                    contentStyle={tooltipStyle}
                    formatter={(value: number) => [`${value} Trainings`, 'Anzahl']}
                  />
                  <Bar dataKey="count" fill="url(#colorCount)" radius={[8, 8, 0, 0]} maxBarSize={36} />
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>

            <ChartCard icon={Clock} title="Trainingszeit pro Woche">
              <ResponsiveContainer width="100%" height={220}>
                <AreaChart data={stats.workoutsOverTime} margin={{ top: 8, right: 4, left: -24, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorMinutes" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#f59e0b" stopOpacity={0.6} />
                      <stop offset="100%" stopColor="#f59e0b" stopOpacity={0.02} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                  <XAxis dataKey="date" stroke="#64748b" tickLine={false} axisLine={false} style={{ fontSize: '12px' }} />
                  <YAxis stroke="#64748b" tickLine={false} axisLine={false} style={{ fontSize: '12px' }} />
                  <Tooltip contentStyle={tooltipStyle} formatter={(value: number) => [`${value} Min`, 'Dauer']} />
                  <Area type="monotone" dataKey="totalMinutes" stroke="#fbbf24" fill="url(#colorMinutes)" strokeWidth={2.5} />
                </AreaChart>
              </ResponsiveContainer>
            </ChartCard>
          </div>
        )}

        {/* Wochentage */}
        <ChartCard icon={Calendar} title="Training nach Wochentag">
          <div className="space-y-3">
            {stats.workoutsByWeekday.map((day) => (
              <div key={day.day}>
                <div className="mb-1 flex justify-between text-sm text-slate-300">
                  <span>{day.day}</span>
                  <span className="font-semibold tabular-nums">{day.count} Trainings</span>
                </div>
                <div className="h-2.5 overflow-hidden rounded-full bg-slate-800">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-indigo-500 to-violet-500 transition-all"
                    style={{ width: `${(day.count / maxWeekday) * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </ChartCard>

        {/* Letzte Trainings */}
        <ChartCard icon={Dumbbell} title="Letzte Trainings">
          {sessions.length === 0 ? (
            <div className="py-8 text-center text-base text-slate-400">
              Noch keine Trainings absolviert.
              <br />
              Starte dein erstes Training!
            </div>
          ) : (
            <ul className="-mx-1 divide-y divide-white/5">
              {sessions
                .toSorted((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
                .map((session) => {
                  const theme = planTheme(session.planName);
                  const Icon = theme.icon;
                  return (
                    <li key={session.id} className="flex items-center gap-3 px-1 py-3">
                      <span className={`grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-gradient-to-br ${theme.gradient} text-white`}>
                        <Icon className="h-5 w-5" />
                      </span>
                      <div className="min-w-0 flex-1">
                        <div className="truncate font-semibold text-white">{planTitle(session.planName)}</div>
                        <div className="text-sm text-slate-400">
                          {new Date(session.date).toLocaleDateString('de-AT', {
                            weekday: 'short',
                            day: '2-digit',
                            month: '2-digit',
                            year: 'numeric',
                          })}
                        </div>
                      </div>
                      <div className="shrink-0 text-right">
                        <div className="font-semibold tabular-nums text-white">{session.completedExercises} {session.completedExercises === 1 ? 'Übung' : 'Übungen'}</div>
                        <div className="text-sm tabular-nums text-slate-400">{session.duration} Min</div>
                      </div>
                    </li>
                  );
                })}
            </ul>
          )}
        </ChartCard>

        {/* Daten sichern / einlesen */}
        <ChartCard icon={Download} title="Daten sichern">
          <p className="mb-3 text-sm text-slate-400">Trainings als Datei speichern oder von einem anderen Gerät übernehmen.</p>
          <div className="grid grid-cols-2 gap-2">
            {sessions.length > 0 && (
              <>
                <Button variant="secondary" size="md" onClick={() => exportToJSON(sessions, person)} title="Als JSON exportieren" className="min-h-12 text-sm!">
                  <Download className="h-4 w-4" />
                  Sichern (JSON)
                </Button>
                <Button variant="secondary" size="md" onClick={() => exportToCSV(sessions)} title="Als CSV exportieren" className="min-h-12 text-sm!">
                  <Download className="h-4 w-4" />
                  Tabelle (CSV)
                </Button>
              </>
            )}
            {onImport && (
              <Button variant="secondary" size="md" onClick={handleImport} title="JSON importieren" className="col-span-2 min-h-12 text-sm!">
                <Upload className="h-4 w-4" />
                Einlesen (JSON)
              </Button>
            )}
          </div>
        </ChartCard>
      </main>
    </div>
  );
}

function ChartCard({ icon: Icon, title, children }: { icon: LucideIcon; title: string; children: ReactNode }) {
  return (
    <section className="rounded-3xl bg-slate-900 p-4 ring-1 ring-white/5">
      <h2 className="mb-4 flex items-center gap-2 text-lg font-bold text-white">
        <Icon className="h-5 w-5 text-indigo-300" />
        {title}
      </h2>
      {children}
    </section>
  );
}
