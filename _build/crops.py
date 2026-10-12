# Per-reel crop for the full-screen players (Resolve-style), so text burned into a reel's
# black bars never clashes with the page headings. Values are percent of the frame.
# fill=False (default) is a plain crop: edges go black. fill=True zooms the cropped picture to cover the screen.
# Set these with the tuning page at thesexpixels.com/tuner/.
# "vimeo:ID" : dict(top=0, bottom=0, left=0, right=0, fill=False),
CROPS = {
}

def crop_of(spec):
    return CROPS.get(spec)

def crop_str(spec):
    c = crop_of(spec)
    if not c: return ""
    return ",".join(str(c.get(k, 0)) for k in ("top", "bottom", "left", "right")) + "," + ("1" if c.get("fill", False) else "0")
