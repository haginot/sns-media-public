// pstack guide original characters (same design as banner/grokbot and figures/grokbot):
// ONE round eye with a pupil, a ball antenna, two little feet. Flat fills only.
// v2 adds an optional flat outline (`ring`) so the black bot reads on the night panel.
(function () {
  const BODY = {
    mochi: 'M10 80 C10 42 28 22 50 22 C72 22 90 42 90 80 C90 103 74 110 50 110 C26 110 10 103 10 80 Z',
    round: 'M50 24 C75 24 94 43 94 68 C94 93 75 110 50 110 C25 110 6 93 6 68 C6 43 25 24 50 24 Z',
    box: 'M36 24 L64 24 C82 24 92 34 92 52 L92 84 C92 102 82 110 64 110 L36 110 C18 110 8 102 8 84 L8 52 C8 34 18 24 36 24 Z',
  };
  window.bot = function ({ kind = 'mochi', color = '#000', size = 100, look = [0.3, 0], rot = 0, eyeY = 64, ring = '', sleepy = false } = {}) {
    const ex = 52, ey = eyeY, er = 16, pr = 7;
    const px = ex + look[0] * (er - pr - 1.5), py = ey + look[1] * (er - pr - 1.5);
    const st = ring ? ` stroke="${ring}" stroke-width="4" stroke-linejoin="round"` : '';
    const ant = `<rect x="47.5" y="8" width="5" height="18" rx="2.5" fill="${color}"${st}/><circle cx="50" cy="8" r="7" fill="${color}"${st}/>`;
    const ft = `<rect x="24" y="104" width="18" height="12" rx="6" fill="${color}"${st}/><rect x="58" y="104" width="18" height="12" rx="6" fill="${color}"${st}/>`;
    const eye = sleepy
      ? `<path d="M38 66 Q52 76 66 66" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/>`
      : `<circle cx="${ex}" cy="${ey}" r="${er}" fill="#FFFFFF"/><circle cx="${px}" cy="${py}" r="${pr}" fill="#111111"/>`;
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="-4 -2 108 124" width="${size}" height="${size * 124 / 108}" style="display:block;overflow:visible;transform:rotate(${rot}deg)">
      ${ant}${ft}<path d="${BODY[kind]}" fill="${color}"${st}/>${eye}</svg>`;
  };
  window.moon = function (size, bg) {
    return `<svg viewBox="0 0 100 100" width="${size}" height="${size}" style="display:block"><circle cx="50" cy="50" r="40" fill="#FFC531"/><circle cx="68" cy="38" r="34" fill="${bg}"/></svg>`;
  };
})();
