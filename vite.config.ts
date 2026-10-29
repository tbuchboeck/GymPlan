import { execSync } from 'node:child_process'
import { readFileSync } from 'node:fs'
import { defineConfig, type Plugin } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

// Build-Info: Version aus package.json, Commit (Vercel liefert ihn per Env,
// lokal aus git) und Build-Zeitpunkt. Wird in die App eingebacken und
// zusätzlich als /version.json ausgeliefert, damit die App erkennt, wenn
// online schon eine neuere Version liegt.
function gitSha(): string {
  if (process.env.VERCEL_GIT_COMMIT_SHA) return process.env.VERCEL_GIT_COMMIT_SHA.slice(0, 7)
  try {
    return execSync('git rev-parse --short HEAD').toString().trim()
  } catch {
    return 'dev'
  }
}

const buildInfo = {
  version: JSON.parse(readFileSync(new URL('./package.json', import.meta.url), 'utf8')).version as string,
  sha: gitSha(),
  builtAt: new Date().toISOString(),
}

function versionJson(): Plugin {
  return {
    name: 'version-json',
    apply: 'build',
    generateBundle() {
      this.emitFile({ type: 'asset', fileName: 'version.json', source: JSON.stringify(buildInfo) })
    },
  }
}

// https://vite.dev/config/
export default defineConfig({
  define: {
    __BUILD_INFO__: JSON.stringify(buildInfo),
  },
  plugins: [
    react(),
    versionJson(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['icon.svg'],
      manifest: {
        name: 'GymPlan - Ganzkörper Training',
        short_name: 'GymPlan',
        description: 'Dein persönlicher Trainingsplan für allgemeine Fitness',
        theme_color: '#4f46e5',
        background_color: '#ffffff',
        display: 'standalone',
        icons: [
          {
            src: '/icon.svg',
            sizes: '512x512',
            type: 'image/svg+xml',
            purpose: 'any maskable'
          }
        ]
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg,webp,woff,woff2}'],
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/.*\.(gif|jpg|jpeg|png|webp)$/i,
            handler: 'CacheFirst',
            options: {
              cacheName: 'exercise-images',
              expiration: {
                maxEntries: 50,
                maxAgeSeconds: 60 * 60 * 24 * 30 // 30 days
              }
            }
          }
        ]
      }
    })
  ],
})
