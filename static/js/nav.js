/* Mobile navigation toggle.
 *
 * Progressive enhancement: the stylesheet only collapses the nav behind this
 * button once `has-js` is on <html>, so with JavaScript disabled the links stay
 * visible and the site remains fully navigable.
 */
(function () {
  'use strict';

  var DESKTOP = '(min-width: 900px)';
  var button = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (!button || !nav) return;

  function setOpen(open) {
    nav.classList.toggle('is-open', open);
    button.setAttribute('aria-expanded', open ? 'true' : 'false');
  }

  function isOpen() {
    return nav.classList.contains('is-open');
  }

  button.addEventListener('click', function () {
    setOpen(!isOpen());
  });

  // Escape closes and returns focus to the button.
  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' && isOpen()) {
      setOpen(false);
      button.focus();
    }
  });

  // A tap outside the open panel dismisses it.
  document.addEventListener('click', function (event) {
    if (!isOpen()) return;
    if (nav.contains(event.target) || button.contains(event.target)) return;
    setOpen(false);
  });

  // Never leave the panel stranded open when the layout becomes two-column.
  var desktop = window.matchMedia(DESKTOP);
  var sync = function (event) {
    if (event.matches) setOpen(false);
  };
  if (desktop.addEventListener) {
    desktop.addEventListener('change', sync);
  } else if (desktop.addListener) {
    desktop.addListener(sync);
  }

  // Rotating a phone into landscape can cross the breakpoint without a change event.
  window.addEventListener('orientationchange', function () {
    if (desktop.matches) setOpen(false);
  });
})();
