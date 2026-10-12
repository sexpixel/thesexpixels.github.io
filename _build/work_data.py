# Work: professional jobs only (Nuke compositor, VFX supervisor, PostVis). Personal projects go on The Fleapit.
# Each project: title, role label as credited, role group (filter), format (filter), company, year or "".
# A project gets a reel by adding video="vimeo:ID:HASH" (and url=...) to its dict.
ROLE_GROUPS = ["Nuke compositor", "VFX supervisor", "PostVis"]
FORMATS = ["Film", "Episodic", "Commercials", "Feature animation"]
PROJECTS = [
    dict(title="Gangs of London S4", role="On-set VFX supervisor", group="VFX supervisor", fmt="Episodic", co="The Sex Pixels", yr="2026"),
    dict(title="Salomon", role="On-set supervision and comp", group="VFX supervisor", fmt="Commercials", co="", yr="2025"),
    dict(title="Rogue Trooper", role="Senior compositor", group="Nuke compositor", fmt="Film", co="Liberty Films · Netflix", yr="2025"),
    dict(title="The Ballad of a Small Player", role="VFX supervisor", group="VFX supervisor", fmt="Film", co="Netflix", yr=""),
    dict(title="Gangs of London S3", role="On-set VFX supervisor", group="VFX supervisor", fmt="Episodic", co="", yr=""),
    dict(title="Panda Plan", role="VFX supervisor", group="VFX supervisor", fmt="Film", co="Horizon VFX", yr=""),
    dict(title="I Am Nobody S2", role="VFX consultant", group="VFX supervisor", fmt="Episodic", co="Horizon VFX", yr=""),
    dict(title="Zinga Poker", role="Compositor", group="Nuke compositor", fmt="Commercials", co="ICHI Worldwide", yr="2024"),
    dict(title="Damsel", role="Lead PostVis artist", group="PostVis", fmt="Film", co="Proof", yr="2023"),
    dict(title="Guardians of the Galaxy Vol. 3", role="Lead PostVis artist", group="PostVis", fmt="Film", co="Framestore FPS", yr=""),
    dict(title="1899", role="PostVis artist", group="PostVis", fmt="Episodic", co="Framestore FPS", yr=""),
    dict(title="The Little Mermaid", role="PostVis artist", group="PostVis", fmt="Film", co="Framestore FPS", yr=""),
    dict(title="Walking With Dinosaurs", role="Compositor", group="Nuke compositor", fmt="Episodic", co="Milk VFX", yr=""),
    dict(title="Tenet", role="Senior compositor", group="Nuke compositor", fmt="Film", co="DNEG", yr=""),
    dict(title="Captain Marvel", role="Senior compositor", group="Nuke compositor", fmt="Film", co="Trixter", yr=""),
    dict(title="The Crown S2", role="Compositor", group="Nuke compositor", fmt="Episodic", co="", yr=""),
    dict(title="Game of Thrones S6", role="In-house VFX supervision team", group="VFX supervisor", fmt="Episodic", co="Molinare", yr=""),
]
