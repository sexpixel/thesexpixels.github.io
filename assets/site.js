// Shared behaviour for thesexpixels.com.
(function(){
  // 1. Nav hides when scrolling down, comes back when scrolling up (Framestore-style).
  var nav = document.getElementById('nav');
  if (nav) {
    var last = window.scrollY, ticking = false;
    var update = function(){
      var y = window.scrollY;
      nav.classList.toggle('solid', y > 40);
      if (nav.classList.contains('open')) { last = y; ticking = false; return; }
      if (y > last && y > 140) nav.classList.add('hide');
      else if (y < last - 4 || y <= 140) nav.classList.remove('hide');
      last = y; ticking = false;
    };
    window.addEventListener('scroll', function(){ if (!ticking) { requestAnimationFrame(update); ticking = true; } }, {passive:true});
    nav.addEventListener('focusin', function(){ nav.classList.remove('hide'); });
  }


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

  // 2. Full-screen player. Any element with data-video="vimeo:ID:HASH" or "youtube:ID" opens it.
  var box, frame, closeBtn, lastFocus;
  function build(){
    box = document.createElement('div');
    box.className = 'lightbox'; box.hidden = true;
    box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true'); box.setAttribute('aria-label', 'Video player');
    box.innerHTML = '<button class="x" type="button" aria-label="Close video">&times;</button>' +
      '<iframe allow="autoplay; fullscreen; picture-in-picture" allowfullscreen title="Video"></iframe>';
    document.body.appendChild(box);
    closeBtn = box.querySelector('.x'); frame = box.querySelector('iframe');
    closeBtn.addEventListener('click', close);
    box.addEventListener('keydown', function(e){ if (e.key === 'Escape') close(); if (e.key === 'Tab') { e.preventDefault(); closeBtn.focus(); } });
    document.addEventListener('fullscreenchange', function(){ if (!document.fullscreenElement && !box.hidden) close(); });
  }
  function srcFor(spec){
    var p = spec.split(':');
    if (p[0] === 'vimeo') return 'https://player.vimeo.com/video/' + p[1] + '?' + (p[2] ? 'h=' + p[2] + '&' : '') + 'autoplay=1&title=0&byline=0&portrait=0&dnt=1';
    if (p[0] === 'youtube') return 'https://www.youtube-nocookie.com/embed/' + p[1] + '?autoplay=1&rel=0&modestbranding=1&playsinline=1';
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

  // 3. Vimeo stills for unlisted videos (they have no fixed image address, so ask Vimeo).
  document.querySelectorAll('img[data-vimeo]').forEach(function(img){
    fetch('https://vimeo.com/api/oembed.json?width=1280&url=' + encodeURIComponent(img.getAttribute('data-vimeo')))
      .then(function(r){ return r.ok ? r.json() : null; })
      .then(function(d){ if (d && d.thumbnail_url) { img.src = d.thumbnail_url; img.hidden = false; } })
      .catch(function(){});
  });
})();
