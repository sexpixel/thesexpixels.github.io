// Shared behaviour for thesexpixels.com.
(function(){
  // 1. Nav hides when scrolling down, comes back when scrolling up (Framestore-style).
  var nav = document.getElementById('nav');
  if (nav) {
    var last = window.scrollY, ticking = false;
    // On player pages the page name sits just under the menu, so the menu never turns solid there
    // (it would cover the name); it simply slides away as soon as you scroll.
    var overTitle = !!document.querySelector('.herotop'), HIDE_AT = overTitle ? 8 : 140;
    var update = function(){
      var y = window.scrollY;
      nav.classList.toggle('solid', y > 40 && !(overTitle && y < window.innerHeight * 0.9));
      if (nav.classList.contains('open')) { last = y; ticking = false; return; }
      if (y > last && y > HIDE_AT) nav.classList.add('hide');
      else if (y < last - 4 || y <= HIDE_AT) nav.classList.remove('hide');
      last = y; ticking = false;
    };
    window.addEventListener('scroll', function(){ if (!ticking) { requestAnimationFrame(update); ticking = true; } }, {passive:true});
    nav.addEventListener('focusin', function(){ nav.classList.remove('hide'); });
  }


  // 1a. Phase row: tap a phase to open its panel (touch screens and the phone menu); the page's
  // current ?phase= is underlined.
  document.querySelectorAll('.phrow .p > button').forEach(function(b){
    b.addEventListener('click', function(){
      var li = b.parentNode, on = !li.classList.contains('open');
      document.querySelectorAll('.phrow .p.open').forEach(function(x){ x.classList.remove('open'); x.firstChild.setAttribute('aria-expanded','false'); });
      li.classList.toggle('open', on); b.setAttribute('aria-expanded', on ? 'true' : 'false');
    });
  });
  document.addEventListener('click', function(e){
    if (!e.target.closest('.phrow') && window.matchMedia('(min-width:1280px)').matches)
      document.querySelectorAll('.phrow .p.open').forEach(function(x){ x.classList.remove('open'); });
  });
  try { var cph = new URL(location.href).searchParams.get('phase'); if (cph) { var h = document.querySelector('.phrow .p[data-ph="' + cph + '"]'); if (h) h.classList.add('here'); } } catch (e) {}

  // 1b. Menu button for narrower screens: opens the menu full screen.
  var btn = document.querySelector('.menu-btn');
  if (btn && nav) {
    var setOpen = function(on){
      nav.classList.toggle('open', on); btn.setAttribute('aria-expanded', on ? 'true' : 'false');
      btn.textContent = on ? 'Close' : 'Menu'; document.body.style.overflow = on ? 'hidden' : '';
    };
    btn.addEventListener('click', function(){ setOpen(!nav.classList.contains('open')); });
    nav.querySelectorAll('nav a').forEach(function(a){ a.addEventListener('click', function(){ setOpen(false); }); });
    document.addEventListener('keydown', function(e){ if (e.key === 'Escape' && nav.classList.contains('open')) { setOpen(false); btn.focus(); } });
  }


  // 1c. TV mode on the homepage reel: after a few seconds with no mouse movement, the menu,
  // captions and cursor fade away and the reel fills the screen like a TV. Any movement,
  // touch, key press or scroll brings them back.
  var hero = document.querySelector('.hero');
  // On touch screens the faded controls stay tappable (see .tv rules in site.css), so one tap both
  // wakes the screen and presses the button under the finger.
  if (hero && !document.body.classList.contains('tuner')) {
    var idle, IDLE_MS = 2500;
    var onHero = function(){ return window.scrollY < hero.offsetHeight * 0.6; };
    var wake = function(){
      document.body.classList.remove('tv');
      clearTimeout(idle);
      idle = setTimeout(function(){
        if (onHero() && !(nav && nav.classList.contains('open')) && !document.querySelector('.lightbox:not([hidden])')) document.body.classList.add('tv');
      }, IDLE_MS);
    };
    ['mousemove', 'touchstart', 'keydown', 'scroll', 'focusin'].forEach(function(ev){ window.addEventListener(ev, wake, {passive:true}); });
    wake();
  }

  // 1c2. Crop, Resolve-style. data-crop="top,bottom,left,right,fill" (percent of the frame).
  // fill=1 scales the cropped picture up to cover the screen; fill=0 leaves the cropped edges black.
  window.TSPcrop = function(stage, frame){
    if (!stage || !frame) return;
    var c = (stage.getAttribute('data-crop') || '').split(',').map(Number);
    var props = ['width', 'height', 'left', 'top', 'transform', 'clip-path'];
    if (window.TSPplaceTitle) window.TSPplaceTitle();
    if (c.length < 4 || !(c[0] || c[1] || c[2] || c[3])) { props.forEach(function(k){ frame.style.removeProperty(k); }); return; }
    var t = c[0] / 100, b = c[1] / 100, l = c[2] / 100, r = c[3] / 100, fill = c[4] === 1;
    var ar = parseFloat(getComputedStyle(stage).getPropertyValue('--ar')) || 16 / 9;
    var box = frame.closest('.fp-slot') || stage;   // on an upright phone the video sits in its own box under the page name
    if (window.matchMedia('(orientation:portrait)').matches && box === stage) box = frame;
    var vw = box.clientWidth, vh = box.clientHeight, fw = Math.max(0.05, 1 - l - r), fh = Math.max(0.05, 1 - t - b), W;
    if (vw < vh) W = fill ? vw / fw : vw;   // phone held upright: fit the width, never crop the sides
    else if (fill) W = Math.max(vw / fw, vh * ar / fh); else W = Math.max(vw, vh * ar);
    var H = W / ar, cx = fill ? W * (l + fw / 2) : W / 2, cy = fill ? H * (t + fh / 2) : H / 2;
    var set = function(k, v){ frame.style.setProperty(k, v, 'important'); };
    set('width', W + 'px'); set('height', H + 'px'); set('left', (vw / 2 - cx) + 'px'); set('top', (vh / 2 - cy) + 'px');
    set('transform', 'none'); set('clip-path', 'inset(' + c[0] + '% ' + c[3] + '% ' + c[1] + '% ' + c[2] + '%)');
    // With a top crop, sit the page name in the black strip: its bottom on the crop line,
    // but never up under the menu.
  };
  // The page name sits directly under Mark's name in the menu bar.
  window.TSPplaceTitle = function(){
    var t = document.querySelector('.herotop'), n = document.getElementById('nav'), mk = n && n.querySelector('.mark');
    if (!t || !mk) return;
    var pr = n.querySelector('.phrow'), low = (pr && pr.offsetParent) ? pr : mk;   // under the phase row when it shows
    var y = (low.getBoundingClientRect().bottom - n.getBoundingClientRect().top + 4) + 'px', hero = t.closest('.hero');
    t.style.top = y;
    // Upright phone: the page is stacked, so the name sits in the flow just under the menu bar.
    if (hero) hero.style.paddingTop = window.matchMedia('(orientation:portrait)').matches ? y : '';
  };
  window.TSPplaceTitle();
  window.addEventListener('resize', function(){
    window.TSPplaceTitle();
    document.querySelectorAll('[data-crop]').forEach(function(st){
      if (st.classList.contains('hero')) window.TSPcrop(st, st.querySelector('.fp-slot iframe, :scope > iframe'));
    });
  });

  // Keep Vimeo subtitles off. Vimeo can switch a caption track on after the video starts (when the
  // video has one set as default), so they're switched off again whenever a track turns on.
  window.TSPnoSubs = function(pl){
    if (!pl || !pl.disableTextTrack) return;
    var off = function(){ pl.disableTextTrack().catch(function(){}); };
    off();
    ['loaded', 'play', 'playing'].forEach(function(ev){ try { pl.on(ev, off); } catch (e) {} });
    try { pl.on('texttrackchange', function(d){ if (d && (d.language || d.kind)) off(); }); } catch (e) {}
  };

  // 1d. Homepage background reel: read the video's real shape so it covers the screen edge to edge.
  var bg = document.querySelector('.hero > iframe[src*="player.vimeo.com"]');
  if (bg) window.TSPcrop(bg.parentNode, bg);
  if (bg) {
    var s = document.createElement('script'); s.src = 'https://player.vimeo.com/api/player.js';
    s.onload = function(){
      try {
        var pl = new window.Vimeo.Player(bg);
        window.TSPnoSubs(pl);
        Promise.all([pl.getVideoWidth(), pl.getVideoHeight()]).then(function(d){
          if (d[0] && d[1]) bg.parentNode.style.setProperty('--ar', d[0] / d[1]);
          window.TSPcrop(bg.parentNode, bg);
        }).catch(function(){});
      } catch (e) {}
    };
    document.head.appendChild(s);
  }

  // 2. Full-screen player. Any element with data-video="vimeo:ID:HASH" or "youtube:ID" opens it.
  var box, frame, closeBtn, lastFocus;
  function build(){
    box = document.createElement('div');
    box.className = 'lightbox'; box.hidden = true;
    box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true'); box.setAttribute('aria-label', 'Video player');
    box.innerHTML = '<button class="x" type="button" aria-label="Close video">&times;</button>' +
      '<iframe allow="autoplay; fullscreen; picture-in-picture; encrypted-media" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen title="Video"></iframe>';
    document.body.appendChild(box);
    closeBtn = box.querySelector('.x'); frame = box.querySelector('iframe');
    closeBtn.addEventListener('click', close);
    box.addEventListener('keydown', function(e){ if (e.key === 'Escape') close(); if (e.key === 'Tab') { e.preventDefault(); closeBtn.focus(); } });
    document.addEventListener('fullscreenchange', function(){ if (!document.fullscreenElement && !box.hidden) close(); });
  }
  function srcFor(spec){
    var p = spec.split(':');
    if (p[0] === 'vimeo') return 'https://player.vimeo.com/video/' + p[1] + '?' + (p[2] ? 'h=' + p[2] + '&' : '') + 'autoplay=1&transparent=0&texttrack=false&title=0&byline=0&portrait=0&dnt=1';
    if (p[0] === 'youtube') return 'https://www.youtube-nocookie.com/embed/' + p[1] + '?autoplay=1&rel=0&modestbranding=1&playsinline=1&cc_load_policy=0&iv_load_policy=3';
    if (p[0] === 'instagram') return 'https://www.instagram.com/reel/' + p[1] + '/embed';
    return null;
  }
  function open(spec){
    var src = srcFor(spec); if (!src) return false;
    if (!box) build();
    lastFocus = document.activeElement;
    box.classList.toggle('vertical', spec.indexOf('instagram:') === 0);
    frame.src = src; box.hidden = false; document.body.style.overflow = 'hidden'; closeBtn.focus();
    if (box.requestFullscreen) box.requestFullscreen().catch(function(){});
    return true;
  }
  function close(){
    if (!box || box.hidden) return;
    box.hidden = true; frame.src = 'about:blank'; document.body.style.overflow = '';
    if (document.fullscreenElement) document.exitFullscreen().catch(function(){});
    if (lastFocus) lastFocus.focus();
  }
  document.addEventListener('click', function(e){
    var el = e.target.closest('[data-video]');
    if (el && open(el.getAttribute('data-video'))) e.preventDefault();
  });

  // 2b. A thumbnail that fails to load is hidden (some browsers draw a white frame round a broken image).
  document.addEventListener('error', function(e){
    var t = e.target; if (t && t.tagName === 'IMG') t.hidden = true;
  }, true);

  // 3. Vimeo stills for unlisted videos (they have no fixed image address, so ask Vimeo).
  document.querySelectorAll('img[data-vimeo]').forEach(function(img){
    fetch('https://vimeo.com/api/oembed.json?width=1280&url=' + encodeURIComponent(img.getAttribute('data-vimeo')))
      .then(function(r){ return r.ok ? r.json() : null; })
      .then(function(d){ if (d && d.thumbnail_url) { img.src = d.thumbnail_url; img.hidden = false; } })
      .catch(function(){});
  });
})();

