import type { LucideIcon } from 'lucide-react';
import { Activity, Building2, Dumbbell, HeartPulse, PersonStanding, Sunrise } from 'lucide-react';

/**
 * Farbwelt je Trainingsplan. Alle Klassen stehen hier als volle Literale,
 * damit Tailwind sie findet.
 */
export interface PlanTheme {
  icon: LucideIcon;
  /** Verlauf für Flächen, z. B. „bg-gradient-to-br {gradient}“ */
  gradient: string;
  /** Akzentfarben als Hex (Timer-Ring, Diagramme) */
  from: string;
  to: string;
  /** Schrift in Akzentfarbe auf dunklem Grund */
  text: string;
  /** Zarte Akzentfläche (Nummern, Chips) */
  soft: string;
  /** Leuchten hinter Kopfbereichen */
  glow: string;
}

const INDIGO: PlanTheme = {
  icon: Building2,
  gradient: 'from-indigo-500 to-purple-600',
  from: '#6366f1',
  to: '#9333ea',
  text: 'text-indigo-300',
  soft: 'bg-indigo-500/15 text-indigo-200',
  glow: 'bg-indigo-500/25',
};

const THEMES: Record<string, PlanTheme> = {
  'Ganzkörper-Trainingsplan (@gym)': INDIGO,
  'Hanteltraining (@hantel)': {
    icon: Dumbbell,
    gradient: 'from-pink-400 to-rose-500',
    from: '#f472b6',
    to: '#f43f5e',
    text: 'text-pink-300',
    soft: 'bg-pink-500/15 text-pink-200',
    glow: 'bg-pink-500/25',
  },
  'Cardio (@cardio)': {
    icon: HeartPulse,
    gradient: 'from-emerald-500 to-green-400',
    from: '#10b981',
    to: '#4ade80',
    text: 'text-emerald-300',
    soft: 'bg-emerald-500/15 text-emerald-200',
    glow: 'bg-emerald-500/25',
  },
  'Rücken-Aufbau (@rücken)': {
    icon: PersonStanding,
    gradient: 'from-teal-500 to-cyan-600',
    from: '#14b8a6',
    to: '#0891b2',
    text: 'text-teal-300',
    soft: 'bg-teal-500/15 text-teal-200',
    glow: 'bg-teal-500/25',
  },
  'Nacken, Schulter & BWS (@nacken)': {
    icon: Activity,
    gradient: 'from-sky-500 to-blue-600',
    from: '#0ea5e9',
    to: '#2563eb',
    text: 'text-sky-300',
    soft: 'bg-sky-500/15 text-sky-200',
    glow: 'bg-sky-500/25',
  },
  'Morgen-Reset (@morgen)': {
    icon: Sunrise,
    gradient: 'from-amber-400 to-orange-500',
    from: '#fbbf24',
    to: '#f97316',
    text: 'text-amber-300',
    soft: 'bg-amber-500/15 text-amber-200',
    glow: 'bg-amber-500/25',
  },
};

export function planTheme(planName: string): PlanTheme {
  return THEMES[planName] ?? INDIGO;
}
