// Shoots assets/previews/the-money-in-the-air.jpg: the top 1200x800 of civic/the-money-in-the-air/index.html at 1200 wide (method copied from stories/php2shell),
// reduced motion, with the hero stamp hidden so the landing card never carries a date line. usage: node preview.mjs
import { spawn } from "node:child_process"
import { writeFileSync } from "node:fs"
import { dirname, resolve } from "node:path"
import { fileURLToPath } from "node:url"
const here = dirname(fileURLToPath(import.meta.url))
const url = "file:///Users/dustinnimmo/DNSC/tools-site/civic/the-money-in-the-air/index.html"
const out = resolve(here, "../../../assets/previews/the-money-in-the-air.jpg")
const port = 9300 + Math.floor(Math.random() * 500)
const chrome = spawn("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  ["--headless=new", "--disable-gpu", "--hide-scrollbars", `--remote-debugging-port=${port}`, `--user-data-dir=/tmp/mitair-prev-${port}`, "about:blank"], { stdio: "ignore" })
const sleep = (ms) => new Promise((r) => setTimeout(r, ms))
let tgt
for (let i = 0; i < 50 && !tgt; i++) { await sleep(200); try { tgt = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).find((t) => t.type === "page") } catch {} }
const ws = new WebSocket(tgt.webSocketDebuggerUrl)
await new Promise((r) => ws.addEventListener("open", r))
let id = 0; const pend = new Map()
ws.addEventListener("message", (m) => { const d = JSON.parse(m.data); if (d.id && pend.has(d.id)) { pend.get(d.id)(d.result); pend.delete(d.id) } })
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pend.set(i, r); ws.send(JSON.stringify({ id: i, method, params })) })
await send("Emulation.setDeviceMetricsOverride", { width: 1200, height: 800, deviceScaleFactor: 1, mobile: false })
await send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-reduced-motion", value: "reduce" }] })
await send("Page.enable")
await send("Page.navigate", { url })
await sleep(4000)
await send("Runtime.evaluate", { expression: "document.querySelector('.stamp').style.visibility='hidden'" })
await sleep(200)
const shot = await send("Page.captureScreenshot", { format: "jpeg", quality: 88, clip: { x: 0, y: 0, width: 1200, height: 800, scale: 1 } })
writeFileSync(out, Buffer.from(shot.data, "base64"))
console.log("ok", out)
ws.close(); chrome.kill(); process.exit(0)
