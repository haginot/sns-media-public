// Generic restyle pass: thick navy frames -> thin light lines + rounded corners; arrows -> soft grey.
(function () {
  const stage = document.getElementById('stage');
  const LINE = '#E1E3E8', ARROW = '#B7BBC2';
  const isInk = (c) => c === 'rgb(17, 17, 17)';
  stage.querySelectorAll('*').forEach((el) => {
    if (el.closest('svg')) return;
    const cs = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    const bw = parseFloat(cs.borderTopWidth) || 0, blw = parseFloat(cs.borderLeftWidth) || 0;
    const triangle = r.width < 2 || r.height < 2 || cs.borderTopColor === 'rgba(0, 0, 0, 0)' && blw > 4;
    const cls = String(el.className || '');
    if (triangle) {
      ['Top', 'Right', 'Bottom', 'Left'].forEach((s) => { if (isInk(cs['border' + s + 'Color'])) el.style['border' + s + 'Color'] = ARROW; });
      return;
    }
    if (/(^|\s|-)arr(ow)?(\s|$|-)|rail/.test(cls) && isInk(cs.backgroundColor)) el.style.backgroundColor = ARROW;
    if (bw >= 2 && cs.borderTopStyle === 'solid') {
      el.style.borderWidth = '1.5px';
      el.style.borderColor = LINE;
      const small = Math.min(r.width, r.height);
      el.style.borderRadius = (small < 70 ? 10 : small < 200 ? 16 : 22) + 'px';
      if (cs.backgroundColor === 'rgb(255, 255, 255)') el.style.boxShadow = '0 2px 0 #E6E8EC';
    } else if (bw >= 2 && cs.borderTopStyle === 'dashed') {
      el.style.borderWidth = '2px'; el.style.borderRadius = '14px';
    }
    if (cs.borderBottomStyle === 'solid' && parseFloat(cs.borderBottomWidth) >= 1 && bw < 2 && isInk(cs.borderBottomColor)) {
      el.style.borderBottomColor = LINE;
    }
    if (cs.borderTopStyle === 'solid' && bw >= 1 && bw < 2 && isInk(cs.borderTopColor)) el.style.borderTopColor = LINE;
  });
  // credit
  const fig = stage.querySelector('.fig-no');
  if (fig && !fig.dataset.credit) { fig.dataset.credit = 1; fig.insertAdjacentHTML('beforeend', '<span style="font-weight:400;color:#5F6368">　作図：萩野貴拓</span>'); }
})();

// Characters placed between the title and the hero numbers (maps). Re-run after a size switch.
window.gbHeaderBots = function (specs) {
  const stage = document.getElementById('stage');
  let box = stage.querySelector('.gb-head');
  if (!box) {
    box = document.createElement('div'); box.className = 'gb-bots gb-head';
    box.innerHTML = specs.map((o) => `<div class="gb-bot" data-w="${o.w}">${bot({ ...o, size: 100 })}</div>`).join('');
    stage.appendChild(box);
  }
  const s1280 = document.body.classList.contains('s1280');
  const k = s1280 ? 0.6 : 1;
  box.querySelectorAll('.gb-bot').forEach((d) => { const w = d.dataset.w * k; d.style.width = w + 'px'; const s = d.querySelector('svg'); s.setAttribute('width', w); s.setAttribute('height', w * 1.2); });
  const st = stage.getBoundingClientRect();
  const h1 = stage.querySelector('h1').getBoundingClientRect();
  const hn = stage.querySelector('.hero-nums').getBoundingClientRect();
  const bw = box.getBoundingClientRect().width;
  const left = Math.max(h1.right + 30 * k, hn.left - bw - 60 * k) - st.left;
  box.style.left = left + 'px';
  box.style.top = (h1.bottom - st.top - box.getBoundingClientRect().height - 4 * k) + 'px';
};
