// Reel crop tuner (private page at /tuner/). Plays each reel full screen behind a sample
// page heading; Zoom and Move set how much of the black bars is pushed off screen.
// "Copy settings" gives the lines to paste back to Claude, who puts them in _build/crops.py.
(function(){
  var stage = document.getElementById('fp-player'), slot = document.getElementById('fp-slot');
  var pick = document.getElementById('t-pick'), zoom = document.getElementById('t-zoom'), shift = document.getElementById('t-shift');
  var zv = document.getElementById('t-zv'), sv = document.getElementById('t-sv'), out = document.getElementById('t-out');
  var head = document.getElementById('t-head'), now = document.getElementById('t-now');
  var panel = document.getElementById('t-panel'), show = document.getElementById('t-show');
  var KEY = 'tsp-crops-v1', saved = {};
  try { saved = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) {}
  TUNE.forEach(function(r){ if (saved[r.spec]) { r.zoom = saved[r.spec][0]; r.shift = saved[r.spec][1]; } });
  function save(){
    var o = {}; TUNE.forEach(function(r){ o[r.spec] = [r.zoom, r.shift]; });
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
  function apply(){
    var r = TUNE[cur];
    stage.style.setProperty('--zoom', r.zoom); stage.style.setProperty('--shift', r.shift);
    zoom.value = r.zoom; shift.value = r.shift;
    zv.textContent = Number(r.zoom).toFixed(2) + '×'; sv.textContent = (r.shift > 0 ? '+' : '') + r.shift + '%';
    out.value = TUNE.filter(function(x){ return x.zoom != 1 || x.shift != 0; })
      .map(function(x){ return x.spec + ' = ' + Number(x.zoom).toFixed(2) + ', ' + x.shift + '   # ' + x.title; }).join('\n') || '(no reels cropped yet)';
  }
  function load(i){
    cur = (i + TUNE.length) % TUNE.length; pick.value = cur;
    var r = TUNE[cur], p = r.spec.split(':');
    head.textContent = r.page; now.textContent = (cur + 1) + ' / ' + TUNE.length + ' · ' + r.title;
    stage.style.removeProperty('--ar'); apply();
    slot.innerHTML = '';
    var f = document.createElement('iframe');
    f.setAttribute('allow', 'autoplay; fullscreen; picture-in-picture'); f.title = r.title;
    if (p[0] === 'vimeo') {
      f.src = 'https://player.vimeo.com/video/' + p[1] + '?' + (p[2] ? 'h=' + p[2] + '&' : '') + 'autoplay=1&muted=1&loop=1&controls=0&title=0&byline=0&portrait=0&dnt=1';
      slot.appendChild(f);
      vimeo().then(function(){
        var pl = new window.Vimeo.Player(f), mine = cur;
        Promise.all([pl.getVideoWidth(), pl.getVideoHeight()]).then(function(d){
          if (mine === cur && d[0] && d[1]) stage.style.setProperty('--ar', d[0] / d[1]);
        }).catch(function(){});
      }).catch(function(){});
    } else if (p[0] === 'youtube') {
      f.src = 'https://www.youtube-nocookie.com/embed/' + p[1] + '?autoplay=1&mute=1&loop=1&playlist=' + p[1] + '&controls=0&rel=0&playsinline=1';
      slot.appendChild(f);
    }
  }

  pick.addEventListener('change', function(){ load(+pick.value); });
  document.getElementById('t-prev').addEventListener('click', function(){ load(cur - 1); });
  document.getElementById('t-next').addEventListener('click', function(){ load(cur + 1); });
  zoom.addEventListener('input', function(){ TUNE[cur].zoom = +zoom.value; apply(); save(); });
  shift.addEventListener('input', function(){ TUNE[cur].shift = +shift.value; apply(); save(); });
  document.getElementById('t-reset').addEventListener('click', function(){ TUNE[cur].zoom = 1; TUNE[cur].shift = 0; apply(); save(); });
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
