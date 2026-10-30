// Alternância de tema (automático → claro → escuro), guardada em localStorage.
// Carregado no <head> para aplicar o tema salvo antes da primeira pintura.
(function () {
  'use strict';
  var root = document.documentElement;
  var THEMES = ['auto', 'light', 'dark'];
  var ICONS = {
    auto: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 1 0 18z" fill="currentColor" stroke="none"/></svg>',
    light: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    dark: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>'
  };
  var LABELS = { auto: 'Tema: automático', light: 'Tema: claro', dark: 'Tema: escuro' };

  function getTheme() {
    try { var t = localStorage.getItem('theme'); return THEMES.indexOf(t) >= 0 ? t : 'auto'; }
    catch (e) { return 'auto'; }
  }
  function applyTheme(t, btn) {
    if (t === 'auto') root.removeAttribute('data-theme'); else root.setAttribute('data-theme', t);
    if (btn) {
      btn.querySelector('.ico').innerHTML = ICONS[t];
      btn.querySelector('.lbl').textContent = LABELS[t];
    }
  }

  applyTheme(getTheme(), null);

  document.addEventListener('DOMContentLoaded', function () {
    var btn = document.getElementById('theme-btn');
    if (!btn) return;
    applyTheme(getTheme(), btn);
    btn.addEventListener('click', function () {
      var next = THEMES[(THEMES.indexOf(getTheme()) + 1) % THEMES.length];
      try { localStorage.setItem('theme', next); } catch (e) {}
      applyTheme(next, btn);
    });
  });
})();
