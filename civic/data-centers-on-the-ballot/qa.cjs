// usage: node qa.cjs  -> checks civic/data-centers-on-the-ballot/index.html at 390 and 1280 in headless Chrome; screenshots to shots/
// Checks: horizontal overflow (page and any element past the right edge), every citation resolving to a numbered source with a link, no em dashes, no console errors.
const { spawn } = require('node:child_process');
const { writeFileSync, mkdirSync } = require('node:fs');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const SHOTS = __dirname + '/shots';
mkdirSync(SHOTS, { recursive: true });
async function run(W) {
  const port = 9700 + Math.floor(Math.random() * 200);
  const chrome = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    ['--headless=new', '--disable-gpu', '--hide-scrollbars', `--remote-debugging-port=${port}`, `--user-data-dir=/tmp/dcbqa-${port}`, 'about:blank'], { stdio: 'ignore' });
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
  await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-reduced-motion', value: 'reduce' }] });
  await send('Emulation.setDeviceMetricsOverride', { width: W, height: 900, deviceScaleFactor: W < 600 ? 2 : 1, mobile: W < 600 });
  await send('Page.enable');
  await send('Page.navigate', { url: 'file://' + __dirname + '/index.html' });
  await sleep(2500);
  const out = { W };
  out.page_overflow = await ev(`document.documentElement.scrollWidth - innerWidth`);
  out.overflowing = await ev(`(()=>{const r=[];document.querySelectorAll('body *').forEach(e=>{const b=e.getBoundingClientRect();if(!b.width||getComputedStyle(e).display==='none')return;if(e.closest('.jump'))return;if(b.right>innerWidth+1||b.left<-1){r.push((e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className)+'<'+e.tagName+'> '+Math.round(b.left)+'..'+Math.round(b.right))}});return r.slice(0,12)})()`);
  out.em_dash = await ev(`document.body.innerText.includes('\\u2014')`);
  out.cites = await ev(`(()=>{const a=[...document.querySelectorAll('.c a')];const bad=a.filter(x=>{const t=document.querySelector(x.getAttribute('href'));return !t||!t.querySelector('a[href^="https://"]')||t.id!=='s'+x.textContent.replace(/\\D/g,'')});return a.length+' citations, '+bad.length+' unresolved'+(bad.length?': '+bad.slice(0,5).map(x=>x.getAttribute('href')).join(' '):'')})()`);
  out.sources = await ev(`document.querySelectorAll('ol.src li').length + ' sources; ' + [...document.querySelectorAll('ol.src li')].filter(l=>!document.querySelector('.c a[href="#'+l.id+'"]')).length + ' never cited; ' + [...document.querySelectorAll('ol.src a')].filter(a=>!/^https:\\/\\//.test(a.href)).length + ' non-https links'`);
  out.posted = await ev(`document.querySelector('.stamp').innerText`);
  out.bg = await ev(`getComputedStyle(document.body).backgroundColor`);
  out.contrast = await ev(`(()=>{const t=document.body.innerText;const r=[];[/\bnot [a-z]+,? but\b/i,/isn't [a-z ]+, it's/i,/\bnot just\b/i].forEach(x=>{const m=t.match(x);if(m)r.push(m[0])});return r})()`);
  out.tracker_marks = await ev(`document.querySelectorAll('.row i.tr').length`);
  out.rows = await ev(`document.querySelectorAll('.board .row').length+' rows, '+document.querySelectorAll('.board .row.won').length+' won, '+document.querySelectorAll('.board .row.lost').length+' lost, '+document.querySelectorAll('.board .row.pend').length+' pending'`);
  out.errors = errors.filter(e => !/cloudflareinsights|ERR_INTERNET|ERR_NAME|net::/.test(e));
  await ev(`window.scrollTo(0,0)`);
  const H = await ev(`document.documentElement.scrollHeight`);
  out.words = await ev(`document.body.innerText.split(/\\s+/).length`);
  out.height = H;
  await send('Emulation.setDeviceMetricsOverride', { width: W, height: Math.min(H, 16000), deviceScaleFactor: 1, mobile: W < 600 });
  await sleep(800);
  const r = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true });
  writeFileSync(`${SHOTS}/full-${W}.png`, Buffer.from(r.data, 'base64'));
  ws.close(); chrome.kill();
  return out;
}
(async () => { for (const W of [390, 1280]) console.log(JSON.stringify(await run(W), null, 1)); process.exit(0); })();
