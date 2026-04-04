# GymPlan — Documentation

## Overview

GymPlan is a Progressive Web App (PWA) for guided workout tracking. It provides exercise-by-exercise navigation with rest timers, set tracking, animated exercise illustrations, session history with charts, and push notification reminders. Built for personal use by user "Neli" with trainer Martin Schiendorfer's workout plans.

**Status:** Active, 149 commits across 62+ PRs. All development via Claude Code on feature branches with PRs to main.

**Key facts:**
- 4 workout plans: Gym (12 exercises), Dumbbell/Hantel (12), Cardio (15), Back Rehab (6)
- 48 animated SVG exercise illustrations
- PIN-locked with Supabase server-side verification + offline fallback
- All session data in localStorage (no cloud sync)
- Deployed on Vercel (static Vite build)

## Architecture

```
┌──────────────────────────────────────────────────┐
│  PinLogin (Supabase PIN verify → sessionStorage) │
├──────────────────────────────────────────────────┤
│  LocationSelector (choose workout plan)          │
├──────────────────────────────────────────────────┤
│  App (view router: home/workout/summary/history) │
│  ├── Home (plan info, quick stats, exercise list)│
│  ├── WorkoutView → ExerciseCard + RestTimer      │
│  ├── WorkoutSummary (post-workout stats)         │
│  ├── WorkoutHistory (charts, export) [lazy]      │
│  └── ReminderSettings (push notifications)       │
├──────────────────────────────────────────────────┤
│  localStorage (sessions) + sessionStorage (PIN)  │
│  Supabase (app_config table for PIN hash)        │
└──────────────────────────────────────────────────┘
```

**Tech stack:**
- React 19 + TypeScript 5.9
- Vite 7 + vite-plugin-pwa (Workbox)
- Tailwind CSS 4
- Recharts 3 (lazy-loaded)
- Lucide React (icons)
- @supabase/supabase-js (PIN auth)

**Data flow:**
1. PIN entered → hashed SHA-256 → compared against Supabase `app_config.pin_hash`
2. If Supabase unreachable → falls back to offline hash comparison
3. Workout sessions saved to `localStorage('workoutSessions')` as JSON array
4. Export: JSON (raw) or CSV (formatted with German locale)
5. Import: JSON with type validation + deduplication by session ID

## File Inventory

| File | Purpose | Status |
|------|---------|--------|
| `src/App.tsx` | Root component, view router, session state management | Active |
| `src/main.tsx` | React entry point (StrictMode) | Active |
| `src/types.ts` | TypeScript interfaces: Exercise, WorkoutPlan, WorkoutSession | Active |
| `src/index.css` | Tailwind import + custom animations (pulse, bounce, fade, shake) | Active |
| `src/components/PinLogin.tsx` | PIN entry screen with numpad, Supabase verification, keyboard support | Active |
| `src/components/LocationSelector.tsx` | Workout plan selector (4 options), Tailwind-styled | Active |
| `src/components/Home.tsx` | Dashboard: plan info, weekly stats, last workout, exercise list | Active |
| `src/components/WorkoutView.tsx` | Exercise navigation, progress bar, set/exercise state machine | Active |
| `src/components/ExerciseCard.tsx` | Single exercise display: image, instructions, set progress | Active |
| `src/components/RestTimer.tsx` | Countdown timer between sets with progress ring | Active |
| `src/components/WorkoutSummary.tsx` | Post-workout celebration with stats | Active |
| `src/components/WorkoutHistory.tsx` | Statistics dashboard with Recharts (lazy-loaded) | Active |
| `src/components/ReminderSettings.tsx` | Push notification scheduling (day/time picker) | Active |
| `src/lib/pin-service.ts` | Supabase PIN verification with offline fallback | Active |
| `src/hooks/useLocalStorage.ts` | Generic localStorage hook with JSON serialization | Active |
| `src/data/workoutPlan.ts` | 4 workout plan definitions with exercise data | Active |
| `src/utils/statistics.ts` | Extended stats: streaks, weekday analysis, weekly charts | Active |
| `src/utils/export.ts` | JSON/CSV export + JSON import with validation | Active |
| `public/exercise-images/*.svg` | 48 animated SVG exercise illustrations | Active |
| `public/icon.svg` | App icon (used by PWA manifest) | Active |
| `index.html` | HTML shell with PWA meta tags | Active |
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
- Supabase project with `app_config` table (shared with CoffeeTracker/EcoFlowMon)

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

