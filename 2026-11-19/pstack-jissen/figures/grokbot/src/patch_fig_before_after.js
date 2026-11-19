// The fix was Claude Code's run, so both headings carry its black mochi character (eye: before looks at the stale pins, after looks up).
(function () {
  document.head.insertAdjacentHTML('beforeend', `<style>
  .gbw { display: inline-block; width: 40px; vertical-align: -6px; margin-right: 12px; }
  body.s1280 .gbw { width: 26px; margin-right: 8px; vertical-align: -4px; }
  .gbw svg { width: 100% !important; height: auto !important; }</style>`);
  const b = document.querySelector('.panel.before .when'), a = document.querySelector('.panel.after .when');
  b.insertAdjacentHTML('afterbegin', `<span class="gbw">${bot({ kind: 'mochi', color: '#000000', size: 40, look: [0.6, 0.6] })}</span>`);
  a.insertAdjacentHTML('afterbegin', `<span class="gbw">${bot({ kind: 'mochi', color: '#000000', size: 40, look: [0.7, -0.4] })}</span>`);
})();
