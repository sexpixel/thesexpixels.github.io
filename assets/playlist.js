// Playlist player (The Fleapit, Nuke Compositor, VFX Supervisor): plays every reel in the grid, one after another.
// Vimeo and YouTube reels advance by themselves when they end. Instagram allows no
// "ended" signal, so on an Instagram reel the player waits for the Next button.
(function(){
  var cells = [].slice.call(document.querySelectorAll('.fp-cell[data-src]'));
  if (!cells.length) return;
  var stage = document.getElementById('fp-player'), slot = document.getElementById('fp-slot'), titleEl = document.getElementById('fp-title');
  var cur = -1, player = null, sound = false, vimeoReady, ytReady;
  var soundBtn = document.getElementById('fp-sound');
  function showSound(){ if (soundBtn) { soundBtn.textContent = sound ? 'Sound off' : 'Sound on'; soundBtn.setAttribute('aria-pressed', sound ? 'true' : 'false'); } }
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
    titleEl.textContent = 'Now playing · ' + (i + 1) + ' / ' + cells.length + ' · ' + c.getAttribute('data-title');
    showSound();
    stage.style.removeProperty('--ar');
    // Per-reel crop (set on the tuning page) pushes text in the black bars off screen.
    if (c.getAttribute('data-crop')) stage.setAttribute('data-crop', c.getAttribute('data-crop')); else stage.removeAttribute('data-crop');
    stage.classList.add('playing'); stage.classList.toggle('tall', p[0] === 'instagram');
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
          'autoplay=1&texttrack=false&muted=' + (sound ? 0 : 1) + '&title=0&byline=0&portrait=0&dnt=1&playsinline=1';
        f.title = c.getAttribute('data-title');
        f.setAttribute('allow', 'autoplay; fullscreen; picture-in-picture; encrypted-media');
        f.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');   // lets Vimeo see the site, for domain-restricted videos
        slot.replaceChild(f, box);
        if (window.TSPcrop) window.TSPcrop(stage, f);
        player = new window.Vimeo.Player(f);
        player.on('ended', next);
        if (player.disableTextTrack) player.disableTextTrack().catch(function(){});   // no subtitles
        Promise.all([player.getVideoWidth(), player.getVideoHeight()]).then(function(d){
          if (cur === mine && d[0] && d[1]) { stage.style.setProperty('--ar', d[0] / d[1]); if (window.TSPcrop) window.TSPcrop(stage, f); }
        }).catch(function(){});
      }).catch(function(){});
    } else if (p[0] === 'youtube') {
      yt().then(function(){
        if (cur !== mine) return;
        player = new window.YT.Player(box, { videoId: p[1], playerVars: { autoplay: 1, mute: sound ? 0 : 1, rel: 0, modestbranding: 1, playsinline: 1, cc_load_policy: 0, iv_load_policy: 3 },
          events: { onReady: function(e){
                      noCaptions(e.target);
                      if (window.TSPcrop) window.TSPcrop(stage, slot.querySelector('iframe')); },
                    onApiChange: function(e){ noCaptions(e.target); },   // fires when YouTube loads its captions module
                    onStateChange: function(e){
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

  cells.forEach(function(c, k){
    c.addEventListener('click', function(){ sound = true; play(k); stage.scrollIntoView({ behavior: 'smooth', block: 'center' }); });
  });
  var start = document.getElementById('fp-start');
  if (start) start.addEventListener('click', function(){ sound = true; play(0); });
  document.getElementById('fp-prev').addEventListener('click', function(){ sound = true; play(cur - 1); });
  document.getElementById('fp-next').addEventListener('click', function(){ sound = true; play(cur + 1); });
  if (soundBtn) soundBtn.addEventListener('click', function(){ sound = !sound; applySound(); });
  document.getElementById('fp-full').addEventListener('click', function(){ if (stage.requestFullscreen) stage.requestFullscreen().catch(function(){}); });

  // Start straight away, muted (browsers only allow sound after a click).
  play(0);
})();
