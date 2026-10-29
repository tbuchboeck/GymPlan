import { Check, ChevronRight, ArrowRight } from 'lucide-react';
import type { Person } from '../lib/auth-service';
import type { WorkoutPlan, WorkoutSession } from '../types';
import { gymWorkoutPlan, homeWorkoutPlan, homeWorkoutPlan2, backWorkoutPlan, neckWorkoutPlan, morningWorkoutPlan } from '../data/workoutPlan';
import { isInWeekOf, isSameLocalDay } from '../utils/statistics';
import { VersionBadge } from './VersionBadge';
import { planTitle } from '../utils/format';
import { planTheme } from '../utils/plan-theme';

export type LocationKey = 'gym' | 'home' | 'home2' | 'back' | 'neck' | 'morning';

interface LocationSelectorProps {
  person: Person;
  sessions: WorkoutSession[];
  onSelectLocation: (location: LocationKey) => void;
}

interface LocationOption {
  key: LocationKey;
  description: string;
  plan: WorkoutPlan;
  onlyFor?: Person;
  // Nur für Neli relevant: Gruppierung nach Ort
  place?: 'studio' | 'home';
}

const locations: LocationOption[] = [
  {
    key: 'gym',
    description: 'Ganzkörper an den Geräten',
    plan: gymWorkoutPlan,
    onlyFor: 'neli', // Thomas geht nicht ins Fitnessstudio
    place: 'studio',
  },
  {
    key: 'home',
    description: 'Mit kleinen Hanteln',
    plan: homeWorkoutPlan,
    place: 'home',
  },
  {
    key: 'home2',
    description: 'Bauch, Beine, Po & Ausdauer',
    plan: homeWorkoutPlan2,
    place: 'home',
  },
  {
    key: 'back',
    description: 'Rumpfstabilität für den Rücken',
    plan: backWorkoutPlan,
    onlyFor: 'thomas',
  },
  {
    key: 'neck',
    description: 'Nacken, Schulter & Brustwirbelsäule',
    plan: neckWorkoutPlan,
    onlyFor: 'thomas',
  },
  {
    key: 'morning',
    description: 'Morgen-Reset in 10 Teilen',
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

  const handleSelect = (key: LocationKey) => {
    saveLastPlan(person, key);
    onSelectLocation(key);
  };

  // Vorschlag für heute = oberster Plan der Reihung, groß hervorgehoben
  const [suggestion, ...rest] = visibleLocations;
  const groups: { title?: string; items: typeof visibleLocations }[] =
    person === 'neli'
      ? [
          { title: 'Im Fitnessstudio', items: rest.filter(l => l.place === 'studio') },
          { title: 'Zu Hause', items: rest.filter(l => l.place !== 'studio') },
        ].filter(g => g.items.length > 0)
      : [{ title: 'Weitere Pläne', items: rest }];

  const name = person === 'thomas' ? 'Thomas' : 'Neli';
  const hour = now.getHours();
  const greeting = hour < 11 ? `Guten Morgen, ${name}` : hour < 18 ? `Hallo ${name}` : `Guten Abend, ${name}`;
  const dateLabel = now.toLocaleDateString('de-AT', { weekday: 'long', day: 'numeric', month: 'long' });

  return (
    <div className="min-h-dvh bg-slate-950 px-safe-4 pt-safe-8 pb-safe-6">
      <div className="mx-auto w-full max-w-[500px]">
        <header className="mb-6 animate-slide-up">
          <p className="text-sm font-medium text-slate-400">{dateLabel}</p>
          <h1 className="mt-1 text-3xl font-bold tracking-tight text-white">{greeting}</h1>
          <p className="mt-1 text-lg text-slate-300">Was trainierst du heute?</p>
        </header>

        {suggestion && (
          <SuggestionCard
            option={suggestion}
            isLast={suggestion.key === lastPlan}
            placeLabel={person === 'neli' ? (suggestion.place === 'studio' ? 'Im Fitnessstudio' : 'Zu Hause') : undefined}
            onSelect={() => handleSelect(suggestion.key)}
          />
        )}

        {groups.map(group => (
          <section key={group.title ?? 'alle'} className="mt-7 animate-slide-up [animation-delay:120ms]">
            {group.title && (
              <h2 className="mb-3 px-1 text-xs font-semibold uppercase tracking-wider text-slate-500">{group.title}</h2>
            )}
            <div className="flex flex-col gap-3">
              {group.items.map(option => (
                <PlanRow
                  key={option.key}
                  option={option}
                  isLast={option.key === lastPlan}
                  onSelect={() => handleSelect(option.key)}
                />
              ))}
            </div>
          </section>
        ))}

        <div className="mt-8 text-center">
          <VersionBadge />
        </div>
      </div>
    </div>
  );
}

type PlanOption = LocationOption & { doneToday: boolean; thisWeek: number };

/** Wochenfortschritt als Punkte (bis 7 Einheiten) */
function WeekDots({ done, goal, onGradient = false }: { done: number; goal: number; onGradient?: boolean }) {
  return (
    <span className="flex items-center gap-1" aria-hidden="true">
      {Array.from({ length: goal }, (_, i) => (
        <span
          key={i}
          className={`h-2 w-2 rounded-full ${
            i < done
              ? onGradient ? 'bg-white' : 'bg-emerald-400'
              : onGradient ? 'bg-white/30' : 'bg-slate-700'
          }`}
        />
      ))}
    </span>
  );
}

function SuggestionCard({ option, isLast, placeLabel, onSelect }: {
  option: PlanOption;
  isLast: boolean;
  placeLabel?: string;
  onSelect: () => void;
}) {
  const { key, description, plan, doneToday, thisWeek } = option;
  const theme = planTheme(plan.name);
  const Icon = theme.icon;
  return (
    <button
      type="button"
      data-plan={key}
      onClick={onSelect}
      className={`group relative w-full overflow-hidden rounded-3xl bg-gradient-to-br ${theme.gradient} p-5 text-left text-white shadow-xl shadow-black/40 transition duration-200 active:scale-[0.98] animate-slide-up [animation-delay:60ms]`}
    >
      {/* dezentes Muster */}
      <svg aria-hidden="true" viewBox="0 0 200 200" className="pointer-events-none absolute -right-10 -top-10 h-52 w-52 text-white/15">
        <circle cx="100" cy="100" r="90" fill="none" stroke="currentColor" strokeWidth="14" />
        <circle cx="100" cy="100" r="55" fill="none" stroke="currentColor" strokeWidth="8" />
      </svg>
      <div aria-hidden="true" className="pointer-events-none absolute inset-0 bg-gradient-to-t from-black/25 via-black/5 to-transparent" />
      <div className="relative">
        <div className="flex items-center justify-between gap-3">
          <span className="rounded-full bg-black/20 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-white/95">
            Vorschlag für heute
          </span>
          {isLast && <span className="text-xs font-medium text-white/80">Zuletzt gewählt</span>}
        </div>

        <div className="mt-5 flex items-center gap-4">
          <span className="grid h-14 w-14 shrink-0 place-items-center rounded-2xl bg-white/20 ring-1 ring-white/30 backdrop-blur-sm">
            <Icon className="h-7 w-7" />
          </span>
          <span className="min-w-0">
            <span data-plan-title className="block text-2xl font-bold leading-tight">{planTitle(plan.name)}</span>
            <span className="block text-base text-white/85">
              {description}
              {placeLabel && <> · {placeLabel}</>}
            </span>
          </span>
        </div>

        <div className="mt-5 flex items-center justify-between gap-3">
          <div className="flex flex-col gap-1.5">
            <WeekDots done={thisWeek} goal={plan.sessionsPerWeek} onGradient />
            <span className="text-sm text-white/90">
              {doneToday ? (
                <span className="inline-flex items-center gap-1 font-semibold">
                  <Check className="h-4 w-4" strokeWidth={3} aria-hidden="true" /> heute erledigt
                </span>
              ) : null}
              {doneToday ? ' · ' : ''}diese Woche {thisWeek}/{plan.sessionsPerWeek}
            </span>
          </div>
          <span className="inline-flex min-h-12 items-center gap-1.5 rounded-2xl bg-white px-4 text-base font-semibold text-slate-900 shadow-md transition group-active:scale-95">
            Los geht’s
            <ArrowRight className="h-5 w-5" aria-hidden="true" />
          </span>
        </div>
      </div>
    </button>
  );
}

function PlanRow({ option, isLast, onSelect }: { option: PlanOption; isLast: boolean; onSelect: () => void }) {
  const { key, description, plan, doneToday, thisWeek } = option;
  const theme = planTheme(plan.name);
  const Icon = theme.icon;
  return (
    <button
      type="button"
      data-plan={key}
      onClick={onSelect}
      className="flex w-full items-center gap-4 rounded-2xl bg-slate-900 p-4 text-left ring-1 ring-white/5 transition duration-200 hover:bg-slate-800/80 active:scale-[0.99]"
    >
      <span className={`relative grid h-12 w-12 shrink-0 place-items-center rounded-xl bg-gradient-to-br ${theme.gradient} text-white shadow-md shadow-black/30`}>
        <Icon className="h-6 w-6" />
        {doneToday && (
          <span className="absolute -bottom-1 -right-1 grid h-5 w-5 place-items-center rounded-full bg-emerald-500 text-white ring-2 ring-slate-900">
            <Check className="h-3 w-3" strokeWidth={3.5} aria-hidden="true" />
          </span>
        )}
      </span>
      <span className="min-w-0 flex-1">
        <span className="flex flex-wrap items-center gap-x-2 gap-y-0.5">
          <span data-plan-title className="text-lg font-semibold leading-tight text-white">{planTitle(plan.name)}</span>
          {isLast && (
            <span className="rounded-md bg-indigo-500/15 px-1.5 py-0.5 text-[11px] font-semibold uppercase tracking-wider text-indigo-300">
              Zuletzt
            </span>
          )}
        </span>
        <span className="block text-sm text-slate-400">{description}</span>
        <span className="mt-2 flex flex-wrap items-center gap-x-2 gap-y-1 text-xs text-slate-400">
          <WeekDots done={thisWeek} goal={plan.sessionsPerWeek} />
          <span className="whitespace-nowrap">diese Woche {thisWeek}/{plan.sessionsPerWeek}</span>
          {doneToday && <span className="whitespace-nowrap font-semibold text-emerald-400">heute erledigt</span>}
        </span>
      </span>
      <ChevronRight className="h-5 w-5 shrink-0 text-slate-600" aria-hidden="true" />
    </button>
  );
}

export default LocationSelector;
