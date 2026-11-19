// Minimal isometric (30°) diagram helpers. Coordinates: grid units (x right-down, y left-down, z up).
const Iso = (() => {
  const NS = 'http://www.w3.org/2000/svg', C = Math.cos(Math.PI/6), S = 0.5;
  let svg, U = 100, OX = 800, OY = 450;
  const el = (tag, attrs = {}, parent = svg) => { const e = document.createElementNS(NS, tag);
    for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v); parent.appendChild(e); return e; };
  const P = (x, y, z = 0) => [OX + (x - y) * C * U, OY + (x + y) * S * U - z * U];
  const pts = a => a.map(p => P(...p).map(n => n.toFixed(2)).join(',')).join(' ');
  function init({ theme, unit = 100, origin = [800, 450] }) {
    document.body.className = theme; U = unit; [OX, OY] = origin;
    svg = document.getElementById('fig');
    const d = el('defs');
    const g = el('linearGradient', { id: 'pv', gradientUnits: 'userSpaceOnUse', x1: 0, y1: 0, x2: 1600, y2: 0 }, d);
    [['0', '#CD1DFB'], ['0.5', '#8745E3'], ['1', '#237FC0']].forEach(([o, c]) => el('stop', { offset: o, 'stop-color': c }, g));
    const m = el('marker', { id: 'ah', viewBox: '0 0 10 10', refX: 8.5, refY: 5, markerWidth: 7, markerHeight: 7, orient: 'auto-start-reverse', markerUnits: 'userSpaceOnUse' }, d);
    m.setAttribute('markerWidth', 14); m.setAttribute('markerHeight', 14);
    el('path', { d: 'M0,1 L10,5 L0,9 z', fill: 'context-stroke' }, m);
    return svg;
  }
  // faint triangular lattice (the "diamond grid"), clipped to a rect
  function lattice({ step = 0.5, rect = [0, 0, 1600, 900] } = {}) {
    const g = el('g', { stroke: 'var(--lattice)', 'stroke-width': 1 });
    const [rx, ry, rw, rh] = rect, s = step * U, dx = s * C * 2;   // spacing of vertical lines = s*C*... keep lattice regular
    const vx = s * C;                                              // vertical line spacing
    for (let x = OX % vx; x < 1600; x += vx) if (x >= rx && x <= rx + rw) el('line', { x1: x, y1: ry, x2: x, y2: ry + rh }, g);
    const span = 2400, k = Math.tan(Math.PI / 6);
    for (let i = -60; i < 60; i++) {           // ±30° families through the origin lattice
      const b = OY + i * s;                     // vertical intercept spacing = s
      el('line', { x1: OX - span, y1: b - span * k, x2: OX + span, y2: b + span * k }, g);
      el('line', { x1: OX - span, y1: b + span * k, x2: OX + span, y2: b - span * k }, g);
    }
    const cp = el('clipPath', { id: 'latclip' }, svg.querySelector('defs')); el('rect', { x: rx, y: ry, width: rw, height: rh }, cp);
    g.setAttribute('clip-path', 'url(#latclip)'); return g;
  }
  function plate(x0, y0, x1, y1, z = 0, o = {}) {
    return el('polygon', { points: pts([[x0, y0, z], [x1, y0, z], [x1, y1, z], [x0, y1, z]]),
      fill: o.fill ?? 'var(--plate)', stroke: o.stroke ?? 'var(--plateLine)', 'stroke-width': o.sw ?? 1.5,
      'stroke-dasharray': o.dash ?? 'none' }, o.parent);
  }
  // extruded box; visible faces: top, y-max side (left), x-max side (right)
  function box(x, y, w, d, h, z = 0, o = {}) {
    const g = el('g', {}, o.parent), st = o.stroke ?? 'var(--edge)', sw = o.sw ?? 1.5;
    const X = x + w, Y = y + d, Z = z + h;
    if (h > 0) {
      el('polygon', { points: pts([[x, Y, z], [X, Y, z], [X, Y, Z], [x, Y, Z]]), fill: o.sideA ?? 'var(--sideA)', stroke: st, 'stroke-width': sw, 'stroke-linejoin': 'round' }, g);
      el('polygon', { points: pts([[X, y, z], [X, Y, z], [X, Y, Z], [X, y, Z]]), fill: o.sideB ?? 'var(--sideB)', stroke: st, 'stroke-width': sw, 'stroke-linejoin': 'round' }, g);
    }
    el('polygon', { points: pts([[x, y, Z], [X, y, Z], [X, Y, Z], [x, Y, Z]]), fill: o.top ?? 'var(--top)', stroke: o.topStroke ?? st, 'stroke-width': o.topSw ?? sw, 'stroke-linejoin': 'round' }, g);
    return g;
  }
  function line(path, o = {}) {
    return el('polyline', { points: pts(path), fill: 'none', stroke: o.stroke ?? 'var(--ink)', 'stroke-width': o.sw ?? 2,
      'stroke-dasharray': o.dash ?? 'none', 'stroke-linejoin': 'round', 'stroke-linecap': o.cap ?? 'butt',
      ...(o.arrow ? { 'marker-end': 'url(#ah)' } : {}) }, o.parent);
  }
  function text(str, at, o = {}) {
    const [sx, sy] = Array.isArray(at[0]) ? at[0] : (at.length === 2 && o.screen ? at : P(...at));
    const t = el('text', { x: sx + (o.dx ?? 0), y: sy + (o.dy ?? 0), class: o.cls ?? 't-jp', 'font-size': o.size ?? 24,
      'text-anchor': o.anchor ?? 'middle', 'dominant-baseline': o.base ?? 'middle', ...(o.fill ? { fill: o.fill } : {}) }, o.parent);
    t.textContent = str; return t;
  }
  function dot(at, r = 5, o = {}) { const [x, y] = P(...at); return el('circle', { cx: x, cy: y, r, fill: o.fill ?? 'var(--ink)', stroke: o.stroke ?? 'none', 'stroke-width': o.sw ?? 0 }, o.parent); }
  function html(cls, inner, style) { const d = document.createElement('div'); d.className = cls; d.innerHTML = inner;
    Object.assign(d.style, style); document.getElementById('stage').appendChild(d); return d; }
  // text drawn ON an isometric side face. face 'L' (y-max face, runs along +x) or 'R' (x-max face, runs along −y).
  // at = grid point of the text anchor (baseline middle), anchor default middle.
  function faceText(str, at, face = 'L', o = {}) {
    const [sx, sy] = P(...at), m = face === 'L' ? [C, S, 0, 1] : face === 'R' ? [C, -S, 0, 1] : [C, S, -C, S];  // 'G' = lying on the ground, along +x
    const t = el('text', { transform: `matrix(${m[0]},${m[1]},${m[2]},${m[3]},${sx.toFixed(2)},${sy.toFixed(2)})`, x: 0, y: 0,
      class: o.cls ?? 't-mono', 'font-size': o.size ?? 13, 'text-anchor': o.anchor ?? 'middle', 'dominant-baseline': 'middle',
      ...(o.fill ? { fill: o.fill } : {}) }, o.parent);
    t.textContent = str; return t;
  }
  // choose unit + origin so that grid points fit a screen rect [x, y, w, h]
  function fit(points, [rx, ry, rw, rh], maxU = 160) {
    const raw = points.map(([x, y, z = 0]) => [(x - y) * C, (x + y) * S - z]);
    const xs = raw.map(p => p[0]), ys = raw.map(p => p[1]);
    const w = Math.max(...xs) - Math.min(...xs), h = Math.max(...ys) - Math.min(...ys);
    U = Math.min(rw / w, rh / h, maxU);
    OX = rx + (rw - w * U) / 2 - Math.min(...xs) * U; OY = ry + (rh - h * U) / 2 - Math.min(...ys) * U; return U;
  }
  function shift(dx, dy) { OX += dx; OY += dy; }
  return { init, fit, shift, faceText, P, el, lattice, plate, box, line, text, dot, html, get U() { return U; } };
})();
