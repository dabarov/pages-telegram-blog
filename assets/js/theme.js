/*
  Theme toggle utility
  - Immediately applies the saved or system theme via data-theme on <html>
  - Updates any .theme-toggle / #theme-toggle buttons with icons and ARIA
  - Persists preference in localStorage('theme')
  - Listens to system scheme changes when no manual preference is stored
*/
(function () {
  var storageKey = 'theme';
  var docEl = document.documentElement;
  var mql;

  function getStored() {
    try { return localStorage.getItem(storageKey) || null; } catch (e) { return null; }
  }
  function setStored(v) {
    try { localStorage.setItem(storageKey, v); } catch (e) {}
  }
  function systemPrefersDark() {
    try { mql = mql || window.matchMedia('(prefers-color-scheme: dark)'); return mql.matches; } catch (e) { return false; }
  }
  function initialTheme() {
    var saved = getStored();
    if (saved === 'dark' || saved === 'light') return saved;
    return systemPrefersDark() ? 'dark' : 'light';
  }
  function applyTheme(theme) {
    docEl.setAttribute('data-theme', theme);
  }
  function updateToggles(theme) {
    var isDark = theme === 'dark';
    var buttons = document.querySelectorAll('.theme-toggle, #theme-toggle');
    buttons.forEach(function (btn) {
      btn.textContent = isDark ? '☀️' : '🌙';
      btn.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
      btn.setAttribute('aria-pressed', String(isDark));
      btn.title = 'Toggle theme';
    });
  }
  function setupListeners() {
    var buttons = document.querySelectorAll('.theme-toggle, #theme-toggle');
    if (buttons.length) {
      buttons.forEach(function (btn) {
        btn.addEventListener('click', function () {
          var current = docEl.getAttribute('data-theme') || initialTheme();
          var next = current === 'dark' ? 'light' : 'dark';
          applyTheme(next);
          setStored(next);
          updateToggles(next);
        });
      });
    }

    try {
      mql = mql || window.matchMedia('(prefers-color-scheme: dark)');
      var onChange = function (e) {
        if (!getStored()) {
          var auto = e.matches ? 'dark' : 'light';
          applyTheme(auto);
          updateToggles(auto);
        }
      };
      if (mql.addEventListener) mql.addEventListener('change', onChange);
      else if (mql.addListener) mql.addListener(onChange);
    } catch (e) {}
  }

  // Apply early to minimize flash of wrong theme
  var initial = initialTheme();
  applyTheme(initial);

  // DOM-dependent work
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      updateToggles(initial);
      setupListeners();
    });
  } else {
    updateToggles(initial);
    setupListeners();
  }
})();
