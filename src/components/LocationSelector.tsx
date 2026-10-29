import type { LucideIcon } from 'lucide-react';
import { Building2, Dumbbell, HeartPulse, PersonStanding, Activity, Sunrise, CircleCheck } from 'lucide-react';
import type { Person } from '../lib/auth-service';
import type { WorkoutPlan, WorkoutSession } from '../types';
import { gymWorkoutPlan, homeWorkoutPlan, homeWorkoutPlan2, backWorkoutPlan, neckWorkoutPlan, morningWorkoutPlan } from '../data/workoutPlan';
import { isInWeekOf, isSameLocalDay } from '../utils/statistics';
import { VersionBadge } from './VersionBadge';
import { planTitle } from '../utils/format';

export type LocationKey = 'gym' | 'home' | 'home2' | 'back' | 'neck' | 'morning';

interface LocationSelectorProps {
  person: Person;
  sessions: WorkoutSession[];
  onSelectLocation: (location: LocationKey) => void;
}

interface LocationOption {
  key: LocationKey;
  description: string;
  gradient: string;
  icon: LucideIcon;
  plan: WorkoutPlan;
  onlyFor?: Person;
  // Nur für Neli relevant: Gruppierung nach Ort
  place?: 'studio' | 'home';
}

const locations: LocationOption[] = [
  {
    key: 'gym',
    description: 'Ganzkörper an den Geräten',
    gradient: 'from-indigo-500 to-purple-600',
    icon: Building2,
    plan: gymWorkoutPlan,
    onlyFor: 'neli', // Thomas geht nicht ins Fitnessstudio
    place: 'studio',
  },
  {
    key: 'home',
    description: 'Mit kleinen Hanteln',
    gradient: 'from-pink-400 to-rose-500',
    icon: Dumbbell,
    plan: homeWorkoutPlan,
    place: 'home',
  },
  {
    key: 'home2',
    description: 'Bauch, Beine, Po & Ausdauer',
    gradient: 'from-emerald-500 to-green-400',
    icon: HeartPulse,
    plan: homeWorkoutPlan2,
    place: 'home',
  },
  {
    key: 'back',
    description: 'Rumpfstabilität für den Rücken',
    gradient: 'from-teal-500 to-cyan-600',
    icon: PersonStanding,
    plan: backWorkoutPlan,
    onlyFor: 'thomas',
  },
  {
    key: 'neck',
    description: 'Nacken, Schulter & Brustwirbelsäule',
    gradient: 'from-sky-500 to-blue-600',
    icon: Activity,
    plan: neckWorkoutPlan,
    onlyFor: 'thomas',
  },
  {
    key: 'morning',
    description: 'Morgen-Reset in 10 Teilen',
    gradient: 'from-amber-400 to-orange-500',
    icon: Sunrise,
    plan: morningWorkoutPlan,
    onlyFor: 'thomas',
  },
];

// Zuletzt gewählter Plan pro Person (nur zum Vorreihen/Hervorheben)
const lastPlanKey = (person: Person) => `lastPlan.${person}`;

function loadLastPlan(person: Person): LocationKey | null {
  try {
    const saved = localStorage.getItem(lastPlanKey(person));
    return locations.some(l => l.key === saved) ? (saved as LocationKey) : null;
  } catch {
    return null;
  }
}

function saveLastPlan(person: Person, key: LocationKey): void {
  try {
    localStorage.setItem(lastPlanKey(person), key);
  } catch {
    // egal – dann eben ohne Vorreihung
  }
}