/* The Fleapit, phones held upright: share any spare screen height between the gaps, so Follow on Instagram sits
   clear of the browser bar and the tiles start just below the screen. Where there is no spare height (Chrome),
   nothing changes. */
(function(){
  var main = document.querySelector('main.pg-fleapit'); if (!main) return;
  // Room kept under the button: Safari's address bar floats over the bottom of the page, so keep the button above it;
  // other browsers (Chrome) keep their bars outside the page, so the button sits at the bottom with a small margin.
  var ua = navigator.userAgent, floatingBar = /Safari/.test(ua) && /iP(hone|od)/.test(ua) && !/CriOS|FxiOS|EdgiOS|OPiOS/.test(ua);
  var BAR = floatingBar ? 100 : 20;
  if (floatingBar) main.classList.add('fp-float');   // Safari: a little more room between the controls and Reels
  function fit(){
    main.style.removeProperty('--fx'); main.style.removeProperty('--ft');
    if (!matchMedia('(orientation:portrait) and (max-width:760px)').matches) return;
    var pill = document.querySelector('.pagelinks .pill'), grid = document.querySelector('.fp-grid');
    if (!pill || !grid) return;
    var y = window.scrollY, h = window.innerHeight;
    var spare = h - BAR - (pill.getBoundingClientRect().bottom + y);
    if (spare > 0) main.style.setProperty('--fx', spare + 'px');
    var tail = h + (floatingBar ? 80 : 0) - (grid.getBoundingClientRect().top + y);   // Safari: also clear the strip behind its see-through bar
    if (tail > 0) main.style.setProperty('--ft', tail + 'px');
  }
  var t; function soon(){ clearTimeout(t); t = setTimeout(fit, 150); }
  window.addEventListener('orientationchange', soon);
  var lastW = window.innerWidth;
  window.addEventListener('resize', function(){ if (window.innerWidth !== lastW || !main.style.getPropertyValue('--fx')) { lastW = window.innerWidth; soon(); } });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit); else window.addEventListener('load', fit);
  fit();
})();

