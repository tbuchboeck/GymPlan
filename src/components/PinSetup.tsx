import { useState } from 'react';
import { Lock, Check } from 'lucide-react';

interface PinSetupProps {
  onComplete: () => void;
}

export function PinSetup({ onComplete }: PinSetupProps) {
  const [step, setStep] = useState<'first' | 'confirm'>('first');
  const [firstPin, setFirstPin] = useState('');
  const [confirmPin, setConfirmPin] = useState('');
  const [error, setError] = useState(false);

  const currentPin = step === 'first' ? firstPin : confirmPin;
  const setCurrentPin = step === 'first' ? setFirstPin : setConfirmPin;

  const handleNumberClick = (num: number) => {
    if (currentPin.length < 4) {
      const newPin = currentPin + num;
      setCurrentPin(newPin);

      if (newPin.length === 4) {
        if (step === 'first') {
          // Move to confirmation step
          setTimeout(() => setStep('confirm'), 300);
        } else {
          // Check if PINs match
          if (newPin === firstPin) {
            localStorage.setItem('gymplan-pin', newPin);
            setTimeout(() => onComplete(), 300);
          } else {
            setError(true);
            setTimeout(() => {
              setConfirmPin('');
              setFirstPin('');
              setStep('first');
              setError(false);
            }, 500);
          }
        }
      }
    }
  };

  const handleDelete = () => {
    setCurrentPin(currentPin.slice(0, -1));
    setError(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-indigo-900 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-full mb-4">
            {step === 'confirm' ? (
              <Check className="w-10 h-10 text-white" />
            ) : (
              <Lock className="w-10 h-10 text-white" />
            )}
          </div>
          <h1 className="text-3xl font-bold text-white mb-2">PIN erstellen</h1>
          <p className="text-slate-300">
            {step === 'first' ? 'Wähle einen 4-stelligen PIN' : 'PIN bestätigen'}
          </p>
        </div>

        {/* PIN Dots */}
        <div className="flex justify-center gap-4 mb-12">
          {[0, 1, 2, 3].map((i) => (
            <div
              key={i}
              className={`w-4 h-4 rounded-full transition-all duration-200 ${
                i < currentPin.length
                  ? error
                    ? 'bg-red-500 scale-110'
                    : step === 'confirm'
                    ? 'bg-gradient-to-r from-green-400 to-emerald-500'
                    : 'bg-gradient-to-r from-cyan-400 to-blue-500'
                  : 'bg-slate-700'
              }`}
            />
          ))}
        </div>

        {error && (
          <div className="text-center mb-6">
            <p className="text-red-400 font-semibold">PINs stimmen nicht überein!</p>
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