function LocationSelector({ person, sessions, onSelectLocation }: LocationSelectorProps) {
  const now = new Date();
  const lastPlan = loadLastPlan(person);

  const withStatus = locations
    .filter(loc => !loc.onlyFor || loc.onlyFor === person)
    .map(loc => {
      const planSessions = sessions.filter(s => s.planName === loc.plan.name);
      return {
        ...loc,
        doneToday: planSessions.some(s => isSameLocalDay(new Date(s.date), now)),
        thisWeek: planSessions.filter(s => isInWeekOf(new Date(s.date), now)).length,
      };
    });

  // Reihenfolge: Thomas vor 11 Uhr die Morgen-Routine zuerst (falls heute offen),
  // dann der zuletzt gewählte Plan, dann der Rest in fester Reihenfolge.
  const rank = (loc: (typeof withStatus)[number]) => {
    if (person === 'thomas' && loc.key === 'morning' && now.getHours() < 11 && !loc.doneToday) return 0;
    if (loc.key === lastPlan) return 1;
    return 2;
  };
  const visibleLocations = withStatus.toSorted((a, b) => rank(a) - rank(b));

  // Neli: nach Ort gruppiert (Fitnessstudio / zu Hause). Thomas: eine Liste.
  const groups: { title?: string; items: typeof visibleLocations }[] =
    person === 'neli'
      ? [
          { title: 'Im Fitnessstudio', items: visibleLocations.filter(l => l.place === 'studio') },
          { title: 'Zu Hause', items: visibleLocations.filter(l => l.place !== 'studio') },
        ].filter(g => g.items.length > 0)
      : [{ items: visibleLocations }];

  const handleSelect = (key: LocationKey) => {
    saveLastPlan(person, key);
    onSelectLocation(key);
  };

  return (
    <div className="min-h-dvh bg-slate-900 px-4 py-8 flex justify-center">
      <div className="max-w-[500px] w-full">
        <h1 className="text-white text-3xl font-bold mb-1">
          Was trainierst du heute?
        </h1>
        <p className="text-slate-400 text-base mb-6">
          Wähle deinen Trainingsplan
        </p>

        {groups.map(group => (
        <section key={group.title ?? 'alle'} className="mb-6">
          {group.title && (
            <h2 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2 px-1">
              {group.title}
            </h2>
          )}
        <div className="flex flex-col gap-3">
          {group.items.map(({ key, description, gradient, icon: Icon, plan, doneToday, thisWeek }) => {
            const isLast = key === lastPlan;
            return (
              <button
                key={key}
                onClick={() => handleSelect(key)}
                className={`flex items-center gap-4 p-4 rounded-2xl border text-left transition-colors active:scale-[0.99] ${
                  isLast
                    ? 'bg-slate-800 border-indigo-500/60 ring-1 ring-indigo-500/40'
                    : 'bg-slate-800/50 border-slate-700/50 hover:bg-slate-800'
                }`}
              >
                <div
                  className={`w-12 h-12 flex items-center justify-center rounded-xl shrink-0 bg-gradient-to-br ${gradient} text-white`}
                >
                  <Icon className="w-6 h-6" />
                </div>
                <div className="flex flex-col gap-0.5 flex-1 min-w-0">
                  <span className="flex items-center gap-2">
                    <span className="text-lg font-semibold text-white leading-tight">{planTitle(plan.name)}</span>
                    {isLast && (
                      <span className="text-[11px] font-medium uppercase tracking-wider text-indigo-300 bg-indigo-500/15 rounded px-1.5 py-0.5">
                        Zuletzt
                      </span>
                    )}
                  </span>
                  <span className="text-sm text-slate-400">{description}</span>
                </div>
                <div className="flex flex-col items-end gap-1 shrink-0 text-right">
                  {doneToday && (
                    <span className="flex items-center gap-1 text-xs font-medium text-emerald-400">
                      <CircleCheck className="w-4 h-4" aria-hidden="true" />
                      heute erledigt
                    </span>
                  )}
                  <span className="text-xs text-slate-500">
                    diese Woche {thisWeek}/{plan.sessionsPerWeek}
                  </span>
                </div>
              </button>
            );
          })}
        </div>
        </section>
        ))}

        <div className="text-center">
          <VersionBadge />
        </div>
      </div>
    </div>
  );
}

export default LocationSelector;
