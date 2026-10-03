/* The Well · sound and touch, opt-in. No audio files: tiny synthesized sounds. Haptics where the browser allows (Android). Remembered per device only. */
(function () {
  var KEY = 'well.sense';
  var on = false;
  try { on = localStorage.getItem(KEY) === '1'; } catch (e) {}
  // One small engine: master gain into a gentle compressor, a shared noise buffer, and a shared delay tail for the bell.
  var ctx = null, out = null, wet = null, noise = null, quietUntil = 0, lastTick = 0; // tick stays in the palette; nothing fires it on hover
  function ac() {
    if (!ctx) {
      var A = window.AudioContext || window.webkitAudioContext; if (!A) return null;
      try { ctx = new A(); } catch (e) { return null; }
      var comp = ctx.createDynamicsCompressor();
      comp.threshold.value = -18; comp.ratio.value = 3; comp.knee.value = 12; comp.attack.value = 0.003; comp.release.value = 0.2;
      out = ctx.createGain(); out.gain.value = 0.9; out.connect(comp); comp.connect(ctx.destination);
      // Bell tail: a feedback delay through a lowpass, sent in on a wet gain
      wet = ctx.createGain(); wet.gain.value = 0.25;
      var dl = ctx.createDelay(1), fb = ctx.createGain(), lp = ctx.createBiquadFilter();
      dl.delayTime.value = 0.12; fb.gain.value = 0.3; lp.type = 'lowpass'; lp.frequency.value = 3000;
      wet.connect(dl); dl.connect(lp); lp.connect(fb); fb.connect(dl); lp.connect(out);
      var n = ctx.sampleRate | 0, b = ctx.createBuffer(1, n, ctx.sampleRate), d = b.getChannelData(0);
      for (var i = 0; i < n; i++) d[i] = Math.random() * 2 - 1;
      noise = b;
    }
    if (ctx.state === 'suspended') { try { ctx.resume(); } catch (e) {} }
    return ctx;
  }
  function env(c, peak, t, atk, dur) {
    var g = c.createGain();
    g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(peak, t + atk); g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    return g;
  }
  function osc(c, f0, f1, t, dur, peak, atk, detune, dest) {
    var o = c.createOscillator(), g = env(c, peak, t, atk, dur);
    o.frequency.setValueAtTime(f0, t); if (f1) o.frequency.exponentialRampToValueAtTime(f1, t + dur);
    if (detune) o.detune.value = detune;
    o.connect(g); g.connect(dest || out); o.start(t); o.stop(t + dur + 0.03);
    return g;
  }
  function hiss(c, type, freq, q, t, dur, peak, atk, to) {
    var s = c.createBufferSource(), f = c.createBiquadFilter(), g = env(c, peak, t, atk, dur);
    s.buffer = noise; f.type = type; f.frequency.setValueAtTime(freq, t); if (to) f.frequency.exponentialRampToValueAtTime(to, t + dur); f.Q.value = q;
    s.connect(f); f.connect(g); g.connect(out);
    s.start(t, Math.random() * 0.4); s.stop(t + dur + 0.03);
  }
  function bell(c, f, t) {
    var g = osc(c, f, 0, t, 0.22, 0.04, 0.004);          // the note
    g.connect(wet);
    osc(c, f * 2, 0, t, 0.22, 0.012, 0.004).connect(wet); // a touch of the 2nd harmonic
  }
  var sounds = {
    // a soft paper tap: felt and paper, a breath of band-passed noise over a tiny low thump
    tap: function (c, t) { hiss(c, 'bandpass', 1100, 1, t, 0.018, 0.022, 0.002); osc(c, 120, 0, t, 0.04, 0.02, 0.003); },
    // almost subliminal: the edge of a page passing under a fingertip
    tick: function (c, t) { hiss(c, 'highpass', 4000, 0, t, 0.008, 0.012, 0.001); },
    // something set down: a card sliding on cloth, no tones, barely there
    place: function (c, t) { hiss(c, 'lowpass', 900, 0.7, t, 0.16, 0.028, 0.01, 250); },
    // a word lands, a grid finishes: three soft bells and a short tail, a little gift
    chime: function (c, t) { bell(c, 659.25, t); bell(c, 987.77, t + 0.09); bell(c, 1318.51, t + 0.18); },
    // a leaf goes under: the low sine sinks, and a breath of wind goes with it
    hush: function (c, t) { osc(c, 220, 110, t, 0.5, 0.035, 0.006); hiss(c, 'lowpass', 700, 0.5, t, 0.5, 0.014, 0.08); }
  };
  sounds.click = sounds.tap;
  var BUZZ = { chime: [12, 40, 18], hush: 24, place: 14, tap: 8, click: 8 };
  function buzz(p) { if (p && navigator.vibrate) { try { navigator.vibrate(p); } catch (e) {} } }
  function sound(kind) { var c = ac(); if (!c || !out) return; try { (sounds[kind] || sounds.tap)(c, c.currentTime + 0.005); } catch (e) {} }
  function play(kind) {
    if (!on) return;
    var now = Date.now(); if (now < quietUntil) return;
    if (kind === 'tick') { if (now - lastTick < 90) return; lastTick = now; }
    sound(kind); buzz(BUZZ[kind] || 0);
  }
  window.wellSense = { play: play, isOn: function () { return on; } };

  // Generic hooks: taps on buttons, keys, game cells and card links; no sounds on hover; the pages call wellSense.play('chime'|'place'|'hush') for their own moments.
  function mine(el) { return el.closest('.sense, .sense-head'); }
  document.addEventListener('click', function (e) {
    var el = e.target.closest && e.target.closest('button, [role=button], .key, .cell, .tile, a.card, a.shot, a.tile');
    if (el && !mine(el)) play('tap');
  }, true);
  function typing(t) {
    if (!t || t === document || t === document.body || t === document.documentElement) return !!document.querySelector('.cell, .key');
    if (t.isContentEditable || t.tagName === 'TEXTAREA') return true;
    if (t.tagName === 'INPUT') return /^(text|search|email|url|tel|password|number)?$/.test(t.type || '');
    return !!(t.classList && (t.classList.contains('cell') || t.classList.contains('key')));
  }
  document.addEventListener('keydown', function (e) {
    if (e.key && e.key.length === 1 && !e.metaKey && !e.ctrlKey && !e.altKey && !e.repeat && typing(e.target)) play('tap');
  }, true);
  // Wake the audio on the first gesture of a visit (browsers keep it asleep until then)
  function wake() { if (on) ac(); document.removeEventListener('pointerdown', wake, true); document.removeEventListener('keydown', wake, true); }
  document.addEventListener('pointerdown', wake, true); document.addEventListener('keydown', wake, true);

  // The toggle: a small ripple mark in the header on every page, and a quiet line in the footer. Both stay in sync.
  var SVG = '<svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true" focusable="false"><circle cx="4" cy="8" r="1.6" fill="currentColor"/><g class="w" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round"><path d="M7.4 5.4a3.6 3.6 0 0 1 0 5.2"/><path d="M10.2 3.2a6.6 6.6 0 0 1 0 9.6"/></g><g class="rp" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round"><path d="M7.4 5.4a3.6 3.6 0 0 1 0 5.2"/><path d="M10.2 3.2a6.6 6.6 0 0 1 0 9.6"/></g></svg>';
  var heads = [], feet = [];
  function footText() { return on ? 'Sound and touch: on' : 'Sound and touch: off, turn on here'; }
  function sync(ripple) {
    heads.forEach(function (b) {
      b.setAttribute('aria-pressed', on); b.title = 'Sound and touch: ' + (on ? 'on' : 'off');
      b.classList.toggle('is-on', on); b.classList.remove('ripple');
      if (ripple) { void b.offsetWidth; b.classList.add('ripple'); }
    });
    feet.forEach(function (b) { b.setAttribute('aria-pressed', on); b.textContent = footText(); });
  }
  function toggle() {
    on = !on; try { localStorage.setItem(KEY, on ? '1' : '0'); } catch (e) {}
    sync(on);
    // Turning on: the first thing heard is the bell, then a short hush so nothing crowds it
    if (on) { ac(); quietUntil = Date.now() + 460; setTimeout(function () { if (on) sound('chime'); }, 60); buzz([12, 40, 18]); }
  }
  function isDark(el) {
    var m = getComputedStyle(el).backgroundColor.match(/[\d.]+/g);
    if (!m) return false;
    return (0.299 * m[0] + 0.587 * m[1] + 0.114 * m[2]) < 128 && (m[3] === undefined || +m[3] > 0.3);
  }
  function render() {
    // Header: inside the shared nav, just before the cta. Standalone tools have no shared nav, so the mark sits at the right of their top bar.
    var nav = document.querySelector('.site-nav .in'), bar = document.querySelector('.dnsc-back');
    var hb = document.createElement('button'); hb.type = 'button'; hb.className = 'sense-head';
    hb.setAttribute('aria-label', 'Sound and touch'); hb.innerHTML = SVG;
    hb.addEventListener('click', toggle);
    if (nav) {
      if (isDark(document.querySelector('.site-nav'))) hb.classList.add('on-dark');
      var cta = nav.querySelector('.cta'), links = nav.querySelector('.links');
      if (cta) nav.insertBefore(hb, cta); else if (links) links.appendChild(hb); else nav.appendChild(hb);
      heads.push(hb);
    } else if (bar) {
      hb.classList.add('in-bar'); bar.classList.add('has-sense'); bar.appendChild(hb); heads.push(hb);
    }
    // Footer line
    var host = document.querySelector('.site-foot .in') || document.body;
    var line = document.createElement('p'); line.className = 'sense';
    var iosNote = /iPhone|iPad/.test(navigator.userAgent) ? ' (sound here; iPhone keeps its haptics to apps)' : '';
    line.innerHTML = '<button type="button"></button><span>' + iosNote + '</span>';
    var fb = line.querySelector('button'); fb.addEventListener('click', toggle); feet.push(fb);
    host.appendChild(line);
    sync(false);
    var st = document.createElement('style');
    st.textContent =
      '.sense{flex-basis:100%;margin:6px 0 0;font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:11.5px;letter-spacing:.08em}.sense button{all:unset;cursor:pointer;color:#D9B25A;text-decoration:underline;text-decoration-color:rgba(217,178,90,.5);text-underline-offset:3px}.sense button:focus-visible{outline:2px solid #3E6A9E;outline-offset:3px}.sense span{color:#7A6A5D}' +
      '.sense-head{all:unset;box-sizing:border-box;flex:none;width:32px;height:32px;display:inline-flex;align-items:center;justify-content:center;border-radius:50%;cursor:pointer;color:#7A6A5D;margin:0 -10px 0 -8px;transition:color .3s ease,background-color .3s ease;-webkit-tap-highlight-color:transparent}' +
      '.sense-head.on-dark{color:#A69686}.sense-head.in-bar{margin:-6px -6px -6px auto;color:inherit;opacity:.85}' +
      '.sense-head:hover{background:rgba(127,112,96,.12)}.sense-head:focus-visible{outline:2px solid #3E6A9E;outline-offset:1px}' +
      '.sense-head svg{display:block;overflow:visible}.sense-head .w{opacity:.35;transition:opacity .3s ease}.sense-head .rp{opacity:0;transform-origin:4px 8px}' +
      '.sense-head.is-on,.sense-head.in-bar.is-on{color:#D9B25A;opacity:1}.sense-head.is-on .w{opacity:1}' +
      '.sense-head.ripple .rp{animation:sense-rp 1.2s ease-out 1}' +
      '@keyframes sense-rp{0%{opacity:.9;transform:scale(1)}100%{opacity:0;transform:scale(1.9)}}' +
      '.dnsc-back.has-sense{display:flex;align-items:center;flex-wrap:nowrap}' +
      '@media (max-width:720px){.site-nav .in{gap:12px}.sense-head{margin:0 -8px 0 -6px}}' +
      '@media (max-width:420px){.site-nav .in{gap:10px;padding-left:16px;padding-right:16px}.site-nav .cta{padding:9px 10px;font-size:11px;letter-spacing:-.01em}}' +
      '@media (max-width:384px){.site-nav .links{display:none}}' +
      '@media (prefers-reduced-motion:reduce){.sense-head,.sense-head .w{transition:none}.sense-head.ripple .rp{animation:none}}';
    document.head.appendChild(st);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', render); else render();
})();
