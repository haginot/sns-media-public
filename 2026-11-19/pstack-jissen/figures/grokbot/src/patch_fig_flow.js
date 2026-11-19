// Each run's own character stands at the end of its bar (Claude Code stops at 7 of 8).
(function () {
  document.head.insertAdjacentHTML('beforeend', `<style>
  .gbr { position: absolute; bottom: calc(100% + 2px); width: 52px; transform: translateX(-50%); }
  body.s1280 .gbr { width: 30px; }
  .gbr svg { width: 100% !important; height: auto !important; }</style>`);
  const looks = { cloud: { kind: 'box', color: '#FF6801' }, night: { kind: 'round', color: '#1386FF' }, claude: { kind: 'mochi', color: '#000000' } };
  document.querySelectorAll('.run').forEach((run) => {
    const k = ['cloud', 'night', 'claude'].find((c) => run.classList.contains(c));
    const bar = run.querySelector('.bar');
    if (!k || !bar) return;
    const d = document.createElement('div'); d.className = 'gbr';
    d.style.left = k === 'claude' ? '87.5%' : 'calc(100% - 26px)';
    d.innerHTML = bot({ ...looks[k], size: 40, look: [0.8, 0] });
    bar.appendChild(d);
  });
})();
