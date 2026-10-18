# Services page content (from Mark's "Services & Skills mockups" canvas, 18 Oct 2026).
# LIVE = False keeps the page a draft: the build writes it to _mock/services/ (never published, not in the menu).
# Set LIVE = True when Mark says "open Services": the page is written to /services/ and added to the menu.
LIVE = False
# While not LIVE, the page is also published at this unlisted address so Mark can see it on the real site.
# Not in the menu, noindex, but anyone given the address can open it. Set to None to take it down.
PREVIEW_PATH = "services-g1kaq0"

LEDE = "From the first draft of the script to the final deliverable. Six phases of production, supervised by one person who has worked in each of them."

# Each phase: number, name, one-line summary (overview card), intro, services, side notes.
# A service ending in " *" is shown with an "In development" tag.
PHASES = [
    dict(slug="development", name="Development",
         line="Scriptwriting, script breakdowns, boards and animatics.",
         intro="Getting the story, and its visual effects, right on the page before money is spent.",
         items=["Scriptwriting", "Script breakdowns for VFX", "Bid input and feasibility", "Storyboards and animatics *"],
         notes=[("Background", "MA Screenwriting, Falmouth · Staff writer — MTV, NBC Superchannel")]),
    dict(slug="pre-production", name="Pre-Production",
         line="Visualisation and planning in Unreal Engine.",
         intro="Building on the script in Unreal Engine, so the shoot is planned and the shots are understood before anyone is on set.",
         items=["Visualisation — previs, techvis, pitchvis *", "Virtual scouting *", "VFX methodology definition", "Postvis direction"],
         notes=[("Related", "Framestore FPS — Lead PostVis · Proof — Damsel, The Family Plan · Unreal Fellowship, Epic Games · Playmaker")]),
    dict(slug="production", name="Production",
         line="On-set supervision and data capture.",
         intro="On-set VFX supervision, and capturing every piece of data that post will need.",
         items=["On-set decision making", "Director and DP liaison", "HDRI, chrome and grey ball capture", "LIDAR",
                "Witness camera arrays", "360 / lat-long capture", "Lens and camera data", "Marker strategy"],
         notes=[("Kit", "iPhone 17 Log · Theta 360 · 15× GoPro array · Canon 5D MkII · grey / chrome ball rig"),
                ("Related", "Gangs of London S3 & S4 · The Ballad of a Small Player, dir. Edward Berger")]),
    dict(slug="production-wrap", name="Production Wrap",
         line="Processing set data for the VFX team.",
         intro="Turning what was captured on set into data a VFX team can use on day one.",
         items=["VFX data wrangling", "Camera and lens metadata", "Photo-modelling and scan geometry", "Gaussian splatting",
                "360 / lat-long processing", "USD scene assembly", "Vendor handover packages"],
         notes=[("Tools", "Assimilate Scratch · CaraVR · Kartaverse · Modo · Mari"),
                ("Related", "[Production] · [Production]")]),
    dict(slug="post-production", name="Post Production",
         line="Compositing and VFX supervision.",
         intro="Nuke compositing and VFX supervision, through dailies to final shot sign-off.",
         items=["VFX supervision", "Dailies leadership", "Sequence continuity", "Final shot sign-off", "Client review",
                "Mentoring artists and comp leads"],
         skills_link=True,
         notes=[("Related", "Panda Plan — VFX Supervisor · I Am Nobody S2 — VFX Consultant · Rogue Trooper — Senior Compositor · Tenet — Senior Compositor")]),
    dict(slug="delivery", name="Delivery & Distribution",
         line="DCP, conforms, social and awards.",
         intro="Getting the finished work out — to cinema, to broadcast and to social.",
         items=["Editorial turnovers and change lists", "EDL / AAF conform and VFX pulls", "Sequence QC", "DCP production",
                "Formats for Instagram and social", "Breakdown and show-and-tell reels", "Oscar and BAFTA submission prep"],
         notes=[("Related", "Absolute Post — deliveries across eight shows · The Fleapit — Instagram")]),
]

ACROSS = [
    ("Formats", "feature film, episodic / streaming, commercial, animation feature, virtual production / LED stage. Worked across the UK, Ireland, Germany, Sweden, Macau and China."),
    ("Pipeline", "AYON, Deadline and USD, built and run in-house at The Sex Pixels."),
]
