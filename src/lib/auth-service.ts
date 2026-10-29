// auth-service.ts — replaces pin-service for the WebAuthn passkey flow
// served by auth.apps.buchboeck.at. Ported from Coffee Tracker's
// authService.js, with APP_ID='gym' and the same singleton surface
// (isSessionValid / clearSession / loginWithPasskey / consumeRecoveryCode).
//
// Multi-user: GymPlan is shared by Neli and Thomas. The auth-buchboeck
// service keys every user off a `label` (defaulting to 'thomas' server-side
// when omitted). We thread the chosen person's label through the login and
// recovery-code flows so each enrolls and authenticates against their own
// auth_users row and gets their own JWT `sub` — which session-sync then uses
// to keep gym_sessions scoped per person.

const APP_ID = 'gym';
const AUTH_API = 'https://auth.apps.buchboeck.at/api/auth';
// Login bleibt bis zu 7 Tage gültig (auch offline / nach Kaltstart):
// Token + Person + Ablauf liegen in localStorage. Der Ablauf ist das
// Minimum aus JWT-exp und Login-Zeitpunkt + 7 Tage.
const SESSION_KEY = 'gym.auth.session';
const LEGACY_SESSION_KEY = 'gym.auth.session.v1'; // früher in sessionStorage
const MAX_SESSION_MS = 7 * 24 * 60 * 60 * 1000;

export interface StoredSession {
  token: string;
  person: Person;
  expiresAt: number; // ms seit Epoch
}

/** Who is logging in. Must match the `label` of the auth_users row in the
 * shared auth-buchboeck Supabase project. */
export type Person = 'neli' | 'thomas';

interface JwtPayload {
  exp?: number;
  [k: string]: unknown;
}

function decodeJwtPayload(token: string): JwtPayload | null {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) return null;
    const b64 = parts[1].replace(/-/g, '+').replace(/_/g, '/');
    const padded = b64 + '='.repeat((4 - (b64.length % 4)) % 4);
    return JSON.parse(atob(padded)) as JwtPayload;
  } catch {
    return null;
  }
}

function b64urlToBuffer(b64url: string): ArrayBuffer {
  const b64 = b64url.replace(/-/g, '+').replace(/_/g, '/');
  const padded = b64 + '='.repeat((4 - (b64.length % 4)) % 4);
  const bin = atob(padded);
  const arr = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
  return arr.buffer;
}

