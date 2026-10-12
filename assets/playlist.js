// Playlist player (The Fleapit, Nuke Compositor): plays every reel in the grid, one after another.
// Vimeo and YouTube reels advance by themselves when they end. Instagram allows no
// "ended" signal, so on an Instagram reel the player waits for the Next button.
(function(){
  var cells = [].slice.call(document.querySelectorAll('.fp-cell[data-src]'));
  if (!cells.length) return;
  var stage = document.getElementById('fp-player'), slot = document.getElementById('fp-slot'), titleEl = document.getElementById('fp-title');
  var cur = -1, player = null, sound = false, vimeoReady, ytReady;

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
  function clear(){ if (player && player.destroy) { try { player.destroy(); } catch (e) {} } player = null; slot.innerHTML = ''; }

  function play(i){
    if (i < 0) i = cells.length - 1;
    if (i >= cells.length) i = 0;
    cur = i;
    var c = cells[i], spec = c.getAttribute('data-src'), p = spec.split(':'), mine = i;
    cells.forEach(function(x, k){ x.classList.toggle('on', k === i); });
    titleEl.textContent = (i + 1) + ' / ' + cells.length + ' · ' + c.getAttribute('data-title');
    stage.classList.add('playing'); stage.classList.toggle('tall', p[0] === 'instagram');
    clear();
    var box = document.createElement('div'); slot.appendChild(box);
    var next = function(){ if (cur === mine) play(cur + 1); };
    if (p[0] === 'vimeo') {
      vimeo().then(function(){
        if (cur !== mine) return;
        player = new window.Vimeo.Player(box, { url: 'https://vimeo.com/' + p[1] + (p[2] ? '/' + p[2] : ''), autoplay: true, muted: !sound,
          title: false, byline: false, portrait: false, dnt: true });
        player.on('ended', next);
      });
    } else if (p[0] === 'youtube') {
      yt().then(function(){
        if (cur !== mine) return;
        player = new window.YT.Player(box, { videoId: p[1], playerVars: { autoplay: 1, mute: sound ? 0 : 1, rel: 0, modestbranding: 1, playsinline: 1 },
          events: { onStateChange: function(e){ if (e.data === 0) next(); } } });
      });
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
  document.getElementById('fp-full').addEventListener('click', function(){ if (stage.requestFullscreen) stage.requestFullscreen().catch(function(){}); });

  // Start straight away, muted (browsers only allow sound after a click).
  play(0);
})();
