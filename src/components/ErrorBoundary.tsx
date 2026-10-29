import { Component, type ErrorInfo, type ReactNode } from 'react';
import { RefreshCw, TriangleAlert } from 'lucide-react';

// Verhindert eine Neulade-Schleife, falls der Chunk auch nach dem Neuladen fehlt
const RELOAD_FLAG = 'gym.chunkReloaded';

function isChunkLoadError(error: unknown): boolean {
  const e = error as { name?: string; message?: string } | null;
  const text = `${e?.name ?? ''} ${e?.message ?? ''}`;
  return /Failed to fetch dynamically imported module|Importing a module script failed|error loading dynamically imported module|ChunkLoadError/i.test(text);
}

interface Props {
  children: ReactNode;
}

interface State {
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { error: null };

  static getDerivedStateFromError(error: Error): State {
    return { error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error('[app] Fehler', error, info.componentStack);

    // Nach einem Deploy fehlen alte Chunks → einmal automatisch neu laden
    if (isChunkLoadError(error)) {
      let alreadyReloaded = false;
      try {
        alreadyReloaded = sessionStorage.getItem(RELOAD_FLAG) === '1';
        if (!alreadyReloaded) sessionStorage.setItem(RELOAD_FLAG, '1');
      } catch {
        alreadyReloaded = true; // ohne sessionStorage lieber nicht automatisch neu laden
      }
      if (!alreadyReloaded) window.location.reload();
    }
  }

  componentDidMount() {
    // App läuft wieder → Flag nach kurzer Zeit freigeben
    window.setTimeout(() => {
      try {
        if (!this.state.error) sessionStorage.removeItem(RELOAD_FLAG);
      } catch {
        // ignorieren
      }
    }, 10_000);
  }

  private reload = () => {
    try {
      sessionStorage.removeItem(RELOAD_FLAG);
    } catch {
      // ignorieren
    }
    window.location.reload();
  };

  render() {
    if (!this.state.error) return this.props.children;

    return (
      <div className="min-h-dvh bg-slate-900 flex items-center justify-center p-6">
        <div className="w-full max-w-sm bg-slate-800 border border-slate-700/50 rounded-2xl p-6 text-center">
          <div className="mx-auto mb-4 w-14 h-14 rounded-full bg-amber-500/15 flex items-center justify-center">
            <TriangleAlert className="w-7 h-7 text-amber-400" />
          </div>
          <h1 className="text-xl font-semibold text-white mb-2">Etwas ist schiefgelaufen</h1>
          <p className="text-sm text-slate-400 mb-5">
            Deine Trainings sind gespeichert. Bitte lade die App neu.
          </p>
          <button
            type="button"
            onClick={this.reload}
            className="w-full bg-indigo-500 hover:bg-indigo-400 text-white py-3 rounded-xl font-semibold flex items-center justify-center gap-2 transition-colors"
          >
            <RefreshCw className="w-5 h-5" />
            Neu laden
          </button>
        </div>
      </div>
    );
  }
}
