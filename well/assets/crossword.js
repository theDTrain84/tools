/* The Well · shared crossword engine (The Daily Line, The Morning Edition).
   Usage: Crossword.mount({ bank, storagePrefix, title, shareUrl, puzzlePath, startDate })
   Optional (the Sunday Edition): puzzle (an already-loaded puzzle, used before the bank), no (the edition number),
   keyByPuzzleDate (keep progress per puzzle date, so a weekly grid survives across days), wordLabel, onPlay(P, from).
   A puzzle is { g:[rows], a:[[ANSWER, clue, {src}?]], d:[...], w:WORD, n:"teaching", sources:[{title,url,date}]? }.
   Any square size works; "#" is a black square. The page provides the element ids used below. */
(function () {
  "use strict";
  var DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    MON = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

  function slotsOf(g) {
    var N = g.length, A = [], D = [], r, c, s;
    for (r = 0; r < N; r++) { c = 0; while (c < N) { if (g[r][c] === "#") { c++; continue } s = c; while (c < N && g[r][c] !== "#") c++; if (c - s > 1) { var cs = []; for (var x = s; x < c; x++) cs.push([r, x]); A.push(cs) } } }
    for (c = 0; c < N; c++) { r = 0; while (r < N) { if (g[r][c] === "#") { r++; continue } s = r; while (r < N && g[r][c] !== "#") r++; if (r - s > 1) { var ds = []; for (var y = s; y < r; y++) ds.push([y, c]); D.push(ds) } } }
    return { A: A, D: D };
  }

  /* Re-derive every entry from the grid and check it against the answer lists. Returns a list of problems (empty = good). */
  function check(p) {
    var bad = [], g = p && p.g, seen = {};
    if (!g || !g.length) return ["no grid"];
    var N = g.length;
    g.forEach(function (row) { if (typeof row !== "string" || row.length !== N) bad.push("row length"); if (!/^[A-Z#]+$/.test(row)) bad.push("bad characters") });
    if (bad.length) return bad;
    var S = slotsOf(g);
    [["A", S.A, p.a], ["D", S.D, p.d]].forEach(function (t) {
      if (!t[2] || t[1].length !== t[2].length) { bad.push(t[0] + " count"); return }
      t[1].forEach(function (cells, j) {
        var w = cells.map(function (rc) { return g[rc[0]][rc[1]] }).join("");
        if (w.length < 3) bad.push(t[0] + j + " short");
        if (!t[2][j] || t[2][j][0] !== w) bad.push(t[0] + j + " " + w + " vs " + (t[2][j] && t[2][j][0]));
        if (seen[w]) bad.push("dup " + w); seen[w] = 1;
        if (!t[2][j] || !t[2][j][1]) bad.push("no clue " + w);
      });
    });
    for (var r = 0; r < N; r++) for (var c = 0; c < N; c++) {
      if (g[r][c] === "#") continue;
      var inA = S.A.some(function (s) { return s.some(function (x) { return x[0] === r && x[1] === c }) }),
        inD = S.D.some(function (s) { return s.some(function (x) { return x[0] === r && x[1] === c }) });
      if (!inA && !inD) bad.push("orphan " + r + "," + c);
    }
    if (!seen[p.w]) bad.push("teaching word not in grid");
    if (!p.n) bad.push("no teaching note");
    if (/—|–/.test(JSON.stringify(p))) bad.push("dash");
    return bad;
  }

  function isoDay(d) { return d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2) }

  function mount(cfg) {
  // Dustin 10/2: the dark squares take a brand colour, a different one each day
  try {
    var sd = cfg.startDate || [2026, 9, 2];
    var d0 = new Date(sd[0], sd[1], sd[2]); var t = new Date(); var d1 = new Date(t.getFullYear(), t.getMonth(), t.getDate());
    var dayIdx = Math.max(0, Math.round((d1 - d0) / 86400000));
    var pal = ['#3E6A9E', '#B4862E', '#2E3A4F', '#D9B25A'];
    var col = pal[dayIdx % pal.length];
    var host = (cfg.root && cfg.root.style) ? cfg.root : document.documentElement;
    host.style.setProperty('--grid-dark', col); host.style.setProperty('--accent', col);
  } catch (e) {}

    var bank = cfg.bank || [], prefix = cfg.storagePrefix, start = cfg.startDate || [2026, 9, 2];
    var errs = [];
    bank.forEach(function (p, i) { var b = check(p); if (b.length) errs.push("Puzzle " + (i + 1) + ": " + b.join("; ")) });
    if (errs.length) console.error("[" + cfg.title + "] bank self-test failed", errs);
    else console.info("[" + cfg.title + "] bank self-test: " + bank.length + "/" + bank.length + " grids pass, all crossings consistent");

    var now = new Date(), iso = isoDay(now);
    var dayIdx = Math.round((Date.UTC(now.getFullYear(), now.getMonth(), now.getDate()) - Date.UTC(start[0], start[1], start[2])) / 864e5);
    var bankPick = bank[((dayIdx % bank.length) + bank.length) % bank.length];

    if (cfg.puzzle) {
      var pb = check(cfg.puzzle);
      if (pb.length) { console.warn("[" + cfg.title + "] the loaded puzzle failed its check, using the bank", pb); run(bankPick, "bank") }
      else run(cfg.puzzle, "cooked");
    } else if (cfg.puzzlePath && window.fetch) {
      fetch(cfg.puzzlePath + iso + ".json", { cache: "no-store" })
        .then(function (r) { return r.ok ? r.json() : Promise.reject(r.status) })
        .then(function (p) {
          var b = check(p);
          if (b.length) { console.warn("[" + cfg.title + "] today's cooked puzzle failed its check, using the bank", b); run(bankPick, "bank") }
          else run(p, "cooked");
        })
        .catch(function () { run(bankPick, "bank") });
    } else run(bankPick, "bank");

    function run(P, from) { play(cfg, P, from, dayIdx, iso, now) }
  }

  function play(cfg, P, from, dayIdx, iso, now) {
    var prefix = cfg.storagePrefix, G = P.g, N = G.length, S = slotsOf(G), entries = [], num = {}, n = 1;
    var no = (cfg.no && from === "cooked") ? cfg.no : Math.max(1, dayIdx + 1);
    var $ = function (id) { return document.getElementById(id) };
    $("date").textContent = (cfg.dateLine ? cfg.dateLine(now, from) : DAYS[now.getDay()] + " · " + MON[now.getMonth()] + " " + now.getDate() + ", " + now.getFullYear()) + " · No. " + no;
    $("pzl").textContent = "No. " + no;
    function load(k) { try { var v = localStorage.getItem(prefix + k); return v ? JSON.parse(v) : null } catch (e) { return null } }
    function save(k, v) { try { localStorage.setItem(prefix + k, JSON.stringify(v)) } catch (e) { } }

    /* ---------- model ---------- */
    for (var r = 0; r < N; r++) for (var c = 0; c < N; c++) {
      if (G[r][c] === "#") continue;
      var sa = (c === 0 || G[r][c - 1] === "#") && c < N - 1 && G[r][c + 1] !== "#", sd = (r === 0 || G[r - 1][c] === "#") && r < N - 1 && G[r + 1][c] !== "#";
      if (sa || sd) num[r + "," + c] = n++;
    }
    S.A.forEach(function (cs, j) { entries.push({ dir: "A", cells: cs, ans: P.a[j][0], clue: P.a[j][1], src: P.a[j][2] && P.a[j][2].src, n: num[cs[0].join(",")] }) });
    S.D.forEach(function (cs, j) { entries.push({ dir: "D", cells: cs, ans: P.d[j][0], clue: P.d[j][1], src: P.d[j][2] && P.d[j][2].src, n: num[cs[0].join(",")] }) });
    entries.sort(function (x, y) { return x.dir === y.dir ? x.n - y.n : (x.dir === "A" ? -1 : 1) });
    var key = ((cfg.keyByPuzzleDate && P.date) ? P.date : iso) + ":" + G.join("");
    var st = load("state");
    if (!st || st.key !== key) st = { key: key, f: {}, t: 0, done: false, help: false, started: false };
    var sel = { r: 0, c: 0, dir: "A" }, tStart = 0, tick = null;

    /* ---------- build DOM ---------- */
    var board = document.querySelector(".board"), gridEl = $("grid"), btn = {};
    board.style.setProperty("--n", N);
    board.classList.toggle("big", N > 5);
    board.classList.toggle("huge", N > 9);
    gridEl.setAttribute("aria-label", "Crossword grid, " + N + " by " + N);
    for (r = 0; r < N; r++) for (c = 0; c < N; c++) {
      var b = document.createElement("button"); b.type = "button"; b.className = "cell";
      if (G[r][c] === "#") { b.className += " blk"; b.tabIndex = -1; b.setAttribute("aria-hidden", "true"); b.disabled = true }
      else {
        if (num[r + "," + c]) { var s = document.createElement("span"); s.className = "n"; s.textContent = num[r + "," + c]; b.appendChild(s) }
        var l = document.createElement("span"); l.className = "l"; b.appendChild(l);
        (function (rr, cc) {
          b.addEventListener("click", function () {
            if (sel.r === rr && sel.c === cc) toggleDir(); else { sel.r = rr; sel.c = cc; if (!entryAt(rr, cc, sel.dir)) toggleDir(true) }
            paint(true);
          })
        })(r, c);
      }
      btn[r + "," + c] = b; gridEl.appendChild(b);
    }
    function entryAt(r, c, dir) { for (var i = 0; i < entries.length; i++) { var e = entries[i]; if (e.dir === dir && e.cells.some(function (x) { return x[0] === r && x[1] === c })) return e } return null }
    function toggleDir(force) { var d = sel.dir === "A" ? "D" : "A"; if (entryAt(sel.r, sel.c, d) || force) sel.dir = d }
    function cur() { return entryAt(sel.r, sel.c, sel.dir) || entryAt(sel.r, sel.c, sel.dir === "A" ? "D" : "A") }

    ["across", "down"].forEach(function (id) {
      var ol = $(id);
      entries.filter(function (e) { return e.dir === (id === "across" ? "A" : "D") }).forEach(function (e) {
        var li = document.createElement("li"), b = document.createElement("button"); b.type = "button"; b.className = "cl";
        b.innerHTML = "<b>" + e.n + "</b><span></span>"; b.lastChild.textContent = e.clue;
        b.setAttribute("aria-label", e.n + " " + (e.dir === "A" ? "across" : "down") + ". " + e.clue + ". " + e.ans.length + " letters");
        b.addEventListener("click", function () { go(e, true) });
        e.btn = b; e.li = li; li.appendChild(b); ol.appendChild(li);
      });
    });

    /* on-screen keyboard for touch */
    var touch = false; try { touch = window.matchMedia("(pointer: coarse)").matches || ("ontouchstart" in window) } catch (e) { }
    if (touch) document.body.classList.add("touch");
    var kb = $("kb");
    ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM<"].forEach(function (row) {
      var d = document.createElement("div"); d.className = "kr";
      row.split("").forEach(function (ch) {
        var k = document.createElement("button"); k.type = "button"; k.className = "key" + (ch === "<" ? " bk" : "");
        k.textContent = ch === "<" ? "⌫" : ch; k.setAttribute("aria-label", ch === "<" ? "Backspace" : ch);
        k.addEventListener("click", function () { if (ch === "<") back(); else typeL(ch) });
        d.appendChild(k);
      }); kb.appendChild(d);
    });

    /* ---------- painting ---------- */
    var lastLive = "";
    function paint(focus) {
      var e = cur(); if (e) sel.dir = e.dir;
      for (var k in btn) {
        var b = btn[k]; if (b.disabled) continue;
        var rc = k.split(","), ch = st.f[k] || "", lab = b.querySelector(".l");
        if (lab.textContent !== ch) lab.textContent = ch;
        b.classList.toggle("sel", +rc[0] === sel.r && +rc[1] === sel.c);
        b.classList.toggle("word", !!e && e.cells.some(function (x) { return x[0] == rc[0] && x[1] == rc[1] }));
        var m = (st.m || {})[k]; b.classList.toggle("ok", m === "ok"); b.classList.toggle("bad", m === "bad"); b.classList.toggle("rev", m === "rev");
        b.setAttribute("aria-label", "Row " + (+rc[0] + 1) + ", column " + (+rc[1] + 1) + ", " + (ch ? "letter " + ch : "empty"));
      }
      entries.forEach(function (x) {
        x.btn.classList.toggle("on", x === e);
        x.btn.classList.toggle("fill", x.cells.every(function (rc) { return st.f[rc.join(",")] }));
      });
      if (e) {
        $("nowTag").textContent = e.n + (e.dir === "A" ? " Across" : " Down");
        $("nowTx").textContent = e.clue;
        var say = e.n + (e.dir === "A" ? " across. " : " down. ") + e.clue + ". " + e.ans.length + " letters.";
        if (say !== lastLive) { $("live").textContent = say; lastLive = say }
      }
      if (focus && !touch) btn[sel.r + "," + sel.c].focus({ preventScroll: true });
      else if (focus && touch && document.activeElement && document.activeElement.classList.contains("cell")) document.activeElement.blur();
    }

    /* ---------- moves ---------- */
    function go(e, focus) { var first = e.cells.find(function (rc) { return !st.f[rc.join(",")] }) || e.cells[0]; sel = { r: first[0], c: first[1], dir: e.dir }; paint(focus) }
    function nextClue(step) {
      var e = cur(), i = entries.indexOf(e), L = entries.length;
      for (var k = 1; k <= L; k++) { var x = entries[(i + step * k + L * k) % L]; if (st.done || x.cells.some(function (rc) { return !st.f[rc.join(",")] })) { go(x, true); return } }
      go(entries[(i + step + L) % L], true);
    }
    function move(dr, dc) {
      var d = dr ? "D" : "A"; if (sel.dir !== d && entryAt(sel.r, sel.c, d)) { sel.dir = d; paint(true); return }
      var r = sel.r, c = sel.c;
      for (var k = 0; k < N; k++) { r += dr; c += dc; if (r < 0 || r > N - 1 || c < 0 || c > N - 1) return; if (G[r][c] !== "#") { sel.r = r; sel.c = c; if (!entryAt(r, c, sel.dir)) toggleDir(true); paint(true); return } }
    }
    function startClock() { if (st.done || tick) return; st.started = true; tStart = Date.now() - st.t * 1000; tick = setInterval(function () { st.t = Math.floor((Date.now() - tStart) / 1000); showTime(); save("state", st) }, 500) }
    function stopClock() { if (tick) { clearInterval(tick); tick = null } }
    function fmt(s) { return Math.floor(s / 60) + ":" + ("0" + (s % 60)).slice(-2) }
    function showTime() { $("timer").textContent = fmt(st.t) }
    function typeL(ch) {
      if (st.done) return; startClock();
      var k = sel.r + "," + sel.c; if (st.m && st.m[k] === "rev") return advance();
      st.f[k] = ch; if (st.m && st.m[k] && st.m[k] !== "rev") delete st.m[k];
      var lab = btn[k].querySelector(".l"); lab.classList.remove("set"); void lab.offsetWidth; lab.classList.add("set");
      advance(); save("state", st); verify();
    }
    function advance() {
      var e = cur(), i = e.cells.findIndex(function (rc) { return rc[0] === sel.r && rc[1] === sel.c });
      for (var k = i + 1; k < e.cells.length; k++) { if (!st.f[e.cells[k].join(",")]) { sel.r = e.cells[k][0]; sel.c = e.cells[k][1]; return paint(true) } }
      if (e.cells.every(function (rc) { return st.f[rc.join(",")] })) { if (i < e.cells.length - 1) { sel.r = e.cells[i + 1][0]; sel.c = e.cells[i + 1][1]; return paint(true) } return nextClue(1) }
      for (k = 0; k < i; k++) { if (!st.f[e.cells[k].join(",")]) { sel.r = e.cells[k][0]; sel.c = e.cells[k][1]; return paint(true) } }
      paint(true);
    }
    function back() {
      if (st.done) return; var k = sel.r + "," + sel.c;
      if (st.f[k] && !(st.m && st.m[k] === "rev")) { delete st.f[k]; if (st.m) delete st.m[k] }
      else { var e = cur(), i = e.cells.findIndex(function (rc) { return rc[0] === sel.r && rc[1] === sel.c }); if (i > 0) { sel.r = e.cells[i - 1][0]; sel.c = e.cells[i - 1][1]; k = sel.r + "," + sel.c; if (!(st.m && st.m[k] === "rev")) { delete st.f[k]; if (st.m) delete st.m[k] } } }
      save("state", st); paint(true);
    }
    function sol(k) { var rc = k.split(","); return G[+rc[0]][+rc[1]] }
    function verify() {
      var keys = Object.keys(btn).filter(function (k) { return !btn[k].disabled }), full = keys.every(function (k) { return st.f[k] });
      if (!full) { status(""); return }
      if (keys.every(function (k) { return st.f[k] === sol(k) })) finish(true);
      else status("Every square is full. A few need another look; Check will show which.");
    }
    function status(t) { $("status").textContent = t }

    $("check").addEventListener("click", function () {
      if (st.done) return; st.m = st.m || {}; var any = false, wrong = 0;
      for (var k in st.f) { if (st.m[k] === "rev") continue; any = true; if (st.f[k] === sol(k)) st.m[k] = "ok"; else { st.m[k] = "bad"; wrong++ } }
      status(!any ? "Nothing to check yet." : wrong ? wrong + (wrong > 1 ? " squares need" : " square needs") + " another look." : "So far, so good.");
      save("state", st); paint(false);
    });
    $("reveal").addEventListener("click", function () {
      if (st.done) return; var e = cur(); if (!e) return; st.m = st.m || {}; st.help = true; startClock();
      e.cells.forEach(function (rc) { var k = rc.join(","); if (st.f[k] !== sol(k)) { st.f[k] = sol(k); st.m[k] = "rev" } });
      save("state", st); paint(true); verify();
    });

    document.addEventListener("keydown", function (ev) {
      if (ev.metaKey || ev.ctrlKey || ev.altKey) return;
      var t = ev.target, k = ev.key;
      if (t && t.closest && (t.closest(".site-nav") || t.closest(".site-foot") || t.closest("a"))) return;
      var inGrid = !!(t && t.classList && t.classList.contains("cell")), free = inGrid || t === document || t === document.body || t === document.documentElement;
      if (/^[a-z]$/i.test(k)) { ev.preventDefault(); typeL(k.toUpperCase()) }
      else if (k === "Backspace" || k === "Delete") { if (free || (t.classList && t.classList.contains("cl"))) { ev.preventDefault(); back() } }
      else if (!free) return;
      else if (k === "ArrowLeft") { ev.preventDefault(); move(0, -1) }
      else if (k === "ArrowRight") { ev.preventDefault(); move(0, 1) }
      else if (k === "ArrowUp") { ev.preventDefault(); move(-1, 0) }
      else if (k === "ArrowDown") { ev.preventDefault(); move(1, 0) }
      else if ((k === "Tab" || k === "Enter") && inGrid) { ev.preventDefault(); nextClue(ev.shiftKey ? -1 : 1) }
      else if (k === " " && inGrid) { ev.preventDefault(); toggleDir(); paint(true) }
    });
    document.addEventListener("visibilitychange", function () { if (document.hidden) stopClock(); else if (st.started && !st.done) startClock() });

    /* ---------- finish: the word, what it teaches, where it came from. No streaks. ---------- */
    function finish(fresh) {
  try { if (window.wellSense) wellSense.play('chime'); } catch (e) {}
      stopClock(); st.done = true; save("state", st);
      st.m = st.m || {}; for (var k in btn) { if (!btn[k].disabled && st.m[k] !== "rev") st.m[k] = "ok" }
      paint(false);
      kb.style.display = "none"; $("check").disabled = true; $("reveal").disabled = true;
      status("Solved in " + fmt(st.t) + (st.help ? ", with a little help." : "."));
      $("doneK").textContent = "Solved · " + fmt(st.t) + (st.help ? " · with help" : "");
      $("doneH").textContent = (cfg.wordLabel || "Today's word") + ": " + P.w.charAt(0) + P.w.slice(1).toLowerCase() + ".";
      $("doneP").textContent = P.n;
      var stats = $("stats"); if (stats) stats.style.display = "none";
      var box = $("srcs");
      if (box && P.sources && P.sources.length) {
        box.innerHTML = "";
        var h = document.createElement("p"); h.className = "srck"; h.textContent = "Where this came from"; box.appendChild(h);
        var ul = document.createElement("ul"); ul.className = "src";
        P.sources.forEach(function (s) {
          var li = document.createElement("li"), a = document.createElement("a");
          a.href = s.url; a.target = "_blank"; a.rel = "noopener"; a.textContent = s.title;
          li.appendChild(a); if (s.date) li.appendChild(document.createTextNode(" · " + s.date)); ul.appendChild(li);
        });
        box.appendChild(ul);
      }
      /* per-clue source links appear only after the solve, so they never give answers away */
      entries.forEach(function (e) {
        if (!e.src || e.li.querySelector(".s")) return;
        var a = document.createElement("a"); a.className = "s"; a.href = e.src; a.target = "_blank"; a.rel = "noopener"; a.textContent = "source";
        e.li.appendChild(a);
      });
      var d = $("done"); d.classList.add("show");
      if (fresh && d.scrollIntoView) setTimeout(function () { d.scrollIntoView({ behavior: "smooth", block: "nearest" }) }, 250);
    }
    var share = $("share");
    if (share) share.addEventListener("click", function () {
      var txt = cfg.title + " No. " + no + " · " + fmt(st.t) + (st.help ? " · with help" : "") + "\n" + cfg.shareUrl, ok = $("copied");
      function fallback() { try { var ta = document.createElement("textarea"); ta.value = txt; ta.style.position = "fixed"; ta.style.opacity = "0"; document.body.appendChild(ta); ta.select(); var r = document.execCommand("copy"); document.body.removeChild(ta); ok.textContent = r ? "Copied." : "Copy did not work here." } catch (e) { ok.textContent = "Copy did not work here." } }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(function () { ok.textContent = "Copied." }, fallback); else fallback();
    });

    /* ---------- start ---------- */
    document.documentElement.setAttribute("data-puzzle-from", from);
    showTime();
    go(entries[0], false);
    if (st.done) finish(false);
    if (cfg.onPlay) try { cfg.onPlay(P, from) } catch (e) { console.warn(e) }
  }

  window.Crossword = { mount: mount, check: check, slotsOf: slotsOf };
})();
