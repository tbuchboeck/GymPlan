import { useEffect, useState } from 'react';

interface RestTimerProps {
  seconds: number;
  onComplete: () => void;
  onSkip: () => void;
}

export function RestTimer({ seconds, onComplete, onSkip }: RestTimerProps) {
  const [timeLeft, setTimeLeft] = useState(seconds);

  useEffect(() => {
    setTimeLeft(seconds);
  }, [seconds]);

  useEffect(() => {
    if (timeLeft <= 0) {
      onComplete();
      return;
    }

    const timer = setInterval(() => {
      setTimeLeft((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [timeLeft, onComplete]);

  const minutes = Math.floor(timeLeft / 60);
  const secs = timeLeft % 60;
  const progress = ((seconds - timeLeft) / seconds) * 100;

  return (
    <div className="bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl p-6 text-white shadow-lg">
      <div className="text-center mb-4">
        <h3 className="text-xl font-semibold mb-2">Pause</h3>
        <div className="text-5xl font-bold font-mono">
          {String(minutes).padStart(2, '0')}:{String(secs).padStart(2, '0')}
        </div>
      </div>

      <div className="w-full bg-white/30 rounded-full h-3 mb-4 overflow-hidden">
        <div
          className="bg-white h-full rounded-full transition-all duration-1000 ease-linear"
          style={{ width: `${progress}%` }}
        />
      </div>

      <button
        onClick={onSkip}
        className="w-full bg-white/20 hover:bg-white/30 backdrop-blur-sm py-3 px-6 rounded-xl font-semibold transition-colors"
      >
        Pause überspringen
      </button>
    </div>
  );
}
