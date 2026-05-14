# GymPlan — Documentation

## Overview

GymPlan is a Progressive Web App (PWA) for guided workout tracking. It provides exercise-by-exercise navigation with rest timers, set tracking, 54 animated exercise illustrations, session history with charts, and push notification reminders. Built for personal use by user "Neli" with trainer Martin Schiendorfer's workout plans.

**Status:** Active, 163 commits across 65+ PRs. All development via Claude Code on feature branches with PRs to main.

**Key facts:**
- 4 workout plans: Gym (12 exercises), Dumbbell/Hantel (12), Cardio (15), Back Rehab (6)
- 54 animated SVG exercise illustrations (all exercises covered)
- PIN-locked with Supabase server-side verification + offline fallback
- Workout sessions sync to Supabase `gym_sessions` table (offline-first)
- All session data also in localStorage (primary, offline-capable)
- Installable PWA with full icon set + `manifest.json` (flat indigo `#4f46e5` canvas, dumbbell motif)
- Deployed on Vercel (static Vite build)

## Architecture

```
┌──────────────────────────────────────────────────┐
│  PinLogin (Supabase PIN verify → sessionStorage) │
├──────────────────────────────────────────────────┤
│  LocationSelector (choose workout plan)          │
├──────────────────────────────────────────────────┤
│  App (view router: home/workout/summary/history) │
│  ├── Home (plan info, stats, exercise list)      │
│  │   └── "Wechseln" → back to LocationSelector  │
│  ├── WorkoutView → ExerciseCard + RestTimer      │
│  ├── WorkoutSummary (post-workout stats)         │
│  ├── WorkoutHistory (charts, export) [lazy]      │
│  └── ReminderSettings (push notifications)       │
├──────────────────────────────────────────────────┤
│  localStorage (sessions, primary)                │
│  Supabase (gym_sessions table, sync layer)       │
│  Supabase (app_config table, PIN hash)           │
│  sessionStorage (PIN session)                    │
└──────────────────────────────────────────────────┘
```

**Tech stack:**
- React 19 + TypeScript 5.9
- Vite 7 + vite-plugin-pwa (Workbox)
- Tailwind CSS 4
- Recharts 3 (lazy-loaded)
- Lucide React (icons)
- @supabase/supabase-js (PIN auth + session sync)

**Data flow:**
1. PIN entered → hashed SHA-256 → compared against Supabase `app_config.pin_hash` (offline fallback to local hash)
2. On unlock → `syncAllSessions()` merges localStorage + Supabase sessions
3. User selects plan → exercises render with animated SVG illustrations
4. Workout sessions saved to localStorage + pushed to Supabase (fire-and-forget)
5. Export: JSON (raw) or CSV (formatted with German locale)
6. Import: JSON with type validation + deduplication by session ID + push to Supabase

## File Inventory

