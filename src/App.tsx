import { useState } from 'react';
import { workoutPlan } from './data/workoutPlan';
import type { WorkoutSession } from './types';
import { useLocalStorage } from './hooks/useLocalStorage';
import { Home } from './components/Home';
import { WorkoutView } from './components/WorkoutView';
import { WorkoutSummary } from './components/WorkoutSummary';
import { WorkoutHistory } from './components/WorkoutHistory';
import { ReminderSettings } from './components/ReminderSettings';
import { PinLogin } from './components/PinLogin';
import LocationSelector from './components/LocationSelector';

type AppView = 'home' | 'workout' | 'summary' | 'history' | 'reminders';
type Location = 'gym' | 'home' | null;

function App() {
  const [isUnlocked, setIsUnlocked] = useState(false);
  const [location, setLocation] = useState<Location>(null);
  const [currentView, setCurrentView] = useState<AppView>('home');
  const [sessions, setSessions] = useLocalStorage<WorkoutSession[]>('workoutSessions', []);
  const [currentSession, setCurrentSession] = useState<WorkoutSession | null>(null);
  const [startExerciseIndex, setStartExerciseIndex] = useState<number>(0);

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

  const handleViewHistory = () => {
    setCurrentView('history');
  };

  const handleManageReminders = () => {
    setCurrentView('reminders');
  };

  const handleExitWorkout = () => {
    setCurrentView('home');
  };

  const handleCloseHistory = () => {
    setCurrentView('home');
  };

  const handleCloseReminders = () => {
    setCurrentView('home');
  };

  // Show PIN login if app is locked
  if (!isUnlocked) {
    return (
      <PinLogin
        onSuccess={() => setIsUnlocked(true)}
      />
    );
  }

  // Show location selector after PIN login
  if (!location) {
    return (
      <LocationSelector
        onSelectLocation={(selectedLocation) => setLocation(selectedLocation)}
      />
    );
  }

  // Show main app once unlocked
  return (
    <>
      {currentView === 'home' && (
        <Home
          workoutPlan={workoutPlan}
          sessions={sessions}
          onStartWorkout={handleStartWorkout}
          onStartExercise={handleStartExercise}
          onViewHistory={handleViewHistory}
          onManageReminders={handleManageReminders}
        />
      )}

      {currentView === 'workout' && (
        <WorkoutView
          exercises={workoutPlan.exercises}
          onComplete={handleWorkoutComplete}
          onExit={handleExitWorkout}
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
        <WorkoutHistory
          sessions={sessions}
          onClose={handleCloseHistory}
        />
      )}

      {currentView === 'reminders' && (
        <ReminderSettings
          onClose={handleCloseReminders}
        />
      )}
    </>
  );
}

export default App;
