// MER-213 interaction spot checks (evidence radios, inspection aid, mobile menu). Evidence tooling only, same setup as browser_audit.js.
let chromium; try { ({ chromium } = require('playwright')); } catch (e) { ({ chromium } = require('/opt/node22/lib/node_modules/playwright')); }
const BASE = 'http://127.0.0.1:8099';
(async () => {
  const browser = await chromium.launch();
  const out = []; let bad = 0;
  const rec = (ok, msg) => { out.push((ok ? 'PASS ' : 'FAIL ') + msg); if (!ok) bad++; };
  for (const lang of ['en', 'tr']) {
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    await ctx.addInitScript((l) => localStorage.setItem('orbgss.lang', l), lang);
    const page = await ctx.newPage();
    const errs = [];
    page.on('console', (m) => m.type() === 'error' && errs.push(m.text()));
    page.on('pageerror', (e) => errs.push(e.message));
    await page.goto(BASE + '/', { waitUntil: 'load' });
    await page.waitForTimeout(500);
    for (const group of [['ev-', '.evidence-tab'], ['cp-', '.inspect-pair']]) {
      const ids = await page.$$eval(`input[type=radio][id^="${group[0]}"]`, (els) => els.map((e) => e.id));
      for (const id of ids) {
        const label = page.locator(`label[for="${id}"]`).first();
        await label.scrollIntoViewIfNeeded();
        await label.click();
        await page.waitForTimeout(700);
        const r = await page.evaluate((i) => {
          const el = document.getElementById(i);
          const scope = el.closest('section') || document;
          const imgs = [...scope.querySelectorAll('img')].filter((im) => im.offsetParent !== null && getComputedStyle(im).opacity !== '0' && im.getBoundingClientRect().width > 200);
          return { checked: el.checked, visibleImgs: imgs.length, allLoaded: imgs.every((im) => im.complete && im.naturalWidth > 0) };
        }, id);
        rec(r.checked && r.allLoaded && r.visibleImgs > 0, `${lang} radio #${id}: checked=${r.checked} visibleImgs=${r.visibleImgs} loaded=${r.allLoaded}`);
      }
    }
    rec(errs.length === 0, `${lang} console errors during interaction: ${errs.join('|') || 'none'}`);
    await ctx.close();
  }
  { // mobile menu
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
    const page = await ctx.newPage();
    await page.goto(BASE + '/', { waitUntil: 'load' });
    await page.waitForTimeout(400);
    await page.tap('.menu-toggle');
    await page.waitForTimeout(300);
    let ex = await page.getAttribute('.menu-toggle', 'aria-expanded');
    rec(ex === 'true', `mobile menu opens (aria-expanded=${ex})`);
    const vis = await page.$$eval('#primary-nav a', (as) => as.filter((a) => a.offsetParent !== null).map((a) => a.textContent.trim()));
    rec(vis.length >= 4, `mobile menu shows top-level links: ${vis.join(', ')}`);
    await page.tap('.nav-trigger');
    await page.waitForTimeout(300);
    const sol = await page.$$eval('#solutions-menu a', (as) => as.filter((a) => a.offsetParent !== null).map((a) => a.textContent.trim() + '->' + a.getAttribute('href')));
    rec(sol.length === 3, `mobile Solutions disclosure shows: ${sol.join(', ')}`);
    await page.tap('.menu-toggle');
    await page.waitForTimeout(300);
    ex = await page.getAttribute('.menu-toggle', 'aria-expanded');
    rec(ex === 'false', `mobile menu closes (aria-expanded=${ex})`);
    await ctx.close();
  }
  await browser.close();
  console.log(out.join('\n') + `\nINTERACTION RESULT: ${bad ? 'FAIL ' + bad : 'PASS'}`);
})();
