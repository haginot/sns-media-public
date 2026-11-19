// pstack guide original characters ("てくぼ"): our own design that only shares the
// Grok Bot tone (flat fills, chubby shapes, bright palette). Deliberately different
// from the official characters: ONE round eye with a pupil, an antenna with a ball,
// and two little feet. Flat fills only: no gradient, blur or transparency.
(function () {
  const BODY = {
    mochi: 'M10 80 C10 42 28 22 50 22 C72 22 90 42 90 80 C90 103 74 110 50 110 C26 110 10 103 10 80 Z',
    round: 'M50 24 C75 24 94 43 94 68 C94 93 75 110 50 110 C25 110 6 93 6 68 C6 43 25 24 50 24 Z',
    box: 'M36 24 L64 24 C82 24 92 34 92 52 L92 84 C92 102 82 110 64 110 L36 110 C18 110 8 102 8 84 L8 52 C8 34 18 24 36 24 Z',
  };
  // look: [dx, dy] pupil offset in -1..1
  window.bot = function ({ kind = 'mochi', color = '#000', size = 100, look = [0.3, 0], rot = 0, eyeY = 64, feet = true, antenna = true } = {}) {
    const ex = 52, ey = eyeY, er = 16, pr = 7;
    const px = ex + look[0] * (er - pr - 1.5), py = ey + look[1] * (er - pr - 1.5);
    const ant = antenna ? `<rect x="47.5" y="8" width="5" height="18" rx="2.5" fill="${color}"/><circle cx="50" cy="8" r="7" fill="${color}"/>` : '';
    const ft = feet ? `<rect x="24" y="104" width="18" height="12" rx="6" fill="${color}"/><rect x="58" y="104" width="18" height="12" rx="6" fill="${color}"/>` : '';
    const h = size * 1.2;
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 120" width="${size}" height="${h}" style="display:block;overflow:visible;transform:rotate(${rot}deg)">
      ${ant}${ft}<path d="${BODY[kind]}" fill="${color}"/>
      <circle cx="${ex}" cy="${ey}" r="${er}" fill="#FFFFFF"/><circle cx="${px}" cy="${py}" r="${pr}" fill="#111111"/></svg>`;
  };
  window.placeBots = function (root = document) {
    root.querySelectorAll('[data-bot]').forEach((el) => {
      const o = JSON.parse(el.dataset.bot);
      o.size = o.size ?? el.getBoundingClientRect().width;
      el.innerHTML = bot(o);
    });
  };
  window.GB = { ink: '#111111', black: '#000000', blue: '#1386FF', purple: '#9259FE', pink: '#FF309C', orange: '#FF6801', amber: '#FF9700', teal: '#00BBA6', brown: '#97683E', grey: '#777777', bg: '#F4F5F7', line: '#E3E5EA' };
})();
