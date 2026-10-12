# Per-reel crop for the full-screen players (Resolve-style), so text burned into a reel's
# black bars never clashes with the page headings. Values are percent of the frame.
# fill=True scales the cropped picture up to cover the screen; False leaves the edges black.
# Set these with the tuning page at thesexpixels.com/tuner/.
# "vimeo:ID" : dict(top=0, bottom=0, left=0, right=0, fill=True),
CROPS = {
}

def crop_of(spec):
    return CROPS.get(spec)

def crop_str(spec):
    c = crop_of(spec)
    if not c: return ""
    return ",".join(str(c.get(k, 0)) for k in ("top", "bottom", "left", "right")) + "," + ("1" if c.get("fill", True) else "0")
