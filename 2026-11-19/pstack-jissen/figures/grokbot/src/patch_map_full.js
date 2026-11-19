(function () {
  document.head.insertAdjacentHTML('beforeend', '<style>body:not(.s1280) .hero-nums { top: 60px !important; }</style>');
  const specs = [{ kind: 'box', color: '#FF6801', w: 54, look: [0.7, 0.2] }, { kind: 'round', color: '#1386FF', w: 64, look: [0.6, -0.3] }, { kind: 'mochi', color: '#000000', w: 78, look: [0.8, 0] }];
  window.gbLayout = () => gbHeaderBots(specs);
  gbLayout();
})();
