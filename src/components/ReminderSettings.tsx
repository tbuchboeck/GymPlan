import { useState, useEffect } from 'react';
import { ArrowLeft, Bell, BellOff } from 'lucide-react';

interface ReminderSettingsProps {
  onClose: () => void;
}

interface ReminderConfig {
  enabled: boolean;
  days: number[]; // 0 = Sunday, 1 = Monday, etc.
  time: string; // HH:MM format
}

const DAYS = ['Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag'];

export function ReminderSettings({ onClose }: ReminderSettingsProps) {
  const [config, setConfig] = useState<ReminderConfig>({
    enabled: false,
    days: [1, 4], // Monday and Thursday by default
    time: '18:00'
  });

  const [notificationSupported, setNotificationSupported] = useState(false);
  const [notificationPermission, setNotificationPermission] = useState<NotificationPermission>('default');

  useEffect(() => {
    // Check if notifications are supported
    if ('Notification' in window) {
      setNotificationSupported(true);
      setNotificationPermission(Notification.permission);
    }

    // Load saved config
    const saved = localStorage.getItem('reminderConfig');
    if (saved) {
      setConfig(JSON.parse(saved));
    }
  }, []);

  const requestPermission = async () => {
    if ('Notification' in window) {
      const permission = await Notification.requestPermission();
      setNotificationPermission(permission);
      if (permission === 'granted') {
        setConfig({ ...config, enabled: true });
      }
    }
  };

  const toggleDay = (day: number) => {
    const newDays = config.days.includes(day)
      ? config.days.filter(d => d !== day)
      : [...config.days, day].sort();

    const newConfig = { ...config, days: newDays };
    setConfig(newConfig);
    localStorage.setItem('reminderConfig', JSON.stringify(newConfig));
  };

  const updateTime = (time: string) => {
    const newConfig = { ...config, time };
    setConfig(newConfig);
    localStorage.setItem('reminderConfig', JSON.stringify(newConfig));
  };

  const toggleEnabled = async () => {
    if (!config.enabled && notificationPermission !== 'granted') {
      await requestPermission();
    } else {
      const newConfig = { ...config, enabled: !config.enabled };
      setConfig(newConfig);
      localStorage.setItem('reminderConfig', JSON.stringify(newConfig));
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-indigo-900">
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 shadow-2xl">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <button
            onClick={onClose}
            className="flex items-center gap-2 text-white hover:text-indigo-100 mb-4 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Zurück</span>
          </button>
          <h1 className="text-3xl font-bold text-white">Erinnerungen</h1>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-8">
        {!notificationSupported ? (
          <div className="bg-yellow-50 border-l-4 border-yellow-400 p-6 rounded-xl">
            <p className="text-yellow-800">
              Dein Browser unterstützt keine Push-Benachrichtigungen.
            </p>
          </div>
        ) : (
          <>
            {/* Enable/Disable Toggle */}
            <div className="bg-gradient-to-br from-indigo-600 to-purple-600 rounded-2xl shadow-2xl p-6 mb-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  {config.enabled ? (
                    <Bell className="w-8 h-8 text-white" />
                  ) : (
                    <BellOff className="w-8 h-8 text-indigo-200" />
                  )}
                  <div>
                    <h2 className="text-xl font-bold text-white">
                      Erinnerungen {config.enabled ? 'aktiv' : 'inaktiv'}
                    </h2>
                    <p className="text-indigo-100 text-sm">
                      {config.enabled
                        ? 'Du erhältst Benachrichtigungen'
                        : 'Aktiviere Erinnerungen für dein Training'}
                    </p>
                  </div>
                </div>
                <button
                  onClick={toggleEnabled}
                  className={`relative w-16 h-8 rounded-full transition-colors ${
                    config.enabled ? 'bg-white/30' : 'bg-white/10'
                  }`}
                >
                  <div
                    className={`absolute top-1 left-1 w-6 h-6 bg-white rounded-full transition-transform shadow-lg ${
                      config.enabled ? 'translate-x-8' : ''
                    }`}
                  />
                </button>
              </div>
            </div>

            {config.enabled && (
              <>
                {/* Time Selection */}
                <div className="bg-gradient-to-br from-blue-600 to-cyan-600 rounded-2xl shadow-2xl p-6 mb-6">
                  <h3 className="font-bold text-white mb-4">Uhrzeit</h3>
                  <input
                    type="time"
                    value={config.time}
                    onChange={(e) => updateTime(e.target.value)}
                    className="w-full p-4 text-2xl font-mono border-2 border-cyan-400 bg-white/90 rounded-xl focus:border-white focus:outline-none focus:ring-2 focus:ring-white"
                  />
                  <p className="text-blue-100 text-sm mt-2">
                    Du wirst um {config.time} Uhr erinnert
                  </p>
                </div>

                {/* Day Selection */}
                <div className="bg-gradient-to-br from-slate-700 to-slate-800 rounded-2xl shadow-2xl p-6 border border-slate-600">
                  <h3 className="font-bold text-white mb-4">Wochentage</h3>
                  <div className="grid grid-cols-7 gap-2">
                    {DAYS.map((day, index) => (
                      <button
                        key={index}
                        onClick={() => toggleDay(index)}
                        className={`p-3 rounded-lg font-semibold transition-all ${
                          config.days.includes(index)
                            ? 'bg-gradient-to-br from-indigo-600 to-purple-600 text-white shadow-lg'
                            : 'bg-slate-600 text-slate-300 hover:bg-slate-500'
                        }`}
                      >
                        <div className="text-xs mb-1">{day.substring(0, 2)}</div>
                      </button>
                    ))}
                  </div>
                  <p className="text-slate-300 text-sm mt-4">
                    {config.days.length === 0
                      ? 'Wähle mindestens einen Tag aus'
                      : `Erinnerungen an ${config.days.length} ${
                          config.days.length === 1 ? 'Tag' : 'Tagen'
                        } pro Woche`}
                  </p>
                </div>

                {/* Info */}
                <div className="bg-blue-50 border-l-4 border-blue-500 p-6 rounded-xl mt-6">
                  <h4 className="font-semibold text-blue-900 mb-2">Tipp</h4>
                  <p className="text-blue-800 text-sm">
                    Dein Trainingsplan empfiehlt 2 Einheiten pro Woche. Wähle zwei Tage aus, die
                    gut in deinen Zeitplan passen!
                  </p>
                </div>
              </>
            )}

            {notificationPermission === 'denied' && (
              <div className="bg-red-50 border-l-4 border-red-400 p-6 rounded-xl mt-6">
                <p className="text-red-800">
                  Benachrichtigungen wurden blockiert. Bitte aktiviere sie in deinen
                  Browser-Einstellungen.
                </p>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
