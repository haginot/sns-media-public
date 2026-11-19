// shared header/footer/helpers for the English Tech Blog banner
// No thumbnail, no logos, no PIVOT name (HAGINO: English readers don't know the show).
function header(_opts = {}){
  Z.div('kick', 'I talked about ontology on a Japanese business TV show');
}
function footer(h){
  const d = Z.div('foot', h || '<b>Canly Tech Blog</b>');
  d.style.left = 'auto';
  d.style.right = '56px';
  d.style.bottom = '40px';
}
function card(x, y, ty, jp, {a='c', tyc='g'} = {}){
  const d = Z.div('card', `<div class="ty ${tyc}">${ty}</div><div class="jp">${jp}</div>`);
  const r = d.getBoundingClientRect();
  d.style.textAlign = a === 'c' ? 'center' : a === 'r' ? 'right' : 'left';
  d.style.left = (a === 'c' ? x - r.width / 2 : a === 'r' ? x - r.width : x) + 'px';
  d.style.top = (y - r.height / 2) + 'px';
  return d;
}
function chip(x, y, t){
  const d = Z.div('codechip', t);
  const r = d.getBoundingClientRect();
  d.style.left = (x - r.width / 2) + 'px';
  d.style.top = (y - r.height / 2) + 'px';
  return d;
}
