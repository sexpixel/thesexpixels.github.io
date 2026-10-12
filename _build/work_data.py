# Work: professional jobs only (Nuke compositor, VFX supervisor, PostVis). Personal projects go on The Fleapit.
# Each project: title, role label as credited, role group (filter), format (filter), company, year or "".
# A project's reels go in clips=[("clip name", "vimeo id"), ...]; each clip becomes its own playable tile.
ROLE_GROUPS = ["Nuke compositor", "VFX supervisor", "PostVis", "Director"]
FORMATS = ["Feature film", "Episodic", "PostVis", "Shorts", "Feature animation"]
FORMAT_SLUGS = {"Feature film": "feature-film", "Episodic": "episodic", "PostVis": "postvis", "Shorts": "shorts", "Feature animation": "feature-animation"}
PROJECTS = [
    dict(title="Gangs of London S4", role="On-set VFX supervisor", group="VFX supervisor", fmt="Episodic", co="The Sex Pixels", yr="2026"),
    dict(title="Salomon", role="On-set supervision and comp", group="VFX supervisor", fmt="Shorts", co="", yr="2025"),
    dict(title="Rogue Trooper", role="Senior compositor", group="Nuke compositor", fmt="Feature film", co="Liberty Films · Netflix", yr="2025"),
    dict(title="The Ballad of a Small Player", role="VFX supervisor", group="VFX supervisor", fmt="Feature film", co="Netflix", yr="",
         clips=[("Official trailer", "youtube:z1B5W55TFyo"), ("Behind the scenes", "youtube:FGYPLc8bB9E")]),
    dict(title="Gangs of London S3", role="On-set VFX supervisor", group="VFX supervisor", fmt="Episodic", co="", yr=""),
    dict(title="Panda Plan", role="VFX supervisor", group="VFX supervisor", fmt="Feature film", co="Horizon VFX", yr=""),
    dict(title="I Am Nobody S2", role="VFX consultant", group="VFX supervisor", fmt="Episodic", co="Horizon VFX", yr=""),
    dict(title="Spotify", role="Director", group="Director", fmt="Shorts", co="The Sex Pixels", yr="",
         clips=[("Happy Ending", "143586386"), ("Run Your Way", "143586363"), ("Procrastinator", "143586362")]),
    dict(title="Zinga Poker", role="Compositor", group="Nuke compositor", fmt="Shorts", co="ICHI Worldwide", yr="2024"),
    dict(title="Damsel", role="Lead PostVis artist", group="PostVis", fmt="Feature film", co="Proof", yr="2023",
         clips=[("The Knights Arrive", "1014291965"), ("The Knights: Rashomon", "1014291669"), ("The Fall", "1014291582")]),
    dict(title="The Family Plan", role="Lead PostVis artist", group="PostVis", fmt="Feature film", co="Proof", yr="2023",
         clips=[("The Tiki Bar Attack", "1014294324"), ("Car Pool Karaoke", "1014294008")]),
    dict(title="Wonka", role="PostVis", group="PostVis", fmt="Feature film", co="Framestore FPS", yr="",  # ROLE TO CONFIRM
         clips=[("Giraffe, parts 1 & 2", "1014150213"), ("Giraffe, part 3", "1014149873")]),
    dict(title="Guardians of the Galaxy Vol. 3", role="Lead PostVis artist", group="PostVis", fmt="Feature film", co="Framestore FPS", yr="",
         clips=[("Guardians of the Galaxy Vol. 3", "1014147480")]),
    dict(title="Moon Knight", role="PostVis", group="PostVis", fmt="Episodic", co="Framestore FPS", yr="",  # ROLE TO CONFIRM
         clips=[("The Castle", "1014146296"), ("The Ice Cream Van Chase", "1014145891"), ("The Book Attack", "1014145603"), ("The Museum", "1014145227"),
                ("Security Desk", "1014145040"), ("Storage Lockup", "1014144960"), ("Khonshu Mentors", "1014144736"),
                ("Pyramid Fight", "1014144315"), ("Desert Magic", "1014144015"), ("The Asylum", "1014143259"), ("The Realm", "1014143091")]),
    dict(title="Lockwood & Co", role="PostVis", group="PostVis", fmt="Episodic", co="Framestore FPS", yr="",  # ROLE TO CONFIRM
         clips=[("S01E03 The Druids", "1014146695")]),
    dict(title="The Rig", role="", group="Nuke compositor", fmt="Episodic", co="Absolute Post", yr="",  # ROLE TO CONFIRM
         clips=[("Season 1", "1014300271")]),
    dict(title="The Buccaneers", role="", group="Nuke compositor", fmt="Episodic", co="Absolute Post", yr="",  # ROLE TO CONFIRM
         clips=[("S01E01 The Prairie Trail", "1014151720"), ("S01E01 The Wedding", "1014151499")]),
    dict(title="1899", role="PostVis artist", group="PostVis", fmt="Episodic", co="Framestore FPS", yr=""),
    dict(title="The Little Mermaid", role="PostVis artist", group="PostVis", fmt="Feature film", co="Framestore FPS", yr=""),
    dict(title="Walking With Dinosaurs", role="Compositor", group="Nuke compositor", fmt="Episodic", co="Milk VFX", yr=""),
    dict(title="Tenet", role="Senior compositor", group="Nuke compositor", fmt="Feature film", co="DNEG", yr=""),
    dict(title="Captain Marvel", role="Senior compositor", group="Nuke compositor", fmt="Feature film", co="Trixter", yr=""),
    dict(title="The Crown S2", role="Compositor", group="Nuke compositor", fmt="Episodic", co="", yr=""),
    dict(title="Save The 365th Day", role="Stereo compositor & stereographer", group="Nuke compositor", fmt="Feature animation", co="ECCG China", yr="2012",
         clips=[("Trailer", "55357193"), ("Excerpt", "75682310")]),
    dict(title="Game of Thrones S6", role="In-house VFX supervision team", group="VFX supervisor", fmt="Episodic", co="Molinare", yr=""),
]


def expand(p):
    """One tile per clip; a project with no clips stays one 'coming soon' tile."""
    if not p.get("clips"):
        return [p]
    out = []
    for name, vid in p["clips"]:
        q = dict(p)
        q["title"] = p["title"] if name == p["title"] else f"{p['title']} · {name}"
        if vid.startswith("youtube:"):
            q["video"] = vid; q["url"] = f"https://youtu.be/{vid[8:]}"
        else:
            q["video"] = f"vimeo:{vid}"; q["url"] = f"https://vimeo.com/{vid}"
        out.append(q)
    return out


def in_format(p, f):
    """PostVis is its own format page, gathering every PostVis job; those jobs also stay on their
    Feature film or Episodic page."""
    return p["group"] == "PostVis" if f == "PostVis" else p["fmt"] == f
