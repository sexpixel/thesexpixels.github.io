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
from work_data import PROJECTS, ROLE_GROUPS, FORMATS, FORMAT_SLUGS, expand
from news_data import NEWS
from crops import CROPS, crop_of, crop_str

def crop_attr(spec):
    c = crop_str(spec)
    return f' data-crop="{c}"' if c else ""


E = html.escape

# Cache-busting: the stylesheet and scripts are linked with a short fingerprint of their contents
# (site.css?v=1a2b3c4d), so browsers fetch the new file as soon as it changes instead of using an old copy.
import hashlib
def _ver(rel):
    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), rel), "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()[:8]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- reels
# Add a reel by filling in its video: "vimeo:ID:HASH" or "youtube:ID". None = coming soon.
REEL_2026 = "vimeo:1232958213:ffbea294d7"
REELS = [
    dict(id="reel-compositor", role="Nuke compositor", title="Compositing showreel", note="Showreel · 2026",
         line="The latest compositing reel.", video=REEL_2026, url="https://vimeo.com/1232958213/ffbea294d7"),
    dict(id="reel-vfx-supervisor", role="VFX supervisor", title="VFX supervisor showreel", note="Stand-in",
         line="On-set and post supervision across film, episodic and commercials.", video="youtube:9KZPd8__8ys", url="https://youtu.be/9KZPd8__8ys",
         thumb="https://i.ytimg.com/vi/9KZPd8__8ys/hqdefault.jpg"),  # STAND-IN until the supervisor reel exists
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
{extra}<link rel="stylesheet" href="/assets/site.css?v={_ver("assets/site.css")}">
</head>'''

def header(current="", sub="VFX Supervisor"):
    def a(href, label, key):
        cur = ' aria-current="page"' if key == current else ""
        return f'<li><a href="{href}"{cur}>{label}</a></li>'
    sub_items = "\n          ".join(f'<li><a href="/work/{FORMAT_SLUGS[f]}/">{" ".join(w.capitalize() for w in f.split())}</a></li>' for f in FORMATS)
    return f'''<header class="nav" id="nav">
  <a class="mark" href="/" aria-label="Mark Pinheiro{", " + sub if sub else ""}, home"><b>Mark Pinheiro</b>{f"<small>{sub}</small>" if sub else ""}</a>
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

<script src="/assets/site.js?v=''' + _ver('assets/site.js') + '''"></script>'''

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
ANNIV = next(n for n in NEWS if n["slug"] == "the-sex-pixels-at-20")  # the 20th anniversary story
# Homepage "Latest": always the newest news post.
import datetime
def nice_date(d): return datetime.date.fromisoformat(d).strftime("%-d %B %Y")
LATEST_NEWS = max(NEWS, key=lambda n: n["date"])  # first listed wins a tie
LATEST_THUMB = ('<div class="thumb anniv-thumb" aria-hidden="true"><span>20</span><i>2006–2026</i></div>'
                if LATEST_NEWS is ANNIV else slate(nice_date(LATEST_NEWS["date"]), "News"))
home = head("Mark Pinheiro · Filmmaker / VFX / AI",
            "Mark Pinheiro: filmmaker, Nuke compositor and VFX supervisor. The Sex Pixels, 20 years: 2006–2026.") + f'''
<body>

{header()}

<main id="top">
  <section class="hero stickyhero" aria-label="Showreel"{crop_attr(REEL_2026)}>
    <iframe
      src="https://player.vimeo.com/video/1232958213?h=ffbea294d7&amp;background=1&amp;texttrack=false&amp;autoplay=1&amp;muted=1&amp;loop=1&amp;autopause=0&amp;controls=0&amp;title=0&amp;byline=0&amp;portrait=0&amp;dnt=1"
      title="Mark Pinheiro compositing showreel 2026, playing muted in the background"
      allow="autoplay; fullscreen; picture-in-picture; encrypted-media"
      referrerpolicy="strict-origin-when-cross-origin"
      tabindex="-1"></iframe>
    <div class="reelbar heroui">
      <a class="anniv" href="/news/{ANNIV["slug"]}/">
        <span class="anniv-n">20</span>
        <span class="anniv-t"><b>Years</b><span>The Sex Pixels · servicing clients since 2006</span><em>BBC World Cup · Match of the Day · Nickelodeon · London Grammar · M.I.A. · Gangs of London</em><i>Read the story →</i></span>
      </a>
      <div class="reelside">
        <span class="lab"><b>Compositing showreel</b> · 2026</span>
        <a class="pill" href="https://vimeo.com/1232958213/ffbea294d7" data-video="{REEL_2026}"><i></i>Watch full screen</a>
      </div>
    </div>
    <div class="scrollcue heroui" aria-hidden="true">Scroll</div>
  </section>

  <div class="over">
  <section aria-labelledby="latest-h">
    <div class="rail"><span class="n">01</span><span id="latest-h">Latest</span><a class="rail-link" href="/news/">All news →</a></div>
    <div class="cards">
      <a class="card" href="/news/{LATEST_NEWS["slug"]}/">
        {LATEST_THUMB}
        <div class="meta">
          <span class="kicker">News · {nice_date(LATEST_NEWS["date"])}</span>
          <h3>{LATEST_NEWS["title"]}</h3>
          <p>{LATEST_NEWS.get("summary") or LATEST_NEWS["body"][0]}</p>
          <span class="go">Read →</span>
        </div>
      </a>
      <a class="card" href="/nukecompositor/">
        <div class="thumb"><img data-vimeo="https://vimeo.com/1232958213/ffbea294d7" alt="" hidden><span class="play"></span></div>
        <div class="meta">
          <span class="kicker">Nuke compositor</span>
          <h3>Compositing showreel</h3>
          <p>The 2026 compositing reel, plus project reels.</p>
          <span class="go">Watch →</span>
        </div>
      </a>
      <a class="card" href="/vfxsupervisor/">
        <div class="thumb"><img src="https://i.ytimg.com/vi/9KZPd8__8ys/hqdefault.jpg" alt="" loading="lazy"><span class="play"></span></div>
        <div class="meta">
          <span class="kicker">VFX supervisor</span>
          <h3>Supervisor showreel</h3>
          <p>On-set and in-facility supervision, plus project reels.</p>
          <span class="go">Watch →</span>
        </div>
      </a>
      <a class="card" href="/thefleapit/">
        <div class="thumb"><img data-vimeo="https://vimeo.com/389670596" alt="" hidden><span class="play"></span></div>
        <div class="meta">
          <span class="kicker">Filmmaker</span>
          <h3>The Fleapit</h3>
          <p>A word from our advertisers.</p>
          <span class="go">Watch →</span>
        </div>
      </a>
    </div>
  </section>

  <section aria-labelledby="explore-h" style="padding-top:0">
    <div class="rail"><span class="n">02</span><span id="explore-h">Explore</span></div>
    <div class="cards">
      <a class="card" href="/work/">
        {slate("Feature film · Episodic · Commercial", "Work")}
        <div class="meta">
          <span class="kicker">Work</span>
          <h3>Project reels by format</h3>
          <span class="go">Work →</span>
        </div>
      </a>
      <a class="card" href="/skills/">
        <div class="thumb" aria-hidden="true">{TREE}</div>
        <div class="meta">
          <span class="kicker">Skills · R&amp;D</span>
          <h3>21 disciplines, 7 stages</h3>
          <span class="go">Skills →</span>
        </div>
      </a>
      <a class="card" href="/about/">
        {slate("Since 1995", "About")}
        <div class="meta">
          <span class="kicker">About</span>
          <h3>Kit, press &amp; laurels</h3>
          <span class="go">About →</span>
        </div>
      </a>
    </div>
  </section>
  </div>
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
        img = (f'<img data-vimeo="{p["url"]}" alt="" hidden>' if p["video"].startswith("vimeo") else
               f'<img src="https://i.ytimg.com/vi/{p["video"][8:]}/hqdefault.jpg" alt="" loading="lazy">' if p["video"].startswith("youtube:") else "")
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

# One page per format. Formats in PLAYER_FORMATS get the full-screen player layout (built further down,
# after player_page); the rest keep this list layout.
PLAYER_FORMATS = ["Feature film", "Episodic", "Commercial", "Feature animation"]
for i, f in enumerate(FORMATS, 1):
    if f in PLAYER_FORMATS: continue
    items = [q for p in PROJECTS if p["fmt"] == f for q in expand(p)]
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
# The commentated showreels: Mark narrates each stage of his career (Vimeo showcase 3003648).
DOC_CHAPTERS = [
    ("2000–2004", "103943083"), ("2004–2006", "103945879"), ("2006–2008", "103949083"), ("2007–2010", "103933560"),
    ("2008–2010", "103953638"), ("2010–2012", "103959201"), ("2012–2013", "103979619"), ("2013–2014", "103982611"),
]
doc_cells = "\n".join(
    f'      <button type="button" class="doc-ch" data-i="{i}" data-id="{vid}" data-title="{yrs}">'
    f'<img data-vimeo="https://vimeo.com/{vid}" alt="" hidden><span class="doc-n">{i + 1:02d}</span><b>{yrs}</b></button>'
    for i, (yrs, vid) in enumerate(DOC_CHAPTERS))
LINKS = [("IMDb", "https://www.imdb.com/name/nm1025041/"), ("LinkedIn", "https://www.linkedin.com/in/markpinheiro"),
         ("Vimeo", "https://vimeo.com/thesexpixels"), ("Instagram", INSTAGRAM)]
LAUREL_BRANCH = open(os.path.join(os.path.dirname(__file__), "laurel_branch.svg.txt")).read()
def laurel(n, k, d):
    return (f'        <li class="laurel"><svg class="lb" aria-hidden="true"><use href="#laurel"/></svg>'
            f'<div class="lt"><b>{n}</b>{f"<i>{k}</i>" if k else ""}<span>{E(d)}</span></div>'
            f'<svg class="lb r" aria-hidden="true"><use href="#laurel"/></svg></li>')
lau = "\n".join(laurel(n, k, d) for n, k, d in AWARDS)
awd = "\n".join(f'        <li><b>{n}</b>{f"<i>{k}</i>" if k else ""}<span>{E(d)}</span></li>' for n, k, d in AWARDS)
eqp = "\n".join(f'        <div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>' for k, v in EQUIPMENT)
edu = "\n".join(f'        <li><span class="b">{E(b)}</span><span><b>{q}</b> · {w}</span></li>' for b, q, w in EDUCATION)
lnk = " ".join(f'<a class="pill ghost" href="{u}" target="_blank" rel="noopener">{n} ↗</a>' for n, u in LINKS)
about = head("About · Mark Pinheiro",
             "Mark Pinheiro: filmmaker, Nuke compositor and VFX supervisor. Laurels, software, equipment and press from twenty-six years in visual effects.") + f'''
<body>

{header("about")}

<main>
  <section class="profile">
    <h1>Mark<br>Pinheiro</h1>
    <div class="roles"><span class="a">Filmmaker / VFX / AI</span><span>Nuke compositor &amp; VFX supervisor</span><span class="loc">London</span></div>
    <svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><symbol id="laurel" viewBox="0 0 40 124">{LAUREL_BRANCH}</symbol></defs></svg>
    <ul class="laurels" aria-label="Laurels">
{lau}
    </ul>
    <p class="awards-note">Promax won outright; the others won by the shows and teams he was part of.</p>
    <div class="bio solo">
      <p class="lede">A filmmaker at heart, with twenty-six years in visual effects.</p>
      <p>Today he still enjoys exploring methods and practices that use technology to simplify filmmaking. He is an <strong>agentic coder</strong>: every tool he builds is written with AI. He designs courses for the NFTS, ECAM Madrid and Escape Studios, and works through his boutique studio, The Sex Pixels.</p>
      <div class="linkrow">{lnk}</div>
    </div>
  </section>

  <section id="story" style="padding-top:0">
    <div class="rail"><span class="n">01</span>In his own words · 2000–2014</div>
    <p class="pagelede">Eight showreels, each narrated by Mark: the stages of a career in VFX, told as a short documentary. Press play and it runs chapter by chapter.</p>
    <div class="doc-stage" id="doc-stage">
      <img class="doc-poster" data-vimeo="https://vimeo.com/{DOC_CHAPTERS[0][1]}" alt="" hidden>
      <button type="button" class="doc-start" id="doc-start"><span class="play"></span><span><b>Play the documentary</b><i>8 chapters · with sound</i></span></button>
    </div>
    <div class="doc-now" id="doc-now" aria-live="polite"></div>
    <div class="doc-chs">
{doc_cells}
    </div>
  </section>

  <section id="kit" style="padding-top:0">
    <div class="rail"><span class="n">02</span>Software &amp; equipment</div>
    <dl class="kit big">
{eqp}
    </dl>
  </section>

  <section id="press" style="padding-top:0">
    <div class="rail"><span class="n">03</span>Press</div>
    <div class="press">
      <figure class="quote">
        <blockquote>“Mark has an undeniably impressive portfolio and his understanding of the industry as a whole makes him a total catch.”</blockquote>
        <figcaption>David Smith, CEO, Absolute · <a href="https://www.televisual.com/news/mark-pinheiro-joins-absolute-as-vfx-super/">Televisual, 2022</a></figcaption>
      </figure>
      <figure class="quote">
        <blockquote>“…he trained a large portion of London’s VFX community.”</blockquote>
        <figcaption><a href="https://www.televisual.com/news/mark-pinheiro-joins-absolute-as-vfx-super/">Televisual, 2022</a> · on Escape Studios</figcaption>
      </figure>
    </div>
  </section>

  <section id="education" style="padding-top:0">
    <div class="rail"><span class="n">04</span>Education</div>
    <ul class="edu">
{edu}
    </ul>
  </section>
</main>

{FOOTER}
</body>
</html>
'''
about = about.replace("</body>", f'<script src="/assets/doc.js?v={_ver("assets/doc.js")}"></script>\n</body>', 1)
write("about/index.html", about)

# ---------------------------------------------------------------- player pages (The Fleapit, Nuke Compositor)
# A player on top that plays every reel in the grid one after another; the grid below.
# video: "vimeo:ID:HASH" or "youtube:ID" (advance on their own), or "instagram:REELCODE"
# (Instagram gives no "ended" signal, so the player waits for Next). None = coming soon.
REEL_2020 = "vimeo:389670596"
FLEAPIT_REELS = [
    dict(title="Showreel 2020", kind="Tonight's programme", video=REEL_2020),  # STAND-IN until the first Fleapit reel is ready
    dict(title="A word from our advertisers", kind="Advertisement", video=None),
    dict(title="Coming attractions", kind="Trailer", video=None),
    dict(title="Intermission", kind="Sting", video=None),
    dict(title="Local advertisers", kind="Advertisement", video=None),
    dict(title="Supporting feature", kind="Short film", video=None),
    dict(title="Programme notes", kind="Notes", video=None),
]
NUKE_REELS = [
    dict(title="Compositing showreel 2026", kind="Showreel", video=REEL_2026),
    dict(title="Showreel 2020", kind="Showreel", video=REEL_2020),
    dict(title="Sizzle reel", kind="17 years in 02:30", video="youtube:SDAXjN_sOlE"),
    # From Mark, 12 Oct. TITLE TO CONFIRM (1014143091, once 'Compositing reel 2', is Moon Knight: The Realm).
    dict(title="Compositing reel 1", kind="Project reel", video="vimeo:1014139706"),
] + [dict(title=q["title"], kind=" · ".join(x for x in (q["role"], q["co"]) if x), video=q.get("video"))
     for p in PROJECTS if p["group"] in ("Nuke compositor", "PostVis") for q in expand(p)]

def reel_cell(i, r):
    if r["video"]:
        img = ""
        if r.get("thumb"): img = f'<img src="{r["thumb"]}" alt="" loading="lazy">'
        elif r["video"].startswith("vimeo:"):
            vid, _, h = r["video"][6:].partition(":"); img = f'<img data-vimeo="https://vimeo.com/{vid}{"/" + h if h else ""}" alt="" hidden>'
        elif r["video"].startswith("youtube:"): img = f'<img src="https://i.ytimg.com/vi/{r["video"][8:]}/hqdefault.jpg" alt="" loading="lazy">'
        return f'''      <button class="fp-cell" type="button" data-i="{i}" data-src="{r["video"]}" data-title="{E(r["title"])}"{crop_attr(r["video"])}>{img}<span class="fp-cap"><b>{E(r["title"])}</b><i>{E(r["kind"])}</i></span><span class="play"></span></button>'''
    return f'''      <div class="fp-cell fp-soon"><span class="fp-cap"><b>{E(r["title"])}</b><i>{E(r["kind"])} · coming soon</i></span></div>'''

def player_page(path, key, sub, title_html, rail_n, rail_label, lede, reels, wide, idle_empty, extra_links, page_title, desc):
    cells = "\n".join(reel_cell(i, r) for i, r in enumerate(reels))
    has_any = any(r["video"] for r in reels)
    idle = "" if has_any else f'''
    <div class="fp-idle"><span class="fp-now">Now showing</span><span class="fp-big">{idle_empty}</span>{extra_links}</div>'''
    ctrls = f'''
        <div class="fp-ctrls">
          <button type="button" class="fp-btn" id="fp-prev" aria-label="Previous reel">◀</button>
          <button type="button" class="fp-btn" id="fp-next" aria-label="Next reel">▶</button>
          <button type="button" class="fp-btn" id="fp-sound" aria-pressed="false">Sound on</button>
          <button type="button" class="fp-btn" id="fp-full">Full screen</button>
        </div>''' if has_any else ""
    pg = head(page_title, desc) + f'''
<body>

{header(key, None)}

<main>
  <section class="hero stickyhero fp-player{"" if has_any else " fp-empty"}" id="fp-player" aria-label="Player">
    <div class="fp-slot" id="fp-slot"></div>{idle}
    <div class="herotitle herotop heroui">
      <span class="lab"><b>{rail_n}</b> · {rail_label}</span>
      <h1 class="herohead">{title_html}</h1>
    </div>
    <div class="reelbar heroui">
      <span class="fp-title" id="fp-title" aria-live="polite"></span>{ctrls}
    </div>
    <div class="scrollcue heroui" aria-hidden="true">Scroll for reels</div>
  </section>

  <div class="over">
  <section class="fp-reels" aria-labelledby="reels-h">
    <div class="rail"><span class="n">Reels</span><span id="reels-h">All</span></div>
    <p class="pagelede">{lede}</p>
    <div class="fp-grid{" wide" if wide else ""}">
{cells}
    </div>
  </section>
  </div>
</main>

{FOOTER}
<script src="/assets/playlist.js?v={_ver("assets/playlist.js")}"></script>
</body>
</html>
'''
    write(path, pg)

player_page("thefleapit/index.html", "fleapit", "The Sex Pixels", 'The Fleapit<span class="dot">.</span>', "SE1", "Filmmaker",
            "A word from our advertisers.",
            FLEAPIT_REELS, False, "The first reel is in the edit",
            f'<a class="pill" href="{INSTAGRAM}" target="_blank" rel="noopener">Follow on Instagram ↗</a>',
            "The Fleapit · Mark Pinheiro",
            "The Fleapit. SE1. A word from our advertisers.")
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
SUP_REELS = [dict(title="VFX supervisor showreel", kind="Stand-in", video=next((r["video"] for r in REELS if r["role"] == "VFX supervisor"), None))] + \
    [dict(title=q["title"], kind=" · ".join(x for x in (q["role"], q["co"]) if x), video=q.get("video"))
     for p in PROJECTS if p["group"] == "VFX supervisor" for q in expand(p)]
player_page("vfxsupervisor/index.html", "vfxsup", "VFX Supervisor", "VFX Supervisor", "SUP", "Showreels",
            "On-set and in-facility supervision across feature film, episodic and commercials. The showreel plays first; pick a project from the grid to play its reel.",
            SUP_REELS, True, "The supervisor showreel is in the edit", "", "VFX Supervisor · Mark Pinheiro",
            "Mark Pinheiro's VFX supervision: showreel and project reels.")

# ---------------------------------------------------------------- work format pages with the player
FORMAT_LEDES = {
    "Feature film": "Feature film project reels: Nuke compositing, PostVis and VFX supervision. Play them all, or pick one from the grid.",
    "Episodic": "Episodic project reels: Nuke compositing, PostVis and VFX supervision. Play them all, or pick one from the grid.",
    "Commercial": "Commercial project reels: on-set supervision and compositing. Play them all, or pick one from the grid.",
    "Feature animation": "Feature animation project reels. Play them all, or pick one from the grid.",
}
for i, f in enumerate(FORMATS, 1):
    if f not in PLAYER_FORMATS: continue
    items = [q for p in PROJECTS if p["fmt"] == f for q in expand(p)]
    reels = [dict(title=q["title"], kind=" · ".join(x for x in (q["role"], q["co"], q["yr"]) if x), video=q.get("video"))
             for q in items]
    reels = [r for r in reels if r["video"]] + [r for r in reels if not r["video"]]
    title = fmt_title(f)
    player_page(f"work/{FORMAT_SLUGS[f]}/index.html", "work", None, title, f"01.{i}", "Work",
                FORMAT_LEDES[f], reels, True, "Reels on their way", "",
                f"{title} · Work · Mark Pinheiro", f"Mark Pinheiro's {f} work: project reels as Nuke compositor and VFX supervisor.")

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
# Simple line icons for the contact page (original drawings, not the brands' own logos).
ICONS = {
    "Showreel": '<circle cx="12" cy="12" r="9.5"/><path d="M10 8.2v7.6l6-3.8z" fill="currentColor"/>',
    "Sizzle": '<path d="M13.5 2.5 5 13.5h6l-1.5 8 8.5-11h-6z"/>',
    "Vimeo": '<rect x="2.5" y="5" width="19" height="14" rx="3"/><path d="M10 9.2v5.6l4.6-2.8z" fill="currentColor"/>',
    "Instagram": '<path d="M3 8.5a2 2 0 0 1 2-2h2.6l1.6-2.2h5.6l1.6 2.2H19a2 2 0 0 1 2 2V18a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><circle cx="12" cy="13" r="3.8"/>',
    "IMDb": '<path d="M3.5 10h17v9.5a1 1 0 0 1-1 1h-15a1 1 0 0 1-1-1z"/><path d="m3.2 9.6 15.9-4.8-.9-3.1L2.3 6.5z"/><path d="m7.4 4.9 2.6 3.3M12.4 3.4 15 6.7"/>',
    "LinkedIn": '<rect x="2.5" y="7" width="19" height="13" rx="2"/><path d="M8.5 7V5a1.5 1.5 0 0 1 1.5-1.5h4A1.5 1.5 0 0 1 15.5 5v2M2.5 12.5h19"/>',
    "Email": '<rect x="2.5" y="5" width="19" height="14" rx="2"/><path d="m3 6 9 7 9-7"/>',
    "Based": '<path d="M12 21s-6.5-6.2-6.5-11.2a6.5 6.5 0 0 1 13 0C18.5 14.8 12 21 12 21z"/><circle cx="12" cy="9.8" r="2.4"/>',
    "Company": '<path d="M4 21V5.5L12 3v18M12 8.5l8 2.5V21M2.5 21h19M7 8h2M7 11.5h2M7 15h2M15 13.5h2M15 17h2"/>',
}
def icon(name, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'
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
{page_intro("04", "Contact", "Contact")}
    <div class="ctop">
      <div>
        <span class="clabel">{icon("Email", "ic big")}Email</span>
        <a class="email" href="mailto:mark@thesexpixels.com">mark@thesexpixels.com</a>
      </div>
      <div>
        <span class="clabel">{icon("Based", "ic big")}Based</span>
        <p class="cbig">London</p>
        <p class="csmall">UK work eligibility · valid passport · available to travel worldwide</p>
      </div>
      <div>
        <span class="clabel">{icon("Company", "ic big")}Company</span>
        <b class="coname">The Sex Pixels Ltd.</b>
        <div class="offices">
          <address><span class="olabel">Studio</span>
            Old Bank Chambers, The Slip<br>
            217 Grange Road, Bermondsey<br>
            London SE1 3AA
          </address>
          <address><span class="olabel">Registered office</span>
            Fifth Floor, Mariner House<br>
            62 Prince Street<br>
            Bristol BS1 4QD
          </address>
        </div>
        <a class="coemail" href="mailto:info@thesexpixels.com">info@thesexpixels.com</a>
      </div>
    </div>
    <ul class="ctiles">
{chr(10).join(f'      <li><a href="{u}" target="_blank" rel="noopener">{icon(k)}<span class="k">{k}</span><span class="t">{E(t)}</span><span class="arr">↗</span></a></li>' for k, t, u in CONTACT_LINKS)}
    </ul>
  </section>
</main>

{FOOTER}
</body>
</html>
'''
write("contact/index.html", contact)
# ---------------------------------------------------------------- tuner (private, not linked)
# Mark plays each reel behind a sample page heading and sets its crop; the page writes out
# the settings for _build/crops.py.
import json
_seen, TUNE = set(), []
# The reels that need cropping come first: The Fleapit's Showreel 2020, then the VFX supervisor showreel.
for page_name, reels in (("The Fleapit.", FLEAPIT_REELS), ("VFX Supervisor", SUP_REELS[:1]),
                         ("Home", [dict(title="Compositing showreel 2026", video=REEL_2026)]),
                         ("Nuke Compositor", NUKE_REELS), ("VFX Supervisor", SUP_REELS)):
    for r in reels:
        v = r.get("video")
        if not v or v in _seen or v.startswith("instagram:"): continue
        _seen.add(v); c = crop_of(v) or {}
        TUNE.append(dict(title=r["title"], spec=v, page=page_name, top=c.get("top", 0), bottom=c.get("bottom", 0),
                         left=c.get("left", 0), right=c.get("right", 0), fill=c.get("fill", False)))
tuner = head("Reel crop tuner · Mark Pinheiro", "Private: set the crop for each reel.", '<meta name="robots" content="noindex">\n') + f"""
<body class="tuner">

{header()}

<main>
  <section class="hero fp-player" id="fp-player" aria-label="Reel being tuned">
    <div class="fp-slot" id="fp-slot"></div>
    <div class="herotitle herotop heroui">
      <span class="lab"><b>Sample</b> · page heading</span>
      <h1 class="herohead" id="t-head">Nuke Compositor</h1>
    </div>
    <div class="reelbar heroui"><span class="fp-title" id="t-now"></span></div>
  </section>
</main>

<aside class="tunepanel" id="t-panel" aria-label="Crop controls">
  <div class="tp-row"><button type="button" class="fp-btn" id="t-prev" aria-label="Previous reel">◀</button>
    <select id="t-pick" aria-label="Reel"></select>
    <button type="button" class="fp-btn" id="t-next" aria-label="Next reel">▶</button></div>
  <div class="tp-crop">
    <label>Crop top <output id="v-top"></output><input type="range" id="c-top" min="0" max="35" step="0.1"></label>
    <label>Crop bottom <output id="v-bottom"></output><input type="range" id="c-bottom" min="0" max="35" step="0.1"></label>
    <label>Crop left <output id="v-left"></output><input type="range" id="c-left" min="0" max="35" step="0.1"></label>
    <label>Crop right <output id="v-right"></output><input type="range" id="c-right" min="0" max="35" step="0.1"></label>
  </div>
  <label class="tp-check"><input type="checkbox" id="c-link"> Link top &amp; bottom</label>
  <label class="tp-check"><input type="checkbox" id="c-fill"> Fill screen (zooms the cropped picture up; off = crop only)</label>
  <div class="tp-row"><button type="button" class="fp-btn" id="t-reset">Reset this reel</button>
    <button type="button" class="fp-btn" id="t-guides" aria-pressed="true">Headings on</button>
    <button type="button" class="fp-btn" id="t-hide">Hide panel (H)</button></div>
  <label>Settings to send Mark's Claude <textarea id="t-out" rows="6" readonly></textarea></label>
  <button type="button" class="pill" id="t-copy">Copy settings</button>
</aside>
<button type="button" class="fp-btn tp-show" id="t-show" hidden>Show panel (H)</button>

<script>
var TUNE = {json.dumps(TUNE)};
</script>
<script src="/assets/site.js?v={_ver('assets/site.js')}"></script>
<script src="/assets/tuner.js?v={_ver('assets/tuner.js')}"></script>
</body>
</html>
"""
write("tuner/index.html", tuner)

print("built: index, work, skills, thefleapit, nukecompositor, vfxsupervisor, news, about, contact, tuner")
