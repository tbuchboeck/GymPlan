import { useState } from 'react';
import { Lock } from 'lucide-react';

interface PinLoginProps {
  onSuccess: () => void;
}

const CORRECT_PIN = '6062';

export function PinLogin({ onSuccess }: PinLoginProps) {
  const [pin, setPin] = useState('');
  const [error, setError] = useState(false);

  const handleNumberClick = (num: number) => {
    if (pin.length < 4) {
      const newPin = pin + num;
      setPin(newPin);

      if (newPin.length === 4) {
        // Check PIN against fixed PIN
        if (newPin === CORRECT_PIN) {
          onSuccess();
        } else {
          setError(true);
          setTimeout(() => {
            setPin('');
            setError(false);
          }, 500);
        }
      }
    }
  };

  const handleDelete = () => {
    setPin(pin.slice(0, -1));
    setError(false);
  };

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
        <div className="flex justify-center gap-4 mb-12">
          {[0, 1, 2, 3].map((i) => (
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
            <p className="text-red-400 font-semibold">Falscher PIN!</p>
          </div>
        )}

        {/* Number Pad */}
        <div className="grid grid-cols-3 gap-4 mb-4">
          {[1, 2, 3, 4, 5, 6, 7, 8, 9].map((num) => (
            <button
              key={num}
              onClick={() => handleNumberClick(num)}
              className="aspect-square bg-gradient-to-br from-slate-800 to-slate-900 border-2 border-slate-700 rounded-xl text-white text-2xl font-bold hover:border-purple-500 hover:shadow-lg hover:shadow-purple-500/50 active:scale-95 transition-all"
            >
              {num}
            </button>
          ))}
        </div>

        <div className="grid grid-cols-3 gap-4">
          <div />
          <button
            onClick={() => handleNumberClick(0)}
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
      </div>
    </div>
  );
}
