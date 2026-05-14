// auth-service.ts — replaces pin-service for the WebAuthn passkey flow
// served by auth.apps.buchboeck.at. Ported from Coffee Tracker's
// authService.js, with APP_ID='gym' and the same singleton surface
// (isSessionValid / clearSession / loginWithPasskey / consumeRecoveryCode).

const APP_ID = 'gym';
const AUTH_API = 'https://auth.apps.buchboeck.at/api/auth';
const SESSION_KEY = 'gym.auth.session.v1';

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

class AuthService {
  isSessionValid(): boolean {
    const raw = sessionStorage.getItem(SESSION_KEY);
    if (!raw) return false;
    const payload = decodeJwtPayload(raw);
    if (!payload || !payload.exp) return false;
    return Date.now() / 1000 < payload.exp - 5;
  }

  clearSession(): void {
    sessionStorage.removeItem(SESSION_KEY);
  }

  async loginWithPasskey(): Promise<string> {
    const optsResp = await api<OptionsResponse>('login?step=options', { app_id: APP_ID });
    const cred = (await navigator.credentials.get({
      publicKey: decodeRequestOptions(optsResp.options as PublicKeyCredentialRequestOptionsJSON),
    })) as PublicKeyCredential;
    const verifyResp = await api<VerifyResponse>('login?step=verify', {
      session_id: optsResp.session_id,
      app_id: APP_ID,
      assertion: encodeAssertionResponse(cred),
    });
    sessionStorage.setItem(SESSION_KEY, verifyResp.session);
    return verifyResp.session;
  }

  async consumeRecoveryCode(code: string): Promise<string> {
    const { bootstrap_token } = await api<RecoveryCodeResponse>('recovery-code?action=consume', {
      code,
      app_id: APP_ID,
    });
    return this.enrollWithBootstrapToken(bootstrap_token);
  }

  private async enrollWithBootstrapToken(bootstrap_token: string): Promise<string> {
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
    sessionStorage.setItem(SESSION_KEY, verifyResp.session);
    return verifyResp.session;
  }
}

export const authService = new AuthService();
