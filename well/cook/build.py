#!/usr/bin/env python3
"""The Well · crossword builder (see ../COOK.md).

Fills a symmetric 7x7 (or 5x5) template with theme words, the practice lexicon and common fill,
verifying every crossing. It writes a grid skeleton with answers; Mise writes the clues.

  python3 build.py --track learning --date 2026-10-05 --theme AGENT,TOKEN
  python3 build.py --track news --date 2026-10-05 --theme CHIPS,MODEL --seed 3

Output: a draft JSON on stdout (grid + answer lists with empty clues) for Mise to finish.
No dependencies; standard library only.
"""
import argparse, json, random, re, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent

# 7x7 templates: rotationally symmetric, every entry >= 3 letters, every white square in an across and a down entry.
TEMPLATES_7 = [
    ["...#...", "...#...", ".......", "##...##", ".......", "...#...", "...#..."],
    ["#...###", "#.....#", ".......", "...#...", ".......", "#.....#", "###...#"],
    ["##...##", "#.....#", ".......", "...#...", ".......", "#.....#", "##...##"],
    ["....###", ".....##", "......#", ".......", "#......", "##.....", "###...."],
    ["###....", "##.....", "#......", ".......", "......#", ".....##", "....###"],
    ["...####", "....###", ".......", "...#...", ".......", "###....", "####..."],
    ["#....##", "#.....#", ".......", "...#...", ".......", "#.....#", "##....#"],
    ["..#....", "..#....", ".......", "###.###", ".......", "....#..", "....#.."],
]
TEMPLATES_5 = [
    ["##...", "#....", ".....", "....#", "...##"],
    ["...##", "....#", ".....", "#....", "##..."],
    ["#....", ".....", ".....", ".....", "....#"],
]


def slots(t):
    n = len(t); out = []
    for r in range(n):
        c = 0
        while c < n:
            if t[r][c] == "#": c += 1; continue
            s = c
            while c < n and t[r][c] != "#": c += 1
            if c - s >= 2: out.append(("A", [(r, x) for x in range(s, c)]))
    for c in range(n):
        r = 0
        while r < n:
            if t[r][c] == "#": r += 1; continue
            s = r
            while r < n and t[r][c] != "#": r += 1
            if r - s >= 2: out.append(("D", [(y, c) for y in range(s, r)]))
    return out


def template_ok(t):
    n = len(t)
    if any(len(row) != n for row in t): return False
    if any(t[r][c] != t[n - 1 - r][n - 1 - c] for r in range(n) for c in range(n)): return False
    ss = slots(t)
    if any(len(cells) < 3 for _, cells in ss): return False
    cover = {}
    for d, cells in ss:
        for rc in cells: cover.setdefault(rc, set()).add(d)
    return all(cover.get((r, c)) == {"A", "D"} for r in range(n) for c in range(n) if t[r][c] != "#")


def load_words():
    fill = [w.strip().upper() for w in (HERE / "fill.txt").read_text().split() if w.strip()]
    lex = json.loads((HERE / "lexicon.json").read_text())
    lexw = [e["word"].upper() for e in lex["words"]]
    return fill, lexw


