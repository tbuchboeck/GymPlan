import { supabase } from './supabase';
import type { WorkoutSession } from '../types';
import { authService } from './auth-service';

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
      .upsert({
        id: session.id,
        user_id: userId,
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
      notes: row.notes ?? undefined,
    }));
  } catch (err) {
    console.warn('Failed to pull sessions from Supabase:', err);
    return [];
  }
}

/**
 * Sync all local sessions to Supabase and pull any remote-only sessions
 * for the current user. Returns merged session array (deduped by ID).
 */
export async function syncAllSessions(
  localSessions: WorkoutSession[]
): Promise<WorkoutSession[]> {
  if (!supabase) return localSessions;
  const userId = authService.getCurrentUserId();
  if (!userId) return localSessions;

  try {
    if (localSessions.length > 0) {
      const { error } = await supabase
        .from('gym_sessions')
        .upsert(
          localSessions.map((s) => ({
            id: s.id,
            user_id: userId,
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

    const remoteSessions = await pullRemoteSessions();

    const merged = new Map<string, WorkoutSession>();
    for (const s of localSessions) merged.set(s.id, s);
    for (const s of remoteSessions) merged.set(s.id, s);

    return Array.from(merged.values());
  } catch (err) {
    console.warn('Session sync failed, using local data:', err);
    return localSessions;
  }
}
