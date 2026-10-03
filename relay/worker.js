// Lunar Life calendar relay · tools.dnsc.ai
// Fetches a calendar the visitor chooses (an .ics link) and hands it back to
// the Lunar Life page, because browsers block reading most calendar feeds
// directly. It keeps nothing: no logging, no storage, no cookies either way.

const ALLOW_ORIGIN = "https://tools.dnsc.ai";
const MAX_BYTES = 2 * 1024 * 1024; // 2 MB
const TIMEOUT_MS = 10_000;

function cors(extra = {}) {
  return {
    "Access-Control-Allow-Origin": ALLOW_ORIGIN,
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
    "Vary": "Origin",
    ...extra,
  };
}

function fail(status, message) {
  return new Response(message, {
    status,
    headers: cors({ "Content-Type": "text/plain; charset=utf-8", "Cache-Control": "no-store" }),
  });
}

function isPrivateHost(host) {
  const h = host.toLowerCase();
  if (h === "localhost" || h.endsWith(".localhost") || h.endsWith(".local") || h.endsWith(".internal")) return true;
  // literal IPs: block loopback, private, link-local and similar ranges
  if (/^\d+\.\d+\.\d+\.\d+$/.test(h)) {
    const [a, b] = h.split(".").map(Number);
    return a === 10 || a === 127 || a === 0 || (a === 169 && b === 254) || (a === 172 && b >= 16 && b <= 31) || (a === 192 && b === 168) || a >= 224;
  }
  if (h.startsWith("[")) return true; // no IPv6 literals
  return false;
}

export default {
  async fetch(request) {
    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: cors() });
    if (request.method !== "GET") return fail(405, "Only GET.");

    const origin = request.headers.get("Origin");
    if (origin && origin !== ALLOW_ORIGIN) return fail(403, "This relay only serves tools.dnsc.ai.");

    const raw = new URL(request.url).searchParams.get("url");
    if (!raw) return fail(400, "Add ?url= with your calendar's .ics link.");

    let target;
    try {
      // calendar apps hand out webcal:// links; they are https underneath
      target = new URL(raw.replace(/^webcal:\/\//i, "https://"));
    } catch {
      return fail(400, "That doesn't look like a link.");
    }
    if (target.protocol !== "https:") return fail(400, "Only https calendar links.");
    if (target.username || target.password) return fail(400, "Links with passwords in them aren't allowed.");
    if (isPrivateHost(target.hostname)) return fail(400, "That address isn't reachable from here.");

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
    let upstream;
    try {
      upstream = await fetch(target.toString(), {
        method: "GET",
        redirect: "follow",
        signal: controller.signal,
        headers: { "Accept": "text/calendar, text/plain;q=0.5", "User-Agent": "LunarLife-relay (tools.dnsc.ai)" },
        // no cookies or credentials are forwarded; the visitor's request headers are not passed along
      });
    } catch (e) {
      clearTimeout(timer);
      return fail(504, e && e.name === "AbortError" ? "The calendar took too long to answer." : "Couldn't reach that calendar.");
    }

    if (!upstream.ok) { clearTimeout(timer); return fail(502, `The calendar answered ${upstream.status}.`); }
    if (new URL(upstream.url).protocol !== "https:") { clearTimeout(timer); return fail(400, "The calendar redirected away from https."); }

    const declared = Number(upstream.headers.get("Content-Length") || 0);
    if (declared > MAX_BYTES) { clearTimeout(timer); return fail(413, "That calendar is larger than 2 MB."); }

    // read with a hard cap, whatever the server claims
    const reader = upstream.body.getReader();
    const chunks = [];
    let total = 0;
    try {
      for (;;) {
        const { done, value } = await reader.read();
        if (done) break;
        total += value.byteLength;
        if (total > MAX_BYTES) { await reader.cancel(); return fail(413, "That calendar is larger than 2 MB."); }
        chunks.push(value);
      }
    } catch {
      return fail(504, "The calendar took too long to answer.");
    } finally {
      clearTimeout(timer);
    }

    const body = new Uint8Array(total);
    let off = 0;
    for (const c of chunks) { body.set(c, off); off += c.byteLength; }

    // only pass through things that are actually calendars
    const head = new TextDecoder().decode(body.slice(0, 2048)).replace(/^﻿/, "").trimStart();
    if (!head.toUpperCase().startsWith("BEGIN:VCALENDAR")) return fail(415, "That link isn't a calendar (.ics) file.");

    return new Response(body, {
      status: 200,
      headers: cors({
        "Content-Type": "text/calendar; charset=utf-8",
        "Cache-Control": "no-store",
        "X-Content-Type-Options": "nosniff",
      }),
    });
  },
};
