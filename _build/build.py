#!/usr/bin/env python3
"""Builds every page of thesexpixels.com except /pipeline/.

Run:  python3 _build/build.py   (from the repo root)

Why a build script: the header, menu and footer appear on every page. Keeping
them here once means a menu change is made in one place, not six.
GitHub Pages ignores folders that start with "_", so this folder is never published.
"""
import html, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from skills_data import stages

E = html.escape
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- reels
# Add a reel by filling in its video: "vimeo:ID:HASH" or "youtube:ID". None = coming soon.
REEL_2026 = "vimeo:1232958213:ffbea294d7"
REELS = [
    dict(id="reel-filmmaker", role="Filmmaker", title="Filmmaking showreel", note="Showreel",
         line="Writing, directing and camera work.", video=None, url=None),
    dict(id="reel-compositor", role="Nuke compositor", title="Compositing showreel", note="Showreel · 2026",
         line="The latest compositing reel.", video=REEL_2026, url="https://vimeo.com/1232958213/ffbea294d7"),
    dict(id="reel-vfx-supervisor", role="VFX supervisor", title="VFX supervisor showreel", note="Showreel",
         line="On-set and post supervision across film, episodic and commercials.", video=None, url=None),
    dict(id="reel-sizzle", role="Archive", title="Sizzle reel", note="02:30",
         line="Seventeen years of work in two and a half minutes.", video="youtube:SDAXjN_sOlE",
         url="https://youtu.be/SDAXjN_sOlE", thumb="https://i.ytimg.com/vi/SDAXjN_sOlE/hqdefault.jpg"),
]
INSTAGRAM = "https://www.instagram.com/t_h_e__p_i_x_x_x_e_l_s"

def reel_link(r):
    return f'href="{r["url"]}" data-video="{r["video"]}"' if r["video"] else f'href="/work/#{r["id"]}"'

# ---------------------------------------------------------------- shared parts
FONTS_SITE = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
              '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
              '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,75..125,400..900;1,75..125,400..900&family=IBM+Plex+Mono:wght@400;600&display=swap">')
FONTS_FLEAPIT = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=IBM+Plex+Sans:wght@400;500;600&family=Yellowtail&display=swap">'

def head(title, desc, extra=""):
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="theme-color" content="#111012">
{FONTS_SITE}
{extra}<link rel="stylesheet" href="/assets/site.css">
</head>'''

def header(current=""):
    def a(href, label, key):
        cur = ' aria-current="page"' if key == current else ""
        return f'<li><a href="{href}"{cur}>{label}</a></li>'
    reels = "\n      ".join(f'<li><a {reel_link(r)}>{r["role"].title().replace("Vfx","VFX")}</a></li>' for r in REELS[:3])
    return f'''<header class="nav" id="nav">
  <a class="mark" href="/" aria-label="Mark Pinheiro, VFX Supervisor, home"><b>Mark Pinheiro</b><small>VFX Supervisor</small></a>
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
  <nav aria-label="Main" id="menu">
    <ul>
      {reels}
      <li class="sep" aria-hidden="true"></li>
      {a("/work/", "Work", "work")}
      {a("/skills/", "Skills", "skills")}
      {a("/fleapit/", "The Fleapit", "fleapit")}
      {a("/about/", "About", "about")}
      {a("/contact/", "Contact", "contact")}
    </ul>
  </nav>
</header>'''

FOOTER = '''<footer>
  <span>© The Sex Pixels Ltd.</span>
  <span class="avail">Available <b>now</b> worldwide</span>
</footer>

