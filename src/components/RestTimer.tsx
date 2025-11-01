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
    <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-3xl p-8 text-white shadow-2xl border-2 border-cyan-500">
      <div className="text-center mb-6">
        <h3 className="text-2xl font-bold mb-4 text-cyan-300">Pause</h3>
        <div className="relative inline-block">
          <div className="absolute inset-0 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-full blur-2xl opacity-50 animate-pulse"></div>
          <div className="relative bg-gradient-to-br from-cyan-500 via-blue-600 to-purple-600 rounded-full p-12 shadow-2xl">
            <div className="text-7xl font-bold font-mono tracking-tight">
              {String(minutes).padStart(2, '0')}:{String(secs).padStart(2, '0')}
            </div>
          </div>
        </div>
      </div>

      <div className="w-full bg-slate-700 rounded-full h-4 mb-6 overflow-hidden shadow-inner">
        <div
          className="bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-500 h-full rounded-full transition-all duration-1000 ease-linear shadow-lg"
          style={{ width: `${progress}%` }}
        />
      </div>

      <div className="text-center text-slate-300 mb-4 text-lg">
        {seconds - timeLeft} von {seconds} Sekunden
      </div>

      <button
        onClick={onSkip}
        className="w-full bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600 backdrop-blur-sm py-4 px-6 rounded-xl font-bold text-lg transition-all transform hover:scale-105 shadow-xl"
      >
        Pause überspringen
      </button>
    </div>
  );
}
