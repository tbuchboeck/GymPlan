import { useEffect, useRef, useState } from 'react';
import { signalTimerEnd } from '../lib/workout-progress';

interface RestTimerProps {
  seconds: number;
  label?: string;
  hint?: string;
  skipLabel?: string;
  onComplete: () => void;
  onSkip: () => void;
}

// Rechnet gegen die Uhrzeit (endAt), damit der Timer auch im Hintergrund
// bzw. bei gedrosseltem setInterval nicht nachgeht.
export function RestTimer({ seconds, label = 'Pause', hint, skipLabel = 'Überspringen →', onComplete, onSkip }: RestTimerProps) {
  const [remainingMs, setRemainingMs] = useState(seconds * 1000);
  const onCompleteRef = useRef(onComplete);
  onCompleteRef.current = onComplete;

  useEffect(() => {
    const endAt = Date.now() + seconds * 1000;
    let done = false;

    const tick = () => {
      if (done) return;
      const left = Math.max(0, endAt - Date.now());
      setRemainingMs(left);
      if (left <= 0) {
        done = true;
        clearInterval(timer);
        signalTimerEnd();
        onCompleteRef.current();
      }
    };

    const timer = setInterval(tick, 250);
    const onVisibility = () => {
      if (document.visibilityState === 'visible') tick();
    };
    document.addEventListener('visibilitychange', onVisibility);
    return () => {
      done = true;
      clearInterval(timer);
      document.removeEventListener('visibilitychange', onVisibility);
    };
  }, [seconds]);

  const timeLeft = Math.ceil(remainingMs / 1000);
  const minutes = Math.floor(timeLeft / 60);
  const secs = timeLeft % 60;
  const circumference = 2 * Math.PI * 54;
  // Ring leert sich: voll am Anfang, leer am Ende
  const fraction = seconds > 0 ? remainingMs / (seconds * 1000) : 0;
  const dashOffset = circumference * (1 - fraction);

  return (
    <div className="bg-slate-800 border border-slate-700 rounded-2xl p-6 shadow-2xl animate-fade-in max-w-xs w-full">
      {/* Label */}
      <div className="text-center mb-4">
        <span className="text-sm text-slate-400 uppercase tracking-wider">{label}</span>
        {hint && <div className="mt-1 text-base font-semibold text-white">{hint}</div>}
      </div>

      {/* Circular progress */}
      <div className="flex justify-center mb-4">
        <div className="relative w-40 h-40">
          <svg viewBox="0 0 120 120" className="w-40 h-40">
            <circle
              cx="60" cy="60" r="54"
              fill="none"
              stroke="#1e293b"
              strokeWidth="8"
            />
            <circle
              cx="60" cy="60" r="54"
              fill="none"
              stroke="#6366f1"
              strokeWidth="8"
              strokeLinecap="round"
              strokeDasharray={circumference}
              strokeDashoffset={dashOffset}
              className="timer-ring"
              transform="rotate(-90 60 60)"
            />
          </svg>
          {/* Time display centered over ring */}
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-4xl font-mono font-bold text-white" aria-live="off">
              {String(minutes).padStart(2, '0')}:{String(secs).padStart(2, '0')}
            </span>
          </div>
        </div>
      </div>

      {/* Skip button */}
      <button
        type="button"
        onClick={onSkip}
        className="w-full min-h-11 px-4 py-2 rounded-xl bg-slate-700 hover:bg-slate-600 text-slate-200 hover:text-white font-medium transition-colors"
      >
        {skipLabel}
      </button>
    </div>
  );
}