<script src="/assets/site.js"></script>'''

TREE = '''<div class="tree">
            <div style="--c:#eeeae4"><span></span>/jobs/Production_Name/</div>
            <div style="--c:#b8b2ab;--a:18px;--b:0px"><span></span>00_Production_Tracking</div>
            <div style="--c:#39d7ff;--a:18px;--b:36px"><span></span>editorial</div>
            <div style="--c:#d4497c;--a:18px;--b:36px"><span></span>vfx</div>
            <div style="--c:#ff7aa6;--a:36px;--b:54px"><span></span>SEQ010 / SH010</div>
            <div style="--c:#5fe0c8;--a:18px;--b:0px"><span></span>Deliverables</div>
          </div>'''

def slate(top, big):
    return f'<div class="thumb" aria-hidden="true"><div class="slate"><span class="st">{E(top)}</span><span class="no">{E(big)}</span></div></div>'

def reel_tile(r):
    if r["video"]:
        if r.get("thumb"):
            img = f'<img src="{r["thumb"]}" alt="" loading="lazy">'
        elif r["video"].startswith("vimeo"):
            img = f'<img data-vimeo="{r["url"]}" alt="" hidden>'
        else:
            img = ""
        return f'''      <a class="card" id="{r["id"]}" {reel_link(r)}>
        <div class="thumb">{img}<span class="play"></span></div>
        <div class="meta">
          <span class="kicker">{E(r["role"])}</span>
          <span class="client">{E(r["note"])}</span>
          <h3>{E(r["title"])}</h3>
          <p>{E(r["line"])}</p>
          <span class="go">Play →</span>
        </div>
      </a>'''
    return f'''      <div class="card" id="{r["id"]}">
        {slate("Showreel", r["role"].split()[0])}
        <div class="meta">
          <span class="kicker">{E(r["role"])}</span>
          <span class="client">{E(r["note"])}</span>
          <h3>{E(r["title"])}</h3>
          <p>{E(r["line"])}</p>
          <span class="go soon">Coming soon</span>
        </div>
      </div>'''

def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)

def page_intro(n, label, title, lede=""):
    lede_html = f'\n    <p class="pagelede">{lede}</p>' if lede else ""
    return f'''    <div class="rail"><span class="n">{n}</span>{label}</div>
    <h1 class="pagetitle">{title}</h1>{lede_html}'''

# ---------------------------------------------------------------- home
home = head("Mark Pinheiro · Filmmaker / VFX / AI",
            "Mark Pinheiro: filmmaker, Nuke compositor and VFX supervisor.",
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Yellowtail&display=swap">\n') + f'''
<body>

{header()}

<main id="top">
  <section class="hero" aria-label="Showreel" style="padding:0;max-width:none">
    <iframe
      src="https://player.vimeo.com/video/1232958213?h=ffbea294d7&amp;background=1&amp;autoplay=1&amp;muted=1&amp;loop=1&amp;autopause=0&amp;controls=0&amp;title=0&amp;byline=0&amp;portrait=0&amp;dnt=1"
      title="Mark Pinheiro compositing showreel 2026, playing muted in the background"
      allow="autoplay; fullscreen; picture-in-picture"
      tabindex="-1"></iframe>
    <div class="reelbar">
      <span class="lab"><b>Compositing showreel</b> · 2026</span>
      <a class="pill" href="https://vimeo.com/1232958213/ffbea294d7" data-video="{REEL_2026}"><i></i>Watch full screen</a>
    </div>
  </section>

  <section class="doors" aria-label="Sections">
    <div class="cards">
      <a class="card" href="/work/">
        <div class="thumb"><img data-vimeo="https://vimeo.com/1232958213/ffbea294d7" alt="" hidden></div>
        <div class="meta">
          <span class="kicker">01 · Work</span>
          <h3>Showreels &amp; finals</h3>
          <p>Project showreels and finished shots.</p>
          <span class="go">Work →</span>
        </div>
      </a>
      <a class="card" href="/skills/">
        <div class="thumb" aria-hidden="true">{TREE}</div>
        <div class="meta">
          <span class="kicker">02 · Skills</span>
          <h3>Skills &amp; R&amp;D</h3>
          <p>21 disciplines across 7 stages of production, each with a working demo as it is made.</p>
          <span class="go">Skills →</span>
        </div>
      </a>
      <a class="card" href="/fleapit/">
        <div class="thumb fleapit-thumb" aria-hidden="true"><span>The Fleapit.</span></div>
        <div class="meta">
          <span class="kicker">03 · The Fleapit</span>
          <h3>Filmmaking experiments</h3>
          <p>Uncommercials, fake trailers, idents and film essays.</p>
          <span class="go">The Fleapit →</span>
        </div>
      </a>
    </div>
  </section>
</main>

