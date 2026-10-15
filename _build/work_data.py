# Work: professional jobs only (Nuke compositor, VFX supervisor, PostVis). Personal projects go on The Fleapit.
# Each project: title, role label as credited, role group (filter), format (filter), company, year or "".
# A project's reels go in clips=[("clip name", "vimeo id"), ...]; each clip becomes its own playable tile.
ROLE_GROUPS = ["Nuke compositor", "VFX supervisor", "PostVis", "Director"]
FORMATS = ["Feature film", "Episodic", "Visualisation", "Shorts", "Feature animation"]
FORMAT_SLUGS = {"Feature film": "feature-film", "Episodic": "episodic", "Visualisation": "visualisation", "Shorts": "shorts", "Feature animation": "feature-animation"}
PROJECTS = [
    dict(title="Gangs of London S4", role="On-set VFX supervisor", group="VFX supervisor", fmt="Episodic", co="The Sex Pixels", yr="2026", phases=["Pre-production", "Production"]),
    dict(title="Salomon", role="On-set supervision and comp", group="VFX supervisor", fmt="Shorts", co="", yr="2025",
         clips=[("XT-Whisper · Sportstyle", "youtube:UeRKN7WWE0c", ["Production", "Post-production"])]),
    dict(title="Rogue Trooper", role="Senior compositor", group="Nuke compositor", fmt="Feature film", co="Liberty Films · Netflix", yr="2025"),
    dict(title="The Ballad of a Small Player", role="VFX supervisor", group="VFX supervisor", fmt="Feature film", co="Netflix", yr="",
         clips=[("Official trailer", "youtube:z1B5W55TFyo", ["Distribution"]), ("Behind the scenes", "youtube:FGYPLc8bB9E", ["Production"])]),
    dict(title="Gangs of London S3", role="On-set VFX supervisor", group="VFX supervisor", fmt="Episodic", co="", yr=""),
    dict(title="Panda Plan", role="VFX supervisor", group="VFX supervisor", fmt="Feature film", co="Horizon VFX", yr=""),
    dict(title="I Am Nobody S2", role="VFX consultant", group="VFX supervisor", fmt="Episodic", co="Horizon VFX", yr=""),
    dict(title="Spotify", role="Director", group="Director", fmt="Shorts", co="The Sex Pixels", yr="",
         clips=[("Happy Ending", "143586386"), ("Run Your Way", "143586363"), ("Procrastinator", "143586362")]),
    # Music videos, clean copies on YouTube (added 15 Oct 2026). credits from Mark 15 Oct; newest first.
    dict(title="London Grammar", role="VFX supervisor", group="VFX supervisor", fmt="Shorts", co="Phink", yr="2013",
         clips=[("Nightcall", "youtube:OZYw0MQp_fI")]),
    dict(title="Little Nikki", role="VFX supervisor", group="VFX supervisor", fmt="Shorts", co="The Sex Pixels", yr="2013",
         clips=[("Little Nikki Says", "youtube:xSW3vtpHOak")]),
    dict(title="Ou Est Le Swimming Pool", role="VFX supervisor and compositor", group="VFX supervisor", fmt="Shorts", co="", yr="",
         clips=[("Jackson's Last Stand", "youtube:F7eMXvvaQgQ")]),
    dict(title="Klaxons", role="Compositor", group="Nuke compositor", fmt="Shorts", co="Blind Pig", yr="2010",
         clips=[("Twin Flames", "youtube:umS0sw8_D30")]),
    dict(title="Reel 2 Real ft. The Mad Stuntman", role="VFX supervisor", group="VFX supervisor", fmt="Shorts", co="The Sex Pixels", yr="2010",
         clips=[("I Like To Move It", "youtube:2z2D7AYlSuw")]),
    # Promax Gold 1996, Best Corporate Promo. Cut from the TVC/promo anthology (SD original, 1995), uploaded 15 Oct 2026.
    dict(title="VH-1", role="Director", group="Director", fmt="Shorts", co="", yr="1995",
         clips=[("Nobody Does It Better", "1236267195")]),
    # Zinga Poker (Compositor · ICHI Worldwide · 2024): reel unavailable, tile removed 13 Oct at Mark's request. Credit kept for the CV.
    # dict(title="Zinga Poker", role="Compositor", group="Nuke compositor", fmt="Shorts", co="ICHI Worldwide", yr="2024"),
    dict(title="Damsel", role="Lead PostVis artist", group="PostVis", fmt="Feature film", co="Proof", yr="2023",
         clips=[("The Knights Arrive", "1014291965"), ("The Knights: Rashomon", "1014291669"), ("The Fall", "1014291582")]),
    dict(title="The Family Plan", role="Lead PostVis artist", group="PostVis", fmt="Feature film", co="Proof", yr="2023",
         clips=[("The Tiki Bar Attack", "1014294324"), ("Car Pool Karaoke", "1014294008")]),
    dict(title="Wonka", role="Lead PostVis artist", group="PostVis", fmt="Feature film", co="Framestore FPS", yr="",
         clips=[("Giraffe, parts 1 & 2", "1014150213"), ("Giraffe, part 3", "1014149873")]),
    dict(title="Guardians of the Galaxy Vol. 3", role="Lead PostVis artist", group="PostVis", fmt="Feature film", co="Framestore FPS", yr="",
         clips=[("Guardians of the Galaxy Vol. 3", "1014147480")]),
    dict(title="Moon Knight", role="Lead PostVis artist", group="PostVis", fmt="Episodic", co="Framestore FPS", yr="",
         clips=[("The Castle", "1014146296"), ("The Ice Cream Van Chase", "1014145891"), ("The Book Attack", "1014145603"), ("The Museum", "1014145227"),
                ("Security Desk", "1014145040"), ("Storage Lockup", "1014144960"), ("Khonshu Mentors", "1014144736"),
                ("Pyramid Fight", "1014144315"), ("Desert Magic", "1014144015"), ("The Asylum", "1014143259"), ("The Realm", "1014143091")]),
    dict(title="Lockwood & Co", role="Lead PostVis artist", group="PostVis", fmt="Episodic", co="Framestore FPS", yr="",
         clips=[("S01E03 The Druids", "1014146695")]),
    dict(title="The Rig", role="", group="Nuke compositor", fmt="Episodic", co="Absolute Post", yr="",  # ROLE TO CONFIRM
         clips=[("Season 1", "1014300271")]),
    dict(title="The Buccaneers", role="", group="Nuke compositor", fmt="Episodic", co="Absolute Post", yr="",  # ROLE TO CONFIRM
         clips=[("S01E01 The Prairie Trail", "1014151720"), ("S01E01 The Wedding", "1014151499")]),
    dict(title="1899", role="PostVis artist", group="PostVis", fmt="Episodic", co="Framestore FPS", yr="",
         clips=[("S01E07 The Storm pt 1", "1014139706")]),
    dict(title="The Little Mermaid", role="PostVis artist", group="PostVis", fmt="Feature film", co="Framestore FPS", yr=""),
    dict(title="Walking With Dinosaurs", role="Compositor", group="Nuke compositor", fmt="Episodic", co="Milk VFX", yr=""),
    dict(title="Tenet", role="Senior compositor", group="Nuke compositor", fmt="Feature film", co="DNEG", yr=""),
    dict(title="Captain Marvel", role="Senior compositor", group="Nuke compositor", fmt="Feature film", co="Trixter", yr=""),
    dict(title="The Crown S2", role="Compositor", group="Nuke compositor", fmt="Episodic", co="", yr=""),
    dict(title="Save The 365th Day", role="Stereographer", group="Nuke compositor", fmt="Feature animation", co="ECCG China", yr="2012",
         clips=[("Trailer", "55357193", ["Distribution"]), ("Excerpt", "75682310", ["Post-production"])]),
    dict(title="Game of Thrones S6", role="In-house VFX supervision team", group="VFX supervisor", fmt="Episodic", co="Molinare", yr=""),
]


