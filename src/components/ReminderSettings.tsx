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
    <div className="min-h-dvh bg-slate-900">
      {/* Header */}
      <div className="bg-slate-800 border-b border-slate-700/50 px-4 py-4">
        <div className="flex items-center gap-3">
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <h1 className="text-lg font-semibold text-white">Erinnerungen</h1>
        </div>
      </div>

      {!notificationSupported ? (
        <div className="bg-amber-500/10 border border-amber-500/20 rounded-xl mx-4 mt-4 p-4">
          <p className="text-amber-300 text-sm">
            Dein Browser unterstützt keine Push-Benachrichtigungen.
          </p>
        </div>
      ) : (
        <>
          {/* Enable/Disable Toggle */}
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-2xl mx-4 mt-4 p-5">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                {config.enabled ? (
                  <Bell className="w-6 h-6 text-indigo-400" />
                ) : (
                  <BellOff className="w-6 h-6 text-slate-500" />
                )}
                <div>
                  <h2 className="text-base font-semibold text-white">
                    Erinnerungen {config.enabled ? 'aktiv' : 'inaktiv'}
                  </h2>
                  <p className="text-sm text-slate-400">
                    {config.enabled
                      ? 'Du erhältst Benachrichtigungen'
                      : 'Aktiviere Erinnerungen für dein Training'}
                  </p>
                </div>
              </div>
              <button
                onClick={toggleEnabled}
                className={`relative w-12 h-6 rounded-full transition-colors ${
                  config.enabled ? 'bg-indigo-500' : 'bg-slate-600'
                }`}
              >
                <div
                  className={`absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full transition-transform ${
                    config.enabled ? 'translate-x-6' : ''
                  }`}
                />
              </button>
            </div>
          </div>

          {config.enabled && (
            <>
              {/* Time Selection */}
              <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl mx-4 mt-3 p-4">
                <label className="text-sm font-medium text-slate-400">Uhrzeit</label>
                <input
                  type="time"
                  value={config.time}
                  onChange={(e) => updateTime(e.target.value)}
                  className="bg-slate-700 border border-slate-600 text-white rounded-lg p-3 w-full mt-2 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                />
                <p className="text-slate-500 text-xs mt-2">
                  Du wirst um {config.time} Uhr erinnert
                </p>
              </div>

              {/* Day Selection */}
              <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl mx-4 mt-3 p-4">
                <h3 className="text-sm font-medium text-slate-400 mb-3">Wochentage</h3>
                <div className="grid grid-cols-7 gap-1.5">
                  {DAYS.map((day, index) => (
                    <button
                      key={index}
                      onClick={() => toggleDay(index)}
                      className={`p-2 rounded-lg text-xs font-medium transition-colors ${
                        config.days.includes(index)
                          ? 'bg-indigo-500 text-white'
                          : 'bg-slate-700 text-slate-400 hover:bg-slate-600'
                      }`}
                    >
                      {day.substring(0, 2)}
                    </button>
                  ))}
                </div>
                <p className="text-slate-500 text-xs mt-3">
                  {config.days.length === 0
                    ? 'Wähle mindestens einen Tag aus'
                    : `Erinnerungen an ${config.days.length} ${
                        config.days.length === 1 ? 'Tag' : 'Tagen'
                      } pro Woche`}
                </p>
              </div>

              {/* Info */}
              <div className="bg-indigo-500/10 border border-indigo-500/20 rounded-xl mx-4 mt-3 p-4">
                <h4 className="font-semibold text-indigo-300 text-sm mb-1">Tipp</h4>
                <p className="text-indigo-300/80 text-sm">
                  Dein Trainingsplan empfiehlt 2 Einheiten pro Woche. Wähle zwei Tage aus, die
                  gut in deinen Zeitplan passen!
                </p>
              </div>
            </>
          )}

          {notificationPermission === 'denied' && (
            <div className="bg-red-500/10 border border-red-500/20 rounded-xl mx-4 mt-3 p-4">
              <p className="text-red-300 text-sm">
                Benachrichtigungen wurden blockiert. Bitte aktiviere sie in deinen
                Browser-Einstellungen.
              </p>
            </div>
          )}
        </>
      )}
    </div>
  );
}