{FOOTER}
</body>
</html>
'''
write("index.html", home)

# ---------------------------------------------------------------- work
work = head("Work · Mark Pinheiro", "Mark Pinheiro's showreels and finished shots.") + f'''
<body>

{header("work")}

<main>
  <section class="page">
{page_intro("01", "Work", "Work", "Project showreels and finals.")}
    <div class="cards">
{chr(10).join(reel_tile(r) for r in REELS)}
    </div>
  </section>
</main>

{FOOTER}
</body>
</html>
'''
write("work/index.html", work)

# ---------------------------------------------------------------- skills
filters = "\n".join(f'      <button type="button" data-f="{n}" aria-pressed="false">{n} · {E(name)}</button>' for n, name, _ in stages)
tiles = []
for n, name, cards in stages:
    for i, (title, items, credit) in enumerate(cards, 1):
        no = f"{n}.{i}"
        line = E(" · ".join(items))
        if no == "00.1":
            tiles.append(f'''      <a class="card" href="/pipeline/" data-stage="{n}">
        <div class="thumb" aria-hidden="true">{TREE}</div>
        <div class="meta">
          <span class="kicker">{no} · {E(name)}</span>
          <span class="client">{E(credit)}</span>
          <h3>{E(title)}</h3>
          <p>{line}</p>
          <span class="go">Open the demo: Scale dictates structure →</span>
        </div>
      </a>''')
        else:
            tiles.append(f'''      <div class="card" data-stage="{n}">
        {slate(f"{n} · {name}", no)}
        <div class="meta">
          <span class="kicker">{no} · {E(name)}</span>
          <span class="client">{E(credit)}</span>
          <h3>{E(title)}</h3>
          <p>{line}</p>
          <span class="go soon">Demo in production</span>
        </div>
      </div>''')
skills = head("Skills · Mark Pinheiro",
              "Mark Pinheiro's skills and R&D: 21 disciplines across 7 stages of production, from planning the shoot to final delivery.") + f'''
<body>

{header("skills")}

<main>
  <section class="page">
{page_intro("02", "Skills · R&amp;D", "Skills", "21 disciplines across 7 stages of production. Each gets a working demo as it is made, and new areas are added as I explore them.")}
    <div class="filters" role="group" aria-label="Filter by stage">
      <button type="button" data-f="all" aria-pressed="true">All</button>
{filters}
    </div>
    <div class="cards" id="tiles">
{chr(10).join(tiles)}
    </div>
  </section>
</main>

{FOOTER}
<script>
// Stage filters, like the category filters on Framestore's work page.
(function(){{
  var btns = document.querySelectorAll('.filters button'), tiles = document.querySelectorAll('#tiles .card');
  btns.forEach(function(b){{
    b.addEventListener('click', function(){{
      var f = b.getAttribute('data-f');
      btns.forEach(function(x){{ x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }});
      tiles.forEach(function(t){{ t.hidden = !(f === 'all' || t.getAttribute('data-stage') === f); }});
    }});
  }});
}})();
</script>
</body>
</html>
'''
write("skills/index.html", skills)

# ---------------------------------------------------------------- the fleapit
# Its own house style (the Fleapit design system), inside the site's frame. Ready to move to its own domain.
PROGRAMME = [
    ("19:00", "Idents & stings", "Short openers and channel idents."),
    ("19:05", "Local-shop ads", "Cheap uncommercials for the corner shop."),
    ("19:15", "Uncommercials", "High-end ad craft advertising the flaw the maker would rather you didn't notice."),
    ("19:40", "Coming attractions", "Trailers for films that don't exist."),
    ("19:55", "The short", "Short films in the 70s pre-feature slot."),
    ("20:15", "Film essays", "Clips from the archive, picked and discussed."),
]
rows = "\n".join(f'''        <li><span class="t">{t}</span><span class="w"><b>{E(w)}</b><span>{E(d)}</span></span><span class="s">Coming soon</span></li>''' for t, w, d in PROGRAMME)
fleapit = head("The Fleapit. SE1 · Mark Pinheiro",
               "The Fleapit. SE1: Mark Pinheiro's filmmaking experiments. Uncommercials, fake trailers, idents and film essays.",
               FONTS_FLEAPIT + "\n") + f'''
<body class="fleapit">

{header("fleapit")}

