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
from work_data import PROJECTS, ROLE_GROUPS, FORMATS, FORMAT_SLUGS
from news_data import NEWS

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

def header(current="", sub="VFX Supervisor"):
    def a(href, label, key):
        cur = ' aria-current="page"' if key == current else ""
        return f'<li><a href="{href}"{cur}>{label}</a></li>'
    sub_items = "\n          ".join(f'<li><a href="/work/{FORMAT_SLUGS[f]}/">{" ".join(w.capitalize() for w in f.split())}</a></li>' for f in FORMATS)
    return f'''<header class="nav" id="nav">
  <a class="mark" href="/" aria-label="Mark Pinheiro, {sub}, home"><b>Mark Pinheiro</b><small>{sub}</small></a>
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
  <nav aria-label="Main" id="menu">
    <ul>
      {a("/thefleapit/", "Filmmaker", "fleapit")}
      {a("/nukecompositor/", "Nuke Compositor", "nuke")}
      {a("/vfxsupervisor/", "VFX Supervisor", "vfxsup")}
      <li class="sep" aria-hidden="true"></li>
      <li class="has-sub"><a href="/work/"{' aria-current="page"' if current == "work" else ""}>Work</a>
        <ul class="sub">
          {sub_items}
        </ul>
      </li>
      {a("/skills/", "Skills", "skills")}
      {a("/news/", "News", "news")}
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
            "Mark Pinheiro: filmmaker, Nuke compositor and VFX supervisor.") + f'''
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
      <a class="card" href="/thefleapit/">
        <div class="thumb fleapit-thumb" aria-hidden="true"><span>The Fleapit<b>.</b></span></div>
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
def fmt_title(f): return " ".join(w.capitalize() for w in f.split())
def proj_tile(p):
    meta_top = " · ".join(x for x in (fmt_title(p["fmt"]), p["yr"]) if x)
    client = " · ".join(x for x in (p["role"], p["co"]) if x)
    attrs = f'data-group="{E(p["group"])}"'
    if p.get("video"):
        img = f'<img data-vimeo="{p["url"]}" alt="" hidden>' if p["video"].startswith("vimeo") else ""
        return f'''      <a class="card" id="{slug(p["title"])}" href="{p["url"]}" data-video="{p["video"]}" {attrs}>
        <div class="thumb">{img}<span class="play"></span></div>
        <div class="meta">
          <span class="kicker">{E(p["group"])} · {E(meta_top)}</span>
          <span class="client">{E(client)}</span>
          <h3>{E(p["title"])}</h3>
          <span class="go">Play full screen →</span>
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

FILTER_JS = '''<script>
// Role filter, like the category filters on Framestore's work page.
(function(){
  var tiles = document.querySelectorAll('#tiles .card');
  document.querySelectorAll('.filters button').forEach(function(b){
    b.addEventListener('click', function(){
      var v = b.getAttribute('data-v');
      document.querySelectorAll('.filters button').forEach(function(x){ x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      tiles.forEach(function(t){ t.hidden = !(v === 'all' || t.getAttribute('data-group') === v); });
    });
  });
})();
</script>'''

# Overview: showreels, then one door per format
doors = []
for f in FORMATS:
    n = sum(1 for p in PROJECTS if p["fmt"] == f)
    count = f"{n} project{'s' if n != 1 else ''}" if n else "Coming soon"
    doors.append(f'''      <a class="card" href="/work/{FORMAT_SLUGS[f]}/">
        {slate(count, fmt_title(f))}
        <div class="meta">
          <span class="kicker">Work · {E(count)}</span>
          <h3>{E(fmt_title(f))}</h3>
          <span class="go">View →</span>
        </div>
      </a>''')
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

  <section id="formats" style="padding-top:0">
    <div class="rail"><span class="n">B</span>Project reels by format</div>
    <div class="cards four">
{chr(10).join(doors)}
    </div>
  </section>
</main>

{FOOTER}
</body>
</html>
'''
write("work/index.html", work)

# One page per format
for i, f in enumerate(FORMATS, 1):
    items = [p for p in PROJECTS if p["fmt"] == f]
    groups = [g for g in ROLE_GROUPS if any(p["group"] == g for p in items)]
    chips = ""
    if len(groups) > 1:
        chips = '    <div class="filters" role="group" aria-label="Filter by role">\n      <span class="flabel">Role</span>\n      <button type="button" data-v="all" aria-pressed="true">All</button>\n' + \
            "\n".join(f'      <button type="button" data-v="{E(g)}" aria-pressed="false">{E(g)}</button>' for g in groups) + "\n    </div>\n"
    body = (f'    <div class="cards" id="tiles">\n{chr(10).join(proj_tile(p) for p in items)}\n    </div>' if items
            else '    <p class="pagelede">Feature animation reels are on their way.</p>')
    title = fmt_title(f)
    pg = head(f"{title} · Work · Mark Pinheiro", f"Mark Pinheiro's {f} work: project reels as Nuke compositor and VFX supervisor.") + f'''
<body>

{header("work")}

<main>
  <section class="page">
    <a class="back" href="/work/">&larr; Work</a>
{page_intro(f"01.{i}", "Work", title)}
{chips}{body}
  </section>
</main>

{FOOTER}
{FILTER_JS if chips else ""}
</body>
</html>
'''
    write(f"work/{FORMAT_SLUGS[f]}/index.html", pg)

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

# ---------------------------------------------------------------- player pages (The Fleapit, Nuke Compositor)
# A player on top that plays every reel in the grid one after another; the grid below.
# video: "vimeo:ID:HASH" or "youtube:ID" (advance on their own), or "instagram:REELCODE"
# (Instagram gives no "ended" signal, so the player waits for Next). None = coming soon.
FLEAPIT_REELS = [
    dict(title="Uncommercials", kind="Uncommercial", video=None),
    dict(title="Coming attractions", kind="Trailer", video=None),
    dict(title="Idents & stings", kind="Ident", video=None),
    dict(title="Local-shop ads", kind="Cheap uncommercial", video=None),
    dict(title="The short", kind="Short film", video=None),
    dict(title="Film essays", kind="Film essay", video=None),
]
NUKE_REELS = [
    dict(title="Compositing showreel 2026", kind="Showreel", video=REEL_2026),
    dict(title="Sizzle reel", kind="17 years in 02:30", video="youtube:SDAXjN_sOlE"),
] + [dict(title=p["title"], kind=" · ".join(x for x in (p["role"], p["co"]) if x), video=p.get("video"))
     for p in PROJECTS if p["group"] == "Nuke compositor"]

def reel_cell(i, r):
    if r["video"]:
        img = ""
        if r.get("thumb"): img = f'<img src="{r["thumb"]}" alt="" loading="lazy">'
        elif r["video"].startswith("vimeo:"):
            vid, _, h = r["video"][6:].partition(":"); img = f'<img data-vimeo="https://vimeo.com/{vid}/{h}" alt="" hidden>'
        elif r["video"].startswith("youtube:"): img = f'<img src="https://i.ytimg.com/vi/{r["video"][8:]}/hqdefault.jpg" alt="" loading="lazy">'
        return f'''      <button class="fp-cell" type="button" data-i="{i}" data-src="{r["video"]}" data-title="{E(r["title"])}">{img}<span class="fp-cap"><b>{E(r["title"])}</b><i>{E(r["kind"])}</i></span><span class="play"></span></button>'''
    return f'''      <div class="fp-cell fp-soon"><span class="fp-cap"><b>{E(r["title"])}</b><i>{E(r["kind"])} · coming soon</i></span></div>'''

def player_page(path, key, sub, title_html, rail_n, rail_label, lede, reels, wide, idle_empty, extra_links, page_title, desc):
    cells = "\n".join(reel_cell(i, r) for i, r in enumerate(reels))
    has_any = any(r["video"] for r in reels)
    idle_btn = '<button class="pill" type="button" id="fp-start"><i></i>Play all</button>' if has_any else extra_links
    pg = head(page_title, desc) + f'''
<body>

{header(key, sub)}

<main>
  <section class="page fp-head">
    <div class="rail"><span class="n">{rail_n}</span>{rail_label}</div>
    <h1 class="pagetitle">{title_html}</h1>
    <p class="pagelede">{lede}</p>
  </section>

  <section class="fp-stage" aria-label="Player">
    <div class="fp-player{"" if has_any else " fp-empty"}" id="fp-player">
      <div class="fp-slot" id="fp-slot"></div>
      <div class="fp-idle"><span class="fp-now">Now showing</span><span class="fp-big">{"Press play" if has_any else idle_empty}</span>{idle_btn}</div>
    </div>
    <div class="fp-bar"{"" if has_any else " hidden"}>
      <button type="button" class="fp-btn" id="fp-prev" aria-label="Previous reel">◀</button>
      <span class="fp-title" id="fp-title" aria-live="polite"></span>
      <button type="button" class="fp-btn" id="fp-next" aria-label="Next reel">▶</button>
      <button type="button" class="fp-btn" id="fp-full">Full screen</button>
    </div>
  </section>

  <section class="fp-reels" aria-labelledby="reels-h">
    <div class="rail"><span class="n">Reels</span><span id="reels-h">All</span></div>
    <div class="fp-grid{" wide" if wide else ""}">
{cells}
    </div>
  </section>
</main>

{FOOTER}
<script src="/assets/playlist.js"></script>
</body>
</html>
'''
    write(path, pg)

player_page("thefleapit/index.html", "fleapit", "The Sex Pixels", 'The Fleapit<span class="dot">.</span>', "SE1", "Filmmaker",
            "Filmmaking experiments: uncommercials, fake trailers, idents and film essays. Shot on iPhone, finished with VFX and AI.",
            FLEAPIT_REELS, False, "The first reel is in the edit",
            f'<a class="pill" href="{INSTAGRAM}" target="_blank" rel="noopener">Follow on Instagram ↗</a>',
            "The Fleapit · Mark Pinheiro",
            "The Fleapit. SE1: Mark Pinheiro's filmmaking experiments. Uncommercials, fake trailers, idents and film essays.")
player_page("nukecompositor/index.html", "nuke", "Nuke Compositor", 'Nuke Compositor', "2D", "Showreels",
            "Compositing showreels and project reels. Play them all, or pick one from the grid.",
            NUKE_REELS, True, "", "", "Nuke Compositor · Mark Pinheiro",
            "Mark Pinheiro's compositing showreels and project reels.")

# Old address: send /fleapit/ visitors to /thefleapit/
write("fleapit/index.html", '''<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><title>The Fleapit · Mark Pinheiro</title>
<link rel="canonical" href="/thefleapit/"><meta http-equiv="refresh" content="0; url=/thefleapit/">
<style>body{background:#111012;color:#eeeae4;font-family:Arial,sans-serif;padding:40px}</style></head>
<body><p>The Fleapit has moved to <a href="/thefleapit/" style="color:#e98aa9">thesexpixels.com/thefleapit</a>.</p></body></html>
''')

# ---------------------------------------------------------------- vfx supervisor (player + grid; showreel first)
SUP_REELS = [dict(title="VFX supervisor showreel", kind="Showreel", video=next((r["video"] for r in REELS if r["role"] == "VFX supervisor"), None))] + \
    [dict(title=p["title"], kind=" · ".join(x for x in (p["role"], p["co"]) if x), video=p.get("video"))
     for p in PROJECTS if p["group"] == "VFX supervisor"]
player_page("vfxsupervisor/index.html", "vfxsup", "VFX Supervisor", "VFX Supervisor", "SUP", "Showreels",
            "On-set and in-facility supervision across feature film, episodic and commercials. The showreel plays first; pick a project from the grid to play its reel.",
            SUP_REELS, True, "The supervisor showreel is in the edit", "", "VFX Supervisor · Mark Pinheiro",
            "Mark Pinheiro's VFX supervision: showreel and project reels.")

# ---------------------------------------------------------------- news
import datetime
def nice_date(d): return datetime.date.fromisoformat(d).strftime("%-d %B %Y")
news_cards = "\n".join(f'''      <a class="card" href="/news/{n["slug"]}/">
        {slate(nice_date(n["date"]), "News")}
        <div class="meta">
          <span class="kicker">{nice_date(n["date"])}</span>
          <h3>{n["title"]}</h3>
          <p>{n["body"][0]}</p>
          <span class="go">Read →</span>
        </div>
      </a>''' for n in NEWS)
news = head("News · Mark Pinheiro", "News and updates from Mark Pinheiro.") + f'''
<body>

{header("news")}

<main>
  <section class="page">
{page_intro("03", "News", "News", "Updates: new reels, demos, jobs and experiments.")}
    <div class="cards">
{news_cards}
    </div>
  </section>
</main>

{FOOTER}
</body>
</html>
'''
write("news/index.html", news)
for n in NEWS:
    body = "\n".join(f"      <p>{para}</p>" for para in n["body"])
    write(f"news/{n['slug']}/index.html", head(f"{n['title']} · News · Mark Pinheiro", n["body"][0]) + f'''
<body>

{header("news")}

<main>
  <article class="page post">
    <a class="back" href="/news/">&larr; News</a>
    <div class="rail"><span class="n">{nice_date(n["date"])}</span>News</div>
    <h1 class="pagetitle">{n["title"]}</h1>
    <div class="postbody">
{body}
    </div>
  </article>
</main>

{FOOTER}
</body>
</html>
''')

# ---------------------------------------------------------------- contact
CONTACT_LINKS = [
    ("Showreel", "Compositing showreel 2026", "https://vimeo.com/1232958213/ffbea294d7"),
    ("Sizzle", "17 years in 02:30", "https://youtu.be/SDAXjN_sOlE"),
    ("Vimeo", "vimeo.com/thesexpixels", "https://vimeo.com/thesexpixels"),
    ("Instagram", "@t_h_e__p_i_x_x_x_e_l_s", INSTAGRAM),
    ("IMDb", "nm1025041", "https://www.imdb.com/name/nm1025041/"),
    ("LinkedIn", "in/markpinheiro", "https://www.linkedin.com/in/markpinheiro"),
]
clinks = "\n".join(f'        <li><span class="k">{k}</span><a href="{u}" target="_blank" rel="noopener">{E(t)} ↗</a></li>' for k, t, u in CONTACT_LINKS)
contact = head("Contact · Mark Pinheiro", "Contact Mark Pinheiro: email, showreels, Vimeo, Instagram, IMDb and LinkedIn.") + f'''
<body>

{header("contact")}

<main>
  <section class="page contactpage">
{page_intro("04", "Contact", "Let's talk")}
    <div class="ctop">
      <div>
        <span class="clabel">Email</span>
        <a class="email" href="mailto:mark@thesexpixels.com">mark@thesexpixels.com</a>
      </div>
      <div>
        <span class="clabel">Based</span>
        <p class="cbig">London</p>
        <p class="csmall">UK work eligibility · valid passport · available to travel worldwide</p>
      </div>
      <div>
        <span class="clabel">Company</span>
        <address>
          <b>The Sex Pixels Ltd.</b>
          Fifth Floor, Mariner House<br>
          62 Prince Street, Bristol BS1 4QD<br>
          <a href="mailto:info@thesexpixels.com">info@thesexpixels.com</a>
        </address>
      </div>
    </div>
    <ul class="ctiles">
{chr(10).join(f'      <li><a href="{u}" target="_blank" rel="noopener"><span class="k">{k}</span><span class="t">{E(t)}</span><span class="arr">↗</span></a></li>' for k, t, u in CONTACT_LINKS)}
    </ul>
  </section>
</main>

{FOOTER}
</body>
</html>
'''
write("contact/index.html", contact)
print("built: index, work, skills, thefleapit, nukecompositor, vfxsupervisor, news, about, contact")