/* Other player pages (Nuke Compositor, VFX Supervisor, the Work formats), phones held upright: the first screen ends
   with the "Reels · All" line sitting at the bottom, so people know the reels are below, and the reels themselves
   start just off the screen. Safari's see-through address bar floats over the page, so there the line sits above it. */
(function(){
  var main = document.querySelector('main[class^="pg-"]:not(.pg-fleapit)'); if (!main) return;
  var rail = main.querySelector('.fp-reels .rail'); if (!rail) return;
  var ua = navigator.userAgent, floatingBar = /Safari/.test(ua) && /iP(hone|od)/.test(ua) && !/CriOS|FxiOS|EdgiOS|OPiOS/.test(ua);
  var BAR = floatingBar ? 96 : 14, BEHIND = floatingBar ? 80 : 0;
  function fit(){
    main.classList.remove('pg-fit'); main.style.removeProperty('--rp'); main.style.removeProperty('--rm');
    if (!matchMedia('(orientation:portrait) and (max-width:760px)').matches) return;
    main.classList.add('pg-fit');   // Reels padding and rail gap start from their smallest
    var y = window.scrollY, h = window.innerHeight, r = rail.getBoundingClientRect();
    var lift = h - BAR - (r.bottom + y);                       // room left under the Reels line
    if (lift > 0) main.style.setProperty('--rp', lift + 'px');
    var next = rail.nextElementSibling; if (!next) return;
    var gap = h + BEHIND - (next.getBoundingClientRect().top + y);   // push what follows off the screen
    if (gap > 0) main.style.setProperty('--rm', gap + 'px');
  }
  var t; function soon(){ clearTimeout(t); t = setTimeout(fit, 150); }
  window.addEventListener('orientationchange', soon);
  var lastW = window.innerWidth, lastH = window.innerHeight;
  window.addEventListener('resize', function(){
    // refit when the phone turns, or when the browser bar settles while the page is still at the top
    if (window.innerWidth !== lastW || (window.scrollY < 8 && Math.abs(window.innerHeight - lastH) > 40)) { lastW = window.innerWidth; lastH = window.innerHeight; soon(); }
  });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit); else window.addEventListener('load', fit);
  fit();
})();