<main>
  <section class="fp-hero">
    <p class="fp-sign" aria-label="The Fleapit.">The Fleapit.</p>
    <p class="fp-sub">SE1 · Filmmaking experiments by Mark Pinheiro</p>
    <p class="fp-lead">Uncommercials, fake trailers, idents and film essays. Shot on iPhone, finished with VFX and AI, and programmed like the reel before the feature.</p>
    <a class="fp-ticket" href="{INSTAGRAM}" target="_blank" rel="noopener">Follow the programme on Instagram</a>
  </section>

  <section class="fp-programme" aria-labelledby="tonight">
    <h2 id="tonight">Tonight's programme</h2>
    <ol>
{rows}
    </ol>
    <p class="fp-note">New reels go up on Instagram first.</p>
  </section>
</main>

{FOOTER}
</body>
</html>
'''
write("fleapit/index.html", fleapit)

# ---------------------------------------------------------------- about
about = head("About · Mark Pinheiro",
             "Mark Pinheiro: filmmaker, Nuke compositor and VFX supervisor. Twenty-six years in visual effects.") + f'''
<body>

{header("about")}

<main>
  <section class="profile">
    <h1>Mark<br>Pinheiro</h1>
    <div class="roles"><span class="a">Filmmaker / VFX / AI</span><span>Nuke compositor &amp; VFX supervisor</span><span>London</span></div>
    <div class="bio">
      <div>
        <p class="lede">Filmmaker, Nuke compositor and VFX supervisor, with twenty-six years in visual effects.</p>
        <p>His first composite, in 1995, was a VH1 promo that won a Promax Gold. Regular VFX work followed from 2000: on-set supervision, previz, compositing and post, across feature film, episodic, commercials and music promos.</p>
        <p>He wrote the compositing course at Escape Studios in London, and still designs courses for the NFTS, ECAM Madrid and Escape Studios.</p>
        <p>He holds an MA in Writing for Script &amp; Screen from Falmouth University, and he is an <strong>agentic coder</strong>: every tool he builds is written with AI.</p>
        <p>He works through his boutique studio, The Sex Pixels, pairing traditional VFX craft with ethical AI.</p>
        <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:10px"><a class="pill" href="https://vimeo.com/1232958213/ffbea294d7" data-video="{REEL_2026}"><i></i>Compositing showreel</a><a class="pill ghost" href="/skills/">Skills →</a></div>
      </div>
      <div>
        <figure class="quote">
          <blockquote>“Mark has an undeniably impressive portfolio and his understanding of the industry as a whole makes him a total catch.”</blockquote>
          <figcaption>David Smith, CEO, Absolute · Televisual</figcaption>
        </figure>
        <figure class="quote">
          <blockquote>“…he trained a large portion of London’s VFX community.”</blockquote>
          <figcaption><a href="https://www.televisual.com/news/mark-pinheiro-joins-absolute-as-vfx-super/" style="text-decoration:none">Televisual, 2022 · on Escape Studios</a></figcaption>
        </figure>
        <ul class="awards" aria-label="Awards">
          <li>Promax</li><li>UK MVA</li><li>Oscar ×2</li><li>BAFTA ×2</li><li>Emmy ×2</li><li>VES</li><li>HPA</li>
        </ul>
        <div class="awards-note">Won outright, or as part of the show's team</div>
      </div>
    </div>
  </section>
</main>

{FOOTER}
</body>
</html>
'''
write("about/index.html", about)

# ---------------------------------------------------------------- contact
contact = head("Contact · Mark Pinheiro", "Contact Mark Pinheiro and The Sex Pixels Ltd.") + f'''
<body>

{header("contact")}

<main>
  <section class="page">
{page_intro("05", "Contact", "Let's talk")}
    <div class="contact">
      <div><a class="email" href="mailto:info@thesexpixels.com">info@thesexpixels.com</a></div>
      <address>
        <b>The Sex Pixels Ltd.</b>
        Fifth Floor, Mariner House<br>
        62 Prince Street, Bristol<br>
        BS1 4QD
      </address>
    </div>
  </section>
</main>

{FOOTER}
</body>
</html>
'''
write("contact/index.html", contact)
print("built: index, work, skills, fleapit, about, contact")
