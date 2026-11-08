// Renders assets/share/the-money-in-the-air.jpg (1200x630) from card.html in this folder (method copied from stories/php2shell), plain Chrome DevTools.
// Oct 13: plain Chrome DevTools (no puppeteer; last week's puppeteer-core lived in a scratchpad that is gone).
// usage: node render.cjs
const { spawn } = require('node:child_process');
const { writeFileSync } = require('node:fs');
const id = 'the-money-in-the-air';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
(async () => {
  const port = 9800 + Math.floor(Math.random() * 100);
  const chrome = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    ['--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files', `--remote-debugging-port=${port}`, `--user-data-dir=/tmp/card-mitair-${port}`, 'about:blank'], { stdio: 'ignore' });
  let tgt;
  for (let i = 0; i < 50 && !tgt; i++) { await sleep(200); try { tgt = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).find((t) => t.type === 'page'); } catch {} }
  const ws = new WebSocket(tgt.webSocketDebuggerUrl);
  await new Promise((r) => ws.addEventListener('open', r));
  let n = 0; const pend = new Map();
  ws.addEventListener('message', (m) => { const d = JSON.parse(m.data); if (d.id && pend.has(d.id)) { pend.get(d.id)(d.result); pend.delete(d.id); } });
  const send = (method, params = {}) => new Promise((r) => { const i = ++n; pend.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
  const ev = async (expression) => (await send('Runtime.evaluate', { expression, returnByValue: true })).result.value;
  await send('Emulation.setDeviceMetricsOverride', { width: 1200, height: 630, deviceScaleFactor: 1, mobile: false });
  await send('Page.enable');
  await send('Page.navigate', { url: 'file://' + __dirname + '/card.html' });
  for (let i = 0; i < 60; i++) { await sleep(250); if (await ev('!!document.body && document.body.hasAttribute("data-ready")')) break; }
  await sleep(400);
  const bad = await ev('document.body.dataset.bad');
  const shot = await send('Page.captureScreenshot', { format: 'jpeg', quality: 90, clip: { x: 0, y: 0, width: 1200, height: 630, scale: 1 } });
  writeFileSync(require('node:path').resolve(__dirname, '../../../assets/share/' + id + '.jpg'), Buffer.from(shot.data, 'base64'));
  console.log('ok', id, bad && bad !== '[]' ? 'OUTSIDE SAFE ZONE ' + bad : 'safe zone ok');
  ws.close(); chrome.kill(); process.exit(0);
})();
