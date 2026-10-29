import type { Feeling, WorkoutSession } from '../types';
import type { Person } from '../lib/auth-service';

// Exportformat ab Version 2: Objekt mit Person, damit beim Import erkannt wird,
// ob die Datei von der anderen Person stammt. Alte Exporte (reines Array) werden weiter gelesen.
interface ExportFile {
  app: 'gymplan';
  version: 2;
  person?: Person;
  exportedAt: string;
  sessions: WorkoutSession[];
}

export function exportToJSON(sessions: WorkoutSession[], person?: Person): void {
  const file: ExportFile = {
    app: 'gymplan',
    version: 2,
    ...(person ? { person } : {}),
    exportedAt: new Date().toISOString(),
    sessions,
  };
  const dataStr = JSON.stringify(file, null, 2);
  const dataBlob = new Blob([dataStr], { type: 'application/json' });

  downloadFile(dataBlob, `workout-sessions-${getDateString()}.json`);
}

const FEELINGS: readonly string[] = ['better', 'same', 'worse'];

function newId(): string {
  if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
    return crypto.randomUUID();
  }
  return `${Date.now()}-${Math.random().toString(36).slice(2, 10)}`;
}

/** Aus geparster Datei die Session-Liste und ggf. die Person holen. */
export function unwrapImport(data: unknown): { sessions: unknown[]; person?: string } | null {
  if (Array.isArray(data)) return { sessions: data };
  if (data && typeof data === 'object') {
    const obj = data as Record<string, unknown>;
    if (Array.isArray(obj.sessions)) {
      return {
        sessions: obj.sessions,
        ...(typeof obj.person === 'string' ? { person: obj.person } : {}),
      };
    }
  }
  return null;
}

export function normalizeImportedSession(s: Record<string, unknown>): WorkoutSession {
  const aborted = Array.isArray(s.abortedExercises)
    ? s.abortedExercises.filter((x): x is string => typeof x === 'string')
    : [];
  return {
    id: String(s.id),
    date: String(s.date),
    planName: String(s.planName),
    completedExercises: Number(s.completedExercises),
    totalExercises: Number(s.totalExercises),
    duration: Number(s.duration),
    ...(typeof s.notes === 'string' ? { notes: s.notes } : {}),
    ...(typeof s.feeling === 'string' && FEELINGS.includes(s.feeling) ? { feeling: s.feeling as Feeling } : {}),
    ...(typeof s.tingling === 'boolean' ? { tingling: s.tingling } : {}),
    ...(aborted.length > 0 ? { abortedExercises: aborted } : {}),
  };
}

/**
 * Bereitet importierte Sessions vor: Stammt die Datei von der anderen Person,
 * bekommen alle Sessions neue IDs (sonst würden sie fremde Einträge überschreiben).
 * Danach werden Sessions verworfen, deren ID schon existiert – nie überschreiben.
 */
export function prepareImport(
  sessions: WorkoutSession[],
  options: { filePerson?: string; currentPerson?: Person; existingIds?: Iterable<string> } = {}
): { sessions: WorkoutSession[]; fromOtherPerson: boolean; skipped: number } {
  const { filePerson, currentPerson, existingIds = [] } = options;
  const fromOtherPerson = !!filePerson && !!currentPerson && filePerson !== currentPerson;
  const existing = new Set(existingIds);
  const withIds = fromOtherPerson ? sessions.map((s) => ({ ...s, id: newId() })) : sessions;

  const result: WorkoutSession[] = [];
  for (const s of withIds) {
    if (existing.has(s.id)) continue;
    existing.add(s.id); // auch Duplikate innerhalb der Datei nur einmal
    result.push(s);
  }
  return { sessions: result, fromOtherPerson, skipped: sessions.length - result.length };
}

