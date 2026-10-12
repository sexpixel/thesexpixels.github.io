# Per-reel crop for the full-screen players, so text burned into a reel's black bars
# sits off screen and never clashes with the page headings.
# video spec -> (zoom, shift). zoom 1.00 = no crop; shift moves the picture up (-) or down (+)
# as a percentage of its height. Set these with the tuning page at thesexpixels.com/tuner/.
CROPS = {
}

def crop_of(spec):
    return CROPS.get(spec)
