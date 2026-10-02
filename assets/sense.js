/* The Well · sound and touch, opt-in. No audio files: tiny synthesized sounds. Haptics where the browser allows (Android). Remembered per device only. */
(function () {
  var KEY = 'well.sense';
  var on = false;
  try { on = localStorage.getItem(KEY) === '1'; } catch (e) {}
  var ctx = null;
  function ac() { if (!ctx) { var A = window.AudioContext || window.webkitAudioContext; if (!A) return null; ctx = new A(); } if (ctx.state === 'suspended') { try { ctx.resume(); } catch (e) {} } return ctx; }
  function tone(f0, f1, dur, gain, type) {
    var c = ac(); if (!c) return; var t = c.currentTime;
    var o = c.createOscillator(), g = c.createGain();
    o.type = type || 'sine'; o.frequency.setValueAtTime(f0, t); if (f1) o.frequency.exponentialRampToValueAtTime(f1, t + dur);
    g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(gain, t + 0.006); g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    o.connect(g); g.connect(c.destination); o.start(t); o.stop(t + dur + 0.02);
  }
  var sounds = {
    click: function () { tone(1400, 900, 0.035, 0.05, 'triangle'); },     // a key, a tap: paper on paper
    place: function () { tone(520, 440, 0.09, 0.05, 'sine'); },           // something set down
    chime: function () { tone(660, 660, 0.12, 0.05, 'sine'); setTimeout(function () { tone(990, 990, 0.18, 0.045, 'sine'); }, 110); }, // a word lands, a grid finishes
    hush: function () { tone(220, 110, 0.5, 0.035, 'sine'); }             // a leaf goes under
  };
  function buzz(ms) { if (navigator.vibrate) { try { navigator.vibrate(ms); } catch (e) {} } }
  function play(kind) {
    if (!on) return;
    (sounds[kind] || sounds.click)();
    buzz(kind === 'chime' ? [12, 40, 18] : kind === 'hush' ? 24 : kind === 'place' ? 14 : 8);
  }
  window.wellSense = { play: play, isOn: function () { return on; } };

  // Generic hooks: taps on buttons, keys and game cells; the pages call wellSense.play('chime'|'place'|'hush') for their own moments.
  document.addEventListener('click', function (e) {
    var el = e.target.closest && e.target.closest('button, .key, .cell, .tile, a.card, a.shot, a.tile');
    if (el && !el.closest('.sense, .sense-head')) play('click');
  }, true);
  document.addEventListener('keydown', function (e) {
    if (e.key && e.key.length === 1 && !e.metaKey && !e.ctrlKey && !e.altKey) play('click');
  }, true);

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
    if (on) { ac(); sounds.chime(); buzz([12, 40, 18]); }
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
