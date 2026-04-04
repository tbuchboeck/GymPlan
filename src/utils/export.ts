import type { WorkoutSession } from '../types';

export function exportToJSON(sessions: WorkoutSession[]): void {
  const dataStr = JSON.stringify(sessions, null, 2);
  const dataBlob = new Blob([dataStr], { type: 'application/json' });

  downloadFile(dataBlob, `workout-sessions-${getDateString()}.json`);
}

export function importFromJSON(onImport: (sessions: WorkoutSession[]) => void): void {
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
      const data = JSON.parse(text);

      // Validierung der importierten Daten
      if (!Array.isArray(data)) {
        alert('Ungültiges JSON-Format. Es wird ein Array von Trainings-Sessions erwartet.');
        return;
      }

      // Validate structure and types of each session
      const isValid = data.every((session: Record<string, unknown>) =>
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

      if (!isValid) {
        alert('Ungültiges Datenformat. Bitte überprüfe die JSON-Datei.');
        return;
      }

      const importedSessions: WorkoutSession[] = data.map((s: Record<string, unknown>) => ({
        id: String(s.id),
        date: String(s.date),
        planName: String(s.planName),
        completedExercises: Number(s.completedExercises),
        totalExercises: Number(s.totalExercises),
        duration: Number(s.duration),
        ...(typeof s.notes === 'string' ? { notes: s.notes } : {}),
      }));

      // Bestätigungsdialog
      const confirmMessage = `Möchtest du ${importedSessions.length} Training(s) importieren?\n\nAchtung: Dies wird zu den bestehenden Daten hinzugefügt.`;

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

function getDateString(): string {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}
