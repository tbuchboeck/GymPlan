import { supabase } from './supabase';
import type { Feeling, WorkoutSession } from '../types';
import { authService } from './auth-service';

// Die Supabase-Tabelle hat keine Spalten für Befinden, Kribbeln und abgebrochene
// Übungen. Ohne DB-Änderung werden sie kompakt als JSON mit Präfix in `notes`
// abgelegt. Alte, freie notes-Texte (ohne Präfix) bleiben gültig.
const NOTES_PREFIX = 'gp:';

interface PackedNotes {
  f?: Feeling;
  t?: boolean;
  a?: string[];
  n?: string;
}

type SessionExtras = Pick<WorkoutSession, 'notes' | 'feeling' | 'tingling' | 'abortedExercises'>;

const FEELINGS: readonly Feeling[] = ['better', 'same', 'worse'];

export function encodeNotes(session: WorkoutSession): string | null {
  const packed: PackedNotes = {};
  if (session.feeling) packed.f = session.feeling;
  if (typeof session.tingling === 'boolean') packed.t = session.tingling;
  if (session.abortedExercises && session.abortedExercises.length > 0) packed.a = session.abortedExercises;
  if (session.notes) packed.n = session.notes;

  const hasExtras = packed.f !== undefined || packed.t !== undefined || packed.a !== undefined;
  if (!hasExtras) {
    // Nur freier Text: unverändert speichern, außer er sieht zufällig wie unser Format aus
    if (!session.notes) return null;
    if (!session.notes.startsWith(NOTES_PREFIX)) return session.notes;
  }
  return NOTES_PREFIX + JSON.stringify(packed);
}

export function decodeNotes(raw: string | null | undefined): SessionExtras {
  if (!raw) return {};
  if (!raw.startsWith(NOTES_PREFIX)) return { notes: raw };
  try {
    const parsed: unknown = JSON.parse(raw.slice(NOTES_PREFIX.length));
    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) return { notes: raw };
    const p = parsed as Record<string, unknown>;
    const out: SessionExtras = {};
    if (typeof p.n === 'string' && p.n) out.notes = p.n;
    if (typeof p.f === 'string' && (FEELINGS as readonly string[]).includes(p.f)) out.feeling = p.f as Feeling;
    if (typeof p.t === 'boolean') out.tingling = p.t;
    if (Array.isArray(p.a)) {
      const names = p.a.filter((x): x is string => typeof x === 'string');
      if (names.length > 0) out.abortedExercises = names;
    }
    return out;
  } catch {
    // Kein gültiges JSON – als freien Text behandeln
    return { notes: raw };
  }
}

function toRow(session: WorkoutSession, userId: string) {
  return {
    id: session.id,
    user_id: userId,
    date: session.date,
    plan_name: session.planName,
    completed_exercises: session.completedExercises,
    total_exercises: session.totalExercises,
    duration: session.duration,
    notes: encodeNotes(session),
  };
}

/**
 * Lokale und entfernte Sessions zusammenführen (nach ID dedupliziert).
 * Remote gewinnt bei gleicher ID, außer die lokale Session hat Befindens-Daten,
 * die remote (noch) fehlen – dann bleibt die lokale Fassung erhalten.
 * Reihenfolge: lokale Reihenfolge zuerst, danach rein entfernte Sessions.
 */
export function mergeSessions(local: WorkoutSession[], remote: WorkoutSession[]): WorkoutSession[] {
  const merged = new Map<string, WorkoutSession>();
  for (const s of local) merged.set(s.id, s);
  for (const r of remote) {
    const l = merged.get(r.id);
    if (!l) {
      merged.set(r.id, r);
      continue;
    }
    merged.set(r.id, {
      ...l,
      ...r,
      feeling: r.feeling ?? l.feeling,
      tingling: r.tingling ?? l.tingling,
      abortedExercises: r.abortedExercises ?? l.abortedExercises,
      notes: r.notes ?? l.notes,
    });
  }
  // undefined-Felder entfernen, damit JSON in localStorage sauber bleibt
  return Array.from(merged.values()).map((s) => {
    const clean = { ...s } as Record<string, unknown>;
    for (const k of Object.keys(clean)) if (clean[k] === undefined) delete clean[k];
    return clean as unknown as WorkoutSession;
  });
}

/**
 * Push a single session to Supabase. Fire-and-forget — failures are logged but don't block the app.
 * Uses upsert so re-pushing the same session is idempotent. Tagged with the
 * current authenticated user_id so sessions stay scoped per person (Thomas
 * vs. Neli) even though both use the same Supabase project.
 */
export async function pushSession(session: WorkoutSession): Promise<void> {
  if (!supabase) return;
  const userId = authService.getCurrentUserId();
  if (!userId) return; // no session → skip remote push, localStorage still holds it

  try {
    const { error } = await supabase
      .from('gym_sessions')
      .upsert(toRow(session, userId), { onConflict: 'id' });

    if (error) throw error;
  } catch (err) {
    console.warn('Failed to push session to Supabase:', err);
  }
}

/**
 * Pull all sessions belonging to the current user from Supabase.
 * Returns empty array on failure (offline fallback) or no auth.
 */
export async function pullRemoteSessions(): Promise<WorkoutSession[]> {
  if (!supabase) return [];
  const userId = authService.getCurrentUserId();
  if (!userId) return [];

  try {
    const { data, error } = await supabase
      .from('gym_sessions')
      .select('*')
      .eq('user_id', userId)
      .order('date', { ascending: false });

    if (error) throw error;
    if (!data) return [];

    return data.map((row) => ({
      id: row.id,
      date: row.date,
      planName: row.plan_name,
      completedExercises: row.completed_exercises,
      totalExercises: row.total_exercises,
      duration: row.duration,
      ...decodeNotes(row.notes),
    }));
  } catch (err) {
    console.warn('Failed to pull sessions from Supabase:', err);
    return [];
  }
}

/**
 * Sync all local sessions to Supabase and pull any remote-only sessions
 * for the current user. Returns merged session array (deduped by ID).
 * Achtung: Das Ergebnis basiert auf dem übergebenen Snapshot. Wer es in den
 * State schreibt, sollte stattdessen `pullRemoteSessions`/`mergeSessions`
 * funktional anwenden (siehe `syncAndMerge`), sonst gehen zwischenzeitlich
 * angelegte Sessions verloren.
 */
export async function syncAllSessions(
  localSessions: WorkoutSession[]
): Promise<WorkoutSession[]> {
  const remote = await pushAllAndPull(localSessions);
  return remote === null ? localSessions : mergeSessions(localSessions, remote);
}

/**
 * Lädt alle lokalen Sessions hoch und liefert die entfernten Sessions,
 * oder null, wenn kein Sync möglich war. Für funktionales Mergen:
 *   const remote = await pushAllAndPull(sessions);
 *   if (remote) setSessions(cur => mergeSessions(cur, remote));
 */
export async function pushAllAndPull(
  localSessions: WorkoutSession[]
): Promise<WorkoutSession[] | null> {
  if (!supabase) return null;
  const userId = authService.getCurrentUserId();
  if (!userId) return null;

  try {
    if (localSessions.length > 0) {
      const { error } = await supabase
        .from('gym_sessions')
        .upsert(localSessions.map((s) => toRow(s, userId)), { onConflict: 'id' });

      if (error) throw error;
    }

    return await pullRemoteSessions();
  } catch (err) {
    console.warn('Session sync failed, using local data:', err);
    return null;
  }
}
