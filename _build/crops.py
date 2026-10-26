# Per-reel crop for the full-screen players (Resolve-style), so text burned into a reel's
# black bars never clashes with the page headings. Values are percent of the frame.
# fill=False (default) is a plain crop: edges go black. fill=True zooms the cropped picture to cover the screen.
# Set these with the tuning page at thesexpixels.com/tuner/.
# "vimeo:ID" : dict(top=0, bottom=0, left=0, right=0, fill=False),
CROPS = {
    "youtube:9KZPd8__8ys": dict(top=13.7, bottom=0, left=0, right=0, fill=False),  # Gangs of London S4 official teaser (VFX Supervisor page), set by Mark 12 Oct 2026
    "vimeo:389670596": dict(top=12, bottom=0, left=0, right=0, fill=False),  # Showreel 2020 (The Fleapit), set by Mark 12 Oct 2026
    "youtube:F7eMXvvaQgQ": dict(top=23.7, bottom=23.7, left=12.5, right=12.5, fill=True),  # Ou Est Le Swimming Pool: a 4:3 480p frame (pillarboxed in the 16:9 player) with a ~2.5:1 picture inside; crop to the picture and fill the width (measured from Mark's screenshot, 26 Oct 2026)
}

# Fade in and out, in seconds: a black veil and the sound ramp over that time. For "youtube:ID:START:END"
# stretches the fade sits outside the points: fade in ends at START, fade out starts at END.
FADES = {
    "youtube:NSJe0wIv718:30:74": (5, 2),  # (in, out) seconds; a single number sets both. Guardians of the Galaxy · Prison Break, asked by Mark 26 Oct 2026
}

# Reels that can't play inside the site (e.g. age-restricted on YouTube): the tile links out to the video
# instead, and the player skips it.
LINK_ONLY = {
    "youtube:umS0sw8_D30",  # Klaxons · Twin Flames: age-restricted on YouTube, so it can't be embedded (Mark, 26 Oct 2026)
}

def crop_of(spec):
    return CROPS.get(spec)

def crop_str(spec):
    c = crop_of(spec)
    if not c: return ""
    return ",".join(str(c.get(k, 0)) for k in ("top", "bottom", "left", "right")) + "," + ("1" if c.get("fill", False) else "0")
