// تستِ خودکارِ عمومی برای همهٔ صفحه‌های سایت (نسخهٔ محلی).
// node crawl.mjs <siteRoot> <out.json> [startPaths...]
// برای هر صفحه: وضعیت، خطای کنسول و اسکریپت، درخواستِ شکسته، بیرون‌زدگی در ۳۹۰px، عنوان، lang/dir،
// توضیح متا، viewport، تصویر بی‌alt، دکمه/پیوندِ بی‌نام، پیوندهای داخلیِ شکسته، پیوندِ برگشت، و axe (دسترس‌پذیری).
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const AXE = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');

const [, , ROOT, OUT, ...START] = process.argv;
const PORT = 8790;
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.woff2': 'font/woff2', '.woff': 'font/woff', '.ico': 'image/x-icon', '.webmanifest': 'application/manifest+json', '.mp3': 'audio/mpeg', '.pdf': 'application/pdf', '.txt': 'text/plain', '.enc': 'application/octet-stream' };
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0].split('#')[0]);
  let f = path.join(ROOT, p);
  if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html');
  if (!fs.existsSync(f)) { res.writeHead(404); res.end('nf'); return; }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
}).listen(PORT);
const BASE = `http://localhost:${PORT}/`;

const queue = [...START.map((s) => BASE + s)], seen = new Set(queue), results = [];
const LIMIT = 900;
const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
await ctx.route(/^https?:\/\/(?!localhost)/, (r) => r.abort());   // no outside network: tests the page itself

async function check(url) {
  const page = await ctx.newPage();
  const r = { url: url.replace(BASE, ''), console: [], pageErrors: [], failed: [] };
  page.on('console', (m) => { if (m.type() === 'error' && !/net::ERR_FAILED|ERR_BLOCKED|Failed to load resource/.test(m.text())) r.console.push(m.text().slice(0, 200)); });
  page.on('pageerror', (e) => r.pageErrors.push(String(e.message).slice(0, 200)));
  page.on('response', (resp) => { if (resp.url().startsWith(BASE) && resp.status() >= 400) r.failed.push(resp.url().replace(BASE, '') + ' ' + resp.status()); });
  try {
    const resp = await page.goto(url, { waitUntil: 'load', timeout: 30000 });
    r.status = resp ? resp.status() : 0;
    await page.waitForTimeout(600);
    Object.assign(r, await page.evaluate(() => {
      const d = document, de = d.documentElement;
      const links = [...d.querySelectorAll('a[href]')].map((a) => { try { return typeof a.href === 'string' ? a.href : new URL(a.getAttribute('href'), location.href).href; } catch (e) { return ''; } });
      return {
        title: d.title,
        lang: de.lang || d.body?.lang || '',
        dir: de.dir || d.body?.dir || getComputedStyle(d.body || de).direction,
        metaDesc: !!d.querySelector('meta[name=description]'),
        viewport: !!d.querySelector('meta[name=viewport]'),
        overflow: Math.max(de.scrollWidth, d.body ? d.body.scrollWidth : 0) - window.innerWidth,
        imgNoAlt: [...d.images].filter((i) => !i.hasAttribute('alt')).length,
        words: (d.body?.innerText || '').split(/\s+/).length,
        links,
      };
    }));
    try {
      await page.addScriptTag({ content: AXE });
      const ax = await page.evaluate(async () => {
        const res = await window.axe.run(document, { runOnly: ['wcag2a', 'wcag2aa'], resultTypes: ['violations'] });
        return res.violations.map((v) => ({ id: v.id, impact: v.impact, n: v.nodes.length }));
      });
      r.axe = ax;
    } catch (e) { r.axe = [{ id: 'axe-failed', n: 0 }]; }
  } catch (e) { r.status = 0; r.error = String(e.message).slice(0, 200); }
  await page.close();
  return r;
}

while (queue.length && results.length < LIMIT) {
  const batch = queue.splice(0, 6);
  const rs = await Promise.all(batch.map(check));
  for (const r of rs) {
    for (const l of r.links || []) {
      if (!l.startsWith(BASE)) continue;
      const u = l.split('#')[0];
      if (/\.(pdf|png|jpg|svg|json|enc|mp3|zip|txt|woff2?)$/i.test(u)) continue;
      if (!seen.has(u)) { seen.add(u); queue.push(u); }
    }
    r.internalLinks = (r.links || []).filter((l) => l.startsWith(BASE)).map((l) => l.replace(BASE, '').split('#')[0]);
    r.externalLinks = (r.links || []).filter((l) => /^https?:/.test(l) && !l.startsWith(BASE)).length;
    delete r.links;
    results.push(r);
  }
  process.stdout.write(`\r${results.length} checked, ${queue.length} queued   `);
}
// broken internal link targets
const byUrl = new Map(results.map((r) => [r.url, r]));
for (const r of results) r.brokenLinks = [...new Set(r.internalLinks.filter((l) => { const t = byUrl.get(l); return t && t.status >= 400; }))];
fs.writeFileSync(OUT, JSON.stringify({ at: new Date().toISOString(), pages: results }, null, 1));
console.log('\ndone', results.length);
await browser.close(); server.close();