def expand(p):
    """One tile per clip; a project with no clips stays one 'coming soon' tile."""
    if not p.get("clips"):
        return [dict(p, phases=phases_of(p))]
    p = dict(p, phases=phases_of(p))
    out = []
    for clip in p["clips"]:
        name, vid = clip[0], clip[1]
        q = dict(p)
        if len(clip) > 2: q["phases"] = clip[2]
        q["title"] = p["title"] if name == p["title"] else f"{p['title']} · {name}"
        if vid.startswith("youtube:"):
            q["video"] = vid; q["url"] = f"https://youtu.be/{vid[8:]}"
        else:
            q["video"] = f"vimeo:{vid}"; q["url"] = f"https://vimeo.com/{vid}"
        out.append(q)
    return out


def in_format(p, f):
    """Visualisation is its own format page, gathering every PostVis job; those jobs also stay on their
    Feature film or Episodic page."""
    return p["group"] in ("PostVis", "Previs") if f == "Visualisation" else p["fmt"] == f


# Production phases (from the Indie Film Production Roadmap). DRAFT tags for Mark to check.
PHASES = ["Development", "Pre-production", "Production", "Post-production", "Distribution"]
GROUP_PHASES = {
    "Nuke compositor": ["Post-production"],
    "PostVis": ["Post-production"],
    "Previs": ["Pre-production"],   # previs jobs: group="Previs" (they also appear on the Visualisation page)
    "VFX supervisor": ["Pre-production", "Production", "Post-production"],
    "Director": PHASES,
}
def phases_of(p):
    """A project's phases: its own list if set, otherwise its role group's."""
    return p.get("phases") or GROUP_PHASES.get(p.get("group"), ["Post-production"])
