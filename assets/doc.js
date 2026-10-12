// About page: the commentated showreels play as one documentary, chapter after chapter, with sound.
(function(){
  var stage = document.getElementById('doc-stage'), start = document.getElementById('doc-start'), now = document.getElementById('doc-now');
  var chs = [].slice.call(document.querySelectorAll('.doc-ch'));
  if (!stage || !chs.length) return;
  var cur = -1, api;
  function vimeo(){
    return api || (api = new Promise(function(res, rej){
      if (window.Vimeo) return res();
      var s = document.createElement('script'); s.src = 'https://player.vimeo.com/api/player.js'; s.onload = res; s.onerror = rej; document.head.appendChild(s);
    }));
  }
  function play(i){
    if (i >= chs.length) { cur = -1; now.textContent = 'The end · thanks for watching'; return; }
    cur = i; var c = chs[i], mine = i;
    chs.forEach(function(x, k){ x.classList.toggle('on', k === i); });
    now.textContent = 'Chapter ' + (i + 1) + ' of ' + chs.length + ' · ' + c.getAttribute('data-title');
    var f = document.createElement('iframe');
    f.src = 'https://player.vimeo.com/video/' + c.getAttribute('data-id') + '?autoplay=1&autopause=0&texttrack=false&title=0&byline=0&portrait=0&dnt=1';
    f.setAttribute('allow', 'autoplay; fullscreen; picture-in-picture; encrypted-media'); f.setAttribute('allowfullscreen', '');
    f.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');   // lets Vimeo see the site, for domain-restricted videos
    f.title = 'In his own words · ' + c.getAttribute('data-title');
    stage.innerHTML = ''; stage.appendChild(f); stage.classList.add('playing');
    vimeo().then(function(){
      if (cur !== mine) return;
      var p = new window.Vimeo.Player(f);
      p.on('ended', function(){ if (cur === mine) play(mine + 1); });
      p.on('error', function(){ if (cur === mine) setTimeout(function(){ play(mine + 1); }, 1500); });
      setTimeout(function(){   // browser refused to start with sound: start muted instead of stalling
        if (cur !== mine) return;
        p.getPaused().then(function(paused){ if (paused && cur === mine) { p.setMuted(true); return p.play(); } }).catch(function(){});
      }, 2500);
    }).catch(function(){});
  }
  start.addEventListener('click', function(){ play(0); });
  chs.forEach(function(c, k){ c.addEventListener('click', function(){ play(k); stage.scrollIntoView({ behavior: 'smooth', block: 'center' }); }); });
})();
