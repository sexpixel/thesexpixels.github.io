// Reel crop tuner (private page at /tuner/). Plays each reel full screen behind a sample
// page heading; Crop top/bottom/left/right work like Resolve's crop, with an option to fill the screen.
// "Copy settings" gives the lines to paste back to Claude, who puts them in _build/crops.py.
(function(){
  var stage = document.getElementById('fp-player'), slot = document.getElementById('fp-slot');
  var pick = document.getElementById('t-pick'), out = document.getElementById('t-out');
  var SIDES = ['top', 'bottom', 'left', 'right'], slider = {}, readout = {};
  SIDES.forEach(function(k){ slider[k] = document.getElementById('c-' + k); readout[k] = document.getElementById('v-' + k); });
  var link = document.getElementById('c-link'), fill = document.getElementById('c-fill');
  var head = document.getElementById('t-head'), now = document.getElementById('t-now');
  var panel = document.getElementById('t-panel'), show = document.getElementById('t-show');
  // v3: crop only by default (fill off). Crops made in v2 are kept, with fill switched off.
  var KEY = 'tsp-crops-v3', saved = {};
  try {
    saved = JSON.parse(localStorage.getItem(KEY) || 'null');
    if (!saved) { saved = JSON.parse(localStorage.getItem('tsp-crops-v2') || '{}') || {}; Object.keys(saved).forEach(function(k){ saved[k].fill = false; }); }
  } catch (e) { saved = {}; }
  TUNE.forEach(function(r){ var v = saved[r.spec]; if (v) { SIDES.forEach(function(k){ r[k] = v[k] || 0; }); r.fill = v.fill === true; } });
  function save(){
    var o = {}; TUNE.forEach(function(r){ o[r.spec] = { top: r.top, bottom: r.bottom, left: r.left, right: r.right, fill: r.fill }; });
    try { localStorage.setItem(KEY, JSON.stringify(o)); } catch (e) {}
  }

  TUNE.forEach(function(r, i){
    var o = document.createElement('option'); o.value = i; o.textContent = (i + 1) + '. ' + r.title + ' (' + r.page + ')'; pick.appendChild(o);
  });

  var cur = 0, vimeoReady;
  function vimeo(){
    return vimeoReady || (vimeoReady = new Promise(function(res, rej){
      if (window.Vimeo) return res();
      var s = document.createElement('script'); s.src = 'https://player.vimeo.com/api/player.js'; s.onload = res; s.onerror = rej; document.head.appendChild(s);
    }));
  }
  function cropped(x){ return x.top || x.bottom || x.left || x.right; }
  function apply(){
    var r = TUNE[cur];
    SIDES.forEach(function(k){ slider[k].value = r[k]; readout[k].textContent = Number(r[k]).toFixed(1) + '%'; });
    fill.checked = r.fill;
    stage.setAttribute('data-crop', [r.top, r.bottom, r.left, r.right, r.fill ? 1 : 0].join(','));
    window.TSPcrop(stage, slot.querySelector('iframe'));
    out.value = TUNE.filter(cropped).map(function(x){
      return x.spec + ' = top ' + x.top + ', bottom ' + x.bottom + ', left ' + x.left + ', right ' + x.right + ', ' + (x.fill ? 'fill screen' : 'crop only') + '   # ' + x.title;
    }).join('\n') || '(no reels cropped yet)';
  }
  function load(i){
    cur = (i + TUNE.length) % TUNE.length; pick.value = cur;
    var r = TUNE[cur], p = r.spec.split(':');
    head.textContent = r.page; now.textContent = (cur + 1) + ' / ' + TUNE.length + ' · ' + r.title;
    stage.style.removeProperty('--ar');
    slot.innerHTML = '';
    var f = document.createElement('iframe');
    f.setAttribute('allow', 'autoplay; fullscreen; picture-in-picture; encrypted-media'); f.title = r.title;
    f.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');
    if (p[0] === 'vimeo') {
      f.src = 'https://player.vimeo.com/video/' + p[1] + '?' + (p[2] ? 'h=' + p[2] + '&' : '') + 'autoplay=1&transparent=0&texttrack=false&muted=1&loop=1&controls=0&title=0&byline=0&portrait=0&dnt=1';
      slot.appendChild(f); apply();
      vimeo().then(function(){
        var pl = new window.Vimeo.Player(f), mine = cur;
        Promise.all([pl.getVideoWidth(), pl.getVideoHeight()]).then(function(d){
          if (mine === cur && d[0] && d[1]) { stage.style.setProperty('--ar', d[0] / d[1]); apply(); }
        }).catch(function(){});
      }).catch(function(){});
    } else if (p[0] === 'youtube') {
      f.src = 'https://www.youtube-nocookie.com/embed/' + p[1] + '?autoplay=1&mute=1&loop=1&playlist=' + p[1] + '&controls=0&rel=0&playsinline=1&cc_load_policy=0&iv_load_policy=3' + (p[2] ? '&start=' + p[2] : '');
      slot.appendChild(f); apply();
    }
  }

  pick.addEventListener('change', function(){ load(+pick.value); });
  document.getElementById('t-prev').addEventListener('click', function(){ load(cur - 1); });
  document.getElementById('t-next').addEventListener('click', function(){ load(cur + 1); });
  SIDES.forEach(function(k){
    slider[k].addEventListener('input', function(){
      var r = TUNE[cur]; r[k] = +slider[k].value;
      if (link.checked && (k === 'top' || k === 'bottom')) r[k === 'top' ? 'bottom' : 'top'] = r[k];
      apply(); save();
    });
  });
  fill.addEventListener('change', function(){ TUNE[cur].fill = fill.checked; apply(); save(); });
  document.getElementById('t-reset').addEventListener('click', function(){
    var r = TUNE[cur]; SIDES.forEach(function(k){ r[k] = 0; }); r.fill = false; apply(); save();
  });
  var guides = document.getElementById('t-guides');
  guides.addEventListener('click', function(){
    var on = document.body.classList.toggle('noguides') === false;
    guides.textContent = on ? 'Headings on' : 'Headings off'; guides.setAttribute('aria-pressed', on ? 'true' : 'false');
  });
  function togglePanel(){ var hide = !panel.hidden; panel.hidden = hide; show.hidden = !hide; }
  document.getElementById('t-hide').addEventListener('click', togglePanel);
  show.addEventListener('click', togglePanel);
  document.addEventListener('keydown', function(e){
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT' || e.target.tagName === 'TEXTAREA') return;
    if (e.key === 'h' || e.key === 'H') togglePanel();
  });
  document.getElementById('t-copy').addEventListener('click', function(){
    var btn = this;
    (navigator.clipboard ? navigator.clipboard.writeText(out.value) : Promise.reject()).then(function(){
      btn.textContent = 'Copied'; setTimeout(function(){ btn.textContent = 'Copy settings'; }, 1500);
    }).catch(function(){ out.select(); });
  });

  load(0);
})();
