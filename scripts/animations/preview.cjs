// Kontaktabzug einer animierten SVG: N Zeitpunkte nebeneinander als PNG.
// Nutzung: node scripts/animations/preview.cjs <datei.svg> <out.png> [frames=8]
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const [svgPath, outPath, framesArg] = process.argv.slice(2);
  const frames = Number(framesArg || 8);
  const svg = fs.readFileSync(svgPath, 'utf8');
  // Loop-Dauer = längste dur im Dokument (Puls-Effekte sind kürzer)
  const durs = [...svg.matchAll(/dur="([\d.]+)s"/g)].map((m) => Number(m[1]));
  const dur = durs.length ? Math.max(...durs) : 4;
  const cells = Array.from({ length: frames }, (_, i) => {
    const t = (dur * i) / frames;
    return `<div class="c"><div class="t">t=${t.toFixed(1)}s</div>${svg.replace(/<\?xml[^>]*>/, '')}</div>`;
  }).join('');
  const html = `<!doctype html><html><body style="margin:0;background:#000">
<style>.g{display:grid;grid-template-columns:repeat(4,400px);gap:4px}.c{position:relative}
.t{position:absolute;left:6px;top:4px;color:#0f0;font:11px monospace;z-index:2}svg{display:block}</style>
<div class="g">${cells}</div></body></html>`;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 4 * 404, height: 800 } });
  await page.setContent(html);
  await page.evaluate((args) => {
    const { dur, frames } = args;
    document.querySelectorAll('svg').forEach((s, i) => {
      s.pauseAnimations();
      s.setCurrentTime((dur * i) / frames);
    });
  }, { dur, frames });
  await page.waitForTimeout(100);
  const grid = await page.$('.g');
  await grid.screenshot({ path: outPath });
  await browser.close();
  console.log(`${path.basename(svgPath)}: dur=${dur}s -> ${outPath}`);
})();
