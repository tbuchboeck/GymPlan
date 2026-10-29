import { useState, useMemo, useEffect, useRef, lazy, Suspense } from 'react';
import { gymWorkoutPlan, homeWorkoutPlan, homeWorkoutPlan2, backWorkoutPlan, neckWorkoutPlan, morningWorkoutPlan } from './data/workoutPlan';
import type { WorkoutSession } from './types';
import { authService, type Person } from './lib/auth-service';
import { useLocalStorage } from './hooks/useLocalStorage';
import { pushSession, pushAllAndPull, mergeSessions } from './lib/session-sync';
import { Home } from './components/Home';
import { WorkoutView } from './components/WorkoutView';
import { WorkoutSummary } from './components/WorkoutSummary';
import { AuthScreen } from './components/AuthScreen';
import LocationSelector, { type LocationKey } from './components/LocationSelector';

const WorkoutHistory = lazy(() => import('./components/WorkoutHistory').then(m => ({ default: m.WorkoutHistory })));

type AppView = 'home' | 'workout' | 'summary' | 'history';
type Location = LocationKey | null;

// Legacy: sessions used to live under one key shared by everyone on the
// device. Hand them to the first person who logs in here, once.
const LEGACY_SESSIONS_KEY = 'workoutSessions';
const sessionsKey = (person: Person) => `workoutSessions.${person}`;

function migrateLegacySessions(person: Person) {
  try {
    const legacy = localStorage.getItem(LEGACY_SESSIONS_KEY);
    if (legacy === null) return;
    if (localStorage.getItem(sessionsKey(person)) === null) {
      localStorage.setItem(sessionsKey(person), legacy);
    }
    localStorage.removeItem(LEGACY_SESSIONS_KEY);
  } catch {
    // localStorage unavailable — nothing to migrate.
  }
}

function App() {
  // Gespeicherte Sitzung (max. 7 Tage) → direkt entsperrt, auch offline
  const [person, setPerson] = useState<Person | null>(() => {
    const saved = authService.getSession()?.person ?? null;
    if (saved) migrateLegacySessions(saved);
    return saved;
  });

  if (!person) {
    return (
      <AuthScreen
        onUnlock={(p) => {
          migrateLegacySessions(p);
          setPerson(p);
        }}
      />
    );
  }

  const handleLogout = () => {
    authService.clearSession();
    setPerson(null);
  };

  return <PersonApp key={person} person={person} onLogout={handleLogout} />;
}

function PersonApp({ person, onLogout }: { person: Person; onLogout: () => void }) {
  const [location, setLocation] = useState<Location>(null);
  const [currentView, setCurrentView] = useState<AppView>('home');
  const [sessions, setSessions] = useLocalStorage<WorkoutSession[]>(sessionsKey(person), []);
  const [currentSession, setCurrentSession] = useState<WorkoutSession | null>(null);
  // undefined = gespeicherten Stand fortsetzen (falls vorhanden), Zahl = gezielt bei dieser Übung einsteigen
  const [startExerciseIndex, setStartExerciseIndex] = useState<number | undefined>(undefined);
  const hasSynced = useRef(false);

  // Scroll to top on every view change
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [currentView]);

  // Sync with Supabase once after unlock
  useEffect(() => {
    if (hasSynced.current) return;
    hasSynced.current = true;

    pushAllAndPull(sessions).then((remote) => {
      if (remote) setSessions((cur) => mergeSessions(cur, remote));
    });
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const workoutPlan = useMemo(() => {
    if (location === 'home') return homeWorkoutPlan;
    if (location === 'home2') return homeWorkoutPlan2;
    if (location === 'back') return backWorkoutPlan;
    if (location === 'neck') return neckWorkoutPlan;
    if (location === 'morning') return morningWorkoutPlan;
    return gymWorkoutPlan;
  }, [location]);

  const handleStartWorkout = () => {
    setStartExerciseIndex(undefined);
    setCurrentView('workout');
  };

  const handleStartExercise = (exerciseIndex: number) => {
    setStartExerciseIndex(exerciseIndex);
    setCurrentView('workout');
  };

  const handleWorkoutComplete = (session: WorkoutSession) => {
    setSessions([...sessions, session]);
    setCurrentSession(session);
    setCurrentView('summary');
    // Fire-and-forget push to Supabase
    pushSession(session);
  };

  const handleSummaryClose = () => {
    setCurrentSession(null);
    setCurrentView('home');
  };

  const handleImportSessions = (importedSessions: WorkoutSession[]) => {
    const existingIds = new Set(sessions.map(s => s.id));
    const uniqueImportedSessions = importedSessions.filter(s => !existingIds.has(s.id));
    const allSessions = [...sessions, ...uniqueImportedSessions];
    setSessions(allSessions);
    // Sync imported sessions to Supabase too
    for (const s of uniqueImportedSessions) {
      pushSession(s);
    }
  };

  if (!location) {
    return <LocationSelector person={person} sessions={sessions} onSelectLocation={(loc) => setLocation(loc)} />;
  }

  return (
    <div className="min-h-dvh bg-slate-900">
      {currentView === 'home' && (
        <Home
          person={person}
          workoutPlan={workoutPlan}
          sessions={sessions}
          onStartWorkout={handleStartWorkout}
          onStartExercise={handleStartExercise}
          onViewHistory={() => setCurrentView('history')}
          onSwitchPlan={() => setLocation(null)}
          onLogout={onLogout}
        />
      )}

      {currentView === 'workout' && (
        <WorkoutView
          exercises={workoutPlan.exercises}
          planName={workoutPlan.name}
          person={person}
          onComplete={handleWorkoutComplete}
          onExit={() => setCurrentView('home')}
          initialExerciseIndex={startExerciseIndex}
        />
      )}

      {currentView === 'summary' && currentSession && (
        <WorkoutSummary
          session={currentSession}
          person={person}
          onClose={handleSummaryClose}
          onUpdateSession={(updated) => {
            setSessions((cur) => cur.map((s) => (s.id === updated.id ? updated : s)));
            setCurrentSession(updated);
            pushSession(updated);
          }}
        />
      )}

      {currentView === 'history' && (
        <Suspense fallback={
          <div className="h-dvh bg-slate-900 flex items-center justify-center">
            <div className="w-8 h-8 border-2 border-indigo-400 border-t-transparent rounded-full animate-spin" />
          </div>
        }>
          <WorkoutHistory
            sessions={sessions}
            person={person}
            onClose={() => setCurrentView('home')}
            onImport={handleImportSessions}
          />
        </Suspense>
      )}

    </div>
  );
}

export default App;