The app shares the `app_config` table with CoffeeTracker and EcoFlowMon. If the table doesn't exist yet:

```sql
CREATE TABLE app_config (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
);

-- Insert PIN hash (SHA-256 of the 4-digit PIN)
INSERT INTO app_config (key, value)
VALUES ('pin_hash', '<sha256-hash-of-your-pin>');

-- RLS: allow anon reads
ALTER TABLE app_config ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow anon read" ON app_config
  FOR SELECT USING (true);
```

### Vercel Deployment

```bash
# Link and deploy (first time)
vercel

# Subsequent deploys
vercel --prod

# Required env vars on Vercel:
#   VITE_SUPABASE_URL
#   VITE_SUPABASE_ANON_KEY
```

## Technical Patterns

- **Supabase PIN with offline fallback**: `pin-service.ts` tries Supabase first, catches network errors, and falls back to a hardcoded SHA-256 hash. This is critical for a gym PWA where WiFi may be spotty. Session persists in `sessionStorage` so re-entering PIN isn't needed within a browser session.

- **Lazy-loaded heavy dependencies**: `WorkoutHistory` (which imports Recharts ~360KB) is loaded via `React.lazy()` + `Suspense`. Initial bundle dropped from 600KB to 240KB. The chart chunk only loads when the user taps "Trainings-Statistiken".

- **useRef for callback stability in timers**: `RestTimer` stores `onComplete` in a `useRef` to avoid including it in `useEffect` deps. Without this, the timer would reset on every parent re-render because callback props get new references each render.

- **Non-mutating array operations**: All sorting uses `.toSorted()` (ES2023) instead of `.sort()` to avoid mutating React state/props. The `tsconfig` targets ES2023 to support this.

- **Typed JSON import validation**: `export.ts` validates imported JSON field-by-field with `typeof` checks, `Date.parse()` for dates, `Number.isFinite()` for numbers. Constructs clean objects from validated data instead of using `as` type casts.

- **SHA-256 via Web Crypto API**: PIN hashing uses `crypto.subtle.digest('SHA-256', ...)` — native browser API, no dependencies, available in all target browsers.

- **PWA with Workbox precaching**: `vite-plugin-pwa` generates a service worker that precaches all static assets with content hashes. Runtime caching for external images. The manual `sw.js` was removed to avoid conflicts.

- **View-based routing without a router**: App uses a simple `useState<AppView>` to switch between views. No React Router — keeps the bundle small and avoids URL management complexity for a PWA that always starts fresh.

- **Security headers via vercel.json**: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `X-XSS-Protection: 1; mode=block` applied to all routes. SW gets `Cache-Control: must-revalidate`.

## Lessons Learned

- **Hardcoded PIN in source code is easily discovered**: Even in a minified bundle, string constants are visible. SHA-256 hashing was the immediate fix; Supabase server-side verification is the proper solution.
- **`sessions.sort()` silently mutates props**: This caused no visible bugs in this app but is a latent issue. `.toSorted()` is the clean modern fix.
- **Duplicate service workers cause confusing caching**: Having both a manual `public/sw.js` and Workbox-generated one led to unpredictable cache behavior. Use only one approach.
- **`onComplete` in `useEffect` deps causes timer chaos**: A callback prop in the dependency array of a timer effect means the effect re-runs on every render. `useRef` is the standard fix.
- **Code splitting Recharts has massive impact**: A single `React.lazy()` call reduced the initial bundle by 60%.

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
| 2026-04-04 | Code review session: security hardening (Supabase PIN auth), bug fixes (RestTimer, array mutation, plan name, double image load), code splitting (Recharts lazy load), Tailwind migration (LocationSelector), cleanup (duplicate SW/manifest, unused files) |
