#!/usr/bin/env node
// Render a scene SVG to PNG with the bundled handwriting fonts, then print a
// detail report so a thin, low-effort drawing gets caught before delivery.
//
//   node scripts/render.mjs <scene.svg> [out.png] [--scale 2]
//
// Needs Playwright with a Chromium build: run `npm install` in the skill folder
// (or `npx playwright install chromium` if no browser is present). Set
// CHROMIUM_PATH to point at a specific browser binary if Playwright can't find one.

import { readFileSync, writeFileSync, mkdtempSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve, dirname, basename } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';

const here = dirname(fileURLToPath(import.meta.url));
const fontsDir = resolve(here, '../assets/fonts');

const args = process.argv.slice(2);
const scaleIdx = args.indexOf('--scale');
const scale = scaleIdx >= 0 ? Number(args.splice(scaleIdx, 2)[1]) : 2;
const [svgArg, outArg] = args;
if (!svgArg) {
  console.error('usage: node scripts/render.mjs <scene.svg> [out.png] [--scale 2]');
  process.exit(2);
}
const svgPath = resolve(svgArg);
const outPath = resolve(outArg ?? svgPath.replace(/\.svg$/i, '.png'));

async function loadChromium() {
  const tries = ['playwright', 'playwright-core', '@playwright/test'];
  // Look next to this script (npm install inside the skill folder), then in the cwd.
  const reqs = [createRequire(import.meta.url), createRequire(join(process.cwd(), 'noop.js'))];
  for (const name of tries) {
    try { return (await import(name)).chromium; } catch {}
    for (const req of reqs) {
      try { return req(name).chromium; } catch {}
    }
  }
  // Fall back to a global install (npm root -g).
  try {
    const { execSync } = await import('node:child_process');
    const root = execSync('npm root -g').toString().trim();
    for (const name of tries) {
      const p = join(root, name);
      if (existsSync(p)) return createRequire(join(root, 'noop.js'))(p).chromium;
    }
  } catch {}
  console.error('Playwright not found. Install it with: npm i -D playwright');
  process.exit(2);
}

const svg = readFileSync(svgPath, 'utf8').replace(/<\?xml[^>]*\?>/, '');
const font = (f) => pathToFileURL(join(fontsDir, f)).href;
const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face { font-family: 'Caveat'; src: url('${font('Caveat.ttf')}'); font-weight: 400 700; }
@font-face { font-family: 'Ma Shan Zheng'; src: url('${font('MaShanZheng.ttf')}'); }
html, body { margin: 0; background: #fff; }
svg { display: block; }
</style></head><body>${svg}</body></html>`;
const htmlPath = join(mkdtempSync(join(tmpdir(), 'pepe-render-')), 'scene.html');
writeFileSync(htmlPath, html);

const chromium = await loadChromium();
const launchOpts = process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {};
const browser = await chromium.launch(launchOpts);
const page = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: scale });
await page.goto(pathToFileURL(htmlPath).href);
await page.evaluate(async () => {
  await Promise.all([document.fonts.load('40px Caveat'), document.fonts.load("40px 'Ma Shan Zheng'", '图')]);
  await document.fonts.ready;
});

const report = await page.evaluate(() => {
  const svg = document.querySelector('svg');
  const vb = svg.getAttribute('viewBox');
  const shapes = svg.querySelectorAll('path, line, polyline, polygon, circle, ellipse, rect');
  const texts = [...svg.querySelectorAll('text')].map((t) => t.textContent.trim()).filter(Boolean);
  const colors = new Set();
  svg.querySelectorAll('*').forEach((el) => {
    for (const a of ['stroke', 'fill']) {
      const v = el.getAttribute(a);
      if (v && v.startsWith('#')) colors.add(v.toLowerCase());
    }
  });
  const fontsOk = document.fonts.check('40px Caveat');
  const box = svg.getBoundingClientRect();
  return { vb, shapeCount: shapes.length, texts, colors: [...colors], fontsOk, w: box.width, h: box.height };
});

const el = await page.$('svg');
await el.screenshot({ path: outPath, omitBackground: false });
await browser.close();

// ---- detail report ----
const ALLOWED = new Set([
  '#fff', '#ffffff', '#1a1a1a', '#111', '#111111', '#000', '#000000', // ink + paper
  '#ef8a1f', '#e0302a', '#2f6fd6', // orange / red / blue annotation inks
  '#7fa23a', '#3f5719', '#1d2711', '#c26a3d', // Pepe's own palette
]);
const warnings = [];
if (report.vb !== '0 0 1600 900') warnings.push(`viewBox is "${report.vb}", expected "0 0 1600 900"`);
if (Math.round(report.w) !== 1600 || Math.round(report.h) !== 900) warnings.push(`rendered at ${report.w}x${report.h}, expected 1600x900 (set width/height)`);
if (report.shapeCount < 150) warnings.push(`only ${report.shapeCount} drawn shapes; a finished scene is usually 150-400. Props are probably under-detailed.`);
if (report.texts.length > 8) warnings.push(`${report.texts.length} labels; the style allows at most 8`);
if (report.texts.length < 2) warnings.push('fewer than 2 handwritten labels');
const off = report.colors.filter((c) => !ALLOWED.has(c));
if (off.length) warnings.push(`colors outside the palette: ${off.join(', ')}`);
if (!report.fontsOk) warnings.push('handwriting font did not load');

console.log(`rendered ${basename(svgPath)} -> ${outPath}`);
console.log(`shapes: ${report.shapeCount}   labels (${report.texts.length}): ${report.texts.map((t) => JSON.stringify(t)).join(' ')}`);
console.log(`colors: ${report.colors.join(' ')}`);
if (warnings.length) {
  console.log('\nWARNINGS');
  for (const w of warnings) console.log(`  - ${w}`);
} else {
  console.log('detail check: ok');
}
console.log('\nNow open the PNG and inspect it against references/qa-checklist.md. Passing this check is necessary, not sufficient.');
