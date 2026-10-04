// The Well · daily board for One Word. Anonymous and opt-in.
// Names are generated on the page from two fixed lists and this worker accepts only those pairs, so nothing typed can reach the board.
// A score counts only if every row is a real guess of the right length and the last row is the day's word.
// Storage: one KV key per edition per day, holding at most 500 entries. Device ids and IPs are hashed and never shown.
// Bind a KV namespace as BOARD. Observability stays off.

const WORDS = __WORDS__;
const ORIGINS = ["https://tools.dnsc.ai", "https://www.tools.dnsc.ai", "http://localhost:8000", "http://127.0.0.1:8000"];
const ED = { regular: { L: 5, T: 6 }, advanced: { L: 7, T: 7 } };
const EPOCH = Date.UTC(2026, 9, 2);
const SHOW = 20, CAP = 500, PER_IP = 3;

function cors(req) {
  const o = req.headers.get("Origin") || "";
  return {
    "Access-Control-Allow-Origin": ORIGINS.includes(o) ? o : ORIGINS[0],
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Vary": "Origin",
  };
}
function json(req, body, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json", "Cache-Control": "no-store", ...cors(req) } });
}
function answer(ed, day) { const b = WORDS[ed]; return b[((day % b.length) + b.length) % b.length]; }
function serverDay() { return Math.floor((Date.now() - EPOCH) / 864e5); }
async function hash(s) {
  const d = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return [...new Uint8Array(d)].slice(0, 12).map((x) => x.toString(16).padStart(2, "0")).join("");
}
function rank(a, b) { return a.guesses - b.guesses || a.ms - b.ms || a.at - b.at; }
function pub(rows) { return rows.slice(0, SHOW).map((r) => ({ name: r.name, guesses: r.guesses, ms: r.ms })); }

export default {
  async fetch(req, env) {
    if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors(req) });
    const url = new URL(req.url);
    const today = serverDay();

    if (req.method === "GET" && url.pathname === "/board") {
      const ed = url.searchParams.get("ed"), day = parseInt(url.searchParams.get("day"), 10);
      if (!ED[ed] || !Number.isInteger(day) || Math.abs(day - today) > 1) return json(req, { error: "Unknown board." }, 400);
      const rows = (await env.BOARD.get(`b:${ed}:${day}`, "json")) || [];
      return json(req, { rows: pub(rows) });
    }

    if (req.method === "POST" && url.pathname === "/submit") {
      const o = ORIGINS.includes(req.headers.get("Origin") || "");
      if (!o) return json(req, { error: "Not from The Well." }, 403);
      let b; try { b = await req.json(); } catch (e) { return json(req, { error: "That didn't go through. Try again." }, 400); }
      const { ed, day, rows, ms, name, device } = b || {};
      const cfg = ED[ed];
      if (!cfg || !Number.isInteger(day) || Math.abs(day - today) > 1) return json(req, { error: "That board is closed." }, 400);
      const re = new RegExp(`^[A-Z]{${cfg.L}}$`), w = answer(ed, day);
      if (!Array.isArray(rows) || rows.length < 1 || rows.length > cfg.T || !rows.every((r) => typeof r === "string" && re.test(r)))
        return json(req, { error: "Those rows don't fit today's game." }, 400);
      if (rows[rows.length - 1] !== w || rows.slice(0, -1).includes(w)) return json(req, { error: "Only solved games go on the board." }, 400);
      const parts = typeof name === "string" ? name.split(" ") : [];
      if (parts.length !== 2 || !WORDS.A.includes(parts[0]) || !WORDS.N.includes(parts[1])) return json(req, { error: "Pick a name with the new name button." }, 400);
      if (typeof device !== "string" || device.length < 6 || device.length > 80) return json(req, { error: "That didn't go through. Try again." }, 400);
      const t = Math.max(0, Math.min(Number(ms) || 0, 86400000));

      const key = `b:${ed}:${day}`;
      const list = (await env.BOARD.get(key, "json")) || [];
      const dev = await hash("d|" + device), ip = await hash(`i|${day}|` + (req.headers.get("CF-Connecting-IP") || ""));
      if (list.some((r) => r.dev === dev)) return json(req, { error: "You're already on today's board.", rows: pub(list) }, 409);
      if (list.filter((r) => r.ip === ip).length >= PER_IP) return json(req, { error: "This connection has added enough scores today." }, 429);
      if (list.some((r) => r.name === name)) return json(req, { error: "That name is taken today. Tap new name and try again." }, 409);
      list.push({ name, guesses: rows.length, ms: t, at: Date.now(), dev, ip });
      list.sort(rank);
      await env.BOARD.put(key, JSON.stringify(list.slice(0, CAP)), { expirationTtl: 60 * 60 * 24 * 4 });
      return json(req, { rows: pub(list) });
    }

    return json(req, { error: "Not here." }, 404);
  },
};
