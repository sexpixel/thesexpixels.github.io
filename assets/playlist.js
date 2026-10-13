// Playlist player (The Fleapit, Nuke Compositor, VFX Supervisor): plays every reel in the grid, one after another.
// Vimeo and YouTube reels advance by themselves when they end. Instagram allows no
// "ended" signal, so on an Instagram reel the player waits for the Next button.
(function(){
  var allCells = [].slice.call(document.querySelectorAll('.fp-cell[data-src]'));
  if (!allCells.length) return;
  var noneHere = false;
  var cells = allCells;   // the reels that play: all of them, or just those in the chosen production phase
  var stage = document.getElementById('fp-player'), slot = document.getElementById('fp-slot'), titleEl = document.getElementById('fp-title');
  var cur = -1, player = null, sound = false, vimeoReady, ytReady;
  var soundBtn = document.getElementById('fp-sound');
  function showSound(){ if (soundBtn) { soundBtn.textContent = sound ? 'Sound off' : 'Sound on'; soundBtn.setAttribute('aria-pressed', sound ? 'true' : 'false'); } }
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
    try {
      if (typeof player.unMute === 'function') { if (sound) { player.unMute(); player.setVolume(100); } else player.mute(); }   // YouTube
      else { if (player.setMuted) player.setMuted(!sound); player.setVolume(sound ? 1 : 0); }                                // Vimeo
    } catch (e) {}
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
  function clear(){ if (player && player.destroy) { try { player.destroy(); } catch (e) {} } player = null; slot.innerHTML = ''; }

  function play(i){
    if (i < 0) i = cells.length - 1;
    if (i >= cells.length) i = 0;
    cur = i;
    var c = cells[i], spec = c.getAttribute('data-src'), p = spec.split(':'), mine = i;
    cells.forEach(function(x, k){ x.classList.toggle('on', k === i); });
    titleEl.textContent = (noneHere ? 'No reels in this phase yet · ' : '') + 'Now playing · ' + (i + 1) + ' / ' + cells.length + ' · ' + c.getAttribute('data-title');
    showSound();
    stage.style.removeProperty('--ar');
    // Per-reel crop (set on the tuning page) pushes text in the black bars off screen.
    if (c.getAttribute('data-crop')) stage.setAttribute('data-crop', c.getAttribute('data-crop')); else stage.removeAttribute('data-crop');
    stage.classList.add('playing'); stage.classList.toggle('tall', p[0] === 'instagram');
    showPaused(false);
    clear();
    var box = document.createElement('div'); slot.appendChild(box);
    var next = function(){ if (cur === mine) play(cur + 1); };
    if (p[0] === 'vimeo') {
      vimeo().then(function(){
        if (cur !== mine) return;
        // Build the iframe ourselves (no width/height from Vimeo), then size it to cover the screen
        // using the video's real shape, so 4:3, 16:9 and scope reels all fill edge to edge.
        var f = document.createElement('iframe');
        f.src = 'https://player.vimeo.com/video/' + p[1] + '?' + (p[2] ? 'h=' + p[2] + '&' : '') +
          'autoplay=1&autopause=0&transparent=0&controls=0&texttrack=false&muted=' + (sound ? 0 : 1) + '&title=0&byline=0&portrait=0&dnt=1&playsinline=1';
        f.title = c.getAttribute('data-title');
        f.setAttribute('allow', 'autoplay; fullscreen; picture-in-picture; encrypted-media');
        f.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');   // lets Vimeo see the site, for domain-restricted videos
        slot.replaceChild(f, box);
        if (window.TSPcrop) window.TSPcrop(stage, f);
        player = new window.Vimeo.Player(f);
        player.on('ended', next);
        player.on('play', function(){ showPaused(false); });
        player.on('pause', function(){ showPaused(true); });
        player.on('error', function(){ setTimeout(next, 1500); });   // a video that can't play (privacy, removed) is skipped
        if (window.TSPnoSubs) window.TSPnoSubs(player); else if (player.disableTextTrack) player.disableTextTrack().catch(function(){});   // no subtitles, even if Vimeo turns them on later
        // If the browser refuses to start the next video with sound, start it muted rather than stall.
        var vp = player;
        setTimeout(function(){
          if (cur !== mine || !vp.getPaused) return;
          vp.getPaused().then(function(paused){
            if (paused && cur === mine) { sound = false; showSound(); vp.setMuted(true); vp.setVolume(0); return vp.play(); }
          }).catch(function(){});
        }, 2500);
        Promise.all([player.getVideoWidth(), player.getVideoHeight()]).then(function(d){
          if (cur === mine && d[0] && d[1]) { stage.style.setProperty('--ar', d[0] / d[1]); if (window.TSPcrop) window.TSPcrop(stage, f); }
        }).catch(function(){});
      }).catch(function(){});
    } else if (p[0] === 'youtube') {
      yt().then(function(){
        if (cur !== mine) return;
        player = new window.YT.Player(box, { videoId: p[1], playerVars: { autoplay: 1, controls: 0, mute: sound ? 0 : 1, rel: 0, modestbranding: 1, playsinline: 1, cc_load_policy: 0, iv_load_policy: 3 },
          events: { onReady: function(e){
                      noCaptions(e.target);
                      var yp = e.target;
                      setTimeout(function(){
                        try { if (cur === mine && yp.getPlayerState && yp.getPlayerState() !== 1) { sound = false; showSound(); yp.mute(); yp.playVideo(); } } catch (x) {}
                      }, 2500);
                      if (window.TSPcrop) window.TSPcrop(stage, slot.querySelector('iframe')); },
                    onApiChange: function(e){ noCaptions(e.target); },   // fires when YouTube loads its captions module
                    onError: function(){ setTimeout(next, 1500); },   // unplayable YouTube video: skip it
                    onStateChange: function(e){
                      if (e.data === 1 || e.data === 2) showPaused(e.data === 2);
                      if (e.data === 1) { noCaptions(e.target); setTimeout(function(){ noCaptions(e.target); }, 1500); }   // playing
                      if (e.data === 0) next(); } } });
      }).catch(function(){});
    } else if (p[0] === 'instagram') {
      var f = document.createElement('iframe');
      f.src = 'https://www.instagram.com/reel/' + p[1] + '/embed'; f.title = c.getAttribute('data-title');
      f.setAttribute('allow', 'autoplay; fullscreen; picture-in-picture');
      slot.replaceChild(f, box);
    }
  }

  allCells.forEach(function(c){
    c.addEventListener('click', function(){ sound = true; play(Math.max(0, cells.indexOf(c))); stage.scrollIntoView({ behavior: 'smooth', block: 'center' }); });
  });

  // Production-phase filter: All, Development … Distribution. Filters the grid and the playlist.
  var phaseBtns = [].slice.call(document.querySelectorAll('.phases button[data-ph]'));
  var tiles = [].slice.call(document.querySelectorAll('.fp-grid .fp-cell'));
  function inPhase(el, ph){ return ph === 'all' || (' ' + (el.getAttribute('data-phases') || '') + ' ').indexOf(' ' + ph + ' ') >= 0; }
  function setPhase(ph, restart){
    phaseBtns.forEach(function(b){ b.setAttribute('aria-pressed', b.getAttribute('data-ph') === ph ? 'true' : 'false'); });
    tiles.forEach(function(t){ t.hidden = !inPhase(t, ph); });
    cells = allCells.filter(function(c){ return inPhase(c, ph); });
    noneHere = !cells.length;   // the phase has projects listed but no reels yet: keep playing everything
    if (noneHere) cells = allCells;
    try { var u = new URL(location.href); if (ph === 'all') u.searchParams.delete('phase'); else u.searchParams.set('phase', ph); history.replaceState(null, '', u); } catch (e) {}
    if (restart) play(0);
  }
  phaseBtns.forEach(function(b){ b.addEventListener('click', function(){ if (!b.disabled) setPhase(b.getAttribute('data-ph'), true); }); });
  var wanted = null;
  try { wanted = new URL(location.href).searchParams.get('phase'); } catch (e) {}
  if (wanted && phaseBtns.some(function(b){ return b.getAttribute('data-ph') === wanted && !b.disabled; })) setPhase(wanted, false);
  var start = document.getElementById('fp-start');
  if (start) start.addEventListener('click', function(){ sound = true; play(0); });
  document.getElementById('fp-prev').addEventListener('click', function(){ sound = true; play(cur - 1); });
  document.getElementById('fp-next').addEventListener('click', function(){ sound = true; play(cur + 1); });
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
  if (soundBtn) soundBtn.addEventListener('click', function(){ sound = !sound; applySound(); });
  // Full screen: the whole player where the browser allows it; iPhones only allow a video itself to go
  // full screen, so there the Vimeo player opens in the phone's own full-screen view.
  document.getElementById('fp-full').addEventListener('click', function(){
    var fs = stage.requestFullscreen || stage.webkitRequestFullscreen;
    if (fs) { try { var r = fs.call(stage); if (r && r.catch) r.catch(function(){ if (player && player.requestFullscreen) player.requestFullscreen().catch(function(){}); }); } catch (e) {} }
    else if (player && player.requestFullscreen) player.requestFullscreen().catch(function(){});
  });

  // Start straight away, muted (browsers only allow sound after a click).
  play(0);
})();