def fill_grid(t, theme, lexw, fill, recent, rng, max_steps=150_000, prefer=()):
    """Backtracking fill: most-constrained slot first, candidates from an index of (length, position, letter)."""
    n = len(t); ss = slots(t)
    grid = [[None if t[r][c] == "#" else "" for c in range(n)] for r in range(n)]
    score = {}
    for w in fill: score[w] = 1
    for w in lexw: score[w] = 5
    for w in theme: score[w] = 50
    for w in prefer: score[w] = 40
    words_by_len = {}
    for w in score:
        if w in recent and w not in theme: continue
        words_by_len.setdefault(len(w), []).append(w)
    for L in words_by_len:
        rng.shuffle(words_by_len[L]); words_by_len[L].sort(key=lambda w: -score[w])
    index = {}
    for L, ws in words_by_len.items():
        for w in ws:
            for i, ch in enumerate(w): index.setdefault((L, i, ch), set()).add(w)
    used = set(); steps = [0]

    def pattern(cells): return [grid[r][c] for r, c in cells]

    def cands(cells):
        L = len(cells); pat = pattern(cells); pool = None
        for i, ch in enumerate(pat):
            if ch:
                s2 = index.get((L, i, ch), set())
                pool = s2 if pool is None else pool & s2
                if not pool: return []
        if pool is None: return [w for w in words_by_len.get(L, []) if w not in used]
        return sorted((w for w in pool if w not in used), key=lambda w: -score[w])

    crossing = {}
    for i, (_, c1) in enumerate(ss):
        crossing[i] = [j for j, (_, c2) in enumerate(ss) if j != i and set(c1) & set(c2)]

    def solve():
        steps[0] += 1
        if steps[0] > max_steps: return False
        best = None
        for i, (_, cells) in enumerate(ss):
            if all(grid[r][c] for r, c in cells): continue
            cs = cands(cells)
            if not cs: return False
            if best is None or len(cs) < len(best[1]): best = (i, cs)
            if len(cs) == 1: break
        if best is None:
            words = ["".join(grid[r][c] for r, c in cells) for _, cells in ss]
            return len(set(words)) == len(words) and all(w in score for w in words)
        i, cs = best; cells = ss[i][1]
        for w in cs[:80]:
            saved = [grid[r][c] for r, c in cells]
            for (r, c), ch in zip(cells, w): grid[r][c] = ch
            used.add(w)
            okk = True
            for j in crossing[i]:
                c2 = ss[j][1]
                if all(grid[r][c] for r, c in c2):
                    if "".join(grid[r][c] for r, c in c2) not in score: okk = False; break
                elif not cands(c2): okk = False; break
            if okk and solve(): return True
            used.discard(w)
            for (r, c), ch in zip(cells, saved): grid[r][c] = ch
        return False

    def reset():
        for r in range(n):
            for c in range(n):
                if grid[r][c] is not None: grid[r][c] = ""
        used.clear()

    if not theme:
        steps[0] = 0
        if not solve(): return None
    else:
        tw = max(theme, key=len)
        spots = [cells for _, cells in ss if len(cells) == len(tw)]
        rng.shuffle(spots)
        for cells in spots:
            reset()
            for (r, c), ch in zip(cells, tw): grid[r][c] = ch
            used.add(tw); steps[0] = 0
            if solve(): break
        else:
            return None
    return ["".join(grid[r][c] or "#" for c in range(n)) for r in range(n)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--track", choices=["learning", "news"], required=True)
    ap.add_argument("--date", required=True)
    ap.add_argument("--theme", default="")
    ap.add_argument("--size", type=int, default=7)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--recent", default="", help="comma list of answers used in the last 14 days")
    a = ap.parse_args()
    rng = random.Random(a.seed or hash(a.date + a.track))
    fill, lexw = load_words()
    theme = [w.strip().upper() for w in a.theme.split(",") if w.strip()]
    recent = set(w.strip().upper() for w in a.recent.split(",") if w.strip())
    temps = TEMPLATES_7 if a.size == 7 else TEMPLATES_5
    temps = [t for t in temps if template_ok(t)]
    order = temps[:]; rng.shuffle(order)
    t0 = time.time()
    for tries in range(len(theme) + 1):
        th = theme[: len(theme) - tries] if tries else theme
        for t in order:
            g = fill_grid(t, th, lexw, fill, recent, rng, prefer=theme)
            if g:
                ss = slots(g)
                acr = ["".join(g[r][c] for r, c in cells) for d, cells in ss if d == "A"]
                dn = ["".join(g[r][c] for r, c in cells) for d, cells in ss if d == "D"]
                out = {"v": 1, "track": a.track, "date": a.date, "size": len(g), "g": g,
                       "a": [[w, ""] for w in acr], "d": [[w, ""] for w in dn],
                       "w": next((w for w in theme if w in acr + dn), ""), "n": "", "sources": [], "checked": False,
                       "_theme_placed": [w for w in theme if w in acr + dn], "_seconds": round(time.time() - t0, 1)}
                print(json.dumps(out, indent=1))
                return 0
    print("no fill found; try other theme words or --seed", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