function bufferToB64url(buf: ArrayBuffer): string {
  const bin = String.fromCharCode(...new Uint8Array(buf));
  return btoa(bin).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function decodeRequestOptions(opts: PublicKeyCredentialRequestOptionsJSON): PublicKeyCredentialRequestOptions {
  return {
    ...opts,
    challenge: b64urlToBuffer(opts.challenge),
    allowCredentials: (opts.allowCredentials || []).map((c) => ({
      ...c,
      id: b64urlToBuffer(c.id),
    })),
  } as PublicKeyCredentialRequestOptions;
}

function decodeCreationOptions(opts: PublicKeyCredentialCreationOptionsJSON): PublicKeyCredentialCreationOptions {
  return {
    ...opts,
    challenge: b64urlToBuffer(opts.challenge),
    user: { ...opts.user, id: b64urlToBuffer(opts.user.id) },
    excludeCredentials: (opts.excludeCredentials || []).map((c) => ({
      ...c,
      id: b64urlToBuffer(c.id),
    })),
  } as PublicKeyCredentialCreationOptions;
}

function encodeAssertionResponse(cred: PublicKeyCredential): EncodedAssertion {
  const r = cred.response as AuthenticatorAssertionResponse;
  return {
    id: cred.id,
    rawId: bufferToB64url(cred.rawId),
    type: cred.type,
    response: {
      authenticatorData: bufferToB64url(r.authenticatorData),
      clientDataJSON: bufferToB64url(r.clientDataJSON),
      signature: bufferToB64url(r.signature),
      userHandle: r.userHandle ? bufferToB64url(r.userHandle) : null,
    },
    clientExtensionResults: (cred.getClientExtensionResults() ?? {}) as Record<string, unknown>,
  };
}

function encodeAttestationResponse(cred: PublicKeyCredential): EncodedAttestation {
  const r = cred.response as AuthenticatorAttestationResponse;
  return {
    id: cred.id,
    rawId: bufferToB64url(cred.rawId),
    type: cred.type,
    response: {
      attestationObject: bufferToB64url(r.attestationObject),
      clientDataJSON: bufferToB64url(r.clientDataJSON),
      transports: typeof r.getTransports === 'function' ? r.getTransports() : undefined,
    },
    clientExtensionResults: (cred.getClientExtensionResults() ?? {}) as Record<string, unknown>,
  };
}

function detectDeviceLabel(): string {
  const ua = navigator.userAgent;
  if (/iPhone|iPad|iPod/.test(ua)) return 'iOS';
  if (/Android/.test(ua)) return 'Android';
  if (/Macintosh/.test(ua)) return 'macOS';
  if (/Windows/.test(ua)) return 'Windows';
  if (/Linux/.test(ua)) return 'Linux';
  return 'Browser';
}

interface ApiError extends Error {
  kind: 'network' | 'http';
  status?: number;
}

async function api<T>(path: string, body: unknown): Promise<T> {
  let r: Response;
  try {
    r = await fetch(`${AUTH_API}/${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
  } catch (netErr) {
    const err = new Error(`network/CORS: ${(netErr as Error).message}`) as ApiError;
    err.kind = 'network';
    throw err;
  }
  const data = (await r.json().catch(() => ({}))) as { error?: string };
  if (!r.ok) {
    const err = new Error(data.error || `HTTP ${r.status}`) as ApiError;
    err.kind = 'http';
    err.status = r.status;
    throw err;
  }
  return data as T;
}

interface PublicKeyCredentialRequestOptionsJSON {
  challenge: string;
  allowCredentials?: Array<{ id: string; type: string; transports?: string[] }>;
  [k: string]: unknown;
}

interface PublicKeyCredentialCreationOptionsJSON {
  challenge: string;
  user: { id: string; name: string; displayName: string };
  excludeCredentials?: Array<{ id: string; type: string; transports?: string[] }>;
  [k: string]: unknown;
}

interface EncodedAssertion {
  id: string;
  rawId: string;
  type: string;
  response: {
    authenticatorData: string;
    clientDataJSON: string;
    signature: string;
    userHandle: string | null;
  };
  clientExtensionResults: Record<string, unknown>;
}

interface EncodedAttestation {
  id: string;
  rawId: string;
  type: string;
  response: {
    attestationObject: string;
    clientDataJSON: string;
    transports?: string[];
  };
  clientExtensionResults: Record<string, unknown>;
}

interface OptionsResponse {
  session_id: string;
  options: PublicKeyCredentialRequestOptionsJSON | PublicKeyCredentialCreationOptionsJSON;
}

interface VerifyResponse {
  session: string;
}

interface RecoveryCodeResponse {
  bootstrap_token: string;
}

function readStoredSession(): StoredSession | null {
  try {
    const raw = localStorage.getItem(SESSION_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as Partial<StoredSession>;
    if (
      typeof parsed.token !== 'string' ||
      (parsed.person !== 'neli' && parsed.person !== 'thomas') ||
      typeof parsed.expiresAt !== 'number'
    ) {
      return null;
    }
    return parsed as StoredSession;
  } catch {
    return null;
  }
}

class AuthService {
  // Fallback, falls localStorage nicht beschreibbar ist (gilt bis zum Neuladen)
  private memorySession: StoredSession | null = null;

  /** Gespeicherte, noch gültige Sitzung – oder null (abgelaufene wird gelöscht). */
  getSession(): StoredSession | null {
    const session = readStoredSession() ?? this.memorySession;
    if (!session) return null;
    if (Date.now() >= session.expiresAt) {
      this.clearSession();
      return null;
    }
    return session;
  }

  isSessionValid(): boolean {
    return this.getSession() !== null;
  }

  /** Returns the authenticated user's UUID (the `sub` claim) or null if no
   * valid session. Used by session-sync to scope gym_sessions per user. */
  getCurrentUserId(): string | null {
    const session = this.getSession();
    if (!session) return null;
    const payload = decodeJwtPayload(session.token);
    if (!payload) return null;
    return typeof payload.sub === 'string' ? payload.sub : null;
  }

  clearSession(): void {
    this.memorySession = null;
    try {
      localStorage.removeItem(SESSION_KEY);
      sessionStorage.removeItem(LEGACY_SESSION_KEY);
    } catch {
      // Speicher nicht verfügbar – nichts zu löschen
    }
  }

  private storeSession(token: string, person: Person): void {
    const payload = decodeJwtPayload(token);
    const maxExpiry = Date.now() + MAX_SESSION_MS;
    const expiresAt = payload?.exp ? Math.min(payload.exp * 1000, maxExpiry) : maxExpiry;
    this.memorySession = { token, person, expiresAt };
    try {
      localStorage.setItem(SESSION_KEY, JSON.stringify(this.memorySession));
      sessionStorage.removeItem(LEGACY_SESSION_KEY);
    } catch {
      // Privater Modus o. Ä.: memorySession gilt bis zum Neuladen
    }
  }

  /** Authenticate `person` with an existing passkey for this app. The label
   * selects which auth_users row (and thus which passkeys) the server offers. */
  async loginWithPasskey(person: Person): Promise<string> {
    const optsResp = await api<OptionsResponse>('login?step=options', { app_id: APP_ID, label: person });
    const cred = (await navigator.credentials.get({
      publicKey: decodeRequestOptions(optsResp.options as PublicKeyCredentialRequestOptionsJSON),
    })) as PublicKeyCredential;
    const verifyResp = await api<VerifyResponse>('login?step=verify', {
      session_id: optsResp.session_id,
      app_id: APP_ID,
      assertion: encodeAssertionResponse(cred),
    });
    this.storeSession(verifyResp.session, person);
    return verifyResp.session;
  }

  /** Redeem a recovery code for `person` and bootstrap-enroll a new passkey on
   * this device. The label must match the user the code was issued for. */
  async consumeRecoveryCode(code: string, person: Person): Promise<string> {
    const { bootstrap_token } = await api<RecoveryCodeResponse>('recovery-code?action=consume', {
      code,
      app_id: APP_ID,
      label: person,
    });
    return this.enrollWithBootstrapToken(bootstrap_token, person);
  }

  // The register flow derives the user from the bootstrap token (server-side),
  // so it needs no label of its own (person only tags the stored session).
  private async enrollWithBootstrapToken(bootstrap_token: string, person: Person): Promise<string> {
    const optsResp = await api<OptionsResponse>('register?step=options', {
      bootstrap_token,
      app_id: APP_ID,
    });
    const cred = (await navigator.credentials.create({
      publicKey: decodeCreationOptions(optsResp.options as PublicKeyCredentialCreationOptionsJSON),
    })) as PublicKeyCredential;
    const verifyResp = await api<VerifyResponse>('register?step=verify', {
      session_id: optsResp.session_id,
      app_id: APP_ID,
      bootstrap_token,
      attestation: encodeAttestationResponse(cred),
      device_label: detectDeviceLabel(),
    });
    this.storeSession(verifyResp.session, person);
    return verifyResp.session;
  }
}

export const authService = new AuthService();
