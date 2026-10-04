#!/usr/bin/env python3
"""The Well · crossword builder (see ../COOK.md).

Fills a symmetric 7x7 (or 5x5, 11x11, 13x13) template with theme words, the practice lexicon and common fill,
verifying every crossing. It writes a grid skeleton with answers; Mise writes the clues.

  python3 build.py --track learning --date 2026-10-05 --theme AGENT,TOKEN
  python3 build.py --track news --date 2026-10-05 --theme CHIPS,MODEL --seed 3
  python3 build.py --track weekly --size 11 --date 2026-10-04 --theme MERIDIAN,ACCORD,ROGUE --seed 1 --budget 240

Sizes: 5 and 7 (the daily pages, unchanged), 11 and 13 (the Sunday Edition; uses fill-long.txt for 8-letter slots).

Output: a draft JSON on stdout (grid + answer lists with empty clues) for Mise to finish.
No dependencies; standard library only.
"""
import argparse, json, math, random, re, sys, time
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

# 11x11 and 13x13 templates (Sunday Edition): rotationally symmetric, every entry 3+ letters, every white square
# checked both ways, one connected grid. Entries run 3 to 8 letters: fill.txt covers 3 to 7, fill-long.txt covers 8,
# and theme words take the long slots first. Found by a random symmetric search, kept for how reliably they fill.
TEMPLATES_11 = [
    ["...#...#...", ".......#...", ".......#...", "....###...#", "...#....###", "##.......##", "###....#...", "#...###....", "...#.......", "...#.......", "...#...#..."],
    ["...####...#", ".....#....#", ".....#.....", ".......#...", "###...##...", "...#...#...", "...##...###", "...#.......", ".....#.....", "#....#.....", "#...####..."],
    ["#...##.....", "#...##.....", "#....#.....", "......#...#", "...#....###", "...#...#...", "###....#...", "#...#......", ".....#....#", ".....##...#", ".....##...#"],
    [".....##...#", ".....##...#", ".....##....", "#...#......", "###....#...", "...#...#...", "...#....###", "......#...#", "....##.....", "#...##.....", "#...##....."],
    ["#...##...##", "#...##.....", "....#......", "......#....", "...#....###", "...#...#...", "###....#...", "....#......", "......#....", ".....##...#", "##...##...#"],
    ["#....##...#", ".....##....", "......#....", "....#......", "...#....###", "###.....###", "###....#...", "......#....", "....#......", "....##.....", "#...##....#"],
    [".....#...##", ".....#....#", ".....#....#", "#...#......", "###....#...", "...#...#...", "...#....###", "......#...#", "#....#.....", "#....#.....", "##...#....."],
    ["...###.....", "....##.....", "....#......", "###...#...#", "...#...#...", "...#...#...", "...#...#...", "#...#...###", "......#....", ".....##....", ".....###..."],
    # with 8-letter slots, for long theme words
    ["###...#...#", "......#....", "......#....", "...##......", "###........", ".....#.....", "........###", "......##...", "....#......", "....#......", "#...#...###"],
    ["#....###...", "#....#.....", "#....#.....", "........###", "......##...", "...#...#...", "...##......", "###........", ".....#....#", ".....#....#", "...###....#"],
    ["...#...#...", ".......#...", ".......#...", "###........", "###...#...#", "#...###...#", "#...#...###", "........###", "...#.......", "...#.......", "...#...#..."],
    [".....##...#", ".....##...#", "......#....", "###....#...", ".......#...", ".....#.....", "...#.......", "...#....###", "....#......", "#...##.....", "#...##....."],
]
TEMPLATES_13 = [
    ["...#...##...#", "...#...##....", ".......#.....", "###......#...", ".....##...###", "...#....#...#", "....#...#....", "#...#....#...", "###...##.....", "...#......###", ".....#.......", "....##...#...", "#...##...#..."],
    ["##.....##...#", "#......#....#", "#......#....#", "......#......", "....#...##...", ".....#...#...", "###.......###", "...#...#.....", "...##...#....", "......#......", "#....#......#", "#....#......#", "#...##.....##"],
    [".......##....", ".......##....", ".......##....", "#.....##....#", "#.....#...###", "....##.......", "...#.....#...", ".......##....", "###...#.....#", "#....##.....#", "....##.......", "....##.......", "....##......."],
    ["##...##......", ".....##......", "......#......", "........##...", "#...#.....###", "...###.......", "......#......", ".......###...", "###.....#...#", "...##........", "......#......", "......##.....", "......##...##"],
    ["#...#...#...#", "....#...#...#", "....#.......#", "...#...#.....", "##...#...#...", "###...#......", "#.....#.....#", "......#...###", "...#...#...##", ".....#...#...", "#.......#....", "#...#...#....", "#...#...#...#"],
    [".....###....#", ".....##......", "......#......", "#...#...##...", "...##.....###", "...#...#....#", "......#......", "#....#...#...", "###.....##...", "...##...#...#", "......#......", "......##.....", "#....###....."],
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


# ---------- 11x11 and 13x13 (the Sunday Edition) ----------
# Same rules as the 7x7 path, a stronger search: theme words are seeded longest first into slots of their length,
# then the rest fills by most-constrained slot first, trying the words that leave the crossings the most room
# (least-constraining value), with forward checking and many short randomized restarts.

def connected(t):
    n = len(t); cells = [(r, c) for r in range(n) for c in range(n) if t[r][c] != "#"]
    seen = {cells[0]}; st = [cells[0]]
    while st:
        r, c = st.pop()
        for y, x in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= y < n and 0 <= x < n and t[y][x] != "#" and (y, x) not in seen: seen.add((y, x)); st.append((y, x))
    return len(seen) == len(cells)


class BigIndex:
    def __init__(self, words):
        self.all = {}; self.idx = {}; self.cache = {}
        for w in words:
            L = len(w); self.all.setdefault(L, set()).add(w)
            for i, ch in enumerate(w): self.idx.setdefault((L, i, ch), set()).add(w)
        self.all = {L: frozenset(v) for L, v in self.all.items()}
        self.idx = {k: frozenset(v) for k, v in self.idx.items()}

    def pool(self, pat):
        r = self.cache.get(pat)
        if r is not None: return r
        L = len(pat); s = self.all.get(L, frozenset())
        for i, ch in enumerate(pat):
            if ch != ".":
                s = s & self.idx.get((L, i, ch), frozenset())
                if not s: break
        self.cache[pat] = s
        return s


def big_fill(t, theme, score, ix, rng, max_nodes=300, place_tries=3, must=()):
    """Maintained-arc-consistency fill: every slot keeps a domain of words that still fit; placing a word prunes its
    crossings letter by letter until nothing changes. Theme words are seeded longest first, each kept only if the grid
    stays consistent. Returns (rows, theme words in the grid) or (None, [])."""
    n=len(t); ss=slots(t); S=len(ss)
    Ls=[len(c) for _,c in ss]
    # crossings: list of (i,a,j,b)
    pos={}
    for i,(_,cells) in enumerate(ss):
        for a,rc in enumerate(cells): pos.setdefault(rc,[]).append((i,a))
    arcs=[(v[0],v[1]) for v in pos.values() if len(v)==2]
    cross=[[] for _ in range(S)]
    for (i,a),(j,b) in arcs: cross[i].append((a,j,b)); cross[j].append((b,i,a))
    def letters(D,a): return {w[a] for w in D}
    def restrict(D,L,a,allowed):
        u=set()
        for ch in allowed: u|=ix.idx.get((L,a,ch),frozenset())
        return D & u
    def ac(dom, queue):
        queue=set(queue)
        while queue:
            i=queue.pop()
            Di=dom[i]
            for a,j,b in cross[i]:
                if len(dom[j])==1 and len(Di)==1: 
                    if next(iter(dom[j]))[b]!=next(iter(Di))[a]: return False
                    continue
                al=letters(Di,a)
                if len(al)==26: continue
                nd=restrict(dom[j],Ls[j],b,al)
                if len(nd)!=len(dom[j]):
                    if not nd: return False
                    dom[j]=nd; queue.add(j)
        return True
    base=[frozenset(ix.all.get(L,frozenset())) for L in Ls]
    # theme placement: longest first, random among slots of matching length; then AC must pass
    best=None
    for attempt in range(place_tries):
        dom=list(base); placed=[]
        for w in [m for m in must if m in theme] + sorted([x for x in theme if x not in must],key=lambda x:(-len(x),rng.random())):
            spots=[i for i in range(S) if Ls[i]==len(w) and w in dom[i] and len(dom[i])>1]
            rng.shuffle(spots)
            for i in spots:
                trial=list(dom); trial[i]=frozenset([w])
                for k in range(S):
                    if k!=i and w in trial[k]: trial[k]=trial[k]-{w}
                if ac(trial,[i]):
                    dom=trial; placed.append(w); break
        if any(m in theme and m not in placed for m in must): continue
        if not ac(dom, range(S)): continue
        nodes=[0]
        def solve(dom):
            nodes[0]+=1
            if nodes[0]>max_nodes: return None
            open_=[i for i in range(S) if len(dom[i])>1]
            if not open_:
                ws=[next(iter(d)) for d in dom]
                return dom if len(set(ws))==len(ws) else None
            i=min(open_,key=lambda k:len(dom[k]))
            cs=list(dom[i]); rng.shuffle(cs); cs.sort(key=lambda w:-score[w]); cs=cs[:60]
            # LCV: prefer words leaving more letters across crossings
            def lcv(w):
                tot=0
                for a,j,b in cross[i]:
                    k=len(dom[j] & ix.idx.get((Ls[j],b,w[a]),frozenset()))
                    if k==0: return None
                    tot+=math.log(k)
                return tot+3*math.log(score[w])+rng.random()
            rk=[(lcv(w),w) for w in cs]; rk=[x for x in rk if x[0] is not None]; rk.sort(reverse=True)
            for _,w in rk[:8]:
                nd=list(dom); nd[i]=frozenset([w])
                for k in range(S):
                    if k!=i and len(nd[k])>1 and w in nd[k]: nd[k]=nd[k]-{w}
                if ac(nd,[i]):
                    r=solve(nd)
                    if r: return r
            return None
        r=solve(dom)
        if r:
            g=[[None if t[y][x]=='#' else '.' for x in range(n)] for y in range(n)]
            for i,(_,cells) in enumerate(ss):
                w=next(iter(r[i]))
                for (y,x),ch in zip(cells,w): g[y][x]=ch
            rows=[''.join(c or '#' for c in row) for row in g]
            ws=[''.join(rows[y][x] for y,x in cells) for _,cells in ss]
            if len(set(ws))==len(ws) and all(w in score for w in ws):
                return rows,[w for w in theme if w in ws]
    return None,[]


def build_big(size, theme, lexw, fill, recent, rng, budget=240.0, want=None, must=()):
    """Try templates and restarts until every theme word lands or the time budget runs out; keep the grid with the most theme words."""
    longw = [w.strip().upper() for w in (HERE / "fill-long.txt").read_text().split() if w.strip()] if (HERE / "fill-long.txt").exists() else []
    extra = [w.strip().upper() for w in (HERE / "fill-extra.txt").read_text().split() if w.strip()] if (HERE / "fill-extra.txt").exists() else []
    score = {}
    for w in extra: score[w] = 0.2   # last resort: less common words, used only where nothing else fits
    for w in fill + longw: score[w] = 1
    for w in lexw: score[w] = 5
    for w in theme: score[w] = 50
    for w in list(score):
        if w in recent and w not in theme: del score[w]
    ix = BigIndex(list(score))
    temps = [t for t in (TEMPLATES_11 if size == 11 else TEMPLATES_13) if template_ok(t) and connected(t)]
    want = want if want is not None else len(theme)
    must = [w for w in must if w in theme] or []
    best = None; t0 = time.time(); tries = 0
    while time.time() - t0 < budget:
        t = rng.choice(temps); tries += 1
        # seed a random subset of the theme each try (all of it on the first few); unseeded theme words can still land in the fill
        k = len(theme) if tries <= 3 else rng.randint(min(2, len(theme)), len(theme))
        sub = rng.sample(theme, k) if theme else []
        sub = must + [w for w in sub if w not in must]
        g, placed = big_fill(t, sub, score, ix, rng, must=must)
        if not g: continue
        ws = ["".join(g[r][c] for r, c in cells) for _, cells in slots(g)]
        if any(w not in ws for w in must): continue
        placed = [w for w in theme if w in ws]
        rare = sum(1 for w in ws if score.get(w, 1) < 1)   # last-resort words in the grid; fewer is cleaner
        if best is None or (len(placed), -rare) > (len(best[1]), -best[2]):
            best = (g, placed, rare)
            print("  found grid with %d/%d theme words, %d last-resort fill, after %d tries, %.0fs" % (len(placed), len(theme), rare, tries, time.time() - t0), file=sys.stderr)
            if len(placed) >= want and rare == 0: break
    return best[:2] if best else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--track", choices=["learning", "news", "weekly"], required=True)
    ap.add_argument("--date", required=True)
    ap.add_argument("--theme", default="")
    ap.add_argument("--size", type=int, default=7)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--recent", default="", help="comma list of answers used in the last 14 days")
    ap.add_argument("--budget", type=float, default=240, help="11/13 only: seconds to search before keeping the best grid")
    ap.add_argument("--must", default="", help="11/13 only: comma list of theme words every kept grid must hold")
    ap.add_argument("--want", type=int, default=None, help="11/13 only: stop once this many theme words land (default: all)")
    a = ap.parse_args()
    rng = random.Random(a.seed or hash(a.date + a.track))
    fill, lexw = load_words()
    theme = [w.strip().upper() for w in a.theme.split(",") if w.strip()]
    recent = set(w.strip().upper() for w in a.recent.split(",") if w.strip())
    if a.size in (11, 13):
        must = [w.strip().upper() for w in a.must.split(",") if w.strip()]
        theme = must + [w for w in theme if w not in must]
        best = build_big(a.size, theme, lexw, fill, recent, rng, budget=a.budget, want=a.want, must=must)
        if not best:
            print("no fill found; try other theme words or --seed", file=sys.stderr); return 1
        g, placed = best; ss = slots(g)
        acr = ["".join(g[r][c] for r, c in cells) for d, cells in ss if d == "A"]
        dn = ["".join(g[r][c] for r, c in cells) for d, cells in ss if d == "D"]
        out = {"v": 1, "track": a.track, "date": a.date, "size": len(g), "g": g,
               "a": [[w, ""] for w in acr], "d": [[w, ""] for w in dn],
               "w": next((w for w in theme if w in acr + dn), ""), "n": "", "sources": [], "coming": [], "checked": False,
               "_theme_placed": placed, "_theme_missed": [w for w in theme if w not in placed]}
        print(json.dumps(out, indent=1))
        return 0
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
