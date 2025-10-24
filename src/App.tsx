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

type AppView = 'home' | 'workout' | 'summary' | 'history' | 'reminders';

function App() {
  const [isUnlocked, setIsUnlocked] = useState(false);
  const [currentView, setCurrentView] = useState<AppView>('home');
  const [sessions, setSessions] = useLocalStorage<WorkoutSession[]>('workoutSessions', []);
  const [currentSession, setCurrentSession] = useState<WorkoutSession | null>(null);

  const handleStartWorkout = () => {
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

  // Show main app once unlocked
  return (
    <>
      {currentView === 'home' && (
        <Home
          workoutPlan={workoutPlan}
          sessions={sessions}
          onStartWorkout={handleStartWorkout}
          onViewHistory={handleViewHistory}
          onManageReminders={handleManageReminders}
        />
      )}

      {currentView === 'workout' && (
        <WorkoutView
          exercises={workoutPlan.exercises}
          onComplete={handleWorkoutComplete}
          onExit={handleExitWorkout}
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
