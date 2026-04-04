import { useState, useCallback, useEffect } from 'react';
import { Lock } from 'lucide-react';
import { verifyPin, isSessionValid } from '../lib/pin-service';

const PIN_LENGTH = 4;

interface PinLoginProps {
  onSuccess: () => void;
}

export function PinLogin({ onSuccess }: PinLoginProps) {
  const [pin, setPin] = useState('');
  const [error, setError] = useState('');
  const [shake, setShake] = useState(false);
  const [checking, setChecking] = useState(false);

  // Skip PIN if session is still valid
  useEffect(() => {
    if (isSessionValid()) {
      onSuccess();
    }
  }, [onSuccess]);

  const handleDigit = useCallback(
    (digit: string) => {
      if (checking) return;
      setError('');
      setPin((prev) => {
        if (prev.length >= PIN_LENGTH) return prev;
        return prev + digit;
      });
    },
    [checking]
  );

  const handleDelete = useCallback(() => {
    if (checking) return;
    setPin((prev) => prev.slice(0, -1));
    setError('');
  }, [checking]);

  // Auto-submit when PIN is complete
  useEffect(() => {
    if (pin.length !== PIN_LENGTH) return;
    setChecking(true);
    verifyPin(pin).then((result) => {
      if (result.success) {
        onSuccess();
      } else {
        setError(result.error ?? 'Falscher PIN');
        setShake(true);
        setTimeout(() => {
          setShake(false);
          setPin('');
          setChecking(false);
        }, 600);
      }
    });
  }, [pin, onSuccess]);

  // Keyboard support
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key >= '0' && e.key <= '9') handleDigit(e.key);
      else if (e.key === 'Backspace') handleDelete();
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [handleDigit, handleDelete]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-indigo-900 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-full mb-4">
            <Lock className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-white mb-2">GymPlan</h1>
          <p className="text-slate-300">PIN eingeben</p>
        </div>

        {/* PIN Dots */}
        <div className={`flex justify-center gap-4 mb-12 ${shake ? 'animate-shake' : ''}`}>
          {Array.from({ length: PIN_LENGTH }).map((_, i) => (
            <div
              key={i}
              className={`w-4 h-4 rounded-full transition-all duration-200 ${
                i < pin.length
                  ? error
                    ? 'bg-red-500 scale-110'
                    : 'bg-gradient-to-r from-cyan-400 to-blue-500'
                  : 'bg-slate-700'
              }`}
            />
          ))}
        </div>

        {error && (
          <div className="text-center mb-6">
            <p className="text-red-400 font-semibold">{error}</p>
          </div>
        )}

        {/* Number Pad */}
        <div className="grid grid-cols-3 gap-4 mb-4">
          {[1, 2, 3, 4, 5, 6, 7, 8, 9].map((num) => (
            <button
              key={num}
              onClick={() => handleDigit(String(num))}
              className="aspect-square bg-gradient-to-br from-slate-800 to-slate-900 border-2 border-slate-700 rounded-xl text-white text-2xl font-bold hover:border-purple-500 hover:shadow-lg hover:shadow-purple-500/50 active:scale-95 transition-all"
            >
              {num}
            </button>
          ))}
        </div>

        <div className="grid grid-cols-3 gap-4">
          <div />
          <button
            onClick={() => handleDigit('0')}
            className="aspect-square bg-gradient-to-br from-slate-800 to-slate-900 border-2 border-slate-700 rounded-xl text-white text-2xl font-bold hover:border-purple-500 hover:shadow-lg hover:shadow-purple-500/50 active:scale-95 transition-all"
          >
            0
          </button>
          <button
            onClick={handleDelete}
            className="aspect-square bg-gradient-to-br from-slate-800 to-slate-900 border-2 border-slate-700 rounded-xl text-white text-xl font-bold hover:border-red-500 hover:shadow-lg hover:shadow-red-500/50 active:scale-95 transition-all"
          >
            ←
          </button>
        </div>

        {checking && (
          <div className="mt-6 flex justify-center">
            <div className="w-6 h-6 border-2 border-purple-400 border-t-transparent rounded-full animate-spin" />
          </div>
        )}
      </div>
    </div>
  );
}
