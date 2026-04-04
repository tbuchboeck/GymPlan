import { supabase } from './supabase';
import type { WorkoutSession } from '../types';

/**
 * Push a single session to Supabase. Fire-and-forget — failures are logged but don't block the app.
 * Uses upsert so re-pushing the same session is idempotent.
 */
export async function pushSession(session: WorkoutSession): Promise<void> {
  if (!supabase) return;

  try {
    const { error } = await supabase
      .from('gym_sessions')
      .upsert({
        id: session.id,
        date: session.date,
        plan_name: session.planName,
        completed_exercises: session.completedExercises,
        total_exercises: session.totalExercises,
        duration: session.duration,
        notes: session.notes ?? null,
      }, { onConflict: 'id' });

    if (error) throw error;
  } catch (err) {
    console.warn('Failed to push session to Supabase:', err);
  }
}

/**
 * Pull all sessions from Supabase and return them as WorkoutSession[].
 * Returns empty array on failure (offline fallback).
 */
export async function pullRemoteSessions(): Promise<WorkoutSession[]> {
  if (!supabase) return [];

  try {
    const { data, error } = await supabase
      .from('gym_sessions')
      .select('*')
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
      notes: row.notes ?? undefined,
    }));
  } catch (err) {
    console.warn('Failed to pull sessions from Supabase:', err);
    return [];
  }
}

/**
 * Sync all local sessions to Supabase and pull any remote-only sessions.
 * Returns merged session array (deduped by ID).
 */
export async function syncAllSessions(
  localSessions: WorkoutSession[]
): Promise<WorkoutSession[]> {
  if (!supabase) return localSessions;

  try {
    // Push all local sessions (upsert = idempotent)
    if (localSessions.length > 0) {
      const { error } = await supabase
        .from('gym_sessions')
        .upsert(
          localSessions.map((s) => ({
            id: s.id,
            date: s.date,
            plan_name: s.planName,
            completed_exercises: s.completedExercises,
            total_exercises: s.totalExercises,
            duration: s.duration,
            notes: s.notes ?? null,
          })),
          { onConflict: 'id' }
        );

      if (error) throw error;
    }

    // Pull everything back (includes any sessions from other devices)
    const remoteSessions = await pullRemoteSessions();

    // Merge: use a Map keyed by ID, remote wins for any conflict
    const merged = new Map<string, WorkoutSession>();
    for (const s of localSessions) merged.set(s.id, s);
    for (const s of remoteSessions) merged.set(s.id, s);

    return Array.from(merged.values());
  } catch (err) {
    console.warn('Session sync failed, using local data:', err);
    return localSessions;
  }
}
