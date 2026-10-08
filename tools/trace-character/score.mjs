// Render a traced SVG on white at native size, for scoring against the reference.
// usage: node score.mjs in.svg out.png   (needs playwright; run `npm install` in pepe-illustrations/)
import { createRequire } from 'node:module';
import { readFileSync } from 'node:fs';
const require = createRequire(new URL('../../pepe-illustrations/package.json', import.meta.url));
const { chromium } = require('playwright');
const [svg, out] = process.argv.slice(2);
const b = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
const p = await b.newPage({ viewport: { width: 1024, height: 1536 } });
await p.setContent(`<html><body style="margin:0;background:#fff">${readFileSync(svg, 'utf8')}</body></html>`);
await p.screenshot({ path: out });
await b.close();
