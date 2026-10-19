# Skills page = CV page 2, "Skills by discipline": compositing, 15 disciplines in 5 stages.
# Keep this in step with the CV (Open to Work Relaunch canvas, CV page 2). Edit here, then run build.py.
#
# Each card: slug (its address: thesexpixels.com/skills/#slug), title, points, credits, and demo.
# demo = None  -> the card is locked: greyed, "In development", no link.
# demo = "vimeo:ID" / "vimeo:ID:HASH" / "youtube:ID" / "/path/" -> the card unlocks and opens its demo.
# Card images: assets/skills/NN.jpg (the strips from the CV).

TITLE_LEDE = ("Compositing in 15 disciplines and 5 stages, the same as page 2 of my CV. "
              "Each card opens a demo of that skill when it is ready; greyed cards are still in development.")

STAGES = [
    ("01", "Clean the plate", [
        dict(slug="prep-cleanup", title="Prep & cleanup",
             points=["Rig, wire and marker removal", "Crew, boom and reflection removal", "Sign, logo and text removal",
                     "General paint fixes", "Body reshaping and digital slimming", "Beauty work — skin and blemishes"],
             credits="Damsel · Poldark S5", demo=None),
        dict(slug="roto-segmentation", title="Roto & segmentation",
             points=["Hero character isolation", "Fine-detail and hair roto", "Garbage and holdout mattes", "Roto for FX holdouts",
                     "Roto for DMP integration", "AI-assisted segmentation and matte QA"],
             credits="The Ballad of a Small Player", demo=None),
        dict(slug="ai-assisted-comp", title="AI-assisted comp",
             points=["Normal and depth map extraction", "Clean-up and object removal", "Face replacement",
                     "Geometry extraction from plates", "Camera tracking via computer vision", "CopyCat training in Nuke", "ComfyUI and LTX Studio workflows"],
             credits="ComfyUI · LTX Studio · NukeGeoTools", demo=None),
    ]),
    ("02", "Solve the plate", [
        dict(slug="tracking-matchmove", title="Tracking & matchmove",
             points=["3D camera tracking", "2D and point tracking", "Object tracking", "Corner pinning",
                     "Clean plate reprojection", "Rolling shutter", "SmartVector"],
             credits="Gangs of London S3 · The Rig", demo=None),
        dict(slug="keying-extraction", title="Keying & extraction",
             points=["Blue and green screen keying", "Core / edge matte separation", "Despill",
                     "Edge refinement", "Hair and fur preservation", "Multi-key"],
             credits="The Crown S2 · Captain Marvel", demo=None),
        dict(slug="plate-reconstruction", title="Plate reconstruction",
             points=["Clean plate generation", "Patch, rebuild and restoration", "Camera and set extension cleanup",
                     "Multi-frame reconstruction", "Projection-based repair", "Prepping plates for comp"],
             credits="The Ballad of a Small Player", demo=None),
    ]),
    ("03", "Build the shot", [
        dict(slug="environments-dmp", title="Environments, 3D & USD",
             points=["Set extensions", "Projection mapping (3D / 2.5D)", "Nuke 3D (USD) camera projection", "USD scene assembly in Nuke",
                     "Photo-modelling and scan geometry", "Matte painting integration", "Multi-plane and parallax builds", "Sky replacements"],
             credits="The Buccaneers · Great Expectations · NukeGeoTools", demo=None),
        dict(slug="cg-aov-integration", title="CG & AOV integration",
             points=["Multi-pass assembly", "AOV rebuilds", "Creature and vehicle integration", "Lighting matched from on-set HDRI and ball refs",
                     "Holdouts, light wraps and refractions", "Re-lighting in Nuke", "Render plate balancing"],
             credits="Guardians of the Galaxy · Captain Marvel", demo=None),
        dict(slug="deep-compositing", title="Deep compositing",
             points=["Deep compositing and multi-depth layers", "Deep holdouts and merges", "Depth, AO and world-position passes",
                     "Deep data from Nuke and Katana", "Depth-ordered atmospherics", "Deep-to-2D flattening"],
             credits="Walking With Dinosaurs", demo=None),
    ]),
    ("04", "Shape the look", [
        dict(slug="camera-lens", title="Camera & lens work",
             points=["Bokeh and defocus", "Flare matching", "Lens distortion / undistortion", "Lens grids and camera data from set",
                     "Plate stabilisation", "Overscan and reframing", "STMap reprojection"],
             credits="Tenet · The French Dispatch", demo=None),
        dict(slug="fx-elements", title="FX element integration",
             points=["FX simulation pass comp", "Practical fire, smoke and sparks", "Library elements",
                     "Muzzle flashes and explosions", "Heat waves", "Contact shadows"],
             credits="Black Sails S4 · Lost in Space S2", demo=None),
        dict(slug="creative-fx", title="Creative & experimental FX",
             points=["Time warping and echo effects", "Procedural comp FX via gizmos", "Stylised and non-photoreal looks",
                     "Music video and promo FX", "Titles"],
             credits="Klaxons ‘Twin Flames’ UKMVA · M.I.A. ‘Borders’ · Coldplay ‘Daddy’", demo=None),
    ]),
    ("05", "Finish the shot", [
        dict(slug="lookdev-finishing", title="Lookdev & shot finishing",
             points=["ACES / OCIO", "Colour matching and balancing", "Day-for-night",
                     "Grain matching and regrain", "Motion blur consistency", "Sequence grade matching"],
             credits="Yardie · Murder Is Easy", demo=None),
        dict(slug="stereo-immersive", title="Stereo & immersive",
             points=["Mono-to-stereo conversion", "Stereo eye matching", "Stereo grading", "Ghosting fixes",
                     "Z-depth repair", "Depth maps", "360 comp passes", "Immersive video tests"],
             credits="Hugo · Save The 365th Day", demo=None),
        dict(slug="nuke-tools", title="Nuke tools & scripting",
             points=["Agentic coding — all tool development", "Custom gizmos and NDK plugins", "Python / TCL development", "Nuke script templating",
                     "EXR / DPX delivery specs", "RV and Syncsketch review"],
             credits="NukeGeoTools", demo=None),
    ]),
]
