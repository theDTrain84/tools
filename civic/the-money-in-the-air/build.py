#!/usr/bin/env python3
"""Build civic/the-money-in-the-air/index.html from src.html + data.json.

Thursday refresh: edit data.json, then run  python3 build.py  in this folder.
Everything with a number on the page (the copy, the charts, the flows, the House
picker, the source list) is rendered here from data.json, and data.json itself is
inlined into the page as <script type="application/json" id="record">.

Template tokens in src.html (and in any text inside data.json):
  {{path.to.figure}}        the figure's display text (its "display", else formatted dollars)
  {{path.to.figure|short}}  short form: $68.7M
  {{path.to.count|n}}       a plain count with commas: 67
  {{date:path}}             a date field as "October 15, 2026"
  [[c:id,id2]]              citation links; numbered in order of first use
  <!--@name-->              a generated block (see BLOCKS)
"""
import html
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(HERE, "data.json"), encoding="utf-8"))
SRC = open(os.path.join(HERE, "src.html"), encoding="utf-8").read()

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
MON3 = ["Jan.", "Feb.", "March", "April", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
REFRESH = "Refresh Thursday"


# ---------- formatting ----------
def esc(s):
    return html.escape(str(s), quote=False)


def attr(s):
    return html.escape(str(s), quote=True)


def num1(x):
    s = f"{x:.1f}"
    return s[:-2] if s.endswith(".0") else s


def money(v, short=False):
    if v is None:
        return "not reported"
    v = float(v)
    if v >= 1e9:
        return f"${num1(v / 1e9)}{'B' if short else ' billion'}"
    if v >= 1e6:
        x = v / 1e6
        return f"${num1(x)}{'M' if short else ' million'}"
    if short and v >= 1e5:
        return f"${v / 1e3:,.0f}K"
    return f"${v:,.0f}"


def fig(o, short=False):
    if isinstance(o, dict):
        if not short and o.get("display"):
            return o["display"]
        return money(o.get("v"), short)
    if isinstance(o, (int, float)):
        return money(o, short)
    return str(o)


def ymd(d):
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", d or "")
    return (int(m[1]), int(m[2]), int(m[3])) if m else None


def longdate(d):
    t = ymd(d)
    return f"{MONTHS[t[1] - 1]} {t[2]}, {t[0]}" if t else ""


def shortdate(d, year=False):
    t = ymd(d)
    if not t:
        return ""
    s = f"{MON3[t[1] - 1]} {t[2]}"
    return s + (f", {t[0]}" if year else "")


def dayno(d):
    import datetime
    t = ymd(d)
    return datetime.date(*t).toordinal()


def lookup(path):
    cur = DATA
    for p in path.split("."):
        if isinstance(cur, list):
            cur = cur[int(p)]
        else:
            cur = cur[p]
    return cur


def text(s):
    """Data text to HTML: escaped, tokens kept for the final pass."""
    return esc(s or "")


def cites(ids):
    return "".join(f"[[c:{i}]]" for i in (ids or []))


def reported(o):
    return ' <span class="tag">reported</span>' if isinstance(o, dict) and o.get("tag") == "REPORTED" else ""


def wrap(s, n):
    words, lines, cur = s.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > n:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


SIDE = {"r": "var(--r)", "d": "var(--d)", "": "var(--mute)"}


# ---------- the Senate line, three elections ----------
def senate_line(W, H, narrow):
    cyc = DATA["senate"]["cycles"]
    res = cyc[-1].get("reserved") or {}
    top = 600e6
    ml, mr, mt, mb = (46, 18, 34, 54) if narrow else (64, 150, 34, 54)
    pw, ph = W - ml - mr, H - mt - mb
    xs = [ml + pw * (i + .5) / len(cyc) for i in range(len(cyc))]
    y = lambda v: mt + ph * (1 - v / top)
    o = [f'<svg class="chart line {"narrow" if narrow else "wide"}" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="AdImpact general-election Senate advertising in Ohio: '
         + "; ".join(f'{c["label"]} {fig(c)}' for c in cyc)
         + (f'; of the 2026 count, {fig(res)} reserved as of {shortdate(res["through"])}' if res else "") + '">']
    for g in range(0, 601, 100):
        gy = y(g * 1e6)
        o.append(f'<line class="grid" x1="{ml}" x2="{W - mr + (0 if narrow else 120)}" y1="{gy:.1f}" y2="{gy:.1f}"/>')
        o.append(f'<text class="ax" x="{ml - 8}" y="{gy + 4:.1f}" text-anchor="end">{"$" + str(g) + "M" if g else "$0"}</text>')
    pts = [(xs[i], y(c["v"])) for i, c in enumerate(cyc)]
    o.append('<path class="ln draw-p" d="M' + " L".join(f"{a:.1f},{b:.1f}" for a, b in pts) + '"/>')
    if res and res.get("v"):
        # the reserved time is part of AdImpact's count, so it is drawn inside the 2026 figure, never above it
        x2, y1, y2 = pts[-1][0] + (14 if narrow else -12), pts[-1][1], y(cyc[-1]["v"] - res["v"])
        o.append(f'<path class="ld" d="M{x2:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}"/>')
        o.append(f'<path class="ld" d="M{x2 - 4:.1f},{y1:.1f} L{x2 + 4:.1f},{y1:.1f} M{x2 - 4:.1f},{y2:.1f} L{x2 + 4:.1f},{y2:.1f}"/>')
    for i, c in enumerate(cyc):
        cx, cy = pts[i]
        o.append(f'<circle class="pt" cx="{cx:.1f}" cy="{cy:.1f}" r="6"/>')
        last = i == len(cyc) - 1
        lab = money(c["v"], True if narrow else False).replace(" million", "M")
        if i == 0:
            tx, ty, anc = cx + 10, cy + 20, "start"
        elif not last:
            tx, ty, anc = cx, cy - 14, "middle"
        else:
            tx, ty, anc = (cx + 6, cy + 24, "end") if narrow else (cx + 14, cy + 24, "start")
        o.append(f'<text class="lab" x="{tx:.1f}" y="{ty:.1f}" text-anchor="{anc}">{esc(lab)}</text>')
        if last:
            o.append(f'<text class="lab s dim" x="{tx:.1f}" y="{ty + 15:.1f}" text-anchor="{anc}">by {shortdate(c["through"])}</text>')
            if res and res.get("v"):
                rl = esc(fig(res).replace(" million", "M")) if narrow else esc(fig(res))
                o.append(f'<text class="lab s" x="{tx:.1f}" y="{ty + 36:.1f}" text-anchor="{anc}">of it, {rl}</text>')
                o.append(f'<text class="lab s dim" x="{tx:.1f}" y="{ty + 50:.1f}" text-anchor="{anc}">reserved, as of {shortdate(res["through"])}</text>')
        o.append(f'<text class="yr" x="{cx:.1f}" y="{H - 30}" text-anchor="middle">{c["label"]}</text>')
        if not narrow:
            o.append(f'<text class="ax" x="{cx:.1f}" y="{H - 13}" text-anchor="middle">{esc(c["race"])}</text>')
    o.append("</svg>")
    return "".join(o)


def block_senate_line():
    cyc = DATA["senate"]["cycles"]
    out = ['<div class="chartbox">', senate_line(640, 340, False), senate_line(360, 330, True), "</div>"]
    out.append('<div class="bought3">')
    for c in cyc:
        out.append(f'<div><b>{c["label"]}</b><span class="fv">{esc(fig(c))}{reported(c)} {cites(c["src"])}</span>'
                   f'<p class="nt">{text(c.get("note"))}</p>'
                   f'<p class="bl"><i>What it bought.</i> {text(c.get("bought"))}</p></div>')
    out.append("</div>")
    return "".join(out)


def block_growth():
    rows = "".join(f'<li><time datetime="{g["date"]}">{shortdate(g["date"])}</time><span>{text(g["text"])} {cites(g["src"])}</span></li>'
                   for g in DATA["senate"]["growth"])
    return f'<ol class="days small">{rows}</ol>'


# ---------- the governor's race beside it ----------
def block_gov_bars():
    a = DATA["governor"]["adimpact"]
    mx = max(a[k]["aired"] + a[k]["reserved"] for k in ("r", "d"))
    out = ['<div class="gbars">']
    for k in ("r", "d"):
        s = a[k]
        tot = s["aired"] + s["reserved"]
        wa, wr = 100 * s["aired"] / mx, 100 * s["reserved"] / mx
        out.append(f'<div class="gb"><div class="gl"><b>{esc(s["label"])}</b><span>{esc(money(tot))} aired or reserved</span></div>'
                   f'<div class="track"><i class="grow" style="width:{wa:.2f}%;background:{SIDE[k]}"></i>'
                   f'<i class="grow hatch" style="width:{wr:.2f}%;color:{SIDE[k]}"></i></div>'
                   f'<div class="gv"><span>aired {esc(money(s["aired"]))}</span><span>reserved {esc(money(s["reserved"]))}</span></div></div>')
    out.append(f'</div><p class="fn">AdImpact, as of {shortdate(a["through"], True)}, as cited by the Ohio Capital Journal on {shortdate(a["date"])}. {cites(a["src"])}</p>')
    return "".join(out)


# ---------- the week ----------
def block_week():
    rows = []
    for w in DATA["week"]:
        cls = ' class="hit"' if w.get("hit") else ""
        rows.append(f'<li{cls}><time datetime="{w["date"]}">{shortdate(w["date"])}</time><span>{text(w["text"])} {cites(w["src"])}</span></li>')
    return '<ol class="days">' + "".join(rows) + "</ol>"


# ---------- flows: who pays, and who funds them ----------
def all_flow_payers():
    for f in ("senate", "governor"):
        for s in DATA["flows"][f]["sides"]:
            for p in s["payers"]:
                yield s, p


def fill_others():
    for s in DATA["flows"]["senate"]["sides"]:
        named = sum(p["v"] for p in s["payers"] if p.get("v") and not p.get("campaign") and not p.get("other"))
        for p in s["payers"]:
            if p.get("other"):
                p["v"] = max(0, s["total"]["outside"] - named)


fill_others()
PAY_MAX = max(p["v"] or 0 for _, p in all_flow_payers())
GIFT_MAX = max([f["v"] for _, p in all_flow_payers() for f in p.get("funders", [])] + [b["v"] for _, p in all_flow_payers() for f in p.get("funders", []) for b in f.get("behind", [])])
S_WIDE = 520 / max(s["total"]["outside"] + s["total"]["campaign"] for s in DATA["flows"]["senate"]["sides"])


BROW = 24


def frow_h(f):
    return 30 + (14 * len(wrap(f["sub"], 52)) + 4 if f.get("sub") else 0)


def behind_h(f):
    b = f.get("behind") or []
    return (22 + sum(BROW + (14 if x.get("sub") else 0) for x in b) + 6) if b else 0


def behind_wide(f, FX, FW, fy):
    """Second-level donors, indented under the funder they gave to, with a bracket up to it."""
    o, x0, y = [], FX + 22, fy + 4
    o.append(f'<text class="fl" x="{x0}" y="{y + 10:.1f}">{esc(f.get("behind_label", ""))}</text>')
    y += 22
    top = y
    for b in f["behind"]:
        if b.get("nd"):
            o.append(f'<rect class="nd" x="{x0}" y="{y - 1:.1f}" width="{FW - 22}" height="{BROW + 12:.0f}"/>')
        o.append(f'<text class="fnm s" x="{x0 + 6}" y="{y + 11:.1f}">{esc(b["name"])}</text>')
        o.append(f'<text class="fam s" x="{FX + FW - 4}" y="{y + 11:.1f}" text-anchor="end">{esc(fig(b, True))}</text>')
        if not b.get("nd"):
            o.append(f'<rect class="gift" x="{x0 + 6}" y="{y + 15:.1f}" width="{max(2, (FW - 32) * b["v"] / GIFT_MAX):.1f}" height="3"/>')
        y += BROW
        if b.get("sub"):
            o.append(f'<text class="fsub" x="{x0 + 6}" y="{y + 6:.1f}">{esc(b["sub"])}</text>')
            y += 14
    o.append(f'<path class="con" d="M{FX + 8},{fy - 6:.1f} L{FX + 8},{y - 8:.1f}"/>')
    o.append(f'<path class="con" d="M{FX + 4},{fy:.1f} L{FX + 8},{fy - 7:.1f} L{FX + 12},{fy:.1f}"/>')
    return "".join(o)


def behind_narrow(f, W, y):
    parts = [f'<text class="fl" x="32" y="{y + 10}">{esc(f.get("behind_label", ""))}</text>']
    y += 18
    y0 = y
    for b in f["behind"]:
        if b.get("nd"):
            parts.append(f'<rect class="nd" x="32" y="{y - 2}" width="{W - 32}" height="{38 if b.get("sub") else 22}"/>')
        parts.append(f'<text class="fnm s" x="38" y="{y + 11}">{esc(b["name"])}</text>')
        parts.append(f'<text class="fam s" x="{W - 4}" y="{y + 11}" text-anchor="end">{esc(fig(b, True))}</text>')
        y += 22
        if b.get("sub"):
            parts.append(f'<text class="fsub" x="38" y="{y + 6}">{esc(b["sub"])}</text>')
            y += 16
    parts.append(f'<path class="con" d="M22,{y0 - 4} L22,{y - 4}"/><path class="con" d="M18,{y0} L22,{y0 - 6} L26,{y0}"/>')
    return "".join(parts), y + 4


def funders_label(p):
    if p.get("funders_label"):
        return p["funders_label"]
    if p.get("funders_through"):
        return f"gave the committee, all races, this cycle, through {shortdate(p['funders_through'])}"
    return ""


def flow_wide(side, scale):
    W = 1000
    FX, FW = 0, 330          # funders column
    BX, BW = 452, 250        # payer box (height = Ohio money)
    RX = BX + BW             # ribbons start at the box's right edge
    SX, SWD = 872, 16        # sink
    ROWF, ROWFS = 30, 44
    rows, y = [], 26
    for p in side["payers"]:
        h = max(3.0, (p["v"] or 0) * scale)
        fs = p.get("funders", [])
        fh = (sum(frow_h(f) + behind_h(f) for f in fs) + 14) if fs else (40 if p.get("nd") else 0)
        nl = wrap(p["name"], 28)
        lh = 18 * len(nl) + 26 + (15 if p.get("short") else 0)
        rh = max(h, fh, lh) + (30 if p.get("campaign") else 16)
        rows.append((p, h, fs, nl, y, rh))
        y += rh
    H = y + 6
    total = sum(r[1] for r in rows)
    sy0 = max(26, (H - total) / 2)
    o = [f'<svg class="flow wide" viewBox="0 0 {W} {H:.0f}" role="img" aria-label="{attr(side["label"])}: who paid and who funds them">']
    o.append(f'<text class="hd" x="{FX}" y="12">Who gave them money</text>')
    o.append(f'<text class="hd" x="{BX}" y="12">Who paid for the ads</text>')
    o.append(f'<text class="hd" x="{SX + SWD}" y="12" text-anchor="end">In Ohio</text>')
    sy = sy0
    for p, h, fs, nl, ry, rh in rows:
        col = "var(--mute)" if p.get("other") else SIDE[side["key"]]
        by = ry + 6
        if p.get("campaign"):
            o.append(f'<line class="sep" x1="{FX}" x2="{RX}" y1="{ry - 4:.1f}" y2="{ry - 4:.1f}"/>')
            by += 12
        bc = by + min(h, 30) / 2
        x0, x1 = RX, SX
        o.append(f'<path class="rib" style="fill:{col}" d="M{x0},{by:.1f} C{(x0 + x1) / 2},{by:.1f} {(x0 + x1) / 2},{sy:.1f} {x1},{sy:.1f} '
                 f'L{x1},{sy + h:.1f} C{(x0 + x1) / 2},{sy + h:.1f} {(x0 + x1) / 2},{by + h:.1f} {x0},{by + h:.1f} Z"/>')
        sy += h
        cls = "pbox camp" if p.get("campaign") else "pbox"
        o.append(f'<rect class="{cls}" x="{BX}" y="{by:.1f}" width="{BW}" height="{h:.1f}" style="fill:{col}"/>')
        o.append(f'<rect class="pedge" x="{BX}" y="{by:.1f}" width="4" height="{max(h, 3):.1f}" style="fill:{col}"/>')
        ty = by + 15
        for i, line in enumerate(nl):
            o.append(f'<text class="pn" x="{BX + 12}" y="{ty + 18 * i:.1f}">{esc(line)}</text>')
        ty += 18 * (len(nl) - 1) + 17
        tail = f" · {p['kind']}" if p.get("kind") else ""
        o.append(f'<text class="pv" x="{BX + 12}" y="{ty:.1f}"><tspan class="amt">{esc(fig(p, True))}</tspan>{esc(tail)}</text>')
        if p.get("short"):
            o.append(f'<text class="psh" x="{BX + 12}" y="{ty + 15:.1f}">{esc(p["short"])}</text>')
        fy = by
        if fs:
            n = len(fs)
            for k, f in enumerate(fs):
                rh_f = frow_h(f)
                o.append(f'<text class="fnm" x="{FX}" y="{fy + 12:.1f}">{esc(f["name"])}</text>')
                o.append(f'<text class="fam" x="{FX + FW}" y="{fy + 12:.1f}" text-anchor="end">{esc(fig(f, True))}</text>')
                bw = max(2, FW * f["v"] / GIFT_MAX)
                o.append(f'<rect class="gift" x="{FX}" y="{fy + 17:.1f}" width="{bw:.1f}" height="4"/>')
                for i_, ln in enumerate(wrap(f.get("sub") or "", 52)):
                    o.append(f'<text class="fsub" x="{FX}" y="{fy + 35 + 14 * i_:.1f}">{esc(ln)}</text>')
                ty2 = by + 6 + min(h, 60) * (k + .5) / n
                o.append(f'<path class="con" d="M{FX + FW + 8},{fy + 18:.1f} C{(FX + FW + BX) / 2 + 20},{fy + 18:.1f} {(FX + FW + BX) / 2 - 10},{ty2:.1f} {BX - 3},{ty2:.1f}"/>')
                fy += rh_f
                if f.get("behind"):
                    o.append(behind_wide(f, FX, FW, fy))
                    fy += behind_h(f)
            o.append(f'<text class="fl" x="{FX}" y="{fy + 4:.1f}">{esc(funders_label(p))}</text>')
        elif p.get("nd"):
            o.append(f'<rect class="nd" x="{FX + FW - 150}" y="{by:.1f}" width="150" height="30"/>')
            o.append(f'<text class="ndt" x="{FX + FW - 75}" y="{by + 19:.1f}" text-anchor="middle">not disclosed</text>')
            o.append(f'<path class="con dash" d="M{FX + FW + 8},{by + 15:.1f} C{(FX + FW + BX) / 2},{by + 15:.1f} {(FX + FW + BX) / 2},{bc:.1f} {BX - 3},{bc:.1f}"/>')
    o.append(f'<rect class="sink" x="{SX}" y="{sy0:.1f}" width="{SWD}" height="{total:.1f}" style="fill:{SIDE[side["key"]]}"/>')
    t = side.get("total")
    lx, ly = SX + SWD + 8, sy0 + 16
    if t:
        o.append(f'<text class="sv" x="{lx}" y="{ly:.1f}">{esc(money(t["outside"] + t["campaign"], True))}</text>')
        o.append(f'<text class="ss" x="{lx}" y="{ly + 16:.1f}">outside</text><text class="ss" x="{lx}" y="{ly + 29:.1f}">{esc(money(t["outside"], True))}</text>')
        o.append(f'<text class="ss" x="{lx}" y="{ly + 45:.1f}">campaign</text><text class="ss" x="{lx}" y="{ly + 58:.1f}">{esc(money(t["campaign"], True))}</text>')
        if t.get("planned"):
            o.append(f'<text class="ss" x="{lx}" y="{ly + 74:.1f}">planned, not</text><text class="ss" x="{lx}" y="{ly + 87:.1f}">counted: {esc(money(t["planned"], True))}</text>')
        o[0] = f'<svg class="flow wide" viewBox="0 0 {W} {H:.0f}" role="img" aria-label="{attr(side["label"])}: who paid and who funds them">'
    o.append("</svg>")
    return "".join(o)


def flow_narrow(side, scale_unused=None):
    W = 360
    o_rows, y = [], 4
    parts = []
    for p in side["payers"]:
        col = "var(--mute)" if p.get("other") else SIDE[side["key"]]
        if p.get("campaign"):
            parts.append(f'<line class="sep" x1="0" x2="{W}" y1="{y + 4}" y2="{y + 4}"/>')
            y += 14
        fs = p.get("funders", [])
        # funders first, flowing down into the payer
        fy0 = y
        for f in fs:
            parts.append(f'<text class="fnm" x="16" y="{y + 12}">{esc(f["name"])}</text>')
            parts.append(f'<text class="fam" x="{W}" y="{y + 12}" text-anchor="end">{esc(fig(f, True))}</text>')
            bw = max(2, (W - 16) * f["v"] / GIFT_MAX)
            parts.append(f'<rect class="gift" x="16" y="{y + 17}" width="{bw:.1f}" height="4"/>')
            parts.append(f'<path class="con" d="M5,{y + 8} L13,{y + 8}"/>')
            y += 28
            if f.get("sub"):
                for ln in wrap(f["sub"], 50):
                    parts.append(f'<text class="fsub" x="16" y="{y + 4}">{esc(ln)}</text>')
                    y += 14
                y += 4
            if f.get("behind"):
                bh, y = behind_narrow(f, W, y)
                parts.append(bh)
        if not fs and p.get("nd"):
            parts.append(f'<rect class="nd" x="16" y="{y}" width="130" height="26"/>')
            parts.append(f'<text class="ndt" x="81" y="{y + 17}" text-anchor="middle">not disclosed</text>')
            parts.append(f'<path class="con" d="M5,{y + 13} L13,{y + 13}"/>')
            y += 34
        if fs and funders_label(p):
            for ln in wrap(funders_label(p), 48):
                parts.append(f'<text class="fl" x="16" y="{y + 6}">{esc(ln)}</text>')
                y += 13
            y += 2
        if fs or p.get("nd"):
            parts.append(f'<path class="con" d="M5,{fy0 + 4} L5,{y + 6}"/>')
            parts.append(f'<path class="con" d="M1,{y + 1} L5,{y + 7} L9,{y + 1}"/>')
            y += 8
        # the payer: a bar whose length is its Ohio money
        bw = max(3, W * (p["v"] or 0) / PAY_MAX)
        nl = wrap(p["name"], 30)
        for i, ln in enumerate(nl):
            parts.append(f'<text class="pn" x="0" y="{y + 14 + 17 * i}">{esc(ln)}</text>')
        parts.append(f'<text class="pv amt" x="{W}" y="{y + 14}" text-anchor="end">{esc(fig(p, True))}</text>')
        y += 17 * len(nl) + 2
        if p.get("kind"):
            parts.append(f'<text class="pv" x="0" y="{y + 10}">{esc(p["kind"])}</text>')
            y += 15
        if p.get("short"):
            parts.append(f'<text class="psh" x="0" y="{y + 10}">{esc(p["short"])}</text>')
            y += 15
        parts.append(f'<rect class="pbar{" camp" if p.get("campaign") else ""}" x="0" y="{y}" width="{bw:.1f}" height="12" style="fill:{col}"/>')
        y += 30
    t = side.get("total")
    if t:
        parts.append(f'<line class="sep strong" x1="0" x2="{W}" y1="{y}" y2="{y}"/>')
        parts.append(f'<text class="sk" x="0" y="{y + 20}">{esc(side["label"])}, in Ohio</text>')
        parts.append(f'<text class="sv" x="{W}" y="{y + 21}" text-anchor="end">{esc(money(t["outside"] + t["campaign"], True))}</text>')
        parts.append(f'<text class="ss" x="0" y="{y + 38}">outside {esc(money(t["outside"], True))} · campaign {esc(money(t["campaign"], True))}</text>')
        y += 46
        if t.get("planned"):
            parts.append(f'<text class="ss" x="0" y="{y + 6}">planned, not counted: {esc(money(t["planned"], True))}</text>')
            y += 16
    return f'<svg class="flow narrow" viewBox="0 0 {W} {y + 4}" role="img" aria-label="{attr(side["label"])}: who paid and who funds them">' + "".join(parts) + "</svg>"


def flow_notes(side):
    notes = []
    for p in side["payers"]:
        bits = []
        if p.get("label"):
            bits.append("<i>" + text(p["label"]) + "</i> " + cites(p.get("label_src")))
        if p.get("note"):
            bits.append(text(p["note"]))
        if p.get("nd_note"):
            bits.append(text(p["nd_note"]))
        if p.get("bought"):
            bits.append("<i>What it bought.</i> " + text(p["bought"]))
        if not bits:
            continue
        used = set(re.findall(r"\[\[c:([^\]]+)\]\]", " ".join(bits)))
        src = cites([i for i in dict.fromkeys(p.get("src", []) + [s for f in p.get("funders", []) for s in f.get("src", [])]) if i not in used])
        notes.append(f'<li><b>{esc(p["name"])}</b>, {esc(fig(p))}{reported(p)}. {" ".join(bits)} {src}</li>')
    return '<ul class="pnotes">' + "".join(notes) + "</ul>" if notes else ""


def block_flow(which):
    F = DATA["flows"][which]
    out = []
    for s in F["sides"]:
        out.append(f'<div class="flowbox side-{s["key"]}"><h3 class="fh"><span class="sw" style="background:{SIDE[s["key"]]}"></span>{esc(s["label"])}'
                   + (f' <small>{esc(s["sub"])}</small>' if s.get("sub") else "") + "</h3>")
        out.append(flow_wide(s, S_WIDE))
        out.append(flow_narrow(s))
        out.append(flow_notes(s))
        out.append("</div>")
    out.append(f'<p class="fn">{text(F["unit_note"])} Bars on the left: what each funder gave, on one scale. Bars in the middle: what each committee spent in this race, on one scale for both races, Senate and governor. The italic label under each committee names its kind and its funders, from its filings or from the outlet named. {cites(F["src"])}</p>')
    if F.get("also"):
        out.append(f'<p class="note">{text(F["also"])}</p>')
    return "".join(out)


# ---------- the House ----------
H = DATA["house"]
PLAB = H.get("payer_labels") or {}
DIST = {d["n"]: d for d in H["districts"]}
ORD = {1: "1st", 2: "2nd", 3: "3rd"}


def ordn(n):
    return ORD.get(n, f"{n}th")


def dname(d):
    return f"Ohio's {ordn(d['n'])}"


def pending(d):
    return d.get("status") == "refresh"


def cand_line(d):
    if not (d.get("r") or d.get("d")):
        return f'<span class="pend">Candidates: {REFRESH}</span>'
    a = []
    for k in ("r", "d"):
        if d.get(k):
            inc = ", incumbent" if d.get("inc") == k else ""
            a.append(f'<span class="c{k}">{esc(d[k])} ({k.upper()}{inc})</span>')
    s = " vs. ".join(a)
    if d.get("others"):
        s += f' <span class="dim">· {esc(d["others"])}</span>'
    return s


def cand_total(d):
    return sum(c["v"] or 0 for c in d.get("cand") or [])


def block_house_pinned():
    pins = [DIST[n] for n in H["pinned"]]
    mx = max((d.get("outside") or {}).get("v") or 0 for d in pins) or 1
    out = ['<div class="pins">']
    for d in pins:
        o = d.get("outside")
        if pending(d) or not o:
            out.append(f'<div class="pin pend-card"><p class="pk">{dname(d)}</p><p class="pc">{cand_line(d)}</p>'
                       f'<p class="pbig dim">{REFRESH}</p></div>')
            continue
        w = 100 * o["v"] / mx
        mg = f'<p class="psub">2024 margin: {esc(d["margin"])}, old lines</p>' if d.get("margin") else ""
        out.append(f'<a class="pin" href="#oh{d["n"]:02d}" data-n="{d["n"]}"><p class="pk">{dname(d)}</p><p class="pc">{cand_line(d)}</p>'
                   f'<p class="pbig">{esc(fig(o))}</p><p class="psub">outside money, rows through {shortdate(o["through"])}</p>'
                   f'<div class="track thin"><i class="grow" style="width:{max(w, .4):.3f}%"></i></div>'
                   f'<p class="psub">candidates raised {esc(money(cand_total(d), True))} (FEC summaries)</p>{mg}</a>')
    out.append("</div>")
    return "".join(out)


def block_house_rank():
    ds = sorted(H["districts"], key=lambda d: -(cand_total(d) + ((d.get("outside") or {}).get("v") or 0)))
    mx = max(cand_total(d) + ((d.get("outside") or {}).get("v") or 0) for d in ds) or 1
    rows = []
    for d in ds:
        o = d.get("outside")
        pin = " pinned" if d["n"] in H["pinned"] else ""
        if pending(d) or not o:
            rows.append(f'<li class="rk pend{pin}"><span class="rn">{ordn(d["n"])}</span><span class="rb"><i class="dash"></i></span><span class="rv">{REFRESH}</span></li>')
            continue
        c, ov = cand_total(d), o["v"]
        rows.append(f'<li class="rk{pin}"><a href="#oh{d["n"]:02d}" data-n="{d["n"]}" class="rn">{ordn(d["n"])}</a>'
                    f'<span class="rb"><i class="grow out" style="width:{max(100 * ov / mx, .15):.3f}%"></i><i class="grow cand" style="width:{max(100 * c / mx, .15):.3f}%"></i></span>'
                    f'<span class="rv"><b>{esc(money(c + ov, True))}</b> <span>outside {esc(money(ov, True))}</span></span></li>')
    t = H.get("totals") or {}
    leg = ('<p class="leg"><span><i style="background:var(--ink)"></i>outside money</span>'
           '<span><i style="background:var(--sky)"></i>raised by the candidates</span></p>')
    foot = (f'<p class="fn">All fifteen: candidates raised {esc(money(t["cand"]))} {esc(t.get("cand_label", "through Sept. 30"))} and spent {esc(money(t["cand_spent"]))} {cites(["fec-webl26"])}; outside groups reported {esc(money(t["outside"]))} {esc(t.get("outside_label", "through Oct. 20"))}. '
            f'Five races, the {", ".join(ordn(n) for n in t["five"][:-1])} and {ordn(t["five"][-1])}, hold {esc(t["five_share"])} of the outside money. '
            + cites([f"fec-oh{n:02d}" for n in t["five"]]) + "</p>") if t else ""
    return leg + '<ol class="rank" aria-label="Money in each Ohio U.S. House race">' + "".join(rows) + "</ol>" + foot


def house_panel(d):
    nid = f"oh{d['n']:02d}"
    head = f'<h3>{dname(d)}</h3><p class="pc">{cand_line(d)}</p>'
    if d.get("where"):
        head += f'<p class="where">{esc(d["where"])} {cites(d.get("where_src"))}</p>'
    if pending(d):
        body = (f'<dl class="facts"><div><dt>Outside money</dt><dd class="pend">{REFRESH}</dd></div>'
                f'<div><dt>Candidate money</dt><dd class="pend">{REFRESH}</dd></div>'
                f'<div><dt>2024 margin</dt><dd class="pend">{REFRESH}</dd></div></dl>')
        return f'<section class="dpanel" id="{nid}" data-n="{d["n"]}" aria-label="{attr(dname(d))}">{head}{body}</section>'
    o = d["outside"]
    crow = []
    for c in d.get("cand") or []:
        val = c.get("display") or money(c["v"])
        note = f'<small>{esc(c["note"])}</small>' if c.get("note") else ""
        sp = f' <span class="dim">· spent {esc(money(c["spent"]))}</span>' if c.get("spent") is not None and not c.get("display") else ""
        crow.append(f'<span class="cm"><b>{esc(c["name"])}</b> {"" if c.get("display") else "raised "}{esc(val)}{sp}{note}</span>')
    cmh = "".join(crow) + (f'<small>raised through {shortdate(d.get("cand_through"))} {cites(d.get("cand_src"))}; '
                           f'spent: total disbursements, through the same date {cites(d.get("cand_spent_src"))}</small>')
    mgh = (f'<b>{esc(d["margin"])}</b><small>{esc(d.get("margin_detail", ""))}, old lines</small>'
           f'<small>2024 president, new lines: {esc(d.get("pres", ""))}</small><small>{cites(d.get("margin_src"))}</small>') if d.get("margin") else f'<span class="pend">{REFRESH}</span>'
    o24 = ""
    if d.get("o24") is not None:
        o24 = f'<small>Outside money in 2024, old lines: {esc(money(d["o24"]))}{", " + esc(d["o24_note"]) if d.get("o24_note") else ""}</small>'
    body = [f'<dl class="facts"><div><dt>Outside money</dt><dd><b class="big">{esc(fig(o))}</b>'
            f'<small>rows through {shortdate(o["through"])} {cites(o["src"])}</small>'
            + (f'<small>{esc(money(o["general"]))} of it in the general election</small>' if o.get("general") else "")
            + f'{o24}</dd></div><div><dt>Candidate money</dt><dd>{cmh}</dd></div><div><dt>2024 margin</dt><dd>{mgh}</dd></div></dl>']
    if d.get("allin"):
        body.append(f'<p class="allin">{esc(d.get("allin_label", "All of it, candidates and outside groups"))}: <b>{esc(money(d["allin"]))}</b>.</p>')
    mx = max(p["v"] for p in d["payers"])
    body.append('<p class="ph">Who paid, outside the campaigns</p><ul class="pay">')
    for p in d["payers"]:
        w = 100 * p["v"] / mx
        pos = f'<em>{esc(p["pos"])}</em>' if p.get("pos") else '<em class="dim">for or against, mixed or not marked</em>'
        lb = PLAB.get(p["name"])
        if lb:
            pos = f'<em class="lab">{text(lb["label"])} {cites(lb.get("src"))}</em>' + pos
        body.append(f'<li><span class="pnm">{esc(p["name"])} {pos}</span><span class="pb"><i class="grow" style="width:{max(w, .6):.2f}%;background:{SIDE[p.get("side", "")]}"></i></span>'
                    f'<span class="pv">{esc(fig(p))}</span></li>')
    body.append("</ul>")
    if d.get("bought"):
        body.append(f'<p class="bl"><i>What it bought.</i> {text(d["bought"])}</p>')
    if d.get("behind"):
        body.append(f'<p class="bl"><i>Behind the payers.</i> {text(d["behind"])}</p>')
    return f'<section class="dpanel" id="{nid}" data-n="{d["n"]}" aria-label="{attr(dname(d))}">{head}{"".join(body)}</section>'


def block_house_picker():
    order = sorted(H["districts"], key=lambda d: d["n"])
    btns = []
    for d in order:
        cls = ["pick"]
        if d["n"] in H["pinned"]:
            cls.append("pinned")
        if pending(d):
            cls.append("pend")
        btns.append(f'<button type="button" class="{" ".join(cls)}" data-n="{d["n"]}" aria-controls="oh{d["n"]:02d}" aria-pressed="false" aria-label="{attr(dname(d))}">{d["n"]}</button>')
    panels = "".join(house_panel(d) for d in order)
    legend = ('<p class="leg"><span><i style="background:var(--r)"></i>helps the Republican</span>'
              '<span><i style="background:var(--d)"></i>helps the Democrat</span>'
              '<span><i style="background:var(--mute)"></i>mixed or not marked</span></p>')
    return (f'<div class="picker"><p class="ph">Pick a district</p><div class="pbtns" role="group" aria-label="Pick a district">{"".join(btns)}</div>'
            f'{legend}<div class="panels">{panels}</div></div>')


# ---------- what it bought ----------
def block_mix():
    m = DATA["bought"]["governor_mix"]
    tot = sum(p["v"] for p in m["parts"])
    shades = ["var(--d)", "#5b86b0", "#8aaccb", "#b5cadf", "#d3e0ec", "#e7eef5"]
    segs = "".join(f'<i class="seg" style="width:{100 * p["v"] / tot:.2f}%;background:{shades[i % 6]}" title="{attr(p["name"])}"></i>' for i, p in enumerate(m["parts"]))
    rows = "".join(f'<li><i style="background:{shades[i % 6]}"></i><b>{esc(p["name"])}</b> {esc(fig(p))}</li>' for i, p in enumerate(m["parts"]))
    return (f'<div class="mix"><div class="stack">{segs}</div><ul class="mixl">{rows}</ul>'
            f'<p class="fn">{esc(m["who"])}, {shortdate(m["from"])} to {shortdate(m["through"])}.{reported(m)} {cites(m["src"])}</p></div>')


def block_markets():
    m = DATA["bought"]["markets_2026"]
    mx = max(r["v"] for r in m["rows"])
    rows = "".join(f'<li><span class="mn">{esc(r["name"])}</span><span class="mb"><i class="grow" style="width:{100 * r["v"] / mx:.1f}%"></i></span><span class="mv">{esc(money(r["v"]))}</span></li>' for r in m["rows"])
    return (f'<ol class="mkts">{rows}</ol><p class="fn">All political advertising, the two weeks ending {shortdate(m["through"], True)}. '
            f'{esc(m["ohio"]["note"])}: {esc(money(m["ohio"]["v"]))}. {cites(m["src"])}</p>')


def block_themes():
    return '<ul class="themes">' + "".join(f'<li>{text(t["text"])}{reported(t)} {cites(t["src"])}</li>' for t in DATA["bought"]["themes"]) + "</ul>"


def block_ai():
    a = DATA["bought"]["ai"]
    n = a["national"]
    return (f'<p>{text(a["ohio"])}</p>'
            f'<p>Across the country, the Wesleyan Media Project counted at least {n["ads"]} AI-generated or AI-enhanced political ads by {shortdate(n["date"])}, '
            f'{esc(n["spend"])} in airtime by AdImpact\'s estimate. Republican candidates and groups ran {esc(n["r_share"])} of them; '
            f'{esc(n["undisclosed"])} carried no AI disclaimer. {cites(n["src"])}</p>'
            f'<p>{text(a["law"])}</p><p>{text(a["fec"])}</p>')


# ---------- the rule and the gap ----------
def block_nest():
    sl = next(p for s in DATA["flows"]["senate"]["sides"] for p in s["payers"] if p["name"] == "Senate Leadership Fund")
    one = next(f for f in sl["funders"] if f["name"] == "One Nation")
    return f'''<svg class="nest" viewBox="0 0 360 560" role="img" aria-label="A 501(c)(4) gives to a super PAC; the ad names only the super PAC">
<rect class="ndbox" x="8" y="8" width="344" height="120" rx="4"/>
<text class="nk" x="24" y="34">One Nation</text>
<text class="ns" x="24" y="54">a 501(c)(4) nonprofit</text>
<rect class="nd" x="24" y="68" width="178" height="40"/><text class="ndt" x="113" y="93" text-anchor="middle">donors: not disclosed</text>
<path class="ln" d="M180,128 L180,176"/><path class="ln" d="M172,166 L180,178 L188,166"/>
<text class="na" x="194" y="158">{esc(fig(one, True))} this cycle</text>
<rect class="box" x="8" y="182" width="344" height="110" rx="4"/>
<text class="nk" x="24" y="208">Senate Leadership Fund</text>
<text class="ns" x="24" y="228">a super PAC; donors filed with the FEC</text>
<text class="ns" x="24" y="250">Elon Musk {esc(money(168000000, True))} · One Nation {esc(fig(one, True))}</text>
<text class="ns" x="24" y="270">Miriam Adelson {esc(money(30000000, True))} · and others</text>
<path class="ln" d="M180,292 L180,340"/><path class="ln" d="M172,330 L180,342 L188,330"/>
<text class="na" x="192" y="312">{esc(fig(sl, True))}</text><text class="na" x="192" y="327">in Ohio's Senate race</text>
<rect class="tv" x="40" y="348" width="280" height="168" rx="10"/>
<rect class="scr" x="54" y="360" width="252" height="132" rx="3"/>
<rect class="dis" x="54" y="472" width="252" height="20"/>
<text class="dt" x="180" y="486" text-anchor="middle">Senate Leadership Fund is responsible for the content</text>
<path class="lt" d="M150,516 L140,536 M210,516 L220,536"/>
<text class="ns c" x="180" y="552" text-anchor="middle">On screen: the super PAC's name, at least 4 seconds</text>
</svg>'''


def block_timeline():
    tl = DATA["rules"]["timeline"]
    d0, d1 = dayno(tl[0]["date"]), dayno(tl[-1]["date"])
    W, Hh = 960, 200
    x = lambda d: 30 + (W - 60) * (dayno(d) - d0) / (d1 - d0)
    o = [f'<svg class="tline wide" viewBox="0 0 {W} {Hh}" role="img" aria-label="Disclosure dates, {longdate(tl[0]["date"])} to {longdate(tl[-1]["date"])}">',
         f'<line class="ln" x1="30" x2="{W - 30}" y1="100" y2="100"/>']
    band = DATA["rules"].get("timeline_band")
    if band:
        sp, ep = x(band["from"]), x(band["to"])
        o.append(f'<rect class="gap" x="{sp:.1f}" y="92" width="{ep - sp:.1f}" height="16"/>')
    for i, t in enumerate(tl):
        tx = x(t["date"])
        up = i % 2 == 0
        y1, y2 = (100, 74) if up else (100, 126)
        o.append(f'<line class="lt" x1="{tx:.1f}" x2="{tx:.1f}" y1="{y1}" y2="{y2}"/><circle class="pt" cx="{tx:.1f}" cy="100" r="5"/>')
        anc = "end" if i == len(tl) - 1 else ("start" if i == 0 else "middle")
        ly = 20 if up else 146
        o.append(f'<text class="td" x="{tx:.1f}" y="{ly}" text-anchor="{anc}">{shortdate(t["date"])}</text>')
        for k, ln in enumerate(wrap(t["label"], 22)):
            o.append(f'<text class="tl" x="{tx:.1f}" y="{ly + 15 + 13 * k}" text-anchor="{anc}">{esc(ln)}</text>')
    o.append("</svg>")
    rows = "".join(f'<li><time datetime="{t["date"]}">{shortdate(t["date"])}</time><span>{esc(t["label"])}</span></li>' for t in tl)
    band = DATA["rules"].get("timeline_band")
    leg = f'<p class="leg"><span><i class="gapkey"></i>{esc(band["label"])}, {shortdate(band["from"])} to {shortdate(band["to"])}</span></p>' if band else ""
    return "".join(o) + f'<ol class="days small tline-list">{rows}</ol>' + leg


# ---------- sources ----------
def block_sources(order):
    by = {s["id"]: s for s in DATA["sources"]}
    items = []
    for n, sid in enumerate(order, 1):
        s = by[sid]
        items.append(f'<li id="s-{n}">{esc(s["title"])}. <a href="{attr(s["url"])}" rel="noopener">{esc(short_url(s["url"]))}</a></li>')
    return '<ol class="src">' + "".join(items) + "</ol>"


def short_url(u):
    u = re.sub(r"^https?://(www\.)?", "", u)
    return u if len(u) <= 60 else u[:57] + "..."


# ---------- the total, and the races that make it ----------
T = DATA["total"]
KCOL = {"outside": "var(--ink)", "camp": "var(--sky)"}
KNAME = {"outside": "outside groups", "camp": "campaigns"}


def race_split(r):
    o = sum(p["v"] for p in r["parts"] if p["kind"] == "outside")
    return o, r["v"] - o


def block_by_race():
    mx = max(r["v"] for r in T["races"])
    rows = []
    for r in T["races"]:
        o, c = race_split(r)
        rows.append(f'<li class="br"><span class="bn"><b>{esc(r["name"])}</b> <span class="dim">{esc(r["race"])}</span></span>'
                    f'<span class="bt"><i class="grow" style="width:{100 * o / mx:.3f}%;background:{KCOL["outside"]}"></i>'
                    f'<i class="grow" style="width:{100 * c / mx:.3f}%;background:{KCOL["camp"]}"></i></span>'
                    f'<span class="bv"><b>{esc(money(r["v"]))}</b><span>outside {esc(money(o, True))} · campaigns {esc(money(c, True))}</span></span>'
                    f'<span class="bs">outside groups {esc(money(o, True))} · campaigns {esc(money(c, True))}</span></li>')
    leg = ('<p class="leg"><span><i style="background:var(--ink)"></i>outside groups</span>'
           '<span><i style="background:var(--sky)"></i>the candidates\' campaigns</span></p>')
    sumline = " + ".join(f'{esc(r["name"].split(",")[0])} {esc(money(r["v"]))}' for r in T["races"])
    out = [f'<div class="byrace">{leg}<ol class="bars" aria-label="Money spent in each race, on one scale">{"".join(rows)}</ol>',
           f'<p class="sumline">{sumline} = <b>{esc(money(T["v"]))}</b></p></div>']
    return "".join(out)


def block_total_parts():
    rows = []
    for r in T["races"]:
        rows.append(f'<li class="prh"><b>{esc(r["name"])}</b><span>{esc(money(r["v"]))}</span></li>')
        for p in r["parts"]:
            rows.append(f'<li><span class="pnm">{esc(p["name"])}<em>{text(p["how"])}; through {shortdate(p["through"], True)} {cites(p["src"])}</em></span>'
                        f'<span class="pv">${p["v"]:,.2f}</span></li>')
    rows.append(f'<li class="prh tot"><b>All three races</b><span>${T["v"]:,.2f}</span></li>')
    lo = "".join(f"<li>{text(x)}</li>" for x in T["leaves_out"])
    return (f'<p>{text(T["count"])}</p><ol class="parts">{"".join(rows)}</ol>'
            f'<p style="margin-top:12px"><b>What the total leaves out</b></p><ul class="lo">{lo}</ul>')


def block_second_measure():
    a = DATA["governor"]["adimpact"]
    gov = sum(a[k]["aired"] + a[k]["reserved"] for k in ("r", "d"))
    sen = DATA["senate"]["cycles"][-1]
    return (f'<p class="note">A second measure, kept apart and never added in: AdImpact\'s count of advertising aired and booked ahead. '
            f'By that count the Senate race had drawn {esc(fig(sen))} by {shortdate(sen["through"])} {cites(sen["src"])} and the governor\'s race '
            f'{esc(money(gov))} by {shortdate(a["through"])} {cites(a["src"])}, and AdImpact projects {esc(fig(DATA["senate"]["statewide_projection"]))} '
            f'in political advertising across all Ohio races this cycle. {cites(DATA["senate"]["statewide_projection"]["src"])}</p>')


def by_race_svg(W=380):
    """The by-race bars as one small SVG, for the share card."""
    mx = max(r["v"] for r in T["races"])
    y, o = 4, []
    for r in T["races"]:
        ov, cv = race_split(r)
        o.append(f'<text class="bn" x="0" y="{y + 14}">{esc(r["name"])}</text>')
        o.append(f'<text class="bvv" x="{W}" y="{y + 14}" text-anchor="end">{esc(money(r["v"]))}</text>')
        wo, wc = W * ov / mx, W * cv / mx
        o.append(f'<rect x="0" y="{y + 22}" width="{W}" height="20" fill="#dbe2e7"/>')
        o.append(f'<rect x="0" y="{y + 22}" width="{max(wo, 1.5):.1f}" height="20" fill="#162029"/>')
        o.append(f'<rect x="{wo:.1f}" y="{y + 22}" width="{max(wc, 1.5):.1f}" height="20" fill="#3E6A9E"/>')
        y += 62
    return f'<svg class="brs" viewBox="0 0 {W} {y}" width="{W}" height="{y}">' + "".join(o) + "</svg>"


BLOCKS = {
    "senate_line": block_senate_line, "growth": block_growth, "gov_bars": block_gov_bars, "week": block_week,
    "flow_senate": lambda: block_flow("senate"), "flow_governor": lambda: block_flow("governor"),
    "house_pinned": block_house_pinned, "house_rank": block_house_rank, "house_picker": block_house_picker,
    "mix": block_mix, "markets": block_markets, "themes": block_themes, "ai": block_ai,
    "nest": block_nest, "timeline": block_timeline,
    "by_race": block_by_race, "total_parts": block_total_parts, "second_measure": block_second_measure,
}


def render():
    out = SRC
    for name, fn in BLOCKS.items():
        out = out.replace(f"<!--@{name}-->", fn())
    out = re.sub(r"\{\{date:([\w.]+)\}\}", lambda m: longdate(lookup(m[1])), out)
    out = re.sub(r"\{\{([\w.]+)\|short\}\}", lambda m: esc(fig(lookup(m[1]), True)), out)
    out = re.sub(r"\{\{([\w.]+)\|n\}\}", lambda m: f"{lookup(m[1]):,}", out)
    out = re.sub(r"\{\{([\w.]+)\}\}", lambda m: esc(fig(lookup(m[1]))), out)
    # citations: numbered by first use, in page order
    order = []
    known = {s["id"] for s in DATA["sources"]}

    def cite(m):
        links = []
        for sid in [s.strip() for s in m[1].split(",") if s.strip()]:
            if sid not in known:
                sys.exit(f"unknown source id: {sid}")
            if sid not in order:
                order.append(sid)
            n = order.index(sid) + 1
            links.append(f'<a class="cite" href="#s-{n}">[{n}]</a>')
        return "".join(links)

    body, tail = out.split("<!--@sources-->") if "<!--@sources-->" in out else (out, "")
    body = re.sub(r"\[\[c:([^\]]+)\]\]", cite, body)
    tail = re.sub(r"\[\[c:([^\]]+)\]\]", cite, tail)
    unused = [s["id"] for s in DATA["sources"] if s["id"] not in order]
    order += unused  # listed, unnumbered in text
    out = body + block_sources(order) + tail
    chk = out
    for bad in ("\u2014", "{{", "[[c:", "<!--@"):
        probe = chk.replace("<!--@record-->", "")
        if bad in probe:
            j = probe.index(bad)
            sys.exit(f"build check failed: {bad!r} left in output near: {probe[max(0, j - 80):j + 80]!r}")
    rec = json.dumps(DATA, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    if "\u2014" in rec:
        sys.exit("build check failed: an em dash in data.json")
    out = out.replace("<!--@record-->", f'<script type="application/json" id="record">{rec}</script>')
    open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(out)
    filled = [d["n"] for d in H["districts"] if not pending(d)]
    print(f"wrote index.html ({len(out):,} bytes); {len(order) - len(unused)} sources cited, {len(unused)} listed only {unused}; "
          f"House districts filled: {filled}; pending: {[d['n'] for d in H['districts'] if pending(d)]}")


if __name__ == "__main__":
    render()