| File | Purpose | Status |
|------|---------|--------|
| `src/App.tsx` | Root component, view router, session state, Supabase sync | Active |
| `src/main.tsx` | React entry point (StrictMode) | Active |
| `src/types.ts` | TypeScript interfaces: Exercise, WorkoutPlan, WorkoutSession | Active |
| `src/index.css` | Tailwind import + custom animations (pulse, bounce, fade, shake, slide-up, timer-ring) | Active |
| `src/lib/supabase.ts` | Shared Supabase client (used by pin-service + session-sync) | Active |
| `src/lib/pin-service.ts` | Supabase PIN verification with offline SHA-256 fallback, sessionStorage | Active |
| `src/lib/session-sync.ts` | Offline-first session sync: pushSession, pullRemoteSessions, syncAllSessions | Active |
| `src/components/PinLogin.tsx` | PIN entry screen with numpad, Supabase verification, keyboard support | Active |
| `src/components/LocationSelector.tsx` | Workout plan selector (4 options), Tailwind-styled | Active |
| `src/components/Home.tsx` | Dashboard: plan info, plan switcher, weekly stats, last workout, exercise list | Active |
| `src/components/WorkoutView.tsx` | Fixed-viewport exercise navigation, progress bar, rest timer overlay, bottom nav | Active |
| `src/components/ExerciseCard.tsx` | Compact exercise display: image, instructions, horizontal set dots, action button | Active |
| `src/components/RestTimer.tsx` | SVG circular progress ring, overlay on ExerciseCard | Active |
| `src/components/WorkoutSummary.tsx` | Post-workout celebration with clean stats | Active |
| `src/components/WorkoutHistory.tsx` | Statistics dashboard with Recharts (lazy-loaded) | Active |
| `src/components/ReminderSettings.tsx` | Push notification scheduling (day/time picker), dark theme | Active |
| `src/hooks/useLocalStorage.ts` | Generic localStorage hook with JSON serialization | Active |
| `src/data/workoutPlan.ts` | 4 workout plan definitions with exercise data (45 exercises, all with imageUrl) | Active |
| `src/utils/statistics.ts` | Extended stats: streaks, weekday analysis, weekly charts | Active |
| `src/utils/export.ts` | JSON/CSV export + JSON import with type validation | Active |
| `public/exercise-images/*.svg` | 54 animated SVG exercise illustrations (articulated line-segment style) | Active |
| `public/icon.svg` | App icon — flat-fill dumbbell on indigo `#4f46e5` (no gradients; ImageMagick raster-safe) | Active |
| `public/icon-{192,512,maskable-512}.png` | Android home-screen + Android adaptive (maskable) icons | Active |
| `public/apple-touch-icon.png` | 180×180 iOS home-screen icon | Active |
| `public/favicon.ico` | Multi-size favicon (16/32/48) | Active |
| `public/manifest.json` | PWA manifest — `background_color: #4f46e5` so install paints no white frame | Active |
| `index.html` | HTML shell with PWA meta tags + icon/manifest links | Active |
| `vite.config.ts` | Vite config + PWA plugin (Workbox precaching) | Active |
| `vercel.json` | Vercel deployment: SPA rewrite + security headers | Active |
| `tsconfig.app.json` | TypeScript config (ES2023, strict, React JSX) | Active |
| `eslint.config.js` | ESLint flat config with React hooks + refresh plugins | Active |
| `tailwind.config.js` | Tailwind content paths | Active |
| `postcss.config.js` | PostCSS with Tailwind + autoprefixer | Active |
| `.env.example` | Template for Supabase credentials | Active |
| `.vercelignore` | Excludes node_modules, .git, dist from deploy | Active |

## Usage

### Prerequisites

- Node.js 20+ (24 LTS recommended)
- npm 10+
- Supabase project with `app_config` and `gym_sessions` tables (shared with CoffeeTracker/EcoFlowMon)

### Environment Setup

```bash
# Copy env template and fill in Supabase credentials
cp .env.example .env.local
# Edit .env.local with:
#   VITE_SUPABASE_URL=https://your-project.supabase.co
#   VITE_SUPABASE_ANON_KEY=your-anon-key
```

### Running Scripts

```bash
# Install dependencies
npm install

# Development server (http://localhost:5173)
npm run dev

# Type-check + production build
npm run build

# Preview production build locally
npm run preview

# Lint
npm run lint
```

### Supabase Table Setup

The app uses the shared Supabase project (`wyiafjbpxbhaflhqvwcu`). Two tables are needed:

```sql
-- PIN authentication (shared with CoffeeTracker/EcoFlowMon)
CREATE TABLE app_config (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
);
INSERT INTO app_config (key, value) VALUES ('pin_hash', '<sha256-hash>');

-- Workout session sync (GymPlan-specific)
CREATE TABLE gym_sessions (
  id TEXT PRIMARY KEY,
  date TIMESTAMPTZ NOT NULL,
  plan_name TEXT NOT NULL,
  completed_exercises INT NOT NULL,
  total_exercises INT NOT NULL,
  duration INT NOT NULL,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- RLS policies for both tables
ALTER TABLE app_config ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow anon read" ON app_config FOR SELECT USING (true);

ALTER TABLE gym_sessions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow anon read" ON gym_sessions FOR SELECT USING (true);
CREATE POLICY "Allow anon insert" ON gym_sessions FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow anon update" ON gym_sessions FOR UPDATE USING (true);
```

### Vercel Deployment

```bash
# Required env vars on Vercel:
#   VITE_SUPABASE_URL
#   VITE_SUPABASE_ANON_KEY
vercel --prod
```

## Technical Patterns

