// MER-213 bounded browser regression audit. Evidence tooling only: run against `python3 -m http.server 8099` from the repo root; needs Playwright and Chromium locally, never a site dependency.
let chromium; try { ({ chromium } = require('playwright')); } catch (e) { ({ chromium } = require('/opt/node22/lib/node_modules/playwright')); }
const fs = require('fs');
const path = require('path');
const OUT = __dirname;
const BASE = 'http://127.0.0.1:8099';
const ROUTES = ['/', '/platform/', '/solutions/', '/pilot/', '/company/', '/contact/', '/404.html'];
const VIEWPORTS = [
  { name: 'desktop-1440', width: 1440, height: 900 },
  { name: 'laptop-1024', width: 1024, height: 768 },
  { name: 'tablet-768', width: 768, height: 1024 },
  { name: 'mobile-390', width: 390, height: 844 },
  { name: 'mobile-360', width: 360, height: 740 },
];
const findings = [];
const log = (...a) => console.log(...a);
const note = (sev, where, msg) => { findings.push({ sev, where, msg }); log(`[${sev}] ${where}: ${msg}`); };

async function scrollAll(page) {
  await page.evaluate(async () => {
    const step = Math.max(300, innerHeight * 0.8);
    for (let y = 0; y < document.documentElement.scrollHeight; y += step) {
      window.scrollTo(0, y);
      await new Promise((r) => setTimeout(r, 120));
    }
    window.scrollTo(0, 0);
  });
  await page.waitForTimeout(600);
}

async function pageChecks(page, where) {
  const r = await page.evaluate(() => {
    const out = {};
    out.overflow = document.documentElement.scrollWidth - document.documentElement.clientWidth;
    out.bodyOverflow = document.body.scrollWidth - document.documentElement.clientWidth;
    out.lang = document.documentElement.lang;
    out.title = document.title;
    out.h1 = [...document.querySelectorAll('h1')].map((h) => h.textContent.trim());
    out.brokenImgs = [...document.images]
      .filter((i) => i.complete && i.naturalWidth === 0 && (i.currentSrc || i.src))
      .map((i) => i.currentSrc || i.src);
    out.pendingImgs = [...document.images]
      .filter((i) => !i.complete && (i.currentSrc || i.src))
      .map((i) => i.currentSrc || i.src);
    const keyLike = /^[a-z0-9_-]+(\.[a-z0-9_-]+)+$/i;
    out.rawKeys = [...document.querySelectorAll('[data-i18n]')]
      .filter((e) => keyLike.test(e.textContent.trim()) || e.textContent.trim() === '')
      .filter((e) => !e.hidden && e.offsetParent !== null || e.textContent.trim() !== '')
      .map((e) => e.getAttribute('data-i18n') + '=>' + e.textContent.trim())
      .filter((s) => keyLike.test(s.split('=>')[1]) || s.endsWith('=>'));
    out.imgNoAlt = [...document.images].filter((i) => !i.hasAttribute('alt')).map((i) => i.src);
    return out;
  });
  if (r.overflow > 1) note('DEFECT', where, `horizontal overflow ${r.overflow}px`);
  if (r.brokenImgs.length) note('DEFECT', where, `broken images: ${r.brokenImgs.join(', ')}`);
  if (r.rawKeys.length) note('DEFECT', where, `raw/empty i18n: ${r.rawKeys.join(' | ')}`);
  if (r.imgNoAlt.length) note('DEFECT', where, `img without alt attr: ${r.imgNoAlt.join(', ')}`);
  return r;
}

