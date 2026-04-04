import { useEffect, useRef, useState } from 'react';

interface RestTimerProps {
  seconds: number;
  onComplete: () => void;
  onSkip: () => void;
}

export function RestTimer({ seconds, onComplete, onSkip }: RestTimerProps) {
  const [timeLeft, setTimeLeft] = useState(seconds);
  const onCompleteRef = useRef(onComplete);
  onCompleteRef.current = onComplete;

  useEffect(() => {
    setTimeLeft(seconds);
  }, [seconds]);

  useEffect(() => {
    if (timeLeft <= 0) {
      onCompleteRef.current();
      return;
    }

    const timer = setInterval(() => {
      setTimeLeft((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [timeLeft]);

  const minutes = Math.floor(timeLeft / 60);
  const secs = timeLeft % 60;
  const circumference = 2 * Math.PI * 54;
  const dashOffset = circumference * (timeLeft / seconds);

  return (
    <div className="bg-slate-800 border border-slate-700 rounded-2xl p-6 shadow-2xl animate-fade-in max-w-xs w-full">
      {/* Label */}
      <div className="text-center mb-4">
        <span className="text-sm text-slate-400 uppercase tracking-wider">Pause</span>
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
            <span className="text-4xl font-mono font-bold text-white">
              {String(minutes).padStart(2, '0')}:{String(secs).padStart(2, '0')}
            </span>
          </div>
        </div>
      </div>

      {/* Skip button */}
      <div className="text-center">
        <button
          onClick={onSkip}
          className="text-slate-400 hover:text-white transition-colors text-sm"
        >
          Überspringen →
        </button>
      </div>
    </div>
  );
}