- **Offline-first Supabase sync**: `session-sync.ts` pushes sessions via fire-and-forget `upsert` (idempotent by ID). On app load, `syncAllSessions()` pushes all local, pulls all remote, merges by ID with Map. Network failures fall back silently to localStorage.

- **Supabase PIN with offline fallback**: `pin-service.ts` tries Supabase `app_config` table first, catches errors, falls back to hardcoded SHA-256 hash. Session persists in `sessionStorage`.

- **Shared Supabase client**: `supabase.ts` exports a single client instance used by both `pin-service.ts` and `session-sync.ts`. Returns `null` when env vars missing (offline mode).

- **Lazy-loaded Recharts**: `React.lazy(() => import('./components/WorkoutHistory'))` in `App.tsx` — reduced initial bundle from 600KB to 240KB.

- **useRef for timer callbacks**: `RestTimer.tsx` stores `onComplete` in `useRef` to avoid re-running the timer interval when parent re-renders.

- **Non-mutating array operations**: All sorting uses `.toSorted()` (ES2023) instead of `.sort()` to avoid mutating React props/state.

- **Fixed-viewport workout layout**: `WorkoutView` uses `h-dvh flex flex-col` with a scrollable content area and fixed header/footer — prevents page scrolling during exercises.

- **Rest timer as overlay**: `RestTimer` renders as an `absolute inset-0` overlay with `backdrop-blur-sm` on top of `ExerciseCard` instead of replacing it — eliminates layout jumps.

- **Typed JSON import validation**: `export.ts` validates imported JSON field-by-field with `typeof` checks, `Date.parse()` for dates, `Number.isFinite()` for numbers. Constructs clean objects instead of `as` casts.

- **SHA-256 via Web Crypto API**: PIN hashing uses `crypto.subtle.digest('SHA-256', ...)` — native browser API, no dependencies.

- **PWA with Workbox precaching**: `vite-plugin-pwa` generates a service worker that precaches all static assets with content hashes. 63 precached entries including all 54 SVGs.

- **View-based routing without a router**: App uses `useState<AppView>` to switch views + `useEffect` scroll-to-top. No React Router — keeps bundle small.

- **Plan switcher**: Home screen has "Wechseln" button that resets `location` state to `null`, showing the `LocationSelector` without app restart.

- **Security headers via vercel.json**: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `X-XSS-Protection: 1; mode=block`.

## Lessons Learned

- **Never push to merged branches**: PRs #63 and #64 were merged before late commits were pushed — commits were silently lost. Always check `gh pr view --json state` before pushing.
- **Hardcoded PIN in source code is easily discovered**: SHA-256 hashing was the immediate fix; Supabase server-side verification is the proper solution.
- **`sessions.sort()` silently mutates props**: `.toSorted()` is the clean ES2023 fix.
- **Duplicate service workers cause confusing caching**: Use only vite-plugin-pwa's generated SW, not manual `public/sw.js`.
- **Code splitting Recharts has massive impact**: Single `React.lazy()` reduced initial bundle by 60%.
- **Supabase MCP auth via WSL2**: OAuth callback to `localhost` can be flaky on WSL2 — long URLs get mangled during copy-paste. Direct SQL in the Supabase dashboard is the reliable fallback.

## Timeline

| Date | Milestone |
|------|-----------|
| 2025-10-24 | Initial PWA created with gym workout plan |
| 2025-10 | Vercel deployment, Tailwind v4 migration, animated SVG exercises |
| 2025-11 | Location selector, home/cardio workout plans, exercise instructions |
| 2025-12 | Cardio plan, step-up exercise, theraband exercises |
| 2026-01 | Statistics dashboard with Recharts, export/import, PIN login |
| 2026-02 | Back rehab workout plan (post-injury), SVG redesigns |
| 2026-03 | Exercise renaming, plan adjustments, core exercises added |
| 2026-04-04 | Major refactoring session: security hardening (Supabase PIN auth), full design overhaul (flat dark theme, fixed viewport, glass nav), code quality fixes (RestTimer closure, array mutation, code splitting), 48 SVG animations rebuilt to articulated style, 6 new SVGs created for Hantel plan, plan switcher added, Supabase session sync (`gym_sessions` table), comprehensive documentation |