(async () => {
  const browser = await chromium.launch();
  const results = { pages: [], links: [], hero: [], nav: [], i18n: [] };

  // ---------- 1. every route x viewport x lang ----------
  for (const lang of ['en', 'tr']) {
    for (const vp of VIEWPORTS) {
      const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height }, deviceScaleFactor: 1 });
      await ctx.addInitScript((l) => { try { localStorage.setItem('orbgss.lang', l); } catch (e) {} }, lang);
      for (const route of ROUTES) {
        const where = `${route} @${vp.name} ${lang}`;
        const page = await ctx.newPage();
        const errs = [];
        const failed = [];
        page.on('console', (m) => { if (m.type() === 'error' || m.type() === 'warning') errs.push(`${m.type()}: ${m.text()}`); });
        page.on('pageerror', (e) => errs.push('pageerror: ' + e.message));
        page.on('requestfailed', (rq) => failed.push(`${rq.url()} ${rq.failure() && rq.failure().errorText}`));
        page.on('response', (rs) => { if (rs.status() >= 400) failed.push(`${rs.url()} HTTP ${rs.status()}`); });
        const resp = await page.goto(BASE + route, { waitUntil: 'load' });
        if (!resp || resp.status() >= 400) note('DEFECT', where, `HTTP ${resp && resp.status()}`);
        await page.waitForTimeout(500);
        await scrollAll(page);
        const r = await pageChecks(page, where);
        if (route !== '/404.html' && lang === 'tr' && r.lang !== 'tr') note('DEFECT', where, `html lang=${r.lang}, expected tr`);
        if (route !== '/404.html' && lang === 'en' && r.lang !== 'en') note('DEFECT', where, `html lang=${r.lang}, expected en`);
        // Ignore aborted media (video aborts are benign) but report everything else.
        const realFailed = failed.filter((f) => !/\.(webm|mp4)/.test(f) || /HTTP/.test(f));
        if (errs.length) note('DEFECT', where, `console: ${errs.join(' || ')}`);
        if (realFailed.length) note('DEFECT', where, `network: ${realFailed.join(' || ')}`);
        results.pages.push({ where, ...r, errs, failed: realFailed });
        await page.close();
      }
      await ctx.close();
    }
  }

  // ---------- 2. links (EN desktop) ----------
  {
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const page = await ctx.newPage();
    const cache = {};
    async function ids(url) {
      if (cache[url]) return cache[url];
      const p = await ctx.newPage();
      const rs = await p.goto(url, { waitUntil: 'load' });
      const status = rs ? rs.status() : 0;
      const idList = await p.evaluate(() => [...document.querySelectorAll('[id]')].map((e) => e.id));
      await p.close();
      return (cache[url] = { status, idList });
    }
    for (const route of ROUTES.slice(0, 6)) {
      await page.goto(BASE + route, { waitUntil: 'load' });
      await page.waitForTimeout(400);
      const hrefs = await page.evaluate(() => [...document.querySelectorAll('a[href]')].map((a) => ({
        href: a.getAttribute('href'), abs: a.href, text: a.textContent.trim().slice(0, 40), visible: a.offsetParent !== null,
      })));
      const seen = new Set();
      for (const h of hrefs) {
        const key = route + '|' + h.abs;
        if (seen.has(key)) continue;
        seen.add(key);
        if (/^mailto:|^tel:/.test(h.href)) {
          results.links.push({ route, href: h.href, ok: true, kind: 'mailto' });
          if (!/^mailto:contact@orbgss\.com/.test(h.href)) note('DEFECT', route, `unexpected mailto ${h.href}`);
          continue;
        }
        const u = new URL(h.abs);
        if (u.origin !== BASE) { results.links.push({ route, href: h.href, kind: 'external', ok: null }); continue; }
        const target = await ids(BASE + u.pathname);
        let ok = target.status < 400;
        let why = ok ? '' : `HTTP ${target.status}`;
        if (ok && u.hash && u.hash.length > 1 && !target.idList.includes(decodeURIComponent(u.hash.slice(1)))) { ok = false; why = `anchor ${u.hash} missing on ${u.pathname}`; }
        results.links.push({ route, href: h.href, ok, why });
        if (!ok) note('DEFECT', `${route} link ${h.href}`, why);
      }
    }
    // externals list
    const ext = results.links.filter((l) => l.kind === 'external');
    log('external links (not fetched):', [...new Set(ext.map((e) => e.href))].join(', ') || 'none');
    await ctx.close();
  }

  // ---------- 3. navigation order + dropdown ----------
  {
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    for (const lang of ['en', 'tr']) {
      await ctx.addInitScript((l) => { try { localStorage.setItem('orbgss.lang', l); } catch (e) {} }, lang);
      const page = await ctx.newPage();
      await page.goto(BASE + '/', { waitUntil: 'load' });
      await page.waitForTimeout(500);
      const top = await page.evaluate(() => [...document.querySelectorAll('.nav-list > li')].map((li) => li.textContent.replace(/\s+/g, ' ').trim()));
      await page.click('.nav-trigger');
      await page.waitForTimeout(200);
      const menu = await page.evaluate(() => ({
        expanded: document.querySelector('.nav-trigger').getAttribute('aria-expanded'),
        items: [...document.querySelectorAll('#solutions-menu a')].map((a) => a.textContent.trim() + ' -> ' + a.getAttribute('href')),
      }));
      results.nav.push({ lang, top, menu });
      log('NAV', lang, JSON.stringify(top), JSON.stringify(menu));
      if (menu.expanded !== 'true') note('DEFECT', `nav ${lang}`, 'Solutions trigger did not expand');
      await page.keyboard.press('Escape');
      await page.waitForTimeout(150);
      const after = await page.evaluate(() => document.querySelector('.nav-trigger').getAttribute('aria-expanded'));
      if (after !== 'false') note('DEFECT', `nav ${lang}`, 'Escape did not close the Solutions menu');
      await page.close();
    }
    await ctx.close();
  }

  // ---------- 4. language switch toggling at runtime + persistence across routes ----------
  {
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const page = await ctx.newPage();
    await page.goto(BASE + '/', { waitUntil: 'load' });
    const en = await page.evaluate(() => document.querySelector('h1').textContent.trim());
    const sw = await page.$$('[data-lang], .lang-switch button, .lang-btn');
    log('lang switch controls found:', sw.length);
    const trBtn = await page.$('button[data-lang="tr"], .lang-switch [data-lang="tr"], [data-set-lang="tr"]');
    if (trBtn) {
      await trBtn.click();
      await page.waitForTimeout(300);
      const tr = await page.evaluate(() => ({ h1: document.querySelector('h1').textContent.trim(), lang: document.documentElement.lang }));
      results.i18n.push({ en, tr });
      log('I18N home h1', JSON.stringify({ en, tr }));
      if (tr.lang !== 'tr' || tr.h1 === en) note('DEFECT', 'lang switch', 'TR did not change h1/lang');
      await page.goto(BASE + '/platform/', { waitUntil: 'load' });
      await page.waitForTimeout(300);
      const persisted = await page.evaluate(() => document.documentElement.lang);
      if (persisted !== 'tr') note('DEFECT', 'lang switch', 'TR did not persist to /platform/');
    } else {
      note('CHECK', 'lang switch', 'could not locate TR button by selector');
    }
    await ctx.close();
  }

  // ---------- 5. hero: desktop motion, reduced motion, mobile, save-data-ish ----------
  async function heroRun(label, ctxOpts, waitMs, shot) {
    const ctx = await browser.newContext(ctxOpts);
    const page = await ctx.newPage();
    const errs = [];
    page.on('console', (m) => { if (m.type() === 'error') errs.push(m.text()); });
    page.on('pageerror', (e) => errs.push('pageerror: ' + e.message));
    const media = [];
    page.on('response', (rs) => { if (/\.(webm|mp4)/.test(rs.url())) media.push(rs.url().split('/').pop() + ' ' + rs.status()); });
    await page.goto(BASE + '/', { waitUntil: 'load' });
    const samples = [];
    const t0 = Date.now();
    while (Date.now() - t0 < waitMs) {
      await page.waitForTimeout(1500);
      samples.push(await page.evaluate(() => {
        const h = document.getElementById('hero');
        const v = h.querySelector('video');
        return {
          state: h.getAttribute('data-hero-state'),
          payoff: h.getAttribute('data-hero-payoff') || h.querySelector('[data-hero-drape]') && !h.querySelector('[data-hero-drape]').hidden,
          src: v.getAttribute('src'), t: +v.currentTime.toFixed(1), paused: v.paused, ended: v.ended, dur: v.duration,
        };
      }));
    }
    const final = samples[samples.length - 1];
    const attrs = await page.evaluate(() => [...document.getElementById('hero').attributes].map((a) => a.name + '=' + (a.value || '').slice(0, 30)));
    if (shot) await page.screenshot({ path: path.join(OUT, shot) });
    log('HERO', label, JSON.stringify(final), 'media:', media.join(','), 'errs:', errs.join('|') || 'none');
    results.hero.push({ label, final, samples, media, errs, attrs });
    await ctx.close();
    return { final, media, errs, samples };
  }

  const d = await heroRun('desktop motion', { viewport: { width: 1440, height: 900 } }, 22000, 'hero-desktop.png');
  if (!/playing|held|payoff/.test(JSON.stringify(d.final.state))) note('CHECK', 'hero desktop', `state=${d.final.state}`);
  if (d.errs.length) note('DEFECT', 'hero desktop', d.errs.join('|'));
  const rm = await heroRun('reduced-motion', { viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' }, 6000, 'hero-reduced.png');
  if (rm.final.src) note('DEFECT', 'hero reduced-motion', `video got src ${rm.final.src}`);
  if (rm.media.length) note('DEFECT', 'hero reduced-motion', `video fetched: ${rm.media.join(',')}`);
  const mb = await heroRun('mobile 390', { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 }, 5000, 'hero-mobile.png');
  if (mb.final.src) note('DEFECT', 'hero mobile', `video got src ${mb.final.src}`);
  if (mb.media.length) note('DEFECT', 'hero mobile', `video fetched: ${mb.media.join(',')}`);
  // JS disabled -> poster is the hero
  {
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, javaScriptEnabled: false });
    const page = await ctx.newPage();
    await page.goto(BASE + '/', { waitUntil: 'load' });
    await page.waitForTimeout(800);
    const r = await page.evaluate(() => ({
      posterLoaded: [...document.querySelectorAll('#hero img')].some((i) => i.complete && i.naturalWidth > 0),
      h1: document.querySelector('h1').textContent.trim(),
    }));
    log('HERO no-JS', JSON.stringify(r));
    if (!r.posterLoaded) note('DEFECT', 'hero no-JS', 'no poster image rendered');
    await page.screenshot({ path: path.join(OUT, 'hero-nojs.png') });
    await ctx.close();
  }

  // ---------- 6. full-page screenshots for the record ----------
  for (const vp of [VIEWPORTS[0], VIEWPORTS[3]]) {
    const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
    const page = await ctx.newPage();
    await page.goto(BASE + '/', { waitUntil: 'load' });
    await scrollAll(page);
    await page.screenshot({ path: path.join(OUT, `home-full-${vp.name}.png`), fullPage: true });
    await ctx.close();
  }

  await browser.close();
  fs.writeFileSync(path.join(OUT, 'results.json'), JSON.stringify({ findings, results }, null, 1));
  const defects = findings.filter((f) => f.sev === 'DEFECT');
  log(`\nDONE. defects=${defects.length} checks=${findings.length - defects.length}`);
})().catch((e) => { console.error('AUDIT SCRIPT FAILURE', e); process.exit(2); });
