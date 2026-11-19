(function () {
  document.head.insertAdjacentHTML('beforeend', '<style>body:not(.s1280) .hero-nums { top: 60px !important; }</style>');
  const specs = [{ kind: 'box', color: '#FF6801', w: 54, look: [0.7, 0.2] }, { kind: 'round', color: '#1386FF', w: 64, look: [0.6, -0.3] }, { kind: 'mochi', color: '#000000', w: 78, look: [0.8, 0] }];
  window.gbLayout = () => gbHeaderBots(specs);
  gbLayout();
})();
// Keep each stamp glued to its item name: move .marks into .nm and bind it to the name's last segment
// with nowrap, so a stamp can never fall onto its own line between two rows.
(function () {
  document.head.insertAdjacentHTML('beforeend', '<style>.item .nm { overflow-wrap: normal !important; word-break: normal !important; } .item .nm .glue { white-space: nowrap; } .item .nm .marks { margin-left: 5px; }</style>');
  document.querySelectorAll('.item .marks').forEach((mk) => {
    const nm = mk.parentElement.querySelector('.nm');
    if (!nm) return;
    const txt = nm.textContent;
    const cut = Math.max(txt.lastIndexOf('-'), txt.lastIndexOf(' ')) + 1;
    nm.textContent = txt.slice(0, cut);
    const glue = document.createElement('span'); glue.className = 'glue';
    glue.textContent = txt.slice(cut);
    glue.appendChild(mk);
    nm.appendChild(glue);
  });
})();
// 1280: the playbook rows ran past the ⑧ box into the footer. Tighten the rows and nudge the footer.
document.head.insertAdjacentHTML('beforeend', `<style>
body.s1280 .item.pb, body.s1280 .item.pb .nm, body.s1280 .item.pb .id { line-height: 1.18 !important; }
body.s1280 .plays { padding-top: 3px !important; padding-bottom: 2px !important; }
body.s1280 .plays .phd { margin-bottom: 2px !important; }
body.s1280 .footer { top: 600px !important; }
</style>`);
window.gbCheckPlays = () => { const f = document.querySelector('.footer p').getBoundingClientRect().top; const box = document.querySelector('.plays').getBoundingClientRect(); const last = Math.max(...[...document.querySelectorAll('.plays .item')].map((e) => e.getBoundingClientRect().bottom)); return { lastItem: last, boxBottom: box.bottom, footerText: f }; };
