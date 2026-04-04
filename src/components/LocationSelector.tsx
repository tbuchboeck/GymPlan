interface LocationSelectorProps {
  onSelectLocation: (location: 'gym' | 'home' | 'home2' | 'back') => void;
}

const locations = [
  {
    key: 'gym' as const,
    label: 'gym',
    description: 'Im Fitnessstudio',
    gradient: 'from-indigo-500 to-purple-600',
  },
  {
    key: 'home' as const,
    label: 'hantel',
    description: 'Hanteltraining',
    gradient: 'from-pink-400 to-rose-500',
  },
  {
    key: 'home2' as const,
    label: 'cardio',
    description: 'Cardio Training',
    gradient: 'from-emerald-500 to-green-400',
  },
  {
    key: 'back' as const,
    label: 'rücken',
    description: 'Rücken-Aufbau & Stabilität',
    gradient: 'from-teal-500 to-cyan-600',
  },
] as const;

function LocationSelector({ onSelectLocation }: LocationSelectorProps) {
  return (
    <div className="flex justify-center items-center min-h-screen bg-gradient-to-br from-indigo-500 to-purple-600 p-5">
      <div className="text-center max-w-[500px] w-full">
        <h1 className="text-white text-4xl sm:text-3xl font-semibold mb-2">
          Was trainierst du heute?
        </h1>
        <p className="text-white/90 text-lg sm:text-base mb-10">
          Wähle deinen Trainingsplan
        </p>

        <div className="flex flex-col gap-5">
          {locations.map(({ key, label, description, gradient }) => (
            <button
              key={key}
              onClick={() => onSelectLocation(key)}
              className="flex items-center gap-5 sm:gap-4 p-6 sm:p-5 bg-white rounded-2xl border-none cursor-pointer transition-all shadow-md hover:-translate-y-1 hover:shadow-lg active:-translate-y-0.5 text-left"
            >
              <div
                className={`text-5xl sm:text-4xl font-bold w-15 h-15 sm:w-[50px] sm:h-[50px] flex items-center justify-center rounded-xl shrink-0 bg-gradient-to-br ${gradient} text-white`}
              >
                @
              </div>
              <div className="flex flex-col gap-1 flex-1">
                <span className="text-2xl sm:text-xl font-semibold text-gray-800">
                  {label}
                </span>
                <span className="text-base sm:text-sm text-gray-500">
                  {description}
                </span>
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export default LocationSelector;
