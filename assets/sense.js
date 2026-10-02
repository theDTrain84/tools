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
    if (el && !el.closest('.sense')) play('click');
  }, true);
  document.addEventListener('keydown', function (e) {
    if (e.key && e.key.length === 1 && !e.metaKey && !e.ctrlKey && !e.altKey) play('click');
  }, true);

  // The tiny line
  function render() {
    var host = document.querySelector('.site-foot .in') || document.body;
    var line = document.createElement('p'); line.className = 'sense';
    var iosNote = /iPhone|iPad/.test(navigator.userAgent) ? ' (sound here; iPhone keeps its haptics to apps)' : '';
    line.innerHTML = '<button type="button" aria-pressed="' + on + '">' + (on ? 'Sound and touch: on' : 'For sound and touch, turn on here') + '</button><span>' + iosNote + '</span>';
    line.querySelector('button').addEventListener('click', function () {
      on = !on; try { localStorage.setItem(KEY, on ? '1' : '0'); } catch (e) {}
      this.setAttribute('aria-pressed', on); this.textContent = on ? 'Sound and touch: on' : 'For sound and touch, turn on here';
      if (on) { ac(); sounds.chime(); buzz([12, 40, 18]); }
    });
    host.appendChild(line);
    var st = document.createElement('style');
    st.textContent = '.sense{flex-basis:100%;margin:6px 0 0;font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:11.5px;letter-spacing:.08em}.sense button{all:unset;cursor:pointer;color:#D9B25A;text-decoration:underline;text-decoration-color:rgba(217,178,90,.5);text-underline-offset:3px}.sense button:focus-visible{outline:2px solid #3E6A9E;outline-offset:3px}.sense span{color:#7A6A5D}';
    document.head.appendChild(st);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', render); else render();
})();
