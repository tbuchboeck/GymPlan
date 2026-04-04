import { createClient } from '@supabase/supabase-js';

const SESSION_KEY = 'gymplan-pin-verified';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL ?? '';
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY ?? '';

const supabase =
  supabaseUrl && supabaseAnonKey
    ? createClient(supabaseUrl, supabaseAnonKey)
    : null;

// Fallback hash for offline use (SHA-256 of the PIN)
const OFFLINE_PIN_HASH =
  '1ec479bb53d3cb6721d3fef41ccc097b017d0959e178e8f3ffe1c9f309b72b71';

async function hashPin(pin: string): Promise<string> {
  const encoder = new TextEncoder();
  const data = encoder.encode(pin);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map((b) => b.toString(16).padStart(2, '0')).join('');
}

export async function verifyPin(
  pin: string
): Promise<{ success: boolean; error?: string }> {
  const enteredHash = await hashPin(pin);

  // Try Supabase first (server-side hash)
  if (supabase) {
    try {
      const { data, error } = await supabase
        .from('app_config')
        .select('value')
        .eq('key', 'pin_hash')
        .single();

      if (error) throw error;
      if (!data) return { success: false, error: 'Kein PIN konfiguriert' };

      if (enteredHash === data.value) {
        sessionStorage.setItem(SESSION_KEY, 'true');
        return { success: true };
      } else {
        return { success: false, error: 'Falscher PIN' };
      }
    } catch (err) {
      console.warn('Supabase unreachable, falling back to offline check:', err);
    }
  }

  // Offline fallback: check against local hash
  if (enteredHash === OFFLINE_PIN_HASH) {
    sessionStorage.setItem(SESSION_KEY, 'true');
    return { success: true };
  }

  return { success: false, error: 'Falscher PIN' };
}

export function isSessionValid(): boolean {
  return sessionStorage.getItem(SESSION_KEY) === 'true';
}

export function clearSession(): void {
  sessionStorage.removeItem(SESSION_KEY);
}
