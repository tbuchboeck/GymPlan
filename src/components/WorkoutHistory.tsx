import type { WorkoutSession } from '../types';
import { Calendar, TrendingUp, Dumbbell, Clock, ArrowLeft, Award, Flame, Target, BarChart3, Download, Upload } from 'lucide-react';
import { calculateExtendedStatistics } from '../utils/statistics';
import { AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { exportToJSON, exportToCSV, importFromJSON } from '../utils/export';

interface WorkoutHistoryProps {
  sessions: WorkoutSession[];
  onClose: () => void;
  onImport?: (sessions: WorkoutSession[]) => void;
}

export function WorkoutHistory({ sessions, onClose, onImport }: WorkoutHistoryProps) {
  const stats = calculateExtendedStatistics(sessions);

  const handleImport = () => {
    if (onImport) {
      importFromJSON(onImport);
    }
  };

  return (
    <div className="min-h-dvh bg-slate-900">
      {/* Header */}
      <div className="bg-slate-800 border-b border-slate-700/50 px-4 py-4">
        <div className="flex items-center justify-between mb-3">
          <button
            onClick={onClose}
            className="flex items-center gap-2 text-slate-400 hover:text-white transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Zurück</span>
          </button>

          {/* Import & Export Buttons */}
          <div className="flex gap-2">
            {onImport && (
              <button
                onClick={handleImport}
                className="flex items-center gap-2 px-3 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-all text-sm border border-slate-600"
                title="JSON importieren"
              >
                <Upload className="w-4 h-4" />
                <span className="font-bold">J</span>
                <span className="hidden sm:inline">SON</span>
              </button>
            )}
            {sessions.length > 0 && (
              <>
                <button
                  onClick={() => exportToJSON(sessions)}
                  className="flex items-center gap-2 px-3 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-all text-sm border border-slate-600"
                  title="Als JSON exportieren"
                >
                  <Download className="w-4 h-4" />
                  <span className="font-bold">J</span>
                  <span className="hidden sm:inline">SON</span>
                </button>
                <button
                  onClick={() => exportToCSV(sessions)}
                  className="flex items-center gap-2 px-3 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-all text-sm border border-slate-600"
                  title="Als CSV exportieren"
                >
                  <Download className="w-4 h-4" />
                  <span className="font-bold">C</span>
                  <span className="hidden sm:inline">SV</span>
                </button>
              </>
            )}
          </div>
        </div>
        <h1 className="text-xl font-bold text-white">Trainings-Statistiken</h1>
      </div>

      <div className="mx-4 py-6">
        {/* Stats Grid */}
        <div className="grid grid-cols-2 lg:grid-cols-3 gap-3 mb-6">
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
            <div className="flex items-center gap-2 mb-2">
              <Dumbbell className="text-indigo-400 w-5 h-5" />
              <div className="text-xs text-slate-400 uppercase tracking-wider">Gesamt Trainings</div>
            </div>
            <div className="text-2xl font-bold text-white">{stats.totalWorkouts}</div>
          </div>

          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
            <div className="flex items-center gap-2 mb-2">
              <Clock className="text-indigo-400 w-5 h-5" />
              <div className="text-xs text-slate-400 uppercase tracking-wider">Gesamt Zeit</div>
            </div>
            <div className="text-2xl font-bold text-white">{stats.totalMinutes} min</div>
          </div>

          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
            <div className="flex items-center gap-2 mb-2">
              <Calendar className="text-indigo-400 w-5 h-5" />
              <div className="text-xs text-slate-400 uppercase tracking-wider">Diese Woche</div>
            </div>
            <div className="text-2xl font-bold text-white">{stats.thisWeek} Trainings</div>
          </div>

          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
            <div className="flex items-center gap-2 mb-2">
              <TrendingUp className="text-indigo-400 w-5 h-5" />
              <div className="text-xs text-slate-400 uppercase tracking-wider">Dieser Monat</div>
            </div>
            <div className="text-2xl font-bold text-white">{stats.thisMonth} Trainings</div>
          </div>

          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
            <div className="flex items-center gap-2 mb-2">
              <BarChart3 className="text-indigo-400 w-5 h-5" />
              <div className="text-xs text-slate-400 uppercase tracking-wider">Durchschnitt</div>
            </div>
            <div className="text-2xl font-bold text-white">{stats.averageDuration} min</div>
          </div>

          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
            <div className="flex items-center gap-2 mb-2">
              <Flame className="text-indigo-400 w-5 h-5" />
              <div className="text-xs text-slate-400 uppercase tracking-wider">Serie</div>
            </div>
            <div className="text-2xl font-bold text-white">{stats.currentStreak} Tage</div>
          </div>
        </div>

        {/* Extended Stats Section */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-6">
          {/* Favorite Plan */}
          {stats.favoritePlan && (
            <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
              <div className="flex items-center gap-3 mb-3">
                <Target className="text-indigo-400 w-5 h-5" />
                <h3 className="text-lg font-bold text-white">Lieblings-Plan</h3>
              </div>
              <div className="text-2xl font-bold text-white mb-1">{stats.favoritePlan.name}</div>
              <div className="text-sm text-slate-400">{stats.favoritePlan.count}x absolviert</div>
            </div>
          )}

          {/* Longest Streak */}
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
            <div className="flex items-center gap-3 mb-3">
              <Award className="text-indigo-400 w-5 h-5" />
              <h3 className="text-lg font-bold text-white">Beste Streak</h3>
            </div>
            <div className="text-2xl font-bold text-white mb-1">{stats.longestStreak} Tage</div>
            <div className="text-sm text-slate-400">Längste Serie</div>
          </div>

          {/* Longest Workout */}
          {stats.longestWorkout && (
            <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
              <div className="flex items-center gap-3 mb-3">
                <Clock className="text-indigo-400 w-5 h-5" />
                <h3 className="text-lg font-bold text-white">Längstes Training</h3>
              </div>
              <div className="text-2xl font-bold text-white mb-1">{stats.longestWorkout.duration} min</div>
              <div className="text-sm text-slate-400">{stats.longestWorkout.planName}</div>
              <div className="text-xs text-slate-500 mt-1">
                {new Date(stats.longestWorkout.date).toLocaleDateString('de-DE')}
              </div>
            </div>
          )}

          {/* Shortest Workout */}
          {stats.shortestWorkout && (
            <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
              <div className="flex items-center gap-3 mb-3">
                <Clock className="text-indigo-400 w-5 h-5" />
                <h3 className="text-lg font-bold text-white">Kürzestes Training</h3>
              </div>
              <div className="text-2xl font-bold text-white mb-1">{stats.shortestWorkout.duration} min</div>
              <div className="text-sm text-slate-400">{stats.shortestWorkout.planName}</div>
              <div className="text-xs text-slate-500 mt-1">
                {new Date(stats.shortestWorkout.date).toLocaleDateString('de-DE')}
              </div>
            </div>
          )}
        </div>

        {/* Charts Section */}
        {stats.workoutsOverTime.length > 0 && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-3 mb-6">
            {/* Workout Frequency Chart */}
            <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
              <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                <TrendingUp className="w-6 h-6" />
                Trainings pro Woche
              </h2>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={stats.workoutsOverTime}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
                  <XAxis
                    dataKey="date"
                    stroke="#94a3b8"
                    style={{ fontSize: '12px' }}
                  />
                  <YAxis
                    stroke="#94a3b8"
                    style={{ fontSize: '12px' }}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#1e293b',
                      border: '1px solid #334155',
                      borderRadius: '8px',
                      color: '#fff',
                    }}
                    formatter={(value: number) => [`${value} Trainings`, 'Anzahl']}
                  />
                  <Bar
                    dataKey="count"
                    fill="url(#colorCount)"
                    radius={[8, 8, 0, 0]}
                  />
                  <defs>
                    <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#6366f1" stopOpacity={1} />
                      <stop offset="100%" stopColor="#8b5cf6" stopOpacity={1} />
                    </linearGradient>
                  </defs>
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Workout Duration Chart */}
            <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
              <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                <Clock className="w-6 h-6" />
                Trainingszeit pro Woche
              </h2>
              <ResponsiveContainer width="100%" height={250}>
                <AreaChart data={stats.workoutsOverTime}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
                  <XAxis
                    dataKey="date"
                    stroke="#94a3b8"
                    style={{ fontSize: '12px' }}
                  />
                  <YAxis
                    stroke="#94a3b8"
                    style={{ fontSize: '12px' }}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#1e293b',
                      border: '1px solid #334155',
                      borderRadius: '8px',
                      color: '#fff',
                    }}
                    formatter={(value: number) => [`${value} min`, 'Dauer']}
                  />
                  <Area
                    type="monotone"
                    dataKey="totalMinutes"
                    stroke="#f59e0b"
                    fill="url(#colorMinutes)"
                    strokeWidth={2}
                  />
                  <defs>
                    <linearGradient id="colorMinutes" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#f59e0b" stopOpacity={0.8} />
                      <stop offset="100%" stopColor="#f59e0b" stopOpacity={0.1} />
                    </linearGradient>
                  </defs>
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {/* Weekday Analysis */}
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 mb-6">
          <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <Calendar className="w-6 h-6" />
            Training nach Wochentag
          </h2>
          <div className="space-y-3">
            {stats.workoutsByWeekday.map((day) => {
              const maxCount = Math.max(...stats.workoutsByWeekday.map(d => d.count), 1);
              const percentage = (day.count / maxCount) * 100;

              return (
                <div key={day.day}>
                  <div className="flex justify-between text-sm text-slate-300 mb-1">
                    <span>{day.day}</span>
                    <span className="font-semibold">{day.count} Trainings</span>
                  </div>
                  <div className="h-3 bg-slate-700 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-indigo-500 rounded-full transition-all"
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Recent Sessions */}
        <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
          <h2 className="text-xl font-bold text-white mb-4">Letzte Trainings</h2>
          {sessions.length === 0 ? (
            <div className="text-center py-8 text-slate-400">
              Noch keine Trainings absolviert.
              <br />
              Starte dein erstes Training!
            </div>
          ) : (
            <div className="space-y-3">
              {sessions
                .toSorted((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
                .map((session) => (
                  <div
                    key={session.id}
                    className="flex items-center justify-between p-4 bg-slate-800/50 border border-slate-700/50 rounded-xl hover:bg-slate-800 transition-all"
                  >
                    <div>
                      <div className="font-semibold text-white">
                        {session.planName}
                      </div>
                      <div className="text-sm text-slate-400">
                        {new Date(session.date).toLocaleDateString('de-DE', {
                          weekday: 'long',
                          day: '2-digit',
                          month: '2-digit',
                          year: 'numeric'
                        })}
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="font-semibold text-white">
                        {session.completedExercises} Übungen
                      </div>
                      <div className="text-sm text-slate-400">
                        {session.duration} Minuten
                      </div>
                    </div>
                  </div>
                ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
