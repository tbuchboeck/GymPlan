import { useEffect, useId, useRef, useState } from 'react';
import { signalTimerEnd } from '../lib/workout-progress';
import { Button } from './ui/Button';

interface RestTimerProps {
  seconds: number;
  label?: string;
  hint?: string;
  skipLabel?: string;
  /** Akzentverlauf des Rings (Plan-Farbe) */
  accentFrom?: string;
  accentTo?: string;
  /** Kleines Vorschaubild (aktuelle bzw. nächste Übung) */
  previewImage?: string;
  onComplete: () => void;
  onSkip: () => void;
}

const R = 88;
const CIRCUMFERENCE = 2 * Math.PI * R;

// Rechnet gegen die Uhrzeit (endAt), damit der Timer auch im Hintergrund
// bzw. bei gedrosseltem setInterval nicht nachgeht.
export function RestTimer({
  seconds,
  label = 'Pause',
  hint,
  skipLabel = 'Überspringen →',
  accentFrom = '#6366f1',
  accentTo = '#8b5cf6',
  previewImage,
  onComplete,
  onSkip,
}: RestTimerProps) {
  const [remainingMs, setRemainingMs] = useState(seconds * 1000);
  const onCompleteRef = useRef(onComplete);
  onCompleteRef.current = onComplete;
  const gradientId = useId();

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
  // Ring leert sich: voll am Anfang, leer am Ende
  const fraction = seconds > 0 ? remainingMs / (seconds * 1000) : 0;
  const dashOffset = CIRCUMFERENCE * (1 - fraction);
  const ringSize = previewImage ? 'h-56 w-56' : 'h-64 w-64';

  return (
    <div className="flex w-full max-w-sm flex-1 flex-col items-center px-safe-6 pt-6 pb-safe-4">
      <div className="flex w-full flex-1 flex-col items-center justify-center gap-6 animate-scale-in">
        {/* Beschriftung */}
        <div className="text-center">
          <div className="text-sm font-semibold uppercase tracking-widest text-slate-400">{label}</div>
          {hint && <div className="mt-1.5 text-xl font-semibold leading-snug text-white">{hint}</div>}
        </div>

        {/* Ring */}
        <div className={`relative ${ringSize}`}>
          <div
            aria-hidden="true"
            className="absolute inset-8 rounded-full opacity-25 blur-2xl"
            style={{ background: `linear-gradient(135deg, ${accentFrom}, ${accentTo})` }}
          />
          <svg viewBox="0 0 200 200" className="relative h-full w-full">
            <defs>
              <linearGradient id={gradientId} x1="0" y1="0" x2="1" y2="1">
                <stop offset="0" stopColor={accentFrom} />
                <stop offset="1" stopColor={accentTo} />
              </linearGradient>
            </defs>
            <circle cx="100" cy="100" r={R} fill="none" stroke="#1e293b" strokeWidth="12" />
            <circle
              cx="100"
              cy="100"
              r={R}
              fill="none"
              stroke={`url(#${gradientId})`}
              strokeWidth="12"
              strokeLinecap="round"
              strokeDasharray={CIRCUMFERENCE}
              strokeDashoffset={dashOffset}
              className="timer-ring"
              transform="rotate(-90 100 100)"
            />
          </svg>
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-6xl font-bold tabular-nums tracking-tight text-white" aria-live="off">
              {String(minutes).padStart(2, '0')}:{String(secs).padStart(2, '0')}
            </span>
          </div>
        </div>

        {previewImage && (
          <img
            src={previewImage}
            alt=""
            className="aspect-[4/3] w-48 rounded-2xl object-contain ring-1 ring-white/10 shadow-lg shadow-black/40"
          />
        )}
      </div>

      {/* Überspringen / Abbrechen im Daumenbereich */}
      <Button variant="secondary" size="lg" block onClick={onSkip} className="mt-6">
        {skipLabel}
      </Button>
    </div>
  );
}
