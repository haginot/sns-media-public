// Timeline cards: the rail keeps only its meaning (cloud: the person who stepped in; night: the moon).
// Each run gets its own original character in the card's open space.
(function () {
  const css = `
  .gbt { position: absolute; left: 50%; transform: translateX(-50%); top: 40px; }
  body.s1280 .gbt { top: 22px; }
  .gbt .hum { width: 40px; height: 72px; display:block } body.s1280 .gbt .hum { width: 24px; height: 43px; }
  .gbt .mn { width: 56px; height: 56px; display:block; margin-top: 8px } body.s1280 .gbt .mn { width: 32px; height: 32px; margin-top: 6px }
  .gbig { flex: 1; display: flex; align-items: center; justify-content: center; gap: 18px; min-height: 0; }
  .gbig .bb { width: 150px; } body.s1280 .gbig .bb { width: 82px; }
  .gbig .bb svg { width: 100% !important; height: auto !important; }`;
  document.head.insertAdjacentHTML('beforeend', `<style>${css}</style>`);
  const human = `<svg class="hum" viewBox="0 0 40 72"><circle cx="20" cy="11" r="10" fill="#111111"/><rect x="5" y="25" width="30" height="47" rx="12" fill="#FF6801"/></svg>`;
  const moon = `<svg class="mn" viewBox="0 0 34 34"><path fill="#1386FF" d="M22 2C14 4 9 11 9 19c0 6 3 10 7 13-9 0-16-7-16-16C0 7 8 0 17 0c2 0 3 1 5 2z"/></svg>`;
  const wrap = (inner) => { const d = document.createElement('div'); d.className = 'gbt'; d.innerHTML = inner; return d; };
  document.querySelectorAll('svg.person').forEach((s) => s.replaceWith(wrap(human)));
  document.querySelectorAll('svg.moon').forEach((s) => s.replaceWith(wrap(moon)));
  document.querySelectorAll('svg.gem').forEach((s) => s.remove());
  const looks = { cloud: { kind: 'box', color: '#FF6801', look: [0.2, -0.8] }, night: { kind: 'round', color: '#1386FF', look: [-0.6, -0.7] }, claude: { kind: 'mochi', color: '#000000', look: [0.7, 0.1] } };
  document.querySelectorAll('.run').forEach((run) => {
    const k = ['cloud', 'night', 'claude'].find((c) => run.classList.contains(c));
    const track = run.querySelector('.track');
    if (!k || !track) return;
    const g = document.createElement('div'); g.className = 'gbig';
    g.innerHTML = `<div class="bb">${bot({ ...looks[k], size: 150 })}</div>`;
    track.after(g);
  });
})();
