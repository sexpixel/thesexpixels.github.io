# Per-reel crop for the full-screen players (Resolve-style), so text burned into a reel's
# black bars never clashes with the page headings. Values are percent of the frame.
# fill=False (default) is a plain crop: edges go black. fill=True zooms the cropped picture to cover the screen.
# Set these with the tuning page at thesexpixels.com/tuner/.
# "vimeo:ID" : dict(top=0, bottom=0, left=0, right=0, fill=False),
CROPS = {
    "youtube:9KZPd8__8ys": dict(top=13.7, bottom=0, left=0, right=0, fill=False),  # VFX supervisor showreel (stand-in), set by Mark 12 Oct 2026
    "vimeo:389670596": dict(top=12, bottom=0, left=0, right=0, fill=False),  # Showreel 2020 (The Fleapit), set by Mark 12 Oct 2026
}

def crop_of(spec):
    return CROPS.get(spec)

def crop_str(spec):
    c = crop_of(spec)
    if not c: return ""
    return ",".join(str(c.get(k, 0)) for k in ("top", "bottom", "left", "right")) + "," + ("1" if c.get("fill", False) else "0")