export function importFromJSON(
  onImport: (sessions: WorkoutSession[]) => void,
  options: { currentPerson?: Person; existingIds?: Iterable<string> } = {}
): void {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = 'application/json,.json';

  input.onchange = async (e: Event) => {
    const target = e.target as HTMLInputElement;
    const file = target.files?.[0];

    if (!file) {
      return;
    }

    try {
      const text = await file.text();
      const unwrapped = unwrapImport(JSON.parse(text));

      // Validierung der importierten Daten
      if (!unwrapped) {
        alert('Ungültiges JSON-Format. Es wird eine Trainings-Exportdatei erwartet.');
        return;
      }

      // Validate structure and types of each session
      const data = unwrapped.sessions;
      const isValid = data.every((entry) => {
        if (!entry || typeof entry !== 'object') return false;
        const session = entry as Record<string, unknown>;
        return (
          typeof session.id === 'string' &&
          typeof session.date === 'string' &&
          !isNaN(Date.parse(session.date as string)) &&
          typeof session.planName === 'string' &&
          typeof session.completedExercises === 'number' &&
          Number.isFinite(session.completedExercises) &&
          typeof session.totalExercises === 'number' &&
          Number.isFinite(session.totalExercises) &&
          typeof session.duration === 'number' &&
          Number.isFinite(session.duration) &&
          session.duration >= 0
        );
      });

      if (!isValid) {
        alert('Ungültiges Datenformat. Bitte überprüfe die JSON-Datei.');
        return;
      }

      const { sessions: importedSessions, fromOtherPerson, skipped } = prepareImport(
        data.map((s) => normalizeImportedSession(s as Record<string, unknown>)),
        { filePerson: unwrapped.person, currentPerson: options.currentPerson, existingIds: options.existingIds }
      );

      if (importedSessions.length === 0) {
        alert('Alle Trainings aus der Datei sind bereits vorhanden. Es wurde nichts importiert.');
        return;
      }

      // Bestätigungsdialog
      const hints: string[] = [];
      if (fromOtherPerson) hints.push('Die Datei stammt von der anderen Person – die Trainings werden als neue Einträge übernommen.');
      if (skipped > 0) hints.push(`${skipped} Training(s) sind bereits vorhanden und werden übersprungen.`);
      const confirmMessage = `Möchtest du ${importedSessions.length} Training(s) importieren?\n\n${hints.length ? hints.join('\n') + '\n\n' : ''}Die Trainings werden zu den bestehenden Daten hinzugefügt.`;

      if (confirm(confirmMessage)) {
        onImport(importedSessions);
        alert(`${importedSessions.length} Training(s) erfolgreich importiert!`);
      }
    } catch (error) {
      console.error('Import-Fehler:', error);
      alert('Fehler beim Importieren der Datei. Bitte überprüfe das JSON-Format.');
    }
  };

  input.click();
}

export function exportToCSV(sessions: WorkoutSession[]): void {
  if (sessions.length === 0) {
    alert('Keine Trainings zum Exportieren vorhanden.');
    return;
  }

  // CSV-Header
  const headers = ['Datum', 'Trainingsplan', 'Abgeschlossene Übungen', 'Gesamt Übungen', 'Dauer (min)', 'Notizen'];

  // CSV-Zeilen
  const rows = sessions.map(session => [
    new Date(session.date).toLocaleString('de-DE'),
    session.planName,
    session.completedExercises.toString(),
    session.totalExercises.toString(),
    session.duration.toString(),
    session.notes || '',
  ]);

  // CSV-String zusammenbauen
  const csvContent = [
    headers.join(','),
    ...rows.map(row =>
      row.map(cell => `"${cell.replace(/"/g, '""')}"`).join(',')
    ),
  ].join('\n');

  const dataBlob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  downloadFile(dataBlob, `workout-sessions-${getDateString()}.csv`);
}

export function downloadTextFile(text: string, filename: string): void {
  downloadFile(new Blob([text], { type: 'text/plain;charset=utf-8' }), filename);
}

function downloadFile(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

export function getDateString(): string {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}
