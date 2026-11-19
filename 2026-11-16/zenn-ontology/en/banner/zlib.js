// shared helpers for the Tech Blog figures (on top of iso.js)
const Z = (() => {
  const theme = new URLSearchParams(location.search).get('theme') || 'dark';
  const div = (cls, inner, style = {}) => { const d = document.createElement('div'); d.className = cls; d.innerHTML = inner;
    Object.assign(d.style, style); document.getElementById('stage').appendChild(d); return d; };
  const px = v => typeof v === 'number' ? v + 'px' : v;
  // place a block; anchor: 'l' (left edge at x), 'r' (right edge at x), 'c' (centered); vertical: 'm' middle, 't' top, 'b' bottom
  function at(cls, inner, x, y, { w = 400, a = 'l', v = 'm', style = {} } = {}) {
    const d = div(cls, inner, { position: 'absolute', width: px(w), textAlign: a === 'r' ? 'right' : a === 'c' ? 'center' : 'left', ...style });
    const left = a === 'l' ? x : a === 'r' ? x - w : x - w / 2; d.style.left = px(left);
    const h = d.getBoundingClientRect().height; d.style.top = px(v === 't' ? y : v === 'b' ? y - h : y - h / 2); return d;
  }
  function setup({ unit = 100, origin = [800, 450], lattice = true, latticeRect } = {}) {
    Iso.init({ theme, unit, origin }); if (lattice) Iso.lattice({ step: 0.5, rect: latticeRect || [0, 0, 1600, 900] });
  }
  const title = html => div('title', html);
  const fict = text => div('fict', text);
  // rect outline in screen space (used for gradient enclosures)
  function rect(x, y, w, h, o = {}) { return Iso.el('rect', { x, y, width: w, height: h, rx: o.rx ?? 8, fill: o.fill ?? 'none', stroke: o.stroke ?? 'url(#pv)', 'stroke-width': o.sw ?? 2, 'stroke-dasharray': o.dash ?? 'none' }); }
  function sline(x1, y1, x2, y2, o = {}) { return Iso.el('line', { x1, y1, x2, y2, stroke: o.stroke ?? 'var(--link)', 'stroke-width': o.sw ?? 2, 'stroke-dasharray': o.dash ?? 'none', ...(o.arrow ? { 'marker-end': 'url(#ah)' } : {}) }); }
  function cross(x, y, r = 11, color = 'var(--deny)') {
    Iso.el('circle', { cx: x, cy: y, r: r + 6, fill: 'var(--bg)', stroke: color, 'stroke-width': 3 });
    Iso.el('path', { d: `M${x - r / 2},${y - r / 2} L${x + r / 2},${y + r / 2} M${x + r / 2},${y - r / 2} L${x - r / 2},${y + r / 2}`, stroke: color, 'stroke-width': 3.5, 'stroke-linecap': 'round' });
  }
  return { theme, div, at, setup, title, fict, rect, sline, cross, done: () => { window.FIG_READY = true; } };
})();
