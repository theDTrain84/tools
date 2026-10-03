/* tools.dnsc.ai: page continuity. Fade in on load, fade out before leaving for
   another page here or on dustinnimmo.com. Skips new-tab and modified clicks, hash links
   and downloads, and respects prefers-reduced-motion. */
(function () {
  var d = document, b = d.body, root = d.documentElement;
  if (!b || window.__dnShell) return; window.__dnShell = 1;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)');
  // Pages that do not load site.css still get the fade out and view transitions.
  if (!getComputedStyle(root).getPropertyValue('--dn-shell')) {
    var s = d.createElement('style');
    s.textContent = '@view-transition{navigation:auto}body.is-leaving{opacity:0;transition:opacity .22s ease-in}' +
      '@media (prefers-reduced-motion:reduce){@view-transition{navigation:none}body.is-leaving{opacity:1;transition:none}}';
    d.head.appendChild(s);
  }
  requestAnimationFrame(function () { b.classList.add('is-ready'); });
  var crossDocVT = 'onpagereveal' in window;
  d.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!a || a.hasAttribute('download')) return;
    var t = a.getAttribute('target'); if (t && t !== '_self') return;
    var raw = a.getAttribute('href'); if (!raw || raw.charAt(0) === '#') return;
    var u; try { u = new URL(a.href, location.href); } catch (_) { return; }
    if (!/^(https?|file):$/.test(u.protocol)) return;
    var here = u.origin === location.origin;
    if (!here && !/(^|\.)(dnsc\.ai|dustinnimmo\.com)$/.test(u.hostname)) return;
    if (u.pathname === location.pathname && u.search === location.search && u.hash) return;
    if (reduce && reduce.matches) return;
    if (here && crossDocVT) return; // the browser's view transition carries it
    e.preventDefault();
    b.classList.add('is-leaving');
    setTimeout(function () { location.href = u.href; }, 220);
  });
  addEventListener('pageshow', function (e) { if (e.persisted) b.classList.remove('is-leaving'); });
})();
