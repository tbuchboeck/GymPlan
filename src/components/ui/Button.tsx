import type { ButtonHTMLAttributes } from 'react';

type Variant = 'primary' | 'secondary' | 'ghost' | 'success' | 'danger';
type Size = 'md' | 'lg' | 'xl';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  size?: Size;
  block?: boolean;
}

const VARIANTS: Record<Variant, string> = {
  primary:
    'bg-gradient-to-br from-indigo-500 to-violet-600 text-white shadow-lg shadow-indigo-950/60 hover:from-indigo-400 hover:to-violet-500',
  secondary: 'bg-slate-800 text-slate-100 ring-1 ring-inset ring-white/5 hover:bg-slate-700',
  ghost: 'text-slate-300 hover:text-white hover:bg-white/5',
  success:
    'bg-gradient-to-br from-emerald-500 to-green-600 text-white shadow-lg shadow-emerald-950/60 hover:from-emerald-400 hover:to-green-500',
  danger: 'bg-red-500/10 text-red-300 ring-1 ring-inset ring-red-500/40 hover:bg-red-500/20',
};

const SIZES: Record<Size, string> = {
  md: 'min-h-11 px-4 text-base rounded-xl',
  lg: 'min-h-14 px-5 text-lg rounded-2xl',
  xl: 'min-h-16 px-6 text-xl rounded-2xl',
};

/** Einheitlicher Knopf: große Touch-Fläche, sanftes Drücken, klare Varianten. */
export function Button({ variant = 'primary', size = 'lg', block = false, className = '', type = 'button', ...props }: ButtonProps) {
  return (
    <button
      type={type}
      className={`inline-flex items-center justify-center gap-2 font-semibold transition duration-150 active:scale-[0.98] disabled:opacity-40 disabled:cursor-not-allowed disabled:active:scale-100 ${VARIANTS[variant]} ${SIZES[size]} ${block ? 'w-full' : ''} ${className}`}
      {...props}
    />
  );
}
