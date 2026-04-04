import { useState, useMemo, useEffect, lazy, Suspense } from 'react';
import { gymWorkoutPlan, homeWorkoutPlan, homeWorkoutPlan2, backWorkoutPlan } from './data/workoutPlan';
import type { WorkoutSession } from './types';
import { useLocalStorage } from './hooks/useLocalStorage';
import { Home } from './components/Home';
import { WorkoutView } from './components/WorkoutView';
import { WorkoutSummary } from './components/WorkoutSummary';
import { ReminderSettings } from './components/ReminderSettings';
import { PinLogin } from './components/PinLogin';
import LocationSelector from './components/LocationSelector';

const WorkoutHistory = lazy(() => import('./components/WorkoutHistory').then(m => ({ default: m.WorkoutHistory })));

type AppView = 'home' | 'workout' | 'summary' | 'history' | 'reminders';
type Location = 'gym' | 'home' | 'home2' | 'back' | null;

function App() {
  const [isUnlocked, setIsUnlocked] = useState(false);
  const [location, setLocation] = useState<Location>(null);
  const [currentView, setCurrentView] = useState<AppView>('home');
  const [sessions, setSessions] = useLocalStorage<WorkoutSession[]>('workoutSessions', []);
  const [currentSession, setCurrentSession] = useState<WorkoutSession | null>(null);
  const [startExerciseIndex, setStartExerciseIndex] = useState<number>(0);

  // Scroll to top on every view change — prevents "starting mid-page"
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [currentView]);

  const workoutPlan = useMemo(() => {
    if (location === 'home') return homeWorkoutPlan;
    if (location === 'home2') return homeWorkoutPlan2;
    if (location === 'back') return backWorkoutPlan;
    return gymWorkoutPlan;
  }, [location]);

  const handleStartWorkout = () => {
    setStartExerciseIndex(0);
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
  };

  const handleSummaryClose = () => {
    setCurrentSession(null);
    setCurrentView('home');
  };

  const handleImportSessions = (importedSessions: WorkoutSession[]) => {
    const existingIds = new Set(sessions.map(s => s.id));
    const uniqueImportedSessions = importedSessions.filter(s => !existingIds.has(s.id));
    setSessions([...sessions, ...uniqueImportedSessions]);
  };

  if (!isUnlocked) {
    return <PinLogin onSuccess={() => setIsUnlocked(true)} />;
  }

  if (!location) {
    return <LocationSelector onSelectLocation={(loc) => setLocation(loc)} />;
  }

  return (
    <div className="min-h-dvh bg-slate-900">
      {currentView === 'home' && (
        <Home
          workoutPlan={workoutPlan}
          sessions={sessions}
          onStartWorkout={handleStartWorkout}
          onStartExercise={handleStartExercise}
          onViewHistory={() => setCurrentView('history')}
          onManageReminders={() => setCurrentView('reminders')}
          onSwitchPlan={() => setLocation(null)}
        />
      )}

      {currentView === 'workout' && (
        <WorkoutView
          exercises={workoutPlan.exercises}
          planName={workoutPlan.name}
          onComplete={handleWorkoutComplete}
          onExit={() => setCurrentView('home')}
          initialExerciseIndex={startExerciseIndex}
        />
      )}

      {currentView === 'summary' && currentSession && (
        <WorkoutSummary
          session={currentSession}
          onClose={handleSummaryClose}
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
            onClose={() => setCurrentView('home')}
            onImport={handleImportSessions}
          />
        </Suspense>
      )}

      {currentView === 'reminders' && (
        <ReminderSettings onClose={() => setCurrentView('home')} />
      )}
    </div>
  );
}

export default App;
