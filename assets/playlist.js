// Playlist player (The Fleapit, Nuke Compositor, VFX Supervisor): plays every reel in the grid, one after another.
// Vimeo and YouTube reels advance by themselves when they end. Instagram allows no
// "ended" signal, so on an Instagram reel the player waits for the Next button.
(function(){
  var allCells = [].slice.call(document.querySelectorAll('.fp-cell[data-src]'));
  if (!allCells.length) return;
  var noneHere = false;
  var cells = allCells;   // the reels that play: all of them, or just those in the chosen production phase
  var stage = document.getElementById('fp-player'), slot = document.getElementById('fp-slot'), titleEl = document.getElementById('fp-title');
  var cur = -1, player = null, kind = null, seq = 0, vimeoReady, ytReady;
  // Sound is the visitor's setting and only the Sound button changes it: swiping, Next, Back and the tiles
  // leave it alone. Phones only let a fresh player start by itself muted, so the site keeps one player and
  // loads each following reel into it (YouTube to YouTube, Vimeo to Vimeo): once sound is on, it stays on.
  // When the browser still refuses sound (a fresh player, or the page just opened), the reel plays muted and
  // the button reads "Tap for sound"; one tap brings it back.
  var sound = false, blocked = false;
  var touch = !!(window.matchMedia && matchMedia('(hover:none) and (pointer:coarse)').matches);
  function mutePl(pl){ try { if (pl.unMute) pl.mute(); else { pl.setMuted(true); pl.setVolume(0); } } catch (x) {} }
  function unmutePl(pl){ try { if (pl.unMute) { pl.unMute(); pl.setVolume(100); } else { pl.setMuted(false); pl.setVolume(1); } } catch (x) {} }
  function playingNow(pl, cb){ try { if (pl.getPlayerState) { var st = pl.getPlayerState(); cb(st === 1 || st === 3); } else pl.getPaused().then(function(q){ cb(!q); }).catch(function(){}); } catch (x) {} }
  function resumePl(pl){ try { if (pl.playVideo) pl.playVideo(); else pl.play().catch(function(){}); } catch (x) {} }
  // Once a reel is playing: match the visitor's sound setting. If unmuting makes the browser pause it, carry on muted.
  function settleSound(pl){
    var tok = pl._tok;
    if (tok !== seq || pl !== player) return;
    if (!sound) { mutePl(pl); return; }
    // A fresh player on a phone has no permission for sound yet. Asking for it there makes iPhones pause the
    // reel, so it plays on muted and the button offers "Tap for sound" instead.
    if (touch && pl._firstTok === tok) { blocked = true; showSound(); return; }
    unmutePl(pl);
    setTimeout(function(){
      if (tok !== seq || pl !== player) return;
      playingNow(pl, function(on){ blocked = !on; showSound(); if (!on) { mutePl(pl); resumePl(pl); } });
    }, 700);
  }
  // Safety net: a reel that hasn't started after 2.5 s (the browser refused it with sound) starts muted.
  function rescue(pl){
    var tok = pl._tok;
    setTimeout(function(){
      if (tok !== seq || pl !== player) return;
      playingNow(pl, function(on){ if (!on) { if (sound) blocked = true; showSound(); mutePl(pl); resumePl(pl); } });
    }, 2500);
  }
  var soundBtn = document.getElementById('fp-sound');
  function showSound(){ if (soundBtn) { soundBtn.textContent = !sound ? 'Sound on' : blocked ? 'Tap for sound' : 'Sound off'; soundBtn.setAttribute('aria-pressed', sound && !blocked ? 'true' : 'false'); } }
  // Play / pause button shows the state; 'paused' class swaps the icon.
  var playBtn = document.getElementById('fp-play');
  function showPaused(p){ if (!playBtn) return; playBtn.classList.toggle('paused', p); playBtn.setAttribute('aria-label', p ? 'Play' : 'Pause'); }
  function isYT(){ return player && typeof player.getPlayerState === 'function'; }
  function togglePlay(){
    if (!player) return;
    try {
      if (isYT()) { if (player.getPlayerState() === 1) { player.pauseVideo(); showPaused(true); } else { player.playVideo(); showPaused(false); } }
      else player.getPaused().then(function(p){ if (p) { player.play(); showPaused(false); } else { player.pause(); showPaused(true); } }).catch(function(){});
    } catch (e) {}
  }
  function seekBy(sec){
    if (!player) return;
    try {
      if (isYT()) player.seekTo(Math.max(0, player.getCurrentTime() + sec), true);
      else player.getCurrentTime().then(function(t){ return player.setCurrentTime(Math.max(0, t + sec)); }).catch(function(){});
    } catch (e) {}
  }
  function applySound(){
    showSound();
    if (!player) return;
    if (sound) { unmutePl(player); resumePl(player); } else mutePl(player);
  }


  function loadScript(src){ return new Promise(function(res, rej){ var s = document.createElement('script'); s.src = src; s.onload = res; s.onerror = rej; document.head.appendChild(s); }); }
  function vimeo(){ return vimeoReady || (vimeoReady = window.Vimeo ? Promise.resolve() : loadScript('https://player.vimeo.com/api/player.js')); }
  function yt(){
    if (ytReady) return ytReady;
    ytReady = new Promise(function(res){
      if (window.YT && window.YT.Player) return res();
      var prev = window.onYouTubeIframeAPIReady;
      window.onYouTubeIframeAPIReady = function(){ if (prev) prev(); res(); };
      loadScript('https://www.youtube.com/iframe_api');
    });
    return ytReady;
  }
  // Keep YouTube's captions off, even for viewers whose YouTube settings switch them on.
  // YouTube can load captions after the video starts, so this runs on ready, on start and when the captions module loads.
  function noCaptions(yp){
    try { yp.setOption('captions', 'track', {}); } catch (x) {}
    try { yp.unloadModule('captions'); } catch (x) {}
    try { yp.unloadModule('cc'); } catch (x) {}
  }
  var swipe = null;   // touch layer over the video (phones), kept on top whenever the slot is refilled
  var fadeT = null;
  function stopExtras(){ clearInterval(fadeT); fadeT = null; [].slice.call(slot.querySelectorAll('.fp-veil')).forEach(function(v){ v.remove(); }); }
  function clear(){ stopExtras(); if (player && player.destroy) { try { player.destroy(); } catch (e) {} } player = null; kind = null; slot.innerHTML = ''; if (swipe) slot.appendChild(swipe); }

  // The banner under the player describes what's playing: project, clip, then Role / Format / Phase.
  var pb = document.querySelector('.pbanner.live'), pbText = pb && pb.querySelector('.anniv-t');
  var SHORT = { 'VFX Supervisor': 'Supervisor', 'Nuke Compositor': 'Compositor', 'Feature Film': 'Film', 'Visualisation': 'Vis',
    'Feature Animation': 'Anim', 'Development': 'Dev', 'Pre-production': 'Pre', 'Production': 'Prod', 'Post-production': 'Post', 'Distribution': 'Dist' };
  function fillBanner(c, i){
    if (!pb) return;
    var t = c.getAttribute('data-title') || '', k = t.indexOf(' · ');
    var set = function(id, v){ var e = document.getElementById(id); if (e) e.textContent = v; };
    set('pb-n', (i + 1 < 10 ? '0' : '') + (i + 1));
    set('pb-title', k > 0 ? t.slice(0, k) : t);
    set('pb-sub', (k > 0 ? t.slice(k + 3) + ' · ' : '') + (i + 1) + ' of ' + cells.length + (noneHere ? ' · no reels in this phase yet' : ''));
    ['role', 'format', 'phase'].forEach(function(f){
      var v = c.getAttribute('data-' + f) || '', dd = document.getElementById('pb-' + f);
      if (dd) {   // full words, plus a short form that phones show so all three lines stay complete
        var sh = v.split(' · ').map(function(x){ return SHORT[x] || x; }).join(' · ');
        dd.innerHTML = '<span class="lg"></span><span class="sm" aria-hidden="true"></span>';
        dd.firstChild.textContent = v; dd.lastChild.textContent = sh; dd.parentNode.hidden = !v;
      }
    });
  }
  // Keep the banner the height of the page's tallest reel, so moving between reels (buttons, swipes) never makes
  // the controls and everything under the banner jump.
  function steadyBanner(){
    if (!pbText || !cells.length) return;
    // Phones upright reserve the height on the whole banner, so the number can sit level with the last line (Phase);
    // elsewhere the text column keeps it, as before.
    var box = matchMedia('(orientation:portrait) and (max-width:760px)').matches ? pb : pbText;
    pbText.style.minHeight = ''; pb.style.minHeight = '';
    var tallest = 0;
    // Measured over every reel on the page, not just the current filter, so changing format or phase doesn't move the controls either.
    allCells.forEach(function(c, j){ fillBanner(c, j); tallest = Math.max(tallest, box.getBoundingClientRect().height); });
    box.style.minHeight = Math.ceil(tallest) + 'px';
    if (cur >= 0 && cells[cur]) fillBanner(cells[cur], cur);
  }

  function vimeoSrc(p){ return 'https://player.vimeo.com/video/' + p[1] + (p[2] ? '?h=' + p[2] : ''); }
  function sizeVimeo(pl, f){
    Promise.all([pl.getVideoWidth(), pl.getVideoHeight()]).then(function(d){
      if (pl === player && d[0] && d[1]) { stage.style.setProperty('--ar', d[0] / d[1]); if (window.TSPcrop) window.TSPcrop(stage, f); }
    }).catch(function(){});
  }
  function skip(pl){ kind = null; setTimeout(function(){ if (pl === player) play(cur + 1); }, 1500); }   // a reel that can't play is skipped (on a fresh player)

  function play(i){
    if (i < 0) i = cells.length - 1;
    if (i >= cells.length) i = 0;
    cur = i;
    var tok = ++seq;
    var c = cells[i], spec = c.getAttribute('data-src'), p = spec.split(':');
    cells.forEach(function(x, k){ x.classList.toggle('on', k === i); });
    titleEl.textContent = (noneHere ? 'No reels in this phase yet · ' : '') + 'Now playing · ' + (i + 1) + ' / ' + cells.length + ' · ' + c.getAttribute('data-title');
    // The banner under the player describes what's playing: project, clip, then Role / Format / Phase.
    fillBanner(c, i);
    showSound();
    // Per-reel crop (set on the tuning page) pushes text in the black bars off screen.
    if (c.getAttribute('data-crop')) stage.setAttribute('data-crop', c.getAttribute('data-crop')); else stage.removeAttribute('data-crop');
    stage.classList.add('playing'); stage.classList.toggle('tall', p[0] === 'instagram');
    showPaused(false);
    // Only YouTube players are reused: Vimeo checks a reel's domain lock against the page that built the player, and a
    // reel loaded into an existing player fails that check (and was skipped), so every Vimeo reel gets a fresh player.
    var reuse = !!player && p[0] === 'youtube' && kind === 'youtube';
    if (reuse) stopExtras(); else { stage.style.removeProperty('--ar'); clear(); }
    var box = document.createElement('div'); if (!reuse) slot.appendChild(box);
    // YouTube "youtube:ID:START:END" plays only that stretch. Fades (data-fade="IN,OUT" seconds, one number sets
    // both): a black veil over the video and the sound ramp. They sit outside the in and out points, so 0:30–1:14
    // with 5,2 plays 0:25–1:16.
    var fd = (c.getAttribute('data-fade') || '').split(','), fadeIn = +fd[0] || 0, fadeOut = fd.length > 1 ? +fd[1] || 0 : fadeIn, fade = fadeIn || fadeOut;
    var sIn = 0, sOut = 0;
    if (p[0] === 'youtube') {
      sIn = +p[2] || 0; sOut = +p[3] || 0;
      if (fade && sIn) sIn = Math.max(0, sIn - fadeIn);
      if (fade && sOut) sOut += fadeOut;
    }
    if (fade) {
      var veil = document.createElement('span'); veil.className = 'fp-veil';
      veil.style.cssText = 'position:absolute;inset:0;background:#000;opacity:1;pointer-events:none;z-index:2';
      slot.appendChild(veil);
      var shade = function(t, end){
        var o = Math.max(0, Math.min(1, fadeIn ? (t - sIn) / fadeIn : 1, end && fadeOut ? (end - t) / fadeOut : 1));
        veil.style.opacity = (1 - o).toFixed(3);
        try { if (sound && !blocked && player) { if (player.unMute) player.setVolume(Math.round(100 * o)); else player.setVolume(o); } } catch (x) {}
      };
      fadeT = setInterval(function(){
        if (tok !== seq || !player || player._tok !== tok) return;
        try {
          if (player.unMute) shade(player.getCurrentTime(), sOut || player.getDuration());   // YouTube
          else Promise.all([player.getCurrentTime(), player.getDuration()]).then(function(d){ shade(d[0], sOut || d[1]); }).catch(function(){});
        } catch (x) {}
      }, 50);
    }
    var startMuted = touch || !sound;
    if (p[0] === 'vimeo') {
      if (reuse) {
        var vp = player; vp._tok = tok;
        vp.loadVideo(vimeoSrc(p)).then(function(){
          if (vp !== player || tok !== seq) return;
          if (window.TSPnoSubs) window.TSPnoSubs(vp); else if (vp.disableTextTrack) vp.disableTextTrack().catch(function(){});
          sizeVimeo(vp, slot.querySelector('iframe'));
          if (!sound || blocked) mutePl(vp);
          resumePl(vp); rescue(vp);
        }).catch(function(){ if (vp === player && tok === seq) { kind = null; play(cur); } });   // couldn't load into it: start a fresh player
        return;
      }
      vimeo().then(function(){
        if (tok !== seq) return;
        // Build the iframe ourselves (no width/height from Vimeo), then size it to cover the screen
        // using the video's real shape, so 4:3, 16:9 and scope reels all fill edge to edge.
        var f = document.createElement('iframe');
        f.src = vimeoSrc(p) + (p[2] ? '&' : '?') +
          'autoplay=1&autopause=0&transparent=0&controls=0&texttrack=false&muted=' + (startMuted ? 1 : 0) + '&title=0&byline=0&portrait=0&dnt=1&playsinline=1';
        f.title = c.getAttribute('data-title');
        f.setAttribute('allow', 'autoplay; fullscreen; picture-in-picture; encrypted-media');
        f.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');   // lets Vimeo see the site, for domain-restricted videos
        slot.replaceChild(f, box);
        if (window.TSPcrop) window.TSPcrop(stage, f);
        var pl = player = new window.Vimeo.Player(f); kind = 'vimeo'; pl._tok = pl._firstTok = tok;
        pl.on('ended', function(){ if (pl === player) play(cur + 1); });
        pl.on('play', function(){ if (pl !== player) return; showPaused(false); if (pl._settled !== pl._tok) { pl._settled = pl._tok; settleSound(pl); } });
        pl.on('pause', function(){ if (pl === player) showPaused(true); });
        pl.on('error', function(e){
          if (pl !== player) return;
          // Only a reel that can't load (privacy, removed) is skipped. A refused play or sound request (iPhones
          // refuse sound without a tap) is not a dead reel: carry on muted instead.
          if (e && (e.name === 'NotAllowedError' || e.method)) { if (sound) blocked = true; showSound(); mutePl(pl); resumePl(pl); return; }
          skip(pl);
        });
        if (window.TSPnoSubs) window.TSPnoSubs(pl); else if (pl.disableTextTrack) pl.disableTextTrack().catch(function(){});   // no subtitles, even if Vimeo turns them on later
        sizeVimeo(pl, f);
        rescue(pl);
      }).catch(function(){});
    } else if (p[0] === 'youtube') {
      var load = { videoId: p[1] };
      if (sIn) load.startSeconds = sIn; if (sOut) load.endSeconds = sOut;
      if (reuse) {
        var yr = player; yr._tok = tok;
        try {
          if (!sound || blocked) yr.mute();
          yr.loadVideoById(load);
          if (window.TSPcrop) window.TSPcrop(stage, slot.querySelector('iframe'));
          rescue(yr);
        } catch (x) { kind = null; play(cur); }
        return;
      }
      yt().then(function(){
        if (tok !== seq) return;
        var pv = { autoplay: 1, controls: 0, mute: startMuted ? 1 : 0, rel: 0, modestbranding: 1, playsinline: 1, cc_load_policy: 0, iv_load_policy: 3 };
        if (sIn) pv.start = sIn; if (sOut) pv.end = sOut;
        var yp = player = new window.YT.Player(box, { videoId: p[1], playerVars: pv,
          events: { onReady: function(e){
                      noCaptions(e.target);
                      if (window.TSPcrop) window.TSPcrop(stage, slot.querySelector('iframe')); },
                    onApiChange: function(e){ noCaptions(e.target); },   // fires when YouTube loads its captions module
                    onError: function(){ if (yp === player) skip(yp); },   // unplayable YouTube video: skip it
                    onStateChange: function(e){
                      if (yp !== player) return;
                      if (e.data === 1 || e.data === 2) showPaused(e.data === 2);
                      if (e.data === 1 && yp._settled !== yp._tok) { yp._settled = yp._tok; settleSound(yp); }
                      if (e.data === 1) { noCaptions(yp); setTimeout(function(){ noCaptions(yp); }, 1500); }   // playing
                      if (e.data === 0) play(cur + 1); } } });
        kind = 'youtube'; yp._tok = yp._firstTok = tok;
        rescue(yp);
      }).catch(function(){});
    } else if (p[0] === 'instagram') {
      var g = document.createElement('iframe');
      g.src = 'https://www.instagram.com/reel/' + p[1] + '/embed'; g.title = c.getAttribute('data-title');
      g.setAttribute('allow', 'autoplay; fullscreen; picture-in-picture');
      slot.replaceChild(g, box);
    }
  }

  allCells.forEach(function(c){
    c.addEventListener('click', function(){ play(Math.max(0, cells.indexOf(c))); stage.scrollIntoView({ behavior: 'smooth', block: 'center' }); });
  });

  // Filters: production phase (data-ph), plus format (data-fm) on role pages or role (data-ro) on format pages.
  // They combine: e.g. VFX Supervisor + Episodic + Production. They filter the grid and the playlist.
  var tiles = [].slice.call(document.querySelectorAll('.fp-grid .fp-cell'));
  var FILTERS = [['ph', 'data-phases', 'phase'], ['fm', 'data-fms', 'format'], ['ro', 'data-ros', 'role']];
  var sel = { ph: 'all', fm: 'all', ro: 'all' };
  function btnsOf(k){ return [].slice.call(document.querySelectorAll('.phases button[data-' + k + ']')); }
  function has(el, attr, v){ return v === 'all' || (' ' + (el.getAttribute(attr) || '') + ' ').indexOf(' ' + v + ' ') >= 0; }
  function passes(el){ return FILTERS.every(function(f){ return has(el, f[1], sel[f[0]]); }); }
  function apply(restart){
    FILTERS.forEach(function(f){ btnsOf(f[0]).forEach(function(b){ b.setAttribute('aria-pressed', b.getAttribute('data-' + f[0]) === sel[f[0]] ? 'true' : 'false'); }); });
    tiles.forEach(function(t){ t.hidden = !passes(t); });
    cells = allCells.filter(passes);
    noneHere = !cells.length;   // nothing matches yet: keep playing everything
    if (noneHere) cells = allCells;
    // The Reels line under the player names the filters in use (e.g. "Film · Prod"), or "All".
    var rh = document.getElementById('reels-h');
    if (rh && FILTERS.some(function(f){ return btnsOf(f[0]).length; })) {
      var on = [];
      FILTERS.slice().reverse().forEach(function(f){   // format or role first, then phase, as on the filter bars
        if (sel[f[0]] === 'all') return;
        var b = btnsOf(f[0]).filter(function(x){ return x.getAttribute('data-' + f[0]) === sel[f[0]]; })[0];
        if (b) { var sm = b.querySelector('.sm'); on.push((sm || b).textContent.trim()); }   // the short label, as on phones
      });
      rh.textContent = on.length ? on.join(' · ') : 'All';
    }
    try { var u = new URL(location.href); FILTERS.forEach(function(f){ if (sel[f[0]] === 'all') u.searchParams.delete(f[2]); else u.searchParams.set(f[2], sel[f[0]]); }); history.replaceState(null, '', u); } catch (e) {}
    if (restart) { play(0); steadyBanner(); }
  }
  function setPhase(ph, restart){ sel.ph = ph; apply(restart); }   // kept for other callers
  FILTERS.forEach(function(f){
    btnsOf(f[0]).forEach(function(b){ b.addEventListener('click', function(){ if (!b.disabled) { sel[f[0]] = b.getAttribute('data-' + f[0]); apply(true); } }); });
  });
  var anyWanted = false;
  try {
    var q = new URL(location.href).searchParams;
    FILTERS.forEach(function(f){ var w = q.get(f[2]); if (w && btnsOf(f[0]).some(function(b){ return b.getAttribute('data-' + f[0]) === w && !b.disabled; })) { sel[f[0]] = w; anyWanted = true; } });
  } catch (e) {}
  if (anyWanted) apply(false);
  var start = document.getElementById('fp-start');
  if (start) start.addEventListener('click', function(){ sound = true; blocked = false; play(0); });   // the big start button asks for sound
  document.getElementById('fp-prev').addEventListener('click', function(){ play(cur - 1); });
  document.getElementById('fp-next').addEventListener('click', function(){ play(cur + 1); });
  if (playBtn) playBtn.addEventListener('click', togglePlay);
  var back = document.getElementById('fp-back'), fwd = document.getElementById('fp-fwd');
  if (back) back.addEventListener('click', function(){ seekBy(-10); });
  if (fwd) fwd.addEventListener('click', function(){ seekBy(10); });
  // Keyboard: space = play/pause, arrow keys = 10 s back / forward (when not typing in a field).
  document.addEventListener('keydown', function(e){
    if (/INPUT|TEXTAREA|SELECT|BUTTON/.test(e.target.tagName)) return;
    if (e.key === ' ') { e.preventDefault(); togglePlay(); }
    else if (e.key === 'ArrowLeft') seekBy(-10);
    else if (e.key === 'ArrowRight') seekBy(10);
  });
  if (soundBtn) soundBtn.addEventListener('click', function(){ if (sound && blocked) blocked = false; else { sound = !sound; blocked = false; } applySound(); });
  // Full screen: the whole player where the browser allows it; iPhones only allow a video itself to go
  // full screen, so there the Vimeo player opens in the phone's own full-screen view.
  // Full screen = the site's own cinema mode. The player takes the whole screen with only a small control bar,
  // and reels with a fill crop (crops.py) are cropped to their picture and fill the width; outside cinema mode
  // they show their original frame. Real full screen where the browser allows it (computers, Android); iPhones
  // have none, so there the player fills the window, and when the phone is upright the picture is turned on
  // its side so you turn the phone to watch. The same button (Exit on the bar), Esc or leaving full screen ends it.
  var cineBar = document.createElement('div'); cineBar.className = 'cine-bar';
  var proxy = function(id, cls, label){
    var src = document.getElementById(id); if (!src) return null;
    var b = document.createElement('button'); b.type = 'button'; b.className = 'fp-btn ' + cls; b.setAttribute('aria-label', label);
    b.innerHTML = src.innerHTML;
    b.addEventListener('click', function(e){ e.stopPropagation(); src.click(); cineWake(); });
    cineBar.appendChild(b); return b;
  };
  var cExit = document.createElement('button'); cExit.type = 'button'; cExit.className = 'fp-btn cexit'; cExit.textContent = 'Exit';
  cExit.addEventListener('click', function(e){ e.stopPropagation(); cineOff(); });
  cineBar.appendChild(cExit);
  proxy('fp-prev', 'ic', 'Previous reel'); var cPlay = proxy('fp-play', 'ic cplay', 'Play / pause'); proxy('fp-next', 'ic', 'Next reel');
  var cSound = proxy('fp-sound', 'csound', 'Sound');
  stage.appendChild(cineBar);
  var mirror = function(){
    if (cPlay && playBtn) cPlay.classList.toggle('paused', playBtn.classList.contains('paused'));
    if (cSound && soundBtn) cSound.textContent = soundBtn.textContent;
  };
  if (window.MutationObserver) {
    if (playBtn) new MutationObserver(mirror).observe(playBtn, { attributes: true, attributeFilter: ['class'] });
    if (soundBtn) new MutationObserver(mirror).observe(soundBtn, { childList: true, characterData: true, subtree: true });
  }
  mirror();
  var cineT = null, realFs = false;
  function cineWake(){ stage.classList.remove('cine-hide'); clearTimeout(cineT); cineT = setTimeout(function(){ stage.classList.add('cine-hide'); }, 2500); }
  function cineOn(){ return stage.classList.contains('cinema'); }
  function recropNow(){ if (window.TSPcrop) window.TSPcrop(stage, slot.querySelector('iframe')); }
  function recropSoon(){ [0, 80, 300, 700, 1200].forEach(function(ms){ setTimeout(function(){ if (window.TSPcrop) window.TSPcrop(stage, slot.querySelector('iframe')); }, ms); }); }
  function cineTurn(){ stage.classList.toggle('turned', cineOn() && !inFs() && matchMedia('(orientation:portrait)').matches); recropSoon(); }
  function cineStart(){
    stage.classList.add('cinema'); document.documentElement.classList.add('cine-lock'); document.body.classList.add('cinema');
    var fn = stage.requestFullscreen || stage.webkitRequestFullscreen;
    if ((document.fullscreenEnabled || document.webkitFullscreenEnabled) && fn) {
      try {
        var r = fn.call(stage);
        var lock = function(){ realFs = true; try { screen.orientation.lock('landscape').catch(function(){}); } catch (x) {} };   // Android: turn to landscape
        if (r && r.then) r.then(function(){ lock(); cineTurn(); }).catch(function(){ cineTurn(); }); else lock();
      } catch (x) {}
    }
    cineTurn(); cineWake();
  }
  function cineOff(){
    if (!cineOn()) return;
    stage.classList.remove('cinema', 'turned', 'cine-hide', 'cine-fill'); document.documentElement.classList.remove('cine-lock'); document.body.classList.remove('cinema');
    clearTimeout(cineT);
    try { screen.orientation.unlock(); } catch (x) {}
    if (inFs()) { try { var x = (document.exitFullscreen || document.webkitExitFullscreen).call(document); if (x && x.catch) x.catch(function(){}); } catch (y) {} }
    recropSoon();
  }
  document.getElementById('fp-full').addEventListener('click', function(){ if (cineOn()) cineOff(); else cineStart(); });
  ['fullscreenchange', 'webkitfullscreenchange'].forEach(function(ev){ document.addEventListener(ev, function(){ if (!inFs() && realFs) { realFs = false; cineOff(); } else recropSoon(); }); });   // left real full screen (Esc, back gesture): leave cinema too
  window.addEventListener('orientationchange', function(){ if (cineOn()) setTimeout(cineTurn, 120); });
  document.addEventListener('keydown', function(e){ if (e.key === 'Escape' && cineOn()) cineOff(); });
  window.TSPcineTap = function(){ if (!cineOn()) return false; if (stage.classList.contains('cine-hide')) cineWake(); else { clearTimeout(cineT); stage.classList.add('cine-hide'); } return true; };

  // Turning a phone sideways fills the screen with the player and hides the overlays. Browsers only allow real
  // full screen after a touch, so where it exists (Android) the first tap goes full screen; iPhones have no page
  // full screen, so there the player simply fills the screen. Turning back upright leaves full screen.
  var landQ = window.matchMedia && matchMedia('(orientation:landscape) and (hover:none) and (pointer:coarse)');
  var fsPending = false;
  function inFs(){ return !!(document.fullscreenElement || document.webkitFullscreenElement); }
  function pageFs(){
    var fn = stage.requestFullscreen || stage.webkitRequestFullscreen;
    if (!(document.fullscreenEnabled || document.webkitFullscreenEnabled) || !fn) return false;
    try { var r = fn.call(stage); if (r && r.then) r.then(function(){ fsPending = false; }).catch(function(){}); } catch (x) {}
    return true;
  }
  function rotated(){
    if (landQ.matches) {
      try { stage.scrollIntoView({ block: 'start' }); } catch (x) {}
      document.body.classList.add('tv');
      fsPending = !inFs() && pageFs();   // some browsers allow it straight away; otherwise the first tap does it
    } else {
      fsPending = false;
      if (inFs()) { try { var x = (document.exitFullscreen || document.webkitExitFullscreen).call(document); if (x && x.catch) x.catch(function(){}); } catch (y) {} }
    }
  }
  if (landQ) {
    if (landQ.addEventListener) landQ.addEventListener('change', rotated); else if (landQ.addListener) landQ.addListener(rotated);
    window.TSPfsTap = function(){ if (fsPending && landQ.matches && !inFs()) { fsPending = false; pageFs(); return true; } return false; };
  }

  // Phones and tablets: swipe the video left for the next reel, right for the previous one; a tap shows or hides
  // the controls, as on YouTube (pause with the Play button); held upright, where the controls sit under the video, a tap plays or pauses.
  // The video players swallow touches, so a see-through layer over the video catches them. Up and down still
  // scroll the page; only a clearly sideways swipe changes the reel.
  if (window.matchMedia && matchMedia('(hover:none) and (pointer:coarse)').matches) {
    swipe = document.createElement('div'); swipe.className = 'fp-swipe'; swipe.setAttribute('aria-hidden', 'true');
    slot.appendChild(swipe);
    // A one-time hint on the video, until the visitor has swiped once.
    var seen = false; try { seen = localStorage.getItem('tsp-swiped') === '1'; } catch (x) {}
    var hint = null;
    if (!seen) {
      hint = document.createElement('span'); hint.className = 'fp-swipehint'; hint.textContent = '‹  Swipe for more reels  ›';
      swipe.appendChild(hint);
      setTimeout(function(){ if (hint) hint.classList.add('gone'); }, 5000);
    }
    var sx = 0, sy = 0, st = 0, moved = false, wasTv = false;
    // Two-finger pinch on the video, as in the iPhone's own video player. Spread the fingers: page → cinema mode
    // (Full screen) → fill the screen (edges trimmed). Pinch them together: fill → fit → back to the page.
    var pinch0 = 0, pinched = false;
    var spread = function(e){ var a = e.touches[0], c = e.touches[1]; return Math.hypot(a.clientX - c.clientX, a.clientY - c.clientY); };
    swipe.addEventListener('touchstart', function(e){ if (e.touches.length === 2) { pinch0 = spread(e); pinched = false; } }, { passive: true });
    swipe.addEventListener('touchmove', function(e){
      if (e.touches.length !== 2 || !pinch0 || pinched) return;
      if (e.cancelable) e.preventDefault();   // no page zoom while pinching the video
      var k = spread(e) / pinch0, filled = stage.classList.contains('cine-fill');
      if (k > 1.3) {
        pinched = true;
        if (!cineOn()) cineStart(); else if (!filled) { stage.classList.add('cine-fill'); recropNow(); }
      } else if (k < 0.75) {
        pinched = true;
        if (filled) { stage.classList.remove('cine-fill'); recropNow(); } else if (cineOn()) cineOff();
      }
    }, { passive: false });
    ['gesturestart', 'gesturechange'].forEach(function(ev){ swipe.addEventListener(ev, function(e){ e.preventDefault(); }, { passive: false }); });   // iPhone: keep its own pinch-zoom off the video
    swipe.addEventListener('touchstart', function(e){ wasTv = document.body.classList.contains('tv'); var t = e.touches[0]; sx = t.clientX; sy = t.clientY; st = Date.now(); moved = false; }, { passive: true });
    swipe.addEventListener('touchmove', function(e){ var t = e.touches[0]; if (Math.abs(t.clientX - sx) > 10 || Math.abs(t.clientY - sy) > 10) moved = true; }, { passive: true });
    swipe.addEventListener('touchend', function(e){
      if (pinch0) { if (!e.touches.length) pinch0 = 0; return; }   // the end of a pinch is neither a swipe nor a tap
      var t = e.changedTouches[0], dx = t.clientX - sx, dy = t.clientY - sy;
      if (stage.classList.contains('turned')) { var q = dx; dx = dy; dy = -q; }   // cinema mode turned on its side: the picture's left-right runs down the screen
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) {
        var dir = dx < 0 ? 1 : -1;
        if (hint) { hint.classList.add('gone'); hint = null; try { localStorage.setItem('tsp-swiped', '1'); } catch (x) {} }
        try { slot.animate([{ transform: 'translateX(0)', opacity: 1 }, { transform: 'translateX(' + (dir > 0 ? -40 : 40) + 'px)', opacity: .2 }], { duration: 180, easing: 'ease-in' }); } catch (x) {}
        setTimeout(function(){ play(cur + dir); }, 170);
      } else if (!moved && Date.now() - st < 400) {
        // Phone held upright: the controls sit under the video and always show, so a tap still plays or pauses.
        if (window.TSPcineTap && window.TSPcineTap()) return;   // cinema mode: a tap shows or hides its control bar
        if (matchMedia('(orientation:portrait) and (max-width:760px)').matches) { if (playBtn) togglePlay(); }
        // sideways: site.js shows or hides the overlays
      }
    }, { passive: true });
  }

  // Start straight away, muted (browsers only allow sound after a click).
  play(0);
  steadyBanner();
  // once the fonts are in, measure again, then let the phone layout refit around the settled banner
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function(){ steadyBanner(); try { window.dispatchEvent(new Event('orientationchange')); } catch (e) {} });
  var sbT; window.addEventListener('resize', function(){ clearTimeout(sbT); sbT = setTimeout(steadyBanner, 200); });
})();
