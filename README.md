# GymPlan - Ganzkörper Trainingsplan App

Eine Progressive Web App (PWA) für deinen persönlichen Ganzkörper-Trainingsplan, erstellt von Trainer Martin Schiendorfer.

## Features

- **Übung-für-Übung Navigation**: Geführtes Training durch alle Übungen
- **Rest Timer**: Automatischer Countdown für Pausen zwischen Sets
- **Set-Tracking**: Abhaken von Sets mit visuellem Fortschritt
- **Detaillierte Anweisungen**: Genaue Ausführungshinweise für jede Übung
- **Übungsbilder**: Animierte GIFs zeigen die richtige Ausführung
- **Trainings-Statistiken**: Verlauf und Analyse deiner Workouts
- **Erinnerungen**: Push-Benachrichtigungen für deine Trainingstage
- **Offline-Modus**: Funktioniert auch ohne Internet
- **Mobile-First**: Optimiert für Smartphone-Nutzung

## Installation

### Entwicklungsumgebung

```bash
# Abhängigkeiten installieren
npm install

# Development Server starten
npm run dev

# Build für Production
npm run build

# Preview Production Build
npm run preview
```

## Als PWA auf dem Handy installieren

### iPhone (Safari)

1. Öffne die App im Safari Browser
2. Tippe auf das "Teilen" Symbol (Quadrat mit Pfeil nach oben)
3. Scrolle runter und wähle "Zum Home-Bildschirm"
4. Tippe auf "Hinzufügen"

### Android (Chrome)

1. Öffne die App im Chrome Browser
2. Tippe auf die drei Punkte (Menü)
3. Wähle "Zum Startbildschirm hinzufügen"
4. Tippe auf "Hinzufügen"

## Verwendung

### Training starten

1. Öffne die App auf dem Startbildschirm
2. Tippe auf "Training starten"
3. Folge den Übungen Schritt für Schritt
4. Markiere jeden Satz als abgeschlossen
5. Der Timer startet automatisch für die Pause

### Erinnerungen einrichten

1. Gehe zur Startseite
2. Tippe auf "Erinnerungen verwalten"
3. Aktiviere die Erinnerungen
4. Wähle deine Trainingstage (empfohlen: 2x pro Woche)
5. Stelle die gewünschte Uhrzeit ein

### Statistiken ansehen

1. Gehe zur Startseite
2. Tippe auf "Trainings-Statistiken"
3. Siehe deinen Fortschritt und Verlauf

## Trainingsplan Details

- **Name**: Ganzkörper-Trainingsplan
- **Ziel**: Allgemeine Fitness
- **Trainer**: Martin Schiendorfer
- **Einheiten pro Woche**: 2
- **Anzahl Übungen**: 10

### Übungen

1. Adduktionsmaschine (3×15 @ 15 kg)
2. Abduktionsmaschine (3×15 @ 15 kg)
3. Beinpresse horizontal (3×15 @ 50 kg)
4. Brustpresse (3×15 @ 15 kg)
5. Seitheben Kurzhantel (3×15 @ 2 kg)
6. Ruderzug Maschine (3×15 @ 19 kg)
7. Butterfly Maschine (3×15 @ 5 kg)
8. Crunch (2×15)
9. Heel Touches (2×15)
10. Hollow Hold (2×15 Sekunden)

## Technologie-Stack

- **Framework**: React 18 + TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Build Tool**: Vite
- **PWA**: vite-plugin-pwa
- **Service Worker**: Workbox

## Datenspeicherung

Alle Daten werden lokal auf deinem Gerät gespeichert:
- Trainings-Sessions im localStorage
- Erinnerungs-Einstellungen im localStorage
- Keine Cloud-Synchronisation
- Deine Daten bleiben privat auf deinem Gerät

## Browser-Kompatibilität

- Chrome/Edge (Desktop & Mobile) ✅
- Safari (iOS & macOS) ✅
- Firefox (Desktop & Mobile) ✅
- Samsung Internet ✅

## Deployment

Die App kann auf verschiedenen Plattformen gehostet werden:

- **Vercel**: Einfaches Deployment direkt aus Git
- **Netlify**: Automatisches Deployment mit PWA-Support
- **GitHub Pages**: Kostenloses Hosting für statische Apps

## Lizenz

Privates Projekt für persönliche Nutzung.

## Support

Bei Fragen oder Problemen wende dich an deinen Trainer Martin Schiendorfer.

---

**Viel Erfolg beim Training!** 💪
