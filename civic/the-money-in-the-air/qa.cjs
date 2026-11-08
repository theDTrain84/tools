// usage: node qa.cjs  -> checks index.html at 390 and 1280 in headless Chrome; screenshots to shots/
// Checks: horizontal overflow (page and any element past the right edge), the House picker,
// every citation resolving to a numbered source with a link, no em dashes, no console errors.
const { spawn } = require('node:child_process');
const { writeFileSync, mkdirSync } = require('node:fs');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const SHOTS = __dirname + '/shots';
mkdirSync(SHOTS, { recursive: true });

async function run(W, { motion = false, shots = true } = {}) {
  const port = 9700 + Math.floor(Math.random() * 200);
  const chrome = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    ['--headless=new', '--disable-gpu', '--hide-scrollbars', `--remote-debugging-port=${port}`, `--user-data-dir=/tmp/mitaqa-${port}`, 'about:blank'], { stdio: 'ignore' });
  let tgt;
  for (let i = 0; i < 60 && !tgt; i++) { await sleep(200); try { tgt = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).find((t) => t.type === 'page'); } catch {} }
  const ws = new WebSocket(tgt.webSocketDebuggerUrl);
  await new Promise((r) => ws.addEventListener('open', r));
  let n = 0; const pend = new Map(); const errors = [];
  ws.addEventListener('message', (m) => { const d = JSON.parse(m.data);
    if (d.method === 'Runtime.exceptionThrown') errors.push(d.params.exceptionDetails.exception?.description || d.params.exceptionDetails.text);
    if (d.method === 'Runtime.consoleAPICalled' && d.params.type === 'error') errors.push(d.params.args.map(a => a.value || a.description).join(' '));
    if (d.id && pend.has(d.id)) { pend.get(d.id)(d.result); pend.delete(d.id); } });
  const send = (method, params = {}) => new Promise((r) => { const i = ++n; pend.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
  const ev = async (expression) => (await send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true })).result.value;
  await send('Runtime.enable');
  if (!motion) await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-reduced-motion', value: 'reduce' }] });
  await send('Emulation.setDeviceMetricsOverride', { width: W, height: 900, deviceScaleFactor: W < 600 ? 2 : 1, mobile: W < 600 });
  await send('Page.enable');
  await send('Page.navigate', { url: 'file://' + __dirname + '/index.html' });
  await sleep(2500);
  const out = { W };
  out.page_overflow = await ev(`document.documentElement.scrollWidth - innerWidth`);
  out.overflowing = await ev(`(()=>{const r=[];document.querySelectorAll('body *').forEach(e=>{const b=e.getBoundingClientRect();if(!b.width||getComputedStyle(e).display==='none')return;if(e.closest('.jump ul'))return;if(b.right>innerWidth+1||b.left<-1){r.push((e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className)+'<'+e.tagName+'> '+Math.round(b.left)+'..'+Math.round(b.right))}});return r.slice(0,12)})()`);
  out.em_dash = await ev(`document.body.innerText.includes('\\u2014')`);
  out.visible_flow = await ev(`[...document.querySelectorAll('svg.flow')].filter(s=>getComputedStyle(s).display!=='none').map(s=>s.classList[1]).join(',')`);
  // citations
  out.cites = await ev(`(()=>{const a=[...document.querySelectorAll('a.cite')];const bad=a.filter(x=>{const t=document.querySelector(x.getAttribute('href'));return !t||!t.querySelector('a[href^="http"]')||t.id!=='s-'+x.textContent.replace(/\\D/g,'')});return a.length+' citations, '+bad.length+' unresolved'+(bad.length?': '+bad.slice(0,5).map(x=>x.getAttribute('href')).join(' '):'')})()`);
  out.sources = await ev(`document.querySelectorAll('ol.src li').length + ' sources; ' + [...document.querySelectorAll('ol.src li')].filter(l=>!document.querySelector('a.cite[href="#'+l.id+'"]')).length + ' never cited'`);
  // picker
  out.picker_default = await ev(`[...document.querySelectorAll('.dpanel')].filter(p=>getComputedStyle(p).display!=='none').map(p=>p.id).join(',')`);
  await ev(`document.querySelector('.pick[data-n="7"]').click()`); await sleep(200);
  out.picker_after_7 = await ev(`[...document.querySelectorAll('.dpanel')].filter(p=>getComputedStyle(p).display!=='none').map(p=>p.id).join(',') + ' pressed=' + document.querySelector('.pick[aria-pressed="true"]').dataset.n`);
  await ev(`document.querySelector('.pick[data-n="10"]').click()`); await sleep(200);
  out.picker_after_10 = await ev(`[...document.querySelectorAll('.dpanel')].filter(p=>getComputedStyle(p).display!=='none').map(p=>p.id).join(',')`);
  await ev(`document.querySelector('a.pin[data-n="8"]').click()`); await sleep(600);
  out.pin_click_8 = await ev(`[...document.querySelectorAll('.dpanel')].filter(p=>getComputedStyle(p).display!=='none').map(p=>p.id).join(',')`);
  out.panel8_text = await ev(`document.getElementById('oh08').innerText.replace(/\\s+/g,' ').slice(0,420)`);
  out.no_editorial = await ev(`!document.getElementById('editorial') && !/editorial/i.test(document.documentElement.outerHTML)`);
  out.errors = errors;
  if (!shots) { ws.close(); chrome.kill(); return out; }
  // screenshots: full page and a few sections
  const shot = async (name, clip) => { const r = await send('Page.captureScreenshot', clip ? { format: 'png', clip: { ...clip, scale: 1 }, captureBeyondViewport: true } : { format: 'png', captureBeyondViewport: true }); writeFileSync(`${SHOTS}/${name}.png`, Buffer.from(r.data, 'base64')); };
  await ev(`window.scrollTo(0,0)`);
  const H = await ev(`document.documentElement.scrollHeight`);
  out.height = H;
  await send('Emulation.setDeviceMetricsOverride', { width: W, height: Math.min(H, 16000), deviceScaleFactor: 1, mobile: W < 600 });
  await sleep(800);
  await shot(`full-${W}`);
  for (const id of ['totals', 'senate-money', 'governor-money', 'house', 'bought', 'rules']) {
    const b = await ev(`(()=>{const r=document.getElementById('${id}').getBoundingClientRect();return {x:0,y:r.top+scrollY,width:innerWidth,height:Math.min(r.height,6000)}})()`);
    await shot(`${id}-${W}`, b);
  }
  ws.close(); chrome.kill();
  return out;
}

(async () => {
  const res = [];
  for (const W of [390, 1280]) res.push(await run(W));
  res.push(await run(1280, { motion: true, shots: false }).then(r => ({ W: '1280 motion', errors: r.errors, page_overflow: r.page_overflow })));
  console.log(JSON.stringify(res, null, 1));
})();
