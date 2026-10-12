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
from work_data import PROJECTS, ROLE_GROUPS, FORMATS

E = html.escape
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- reels
# Add a reel by filling in its video: "vimeo:ID:HASH" or "youtube:ID". None = coming soon.
REEL_2026 = "vimeo:1232958213:ffbea294d7"
REELS = [
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
    cur_f = ' aria-current="page"' if current == "fleapit" else ""
    reels = f'<li><a href="/fleapit/"{cur_f}>Filmmaker</a></li>\n      ' + "\n      ".join(
        f'<li><a {reel_link(r)}>{r["role"].title().replace("Vfx","VFX")}</a></li>' for r in REELS[:2])
    return f'''<header class="nav" id="nav">
  <a class="mark" href="/" aria-label="Mark Pinheiro, VFX Supervisor, home"><b>Mark Pinheiro</b><small>VFX Supervisor</small></a>
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
  <nav aria-label="Main" id="menu">
    <ul>
      {reels}
      <li class="sep" aria-hidden="true"></li>
      {a("/work/", "Work", "work")}
      {a("/skills/", "Skills", "skills")}
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
def slug(t): return "".join(c if c.isalnum() else "-" for c in t.lower()).strip("-")
def proj_tile(p):
    meta_top = " · ".join(x for x in (p["fmt"], p["yr"]) if x)
    client = " · ".join(x for x in (p["role"], p["co"]) if x)
    attrs = f'data-group="{E(p["group"])}" data-fmt="{E(p["fmt"])}"'
    if p.get("video"):
        return f'''      <a class="card" id="{slug(p["title"])}" href="{p["url"]}" data-video="{p["video"]}" {attrs}>
        <div class="thumb">{f'<img data-vimeo="{p["url"]}" alt="" hidden>' if p["video"].startswith("vimeo") else ""}<span class="play"></span></div>
        <div class="meta">
          <span class="kicker">{E(p["group"])} · {E(meta_top)}</span>
          <span class="client">{E(client)}</span>
          <h3>{E(p["title"])}</h3>
          <span class="go">Play project reel →</span>
        </div>
      </a>'''
    return f'''      <div class="card" id="{slug(p["title"])}" {attrs}>
        {slate(meta_top, p["title"])}
        <div class="meta">
          <span class="kicker">{E(p["group"])} · {E(meta_top)}</span>
          <span class="client">{E(client)}</span>
          <h3>{E(p["title"])}</h3>
          <span class="go soon">Project reel in production</span>
        </div>
      </div>'''
def chips(kind, values):
    present = {p["group"] if kind == "group" else p["fmt"] for p in PROJECTS}
    return "\n".join(f'      <button type="button" data-k="{kind}" data-v="{E(v)}" aria-pressed="false">{E(v)}</button>' for v in values if v in present)
work = head("Work · Mark Pinheiro", "Mark Pinheiro's showreels and project reels as Nuke compositor and VFX supervisor.") + f'''
<body>

{header("work")}

<main>
  <section class="page">
{page_intro("01", "Work", "Work", "Showreels and project reels from my work as a Nuke compositor and VFX supervisor.")}
    <div class="rail"><span class="n">A</span>Showreels</div>
    <div class="cards">
{chr(10).join(reel_tile(r) for r in REELS)}
    </div>
  </section>

  <section id="projects" style="padding-top:0">
    <div class="rail"><span class="n">B</span>Project reels</div>
    <div class="filters" role="group" aria-label="Filter by role">
      <span class="flabel">Role</span>
      <button type="button" data-k="group" data-v="all" aria-pressed="true">All</button>
{chips("group", ROLE_GROUPS)}
    </div>
    <div class="filters" role="group" aria-label="Filter by format">
      <span class="flabel">Format</span>
      <button type="button" data-k="fmt" data-v="all" aria-pressed="true">All</button>
{chips("fmt", FORMATS)}
    </div>
    <div class="cards" id="tiles">
{chr(10).join(proj_tile(p) for p in PROJECTS)}
    </div>
    <p class="empty" id="empty" hidden>Nothing in this combination yet.</p>
  </section>
</main>

{FOOTER}
<script>
// Two filter rows (role, format) that combine, like Framestore's work filters.
(function(){{
  var sel = {{group:'all', fmt:'all'}}, tiles = document.querySelectorAll('#tiles .card'), empty = document.getElementById('empty');
  document.querySelectorAll('.filters button').forEach(function(b){{
    b.addEventListener('click', function(){{
      var k = b.getAttribute('data-k'); sel[k] = b.getAttribute('data-v');
      document.querySelectorAll('.filters button[data-k="' + k + '"]').forEach(function(x){{ x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }});
      var shown = 0;
      tiles.forEach(function(t){{
        var ok = (sel.group === 'all' || t.getAttribute('data-group') === sel.group) && (sel.fmt === 'all' || t.getAttribute('data-fmt') === sel.fmt);
        t.hidden = !ok; if (ok) shown++;
      }});
      empty.hidden = shown > 0;
    }});
  }});
}})();
</script>
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
HISTORY = [
    ("1992–2004", "Stage & screen", "Staff writer for MTV, NBC Superchannel and UK Play; writer, director and actor; freelance cameraman on CD:UK; theatre with Soapbox Cabaret and Hydrae Theatre Company; idents for MTV, the BBC and the NFTS."),
    ("1995", "First composite", "A VH1 promo, which went on to win a Promax Gold."),
    ("2000–04", "Mocap performer", "Centroid. Regular visual effects work begins."),
    ("2004–10", "Head of 2 Dimensions, Escape Studios", "Wrote the 12-week compositing course, which went on to shape the school's BA (Hons) and MArt in 2D computer animation."),
    ("2006–now", "Creative director, The Sex Pixels", "BBC World Cup titles (2010), Match of the Day 50th anniversary titles, Nickelodeon, London Grammar, M.I.A., Dimitri Vegas &amp; Like Mike."),
    ("2010–12", "Stereo compositor &amp; stereographer", "Pixomondo and ECCG China: stereo on Scorsese's <em>Hugo</em>, and his first feature, <em>Save The 365th Day</em>."),
    ("2015", "Multi-camera array director", "Timeslice Films."),
    ("2016–18", "2D supervisor", "Screen Scene, Lexhag and Absolute Post."),
    ("2021–23", "Lead PostVis artist", "Framestore FPS and Proof: Guardians of the Galaxy Vol. 3, Damsel, The Family Plan."),
    ("2022", "MA, Writing for Script &amp; Screen", "Falmouth University."),
    ("2022–now", "VFX supervisor", "On-set and in-facility: The Ballad of a Small Player, Gangs of London S3 and S4, Panda Plan, I Am Nobody S2, We Hunt Together, Poirot."),
]
AWARDS = [
    ("Promax", "Gold · own win", "VH1 promo, 1996"),
    ("UK MVA", "", "Klaxons, 'Twin Flames', 2011"),
    ("Oscar ×2", "", "Hugo 2012 · Tenet 2021"),
    ("BAFTA ×2", "", "The Crown 2017 · Tenet 2021"),
    ("Emmy ×2", "", "Game of Thrones · Man in an Orange Shirt"),
    ("VES", "", "Hugo, 2012"),
    ("HPA", "", "Black Sails, 2017"),
]
EQUIPMENT = [
    ("Cameras", "iPhone 17 Log · Theta 360 · 15× GoPro · Canon 5D MkII"),
    ("VFX kit", "Grey / chrome ball rig · 2× large silver balls"),
    ("Wrangle", "Assimilate Scratch · Gaussian splatting · CaraVR · Kartaverse"),
    ("Comp", "NukeX · Boris FX Suite"),
    ("Track", "Mocha · SynthEyes"),
    ("3D", "Modo · Mari · Katana · Blender"),
    ("Real-time", "Unreal Engine"),
    ("AI", "Claude · ComfyUI"),
    ("Pipeline", "USD · AYON · Deadline"),
    ("Review", "Nuke Studio · xStudio · RV · Syncsketch"),
    ("Finishing", "DaVinci Resolve Studio"),
]
EDUCATION = [
    ("MA", "Screenwriting", "Falmouth University"),
    ("Fellow", "Virtual Production", "Epic Games"),
    ("PG Dip", "Visual Effects", "NFTS"),
    ("Dip", "Professional Acting", "City Literary Institute"),
    ("A-level", "Film Studies", "Merton College"),
    ("BTEC", "Art &amp; Design", "Chelsea College of Art &amp; Design"),
    ("BTEC", "Business &amp; Finance", "SFX"),
]
LINKS = [("IMDb", "https://www.imdb.com/name/nm1025041/"), ("LinkedIn", "https://www.linkedin.com/in/markpinheiro"),
         ("Vimeo", "https://vimeo.com/thesexpixels"), ("Instagram", INSTAGRAM)]
hist = "\n".join(f'        <li><span class="y">{y}</span><span><b>{w}</b><span>{d}</span></span></li>' for y, w, d in HISTORY)
awd = "\n".join(f'        <li><b>{n}</b>{f"<i>{k}</i>" if k else ""}<span>{E(d)}</span></li>' for n, k, d in AWARDS)
eqp = "\n".join(f'        <div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>' for k, v in EQUIPMENT)
edu = "\n".join(f'        <li><span class="b">{E(b)}</span><span><b>{q}</b> · {w}</span></li>' for b, q, w in EDUCATION)
lnk = " ".join(f'<a class="pill ghost" href="{u}" target="_blank" rel="noopener">{n} ↗</a>' for n, u in LINKS)
about = head("About · Mark Pinheiro",
             "Mark Pinheiro: filmmaker, Nuke compositor and VFX supervisor. History, awards and kit from twenty-six years in visual effects.") + f'''
<body>

{header("about")}

<main>
  <section class="profile">
    <h1>Mark<br>Pinheiro</h1>
    <div class="roles"><span class="a">Filmmaker / VFX / AI</span><span>Nuke compositor &amp; VFX supervisor</span><span>London</span></div>
    <div class="bio">
      <div>
        <p class="lede">A filmmaker at heart, with twenty-six years in visual effects.</p>
        <p>Mark's first composite won a Promax Gold in 1995, and he has worked steadily in VFX since 2000. The 2000s brought the Escape Studios compositing course. The 2010s brought stereo on Scorsese's <em>Hugo</em>, his first feature, <em>Save The 365th Day</em>, and a decade of award-winning shows. The 2020s brought a Masters in screenwriting, and finally accepting the role of department head.</p>
        <p>Today he still enjoys exploring methods and practices that use technology to simplify filmmaking. He is an <strong>agentic coder</strong>: every tool he builds is written with AI. He still designs courses for the NFTS, ECAM Madrid and Escape Studios, and works through his boutique studio, The Sex Pixels.</p>
        <div class="linkrow">{lnk}</div>
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
      </div>
    </div>
  </section>

  <section id="history" style="padding-top:0">
    <div class="rail"><span class="n">01</span>History</div>
    <ol class="timeline">
{hist}
    </ol>
  </section>

  <section id="awards" style="padding-top:0">
    <div class="rail"><span class="n">02</span>Successes</div>
    <ul class="awardgrid">
{awd}
    </ul>
    <div class="awards-note">Promax won outright; the others won by the shows and teams he was part of.</div>
  </section>

  <section id="kit" style="padding-top:0">
    <div class="about2">
      <div>
        <div class="rail"><span class="n">03</span>Software &amp; equipment</div>
        <dl class="kit">
{eqp}
        </dl>
      </div>
      <div>
        <div class="rail"><span class="n">04</span>Education</div>
        <ul class="edu">
{edu}
        </ul>
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
{page_intro("04", "Contact", "Let's talk")}
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
