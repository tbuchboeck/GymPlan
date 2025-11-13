import type { WorkoutSession } from '../types';

export function exportToJSON(sessions: WorkoutSession[]): void {
  const dataStr = JSON.stringify(sessions, null, 2);
  const dataBlob = new Blob([dataStr], { type: 'application/json' });

  downloadFile(dataBlob, `workout-sessions-${getDateString()}.json`);
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
