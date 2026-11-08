// Renders assets/share/who-guards-the-pipes.jpg (1200x630) from card.html, and assets/previews/who-guards-the-pipes.jpg (1200x800, the top of index.html with the stamp hidden). Plain Chrome DevTools. usage: node render.cjs
const { spawn } = require('node:child_process');
const { writeFileSync } = require('node:fs');
const path = require('node:path');
const id = 'who-guards-the-pipes';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function open(w, h, url) {
  const port = 9800 + Math.floor(Math.random() * 100);
  const chrome = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    ['--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files', `--remote-debugging-port=${port}`, `--user-data-dir=/tmp/card-wgtp-${port}`, 'about:blank'], { stdio: 'ignore' });
  let tgt;
  for (let i = 0; i < 50 && !tgt; i++) { await sleep(200); try { tgt = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).find((t) => t.type === 'page'); } catch {} }
  const ws = new WebSocket(tgt.webSocketDebuggerUrl);
  await new Promise((r) => ws.addEventListener('open', r));
  let n = 0; const pend = new Map();
  ws.addEventListener('message', (m) => { const d = JSON.parse(m.data); if (d.id && pend.has(d.id)) { pend.get(d.id)(d.result); pend.delete(d.id); } });
  const send = (method, params = {}) => new Promise((r) => { const i = ++n; pend.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
  const ev = async (expression) => (await send('Runtime.evaluate', { expression, returnByValue: true })).result.value;
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 1, mobile: false });
  await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-reduced-motion', value: 'reduce' }] });
  await send('Page.enable');
  await send('Page.navigate', { url });
  return { ws, chrome, send, ev };
}
(async () => {
  // share card
  let c = await open(1200, 630, 'file://' + __dirname + '/card.html');
  for (let i = 0; i < 60; i++) { await sleep(250); if (await c.ev('!!document.body && document.body.hasAttribute("data-ready")')) break; }
  await sleep(400);
  let shot = await c.send('Page.captureScreenshot', { format: 'jpeg', quality: 90, clip: { x: 0, y: 0, width: 1200, height: 630, scale: 1 } });
  writeFileSync(path.resolve(__dirname, '../../../assets/share/' + id + '.jpg'), Buffer.from(shot.data, 'base64'));
  console.log('ok share');
  c.ws.close(); c.chrome.kill();
  // preview
  c = await open(1200, 800, 'file://' + path.resolve(__dirname, '../index.html'));
  await sleep(4000);
  await c.ev("document.querySelector('.stamp').style.visibility='hidden'");
  await sleep(200);
  shot = await c.send('Page.captureScreenshot', { format: 'jpeg', quality: 88, clip: { x: 0, y: 0, width: 1200, height: 800, scale: 1 } });
  writeFileSync(path.resolve(__dirname, '../../../assets/previews/' + id + '.jpg'), Buffer.from(shot.data, 'base64'));
  console.log('ok preview');
  c.ws.close(); c.chrome.kill(); process.exit(0);
})();
